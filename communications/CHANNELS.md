# LILA Lab — Channel Inventory

> Complete list of every channel LILA Lab operates, with purpose, audience, URL, and owner.

---

## Social Media

| Channel | Handle / URL | Purpose | Primary Audience | Post Cadence | Owner |
|---------|-------------|---------|------------------|-------------|-------|
| **X (Twitter)** | `@LILA_Lab` | Research updates, paper drops, thread summaries of findings, calls for contributors, NLP community engagement | NLP researchers, linguists, computational social scientists | 3–5×/week | Ann N. Nabil |
| **LinkedIn** | `/company/lila-lab` | Longer-form research commentary, collaboration recruitment, academic network building | Academics, university departments, policy institutions | 2–3×/week | Ann N. Nabil |
| **YouTube** | `@LILA_Lab` | Pipeline walkthroughs, paper presentations (5-min summaries), tutorial series, conference talk recordings | Visual learners, students, new contributors | 1×/week | Ann N. Nabil |
| **Facebook Page** | `/LILALabResearch` | Community outreach in South Asia, Bangla-language content, broader public awareness | General public in Bangladesh/India/Nepal | 1–2×/week | Ann N. Nabil |

---

## Research Platforms

| Platform | URL | Purpose | Content | Update Trigger |
|----------|-----|---------|---------|----------------|
| **GitHub** | `github.com/LilaLABx/LILA-LAB` | **Code of record**, collaboration hub, issue tracking, communications source of truth | All code, papers, docs, communications, templates | Continuous |
| **OSF** | `osf.io/[project-id]` | Open science project hub — front door for researchers | Preprints, protocols, figures, supplementary materials, links to everything | Paper submission |
| **Zenodo** | `doi.org/10.5281/zenodo.20585401` | Permanent DOI minting for datasets and code releases | Dataset archives, code snapshots, paper preprints | GitHub release |
| **Hugging Face** | `huggingface.co/nabil0x` | NLP community discovery — models, datasets, interactive demo | Fine-tuned models, narrative index dataset, Gradio space | Model training |
| **arXiv** | `arxiv.org/search/?query=LILA+Lab` | Paper preprints for citation and discoverability | Academic paper PDFs | Paper submission |
| **Google Scholar** | `scholar.google.com` | Citation tracking, researcher profile | All published papers | Paper publication |
| **ORCID** | `orcid.org/0009-0006-3561-045X` | Persistent researcher identifier | Ann N. Nabil's publication record | Paper publication |
| **Mendeley Data** | `data.mendeley.com/datasets/v362rp78dc` | Raw corpus distribution | Potrika Bangla News Corpus (upstream) | Corpus update |

---

## Utility Channels

| Channel | URL | Purpose | Content |
|---------|-----|---------|---------|
| **Website** | `lila-lab.org` (GitHub Pages) | Central brand landing page — links to all channels, showcases pipelines, lists contributors | Overview, pipeline maps, contributor directory, channel links |
| **Substack / Newsletter** | `lila.substack.com` | Monthly research digest for followers who prefer email | Monthly summary of new papers, datasets, pipeline improvements, contributor spotlights |
| **Discord** | `discord.gg/TrrdKbky` | Real-time community discussion, contributor coordination, Q&A, language annotation coordination | Discussion threads, annotation coordination, newcomer onboarding |
| **Email** | `lila.lab0x@gmail.com` | Direct contact for collaboration inquiries, paper submissions, media | Inquiries, proposals, support |

---

## Content Flow Rules

| From | To | Rule |
|------|----|------|
| Paper accepted | OSF, arXiv, Zenodo, GitHub release | Upload same day |
| arXiv upload | X, LinkedIn, Substack | Announce within 24h |
| New dataset | Zenodo, Hugging Face | DOI before announcement |
| GitHub release | Zenodo (auto), X, LinkedIn | Announce same day |
| YouTube video | X, LinkedIn, Facebook, Substack | Cross-post with link |
| Blog post (Substack) | X, LinkedIn, Facebook | Excerpt + link |
| New contributor | Discord welcome + OWNERS.csv | Same day |

---

## Analytics & Metrics

| Channel | Key Metric | Target | Tool |
|---------|-----------|--------|------|
| X | Impressions / engagement rate | → 10K impressions/mo | X Analytics |
| LinkedIn | Post views / connection growth | → 500 connections | LinkedIn Analytics |
| YouTube | Views / subscriber growth | → 100 subs | YouTube Studio |
| GitHub | Stars / forks / clones | → 50 stars | GitHub Insights |
| OSF | Views / downloads | → 500 views | OSF Analytics |
| Hugging Face | Model downloads | → 1K downloads | HF Dashboard |
| Substack | Subscribers / open rate | → 200 subs | Substack Analytics |
| Discord | Active members / messages | → 50 active | Discord Server Insights |

---

## Channel Ownership & Continuity

| Role | Person | Channels |
|------|--------|----------|
| **Maintainer** | Ann Naser Nabil | All channels — final approval on all content |
| **Channel Owner** | Ann Naser Nabil | All channels — daily operations |
| **Technical Co-owner** | Ann Naser Nabil | GitHub, HF, Zenodo, OSF, Website |

*As the lab grows, channel ownership can be delegated to contributors. The communications/ directory in this repo enables smooth handoff — everything is documented.*

---

## Onboarding a New Channel

To add a new channel:

1. Add it to this file with all fields populated
2. Add post templates in `communications/templates/`
3. Add the channel to the flow diagram in `COMMUNICATIONS.md`
4. Add to the content calendar in `communications/CONTENT_CALENDAR.md`
5. Update root `README.md` link section
