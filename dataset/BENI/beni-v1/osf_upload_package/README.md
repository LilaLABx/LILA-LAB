# BENI v1.0 OSF Upload Package

This package contains the OSF-safe preprint materials for:

**BENI v1.0: A Harmonised Bangla News Dataset for Economic Narrative Measurement**

## Included

- `paper/BENI_v1_data_paper_preprint.pdf`: OSF-ready preprint PDF.
- `paper/main.tex`: LaTeX source.
- `paper/references.bib`: bibliography.
- `DATA_LICENSE.md`: layered data licence and use directions.
- `CODE_LICENSE.md`: MIT code licence.
- `CITATION.cff`: citation metadata.
- `OSF_PREPRINT_UPLOAD.md`: suggested OSF title, abstract, tags, licence, and data availability text.
- `docs/PRELIMINARY_MERGE_RESULT.md`: merge-result note.
- `data/processed/beni_unified_articles_summary.json`: machine-readable build summary.
- `scripts/build_beni_v1_articles.py`: reproducible build script.

## Intentionally Excluded

Full article-body CSV files are excluded from this OSF package because they are
large and may contain text governed by upstream corpus and news-source terms.

The public OSF release should share BENI metadata, hashes, labels, documentation,
summary statistics, and scripts. Full article text should be redistributed only
when upstream rights are documented.

## Recommended OSF Licence

Use **CC BY 4.0** for the OSF preprint and BENI-derived metadata/documentation.
Use the separate MIT licence for code.

