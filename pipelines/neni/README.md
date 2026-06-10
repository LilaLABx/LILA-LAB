# NENI — Nepali Exploration & Native-language Intelligence

> **Status**: 🔜 Seeking contributors
> **Language**: Nepali (नेपाली) — 25M speakers
> **Region**: Nepal

## Overview

NENI will bring the XENI pipeline to Nepali, the national language of Nepal. With 25 million speakers and a growing digital news landscape, Nepali presents a strong opportunity for narrative measurement.

## Current State

- Pipeline structure: Ready (copy from `pipelines/template/`)
- Data collection: Needs identification of major Nepali news sources
- Annotation: Needs native speakers for schema validation
- Index: First domain (economic) is the recommended starting point

## How to Contribute

We need:

| Role | What You Do |
|------|-------------|
| 🗣️ **Native Speaker** | Validate annotation schemas, review LLM outputs |
| 📊 **Researcher** | Lead the first index construction and paper |
| 💻 **Developer** | Adapt the LLM annotation pipeline for Nepali script (Devanagari) |
| 📰 **Data Collector** | Identify and scrape Nepali news sources |

## Getting Started

```bash
# Copy the template to bootstrap
cp -r pipelines/template/* pipelines/neni/
cd pipelines/neni/
```

## Deliverable

A validated NENI pipeline producing narrative indices across one or more domains, with a first-author paper on Nepali economic narratives (or your chosen domain).

**→ Full contribution framework:** [`COLLABORATION.md`](../../docs/COLLABORATION.md)
