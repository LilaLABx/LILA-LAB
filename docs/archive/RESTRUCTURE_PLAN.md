# LILA Lab Repository Restructuring Plan

> **STATUS**: ⚠️ SUPERSEDED (as of 2026-06-12). All phases completed. The repository now follows the structure described herein. For current source-of-truth, see [`docs/REPOSITORY_OPERATING_MODEL.md`](../REPOSITORY_OPERATING_MODEL.md) and [`docs/index.md`](../index.md).

## Current Structure Analysis

The current repository is organized around the BENI research project. To properly represent LILA Lab as a research organization, we need to restructure to support:

1. **Multiple pipelines** (BENI, AENI, NENI, etc.)
2. **Shared infrastructure** (communications, templates, tools)
3. **Clear separation** between research, data, and infrastructure
4. **Scalability** for future growth

---

## New Structure Design

```
lila-lab/
│
├── 📋 ROOT FILES
│   ├── README.md                          # Lab overview and entry point
│   ├── LICENSE                            # MIT License (code)
│   ├── CITATION.cff                       # Citation metadata
│   ├── CONTRIBUTING.md                    # General contribution guide
│   ├── CODE_OF_CONDUCT.md                 # Community code of conduct
│   ├── ../../communications/COMMUNICATIONS.md                  # Multi-channel command center
│   ├── ../COLLABORATION.md                   # Research collaboration framework
│   ├── ../LINGUISTIC_CONTRIBUTION_GUIDE.md   # Language data contribution
│   ├── ../SUBREPOS.md                        # Git submodule guide
│   ├── .gitignore
│   └── .env.example                       # Environment template
│
├── 📁 pipelines/                          # XENI Pipeline Collection
│   ├── README.md                          # Pipeline overview and status
│   │
│   ├── beni/                              # Bangla Exploration & Native-language Intelligence
│   │   ├── README.md                      # BENI-specific documentation
│   │   ├── annotation/                    # LLM annotation pipeline
│   │   ├── index/                         # Index construction
│   │   ├── experiment/                    # Model training & evaluation
│   │   ├── database/                      # SQLite schema and pipeline
│   │   ├── data/                          # BENI-specific data
│   │   └── figures/                       # Paper figures
│   │
│   ├── aeni/                              # Assamese (planned)
│   │   └── README.md
│   │
│   ├── neni/                              # Nepali (planned)
│   │   └── README.md
│   │
│   ├── seni/                              # Sylheti (planned)
│   │   └── README.md
│   │
│   ├── ceni/                              # Chittagonian (planned)
│   │   └── README.md
│   │
│   └── template/                          # Pipeline template for new languages
│       ├── README.md
│       ├── annotation/
│       ├── indices/
│       ├── experiment/
│       ├── database/
│       └── data/
│
│   ⚠️  `shared/` not yet created — may add if shared utilities across pipelines grow
│
├── 📁 technical-reports/                             # Research Papers
│   ├── README.md                          # Paper series overview
│   │
│   ├── paper1_statistical_economics/      # Paper 1
│   │   └── README.md
│   │
│   ├── paper2_systematic_review/          # Paper 2
│   │   └── ...
│   │
│   ├── paper3_beni_method/                # Paper 3
│   │   └── ...
│   │
│   ├── paper4_beni_nowcasting/            # Paper 4
│   │   └── ...
│   │
│   ├── paper5_text_as_data_survey/        # Paper 5
│   │   └── ...
│   │
│   ├── paper6_llm_narrative_extraction/   # Paper 6
│   │   └── ...
│   │
│   ├── contributions/                     # Contributor records
│   │   ├── OWNERS.csv                     # Contribution log
│   │   └── linguistic_data/               # Data submission templates
│   │
│   └── extensions/                        # Extension proposals
│       ├── INDEX.md                       # Extension registry
│       ├── EXTENSION_TEMPLATE.md          # Proposal template
│       └── REPLICATION_TEMPLATE.md        # Replication template
│
├── 📁 dataset/                            # Datasets (actual: `dataset/`, not `data/`)
│   ├── README.md                          # Data overview
│   │
│   ├── beni-v1/                           # BENI v1 dataset
│   │   ├── README.md
│   │   ├── CITATION.cff
│   │   └── ...
│   │
│   ├── raw/                               # Raw upstream data
│   │   ├── potrika/                       # Potrika corpus
│   │   └── bnlp/                          # BNLP resources
│   │
│   └── processed/                         # Processed datasets
│       ├── annotations/
│       └── indices/
│
├── 📁 communications/                     # Communications Center
│   ├── README.md                          # Communications overview
│   ├── CHANNELS.md                        # Channel inventory
│   ├── BRAND_GUIDELINES.md                # Brand identity
│   ├── SOCIAL_MEDIA_STRATEGY.md           # Social strategy
│   ├── RESEARCH_PLATFORMS.md              # Research platforms
│   ├── COMMUNITY.md                       # Community coordination
│   ├── CONTENT_CALENDAR.md                # Content schedule
│   ├── P0_P1_COMMUNITY_SETUP.md           # Setup execution plan
│   └── templates/                         # Content templates
│       ├── x_thread.md
│       ├── x_single.md
│       ├── linkedin.md
│       ├── youtube.md
│       └── substack.md
│
├── 📁 infrastructure/                     # Infrastructure & Tools
│   ├── README.md                          # Infrastructure overview
│   │
│   ├── discord-bot/                       # Discord bot
│   │   ├── bot.py
│   │   ├── config.py
│   │   ├── cogs/
│   │   └── README.md
│   │
│   ├── website/                           # Website source
│   │   ├── index.html
│   │   ├── styles.css
│   │   └── assets/
│   │
│   └── scripts/                           # Utility scripts
│       ├── deployment/
│       └── maintenance/
│
├── 📁 docs/                               # Documentation
│   ├── README.md
│   ├── pipelines/                         # Pipeline documentation
│   ├── research/                          # Research documentation
│   └── assets/                            # Documentation assets
│
└── 📁 archive/                            # Archived files
    └── README.md
```

