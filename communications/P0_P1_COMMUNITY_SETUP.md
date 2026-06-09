# LILA Lab — P0/P1 Community Establishment

> Execution plan to activate LILA Lab's community channels and enable contribution.

---

## P0 — Critical Path (Must Complete Before Public Launch)

These items block community contribution. Without them, people cannot find, join, or contribute to LILA Lab.

### P0.1 — GitHub Repository Public Readiness

| Task | Status | Owner | Notes |
|------|--------|-------|-------|
| Rename repo from `economic-narrative-indices` to `lila-lab` | ⏳ Pending | Ann N. Nabil | Aligns with brand. Redirects auto-create. |
| Add `README.md` with channel links, contribution guide, and badge | ⏳ Pending | Ann N. Nabil | First thing newcomers see. Must include Discord, OSF, HF links. |
| Add `CONTRIBUTING.md` with 8 contribution models | ⏳ Pending | Ann N. Nabil | Reference `COLLABORATION.md` content. |
| Add `CODE_OF_CONDUCT.md` | ⏳ Pending | Ann N. Nabil | Pull from `communications/COMMUNITY.md` Section "Code of Conduct" |
| Add `LICENSE` file | ⏳ Pending | Ann N. Nabil | MIT or Apache 2.0 — standard for academic open source |
| Add `CITATION.cff` | ⏳ Pending | Ann N. Nabil | Enables "Cite this repository" on GitHub |
| Create GitHub Topics: `lila-lab`, `low-resource-nlp`, `bangla-nlp`, `narrative-economics` | ⏳ Pending | Ann N. Nabil | Discoverability in GitHub search |
| Enable GitHub Discussions | ⏳ Pending | Ann N. Nabil | Q&A, announcements, extension proposals |
| Create issue templates: bug, extension proposal, contribution, question | ⏳ Pending | Ann N. Nabil | Standardize incoming requests |
| Add `OWNERS.csv` structure for contributor tracking | ⏳ Pending | Ann N. Nabil | Core to recognition model |

### P0.2 — Discord Server Activation

| Task | Status | Owner | Notes |
|------|--------|-------|-------|
| Create Discord server at `discord.gg/TrrdKbky` | ⏳ Pending | Ann N. Nabil | — |
| Set up channels per `COMMUNITY.md`: `#welcome`, `#announcements`, `#general`, `#linguistic-data`, `#pipelines`, `#extensions`, `#paper-writing`, `#monthly-lab-call` | ⏳ Pending | Ann N. Nabil | Match documented structure exactly |
| Write `#welcome` pinned message with rules + onboarding flow | ⏳ Pending | Ann N. Nabil | Link to `COLLABORATION.md`, `LINGUISTIC_CONTRIBUTION_GUIDE.md` |
| Set up role hierarchy: `@Researcher`, `@Contributor`, `@Annotator`, `@Newcomer` | ⏳ Pending | Ann N. Nabil | Enables channel access control |
| Create Discord invite link with no expiry | ⏳ Pending | Ann N. Nabil | Permanent link for all docs |
| Add Discord widget to GitHub README | ⏳ Pending | Ann N. Nabil | One-click join from repo |

### P0.3 — Website Launch (GitHub Pages)

| Task | Status | Owner | Notes |
|------|--------|-------|-------|
| Deploy `lila-lab.org` via GitHub Pages | ⏳ Pending | Ann N. Nabil | Use existing `index.html` + `styles.css` as base |
| Add pages: Home, Research, Pipelines, Contribute, Team, Contact | ⏳ Pending | Ann N. Nabil | — |
| Add channel links section (all 15+ channels) | ⏳ Pending | Ann N. Nabil | Matches `CHANNELS.md` inventory |
| Add "Contributor Directory" page (pull from `OWNERS.csv`) | ⏳ Pending | Ann N. Nabil | Recognition at scale |
| Add Gradio demo embed (if available) | ⏳ Pending | Ann N. Nabil | Interactive pipeline showcase |
| Set up custom domain `lila-lab.org` | ⏳ Pending | Ann N. Nabil | DNS + CNAME config |

### P0.4 — Research Platform Registration

