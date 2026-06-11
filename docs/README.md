# LILA Lab — Documentation & Website

This directory serves **two roles**:

## 1. GitHub Pages Website (`docs/` root)

These files are deployed to **lilalab.pro.bd** via GitHub Actions (see `.github/workflows/pages.yml`):

- `index.html` — Main landing page
- `beni.html` — BENI pipeline showcase
- `docs.html` — Documentation viewer (loads markdown from repo)
- `dashboard.html` — Lab control room dashboard
- `*.css` / `*.js` — Stylesheets and scripts
- `CNAME` — Custom domain mapping
- `robots.txt` — Search engine crawling rules
- `assets/` — Images and media
- `research/` — Research-related web pages

## 2. Documentation Content

- `guides/` — Markdown documentation files (guides, reference)
- `adr/` — Architecture Decision Records
- `archive/` — Historical/archived docs

## Editing the Website

Website files are plain HTML/CSS/JS. Edit directly and push to `main` — the GitHub Pages workflow auto-deploys.

For the documentation viewer (`docs.html`), markdown content is fetched live from the GitHub repository. The sidebar navigation is configured in `docs.js`.

## Related

- `infrastructure/website/` — Additional dashboard files (legacy)
- `infrastructure/scripts/` — Deployment/linting scripts