---

## Migration Steps

### Phase 1: Create New Directory Structure

1. Create top-level directories:
   - `pipelines/`
   - `data/`
   - `infrastructure/`

2. Create subdirectories with README files

### Phase 2: Move Files

| Current Location | New Location | Notes |
|-----------------|--------------|-------|
| `beni/` | `pipelines/beni/` | ✅ Done — Core pipeline |
| `data-paper/` | `dataset/beni-v1/` | ✅ Done — Dataset release (note: `dataset/` not `data/`) |
| `discord-bot/` | `infrastructure/discord-bot/` | ✅ Done — Bot code |
| Root HTML/CSS | `infrastructure/website/` | ✅ Done — Website |
| `releases/` | `dataset/` or archive | ⚠️ Partial — Version manifests still at root level |

### Phase 3: Update References

- Update all README files with new paths
- Update CITATION.cff repository URL
- Update communications docs with new structure
- Update .gitignore if needed

### Phase 4: Create New Root README

- Lab overview
- Pipeline status
- Quick start guides
- Repository map

---

## File Mapping

### Root Files (Keep)
- `README.md` → Update with new structure
- `LICENSE` → Create if missing
- `CITATION.cff` → Update repository URL
- `CONTRIBUTING.md` → Keep as-is
- `CODE_OF_CONDUCT.md` → Create from COMMUNITY.md
- `../../communications/COMMUNICATIONS.md` → Update paths
- `../COLLABORATION.md` → Keep as-is
- `../LINGUISTIC_CONTRIBUTION_GUIDE.md` → Keep as-is
- `../SUBREPOS.md` → Keep as-is
- `.gitignore` → Update paths

### Move: beni/ → pipelines/beni/
All BENI pipeline files move here.

### Move: data-paper/ → dataset/beni-v1/
Dataset release files move here.

### Move: discord-bot/ → infrastructure/discord-bot/
Bot code moves here.

### Move: Root index.html/styles.css → infrastructure/website/
Website files move here.

### Archive or Remove
- `releases/` → Contents may be archived (manifests are now in data/)
- `.agents/`, `.codex/`, `.omo/` → Keep as-is (tooling directories)

---

## Benefits of New Structure

1. **Scalability**: Easy to add new pipelines (AENI, NENI, etc.)
2. **Clarity**: Clear separation between pipelines, papers, data, and infrastructure
3. **Discoverability**: New contributors can find what they need quickly
4. **Professionalism**: Represents LILA Lab as an organization, not just one project
5. **Maintainability**: Shared code lives in `pipelines/shared/`

---

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| Broken links in documentation | Update all READMEs after migration |
| Git history confusion | Use `git mv` for moves to preserve history |
| Contributor confusion | Announce restructuring in Discord |
| External links break | Set up redirects if using GitHub Pages |

---

## Timeline

- **Phase 1** (10 min): Create directory structure
- **Phase 2** (20 min): Move files with `git mv`
- **Phase 3** (30 min): Update all references
- **Phase 4** (15 min): Create new root README
- **Total**: ~75 minutes
