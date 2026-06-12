# ADR-003: Dataset ↔ Pipeline Separation

**Status:** Accepted

**Date:** 2026-06-12

## Context

The original repository structure, designed around the BENI research project, stored datasets, pipeline code, and experiment artifacts together under a `pipelines/` directory hierarchy. As the project expands to support 10 languages, each with its own pipeline, raw corpus, processed annotations, and published releases, the coupling of data and code creates several problems:

- **Repository bloat**: Large corpora (664k articles, 3.3 GB for BENI alone) in version control slow clones, pull requests, and CI operations
- **Release confusion**: Dataset releases have different access patterns (DOIs, platform distribution) than code releases (PyPI, Git tags)
- **Permission asymmetry**: Data may have different licensing (CC BY 4.0) than code (MIT); mixing them makes compliance harder
- **Contribution friction**: Linguistic contributors who want to provide raw news articles should not need to navigate pipeline code structure

## Decision

We separate datasets and pipeline code into distinct top-level directories:

```
pipelines/    → Code, schemas, configs, small examples only
dataset/      → Raw corpora, processed releases, dataset cards, manifests
```

### Ownership Boundaries

| Concern | Lives in `pipelines/` | Lives in `dataset/` |
|---------|----------------------|---------------------|
| Annotation schemas | `pipelines/[x]eni/annotation/schemas/` | — |
| Raw article corpora | — | `dataset/[x]eni/raw/` |
| Processed annotations | — | `dataset/[x]eni/processed/annotations/` |
| Index construction code | `pipelines/[x]eni/indices/` | — |
| Built narrative indices | — | `dataset/[x]eni/processed/indices/` |
| Dataset cards & release notes | — | `dataset/[x]eni/README.md` + `DATASET_CARD.md` |
| Distribution manifests | `dist/manifests/` | — |
| Experiment/training code | `pipelines/[x]eni/experiment/` | — |
| Experiment output artifacts | `.gitignore` (not tracked) | — |

### Reference Implementation

The BENI pipeline (`pipelines/BENI/`) references the BENI dataset (`dataset/BENI/`) via relative paths and symlinks where appropriate. The dataset release process is documented in `docs/DATA_RELEASE_CHECKLIST.md`.

## Consequences

### Positive

- **Clear contribution paths**: Linguistic contributors work in `dataset/`, developers in `pipelines/`
- **License clarity**: Code in `pipelines/` is MIT; data in `dataset/` is CC BY 4.0, with per-language license statements
- **Scalability**: New language pipelines can be added without bloating the repository with data
- **CI efficiency**: Pipeline code CI only triggers on `pipelines/` changes; dataset metadata CI triggers on `dataset/` changes

### Negative

- **Cross-repository coordination**: Pipeline code and dataset must stay in sync (schema version, annotation format) — mitigated by the pipeline contract (`registry/xeni_pipeline_contract.json`)
- **Dataset release complexity**: Full dataset releases (with DOIs) may live outside the repository on Zenodo/OSF; the `dataset/` directory contains metadata and subset examples

### Neutral

- Datasets that are too large for GitHub (samples > 100MB) should use Git LFS or external distribution with a manifest in `dist/manifests/`
- This ADR formalizes a separation that was partially implemented before June 2026
