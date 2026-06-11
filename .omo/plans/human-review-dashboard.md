# Human Review Dashboard — Plan

## Overview

Build a unified **Human Review Dashboard** for LILA Lab's annotation pipelines. The dashboard serves as the human-in-the-loop validation layer across two modalities:

| Pipeline | Modality | What Gets Reviewed |
|----------|----------|-------------------|
| **Audio Annotation Lab (AAL)** | Audio → Text | ASR transcriptions, LLM annotations on transcribed segments, speaker diarization |
| **BENI / XENI (text)** | News articles | LLM economic relevance labels, multi-LLM disagreements, low-confidence cases |

The dashboard must be **modular**: shared review core + pipeline-specific adapters, so every future XENI pipeline gets review capability for free.

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                   Human Review Dashboard                      │
│                        (Gradio/Streamlit)                    │
├──────────────────────────┬───────────────────────────────────┤
│                          │                                   │
│    ┌─────────────────┐   │   ┌─────────────────────────────┐ │
│    │  Shared Core     │   │   │  Pipeline Adapters          │ │
│    │                  │   │   │                             │ │
│    │ - Auth/Users     │   │   │  ├── AAL Adapter           │ │
│    │ - Review Queue   │   │   │  │   - Audio player        │ │
│    │ - Quality Metrics│   │   │  │   - Waveform viz        │ │
│    │ - Export         │   │   │  │   - Segment timeline    │ │
│    │ - Progress       │   │   │  │   - ASR correction      │ │
│    │ - API Layer      │   │   │  │                         │ │
│    └─────────────────┘   │   │  ├── BENI/XENI Adapter     │ │
│                          │   │  │   - Article text view    │ │
│                          │   │  │   - Schema labels        │ │
│                          │   │  │   - Model disagreement   │ │
│                          │   │  │   - Confidence flags      │ │
│                          │   │  │                         │ │
│                          │   │  └── Template Adapter      │ │
│                          │   │      - Generic schema view  │ │
│                          │   │      - Multi-annotator view │ │
│                          │   └─────────────────────────────┘ │
└──────────────────────────┴───────────────────────────────────┘
```

### Component Breakdown

**Shared Core** (`pipelines/review-dashboard/`)
- User authentication & role management
- Queue management (fetch, filter, sort, paginate)
- Quality metrics engine (agreement, confidence distributions)
- Export service (approved → final format)
- Progress tracking per session/pipeline

**AAL Adapter** (`pipelines/audio-annotation-lab/interface/`)
- Audio player with segment navigation
- Waveform + segment timeline visualization
- Transcription correction interface
- Label review/approve/reject workflow
- Speaker identification

**BENI/XENI Adapter** (`pipelines/beni/annotation/` or `pipelines/review-dashboard/adapters/xeni/`)
- Article text viewer with highlighting
- Schema field display per annotation
- Multi-annotator comparison view
- Disagreement resolution UI
- Low-confidence review queue

---

## Data Flow

```
Pipeline Output (JSONL/dataclasses)
    │
    ▼
