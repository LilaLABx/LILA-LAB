# Research Collaboration Framework

## Contribute Your Research. Build the Multilingual AI Infrastructure Together.

> This is not a data extraction project. This is a **research collective** — a community of linguists, economists, NLP researchers, and data scientists building the measurement infrastructure for low-resource languages.

---

## Eight Ways to Contribute Research

### 1. Language Extension Paper 🆕
**Take the BENI pipeline, apply it to YOUR language, publish a comparative paper.**

```
Your language's news corpus
    → BENI pipeline (existing, proven)
    → Your language's narrative index
    → Cross-language comparison with Bangla
    → New paper: you as first author, we as co-authors
```

**What you need**: 5,000+ articles in your language + 1 annotator (you)
**What you get**: First-author publication + your language's first LLM-validated narrative index
**Innovation**: Every new language reveals something about how economic narratives work differently — you discover that.

**→ Template**: `papers/extensions/EXTENSION_TEMPLATE.md`

---

### 2. Cross-Domain Extension Paper 🆕
**Apply the narrative framework to a NEW domain — health, climate, education, politics.**

The BENI pipeline classifies "Economic" vs "Not Economic." Modify it to classify any domain:

```
Your domain's texts (health news, climate reports, education policy)
    → Modify the annotation schema
    → BENI pipeline (retrain classifier)
    → Your Health Narrative Index / Climate Narrative Index
    → New paper: domain-specific narrative measurement
```

**What you need**: Domain expertise + 3,000+ domain-tagged articles
**What you get**: First-author publication + opens a new measurement subfield
**Innovation**: You create the first climate narrative index for a low-resource language. Nobody has done this.

**→ Template**: `papers/extensions/EXTENSION_TEMPLATE.md`

---

### 3. Methodological Contribution 🧪
**Improve the pipeline itself — better classifier, cheaper annotation, smarter validation.**

| Improvement | Impact | Effort |
|-------------|--------|--------|
| Replace TF-IDF with a better baseline | +2–5% accuracy | 1–2 weeks |
| Compare open-source LLMs (Llama, Mistral) vs API-based (Claude, GPT) | Cost reduction 50–90% | 2–3 weeks |
| Active learning optimization — fewer labels, same accuracy | Reduces annotation bottleneck | 3–4 weeks |
| Time-series forecasting model for the index | New paper in itself | 4–6 weeks |
| Multilingual zero-shot transfer — train on Bangla, predict on Assamese | Breakthrough method | 6–8 weeks |

**What you get**: Methodological co-authorship + citation from every paper using your method
**Innovation**: You make the pipeline cheaper, faster, or more accurate — everyone benefits.

---

### 4. Replication + Validation ✓
**Independently reproduce our results. Publish a replication report.**

```bash
# Fork → reproduce → publish
git clone https://github.com/nabil0x/LILA-LAB
cd papers/paper2_systematic_review/replications/
python3 run_all_phases.py

# Write your replication report
cp papers/extensions/REPLICATION_TEMPLATE.md my_replication.md
# Fill in: which results replicated, which didn't, why
```

**What you need**: Python skills + critical thinking
**What you get**: Replication report published in this repository + potential co-authorship on a replication paper
**Innovation**: Science advances when results are independently verified.

**→ Template**: `papers/extensions/REPLICATION_TEMPLATE.md`

---

### 5. Citizen Science Annotation 📝
**Contribute annotations as a native speaker — no expertise required, just your language.**

We provide the guide, the interface, and the schema. You provide your native-language intuition.

```
Sign up → we send you 100 articles in your language → you label Economic / Not Economic
    → Your labels train the LLM → your language gets smarter AI
```

**What you need**: Native fluency in a language listed in our priority table
**What you get**: Acknowledgement in publications + your contribution recorded permanently
**Innovation**: The crowd intelligence model for low-resource language annotation — every label is valuable.

**→ Set up**: See `LINGUISTIC_CONTRIBUTION_GUIDE.md`

---

### 6. Policy & Application Brief 📊
**Use the index to write a policy analysis for your country.**

