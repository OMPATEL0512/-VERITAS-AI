import os
import sys
import argparse
import numpy as np
import torch
from typing import Dict
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
    DataCollatorWithPadding,
    EarlyStoppingCallback
)
from datasets import Dataset

try:
    from model_training.preprocess import load_kaggle_dataset, split_data
except ImportError:
    from preprocess import load_kaggle_dataset, split_data


def compute_metrics(eval_pred) -> Dict[str, float]:
    """Computes evaluation metrics: Accuracy, F1, Precision, Recall."""
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, predictions, average="binary")
    acc = accuracy_score(labels, predictions)
    return {
        "accuracy": acc,
        "f1": f1,
        "precision": precision,
        "recall": recall
    }


def train(
    data_dir: str = "data",
    fake_csv: str = "Fake.csv",
    true_csv: str = "True.csv",
    model_name: str = "distilbert-base-uncased",
    output_dir: str = "backend/model/saved_model",
    epochs: int = 3,
    batch_size: int = 16,
    learning_rate: float = 2e-5,
    max_length: int = 256,
    sample_size: int = None
):
    fake_path = os.path.join(data_dir, fake_csv)
    true_path = os.path.join(data_dir, true_csv)

    print("==================================================")
    print(" Fake News Detection: DistilBERT Training Pipeline")
    print("==================================================")
    print(f"Device available: {'CUDA (GPU)' if torch.cuda.is_available() else 'CPU'}")
    print(f"Base Model: {model_name}")
    print(f"Output Directory: {output_dir}")

    # 1. Load Data
    df = load_kaggle_dataset(fake_path, true_path, sample_size=sample_size)
    X_train, X_val, y_train, y_val = split_data(df, test_size=0.2)

    # 2. Tokenizer
    print(f"Loading Tokenizer: {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    train_df = pd.DataFrame({"text": X_train.values, "label": y_train.values})
    val_df = pd.DataFrame({"text": X_val.values, "label": y_val.values})

    ds_train = Dataset.from_pandas(train_df)
    ds_val = Dataset.from_pandas(val_df)

    def tokenize_fn(batch):
        return tokenizer(batch["text"], truncation=True, max_length=max_length)

    print("Tokenizing datasets...")
    ds_train = ds_train.map(tokenize_fn, batched=True)
    ds_val = ds_val.map(tokenize_fn, batched=True)

    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    # 3. Model Architecture
    print(f"Instantiating {model_name} with binary sequence classification head...")
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        num_labels=2,
        id2label={0: "Fake", 1: "Real"},
        label2id={"Fake": 0, "Real": 1}
    )

    # 4. Training Arguments
    training_args = TrainingArguments(
        output_dir="./checkpoints",
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size * 2,
        warmup_ratio=0.1,
        weight_decay=0.01,
        learning_rate=learning_rate,
        logging_dir="./logs",
        logging_steps=50,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        greater_is_better=True,
        save_total_limit=2,
        fp16=torch.cuda.is_available(),
        report_to="none"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=ds_train,
        eval_dataset=ds_val,
        tokenizer=tokenizer,
        data_collator=data_collator,
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=2)]
    )

    # 5. Train
    print("Starting fine-tuning...")
    trainer.train()

    # 6. Evaluate
    print("\nRunning final validation evaluation...")
    eval_results = trainer.evaluate()
    print("Validation Results:")
    for k, v in eval_results.items():
        print(f"  {k}: {v:.4f}" if isinstance(v, float) else f"  {k}: {v}")

    # 7. Save Model & Tokenizer
    os.makedirs(output_dir, exist_ok=True)
    print(f"\nSaving fine-tuned model and tokenizer to '{output_dir}'...")
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    print("Saved successfully!")


if __name__ == "__main__":
    import pandas as pd
    parser = argparse.ArgumentParser(description="Fine-tune DistilBERT for Fake News Detection")
    parser.add_argument("--data_dir", type=str, default="data", help="Directory containing Fake.csv and True.csv")
    parser.add_argument("--fake_csv", type=str, default="Fake.csv", help="Filename of fake news CSV")
    parser.add_argument("--true_csv", type=str, default="True.csv", help="Filename of real news CSV")
    parser.add_argument("--output_dir", type=str, default="backend/model/saved_model", help="Directory to save fine-tuned model")
    parser.add_argument("--epochs", type=int, default=3, help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=16, help="Batch size")
    parser.add_argument("--lr", type=float, default=2e-5, help="Learning rate")
    parser.add_argument("--max_length", type=int, default=256, help="Max token sequence length")
    parser.add_argument("--sample_size", type=int, default=None, help="Optional sample limit for quick testing")

    args = parser.parse_args()
    train(
        data_dir=args.data_dir,
        fake_csv=args.fake_csv,
        true_csv=args.true_csv,
        output_dir=args.output_dir,
        epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.lr,
        max_length=args.max_length,
        sample_size=args.sample_size
    )
