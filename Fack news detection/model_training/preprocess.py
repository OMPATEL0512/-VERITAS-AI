"""
Data Preprocessing module for Fake News Detection.
Cleans raw text, handles dataset ingestion (e.g. Kaggle Fake.csv and True.csv),
and prepares tokenized datasets for DistilBERT and classical ML pipelines.
"""

import os
import re
import string
import pandas as pd
import numpy as np
from typing import Tuple, List, Optional
from sklearn.model_selection import train_test_split


def clean_text(text: str) -> str:
    """
    Cleans raw news article text:
    - Removes URLs
    - Removes HTML tags
    - Strips special publisher artifacts (e.g., 'Reuters - ' prefixes)
    - Normalizes excessive whitespace
    - Preserves sentence structure and semantic markers for Transformer context
    """
    if not isinstance(text, str):
        return ""

    # Remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", "", text)

    # Remove HTML tags
    text = re.sub(r"<.*?>", "", text)

    # Remove bracketed artifacts e.g. [Reuters], (Reuters)
    text = re.sub(r"\[.*?\]", "", text)

    # Remove typical publisher prefixes e.g. "WASHINGTON (Reuters) - "
    text = re.sub(r"^[A-Z\s]+(?:\([A-Za-z\s]+\))?\s*[-–—]\s*", "", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


def load_kaggle_dataset(
    fake_csv_path: str,
    true_csv_path: str,
    sample_size: Optional[int] = None,
    random_state: int = 42
) -> pd.DataFrame:
    """
    Loads and merges Kaggle Fake and True news datasets:
    - Label 1 = Real / True News
    - Label 0 = Fake / Fabricated News
    """
    if not os.path.exists(fake_csv_path) or not os.path.exists(true_csv_path):
        raise FileNotFoundError(
            f"Dataset files not found. Ensure '{fake_csv_path}' and '{true_csv_path}' exist."
        )

    print(f"Loading Fake news from: {fake_csv_path}")
    df_fake = pd.read_csv(fake_csv_path)
    df_fake["label"] = 0

    print(f"Loading True news from: {true_csv_path}")
    df_true = pd.read_csv(true_csv_path)
    df_true["label"] = 1

    # Merge title and text for rich context
    df_combined = pd.concat([df_fake, df_true], ignore_index=True)

    # Handle missing values
    df_combined["title"] = df_combined["title"].fillna("")
    df_combined["text"] = df_combined["text"].fillna("")
    df_combined["full_text"] = df_combined["title"] + " " + df_combined["text"]

    # Clean text
    print("Preprocessing and cleaning text...")
    df_combined["clean_text"] = df_combined["full_text"].apply(clean_text)

    # Remove empty entries after cleaning
    df_combined = df_combined[df_combined["clean_text"].str.len() > 20]

    # Shuffle
    df_combined = df_combined.sample(frac=1.0, random_state=random_state).reset_index(drop=True)

    if sample_size and sample_size < len(df_combined):
        df_combined = df_combined.head(sample_size)
        print(f"Sampled {sample_size} records.")

    print(f"Dataset loaded: {len(df_combined)} samples (Real: {(df_combined['label']==1).sum()}, Fake: {(df_combined['label']==0).sum()})")
    return df_combined


def split_data(
    df: pd.DataFrame,
    test_size: float = 0.2,
    random_state: int = 42
) -> Tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
    """Splits dataset into train and validation sets with stratification."""
    X = df["clean_text"]
    y = df["label"]
    return train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)


if __name__ == "__main__":
    sample = "WASHINGTON (Reuters) - The US Congress approved a new bill on clean energy today! Visit https://example.com for details."
    print("Original:", sample)
    print("Cleaned :", clean_text(sample))
