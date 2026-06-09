# LILA Lab — Communications Center

> **This repository is the command center** for LILA Lab's entire multi-channel presence.
> Every social platform, research repository, utility service, and community channel is documented, coordinated, and version-controlled from here.

---

## What This Is

The LILA Lab Communications Center is a **single source of truth** for:

- **What** — every channel we operate, its purpose, and its audience
- **When** — content cadence, campaign calendars, release synchronization
- **How** — brand voice, visual identity, cross-platform content flow
- **Who** — channel ownership, permissions, escalation paths

No channel operates in isolation. Every post, upload, and announcement is designed to feed into the others — creating a **network effect** where each platform amplifies the rest.

---

## Channel Map

```
                               ┌─────────────────────┐
                               │   LILA Lab           │
                               │   lila-lab.org       │
                               │   (GitHub Pages)     │
                               └──────────┬──────────┘
                                          │
            ┌─────────────────────────────┼─────────────────────────────┐
            │                             │                             │
            ▼                             ▼                             ▼
   ┌─────────────────┐        ┌─────────────────────┐       ┌─────────────────────┐
   │  SOCIAL          │        │  RESEARCH            │       │  UTILITY            │
   │  (audience)      │        │  (credibility)       │       │  (infrastructure)    │
   ├─────────────────┤        ├─────────────────────┤       ├─────────────────────┤
   │ X / Twitter      │        │ GitHub (⬡ this repo)│       │ Gradio Demo         │
   │ LinkedIn         │        │ OSF                 │       │ Website             │
   │ YouTube          │        │ Zenodo              │       │ Substack Newsletter │
   │ Facebook Page    │        │ Hugging Face        │       │ Discord Community   │
   │                  │        │ arXiv               │       │ Email (contact)     │
   │                  │        │ Google Scholar      │       │                     │
   │                  │        │ ORCID               │       │                     │
   └────────┬────────┘        └────────┬────────────┘       └─────────┬───────────┘
            │                          │                              │
            └──────────────────────────┼──────────────────────────────┘
                                       │
                                       ▼
                          ┌──────────────────────┐
                          │  COMMUNICATIONS.md    │
                          │  (this file)          │
                          │  ─ All channel docs   │
                          │    live in            │
                          │    communications/     │
                          │  ─ Content originates  │
                          │    from papers/ and   │
                          │    beni/ pipelines    │
                          └──────────────────────┘
```

---

## How Content Flows

```
papers/  ──→ research output ──→ OSF preprint + Zenodo DOI + arXiv
                │
                ├──→ GitHub release ──→ Hugging Face model/dataset
                │
                ├──→ Social post (X, LinkedIn) ──→ blog summary (Substack)
                │         │
                │         └──→ YouTube walkthrough video
                │
                └──→ Website update ──→ Community discussion (Discord)
```

**Rule**: Every content piece is created once and distributed multiple times through different channels — each channel getting the format it deserves.

---

## Directory Structure

| Path | Purpose |
|------|---------|
| `COMMUNICATIONS.md` | This file — hub entry point |
| `communications/CHANNELS.md` | Complete inventory: 15+ channels with purposes, URLs, owners |
| `communications/SOCIAL_MEDIA_STRATEGY.md` | X, LinkedIn, YouTube — content pillars, posting cadence, growth |
| `communications/RESEARCH_PLATFORMS.md` | OSF, Zenodo, HF, arXiv — sync protocol, upload manifests |
| `communications/BRAND_GUIDELINES.md` | LILA+XENI naming, voice, visual identity, color palette |
| `communications/COMMUNITY.md` | Discord, mailing list — contributor coordination framework |
| `communications/CONTENT_CALENDAR.md` | Scheduled posts, paper releases, event timelines |
| `communications/templates/` | Reusable post templates: X threads, LinkedIn, YouTube, Substack |

---

## Quick Start

```bash
# 1. Understand the full channel ecosystem
cat communications/CHANNELS.md

# 2. Read brand guidelines before posting anything
cat communications/BRAND_GUIDELINES.md

# 3. Check the content calendar for what's due
cat communications/CONTENT_CALENDAR.md

# 4. Find the template for whatever you need to publish
ls communications/templates/
```

---

## Related Documents

| Document | Connection |
|----------|------------|
| `DISTRIBUTION_STRATEGY.md` | Research platform upload manifests (OSF, Zenodo, HF, Mendeley) |
| `COLLABORATION.md` | How researchers contribute — includes communication about contributions |
| `README.md` | Public face of the repo — links to all channels |
| `CITATION.cff` | Citation metadata — used by every research platform |
| `papers/extensions/INDEX.md` | Extension registry — announced through social channels |

---

## Principles

1. **The repo is the source of truth.** All channel strategies are documented here, not in platform dashboards.
2. **Content is research-first.** Every post originates from actual research output (paper, dataset, pipeline improvement).
3. **Every channel has a job.** No channel exists without a defined purpose and audience.
4. **Cross-promotion is mandatory.** A paper upload to OSF triggers a social post, a newsletter issue, and a website update.
5. **One voice, many formats.** The same insight takes different forms on X (thread), LinkedIn (article), YouTube (walkthrough).
6. **Attribution is non-negotiable.** Every channel credits contributors, co-authors, and data sources.
