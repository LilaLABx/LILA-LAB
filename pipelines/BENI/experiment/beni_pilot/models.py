from __future__ import annotations

from config import ExperimentConfig
from sklearn.pipeline import Pipeline

from pipelines.shared.models import build_tfidf_logreg as _shared_build


def build_tfidf_logreg(config: ExperimentConfig) -> Pipeline:
    """Build a TF-IDF + Logistic Regression pipeline.

    Delegates to ``shared.models.build_tfidf_logreg``, unpacking
    config fields for the keyword-based API.
    """
    return _shared_build(
        max_features=config.max_features,
        min_df=config.min_df,
        ngram_range=config.ngram_range,
        max_iter=config.max_iter,
        seed=config.seed,
        class_weight="balanced",
        solver="liblinear",
    )
