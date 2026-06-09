# LILA Lab Pipelines

## Your Language. Your Data. Your Index.

**LILA Lab builds open-source NLP pipelines that let any low-resource language participate in the LLM revolution.**

We don't just talk about multilingual AI — we build the infrastructure for it. Our XENI pipeline framework takes raw native-language news and produces validated narrative indices across any domain — economics, health, climate, education, and beyond.

> **84% of NLP research is English-only.** If your language isn't served, you're invisible in the data that shapes global decisions.
>
> We fix that.

---

## What Is a XENI Pipeline?

**XENI** = [Language initial] + **E**xploration & **N**ative-language **I**ntelligence

Each language gets its own pipeline that:

1. **Collects** native-language news articles
2. **Annotates** them using LLM ensembles (Claude, GPT-4o, local models)
3. **Classifies** narratives into domain-specific categories (economic, health, climate, ...)
4. **Builds** monthly narrative indices for each domain
5. **Validates** against real-world indicators (CPI, health outcomes, climate data, ...)

**The result:** A reproducible, open-source narrative observatory for your language, capable of measuring discourse across any domain.

### Pipeline vs Index: How Naming Works

A XENI is the **pipeline** (the language instrument). Each pipeline can produce many **indices** across different domains.

```
          ┌─────────────────────────────────────────┐
          │  BENI (Bangla Exploration &              │
          │  Native-language Intelligence)           │
          │  ─ the pipeline, the instrument          │
          ├─────────────────────────────────────────┤
          │  Produces:                               │
          │  ├── BENI Economic Index   (proven)      │
          │  ├── BENI Health Index     (planned)     │
          │  ├── BENI Climate Index    (open)        │
          │  └── BENI [Domain] Index   (yours)      │
          └─────────────────────────────────────────┘
```

| Element | Convention | Example |
|---------|-----------|---------|
| **Pipeline** | XENI (language initial + ENI) | BENI, HENI, AENI |
| **Index** | XENI [Domain] Index | BENI Economic Index, HENI Health Index |

The self-teaching pattern works on **two levels**:
- **Language**: BENI → AENI → NENI → *your language here*
- **Domain**: BENI Economic Index → BENI Health Index → BENI Climate Index → *your domain here*

> BENI was always the Bangla pipeline, not the economic index. Its first index happened to be economic. The same instrument can now measure health discourse, climate narratives, education policy — whatever domain a research group builds a schema for.

---

## Active & Planned Pipelines

| Pipeline | Language | Speakers | Status | Index |
|----------|----------|----------|--------|-------|
| **BENI** | Bangla (বাংলা) | 265M | ✅ Active | 79 months (2014–2020) |
| **AENI** | Assamese (অসমীয়া) | 15M | 🔜 Planned | — |
| **NENI** | Nepali (नेपाली) | 25M | 🔜 Planned | — |
| **SENI** | Sylheti (চিটাঙ্গ) | 11M | 🔜 Planned | — |
| **CENI** | Chittagonian (চাঁটগাঁইয়া) | 16M | 🔜 Planned | — |

**Don't see your language?** Start a new pipeline — we'll help you set it up.

---

## Pipeline Structure

Every XENI pipeline follows the same structure, making it easy to replicate and extend:

```
[x]eni/
├── README.md              # Pipeline-specific documentation
├── annotation/            # LLM annotation pipeline (domain-agnostic core)
│   ├── schemas/           # Per-domain annotation schemas
│   │   ├── economic.json  # Economic narrative schema
│   │   ├── health.json    # Health discourse schema
│   │   └── ...            # Your domain here
│   ├── llm_annotate.py    # Multi-LLM annotation (works with any schema)
│   └── adjudicate.py      # Resolve disagreements
├── indices/               # Index construction — one subdirectory per domain
│   ├── eco/               # Economic narrative index
│   │   ├── build_index.py
│   │   └── validate.py    # Validate against CPI, FX, etc.
│   ├── health/            # Health discourse index
│   │   ├── build_index.py
│   │   └── validate.py    # Validate against health outcomes
│   └── ...                # Your domain here
├── experiment/            # Model training & evaluation
│   ├── train.py           # Train classifiers
│   └── evaluate.py        # Benchmark performance
├── database/              # Data storage
└── data/                  # Pipeline-specific data
```

### Shared Utilities

The `shared/` directory contains language-agnostic tools:

- `shared/annotation/` — LLM annotation framework (works with any language)
- `shared/classifiers/` — TF-IDF, BERT, and ensemble classifiers
- `shared/utils/` — Data processing, validation, and visualization

---

## Start Your Own Pipeline

### Step 1: Choose Your Language

Any low-resource language with a news ecosystem works. We prioritize:

