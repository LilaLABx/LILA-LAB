# ADR-002: Documentation Structure & Portal

**Status:** Accepted

**Date:** 2026-06-12

## Context

The LILA Lab repository had grown to 217+ public-facing Markdown files across 8 top-level directories, 36 READMEs, and approximately 24,000 lines of documentation. While the content was comprehensive, it was not navigable: there was no central documentation index, no stakeholder-based entry points, and `docs/README.md` ambiguously described both GitHub Pages website files and lab documentation, creating confusion for both website maintainers and documentation consumers.

Key problems identified:

- **No single entry point**: New visitors landed on the root `README.md`, which is a project README, not a documentation portal. Finding the right document required knowing it existed first.
- **Stakeholder paths were implicit**: Researchers, linguistic contributors, developers, and maintainers all navigated the same structure despite needing different entry points. No document mapped "if you are a [role], start here →".
- **`docs/README.md` served dual purposes**: It documented both GitHub Pages website deployment (`index.html`, `dashboard.html`, etc.) and lab operating docs (`REPOSITORY_OPERATING_MODEL.md`, `COLLABORATION.md`, etc.). Contributing website HTML and contributing documentation guides were conflated.
- **Research docs were split across locations**: Methodologies lived in `docs/research/`, papers in `technical-reports/`, dataset papers in `dataset/BENI/beni-v1/docs/`, and historical plans in `docs/archive/`, with no cross-links.
- **ADRs were underused**: Only 1 ADR existed for a complex monorepo with multiple pipelines, datasets, and research outputs.

Several alternatives were considered: (a) keep the existing structure and rely on a "best effort" FAQ approach, (b) migrate all documentation to a separate `wiki` repository, (c) adopt a full static site generator (MkDocs, Docusaurus). Alternative (a) would not solve navigation; alternative (b) would separate docs from code they describe; alternative (c) was premature for the project's current maturity.

## Decision

We adopt a **central documentation portal model** with the following structure:

### 1. Central Portal

Create `docs/index.md` as the single entry point for all documentation, organized by 7 stakeholder personas: Researchers, Linguistic Contributors, Developers, Maintainers, Dataset Users, Collaborators, and Communications.

### 2. Stakeholder Mapping

Each major document cluster is mapped to a stakeholder role in both the root `README.md` and `docs/index.md`. The root `README.md` includes a "Documentation Quick Links" table with role → starting document mapping.

### 3. Clear Separation

`docs/README.md` is replaced by `docs/WEBSITE.md`, which is scoped explicitly to GitHub Pages website deployment. The documentation portal at `docs/index.md` becomes the canonical navigation hub.

### 4. Cross-Linking

Research locations (`docs/research/`, `technical-reports/`, `dataset/BENI/beni-v1/docs/`) are cross-linked from each other, with explicit "Related Resources" sections.

### 5. Quick Reference

`docs/QUICK_REFERENCE.md` provides a single-page cheat sheet covering directory structure, common commands, key terms, and where to find things.

### Implementation

This structure was implemented in June 2026. See the [refinement plan](../refinement-plan.md) for the full audit and decision rationale.

## Consequences

### Positive

- **Single source of truth**: One portal to update when documentation structure changes
- **Stakeholder-friendly**: Each role has a clear starting point
- **Contribution clarity**: Website maintainers edit `docs/WEBSITE.md` assets; doc authors update `docs/index.md`
- **Discoverable**: The portal is linked from root `README.md`, `docs/WEBSITE.md`, and all research entry points

### Negative

- **Gateway dependency**: If `docs/index.md` goes missing or stale, navigation degrades significantly
- **Two-file maintenance**: Adding a new doc requires updates to both the doc itself and the portal — mitigated by the maintenance rule added to `REPOSITORY_OPERATING_MODEL.md`

### Neutral

- This ADR supersedes any implicit documentation conventions from before June 2026
- The structure is compatible with future migration to a static site generator (e.g., MkDocs, Docusaurus) — the portal acts as a semantic sitemap that can be translated to navigation config
