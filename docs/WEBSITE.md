# LILA Lab — GitHub Pages Website

> **Formerly `docs/README.md`.** This file describes the GitHub Pages website assets deployed to `lilalab.pro.bd`. For documentation by stakeholder role, see [`docs/index.md`](index.md).

This directory contains both GitHub Pages assets and the lab operating docs.

## Start Here

| Role | Path |
| --- | --- |
| Researchers | `docs/COLLABORATION.md`, `technical-reports/README.md`, `docs/research/RUN_MANIFEST_TEMPLATE.md` |
| Linguistic contributors | `docs/LINGUISTIC_CONTRIBUTION_GUIDE.md`, `dataset/README.md` |
| Data releasers | `docs/DATA_RELEASE_CHECKLIST.md`, `dist/README.md` |
| Infrastructure contributors | `docs/REPOSITORY_OPERATING_MODEL.md`, `cli/README.md`, `infrastructure/README.md` |
| Maintainers | `docs/REPOSITORY_OPERATING_MODEL.md`, `registry/languages.json`, `registry/xeni_pipeline_contract.json` |

## Website Files

These files are deployed to `lilalab.pro.bd` via `.github/workflows/pages.yml`:

- `index.html` — main landing page
- `beni.html` — BENI pipeline showcase
- `docs.html` — documentation viewer
- `dashboard.html` — lab control room dashboard
- `*.css` / `*.js` — stylesheets and scripts
- `CNAME`, `robots.txt`, and `assets/`

## Operating Docs

- `REPOSITORY_OPERATING_MODEL.md` defines what belongs in each top-level area.
- `DATA_RELEASE_CHECKLIST.md` defines FAIR/data-card release gates.
- `research/RUN_MANIFEST_TEMPLATE.md` defines reproducibility metadata for research runs.
- `adr/` stores architecture decisions.
- `archive/` stores historical plans.

## HTML ↔ Markdown Duplication Audit

Seven HTML files have Markdown counterparts with overlapping content. This creates drift risk — edits to the `.md` file are not reflected in the `.html` file (or vice versa).

| HTML File | MD Counterpart | Risk |
|-----------|---------------|------|
| `collaboration-framework.html` | `COLLABORATION.md` | Drift |
| `linguistic-contribution.html` | `LINGUISTIC_CONTRIBUTION_GUIDE.md` | Drift |
| `quickstart-guide.html` | `CONTRIBUTOR_QUICKSTART.md` | Drift |
| `pipeline-flow.html` | `PIPELINE_FLOW.md` | Drift |
| `faq.html` | `FAQ.md` | Drift |
| `project-roadmap.html` | `ROADMAP.md` | Drift |
| `xeni-naming-convention.html` | `adr/ADR-001-xeni-naming-convention.md` | Drift |

**Recommendation:** Migrate to a Jekyll-based GitHub Pages setup that auto-renders `.md` files, eliminating the need for hand-maintained `.html` copies. Until then, each `.html` file should include a comment: `<!-- Generated from [path].md — edit the .md, not this file -->`.

The remaining HTML files (`dashboard.html`, `docs.html`, `index.html`, `beni.html`) are standalone web applications with no Markdown counterpart.

## Validation

Run these before claiming a structural change is complete:

```bash
python -m cli validate
python infrastructure/scripts/validate_schemas.py
make audit
```

For the documentation viewer (`docs.html`), markdown content is fetched from the repository and sidebar navigation is configured in `docs.js`.