| Priority | Languages | Status |
|----------|-----------|--------|
| 🔴 **High** | Assamese, Nepali, Sylheti, Chittagonian | Seeking contributors |
| 🟡 **Medium** | Maithili, Odia, Meitei, Rohingya | Open to proposals |
| 🟢 **Open** | Any underserved language | Welcome anytime |

### Step 2: Fork & Set Up

```bash
# Fork the repo, then:
cp -r pipelines/beni/ pipelines/[your-lang]/
cd pipelines/[your-lang]/

# Rename for your language (e.g., YOR for Yoruba, QUE for Quechua)
mv BENI_ROADMAP.md [YOUR-LANG]_ROADMAP.md
```

### Step 3: Adapt the Pipeline

1. **Annotation schema** — Define categories relevant to your language/context
2. **Data collection** — Identify news sources in your language
3. **LLM annotation** — Run the ensemble on your data
4. **Classifier training** — Train on your annotated data
5. **Index construction** — Build your monthly narrative index

### Step 4: Validate & Publish

- Compare your index against real-world indicators (CPI, health outcomes, climate data — whatever your domain calls for)
- Write up your methodology
- Submit to our paper series or your own venue

**We provide:** Templates, code, mentorship, and co-authorship opportunities.

---

## Proven Results (Bangla Pipeline)

The BENI pipeline demonstrates what's possible:

| Metric | Result |
|--------|--------|
| Classification accuracy | 91.7% (TF-IDF) |
| Monthly index built | 79 months (2014–2020) |
| Level correlation with CPI | r = −0.75 (p < 0.001) |
| Level correlation with FX rate | r = −0.72 (p < 0.001) |
| Data volume processed | 664,000+ articles |
| Papers published | 2 submitted, 4 in pipeline |

**This works. Now let's do it for your language.**

---

## Why Contribute?

### For Researchers

- **First-author paper** on your language's narratives — economics, health, climate, or your domain
- **Open-source pipeline** you can cite and build on
- **Validation data** for your language's NLP capabilities
- **Network** with researchers working on similar problems

### For Graduate Students

- **Publication-ready project** with clear methodology
- **Mentorship** from an active research lab
- **Skill development** in NLP, data science, and research communication
- **Collaboration opportunities** across languages and institutions

### For Language Communities

- **Representation** in global AI research
- **Tools** built for your language's specific needs
- **Documentation** of your language's narratives across domains
- **Voice** in conversations that shape policy

---

## How to Contribute

| Contribution | What You Do | What You Get |
|-------------|-------------|--------------|
| 🌍 **Language Extension** | Apply the pipeline to your language | First-author paper |
| 🔬 **Cross-Domain Extension** | Apply to health, climate, education | First-author paper |
| ⚙️ **Methodological** | Improve classifier, reduce cost | Co-authorship |
| ✅ **Replication** | Independently verify results | Replication report |
| 🗣️ **Citizen Annotation** | Label articles in your language | Acknowledgment |
| 📊 **Policy Brief** | Analyze narratives for policy | Co-authorship |
| 🛠️ **Infrastructure** | Build dashboards, APIs, tools | Tool paper co-authorship |
| 📖 **Education** | Create tutorials, course modules | Educational paper |

**→ Full framework:** [`COLLABORATION.md`](../COLLABORATION.md)

---

## Getting Started

### Quick Start (5 minutes)

```bash
# 1. Clone the repo
git clone https://github.com/nabil0x/LILA-LAB.git
cd LILA-LAB/pipelines/

# 2. Explore the BENI pipeline
ls beni/
cat beni/README.md

# 3. Run a test annotation
cd beni/annotation/
python llm_annotate.py --help
```

### For Researchers

```bash
# 1. Explore the BENI pipeline
cd pipelines/beni/

# 2. Run the baseline classifier
python3 experiment/beni_pilot/train.py --task economic --model-type tfidf

# 3. Build the narrative index
python3 experiment/beni_pilot/build_index.py --model-type tfidf
```

### For Developers

```bash
# 1. Set up the Discord bot
cd infrastructure/discord-bot/
cp .env.example .env
pip install -r requirements.txt
python bot.py

# 2. Contribute to the website
cd infrastructure/website/
# Edit index.html, styles.css
```

---

## Join the Community

- **Discord:** [discord.gg/TrrdKbky](https://discord.gg/TrrdKbky) — Ask questions, find collaborators, get help
- **Email:** lila.lab0x@gmail.com — For formal inquiries and partnerships
- **GitHub Issues:** [github.com/nabil0x/LILA-LAB/issues](https://github.com/nabil0x/LILA-LAB/issues) — Report bugs, request features, propose languages

---

## License

- **Code:** MIT License — Use, modify, distribute freely
- **Data:** CC BY 4.0 — Attribute the source
- **Papers:** © Authors — Cite properly
- **Contributions:** Attributed to contributor, shared under CC BY 4.0

---

**Your language is underserved by current AI. Let's change that — together.**
