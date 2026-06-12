# Documentation Refinement Plan

> **Audit date:** 2026-06-12
> **Scope:** 217 public-facing .md files across 8 top-level directories, 36 READMEs, ~24,434 total lines
> **Goal:** Make lab documentation accessible, navigable, and stakeholder-appropriate

---

## Executive Summary

The LILA Lab documentation is **comprehensive but not navigable**. It has excellent README coverage (36 READMEs), thorough methodology docs (12 levels), and strong governance (operating model, collaboration framework, ADRs). The problem: finding the right document requires knowing it exists first. There is no central portal, no stakeholder-based navigation, and the sheer volume (217 files) creates noise.

**Key numbers:**
| Metric | Count |
|--------|-------|
| Public .md files | 217 |
| README files | 36 |
| Top-level doc directories | 8 (docs/, pipelines/, dataset/, communications/, technical-reports/, infrastructure/, registry/, dist/) |
| Largest single doc | 1,162 lines (methodologies reference) |
| ADRs | 1 (should be 5-10) |
| Empty doc directories | 1 (docs/pipelines/) |

---

## Current State Assessment

### Strengths (preserve these)

| Strength | Evidence |
|----------|----------|
| **Excellent README coverage** | Every pipeline, every dataset, every tool has a README |
| **Consistent naming conventions** | `docs/REPOSITORY_OPERATING_MODEL.md` defines clear ownership boundaries |
| **Glossary + FAQ** | `docs/GLOSSARY.md` (110 lines) and `docs/FAQ.md` (307 lines) are well-maintained |
| **Research methodology depth** | 12-level methodology hierarchy (6,000+ lines total) with cross-links |
| **Governance structures** | Collaboration framework, ADR system, data release checklist |
| **Stakeholder-specific guides** | Linguistic contribution guide, contributor quickstart |

### Weaknesses (fix these)

| # | Issue | Evidence | Impact |
|---|-------|----------|--------|
| **W1** | **No central documentation portal** | Root `README.md` is a great project README but not a docs index; `docs/README.md` describes website files, not doc organization | Researchers, contributors, and devs all land on the same page and must self-sort |
| **W2** | **Stakeholder paths are implicit** | Nowhere maps "if you are a [researcher/contributor/developer/maintainer], start here →" | Each user reverse-engineers their own path |
| **W3** | **Research docs split across locations** | `docs/research/` (methodologies), `technical-reports/` (papers), `docs/archive/` (historical plans), `dataset/BENI/beni-v1/docs/` (dataset papers) | No single research entry point; hard to find all research outputs |
| **W4** | **Website HTML ↔ Markdown duplication** | `docs/` contains both `.html` (30+ files for GitHub Pages) and `.md` files with overlapping content | Risk of drift; contributors unsure which to edit |
| **W5** | **Empty/broken directories** | `docs/pipelines/` exists but is empty; `docs/archive/RESTRUCTURE_PLAN.md` exists but no cross-reference to current status | Dead ends frustrate navigation |
| **W6** | **ADR system underused** | Only 1 ADR (naming convention) for a complex monorepo with 8+ top-level areas | Architectural decisions are lost or duplicated in prose docs |
| **W7** | **No search or quick-reference** | No cheat sheet, no "where is X" card | Users grep for everything |
| **W8** | **Communications docs isolated** | `communications/` at root level with 8 docs + templates but no cross-link from main docs | Hard to find brand/content assets |

---

## Refinement Plan

### Phase 0: Quick Wins (Immediate — < 1 hour)

#### 0.1 Audit and fix empty directories
- [ ] **`docs/pipelines/`**: Either add content (pipeline overview page) or delete the directory and update `docs/README.md`
- [ ] **`docs/archive/RESTRUCTURE_PLAN.md`**: Either mark as `(superseded)` or `(applied)` with a date, or migrate any still-valid decisions

#### 0.2 Add "docs portal" link cluster to root README
- [ ] In root `README.md`, after the "Repository Overview" table, add a **Documentation Quick Links** section that maps stakeholder → entry point:

```markdown
## Documentation Quick Links

| You Are | Start Here |
|---------|------------|
| 🧪 **Researcher** | `docs/research/` — methodologies, papers, run manifests |
| 🌍 **Linguistic contributor** | `docs/LINGUISTIC_CONTRIBUTION_GUIDE.md` |
| 👨‍💻 **Developer** | `pipelines/README.md` → your pipeline |
| 🛠️ **Maintainer** | `docs/REPOSITORY_OPERATING_MODEL.md`, `docs/adr/` |
| 📊 **Dataset user** | `dataset/README.md` |
| 🤝 **Collaborator** | `docs/COLLABORATION.md` |
```

#### 0.3 Cross-link communications/ from main docs
- [ ] Add a line in `docs/README.md`: "For brand guidelines, content strategy, and community management → [`communications/`](../communications/COMMUNICATIONS.md)"

---

### Phase 1: Structural Improvements (Week 1)

