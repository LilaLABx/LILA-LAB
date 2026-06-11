# LILA Lab

**Language Intelligence for Low-resource Applications**

Your language. Your stories. Amplified by AI.

> 84% of NLP research is in English. 56% is US-focused. **0% is Bangla. 0% is Assamese. 0% is Hausa. 0% is Swahili.**
>
> We are building the infrastructure that lets every language participate in the LLM revolution — targeting 10 emerging-economy languages by 2027.

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/code-MIT-green)](./LICENSE)
[![License: CC BY 4.0](https://img.shields.io/badge/data-CC%20BY%204.0-lightgrey)](https://creativecommons.org/licenses/by/4.0/)
[![Discord](https://img.shields.io/badge/discord-join-7289DA?logo=discord)](https://discord.gg/TrrdKbky)
[![Target](https://img.shields.io/badge/target-10%20emerging%20economies-006D77)](dataset/README.md)

---

## Table of Contents

- [What Is LILA Lab?](#what-is-lila-lab)
- [The XENI Pipeline Framework](#the-xeni-pipeline-framework)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
  - [For Researchers](#for-researchers)
  - [For Linguistic Contributors](#for-linguistic-contributors)
  - [For Developers](#for-developers)
- [Repository Overview](#repository-overview)
- [Project Status & Results](#project-status--results)
- [How to Contribute](#how-to-contribute)
- [How to Cite](#how-to-cite)
- [Community & Contact](#community--contact)
- [License](#license)

---

## What Is LILA Lab?

LILA Lab is a research collective building **open-source NLP pipelines** that let any low-resource language participate in the LLM revolution. We don't just talk about multilingual AI — we build the infrastructure for it.

Our first pipeline, **BENI** (Bangla Exploration & Native-language Intelligence), is proven and production-tested:

```
Raw Bangla news articles (664,000+)
    → LLM annotation (Claude, GPT-4o ensemble)
    → Multi-model classification (TF-IDF, BanglaBERT)
    → BENI Economic Index (monthly narrative index)
    → Macroeconomic validation (CPI, FX, reserves)
    → Published papers + open-source code
```

**Proven in Bangla (265M speakers). Targeting 10 emerging-economy languages by 2027. Ready for your language and domain.**

See the [pipeline flowchart](docs/PIPELINE_FLOW.md) for a visual walkthrough of each stage.

---

## The XENI Pipeline Framework

**XENI** stands for **[Language initial] + Exploration & Native-language Intelligence**. Each language gets its own pipeline that collects native-language news, classifies narratives across domains, and produces validated monthly indices.

Every XENI pipeline follows the same structure:

```
[x]eni/
├── annotation/          # LLM annotation pipeline (domain-agnostic)
│   ├── schemas/         # Per-domain annotation schemas
│   ├── llm_annotate.py  # Multi-LLM annotation (Claude, GPT-4o, ...)
│   └── adjudicate.py    # Resolve annotation disagreements
├── indices/             # Index construction — one subdirectory per domain
│   ├── eco/             # Economic narrative index
│   │   ├── build_index.py
│   │   └── validate.py  # Validate against CPI, FX, etc.
│   └── health/          # (planned)
├── experiment/          # Model training & evaluation
├── database/            # Data storage
└── data/                # Pipeline-specific data
```

| Element | Convention | Example |
|---------|-----------|---------|
| **Pipeline** | XENI (language initial + ENI) | BENI, AENI, NENI |
| **Index** | XENI [Domain] Index | BENI Economic Index |

A single pipeline can produce many domain indices. BENI's first index happens to be economic — the same instrument can measure health, climate, or education narratives.

**Target: 10 emerging-economy low-resource languages by H1 2027.**

| Pipeline | Language | Region | Speakers | Dataset | Status |
|----------|----------|--------|----------|---------|--------|
| **BENI** | Bangla (বাংলা) | South Asia | 265M | ✅ 664k articles | ✅ Active |
| **AENI** | Assamese (অসমীয়া) | South Asia | 15M | 🔴 Not started | 🔜 Seeking contributors |
| **NENI** | Nepali (नेपाली) | South Asia | 25M | 🔴 Not started | 🔜 Seeking contributors |
| **SENI** | Sylheti (চিটাঙ্গ) | South Asia | 11M | 🔴 Not started | 🔜 Planned |
| **CENI** | Chittagonian (চাঁটগাঁইয়া) | South Asia | 16M | 🔴 Not started | 🔜 Planned |
| **HENI** | Hausa | Africa | 80M | 🔴 Not started | 🔜 Planned |
| **KIENI** | Kiswahili (Swahili) | Africa | 100M | 🔴 Not started | 🔜 Planned |
| **VIENI** | Vietnamese (Tiếng Việt) | SE Asia | 100M | 🔴 Not started | 🔜 Planned |
| **TIENI** | Tagalog (Filipino) | SE Asia | 80M | 🔴 Not started | 🔜 Planned |
| **IDENI** | Indonesian (Bahasa Indonesia) | SE Asia | 200M | 🔴 Not started | 🔜 Planned |

**Don't see your language?** [Start a new pipeline.](#how-to-contribute) — see the full [dataset tracker](dataset/README.md) for collection progress.

---

## Prerequisites

- **Python 3.10+** — the entire pipeline ecosystem targets 3.10+
- **Git** — for cloning and contributing
- **pip** — Python package manager
- **Optional:** A Discord account if you want to [join the community](https://discord.gg/TrrdKbky)

For LLM annotation (Claude, GPT-4o), you'll need API keys from [Anthropic](https://console.anthropic.com/) and/or [OpenAI](https://platform.openai.com/). The pipeline gracefully degrades — you can still run classification and index construction without them.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/LilaLABx/LILA-LAB.git
cd LILA-LAB
```

### 2. Install core dependencies

```bash
pip install -e ".[core]"
```

This installs the shared pipeline library (`pandas`, `scikit-learn`, `numpy`, etc.) defined in [`pyproject.toml`](pyproject.toml).

### 3. (Optional) Install LLM annotation extras

```bash
pip install -e ".[llm]"      # For running LLM annotation (Claude, GPT)
pip install -e ".[dev]"      # For development (ruff, pytest)
pip install -e ".[all]"      # Everything above
```

### 4. (Optional) Install BENI pilot experiment dependencies

```bash
cd pipelines/BENI/experiment/beni_pilot
pip install -r requirements.txt
cd ../../..
```

This adds `torch`, `transformers`, `streamlit`, and other experiment-specific packages.

---

## Quick Start

### For Researchers

Run the BENI pilot baseline — from clone to narrative index in a few commands:

```bash
# 1. Install dependencies (see Installation section above)

# 2. Train the baseline TF-IDF classifier
cd pipelines/BENI/experiment/beni_pilot
python3 train.py --task economic --model-type tfidf --data-source potrika-timeseries

# 3. Build the 79-month BENI Economic Index
python3 build_index.py

# 4. Correlate with macroeconomic indicators (CPI, FX, reserves)
python3 correlate.py
```

**What you'll get:** A monthly narrative index (2014–2020), model artifacts, and correlation reports. See [`pipelines/beni/experiment/beni_pilot/README.md`](pipelines/beni/experiment/beni_pilot/README.md) for full documentation.

**Need the Potrika dataset?** Download it from [Mendeley Data](https://data.mendeley.com/datasets/v362rp78dc/4) (3.3 GB, CC BY 4.0) and place it in `pipelines/BENI/data/raw/potrika/`.

### For Linguistic Contributors

Want to bring the XENI pipeline to your language?

```bash
# 1. Read the contribution guide
cat docs/LINGUISTIC_CONTRIBUTION_GUIDE.md

# 2. Check which languages are most needed
cat technical-reports/extensions/INDEX.md

# 3. Register as a contributor
# Use /register in Discord or email lila.lab0x@gmail.com
```

**No coding required.** We need native speakers for annotation, schema design, and language expertise.

### For Developers

```bash
# 1. Set up the Discord bot
cd infrastructure/discord-bot/
cp .env.example .env
# Edit .env with your bot token
pip install -r requirements.txt
python bot.py

# 2. Work on the website
cd infrastructure/website/
# Files: dashboard.html, dashboard-styles.css, dashboard.js
# Open dashboard.html in a browser to preview
```

---

## Repository Overview

```
lila-lab/
├── .github/                    # CI workflows, issue templates, funding
├── .vscode/                    # Workspace settings, recommended extensions
│
├── pipelines/                  # XENI Pipeline Collection (10 emerging economies)
│   ├── BENI/                   # Bangla ✅ (proven)
│   ├── AENI/...                # 9 more bootstrapped pipelines
│   ├── LAB/                    # Annotation infrastructure (AAL, TAL)
│   ├── shared/                 # Language-agnostic utilities
│   └── template/               # Bootstrap template (start here for new languages)
│
├── dataset/                    # Raw corpora + processed releases per language
├── registry/                   # Central registry (languages, schemas, publications)
├── api/                        # REST API (planned)
├── cli/                        # CLI tool (planned)
├── dist/                       # Distribution manifests (Zenodo, HuggingFace, OSF)
│
├── technical-reports/          # 6-paper research series
├── communications/             # Brand, social media, community strategy
├── infrastructure/             # Discord bot, website, scripts
│
├── tests/                      # Shared test infrastructure
└── docs/                       # Website (GitHub Pages) + documentation guides
```

**Key entry points:**
- [`pipelines/README.md`](pipelines/README.md) — full pipeline framework documentation
- [`pipelines/BENI/README.md`](pipelines/BENI/README.md) — BENI deep dive
- [`registry/languages.json`](registry/languages.json) — language registry & pipeline status
- [`registry/publications.bib`](registry/publications.bib) — full publication bibliography
- [`docs/COLLABORATION.md`](docs/COLLABORATION.md) — full contribution framework
- [`docs/LINGUISTIC_CONTRIBUTION_GUIDE.md`](docs/LINGUISTIC_CONTRIBUTION_GUIDE.md) — guide for language contributors

---

## Project Status & Results

### BENI Benchmark

| Metric | Result |
|--------|--------|
| Classification accuracy | 91.7% (TF-IDF) |
| Monthly index built | 79 months (2014–2020) |
| Level correlation with CPI | r = −0.75 (p < 0.001) |
| Level correlation with FX | r = −0.72 (p < 0.001) |
| Papers published | 2 submitted, 4 in pipeline |

### Paper Series

| Paper | Title | Status |
|-------|-------|--------|
| 1 | Statistical Economics of Narrative | ✅ Complete |
| 2 | Economic Narrative Indices: Systematic Review | ✅ Submitted |
| 3 | Building BENI Pipeline | 🔄 Active (July 2026) |
| 4 | Nowcasting Inflation with BENI | 📋 Planned (Aug 2026) |
| 5 | Text as Data in Social Science | 📋 Planned (Oct 2026) |
| 6 | LLMs as Measurement Devices | 💡 Proposed (Jan 2027) |

**Full details:** [`technical-reports/README.md`](technical-reports/README.md)

---

## How to Contribute

| Model | What You Do | What You Get |
|-------|-------------|--------------|
| 🌍 **Language Extension** | Apply the pipeline to YOUR language | First-author paper |
| 🔬 **Cross-Domain Extension** | Apply to health, climate, education | First-author paper |
| ⚙️ **Methodological** | Improve classifier, reduce cost | Co-authorship |
| ✅ **Replication** | Independently verify results | Replication report |
| 🗣️ **Citizen Annotation** | Label articles in your language | Acknowledgment |
| 📊 **Policy Brief** | Analyze narratives for policy | Co-authorship |
| 🛠️ **Infrastructure** | Build dashboards, APIs, tools | Tool paper co-authorship |
| 📖 **Education** | Create tutorials, course modules | Educational paper |

**→ Full framework:** [`docs/COLLABORATION.md`](docs/COLLABORATION.md)

---

## How to Cite

If you use LILA Lab pipelines or data in your research:

```bibtex
@software{lila_lab,
  author = {Nabil, Ann Naser and others},
  title = {LILA Lab: Language Intelligence for Low-resource Applications},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/LilaLABx/LILA-LAB}
}
```

For individual papers in the series, see [`technical-reports/README.md`](technical-reports/README.md) for specific citations.

---

## Community & Contact

- **Discord:** [discord.gg/TrrdKbky](https://discord.gg/TrrdKbky) — Ask questions, find collaborators, get help
- **Email:** [lila.lab0x@gmail.com](mailto:lila.lab0x@gmail.com) — Formal inquiries and partnerships
- **GitHub Issues:** [Open an issue](https://github.com/LilaLABx/LILA-LAB/issues) — Bug reports, feature requests, language proposals
- **X (Twitter):** [@LILA_Lab](https://x.com/LILA_Lab)
- **Website:** [lilalab.pro.bd](https://lilalab.pro.bd/)

**Maintainer:** Ann Naser Nabil — Department of Economics, Jahangirnagar University ([ORCID](https://orcid.org/0009-0006-3561-045X))

---

## License

- **Code:** MIT License — Use, modify, distribute freely
- **Data:** CC BY 4.0 — Attribute the source
- **Papers:** © Ann Naser Nabil
- **Contributions:** Attributed to contributor, shared under CC BY 4.0

---

**Your language is underserved by current AI. Let's change that — together.**
