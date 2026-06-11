# IDENI — Indonesian Exploration & Native-language Intelligence

> **Status**: 🔜 Planned
> **Language**: Indonesian (Bahasa Indonesia) — 200M speakers
> **Region**: Indonesia
> **Dataset**: [`dataset/IDENI/`](../dataset/IDENI/)

## Overview

IDENI will bring the XENI pipeline to Indonesian, the national language of Indonesia with ~200M speakers — the largest target language in the XENI program. Indonesia has an extensive digital news ecosystem including Kompas, Detik, Tempo, Republika, and Antara.

## Current State

| Component | Status |
|-----------|--------|
| Pipeline structure | ✅ Bootstrapped from template |
| Data collection | 🔜 Needs scraping of Indonesian news portals |
| Annotation | 🔜 Needs native speakers for schema validation |
| Index | First domain (economic) is the recommended starting point |

## Validation

```bash
python -m cli validate
```

This command proves IDENI is a valid scaffold. It does not mean the dataset or index is operational.

## How to Contribute

| Role | What You Do |
|------|-------------|
| 🗣️ **Native Speaker** | Validate annotation schemas, review LLM outputs |
| 📊 **Researcher** | Lead the first index construction and paper |
| 💻 **Developer** | Adapt the LLM annotation pipeline for Indonesian |
| 📰 **Data Collector** | Identify and scrape Indonesian news sources |

## Structure

```
ideni/
├── annotation/schemas/     # Annotation schemas (economic, health, ...)
├── data/                   # Raw & processed data
├── database/               # Data storage
├── experiment/             # Model training & evaluation
└── indices/eco/ + health/  # Index construction
```

## Deliverable

A validated IDENI pipeline producing narrative indices across one or more domains, with a first-author paper on Indonesian economic narratives (or your chosen domain).

→ Full contribution framework: [`docs/COLLABORATION.md`](../../docs/COLLABORATION.md)