#### 1.1 Create a central Documentation Portal (`docs/index.md`)

A single landing page that organizes ALL documentation by stakeholder need. This is the most impactful change.

```markdown
# LILA Lab Documentation

## For Researchers
- [Methodology Hierarchy](research/NARRATIVE_EXTRACTION_METHODOLOGIES.md) — 12 levels of narrative extraction
- [Technical Reports](../technical-reports/README.md) — Paper series
- [Run Manifest Template](research/RUN_MANIFEST_TEMPLATE.md) — Reproducibility
- [BENI Pilot Results](research/BENI_PILOT_RUN_MANIFEST.md)

## For Linguistic Contributors
- [Contribution Guide](LINGUISTIC_CONTRIBUTION_GUIDE.md) — How to contribute your language
- [Dataset Tracker](../dataset/README.md) — Language progress
- [Extension Templates](../technical-reports/extensions/)

## For Developers
- [Pipeline Framework](../pipelines/README.md) — XENI architecture
- [API Docs](../api/README.md) — (planned)
- [CLI Tools](../cli/README.md)

## For Maintainers
- [Repository Operating Model](REPOSITORY_OPERATING_MODEL.md)
- [Architecture Decisions](adr/)
- [Data Release Checklist](DATA_RELEASE_CHECKLIST.md)

## Reference
- [Glossary](GLOSSARY.md)
- [FAQ](FAQ.md)
- [Roadmap](ROADMAP.md)
- [Pipeline Flow](PIPELINE_FLOW.md)
```

Then link this from: root `README.md`, `docs/README.md`, and include it in the repo's GitHub Pages navigation.

#### 1.2 Consolidate research documentation entry points

| Current | Issue | Action |
|---------|-------|--------|
| `docs/research/` | Methodologies + run manifests | Keep as research methods hub |
| `technical-reports/` | Papers + extensions | Keep as publication hub |
| `docs/archive/` | Historical plans | Mark clearly as `(historical)` |
| `dataset/BENI/beni-v1/docs/` | Dataset paper | Cross-link from technical-reports/README.md |

Add explicit cross-links:
- `docs/research/README.md` should list all research-related locations
- `technical-reports/README.md` should link back to `docs/research/` for methodology

#### 1.3 Consolidate root-level READMEs

Currently there are multiple competing "where to start" documents:

| File | Purpose | vs. Root README |
|------|---------|-----------------|
| `README.md` | Project overview + quick start | Primary |
| `CONTRIBUTING.md` | Generic contribution info | Should link to `docs/COLLABORATION.md` |
| `docs/README.md` | Website file description | Confusingly named — rename or reframe |
| `docs/REPOSITORY_OPERATING_MODEL.md` | Source-of-truth map | Clear, keep |

**Action:** Rename `docs/README.md` to `docs/WEBSITE.md` or clearly state "this describes the GitHub Pages website files" in its first line. Update all cross-references.

---

### Phase 2: Navigation & Cross-Reference (Week 2)

#### 2.1 Add a "Quick Reference Card" (`docs/QUICK_REFERENCE.md`)

A single-page cheat sheet covering:
- Directory structure (one-line per directory)
- Where to find: pipelines, datasets, papers, methodologies
- Common commands (validate, build, test)
- Key terms (BENI, XENI, narrative index)
- Links to detailed docs

This should be discoverable from everywhere — linked in root `README.md`, `docs/README.md`, and the GitHub Pages sidebar.

#### 2.2 Expand ADR coverage

Current: 1 ADR. Minimum target: 5 ADRs covering:

| ADR | Title | Existing documentation |
|-----|-------|----------------------|
| ADR-001 | XENI Pipeline Naming Convention | ✅ Done |
| ADR-002 | Documentation Structure & Portal Decision | Documents the outcome of this plan |
| ADR-003 | Dataset ↔ Pipeline Separation | Currently in `REPOSITORY_OPERATING_MODEL.md` |
| ADR-004 | LLM Annotation Schema Versioning | Currently in annotation docs |
| ADR-005 | Multi-Language Coordination Protocol | Critical for 10-language target |

An ADR per major architectural decision preserves rationale and prevents re-litigation.

#### 2.3 Add "Breadcrumb" navigation to deep docs

Deeply nested docs (methodology pages, technical reports) should have breadcrumb-style navigation headers:

```markdown
<!-- Top of each methodology page -->
**Home > [Research](..) > [Methodologies](.) > [L08: Narrative Graphs](research/methodologies/L08_narrative_networks_graphs.md)**
```

#### 2.4 Audit and deduplicate website HTML vs. Markdown

| File Pair | Risk | Action |
|-----------|------|--------|
| `docs/COLLABORATION.md` ↔ `docs/collaboration-framework.html` | Drift | Generate HTML from .md in CI; or add comment "Generated from COLLABORATION.md" |
| `docs/LINGUISTIC_CONTRIBUTION_GUIDE.md` ↔ `docs/linguistic-contribution.html` | Drift | Same |
| Other .html files with markdown counterparts | Duplication | Audit all 30+ HTML files |

