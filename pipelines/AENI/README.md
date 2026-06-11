# AENI — Assamese Exploration & Native-language Intelligence

> **Status**: 🔜 Seeking contributors
> **Language**: Assamese (অসমীয়া) — 15M speakers
> **Region**: Assam, India
> **Dataset**: [`dataset/AENI/`](../dataset/AENI/)

## Overview

AENI will bring the XENI pipeline to Assamese, the official language of Assam. With 15 million speakers and a vibrant news ecosystem, Assamese is the next frontier for narrative measurement in South Asia.

## Current State

- Pipeline structure: ✅ Bootstrapped from template
- Data collection: 🔜 Needs identification of major Assamese news sources
- Annotation: 🔜 Needs native speakers for schema validation
- Index: First domain (economic) is the recommended starting point

## Validation

```bash
python -m cli validate
```

This command proves AENI is a valid scaffold. It does not mean the dataset or index is operational.

## How to Contribute

| Role | What You Do |
|------|-------------|
| 🗣️ **Native Speaker** | Validate annotation schemas, review LLM outputs |
| 📊 **Researcher** | Lead the first index construction and paper |
| 💻 **Developer** | Adapt the LLM annotation pipeline for Assamese script |
| 📰 **Data Collector** | Identify and scrape Assamese news sources |

## Structure

```
aeni/
├── annotation/schemas/     # Annotation schemas (economic, health, ...)
├── data/                   # Raw & processed data (small files, pointers to dataset/)
├── database/               # Data storage
├── experiment/             # Model training & evaluation
└── indices/eco/ + health/  # Index construction
```

## Deliverable

A validated AENI pipeline producing narrative indices across one or more domains, with a first-author paper on Assamese economic narratives (or your chosen domain).

→ Full contribution framework: [`docs/COLLABORATION.md`](../../docs/COLLABORATION.md)
