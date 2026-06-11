"""
LILA Lab — Shared Pipeline Library

Language-agnostic utilities for XENI pipeline construction:
data loading, model training, evaluation, LLM annotation,
statistical agreement, and configuration management.

Explicit re-exports for direct import:
    from pipelines.shared import BaseExperimentConfig
    from pipelines.shared import evaluate_model, build_tfidf_logreg
    from pipelines.shared import normalize_text, set_seed
"""

from .analysis import (  # noqa: F401
    corpus_profile,
    coverage_diagnostics,
    detect_source_boundary,
    generate_registry_update,
    generate_report,
    log_odds_ratio,
    plot_category_distribution,
    plot_source_temporal_coverage,
    plot_source_transition_diagnostic,
    plot_temporal_coverage,
    plot_text_length_distribution,
    plot_wordcloud,
    run_profile,
    run_schema_validation,
    run_temporal,
    run_vocabulary,
    validate_schema_coverage,
    vocabulary_profile,
)
from .config import BaseExperimentConfig
from .data import label_by_keywords, normalize_text, set_seed
from .eval import evaluate_model
from .io import (
    read_csv_safe,
    read_json,
    read_jsonl,
    save_jsonl,
    write_json,
    zip_outputs,
)
from .models import build_tfidf_logreg
from .stats import (
    classification_report,
    cohens_kappa,
    confusion_matrix,
    fleiss_kappa,
)

__all__ = [
    "BaseExperimentConfig",
    "normalize_text",
    "set_seed",
    "label_by_keywords",
    "evaluate_model",
    "build_tfidf_logreg",
    "write_json",
    "read_json",
    "save_jsonl",
    "read_jsonl",
    "read_csv_safe",
    "zip_outputs",
    "cohens_kappa",
    "fleiss_kappa",
    "confusion_matrix",
    "classification_report",
    "corpus_profile",
    "coverage_diagnostics",
    "detect_source_boundary",
    "generate_report",
    "generate_registry_update",
    "log_odds_ratio",
    "plot_category_distribution",
    "plot_source_temporal_coverage",
    "plot_source_transition_diagnostic",
    "plot_temporal_coverage",
    "plot_text_length_distribution",
    "plot_wordcloud",
    "run_profile",
    "run_schema_validation",
    "run_temporal",
    "run_vocabulary",
    "validate_schema_coverage",
    "vocabulary_profile",
]
