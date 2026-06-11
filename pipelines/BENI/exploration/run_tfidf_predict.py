#!/usr/bin/env python3
"""Load trained TF-IDF model and predict on full corpus in chunks."""
from __future__ import annotations

import logging
import sys
import time
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s",
                    datefmt="%H:%M:%S")
logger = logging.getLogger("tfidf_predict")

_HERE = Path(__file__).resolve().parent
_PIPELINES = _HERE.parents[1]
sys.path.insert(0, str(_PIPELINES))

import joblib
import numpy as np
import pandas as pd
from scipy.sparse import vstack

from shared.io import read_zst_csv

CORPUS_PATH = (
    _HERE / "../../../dataset/BENI/beni-v1/data/processed/"
    / "beni_unified_articles_deduped.csv.zst"
)
MODEL_DIR = _HERE / "outputs" / "07_tfidf_index" / "model"
OUTPUT_DIR = _HERE / "outputs" / "07_tfidf_index"
CHUNK_SIZE = 100_000

USE_COLS = [
    "article_id", "dataset_source", "newspaper",
    "publication_date", "year_month",
    "category_harmonised", "text_clean",
]


def main():
    logger.info("Loading model from %s", MODEL_DIR)
    vectorizer = joblib.load(MODEL_DIR / "tfidf_vectorizer.joblib")
    clf = joblib.load(MODEL_DIR / "lr_classifier.joblib")
    logger.info("Model loaded. Vocab size: %d", len(vectorizer.get_feature_names_out()))

    logger.info("Loading corpus from %s", CORPUS_PATH)
    t0 = time.time()
    df = read_zst_csv(CORPUS_PATH, usecols=USE_COLS)
    logger.info("Loaded %d articles in %.0fs", len(df), time.time() - t0)

    df = df.dropna(subset=["text_clean"]).reset_index(drop=True)
    df["label"] = (df["category_harmonised"].str.lower().str.strip() == "economy").astype(int)
    full_len = len(df)

    probs = np.empty(full_len, dtype=np.float64)

    logger.info("Predicting in chunks of %d ...", CHUNK_SIZE)
    t0 = time.time()
    for start in range(0, full_len, CHUNK_SIZE):
        end = min(start + CHUNK_SIZE, full_len)
        chunk_text = df.iloc[start:end]["text_clean"]
        X_chunk = vectorizer.transform(chunk_text)
        probs[start:end] = clf.predict_proba(X_chunk)[:, 1]
        elapsed = time.time() - t0
        rate = end / elapsed if elapsed > 0 else 0
        logger.info("  chunk %d–%d done in %.0fs (%.0f docs/s)", start, end, elapsed, rate)

    df["economic_prob"] = probs
    df["economic_pred"] = (probs > 0.5).astype(int)
    logger.info("Prediction done in %.0fs — mean prob=%.3f, pred rate=%.1f%%",
                 time.time() - t0, probs.mean(), df["economic_pred"].mean() * 100)

    monthly = (
        df.groupby("year_month", sort=True)
        .agg(
            n_articles=("economic_prob", "count"),
            mean_prob=("economic_prob", "mean"),
            economic_share=("economic_pred", "mean"),
            n_economic=("economic_pred", "sum"),
        )
        .reset_index()
    )

    mu = monthly["economic_share"].mean()
    sigma = monthly["economic_share"].std()
    monthly["tfidf_index"] = 100.0 + (monthly["economic_share"] - mu) / sigma * 10.0

    logger.info("Monthly index: %d months, share=[%.3f, %.3f], index=[%.1f, %.1f]",
                 len(monthly),
                 monthly["economic_share"].min(), monthly["economic_share"].max(),
                 monthly["tfidf_index"].min(), monthly["tfidf_index"].max())

    monthly_out = OUTPUT_DIR / "beni_tfidf_index.csv"
    monthly.to_csv(monthly_out, index=False)
    logger.info("Index written to %s", monthly_out)

    full_out = OUTPUT_DIR / "beni_tfidf_predictions.csv"
    df.to_csv(full_out, index=False)
    logger.info("Full predictions written to %s", full_out)

    test_df = df.iloc[int(len(df) * 0.8):]
    test_probs = probs[int(len(df) * 0.8):]
    test_pred = (test_probs > 0.5).astype(int)
    test_acc = (test_pred == test_df["label"]).mean()
    logger.info("Test accuracy: %.4f", test_acc)

    print("\n═══ Top 5 TF-IDF Index Months ═══")
    for _, row in monthly.nlargest(5, "tfidf_index").iterrows():
        print(f"  {row['year_month']}: {row['tfidf_index']:.1f}  "
              f"(share={row['economic_share']:.1%}, n={int(row['n_articles'])})")
    print("\n═══ Bottom 5 ═══")
    for _, row in monthly.nsmallest(5, "tfidf_index").iterrows():
        print(f"  {row['year_month']}: {row['tfidf_index']:.1f}  "
              f"(share={row['economic_share']:.1%}, n={int(row['n_articles'])})")
    print()


if __name__ == "__main__":
    main()
