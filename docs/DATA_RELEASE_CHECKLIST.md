# Data Release Checklist

Use this checklist before calling any LILA Lab dataset release complete. It combines FAIR data principles, reproducible research practice, and dataset-card conventions.

## Findability

- Registry row exists in `registry/languages.json`.
- Dataset README exists under `dataset/<PIPELINE>/README.md`.
- Dataset card exists for released datasets.
- DOI or platform identifier is recorded in `dist/manifests/<PIPELINE>/` when available.

## Accessibility

- Download location or access request path is documented.
- License is explicit for code, data, and third-party upstream sources.
- Large files are distributed through external platforms, not committed directly to Git.

## Interoperability

- File formats are documented.
- Required columns and schema fields are listed.
- Language, script, date, source, title, and text metadata are preserved when available.
- Annotation schemas are valid JSON and pass `python infrastructure/scripts/validate_schemas.py`.

## Reuse

- Provenance explains collection source, date range, processing steps, and known exclusions.
- Limitations and bias notes describe source coverage, dialect coverage, annotation uncertainty, and known structural breaks.
- Citation metadata is present when the dataset is public.
- Contributor credit is recorded in `technical-reports/contributions/OWNERS.csv`.

## Sensitive Data and Ethics

- Private credentials, tokens, cookies, and raw `.env` files are absent.
- Sensitive personal data has been removed or the consent basis is documented.
- Native-speaker review is recorded for annotation schemas and culturally specific labels.
- License consent is documented for contributed corpora.

## Release Evidence

Before release, capture:

- `python -m cli validate`
- `python infrastructure/scripts/validate_schemas.py`
- dataset card review result
- manifest review result
- final `git status --short`