| Task | Status | Owner | Notes |
|------|--------|-------|-------|
| Create OSF project page | ⏳ Pending | Ann N. Nabil | Central research hub. Link to all papers, datasets. |
| Create Zenodo record with DOI | ⏳ Pending | Ann N. Nabil | `doi.org/10.5281/zenodo.20585401` — verify minting |
| Create Hugging Face organization `nabil0x` | ⏳ Pending | Ann N. Nabil | Host models + datasets |
| Upload BENI dataset to Hugging Face Datasets | ⏳ Pending | Ann N. Nabil | `lila-beni-v1.0` — with dataset card |
| Create arXiv author profile | ⏳ Pending | Ann N. Nabil | Enables paper discoverability |
| Set up Google Scholar profile | ⏳ Pending | Ann N. Nabil | Citation tracking |
| Verify ORCID `0009-0006-3561-045X` is public | ⏳ Pending | Ann N. Nabil | — |

### P0.5 — Social Media Account Activation

| Task | Status | Owner | Notes |
|------|--------|-------|-------|
| Create X/Twitter `@LILA_Lab` | ⏳ Pending | Ann N. Nabil | Handle reserved per `CHANNELS.md` |
| Create LinkedIn company page `/company/lila-lab` | ⏳ Pending | Ann N. Nabil | — |
| Create YouTube channel `@LILA_Lab` | ⏳ Pending | Ann N. Nabil | — |
| Create Facebook page `/LILALabResearch` | ⏳ Pending | Ann N. Nabil | South Asia outreach |
| Create Substack `lila.substack.com` | ⏳ Pending | Ann N. Nabil | Monthly newsletter |
| Cross-link all accounts (website → social, social → repo) | ⏳ Pending | Ann N. Nabil | Network effect |

### P0.6 — Content Seeding (Pre-Launch)

| Task | Status | Owner | Notes |
|------|--------|-------|-------|
| Write 3 launch X posts (intro thread, BENI explainer, CTA) | ⏳ Pending | Ann N. Nabil | Use templates from `communications/templates/` |
| Write 1 LinkedIn launch article | ⏳ Pending | Ann N. Nabil | Long-form intro to LILA Lab |
| Record 1 YouTube intro video (5 min) | ⏳ Pending | Ann N. Nabil | "What is LILA Lab?" |
| Write Substack launch issue | ⏳ Pending | Ann N. Nabil | "Welcome to LILA Lab" |
| Prepare 2 weeks of content in `CONTENT_CALENDAR.md` | ⏳ Pending | Ann N. Nabil | Batch before launch |

---

## P1 — Enhancement (Complete Within 30 Days of Launch)

These items improve community experience and growth but don't block initial contribution.

### P1.1 — Contributor Onboarding Automation

| Task | Status | Owner | Notes |
|------|--------|-------|-------|
| Create Discord bot for newcomer welcome + role assignment | ⏳ Pending | Ann N. Nabil | Auto-assign `@Newcomer` on join |
| Set up GitHub Actions for `OWNERS.csv` validation | ⏳ Pending | Ann N. Nabil | Prevent merge if contributor record incomplete |
| Create "First Contribution" issue template with checklist | ⏳ Pending | Ann N. Nabil | Guided path for new contributors |
| Write onboarding email sequence (5 emails over 2 weeks) | ⏳ Pending | Ann N. Nabil | For Substack subscribers |

### P1.2 — Content Production Infrastructure

| Task | Status | Owner | Notes |
|------|--------|-------|-------|
| Create YouTube video templates (intro, tutorial, spotlight) | ⏳ Pending | Ann N. Nabil | Standardize production |
| Set up screen recording workflow (OBS + Loom backup) | ⏳ Pending | Ann N. Nabil | — |
| Create thumbnail templates (Canva or Figma) | ⏳ Pending | Ann N. Nabil | Brand-consistent visuals |
| Write 4 Substack templates (monthly digest, paper summary, contributor spotlight, pipeline update) | ⏳ Pending | Ann N. Nabil | — |
| Create X thread template library (10+ patterns) | ⏳ Pending | Ann N. Nabil | Reduce content creation friction |

### P1.3 — Community Engagement Infrastructure

