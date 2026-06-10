# CENI — Chittagonian Exploration & Native-language Intelligence

> **Status**: 🔜 Seeking contributors
> **Language**: Chittagonian (চাঁটগাঁইয়া) — 16M speakers
> **Region**: Chittagong region, Bangladesh

## Overview

CENI will bring the XENI pipeline to Chittagonian, spoken by 16 million people in the Chittagong region of Bangladesh. As a language distinct from Bangla with its own news ecosystem, Chittagonian is a uniquely underserved language for NLP infrastructure.

## Current State

- Pipeline structure: Ready (copy from `pipelines/template/`)
- Data collection: Needs identification of Chittagonian news sources
- Annotation: Needs native speakers — very limited NLP resources exist
- Index: First domain (economic) is the recommended starting point

## How to Contribute

We need:

| Role | What You Do |
|------|-------------|
| 🗣️ **Native Speaker** | Critical — validate annotations, help build written resources |
| 📊 **Researcher** | Lead the first index construction and paper |
| 💻 **Developer** | Adapt annotation pipeline for Chittagonian |
| 📰 **Data Collector** | Find Chittagonian news sources (print, digital) |

## Getting Started

```bash
# Copy the template to bootstrap
cp -r pipelines/template/* pipelines/ceni/
cd pipelines/ceni/
```

## Deliverable

A validated CENI pipeline producing narrative indices across one or more domains, with a first-author paper on Chittagonian narratives (or your chosen domain).

**→ Full contribution framework:** [`COLLABORATION.md`](../../docs/COLLABORATION.md)
