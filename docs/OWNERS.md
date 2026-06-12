# Documentation Ownership

> **Responsibility matrix** for LILA Lab documentation areas. Each area has a designated owner who reviews changes.

| Area | Owner | Review Required For |
|------|-------|---------------------|
| `docs/research/` (methodologies, manifests) | Research lead | Methodology additions, run manifest changes |
| `docs/adr/` | Maintainer | New ADRs, status changes |
| `docs/WEBSITE.md`, `.html`, `.css`, `.js` files | Web maintainer | HTML/CSS/JS changes, deployment config |
| `docs/index.md` (portal) | Maintainer | Adding/removing doc entries |
| `docs/COLLABORATION.md`, `CONTRIBUTOR_QUICKSTART.md` | Community manager | Collaboration model changes |
| `docs/LINGUISTIC_CONTRIBUTION_GUIDE.md` | Community manager | Contribution process changes |
| `docs/GLOSSARY.md`, `docs/FAQ.md` | All (shared) | Term/definition updates |
| `docs/ROADMAP.md` | Maintainer | Milestone changes |
| `technical-reports/` | Per-paper authors | Manuscript, figures, data references |
| `communications/` | Community manager | Brand, content, community docs |
| `infrastructure/` docs | Infrastructure lead | Bot, website, script docs |
| `pipelines/` READMEs | Per-pipeline maintainers | Pipeline-specific documentation |

## Process

1. **Minor changes** (typos, clarifications, link updates): No review required — direct commits welcome
2. **Major changes** (restructuring, new docs, process changes): Open an issue or PR for the area owner
3. **Cross-area changes** (affecting multiple areas): Tag all affected owners

## Adding New Documentation

When adding a new document:
1. Update `docs/index.md` to include a link in the appropriate stakeholder section
2. If it's a new area of documentation, add an entry in this OWNERS file
3. Ensure the new doc is linked from the relevant README and `docs/WEBSITE.md` if it's website-visible

*Last updated: 2026-06-12*
