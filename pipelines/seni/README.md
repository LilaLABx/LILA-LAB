# SENI — Sylheti Exploration & Native-language Intelligence

> **Status**: 🔜 Seeking contributors
> **Language**: Sylheti (চিটাঙ্গ / ছিলটি) — 11M speakers
> **Region**: Sylhet region (Bangladesh) + diaspora

## Overview

SENI will bring the XENI pipeline to Sylheti, a language spoken by 11 million people in the Sylhet region of Bangladesh and a large diaspora community. Sylheti is primarily oral — developing news-based NLP infrastructure for it is a pioneering effort.

## Current State

- Pipeline structure: Ready (copy from `pipelines/template/`)
- Data collection: Needs identification of Sylheti news/digital media sources
- Annotation: Needs native speakers — Sylheti has limited written corpus, making this both challenging and impactful
- Index: First domain (economic) is the recommended starting point

## How to Contribute

We need:

| Role | What You Do |
|------|-------------|
| 🗣️ **Native Speaker** | Critical — validate annotations, help build written resources |
| 📊 **Researcher** | Lead the first index construction and paper |
| 💻 **Developer** | Adapt annotation pipeline for Sylheti's orthographic variation |
| 📰 **Data Collector** | Find Sylheti news sources (print, digital, social media) |

## Getting Started

```bash
# Copy the template to bootstrap
cp -r pipelines/template/* pipelines/seni/
cd pipelines/seni/
```

## Deliverable

A validated SENI pipeline producing narrative indices across one or more domains, with a first-author paper on Sylheti narratives (or your chosen domain).

**→ Full contribution framework:** [`COLLABORATION.md`](../../COLLABORATION.md)
