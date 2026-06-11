# TIENI — Tagalog Exploration & Native-language Intelligence

> **Status**: 🔜 Planned
> **Language**: Tagalog (Filipino) — 80M speakers
> **Region**: Philippines
> **Dataset**: [`dataset/TIENI/`](../dataset/TIENI/)

## Overview

TIENI will bring the XENI pipeline to Tagalog, the basis of the Filipino national language with ~80M speakers. The Philippines has a major news ecosystem including ABS-CBN, GMA News, Inquirer, and Pilipino Star Ngayon.

## Current State

| Component | Status |
|-----------|--------|
| Pipeline structure | ✅ Bootstrapped from template |
| Data collection | 🔜 Needs scraping of Tagalog news portals |
| Annotation | 🔜 Needs native speakers for schema validation |
| Index | First domain (economic) is the recommended starting point |

## How to Contribute

| Role | What You Do |
|------|-------------|
| 🗣️ **Native Speaker** | Validate annotation schemas, review LLM outputs |
| 📊 **Researcher** | Lead the first index construction and paper |
| 💻 **Developer** | Adapt the LLM annotation pipeline for Tagalog |
| 📰 **Data Collector** | Identify and scrape Tagalog news sources |

## Structure

```
tieni/
├── annotation/schemas/     # Annotation schemas (economic, health, ...)
├── data/                   # Raw & processed data
├── database/               # Data storage
├── experiment/             # Model training & evaluation
└── indices/eco/ + health/  # Index construction
```

## Deliverable

A validated TIENI pipeline producing narrative indices across one or more domains, with a first-author paper on Tagalog economic narratives (or your chosen domain).

→ Full contribution framework: [`docs/COLLABORATION.md`](../../docs/COLLABORATION.md)
