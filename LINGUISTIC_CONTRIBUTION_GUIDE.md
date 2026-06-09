# Linguistic Contribution Guide

## How to Contribute Your Native Language Data

> **You are not a data source. You are a collaborator.** This guide is for linguistic experts, native speakers, and language researchers who want to make LLMs understand their language.

---

## What We Need

### Tier 1: Text Corpus (Most Valuable)
A collection of **news articles, social media posts, or any written text** in your native language.

| Requirement | Minimum | Ideal |
|-------------|---------|-------|
| Articles | 1,000 | 50,000+ |
| Date range | Any | 2014–present |
| Topics | General news | Mix of economic, political, social |
| Format | Plain text or CSV | With date + source metadata |

**How to prepare:**
1. Collect text files (`.txt` or `.csv`)
2. Each file/row should have: the text content + date (if known) + source (if known)
3. Use the template at `papers/contributions/linguistic_data/text_submission_template.csv`

### Tier 2: Annotations (Expert Knowledge)
Label articles in your language as "Economic" or "Not Economic" — applying your cultural understanding.

**What counts as "Economic" in your language:**
- Inflation, prices, market conditions
- Exchange rates, remittances
- Employment, wages, labor
- Trade, tariffs, exports/imports
- Fiscal policy, government spending
- Business, industry, agriculture
- Infrastructure projects
- Any topic where money, resources, or economic well-being is discussed

**How to annotate:**
1. Download the annotation template: `papers/contributions/linguistic_data/annotation_template.csv`
2. For each article, set `label` to `economic` or `not_economic`
3. Add notes explaining your reasoning (especially for culturally specific cases)
4. Submit via pull request or email

### Tier 3: Dialectal Variants (Deep Expertise)
If your language has dialects or regional variants not well-covered by standard NLP:

- Provide parallel examples: "How X is said in the standard dialect vs. your dialect"
- Document idioms, metaphors, and culturally specific expressions
- Explain how economic concepts are expressed differently

**Template:** `papers/contributions/linguistic_data/dialect_template.csv`

---

## What Happens After You Submit

```
Your submission → We review for format → We run through the LLM pipeline
    → LLM extracts narratives in your language → You validate the outputs
    → We publish results with your co-authorship → Your language gets LLM infrastructure
```

**Step-by-step:**

1. **You submit** data via pull request, email, or shared drive
2. **We verify** format and metadata (2–5 business days)
3. **You are recorded** in `papers/contributions/OWNERS.csv` as a contributor
4. **We run the pipeline** — LLM annotation, classification, index construction
5. **You validate** — we send you a sample of LLM outputs. You correct cultural/linguistic errors
6. **We iterate** — your corrections retrain the model
7. **Publication** — any paper using your data includes you as co-author or in acknowledgements
8. **You own your data** — licensed CC BY 4.0 (you choose the license)

---

## What You Get

| Contribution | Recognition |
|-------------|-------------|
| 1,000+ articles | Acknowledgements in publications |
| 10,000+ articles + annotations | Co-authorship on papers using your data |
| Dialectal expertise + validation | Co-authorship + credit on model releases |
| Full pipeline contribution (data + annotation + validation) | First co-author on a language-specific paper |

Your row in `OWNERS.csv` serves as your permanent scholarly record for this contribution.

---

## Language Priority List

We are actively seeking contributions for:

| Language | Speakers | Priority | Status |
|----------|----------|----------|--------|
| Bangla (বাংলা) — Standard | 265M | ✅ Have pipeline | Active |
| Bangla — Chittagonian (চাঁটগাঁইয়া) | 13M | 🔴 High | No data |
| Bangla — Sylheti (ꠍꠤꠟꠐꠤ) | 11M | 🔴 High | No data |
| Bangla — Rangpuri (রংপুরী) | 15M | 🔴 High | No data |
| Assamese (অসমীয়া) | 15M | 🔴 High | No data |
| Nepali (नेपाली) | 25M | 🟡 Medium | No data |
| Maithili (मैथिली) | 12M | 🟡 Medium | No data |
| Odia (ଓଡ଼ିଆ) | 35M | 🟡 Medium | No data |
| Meitei (মৈতৈ) | 2M | 🟢 Interested | No data |
| My language? | — | — | Tell us! |

Don't see your language? Open an issue. The pipeline works for any language.

---

## Technical Requirements

### Text Submission Format
```csv
article_id,date,source,title,text,language,dialect
bd_001,2026-01-15,Daily Star,Bangla title here,"Full article text here...",bangla,standard
```

### Annotation Format
```csv
article_id,label,confidence,notes,annotator,date
bd_001,economic,high,"Discusses inflation impact on food prices",Your Name,2026-06-10
```

**Labels:** `economic` / `not_economic` / `uncertain`
**Confidence:** `high` / `medium` / `low`

---

## Ways to Submit

| Method | Best for | How |
|--------|----------|-----|
| **GitHub Pull Request** | Technical users | Fork repo, add data to `papers/contributions/linguistic_data/submissions/`, open PR |
| **Email** | Non-technical users | Email ann.n.nabil@gmail.com with your data |
| **Google Drive / Dropbox** | Large datasets | Share a link (ensure download permission) |
| **In-person / interview** | Dialect expertise | Contact us for a recorded session |

---

## FAQ

**Q: Do I need to know programming?**
A: No. Plain text files or CSV is enough. We handle the technical pipeline.

**Q: How much time does it take?**
A: Data collection: 2–10 hours depending on corpus size. Annotation: ~30 seconds per article.

**Q: Can I contribute data in a non-South-Asian language?**
A: Yes—but our current pipeline validation and publication focus is South Asia. Other languages welcome if we can find publication venues.

**Q: Will my data be used for commercial AI?**
A: Only if you choose a permissive license. You control the license. Default is CC BY 4.0 (attribution required).

**Q: Do I retain ownership of my language data?**
A: Yes. You license it to the project under your chosen open license. You can revoke future use at any time (published works already using it will keep their license).

**Q: I am a student. Can I contribute for my thesis?**
A: Yes — we actively support student contributors. Your contribution can form part of a dissertation chapter, and we provide letters confirming your role for ethics boards and supervisors.

---

## Start Here

```bash
# 1. Record your intent
echo "Your Full Name,Linguist,paper3,Contribute Assamese news corpus,in_progress,2026-06-10," >> papers/contributions/OWNERS.csv

# 2. Download the template
cp papers/contributions/linguistic_data/text_submission_template.csv my_language_submission.csv

# 3. Fill it with your data and submit
```

**Questions?** Open a GitHub Discussion or email ann.n.nabil@gmail.com
