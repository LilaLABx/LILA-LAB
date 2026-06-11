# BENI Pilot Run Manifest

## Study

- Title: BENI TF-IDF baseline and narrative index pilot
- Pipeline: BENI
- Domain: Economic narratives
- Owner: LILA Lab
- Date: 2026-06-12

## Software Versions

- Python: 3.10+
- Package install command: `pip install -e ".[core,dev]"`
- Git commit: record with `git rev-parse HEAD` before running
- Operating system: record with `python -m platform`

## Input Data

- Dataset: Potrika Bangla news corpus
- Source location: `pipelines/BENI/data/raw/potrika/` or external Mendeley download
- License: CC BY 4.0 for released data, upstream license where applicable
- Date range: 2014-2020 for the original pilot index
- Required columns: article id, date, source, title/headline, text, category when available

## Commands

```bash
cd pipelines/BENI/experiment/beni_pilot
python3 train.py --task economic --model-type tfidf --data-source potrika-timeseries
python3 build_index.py
python3 correlate.py
```

## Random Seed and Determinism

- Random seed: use the seed defined in `pipelines/BENI/experiment/beni_pilot/config.py`
- Deterministic preprocessing notes: record tokenization and data split configuration before training
- Known non-deterministic steps: external LLM annotation and GPU transformer training require separate manifests

## Output Paths

- Tables: `pipelines/BENI/experiment/outputs/`
- Figures: `pipelines/BENI/experiment/outputs/` when generated
- Model artifacts: `pipelines/BENI/experiment/models/`
- Validation reports: `pipelines/BENI/experiment/outputs/` and related technical report directories

## Validation

- Automated command: `python -m pytest -q`
- Manual/inspection command: inspect the generated monthly index CSV and correlation output
- Expected observable: a monthly index covering the configured period and correlation output for CPI, FX, and reserves

## Limitations

- Data limitations: source coverage depends on the Potrika corpus and may not represent every Bangla news outlet.
- Model limitations: TF-IDF is the interpretable baseline, not the final BanglaBERT target model.
- Reuse cautions: do not compare new language results without documenting source coverage and date-range differences.
