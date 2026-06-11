# KIENI — Kiswahili Exploration & Native-language Intelligence

> **Status**: 🔜 Planned
> **Language**: Kiswahili (Swahili) — 100M+ speakers
> **Region**: East Africa (Tanzania, Kenya, Uganda, DRC)
> **Dataset**: [`dataset/KIENI/`](../dataset/KIENI/)

## Overview

KIENI will bring the XENI pipeline to Kiswahili, the most widely spoken language in East Africa with over 100 million speakers. Swahili has extensive news coverage including Mwananchi, The Citizen, Nipashe, and BBC Swahili.

## Current State

| Component | Status |
|-----------|--------|
| Pipeline structure | ✅ Bootstrapped from template |
| Data collection | 🔜 Needs scraping of Swahili news portals |
| Annotation | 🔜 Needs native speakers for schema validation |
| Index | First domain (economic) is the recommended starting point |

## How to Contribute

| Role | What You Do |
|------|-------------|
| 🗣️ **Native Speaker** | Validate annotation schemas, review LLM outputs |
| 📊 **Researcher** | Lead the first index construction and paper |
| 💻 **Developer** | Adapt the LLM annotation pipeline for Swahili |
| 📰 **Data Collector** | Identify and scrape Swahili news sources |

## Structure

```
kieni/
├── annotation/schemas/     # Annotation schemas (economic, health, ...)
├── data/                   # Raw & processed data
├── database/               # Data storage
├── experiment/             # Model training & evaluation
└── indices/eco/ + health/  # Index construction
```

## Deliverable

A validated KIENI pipeline producing narrative indices across one or more domains, with a first-author paper on Swahili economic narratives (or your chosen domain).

→ Full contribution framework: [`docs/COLLABORATION.md`](../../docs/COLLABORATION.md)