┌──────────────────────────────────────┐
│  Store (existing database/store.py)   │
│  - Sessions, Segments, Annotations   │
│  - JSONL-backed, no external DB      │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│  Review Queue Builder                │
│  (existing quality/review.py)        │
│  - threshold_filter                  │
│  - priority_sort                     │
│  - create_review_queue               │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│  Dashboard Web App                   │
│  - Loads queue from store            │
│  - Presents items for review         │
│  - Accepts approve/reject/correct    │
│  - Saves decisions back to store     │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│  Exported Approved Data              │
│  (existing export/*.py)              │
│  - JSONL, CSV, HuggingFace           │
└──────────────────────────────────────┘
```

---

## Issue Breakdown

### Milestone 1: Foundation & Core Infrastructure

| # | Issue | Description | Complexity | Dependencies |
|---|-------|-------------|-----------|-------------|
| 1 | **Review Dashboard Project Scaffold** | Create `pipelines/review-dashboard/` package with `pyproject.toml`, `__init__.py`, CLI entry point, and directory structure (core/, adapters/, config/). Set up Gradio/Streamlit skeleton app with health endpoint. | Easy | None |
| 2 | **Review Queue Data Model & Store Integration** | Build ReviewSession, ReviewDecision models; extend `Store` to persist review decisions (approve/reject/correct); add methods to query pending, approved, rejected items with pagination. | Medium | #1 |
| 3 | **Quality Metrics Engine** | Interactive dashboard page showing: confidence distribution histogram, agreement scores per field (Krippendorff's α, Cohen's κ), throughput over time, annotation progress bars. Consumes existing `quality/` module. | Medium | #1 |
| 4 | **User Authentication & Role System** | Simple auth (token-based or local accounts) with roles: `reviewer`, `admin`, `viewer`. Track who reviewed what, with timestamps. Config via JSON/YAML file. | Medium | #2 |

### Milestone 2: Audio Annotation Lab (AAL) Dashboard

| # | Issue | Description | Complexity | Dependencies |
|---|-------|-------------|-----------|-------------|
| 5 | **Audio Player with Segment Navigation** | Build audio player component (WaveSurfer.js or Gradio Audio) that loads audio by session_id, displays segment boundaries as clickable markers, plays selected segment. | Hard | #1, #2 |
| 6 | **ASR Transcription Review & Correction** | Review page showing: segment text, audio playback controls, editable text box for ASR correction, approve/reject buttons. Track WER before/after correction. | Medium | #5 |
| 7 | **Annotation Label Review & Adjudication** | Page showing: segment context, current LLM labels per field, confidence scores, dropdown to change labels, approve/reject per field. Show multi-annotator comparison when available. | Medium | #5, #6 |
| 8 | **Speaker Diarization Review** | Display speaker labels per segment with timeline; allow reassigning speaker; merge/split segments as needed. | Hard | #5 |
| 9 | **AAL Review Dashboard Home** | Landing page for AAL review: session list with stats (total segments, pending review, approved %, confidence distribution), queue priority sorting, quick filters. | Medium | #6, #7, #8 |

### Milestone 3: Text/XENI Pipeline Dashboard

| # | Issue | Description | Complexity | Dependencies |
|---|-------|-------------|-----------|-------------|
| 10 | **Article Text Review & Schema Labeling** | Page showing: full article text, current schema labels (economic_relevance, sentiment, topic, etc.), confidence indicators, label edit controls. Support any schema (not just economic). | Medium | #1, #2 |
| 11 | **Multi-Annotator Disagreement Resolution** | Side-by-side comparison of annotations from multiple LLMs/humans; highlight disagreement fields; resolve by selecting best label manually; show agreement metrics per field. | Hard | #10 |
| 12 | **Review Queue Dashboard (BENI/XENI)** | Landing page: filterable table of flagged articles (low confidence, model disagreement, ambiguous); priority sorting; batch approve/reject; progress tracking per batch/domain. | Medium | #10, #11 |
| 13 | **Batch Operations & Bulk Actions** | Select multiple queue items; bulk approve, bulk reject, bulk reassign; export selected items to JSONL/CSV. | Medium | #10 |

### Milestone 4: Integration & Deployment

| # | Issue | Description | Complexity | Dependencies |
|---|-------|-------------|-----------|-------------|
| 14 | **Export Pipeline for Reviewed Data** | Extend existing export modules to output only approved/reviewed items; add "review_status" filter to `export_to_jsonl()`, `export_to_csv()`, `export_to_huggingface()`. Track approved vs total ratios. | Medium | #7, #10 |
| 15 | **Docker Deployment & Configuration** | Dockerfile + docker-compose for the dashboard; environment-based config for store path, auth settings, pipeline adapters to enable. | Medium | #1 |
| 16 | **Documentation & Contributor Guide** | README with screenshots, setup guide, workflow docs; developer docs for adding new pipeline adapters; annotated example review session. | Easy | #9, #12 |
| 17 | **CI/CD & GitHub Actions** | Lint/type-check/test on PR; build + test Docker image; optional deploy trigger. | Easy | #15 |

---

## Technology Choices

| Component | Choice | Rationale |
|-----------|--------|-----------|
| **Framework** | **Gradio** (first-class `gr.Audio`, `gr.Dataframe`) | Already in AAL requirements.txt; excellent for ML demo UIs; built-in audio support; faster to ship than full Django/Flask |
| **Backend State** | **JSONL Store** (existing `store.py`) | Zero infrastructure; matches existing AAL patterns; easy to inspect/debug |
| **Audio Player** | **Gradio Audio** + **WaveSurfer.js** | Gradio for basic playback; WaveSurfer.js embedded via `gr.HTML` for segment timeline |
| **Auth** | **Simple token/config** | No DB overhead; sufficient for lab setting; upgrade path to OAuth later |
| **Visualization** | **Plotly** (via Gradio `gr.Plot`) | Interactive charts for quality metrics; works well in Gradio |
| **Packaging** | **pip install -e .** (in extras) | Consistent with `pyproject.toml` pattern |

---

## Implementation Order

```
Sprint 1 (Foundation)
  Issue #1  →  Scaffold
  Issue #2  →  Review Queue + Store
  Issue #4  →  Auth

Sprint 2 (Audio Review)
  Issue #5  →  Audio Player
  Issue #6  →  ASR Review
  Issue #7  →  Label Review
  Issue #9  →  AAL Dashboard Home

Sprint 3 (XENI Review)
  Issue #10 →  Article Review
  Issue #11 →  Disagreement Resolution
  Issue #12 →  XENI Dashboard Home

Sprint 4 (Quality & Polish)
  Issue #3  →  Quality Metrics
  Issue #13 →  Batch Operations

Sprint 5 (Export & Deploy)
  Issue #14 →  Export Pipeline
  Issue #15 →  Docker
  Issue #16 →  Documentation
  Issue #17 →  CI/CD
```

---

## Files to Create / Modify

### New Files
```
pipelines/review-dashboard/
├── __init__.py
├── pyproject.toml
├── core/
│   ├── __init__.py
│   ├── auth.py              # Simple auth
│   ├── queue.py             # Review queue manager
│   ├── models.py            # ReviewSession, ReviewDecision
│   ├── metrics.py           # Quality metrics engine
│   └── export.py            # Export service
├── adapters/
│   ├── __init__.py
│   ├── aal.py               # AAL adapter
│   └── xeni.py              # XENI adapter
├── config/
│   └── default_config.yaml  # Default configuration
└── app.py                   # Main Gradio app entry point
```

### Modified Files
```
pipelines/audio-annotation-lab/
├── interface/               # ← AAL adapter already lives here
│   ├── app.py               # ← Overhaul or integrate with review-dashboard

pipelines/audio-annotation-lab/database/store.py
  # Add review-decision persistence

pipelines/audio-annotation-lab/export/
  # Add review-status filters

pipelines/shared/            # ← Add shared models if needed
```

---

## Review Workflow (End-to-End)

```
1. Pipeline generates annotations (LLM or ASR)
2. quality/confidence.py scores each segment
3. quality/review.py builds review queue (low-conf items)
4. Dashboard fetches queue from Store
5. Reviewer opens item → sees data + audio (if AAL)
6. Reviewer: Approve / Reject with reason / Correct labels
7. Decision saved to Store as ReviewDecision
8. Once all items reviewed → quality/agreement.py generates report
9. export/ layer exports only approved items
```

---

## Existing Code That Gets Reused

| Module | What We Reuse |
|--------|---------------|
| `quality/review.py` | `ReviewItem`, `create_review_queue()`, `priority_sort()`, `review_stats()` |
| `quality/confidence.py` | `label_confidence()`, `segment_confidence()`, `threshold_filter()`, `confidence_distribution()` |
| `quality/agreement.py` | `krippendorff_alpha()`, `cohens_kappa()`, `pairwise_agreement_matrix()`, `agreement_report()` |
| `database/store.py` | `Store` class with full CRUD for sessions, segments, annotations |
| `database/models.py` | `AudioSession`, `AudioSegment`, `Annotation` dataclasses |
| `annotation/adjudicate.py` | `majority_vote()`, `confidence_weighted()`, `adjudicate_segment()` |
| `audio_annotate.py` | `context_window()`, `merge_adjacent_segments()`, `split_long_segment()` |
| `export/*.py` | `to_jsonl.py`, `to_csv.py`, `to_huggingface.py` |
