import os
import sys
import argparse
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    roc_auc_score,
    precision_recall_fscore_support
)

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    from model_training.preprocess import load_kaggle_dataset, clean_text
except ImportError:
    from preprocess import load_kaggle_dataset, clean_text


def evaluate_baseline(model_path: str, data_dir: str, fake_csv: str = "Fake.csv", true_csv: str = "True.csv"):
    if not os.path.exists(model_path):
        print(f"Error: Model file '{model_path}' does not exist.")
        return

    print(f"Loading baseline model from: {model_path}")
    pipeline = joblib.load(model_path)

    fake_path = os.path.join(data_dir, fake_csv)
    true_path = os.path.join(data_dir, true_csv)

    if os.path.exists(fake_path) and os.path.exists(true_path):
        df = load_kaggle_dataset(fake_path, true_path, sample_size=2000)
        X = df["clean_text"]
        y_true = df["label"]
    else:
        print("Kaggle dataset not found. Evaluating on synthetic benchmark...")
        from model_training.train_baseline import BOOTSTRAP_DATA
        texts, labels = zip(*BOOTSTRAP_DATA)
        X = [clean_text(t) for t in texts]
        y_true = labels

    y_pred = pipeline.predict(X)
    probs = pipeline.predict_proba(X)[:, 1] if hasattr(pipeline, "predict_proba") else None

    acc = accuracy_score(y_true, y_pred)
    cm = confusion_matrix(y_true, y_pred)
    p, r, f1, _ = precision_recall_fscore_support(y_true, y_pred, average="binary")

    print("\n================ EVALUATION SUMMARY ================")
    print(f"Accuracy : {acc * 100:.2f}%")
    print(f"Precision: {p * 100:.2f}%")
    print(f"Recall   : {r * 100:.2f}%")
    print(f"F1-Score : {f1 * 100:.2f}%")
    if probs is not None:
        try:
            auc = roc_auc_score(y_true, probs)
            print(f"ROC-AUC  : {auc:.4f}")
        except Exception:
            pass
    print("\nConfusion Matrix:")
    print(f"  [True Negative (Fake as Fake): {cm[0][0]:>4}]  [False Positive (Fake as Real): {cm[0][1]:>4}]")
    print(f"  [False Negative (Real as Fake): {cm[1][0]:>4}] [True Positive (Real as Real):  {cm[1][1]:>4}]")
    print("\nDetailed Classification Report:")
    print(classification_report(y_true, y_pred, target_names=["Fake News (0)", "Real News (1)"]))


def evaluate_adversarial(csv_path: str = "adversarial_examples.csv"):
    """Evaluates full pipeline and baseline model on the hard adversarial dataset."""
    if not os.path.exists(csv_path):
        alt_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "adversarial_examples.csv")
        if os.path.exists(alt_path):
            csv_path = alt_path
        else:
            print(f"Error: Adversarial dataset '{csv_path}' not found.")
            return

    print(f"\n================ ADVERSARIAL BENCHMARK EVALUATION ================")
    print(f"Dataset: {csv_path}")
    df = pd.read_csv(csv_path).dropna()
    print(f"Total Hard Adversarial Test Cases: {len(df)} (Real: {(df['label']==1).sum()}, Fake: {(df['label']==0).sum()})")

    from backend.model.inference import predict, predict_baseline

    results_hybrid = []
    results_baseline = []

    print("\nRunning inference across all adversarial test cases...")
    for _, row in df.iterrows():
        text = row["text"]
        true_lbl = int(row["label"])

        # Hybrid prediction
        res_h = predict(text)
        pred_h = 1 if res_h.get("label") == "Real" else 0
        results_hybrid.append((true_lbl, pred_h))

        # Baseline prediction
        res_b = predict_baseline(text)
        pred_b = 1 if res_b.get("label") == "Real" else 0
        results_baseline.append((true_lbl, pred_b))

    y_true, y_pred_h = zip(*results_hybrid)
    _, y_pred_b = zip(*results_baseline)

    acc_h = accuracy_score(y_true, y_pred_h)
    p_h, r_h, f1_h, _ = precision_recall_fscore_support(y_true, y_pred_h, average="binary")

    acc_b = accuracy_score(y_true, y_pred_b)
    p_b, r_b, f1_b, _ = precision_recall_fscore_support(y_true, y_pred_b, average="binary")

    print("\n--- RESULTS ON ADVERSARIAL HARD EXAMPLES ---")
    print(f"Hybrid Neural Architecture Accuracy: {acc_h * 100:.2f}% (F1: {f1_h * 100:.2f}%)")
    print(f"Baseline Scikit-Learn Accuracy     : {acc_b * 100:.2f}% (F1: {f1_b * 100:.2f}%)")
    print("\nDetailed Hybrid Classification Report:")
    print(classification_report(y_true, y_pred_h, target_names=["Fake (0)", "Real (1)"]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate Fake News Detection Model")
    parser.add_argument("--model_path", type=str, default="backend/model/saved_model/baseline_model.joblib")
    parser.add_argument("--data_dir", type=str, default="data")
    parser.add_argument("--adversarial", action="store_true", help="Run evaluation on hard adversarial benchmark")
    args = parser.parse_args()

    if args.adversarial:
        evaluate_adversarial()
    else:
        evaluate_baseline(args.model_path, args.data_dir)
        evaluate_adversarial()

