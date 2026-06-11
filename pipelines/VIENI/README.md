# VIENI — Vietnamese Exploration & Native-language Intelligence

> **Status**: 🔜 Planned
> **Language**: Vietnamese (Tiếng Việt) — 100M speakers
> **Region**: Vietnam
> **Dataset**: [`dataset/VIENI/`](../dataset/VIENI/)

## Overview

VIENI will bring the XENI pipeline to Vietnamese, the national language of Vietnam with ~100 million speakers. Vietnam has a vibrant digital news ecosystem including VnExpress, Tuổi Trẻ, Thanh Niên, and Dân Trí.

## Current State

| Component | Status |
|-----------|--------|
| Pipeline structure | ✅ Bootstrapped from template |
| Data collection | 🔜 Needs scraping of Vietnamese news portals |
| Annotation | 🔜 Needs native speakers for schema validation |
| Index | First domain (economic) is the recommended starting point |

## How to Contribute

| Role | What You Do |
|------|-------------|
| 🗣️ **Native Speaker** | Validate annotation schemas, review LLM outputs |
| 📊 **Researcher** | Lead the first index construction and paper |
| 💻 **Developer** | Adapt the LLM annotation pipeline for Vietnamese (Latin + diacritics) |
| 📰 **Data Collector** | Identify and scrape Vietnamese news sources |

## Structure

```
vieni/
├── annotation/schemas/     # Annotation schemas (economic, health, ...)
├── data/                   # Raw & processed data
├── database/               # Data storage
├── experiment/             # Model training & evaluation
└── indices/eco/ + health/  # Index construction
```

## Deliverable

A validated VIENI pipeline producing narrative indices across one or more domains, with a first-author paper on Vietnamese economic narratives (or your chosen domain).

→ Full contribution framework: [`docs/COLLABORATION.md`](../../docs/COLLABORATION.md)
