#!/usr/bin/env python3
"""Train TF-IDF classifier on full BENI corpus and build monthly narrative index.

Usage::

    python run_tfidf_index.py                            # full pipeline
    python run_tfidf_index.py --sample 50000              # quick test
    python run_tfidf_index.py --output outputs/07_tfidf_index
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("tfidf_index")

_HERE = Path(__file__).resolve().parent
_PIPELINES = _HERE.parents[1]
sys.path.insert(0, str(_PIPELINES))

import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from scipy.sparse import csr_matrix

from shared.io import read_zst_csv

CORPUS_PATH = (
    _HERE / "../../../dataset/BENI/beni-v1/data/processed/"
    / "beni_unified_articles_deduped.csv.zst"
)
OUTPUT_DIR = _HERE / "outputs" / "07_tfidf_index"

USE_COLS = [
    "article_id", "dataset_source", "newspaper",
    "publication_date", "year_month",
    "category_harmonised", "text_clean",
]


def main():
    parser = argparse.ArgumentParser(description="BENI TF-IDF narrative index")
    parser.add_argument("--sample", type=int, default=None)
    parser.add_argument("--output", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--max-features", type=int, default=50000,
                        help="TF-IDF max features (default 50K, reduce if OOM)")
    parser.add_argument("--min-df", type=int, default=5,
                        help="TF-IDF min document frequency (default 5)")
    parser.add_argument("--train-split", type=float, default=0.8,
                        help="Fraction for training (default 0.8)")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info("Loading corpus from %s", CORPUS_PATH)
    t0 = time.time()
    df = read_zst_csv(CORPUS_PATH, usecols=USE_COLS)
    logger.info("Loaded %d articles in %.0fs", len(df), time.time() - t0)

    df = df.dropna(subset=["text_clean"]).reset_index(drop=True)
    df["label"] = (df["category_harmonised"].str.lower().str.strip() == "economy").astype(int)

    n_econ = df["label"].sum()
    logger.info("Labels: %d economy (%.1f%%), %d non-economy (%.1f%%)",
                 n_econ, n_econ / len(df) * 100,
                 len(df) - n_econ, (1 - n_econ / len(df)) * 100)

    if args.sample and args.sample < len(df):
        df = df.sample(n=args.sample, random_state=42).reset_index(drop=True)
        logger.info("Sampled %d articles", len(df))

    df = df.sort_values("publication_date").reset_index(drop=True)

    split_idx = int(len(df) * args.train_split)
    train_df = df.iloc[:split_idx]
    test_df = df.iloc[split_idx:]

    logger.info("Train: %d (%s to %s)", len(train_df),
                 train_df["publication_date"].min(), train_df["publication_date"].max())
    logger.info("Test:  %d (%s to %s)", len(test_df),
                 test_df["publication_date"].min(), test_df["publication_date"].max())

    logger.info("Training TF-IDF (max_features=%d, min_df=%d) ...", args.max_features, args.min_df)
    t0 = time.time()
    vectorizer = TfidfVectorizer(
        max_features=args.max_features,
        min_df=args.min_df,
        ngram_range=(1, 2),
        sublinear_tf=True,
    )
    X_train = vectorizer.fit_transform(train_df["text_clean"])
    logger.info("TF-IDF fit done in %.0fs — vocab=%d, shape=%s",
                 time.time() - t0, len(vectorizer.get_feature_names_out()), X_train.shape)

    logger.info("Training LogisticRegression ...")
    t0 = time.time()
    clf = LogisticRegression(class_weight="balanced", max_iter=1000, n_jobs=-1)
    clf.fit(X_train, train_df["label"])
    logger.info("LR fit done in %.0fs", time.time() - t0)

    model_dir = output_dir / "model"
    model_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(vectorizer, model_dir / "tfidf_vectorizer.joblib")
    joblib.dump(clf, model_dir / "lr_classifier.joblib")
    logger.info("Model saved to %s", model_dir)

    logger.info("Predicting on full corpus (%d articles) ...", len(df))
    t0 = time.time()
    X_full = vectorizer.transform(df["text_clean"])
    probs = clf.predict_proba(X_full)[:, 1]
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
    monthly["month"] = pd.to_datetime(monthly["year_month"] + "-01")

    mu = monthly["economic_share"].mean()
    sigma = monthly["economic_share"].std()
    monthly["tfidf_index"] = 100.0 + (monthly["economic_share"] - mu) / sigma * 10.0

    logger.info("Monthly index: %d months, share range=[%.3f, %.3f], index=[%.1f, %.1f]",
                 len(monthly),
                 monthly["economic_share"].min(), monthly["economic_share"].max(),
                 monthly["tfidf_index"].min(), monthly["tfidf_index"].max())

    monthly_out = output_dir / "beni_tfidf_index.csv"
    monthly.to_csv(monthly_out, index=False)
    logger.info("Index written to %s", monthly_out)

    test_probs = clf.predict_proba(vectorizer.transform(test_df["text_clean"]))[:, 1]
    test_pred = (test_probs > 0.5).astype(int)
    test_acc = (test_pred == test_df["label"]).mean()
    logger.info("Test accuracy: %.4f", test_acc)

    summary = {
        "n_train": len(train_df),
        "n_test": len(test_df),
        "n_months": len(monthly),
        "train_date_range": {
            "start": train_df["publication_date"].min(),
            "end": train_df["publication_date"].max(),
        },
        "test_date_range": {
            "start": test_df["publication_date"].min(),
            "end": test_df["publication_date"].max(),
        },
        "test_accuracy": round(float(test_acc), 4),
        "vocab_size": len(vectorizer.get_feature_names_out()),
        "max_features": args.max_features,
        "mean_economic_share": round(float(monthly["economic_share"].mean()) * 100, 1),
        "mean_index": round(float(monthly["tfidf_index"].mean()), 1),
        "std_index": round(float(monthly["tfidf_index"].std()), 1),
    }
    (output_dir / "tfidf_index_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print("\n═══ Top 5 TF-IDF Index Months ═══")
    for _, row in monthly.nlargest(5, "tfidf_index").iterrows():
        print(f"  {row['year_month']}: {row['tfidf_index']:.1f}  "
              f"(share={row['economic_share']:.1%}, n={int(row['n_articles'])})")
    print("\n═══ Bottom 5 TF-IDF Index Months ═══")
    for _, row in monthly.nsmallest(5, "tfidf_index").iterrows():
        print(f"  {row['year_month']}: {row['tfidf_index']:.1f}  "
              f"(share={row['economic_share']:.1%}, n={int(row['n_articles'])})")
    print()


if __name__ == "__main__":
    main()
