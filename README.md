# LILA Lab

## Language Intelligence for Low-resource Applications

### Your language. Your stories. Amplified by AI.

> 84% of NLP research is in English. 56% is US-focused. **0% is Bangla. 0% is Assamese. 0% is Sylheti. 0% is Chittagonian.**
>
> We are building the infrastructure that lets every language participate in the LLM revolution — starting with South Asia.

---

## To the Linguists, Native Speakers, and Language Experts of South Asia

**We need your expertise.**

Large Language Models are transforming how the world processes text — but they are blind to most of the world's languages. A model trained on English internet text does not understand the economic anxiety expressed in a Bangla newspaper, the agricultural metaphors of a Nepali farmer, or the code-switched conversation of a Dhaka street market.

This repository is a **collaborative platform** where linguistic experts contribute their native-language data, and we apply LLM infrastructure to extract insights, build indices, and improve multilingual AI cognition.

**You bring the language. We bring the LLM pipeline. Together we build AI that understands your world.**

---

## What We Have Already Built

A complete, production-tested pipeline that takes raw native-language news and produces validated measurements:

```
Raw Bangla news articles (664,000+)
    → LLM annotation (Claude, GPT-4o ensemble)
    → Multi-model classification (TF-IDF, BanglaBERT)
    → Monthly narrative index
    → Macroeconomic validation (CPI, FX, reserves)
    → Published papers + open-source code
```

**Proven in Bangla (265M speakers). Ready for your language.**

| Benchmark | Result |
|-----------|--------|
| Classification accuracy | 91.7% (TF-IDF), expected higher with LLM labels |
| Monthly index built | 79 months (2014–2020) |
| Level correlation with CPI | r = −0.75 (p < 0.001) |
| Level correlation with FX | r = −0.72 (p < 0.001) |
| Papers published | 2 submitted, 4 in pipeline |
| LLM annotation cost | ~$0.02/article (Claude), ~$0.03/article (GPT-4o) |

---

## Why Your Linguistic Expertise Is Irreplaceable

LLMs fail at low-resource languages in specific, predictable ways. You can fix them:

| Problem | How Linguists Help |
|---------|-------------------|
| **Wrong sentiment** — LLM misreads cultural tone | You annotate with native context |
| **Missing idioms** — "Price hike eats the salt" makes no sense to GPT | You document local metaphors |
| **Code-switching** — Bangla-English mixed in one sentence | You provide real-world bilingual data |
| **Dialect gaps** — Standard Bangla ≠ Chittagonian ≠ Sylheti | You contribute dialectal variants |
| **Topic blindness** — "Rickshaw fare increase" is economic news but LLM classifies it as transport | You define the economic narrative frame |
| **Historical amnesia** — Pre-2020 data is not on the internet | Your community archives are the only source |

**Every annotation, every correction, every cultural insight you contribute makes the LLM smarter for your language.**

---

## How to Contribute Your Language Data

### 1. Submit Text Data

We need **native-language news articles, social media posts, or any text** in your language. Minimum 1,000 articles.

→ Use the template at [`papers/contributions/linguistic_data/`](papers/contributions/linguistic_data/)

### 2. Annotate for Economic Relevance

Label articles as "Economic" or "Not Economic" in your language — with cultural context.

→ Guide: [`LINGUISTIC_CONTRIBUTION_GUIDE.md`](LINGUISTIC_CONTRIBUTION_GUIDE.md)

### 3. Validate LLM Outputs

Review what the LLM extracted from your language data. Correct its mistakes. Teach it your language's narrative patterns.

### What You Get in Return

- **Co-authorship** on papers that use your data (you are not a data source — you are a collaborator)
- **Your language's first LLM-validated narrative index**
- **Attribution** in all publications, datasets, and model releases
- **Your contribution recorded** in `papers/contributions/OWNERS.csv` as a permanent scholarly record
- **A working LLM pipeline** trained on your language — use it for your own research

---

## 🎯 Research Collaboration: Eight Ways to Contribute

> Linguistic data is one path. There are **seven more** — and they all lead to co-authored publications.

This framework is designed so that **every contributor can earn academic authorship** — whether you build a new language extension, replicate our results, improve the pipeline, or write a policy brief.

