# NENI — Nepali Exploration & Native-language Intelligence

> **Status**: 🔜 Seeking contributors
> **Language**: Nepali (नेपाली) — 25M speakers
> **Region**: Nepal
> **Dataset**: [`dataset/NENI/`](../dataset/NENI/)

## Overview

NENI will bring the XENI pipeline to Nepali, the official language of Nepal. With 25 million speakers and a mature news ecosystem, Nepali is well-positioned for rapid pipeline development.

## Current State

| Component | Status |
|-----------|--------|
| Pipeline structure | ✅ Bootstrapped from template |
| Data collection | 🔜 Needs scraping of Nepali news portals |
| Annotation | 🔜 Needs native speakers for schema validation |
| Index | First domain (economic) is the recommended starting point |

## Validation

```bash
python -m cli validate
```

This command proves NENI is a valid scaffold. It does not mean the dataset or index is operational.

## How to Contribute

| Role | What You Do |
|------|-------------|
| 🗣️ **Native Speaker** | Validate annotation schemas, review LLM outputs |
| 📊 **Researcher** | Lead the first index construction and paper |
| 💻 **Developer** | Adapt the LLM annotation pipeline for Nepali script (Devanagari) |
| 📰 **Data Collector** | Identify and scrape Nepali news sources |

## Structure

```
neni/
├── annotation/schemas/     # Annotation schemas (economic, health, ...)
├── data/                   # Raw & processed data
├── database/               # Data storage
├── experiment/             # Model training & evaluation
└── indices/eco/ + health/  # Index construction
```

## Getting Started

```bash
pip install -r requirements.txt
# Start with annotation schema design
cd annotation/schemas/
```

## Deliverable

A validated NENI pipeline producing narrative indices across one or more domains, with a first-author paper on Nepali economic narratives (or your chosen domain).

→ Full contribution framework: [`docs/COLLABORATION.md`](../../docs/COLLABORATION.md)
