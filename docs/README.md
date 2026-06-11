# LILA Lab — Documentation & Website

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

## Validation

Run these before claiming a structural change is complete:

```bash
python -m cli validate
python infrastructure/scripts/validate_schemas.py
make audit
```

For the documentation viewer (`docs.html`), markdown content is fetched from the repository and sidebar navigation is configured in `docs.js`.