| Contribution Model | What You Do | What You Get |
|--------------------|-------------|--------------|
| 🌍 **Language Extension** | Apply the pipeline to YOUR language | First-author paper |
| 🔬 **Cross-Domain Extension** | Apply to health, climate, education | First-author paper |
| ⚙️ **Methodological** | Improve classifier, reduce cost | Co-authorship |
| ✅ **Replication** | Independently verify results | Replication report |
| 🗣️ **Citizen Annotation** | Label articles in your language | Acknowledgment |
| 📊 **Policy Brief** | Analyze narratives for policy | Co-authorship |
| 🛠️ **Infrastructure** | Build dashboards, APIs, tools | Tool paper co-authorship |
| 📖 **Education** | Create tutorials, course modules | Educational paper |

**→ Full framework with templates:** [`COLLABORATION.md`](COLLABORATION.md)
**→ Extension registry + templates:** [`papers/extensions/`](papers/extensions/)
**→ Submodule integration guide:** [`SUBREPOS.md`](SUBREPOS.md)

---

## 📡 Communications Center

> This repository is the **command center** for LILA Lab's entire multi-channel presence — social media, research platforms, community spaces, and infrastructure.

| Channel Layer | Channels | Managed In |
|--------------|----------|-----------|
| 🐦 **Social** | X (`@LILA_Lab`), LinkedIn, YouTube, Facebook | [`communications/SOCIAL_MEDIA_STRATEGY.md`](communications/SOCIAL_MEDIA_STRATEGY.md) |
| 📄 **Research** | GitHub, OSF, Zenodo, Hugging Face, arXiv, Google Scholar, ORCID | [`communications/RESEARCH_PLATFORMS.md`](communications/RESEARCH_PLATFORMS.md) |
| 💬 **Community** | Discord, email, monthly lab calls | [`communications/COMMUNITY.md`](communications/COMMUNITY.md) |
| 🎨 **Brand** | LILA+XENI naming, voice, visual identity | [`communications/BRAND_GUIDELINES.md`](communications/BRAND_GUIDELINES.md) |
| 📅 **Calendar** | Scheduled posts, paper releases, milestones | [`communications/CONTENT_CALENDAR.md`](communications/CONTENT_CALENDAR.md) |
| 📝 **Templates** | X threads, LinkedIn articles, YouTube scripts, newsletters | [`communications/templates/`](communications/templates/) |

**→ Full communications hub:** [`COMMUNICATIONS.md`](COMMUNICATIONS.md)

---

## How This Makes LLMs Smarter for Your Language

The pipeline works like this:

```
Your language text → LLM extracts narratives → we validate with you → we build a cognitive model of how your language expresses economic concepts → we fine-tune open-source LLMs → better AI for your language
```

**This is not "data extraction." This is cognitive infrastructure.** Every linguistic insight you contribute is encoded into the LLM's understanding of how your language thinks about the world.

---

## For the Research Community

This repository is also home to the **LILA Lab Technical Report Series** — a 6-paper academic research program on economic narrative measurement in low-resource languages. The papers provide the methodological foundation for the linguistic data work.

| Paper | Title | Status |
|-------|-------|--------|
| **1** | Statistical Economics | ✅ Complete |
| **2** | Economic Narrative Indices: Systematic Review (2007–2025) | ✅ Submitted to arXiv |
| **3** | Building Local-Language Economic Narrative Indices | 🔄 Active (July 2026) |
| **4** | Nowcasting Inflation with BENI | 📋 Planned (Aug 2026) |
| **5** | Text as Data in Social Science (1916–2026) | 📋 Planned (Oct 2026) |
| **6** | LLMs as Measurement Devices | 💡 Proposed (Jan 2027) |

→ Full details: [`papers/README.md`](papers/README.md)

---

## Repository Map