```
BENI index + your country's economic data
    → Policy brief: "What Bangla news narratives tell us about inflation expectations"
    → Published in this repository + submitted to policy outlets
```

**What you need**: Economics background + knowledge of your country's policy landscape
**What you get**: Co-authored policy brief + real-world impact
**Innovation**: Bridge between NLP research and policy-making — rare and valuable.

---

### 7. Infrastructure & Tooling 🛠️
**Build the tools that make the index usable.**

| Tool | Impact |
|------|--------|
| Interactive dashboard (Streamlit/Gradio) | Policymakers can explore the index |
| REST API for the index | Other researchers can query it programmatically |
| Mobile app for field data collection | Collect news from offline areas |
| Visualization library | Better communication of narrative trends |
| Automated report generator | Weekly economic narrative reports |

**What you need**: Web development, API design, or data visualization skills
**What you get**: Co-authorship on an infrastructure paper + your tool used by researchers across South Asia
**Innovation**: Your tool becomes the interface between cutting-edge NLP and real-world policy.

---

### 8. Teaching & Educational Materials 📖
**Create tutorials, courses, and documentation that train the next generation.**

```
BENI pipeline → Jupyter notebook tutorial → University course module
    → Students learn NLP + economics + low-resource languages simultaneously
```

**What you need**: Teaching experience + any technical background
**What you get**: Co-authorship on educational paper + your materials used in universities
**Innovation**: You train the people who will build the next generation of language technology.

---

## How Integration Works

### Option A: Git Repository Merge

The cleanest way to contribute a substantial research extension:

```
1. Fork this repository
2. Create your extension in papers/extensions/your_study/
3. Add your code, data, manuscript
4. Open a Pull Request
5. We review, merge, and you become a contributor
```

Your extension becomes a permanent part of this repository — cited, maintained, and discoverable alongside the core research.

### Option B: Git Submodule Link

If you prefer to maintain your own independent repository:

```
1. Develop your extension in your own repo
2. Open an issue in this repo with a link
3. We add your repo as a git submodule under papers/extensions/
4. Your repo stays yours — we link to it
```

Your work remains independent while being part of the collective infrastructure.

### Option C: Paper Submission

If you don't use git:

```
1. Submit your paper draft + data to ann.n.nabil@gmail.com
2. We review for fit with the research program
3. We collaborate on revisions
4. Paper gets published as part of the BENI extension series
```

---

## Academic Credit & Authorship

| Contribution Type | Credit Model |
|-------------------|-------------|
| Language Extension Paper | First author (you) + core team (us) |
| Cross-Domain Extension | First author (you) + core team (us) |
| Methodological Improvement | Shared co-authorship based on contribution |
| Replication Study | Sole or first author |
| Data + Annotation | Acknowledgement to co-author depending on volume |
| Policy Brief | Co-authorship |
| Infrastructure/Tooling | Co-authorship on dedicated tool paper |
| Educational Materials | Co-authorship on educational paper |

**All contributions** are recorded in `papers/contributions/OWNERS.csv` as a permanent scholarly record.

---

## The Innovation Model

This framework is designed to produce **novel, publishable contributions** at every level:

```
Level 1: Apply existing method to new language     → novel empirical result
Level 2: Apply existing method to new domain       → novel domain contribution
Level 3: Improve existing method                   → novel methodological contribution
Level 4: Create new tool/infrastructure             → novel infrastructure contribution
Level 5: Cross-language comparative analysis       → novel theoretical insight
```

**Every level is publishable.** You do not need to invent a new algorithm to make a valuable contribution. Applying the pipeline to Assamese and showing that economic narratives work differently in Assamese-language news is a novel, publishable finding.

---

## Start Here

```bash
# 1. Choose your contribution model (1–8 above)
# 2. Find the relevant template
ls papers/extensions/
cat papers/extensions/EXTENSION_TEMPLATE.md

# 3. Record your intent
echo "Your Name,Extension Author,papers/extensions,Apply BENI to Assamese,in_progress,2026-06-10," >> papers/contributions/OWNERS.csv

# 4. Build your extension and submit
```

**Questions?** Open a GitHub Discussion or email ann.n.nabil@gmail.com
