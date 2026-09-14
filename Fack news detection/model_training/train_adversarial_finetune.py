"""
Fine-tuning and Robustness Training Pipeline with Adversarial Data Augmentation.
Fine-tunes the pre-trained RoBERTa model ('jy46604790/Fake-News-Bert-Detect') and
the Scikit-Learn baseline on an augmented dataset with oversampled adversarial examples:
1. Real-but-unusual news stories
2. Fake-but-well-cited institutional spoofed claims
"""

import os
import sys
import argparse
import numpy as np
import pandas as pd
import torch
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    pipeline
)
from datasets import Dataset

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
ADVERSARIAL_CSV = os.path.join(SCRIPT_DIR, "adversarial_examples.csv")
SAVED_MODEL_DIR = os.path.join(PROJECT_ROOT, "backend", "model", "saved_model")
FINETUNED_MODEL_DIR = os.path.join(PROJECT_ROOT, "finetuned_model")
BASELINE_JOB_PATH = os.path.join(SAVED_MODEL_DIR, "baseline_model.joblib")

os.makedirs(SAVED_MODEL_DIR, exist_ok=True)
os.makedirs(FINETUNED_MODEL_DIR, exist_ok=True)


def load_augmented_dataset(adversarial_oversample_factor: int = 10) -> pd.DataFrame:
    """Loads base Kaggle datasets (if present) and merges with oversampled adversarial examples."""
    fake_csv = os.path.join(PROJECT_ROOT, "Fake.csv")
    true_csv = os.path.join(PROJECT_ROOT, "True.csv")

    base_dfs = []
    if os.path.exists(fake_csv) and os.path.exists(true_csv):
        print("Loading base Kaggle datasets...")
        df_fake = pd.read_csv(fake_csv, nrows=1000)
        df_true = pd.read_csv(true_csv, nrows=1000)
        df_fake["label"] = 0
        df_true["label"] = 1
        base_df = pd.concat([
            df_fake[["text", "label"]].dropna(),
            df_true[["text", "label"]].dropna()
        ], ignore_index=True)
        base_dfs.append(base_df)
    else:
        print("Base Kaggle CSVs not found in root; using synthetic standard base corpus...")
        standard_samples = [
            {"text": "The United Nations General Assembly opened its annual autumn session in New York to debate climate financing.", "label": 1},
            {"text": "Federal Reserve officials voted to maintain interest rates within current target ranges following labor reports.", "label": 1},
            {"text": "SHOCKING TRUTH: Elites put secret mind-control frequencies into microwave ovens to control election outcomes!", "label": 0},
            {"text": "Miracle cure revealed: Drinking hot boiled water and ginger instantly destroys all cardiovascular illness!", "label": 0}
        ] * 50
        base_dfs.append(pd.DataFrame(standard_samples))

    if not os.path.exists(ADVERSARIAL_CSV):
        raise FileNotFoundError(f"Adversarial examples not found at {ADVERSARIAL_CSV}. Run generate_adversarial_dataset.py first.")

    df_adversarial = pd.read_csv(ADVERSARIAL_CSV).dropna()
    print(f"Loaded {len(df_adversarial)} unique adversarial samples.")

    # Oversample adversarial examples so the model learns the nuances
    df_adv_upsampled = pd.concat([df_adversarial] * adversarial_oversample_factor, ignore_index=True)
    print(f"Adversarial examples upsampled to {len(df_adv_upsampled)} records.")

    full_dataset = pd.concat(base_dfs + [df_adv_upsampled], ignore_index=True)
    full_dataset = full_dataset.sample(frac=1.0, random_state=42).reset_index(drop=True)
    print(f"Full augmented training dataset: {len(full_dataset)} total samples (Real: {(full_dataset['label']==1).sum()}, Fake: {(full_dataset['label']==0).sum()})")
    return full_dataset, df_adversarial


