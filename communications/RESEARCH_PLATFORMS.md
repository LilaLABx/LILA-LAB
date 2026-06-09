# LILA Lab — Research Platform Integration

> How LILA Lab's research platforms connect to each other and to the social/utility channels.
> This updates and supersedes the BENI-era distribution strategy with the LILA+XENI brand architecture.

---

## Platform Map

```
                         ┌──────────────────┐
                         │    GITHUB         │
                         │  (source of truth)│
                         │  All code, papers,│
                         │  communications,  │
                         │  contribution docs│
                         └────────┬─────────┘
                                  │
                  ┌───────────────┼───────────────┐
                  ▼               ▼               ▼
          ┌────────────┐  ┌────────────┐  ┌────────────┐
          │    OSF     │  │  ZENODO   │  │  HF SPACE │
          │  Project   │  │  DOI for  │  │  Interactive│
          │  Hub       │  │  datasets  │  │  Gradio demo│
          │  Preprints │  │  + code    │  └────────────┘
          │  Protocols │  └────────────┘
          └────────────┘
               │
               ▼
          ┌────────────┐
          │   arXiv    │
          │  Papers    │
          │  Preprints │
          └────────────┘
```

---

## Brand Migration: BENI → LILA

| Context | BENI (old) | LILA (new) |
|---------|-----------|-------------|
| GitHub repo name | `economic-narrative-indices` | `lila-lab` (pending rename) |
| OSF project title | "Bangla Economic Narrative Indices (BENI)" | "LILA Lab: Language Intelligence for Low-resource Applications" |
| OSF component names | "Paper 3: BENI Pipeline" | "Technical Report #3: Building BENI" |
| Zenodo dataset | "BENI v1.0: Bangla Economic Narrative Index" | "LILA-BENI v1.0: Bangla Economic Narrative Index Pipeline" |
| Hugging Face org | `nabil0x` | `lila-lab` (or `nabil0x` as personal namespace, add org) |
| arXiv headers | "BENI Research Program" | "LILA Lab Technical Report" |

**Transition rule**: When creating new uploads or updating existing ones, use the LILA brand. Historical BENI entries keep their names but link to the LILA project.

---

## Platform Sync Protocols

### Paper Submission Flow

```
Paper manuscript finalized
    │
    ├── 1. Upload preprint to OSF component
    ├── 2. Submit to arXiv (if eligible)
    ├── 3. Archive code to Zenodo (GitHub release → auto DOI)
    ├── 4. Announce on X (thread with key figure)
    ├── 5. Publish LinkedIn article summarizing contribution
    ├── 6. Record YouTube walkthrough (5 min)
    ├── 7. Include in next Substack newsletter
    └── 8. Update Google Scholar profile
```

### Dataset Release Flow

```
Dataset finalized and validated
    │
    ├── 1. Upload to Zenodo → get DOI
    ├── 2. Upload to Hugging Face Datasets
    ├── 3. Create/update Gradio Space if applicable
    ├── 4. Update DATASET_CARD.md in repo
    ├── 5. GitHub release → auto Zenodo DOI for code
    ├── 6. Announce on X with dataset card preview
    └── 7. Add to OSF component supplementary materials
```

### Pipeline Update Flow

```
Pipeline improvement merged to main
    │
    ├── 1. Update Hugging Face model if applicable
    ├── 2. Update documentation in repo
    ├── 3. Create release notes
    ├── 4. Announce on X (technical thread)
    └── 5. Consider YouTube walkthrough if major update
```

---

## Platform-Specific Details

### GitHub — Code of Record

| Setting | Value |
|---------|-------|
| **Owner** | `nabil0x` |
| **Repo name** | `economic-narrative-indices` (current) → `lila-lab` (planned rename) |
| **Topics** | `lila-lab`, `low-resource-nlp`, `bangla-nlp`, `economic-narrative`, `text-as-data` |
| **Website** | `https://lila-lab.org` |
| **Description** | "LILA Lab — Language Intelligence for Low-resource Applications. Collaborative platform for building AI infrastructure for underserved languages." |
| **Badges** | Zenodo DOI, OSF project, Hugging Face model, GitHub Actions |

### OSF — Project Hub

| Setting | Value |
|---------|-------|
| **Title** | "LILA Lab: Language Intelligence for Low-resource Applications" |
| **Description** | "LILA Lab is a collaborative research platform building measurement infrastructure for languages underserved by current AI. We develop pipelines (XENI: Exploration & Native-language Intelligence) that enable researchers and linguists to extract, measure, and amplify narrative signals from low-resource language text." |
| **Components** | LILA Overview, Technical Reports (1–6), XENI Pipelines, Data Releases, Community |
| **License** | CC BY 4.0 |
| **Links** | GitHub, Zenodo, Hugging Face, Mendeley, Social channels (X, LinkedIn, YouTube) |

### Zenodo — DOI Minting

| Setting | Value |
|---------|-------|
| **Community** | Create "LILA Lab" Zenodo community for all releases |
| **Naming** | `lila-{pipeline}-v{major}.{minor}.{patch}` |
| **Reserved DOI** | `10.5281/zenodo.20585401` (BENI v1.0) — remains valid, LILA-branded metadata update |
| **GitHub integration** | Enable auto-archiving on release |

### Hugging Face — NLP Community

| Setting | Value |
|---------|-------|
| **Organization** | Consider creating `lila-lab` org on HF. Until then, use `nabil0x` namespace with `lila-` prefix |
| **Models** | `lila-{pipeline}-{model-type}` (e.g., `lila-beni-banglabert`) |
| **Datasets** | `lila-{pipeline}-{data-type}` (e.g., `lila-beni-narrative-index`) |
| **Spaces** | `lila-{pipeline}-demo` (e.g., `lila-beni-classifier-demo`) |

### arXiv — Paper Preprints

| Setting | Value |
|---------|-------|
| **Submission header** | "LILA Lab Technical Report #[N]" |
| **Categories** | cs.CL (Computation and Language), econ.GN (General Economics), stat.AP (Applications) |
| **Comments** | "N pages, N figures. Part of the LILA Lab Technical Report Series. Code and data: https://github.com/nabil0x/LILA-LAB" |

---

## DOI Checklist

| Object | DOI / ID | Status | Platform |
|--------|----------|--------|----------|
| LILA-BENI v1.0 dataset | `10.5281/zenodo.20585401` | Pre-reserved | Zenodo |
| Potrika corpus | `10.17632/v362rp78dc.4` | ✅ Published | Mendeley |
| Technical Report #1 | arXiv ID (TBD) | — | arXiv |
| Technical Report #2 | arXiv ID (TBD) | Submitted Jun 2026 | arXiv |
| Technical Report #3 | arXiv ID (TBD) | Planned Jul 2026 | arXiv |
| Technical Report #4 | arXiv ID (TBD) | Planned Sep 2026 | arXiv |
| Technical Report #5 | arXiv ID (TBD) | Planned Dec 2026 | arXiv |
| Technical Report #6 | arXiv ID (TBD) | Planned Mar 2027 | arXiv |
| LILA Lab OSF project | OSF ID (TBD) | — | OSF |
