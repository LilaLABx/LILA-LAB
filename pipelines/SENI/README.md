# SENI — Sylheti Exploration & Native-language Intelligence

> **Status**: 🔜 Feasibility study
> **Language**: Sylheti (চিটাঙ্গ) — 11M speakers
> **Region**: Sylhet, Bangladesh
> **Dataset**: [`dataset/SENI/`](../dataset/SENI/)

## Overview

SENI aims to bring the XENI pipeline to Sylheti, a minority language of Bangladesh. With ~11M speakers but limited digital news presence, the first phase is a feasibility study to identify viable sources.

## Current State

| Component | Status |
|-----------|--------|
| Pipeline structure | ✅ Bootstrapped from template |
| Data collection | 🔜 Feasibility — sources need surveying |
| Annotation | 🔜 Needs native speakers |
| Index | First domain TBD based on available data |

## Background

Sylheti is a minority language spoken primarily in the Sylhet region of Bangladesh and the Bangladeshi diaspora. Digital news presence is limited — feasibility work is needed to identify viable sources before full pipeline construction.

## How to Contribute

| Role | What You Do |
|------|-------------|
| 🗣️ **Native Speaker** | Help identify Sylheti-language news sources |
| 📊 **Researcher** | Lead feasibility assessment and first paper |
| 📰 **Data Collector** | Search for and archive Sylheti content |

## Structure

```
seni/
├── annotation/schemas/     # Annotation schemas (when ready)
├── data/                   # Data placeholders
├── database/               # Data storage (when ready)
├── experiment/             # Model training & evaluation
└── indices/                # Index construction (when ready)
```

## Deliverable

A validated SENI pipeline producing narrative indices across one or more domains, beginning with a feasibility report on available Sylheti news sources.

→ Full contribution framework: [`docs/COLLABORATION.md`](../../docs/COLLABORATION.md)