| Task | Status | Owner | Notes |
|------|--------|-------|-------|
| Set up monthly lab call (first Friday, Google Meet) | ⏳ Pending | Ann N. Nabil | Calendar invite + Discord channel |
| Create "Contributor of the Month" recognition system | ⏳ Pending | Ann N. Nabil | Monthly X/LinkedIn post + Discord announcement |
| Set up annotation coordination workflow in Discord | ⏳ Pending | Ann N. Nabil | Thread per language, task tracking |
| Create FAQ document from Discord Q&A | ⏳ Pending | Ann N. Nabil | Living doc, updated weekly |
| Set up quarterly community survey | ⏳ Pending | Ann N. Nabil | Feedback loop |

### P1.4 — Analytics & Growth Tracking

| Task | Status | Owner | Notes |
|------|--------|-------|-------|
| Set up UTM parameters for all channel links | ⏳ Pending | Ann N. Nabil | Track which channels drive contribution |
| Create `ANALYTICS.md` with monthly metrics dashboard | ⏳ Pending | Ann N. Nabil | Per `CHANNELS.md` targets |
| Set up GitHub Insights monitoring (stars, forks, clones) | ⏳ Pending | Ann N. Nabil | — |
| Set up Discord server analytics | ⏳ Pending | Ann N. Nabil | Track active members, messages per channel |
| Create monthly growth report template | ⏳ Pending | Ann N. Nabil | Auto-populate from platform dashboards |

### P1.5 — Collaboration Tools

| Task | Status | Owner | Notes |
|------|--------|-------|-------|
| Set up GitHub Projects board for contribution tracking | ⏳ Pending | Ann N. Nabil | Visualize contributor pipeline |
| Create shared Google Drive for drafts and assets | ⏳ Pending | Ann N. Nabil | Collaborative editing space |
| Set up Overleaf project for paper collaboration | ⏳ Pending | Ann N. Nabil | LaTeX templates per `technical-reports/` |
| Create Notion workspace for internal coordination | ⏳ Pending | Ann N. Nabil | Optional — if team grows |

### P1.6 — Extension Pipeline Onboarding

| Task | Status | Owner | Notes |
|------|--------|-------|-------|
| Create "Extend LILA Lab" tutorial (video + written) | ⏳ Pending | Ann N. Nabil | Step-by-step for new language pipelines |
| Create extension proposal template (GitHub Issue) | ⏳ Pending | Ann N. Nabil | Structured intake |
| Set up AENI (Assamese) as first extension pilot | ⏳ Pending | Ann N. Nabil | Prove the extension model works |
| Create language-specific Discord channels (as needed) | ⏳ Pending | Ann N. Nabil | `#assamese`, `#nepali`, etc. |

---

## Execution Order

```
P0.1 (GitHub)  ──┐
P0.2 (Discord) ──┤──→  LAUNCH  ──→  P1.1 (Onboarding)
P0.3 (Website) ──┤                    P1.2 (Content)
P0.4 (Research)──┤                    P1.3 (Engagement)
P0.5 (Social)  ──┘                    P1.4 (Analytics)
                                       P1.5 (Tools)
P0.6 (Content) ──→ PUBLISH LAUNCH     P1.6 (Extensions)
```

**Target timeline:**
- **Week 1–2**: Complete all P0 items
- **Week 3**: Soft launch (Discord + GitHub + Website)
- **Week 4**: Public launch (social media + Substack + YouTube)
- **Month 2–3**: Complete P1 items

---

## Success Criteria

| Milestone | Metric | Target |
|-----------|--------|--------|
| P0 complete | All channels live and cross-linked | 100% |
| Launch week | Discord members | 20+ |
| Launch month | GitHub stars | 30+ |
| Launch month | First external contributor | 1+ |
| Month 3 | Monthly active Discord members | 50+ |
| Month 3 | First extension proposal (non-Bangla) | 1+ |

---

## Blocked Dependencies

| Item | Blocked By | Resolution |
|------|-----------|------------|
| Website content | `lila-lab.org` domain DNS | Purchase domain or use GitHub Pages subdomain |
| Gradio demo | BENI pipeline running externally | Deploy to HF Spaces |
| YouTube videos | Screen recording setup | Use Loom for v1, upgrade later |
| Monthly lab call | 3+ active contributors | Start with office hours |
