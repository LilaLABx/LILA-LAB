"""
LILA Lab — Shared Analysis Module

Exploration and diagnostics infrastructure for narrative index construction.
All 10 XENI pipelines use these utilities for dataset profiling, vocabulary
analysis, temporal diagnostics, schema validation, reporting, and now
annotation, index construction, and macroeconomic validation.

Typical usage::

    from shared.analysis.profiler import corpus_profile
    from shared.analysis.vocabulary import vocabulary_profile
    from shared.analysis.temporal import coverage_diagnostics
    from shared.analysis.schema_validator import validate_schema_coverage
    from shared.analysis.reporter import generate_report
    from shared.analysis.annotator import run_pilot_annotation
    from shared.analysis.index_builder import build_monthly_index
    from shared.analysis.validator import correlate_with_macro

    # Preprocessing pipeline factory (for 4 index construction methods)
    from shared.analysis.preprocessing import PreprocessingPipeline
    pipe = PreprocessingPipeline.preset("bbd")
"""

from .annotator import (
    compute_agreement,
    field_level_reliability,
    run_batch_annotation,
    run_pilot_annotation,
)
from .index_builder import (
    apply_calibration,
    build_monthly_index,
    load_macro_series,
    merge_macro_data,
    normalize_index,
)
from .preprocessing import (
    PreprocessingPipeline,
    clean_text,
    load_stopwords,
    simple_tokenizer,
    stopword_filtered_tokenizer,
    tokenizer_for_pipeline,
)
from .profiler import corpus_profile, run_profile
from .reporter import generate_registry_update, generate_report
from .schema_validator import (
    run_schema_validation,
    validate_schema_coverage,
)
from .temporal import (
    coverage_diagnostics,
    detect_source_boundary,
    run_temporal,
)
from .validator import (
    annual_correlation,
    correlate_with_macro,
    first_differenced_correlation,
    generate_validation_report,
    lead_lag_analysis,
)
from .visualizer import (
    plot_category_distribution,
    plot_source_temporal_coverage,
    plot_source_transition_diagnostic,
    plot_temporal_coverage,
    plot_text_length_distribution,
    plot_wordcloud,
)
from .vocabulary import (
    log_odds_ratio,
    run_vocabulary,
    vocabulary_profile,
)

__all__ = [
    # preprocessing
    "PreprocessingPipeline",
    "load_stopwords",
    "simple_tokenizer",
    "stopword_filtered_tokenizer",
    "clean_text",
    "tokenizer_for_pipeline",
    # annotator
    "run_pilot_annotation",
    "compute_agreement",
    "field_level_reliability",
    "run_batch_annotation",
    # index_builder
    "build_monthly_index",
    "apply_calibration",
    "normalize_index",
    "merge_macro_data",
    "load_macro_series",
    # profiler
    "corpus_profile",
    "run_profile",
    # validator
    "correlate_with_macro",
    "first_differenced_correlation",
    "lead_lag_analysis",
    "annual_correlation",
    "generate_validation_report",
    # vocabulary
    "vocabulary_profile",
    "log_odds_ratio",
    "run_vocabulary",
    # temporal
    "coverage_diagnostics",
    "detect_source_boundary",
    "run_temporal",
    # schema_validator
    "validate_schema_coverage",
    "run_schema_validation",
    # visualizer
    "plot_category_distribution",
    "plot_text_length_distribution",
    "plot_temporal_coverage",
    "plot_source_temporal_coverage",
    "plot_wordcloud",
    "plot_source_transition_diagnostic",
    # reporter
    "generate_report",
    "generate_registry_update",
]
