# LILA Lab — Brand Guidelines

> How we present ourselves across every channel. This is the single source of truth for LILA Lab's visual and verbal identity.

---

## 1. The Brand Architecture

```
LILA Lab
├── Name: Language Intelligence for Low-resource Applications
├── Pronunciation: /ˈliːlə/ (LEE-lah)
├── Tagline: "Your language. Amplified by AI."
├── Vibe: Academic rigor × South Asian cultural roots × open collaboration
│
├── Pipelines (XENI naming system):
│   ├── BENI  → Bangla  Exploration & Native-language Intelligence (Bangladesh)
│   ├── AENI  → Assamese  " (Assam, India)
│   ├── NENI  → Nepali  " (Nepal)
│   ├── SENI  → Sylheti  " (Sylhet region)
│   ├── CENI  → Chittagonian  " (Chittagong region)
│   └── [X]ENI → [Language] Exploration & Native-language Intelligence
│
└── The ENI suffix means "Exploration & Native-language Intelligence"
    First letter = language initial (e.g., B for Bangla, A for Assamese)
```

### Why LILA?

**Lila** (লীলা / लीला / লীলা) in Sanskrit, Bangla, Hindi, Nepali, and Assamese means *divine play, creative exploration, cosmic rhythm*. It captures:

- **Exploration** — discovering how languages think about the world
- **Creativity** — building new tools at the intersection of linguistics and AI
- **Playfulness** — the joy of scientific discovery
- **South Asian roots** — the name belongs to the region the project serves

### Why XENI?

Every pipeline is an **XENI** — [Language initial] + **E**xploration & **N**ative-language **I**ntelligence.

```
BENI = Bangla Exploration & Native-language Intelligence
AENI = Assamese Exploration & Native-language Intelligence
```

The naming is **self-teaching**: a contributor who sees "BENI" and "AENI" instantly understands the pattern and knows that their language fits as "[initial]ENI."

---

## 2. Brand Voice

| Dimension | How We Sound |
|-----------|-------------|
| **Tone** | Warm, precise, confident — never hype |
| **Formality** | Professional but not academic-stuffy. Write like a senior researcher explaining to a curious peer |
| **Audience** | Linguistic experts, NLP researchers, economists, data scientists, native speakers — all equally welcome |
| **First-person** | Use "we" — LILA Lab is a collective, not a solo project |
| **Cultural awareness** | Never "exoticize" low-resource languages. They are not "untapped" or "discovered." They are underserved by current technology. |
| **Citations** | Always cite contributors, data sources, and prior work. Attribution is non-negotiable. |

### Voice Examples

| ✅ Do | ❌ Don't |
|-------|----------|
| "We built a pipeline to measure economic narratives in Bangla" | "We revolutionized NLP" |
| "Your language is underserved by current LLMs. We can change that together." | "Your language is primitive according to AI" |
| "BENI achieves 88.2% accuracy on gold-standard human annotations" | "BENI crushes benchmarks" |
| "This framework is designed for easy adaptation to new languages" | "One-click language support" |

---

## 3. Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| **Umbrella** | LILA Lab | LILA Lab |
| **Pipeline** | XENI (language initial + ENI) | BENI, AENI, NENI |
| **Full name** | [Language] Exploration & Native-language Intelligence | Bangla Exploration & Native-language Intelligence |
| **Papers** | "LILA Technical Report #N: Title" | "LILA Technical Report #3: Building BENI" |
| **Series** | LILA Technical Report Series | — |
| **Data releases** | `lila-{pipeline}-{version}` | `lila-beni-v1.0` |
| **Tags** | `lila-lab`, `lila-{pipeline}`, `{language}-nlp` | `lila-benai`, `bangla-nlp` |

### Transition from BENI (old) to LILA (new)

| Context | Old | New |
|---------|-----|-----|
| Repository | `economic-narrative-indices` | `lila-lab` (future rename) |
| Research program | "BENI Research Program" | "LILA Lab Technical Reports" |
| Bangla pipeline | BENI (stays) | BENI (no change — it was always BENI) |
| Acknowledgements | "BENI research program" | "LILA Lab" |

**Key point**: Existing BENI papers remain valid. BENI was always the Bangla pipeline. It still is. What changes is the *umbrella organization* — from "BENI Research Program" to "LILA Lab."

---

## 4. Color Palette

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| Primary | Deep Teal | `#006D77` | Headers, logos, primary buttons |
| Secondary | Warm Gold | `#E29578` | Accents, highlights, calls to action |
| Background | Light Sand | `#FFDDD2` | Card backgrounds, subtle sections |
| Neutral | Charcoal | `#2D3748` | Body text |
| Light | White | `#FFFFFF` | Page background |
| Accent | Coral | `#E76F51` | Warnings, new items, attention |

*Rationale*: The palette is inspired by South Asian natural tones — river teal, harvest gold, desert sand. It feels regionally grounded without being stereotypical.

---

## 5. Logo & Visual Elements

*Pending design. Placeholder rules:*

| Element | Rule |
|---------|------|
| **Wordmark** | "LILA Lab" in title case, no hyphen |
| **Icon** | Consider: stylized ব (Bangla letter) or leaf/network motif |
| **Minimum size** | Wordmark never below 24px |

---

## 6. Channel-Specific Voice Adaptations

| Channel | Adaptation |
|---------|-----------|
| **X** | Short, punchy. Threads for substantive content. Visual-first (figures > text) |
| **LinkedIn** | More narrative. Frame as "here's what we learned" stories. Tag collaborators |
| **YouTube** | Conversational, walkthrough style. "Let me show you how this works" |
| **Facebook** | Bangla-first content when targeting South Asia. Community announcements |
| **Substack** | Newsletter voice — "Dear fellow language explorers..." Longer-form reflection |
| **Discord** | Casual, helpful. Answer questions, celebrate contributions, coordinate work |

---

## 7. Hashtag & Metadata Strategy

| Platform | Primary Tags | Secondary Tags |
|----------|-------------|----------------|
| **X** | `#LILALab` `#LowResourceNLP` | `#BanglaNLP` `#LanguageTech` `#LILA_Lab` |
| **LinkedIn** | `#LILALab` `#NLP` `#LowResourceLanguages` | `#ComputationalSocialScience` `#OpenResearch` |
| **YouTube** | `LILA Lab` `low-resource NLP` | `Bangla NLP tutorial` `narrative economics` |

---

## 8. Brand Checklist (Before Posting)

- [ ] Does this use "LILA Lab" not "BENI Research Program" (unless referring to historical BENI work)?
- [ ] Is the XENI naming correct? (BENI = Bangla, not generic)
- [ ] Are all contributors credited?
- [ ] Is the tone warm and precise (not hype)?
- [ ] Are low-resource languages described as underserved, not primitive?
- [ ] Does this reference the repo as the source of truth?
- [ ] Are all links included (GitHub, relevant DOI)?
