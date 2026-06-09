# AENI — Assamese Exploration & Native-language Intelligence

> **Status**: 🔜 Seeking contributors
> **Language**: Assamese (অসমীয়া) — 15M speakers
> **Region**: Assam, India

## Overview

AENI will bring the XENI pipeline to Assamese, the official language of Assam. With 15 million speakers and a vibrant news ecosystem, Assamese is the next frontier for narrative measurement in South Asia.

## Current State

- Pipeline structure: Ready (copy from `pipelines/template/`)
- Data collection: Needs identification of major Assamese news sources
- Annotation: Needs native speakers for schema validation
- Index: First domain (economic) is the recommended starting point

## How to Contribute

We need:

| Role | What You Do |
|------|-------------|
| 🗣️ **Native Speaker** | Validate annotation schemas, review LLM outputs |
| 📊 **Researcher** | Lead the first index construction and paper |
| 💻 **Developer** | Adapt the LLM annotation pipeline for Assamese script |
| 📰 **Data Collector** | Identify and scrape Assamese news sources |

## Getting Started

```bash
# Copy the template to bootstrap
cp -r pipelines/template/* pipelines/aeni/
cd pipelines/aeni/
```

## Deliverable

A validated AENI pipeline producing narrative indices across one or more domains, with a first-author paper on Assamese economic narratives (or your chosen domain).

**→ Full contribution framework:** [`COLLABORATION.md`](../../COLLABORATION.md)