def train_baseline_model(full_dataset: pd.DataFrame, adversarial_test_df: pd.DataFrame):
    """Fine-tunes the baseline TF-IDF + Logistic Regression pipeline on the augmented data."""
    print("\n--- Training Augmented Scikit-Learn Baseline Model ---")
    train_df, val_df = train_test_split(full_dataset, test_size=0.15, random_state=42, stratify=full_dataset["label"])

    model = Pipeline([
        ("tfidf", TfidfVectorizer(max_features=15000, ngram_range=(1, 2), stop_words="english")),
        ("clf", LogisticRegression(C=2.5, max_iter=1000, solver="lbfgs"))
    ])

    model.fit(train_df["text"], train_df["label"])
    val_preds = model.predict(val_df["text"])
    val_acc = accuracy_score(val_df["label"], val_preds)
    print(f"Baseline Validation Accuracy: {val_acc * 100:.2f}%")

    # Evaluate on adversarial test subset
    adv_preds = model.predict(adversarial_test_df["text"])
    adv_acc = accuracy_score(adversarial_test_df["label"], adv_preds)
    print(f"Baseline Accuracy specifically on Hard Adversarial Subset: {adv_acc * 100:.2f}%")

    joblib.dump(model, BASELINE_JOB_PATH)
    print(f"Saved augmented baseline model to {BASELINE_JOB_PATH}")
    return model


def finetune_transformer(full_dataset: pd.DataFrame, adversarial_test_df: pd.DataFrame, epochs: int = 2):
    """Fine-tunes the RoBERTa Transformer model on the augmented dataset."""
    print("\n--- Fine-Tuning Transformer Model (jy46604790/Fake-News-Bert-Detect) ---")
    MODEL_NAME = "jy46604790/Fake-News-Bert-Detect"

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)

    train_df, val_df = train_test_split(full_dataset, test_size=0.15, random_state=42, stratify=full_dataset["label"])
    train_ds = Dataset.from_pandas(train_df[["text", "label"]])
    val_ds = Dataset.from_pandas(val_df[["text", "label"]])

    def tokenize_fn(batch):
        return tokenizer(batch["text"], padding="max_length", truncation=True, max_length=256)

    print("Tokenizing datasets...")
    train_ds = train_ds.map(tokenize_fn, batched=True)
    val_ds = val_ds.map(tokenize_fn, batched=True)

    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        preds = np.argmax(logits, axis=-1)
        acc = accuracy_score(labels, preds)
        precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average="binary")
        return {"accuracy": acc, "f1": f1, "precision": precision, "recall": recall}

    # Training Arguments
    training_args = TrainingArguments(
        output_dir=FINETUNED_MODEL_DIR,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=epochs,
        learning_rate=2e-5,
        logging_steps=20,
        eval_strategy="epoch",
        save_strategy="epoch",
        save_total_limit=1,
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        report_to="none"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        compute_metrics=compute_metrics
    )

    print("Starting fine-tuning...")
    trainer.train()

    print("Saving fine-tuned transformer and tokenizer...")
    trainer.save_model(FINETUNED_MODEL_DIR)
    tokenizer.save_pretrained(FINETUNED_MODEL_DIR)

    # Also copy to backend/model/saved_model/finetuned_model
    backend_save_dir = os.path.join(SAVED_MODEL_DIR, "finetuned_model")
    trainer.save_model(backend_save_dir)
    tokenizer.save_pretrained(backend_save_dir)
    print(f"Fine-tuned model saved to: {FINETUNED_MODEL_DIR} and {backend_save_dir}")

    # Evaluate on adversarial test dataset
    print("\n--- Evaluating Fine-Tuned Transformer on Hard Adversarial Subset ---")
    pipe = pipeline("text-classification", model=FINETUNED_MODEL_DIR, tokenizer=FINETUNED_MODEL_DIR, truncation=True, max_length=256)
    adv_texts = adversarial_test_df["text"].tolist()
    adv_labels = adversarial_test_df["label"].tolist()

    results = pipe(adv_texts)
    predicted_labels = [1 if r["label"] in ["LABEL_1", "Real", "real"] else 0 for r in results]

    acc = accuracy_score(adv_labels, predicted_labels)
    print(f"Post-Finetuning Accuracy on Hard Adversarial Examples: {acc * 100:.2f}%")
    print(classification_report(adv_labels, predicted_labels, target_names=["Fake (0)", "Real (1)"]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fine-tune on augmented adversarial dataset")
    parser.add_argument("--epochs", type=int, default=1, help="Number of fine-tuning epochs")
    parser.add_argument("--skip_transformer", action="store_true", help="Skip heavy transformer training and only train baseline")
    args = parser.parse_args()

    full_ds, adv_ds = load_augmented_dataset()
    train_baseline_model(full_ds, adv_ds)

    if not args.skip_transformer:
        finetune_transformer(full_ds, adv_ds, epochs=args.epochs)
