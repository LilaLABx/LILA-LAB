# CENI — Chittagonian Exploration & Native-language Intelligence

> **Status**: 🔜 Feasibility study
> **Language**: Chittagonian (চাঁটগাঁইয়া) — 16M speakers
> **Region**: Chittagong, Bangladesh
> **Dataset**: [`dataset/CENI/`](../dataset/CENI/)

## Overview

CENI aims to bring the XENI pipeline to Chittagonian, a minority language of Bangladesh. With ~16M speakers but limited digital news presence, the first phase is a feasibility study to identify viable sources.

## Current State

| Component | Status |
|-----------|--------|
| Pipeline structure | ✅ Bootstrapped from template |
| Data collection | 🔜 Feasibility — sources need surveying |
| Annotation | 🔜 Needs native speakers |
| Index | First domain TBD based on available data |

## Validation

```bash
python -m cli validate
```

This command proves CENI is a valid scaffold. It does not mean the dataset or index is operational.

## Background

Chittagonian is a minority language spoken primarily in the Chittagong region of Bangladesh. Digital news presence is limited — feasibility work is needed to identify viable sources before full pipeline construction.

## How to Contribute

| Role | What You Do |
|------|-------------|
| 🗣️ **Native Speaker** | Help identify Chittagonian-language news sources |
| 📊 **Researcher** | Lead feasibility assessment and first paper |
| 📰 **Data Collector** | Search for and archive Chittagonian content |

## Structure

```
ceni/
├── annotation/schemas/     # Annotation schemas (when ready)
├── data/                   # Data placeholders
├── database/               # Data storage (when ready)
├── experiment/             # Model training & evaluation
└── indices/                # Index construction (when ready)
```

## Deliverable

A validated CENI pipeline producing narrative indices across one or more domains, beginning with a feasibility report on available Chittagonian news sources.

→ Full contribution framework: [`docs/COLLABORATION.md`](../../docs/COLLABORATION.md)
