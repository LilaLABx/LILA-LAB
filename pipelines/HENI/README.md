# HENI — Hausa Exploration & Native-language Intelligence

> **Status**: 🔜 Planned
> **Language**: Hausa — 80M speakers
> **Region**: Nigeria, Niger, West Africa
> **Dataset**: [`dataset/HENI/`](../dataset/HENI/)

## Overview

HENI will bring the XENI pipeline to Hausa, the most widely spoken Chadic language with ~80M speakers across West Africa. Hausa has a vibrant media ecosystem including BBC Hausa, VOA Hausa, and local outlets.

## Current State

| Component | Status |
|-----------|--------|
| Pipeline structure | ✅ Bootstrapped from template |
| Data collection | 🔜 Needs identification of major Hausa news sources |
| Annotation | 🔜 Needs native speakers for schema validation |
| Index | First domain (economic) is the recommended starting point |

## How to Contribute

| Role | What You Do |
|------|-------------|
| 🗣️ **Native Speaker** | Validate annotation schemas, review LLM outputs |
| 📊 **Researcher** | Lead the first index construction and paper |
| 💻 **Developer** | Adapt the LLM annotation pipeline for Hausa (Latin/Ajami script) |
| 📰 **Data Collector** | Identify and scrape Hausa news sources |

## Structure

```
heni/
├── annotation/schemas/     # Annotation schemas (economic, health, ...)
├── data/                   # Raw & processed data
├── database/               # Data storage
├── experiment/             # Model training & evaluation
└── indices/eco/ + health/  # Index construction
```

## Deliverable

A validated HENI pipeline producing narrative indices across one or more domains, with a first-author paper on Hausa economic narratives (or your chosen domain).

→ Full contribution framework: [`docs/COLLABORATION.md`](../../docs/COLLABORATION.md)