```
economic narrative indices/
│
├── 📋 COMMUNICATIONS.md                 ← LILA Lab's multi-channel command center
├── 📋 COLLABORATION.md                 ← START HERE for research collaboration
├── 📋 LINGUISTIC_CONTRIBUTION_GUIDE.md ← START HERE if you're a linguist
├── 📋 README.md                          ← This file
├── 📋 CONTRIBUTING.md                    ← General contribution guide
├── 📋 SUBREPOS.md                        ← Git submodule integration guide
│
├── 📁 papers/contributions/linguistic_data/   ← Templates for data submission
│
├── 📁 papers/                        ← 6 research papers
│   ├── 📋 CONTRIBUTING.md             ← Standard contribution workflows
│   ├── 📁 contributions/              ← Ownership logs, screening records
│   ├── 📁 extensions/                 ← Research extension registry + templates
│   │   ├── 📋 INDEX.md                ← Active extensions listing
│   │   ├── 📋 EXTENSION_TEMPLATE.md   ← Extension proposal template
│   │   └── 📋 REPLICATION_TEMPLATE.md ← Replication report template
│   ├── paper2_systematic_review/      ← Paper 2
│   ├── paper3_beni_method/            ← Paper 3 (BENI Pipeline)
│   ├── paper4_beni_nowcasting/        ← Paper 4 (Nowcasting)
│   ├── paper5_text_as_data_survey/    ← Paper 5 (Survey)
│   └── paper6_llm_narrative_extraction/ ← Paper 6 (LLM Extraction)
│
├── 📁 communications/                 ← Multi-channel command center
│   ├── 📋 CHANNELS.md                  ← 15+ channels with purposes, URLs, sync rules
│   ├── 📋 BRAND_GUIDELINES.md          ← LILA+XENI naming, voice, visual identity
│   ├── 📋 SOCIAL_MEDIA_STRATEGY.md    ← X, LinkedIn, YouTube content plan
│   ├── 📋 RESEARCH_PLATFORMS.md       ← OSF, Zenodo, HF, arXiv integration
│   ├── 📋 COMMUNITY.md                ← Discord, contributor coordination
│   ├── 📋 CONTENT_CALENDAR.md         ← Scheduled posts, release timelines
│   └── 📁 templates/                   ← Reusable post templates per platform
│
├── 📁 beni/                           ← Core codebase & data (39 GB)
│   ├── annotation/                     ← LLM annotation pipeline
│   ├── index/                          ← Index construction
│   ├── experiment/                     ← Model training & evaluation
│   └── figures/                        ← Paper figures
│
├── 📁 data-paper/                     ← BENI v1 data release
├── 📁 distribution/                   ← Platform distribution manifests
└── 📁 archive/                        ← Archived files
```

---

## Quick Start

### For Linguistic Contributors
```bash
# 1. Read the guide
cat LINGUISTIC_CONTRIBUTION_GUIDE.md

# 2. Check what languages are most needed
ls papers/contributions/linguistic_data/

# 3. Record your intent
echo "Your Name,Linguist,paper3,Annotate Assamese economic news,in_progress,2026-06-10," >> papers/contributions/OWNERS.csv
```

### For Researchers
```bash
# Train the TF-IDF baseline (no GPU)
cd beni/experiment/beni_pilot/
python3 train.py --task economic --model-type tfidf --data-source potrika-timeseries
python3 build_index.py --model-type tfidf
python3 correlate.py
```

---

## Data Sources

| Dataset | Language | Size | License |
|---------|----------|------|---------|
| Potrika Bangla News | Bangla (বাংলা) | 3.3 GB | CC BY 4.0 |
| Bangla News Database | Bangla (বাংলা) | ~14 GB | — |
| BNLP News Categorization | Bangla (বাংলা) | 56 MB | CC BY-NC-SA 4.0 |

**YOUR LANGUAGE HERE** — submit via the linguistic contribution guide.

---

## Languages We Want to Cover

**Immediate priority:** Bangla dialects (Chittagonian, Sylheti, Rangpuri), Assamese, Nepali, Maithili, Odia, and other under-represented languages of Bangladesh, Northeast India, Nepal, and Myanmar.

**The pipeline is language-agnostic.** If you speak it, we can process it.

---

## Contact

**Ann Naser Nabil** — Department of Economics, Jahangirnagar University
ann.n.nabil@gmail.com | [ORCID](https://orcid.org/0009-0006-3561-045X)

Open an issue or start a discussion for linguistic data contributions.

---

## License

- **Code**: MIT License
- **Data**: CC BY 4.0 (unless otherwise specified by contributor)
- **Papers**: © Ann Naser Nabil
- **Linguistic contributions**: Attributed to contributor, shared under CC BY 4.0