**Recommendation:** Use GitHub Pages with a Jekyll theme that auto-renders `.md` files, eliminating the need for hand-maintained `.html` files. Alternatively, add a CI step that validates HTML ↔ MD consistency.

---

### Phase 3: Sustainability (Week 3+)

#### 3.1 Add documentation quality checks to CI

```yaml
# .github/workflows/doc-quality.yml
- name: Check documentation cross-references
  run: python scripts/check_doc_links.py  # Verify all internal links resolve
- name: Check README coverage
  run: python scripts/check_readme_coverage.py  # Every dir should have README
- name: Validate ADR index
  run: python scripts/check_adr_index.py  # ADR index matches actual files
```

#### 3.2 Create a documentation OWNERS file

```markdown
# docs/OWNERS.md
| Area | Owner | Review Required |
|------|-------|-----------------|
| `docs/research/` | Research lead | For methodology changes |
| `docs/` website | Web maintainer | For HTML/CSS changes |
| `communications/` | Community manager | For brand/content |
| `technical-reports/` | Paper authors | Per-paper |
```

#### 3.3 Establish documentation review gates

Add to `docs/REPOSITORY_OPERATING_MODEL.md`:

> **Documentation change requires:**
> 1. Link check passes (no broken internal references)
> 2. If adding a new doc: update `docs/index.md` (once created) and relevant README
> 3. If removing a doc: add a redirect or tombstone note

---

## Prioritized Action List

| # | Action | Effort | Impact | Phase |
|---|--------|--------|--------|-------|
| 1 | Add stakeholder link cluster to root README | 15 min | High | 0 |
| 2 | Fix empty `docs/pipelines/` directory | 5 min | Medium | 0 |
| 3 | Mark archive plan as superseded | 5 min | Low | 0 |
| 4 | Create `docs/index.md` (central portal) | 1 hr | Very High | 1 |
| 5 | Rename `docs/README.md` → `docs/WEBSITE.md` | 30 min | High | 1 |
| 6 | Consolidate research entry points with cross-links | 1 hr | High | 1 |
| 7 | Create Quick Reference Card | 1 hr | High | 2 |
| 8 | Expand ADR coverage (4 new ADRs) | 2-3 hrs | Medium | 2 |
| 9 | Audit HTML↔MD duplication, set generation strategy | 2 hrs | Medium | 2 |
| 10 | Add breadcrumb navigation to deep docs | 1 hr | Medium | 2 |
| 11 | Add doc quality CI checks | 2 hrs | Medium | 3 |
| 12 | Create documentation OWNERS file | 30 min | Low | 3 |
| 13 | Formalize doc review gates in operating model | 30 min | Low | 3 |

**Total estimated effort:** ~12-15 hours over 3 phases.

---

## Success Criteria

After implementation:
1. A **new contributor** can find their relevant docs within 30 seconds of opening the repo
2. A **researcher** can navigate from root README → methodology page → technical report in 2 clicks
3. A **linguistic contributor** can find the contribution guide, dataset tracker, and template from a single "For Contributors" link
4. All internal cross-references resolve correctly (CI-verified)
5. No empty documentation directories exist
6. ADR index shows 5+ architectural decisions
7. `docs/README.md` clearly states its purpose (or is renamed)
8. The archive directory has clear status markers

---

## Appendix: Current Documentation Topology

```text
Root README ─────────────────────────────────────────────────────────────┐
├── docs/ (51 entries: .html + .md + assets)                            │
│   ├── research/                                                        │
│   │   ├── NARRATIVE_EXTRACTION_METHODOLOGIES.md (1162 lines) ──── Cross-links to ──┐
│   │   └── methodologies/ (12 level pages + INDEX.md, ~6500 total lines)            │
│   ├── adr/ (1 ADR + template)                                         │
│   ├── archive/ (1 stale plan)                                          │
│   ├── COLLABORATION.md, GLOSSARY.md, FAQ.md, ROADMAP.md               │
│   ├── LINGUISTIC_CONTRIBUTION_GUIDE.md                                │
│   ├── DATA_RELEASE_CHECKLIST.md, PIPELINE_FLOW.md                     │
│   └── 30+ .html files (GitHub Pages website)                         │
├── pipelines/ (14 pipelines + shared/ + template + LAB/)               │
│   └── README.md at each level                                         │
├── dataset/ (10 languages + README.md)                                 │
├── technical-reports/ (papers + extensions + contributions)             │
├── communications/ (brand, strategy, content calendar, templates)      │
├── registry/ (languages, schemas, publications, contracts)             │
├── infrastructure/ (discord-bot, website scripts)                      │
├── api/, cli/, dist/ (planned/stubs)                                   │
└── CONTRIBUTING.md                                                     │
                                                                        │
└─── Problem: No central portal maps these 8+ areas to user needs ──────┘
```

---

**Status:** Proposed
**Author:** Doc audit
**Next step:** Present to maintainers for discussion → ADR-002
