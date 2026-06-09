# X Thread Template

> Use for paper releases, pipeline announcements, and substantive research updates.

---

**Tweet 1 (Hook):**
> [One-line finding or announcement that creates curiosity]
>
> A thread 🧵 👇

**Tweet 2 (Problem):**
> [Why this matters — the problem we're solving]
>
> [1-2 sentences. Who is affected? Why hasn't this been done before?]

**Tweet 3 (What we did):**
> [Our approach in plain language]
>
> [1-2 sentences. What data, what method, what scale.]

**Tweet 4 (How it works — optional):**
> [Simple diagram or 3-step process]
>
> Step 1: [ ]
> Step 2: [ ]
> Step 3: [ ]
>
> [Attach figure/pipeline diagram]

**Tweet 5 (Results):**
> Key finding:
>
> [One result that surprises people]
>
> [Include chart/table visual]

**Tweet 6 (Impact):**
> What this means:
>
> [1-2 sentences on implications for the field]

**Tweet 7 (Call to action):**
> Want to contribute YOUR language?
>
> → [Link to COLLABORATION.md]
> → [Link to paper/dataset]
> → [Link to GitHub]
>
> #LILALab #LowResourceNLP

---

## Example (filled)

> 📢 New LILA Lab Technical Report: "How LILA-BENI Measures Economic Narratives in Bangla News"
>
> We analyzed 664K Bangla news articles using LLM-corrected labels and built a validated narrative index.
>
> Key finding: The Bangla economic narrative index correlates with CPI at r=-0.75 (p<0.001). News narratives track inflation — in Bangla.
>
> 🧵👇

> The problem: 84% of NLP research is in English. 0% is in Bangla, despite 265M speakers.
>
> Economic narratives drive inflation expectations — but we can't measure them outside English.
>
> We built the tool to fix that.

> Our approach:
> 1. Collected 664K Bangla news articles (Potrika corpus)
> 2. LLM-annotated 300 articles (Claude + GPT-4o ensemble)
> 3. Trained TF-IDF classifier on 3,200 labels → 88.2% accuracy
> 4. Built monthly index → validated against CPI, FX, reserves

> Results:
> 📊 Level correlation with CPI: r = −0.75
> 📊 Level correlation with FX: r = −0.72
> 📊 First proven economic narrative index for Bangla

> What this means:
> Economic narratives in Bangla news DO track real economic indicators.
> The pipeline works — and it's language-agnostic.
> Your language is next.

> Want to build this for YOUR language?
>
> → COLLABORATION.md explains how: [link]
> → Full paper: [OSF/arXiv link]
> → Code: [GitHub link]
>
> #LILALab #LowResourceNLP #BanglaNLP
