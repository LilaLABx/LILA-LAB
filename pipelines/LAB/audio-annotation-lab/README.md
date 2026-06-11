# Audio Annotation Lab (AAL)

> **Turning speech in low-resource languages into structured, annotated data for narrative intelligence.**

The Audio Annotation Lab is LILA Lab's cross-modal annotation infrastructure. While XENI pipelines handle **text** (news articles), AAL handles **speech** — the original modality of every language. For low-resource languages that lack written news ecosystems, audio is often the only medium where narratives exist.

---

## Why Audio Annotation?

| Challenge | Audio Advantage |
|-----------|----------------|
| 40% of the world's languages lack a standard writing system | Audio captures oral narratives directly |
| News ecosystems are sparse in low-resource languages | Community radio, social media audio, and interviews are abundant |
| LLMs work primarily in text | Audio → transcription bridges the gap; LLMs then annotate what was said |
| Economic/financial narratives exist orally | Policy speeches, farmer interviews, market talk — all happen in spoken language |

**The vision:** Any audio in any language → transcription → LLM annotation → narrative index. The same downstream pipeline as XENI, but the input is speech.

---

## Architecture Overview

```
Audio files (MP3/WAV/OGG/FLAC)
    │
    ▼
┌──────────────────────────────────────────────┐
│              1. ASR PIPELINE                  │
│                                               │
│  Audio → Preprocessing → Diarization → STT   │
│  (ffmpeg)    (noise reduction,   (Whisper,   │
│              resampling,         wav2vec2,   │
│              silence removal)    local ASR)   │
│                                  │            │
│                                  ▼            │
│                      Forced Alignment         │
│                      (word-level timestamps)  │
└──────────────────┬───────────────────────────┘
                   │
                   ▼ Transcript (JSONL with segments, speakers, timestamps)
                   │
                   ▼
┌──────────────────────────────────────────────┐
│              2. ANNOTATION LAYER              │
│                                               │
│  ┌─────────────────────┐  ┌─────────────────┐ │
│  │ LLM Annotation      │  │ Manual           │ │
│  │ (on transcribed     │  │ Annotation       │ │
│  │  text segments)     │  │ (UI-based)       │ │
│  │                     │  │                  │ │
│  │ - Speaker labeling  │  │ - Segment        │ │
│  │ - Sentiment/tone    │  │   boundary fix   │ │
│  │ - Topic/narrative   │  │ - Transcription  │ │
│  │ - Entity extraction │  │   correction     │ │
│  │ - Economic signal   │  │ - Label          │ │
│  │   classification    │  │   verification   │ │
│  └─────────────────────┘  └─────────────────┘ │
│              │              │                  │
│              ▼              ▼                  │
│         ┌────────────────────────┐             │
│         │    Adjudication        │             │
│         │  (resolve conflicts)   │             │
│         └────────────────────────┘             │
└──────────────────┬───────────────────────────┘
                   │
                   ▼ Annotated segments (JSONL)
                   │
                   ▼
┌──────────────────────────────────────────────┐
│          3. QUALITY CONTROL                   │
│                                               │
│  Inter-annotator agreement (Krippendorff's α) │
│  Confidence scoring per segment               │
│  Review queues for low-confidence labels      │
└──────────────────┬───────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────┐
│          4. EXPORT LAYER                      │
│                                               │
│  JSONL (LILA standard format)                 │
│  CSV (spreadsheet-friendly)                   │
│  Hugging Face Datasets format                 │
│  XENI-compatible (for direct ingestion)       │
└──────────────────────────────────────────────┘
                   │
                   ▼
         XENI Pipeline-ready data
         (narrative index construction)
```

---

## Directory Structure

```
pipelines/audio-annotation-lab/
│
├── README.md                       # This file
├── requirements.txt                # Dependencies (whisper, torch, etc.)
│
├── asr/                            # Automatic Speech Recognition
│   ├── __init__.py
│   ├── transcribe.py               # Main ASR pipeline (Whisper/local models)
│   ├── align.py                    # Forced alignment (text-to-audio)
│   ├── preprocess.py               # Audio preprocessing (noise reduction, VAD)
│   └── models.py                   # ASR model configuration registry
│
├── annotation/                     # Annotation infrastructure
│   ├── __init__.py
│   ├── llm_annotate.py             # LLM annotation on transcribed segments
│   ├── adjudicate.py               # Resolve annotation disagreements
│   ├── audio_annotate.py           # Audio-segment-specific annotation logic
│   └── schemas/                    # Annotation schemas (JSON)
│       ├── speaker.json            # Speaker diarization schema
│       ├── sentiment.json          # Sentiment/tone schema
│       ├── topic.json              # Topic classification schema
│       └── narrative.json          # Narrative/economic signal schema
│
├── interface/                      # Annotation UI (future)
│   ├── __init__.py
│   ├── app.py                      # Gradio/Streamlit web interface
│   ├── audio_player.py             # Custom audio player with segments
│   └── timeline.py                 # Timeline visualization for segments
│
├── database/                       # Storage layer
│   ├── __init__.py
│   ├── models.py                   # SQLAlchemy/SQLite ORM models
│   └── store.py                    # Data access layer
│
├── export/                         # Export to standard formats
│   ├── __init__.py
│   ├── to_jsonl.py                 # LILA-standard JSONL export
│   ├── to_csv.py                   # CSV/Excel export
│   └── to_huggingface.py           # Hugging Face Dataset format
│
├── quality/                        # Quality control
│   ├── __init__.py
│   ├── agreement.py                # Inter-annotator agreement metrics
│   ├── confidence.py               # Confidence scoring
│   └── review.py                   # Review workflow
│
├── utils/                          # Shared utilities
│   ├── __init__.py
│   ├── audio.py                    # Audio I/O (ffmpeg wrapper, format conversion)
│   └── viz.py                      # Audio waveform + segment visualization
│
└── data/                           # Data directory
    ├── raw/                        # Raw audio files
    ├── processed/                  # Transcribed/processed audio
    ├── annotations/                # Annotation outputs
    └── exports/                    # Exported datasets
```

---

## Data Model

The core data model follows a **session → segment → annotation** hierarchy:

```
AudioSession                    AudioSegment                    Annotation
┌─────────────────┐           ┌─────────────────────┐         ┌────────────────────┐
│ id: UUID        │──1:N──▶   │ id: UUID            │──1:N──▶ │ id: UUID           │
│ file_path: str  │           │ session_id: UUID    │         │ segment_id: UUID   │
│ duration: float │           │ start_time: float   │         │ annotator: str     │
│ sample_rate: int│           │ end_time: float     │         │ annotator_type:    │
│ channels: int   │           │ speaker: str        │         │   (llm|human)      │
│ format: str     │           │ transcript: str     │         │ labels: dict       │
│ metadata: dict  │           │ confidence: float   │         │ confidence: float  │
│ created_at: dt  │           │ language: str       │         │ created_at: dt     │
└─────────────────┘           └─────────────────────┘         └────────────────────┘
```

### Segment Types

| Type | Description | Example |
|------|-------------|---------|
| **utterance** | A single speaker's turn | "The price of rice has gone up again" |
| **sentence** | Grammatical sentence boundary | "Farmers are struggling this season." |
| **word** | Individual word with timestamp | "rice" [2.3s–2.6s] |
| **custom** | User-defined segment boundary | Any manual selection |

---

## ASR Pipeline

### Supported Models

| Model | Language Support | Local? | Quality | Use Case |
|-------|-----------------|--------|---------|----------|
| **Whisper** (openai/whisper) | 100+ langs, incl. low-resource | ✅ Yes | ★★★★ | General-purpose, best first-pass |
| **WhisperX** (faster-whisper) | Same as Whisper | ✅ Yes | ★★★★ | + word-level timestamps, speaker diarization |
| **wav2vec2-XLSR** | 100+ langs (fine-tuned) | ✅ Yes | ★★★☆ | Lightweight, good for specific languages |
| **SeamlessM4T** | 100+ langs | ⚠️ GPU needed | ★★★★ | Speech-to-text + translation |
| **Local fine-tunes** | Single language | ✅ Yes | ★★★★☆ | Best for a specific low-resource language |

### Pipeline Steps

1. **Preprocessing** — Normalize sample rate (16kHz), convert format, noise reduction, VAD (voice activity detection) to strip silence
2. **Diarization** — Identify who speaks when (WhisperX/pyannote)
3. **Transcription** — Run ASR model on each speaker segment
4. **Forced Alignment** — Map words to precise timestamps (whisper-timestamped, CTC segmentation)
5. **Output** — JSONL with full segment structure

### CLI Usage

```bash
# Transcribe a single file
python -m pipelines.audio_annotation_lab.asr.transcribe \
    --input data/raw/interview.mp3 \
    --output data/processed/ \
    --model whisper-large-v3 \
    --language bengali \
    --device cuda

# Batch transcribe a directory
python -m pipelines.audio_annotation_lab.asr.transcribe \
    --input data/raw/ \
    --batch \
    --output data/processed/
```

---

## Annotation Pipeline

### LLM Annotation

Adapts the XENI `llm_annotate.py` pattern for audio transcripts. Each transcribed segment is treated as an annotation unit (analogous to a news article):

```bash
python -m pipelines.audio_annotation_lab.annotation.llm_annotate \
    --input data/processed/session_001.jsonl \
    --schema annotation/schemas/narrative.json \
    --output data/annotations/
```

### Schemas

Schemas follow the same JSON format as XENI pipelines:

```json
{
  "domain": "economic_narrative",
  "description": "Economic narrative annotation for audio segments",
  "primary_field": "economic_relevance",
  "fields": [
    {
      "name": "economic_relevance",
      "description": "Does this segment discuss economic topics?",
      "options": ["relevant", "not_relevant", "tangential"],
      "type": "categorical"
    },
    {
      "name": "sentiment",
      "description": "Overall economic sentiment expressed",
      "options": ["positive", "negative", "neutral", "mixed"],
      "type": "categorical"
    },
    {
      "name": "topic",
      "description": "Primary economic topic discussed",
      "options": [
        "prices_inflation",
        "employment_wages",
        "agriculture",
        "trade_commerce",
        "finance_banking",
        "infrastructure",
        "general"
      ],
      "type": "categorical"
    }
  ]
}
```

### Manual Annotation (UI)

A Gradio-based web interface for:
- **Transcription review** — Listen to segments, correct ASR errors
- **Label assignment** — Apply schema labels to segments
- **Segment boundary adjustment** — Fix start/end times
- **Speaker identification** — Name unknown speakers

---

## Quality Control

### Inter-Annotator Agreement

| Metric | Purpose | Target |
|--------|---------|--------|
| Krippendorff's α | Multi-annotator categorical agreement | ≥ 0.80 |
| Cohen's κ | Pairwise annotator agreement | ≥ 0.80 |
| Word Error Rate (WER) | ASR transcription accuracy | ≤ 20% |
| Confidence threshold | Minimum confidence per label | ≥ 0.70 |

### Review Workflow

```
Annotated segments (LLM + Human)
    │
    ▼
Score confidence per segment
    │
    ├── Confidence ≥ 0.80 → Auto-accept
    ├── 0.50 ≤ Confidence < 0.80 → Queue for human review
    └── Confidence < 0.50 → Re-annotate with different model/annotator
```

---

## Integration with XENI Pipelines

**AAL output is XENI-compatible by design.** Transcribed and annotated audio segments share the same JSONL format as XENI news articles:

```
# XENI news article
{
  "id": "article_001",
  "text": "The central bank raised interest rates...",
  "source": "daily_star",
  "date": "2024-01-15",
  "annotation": {
    "economic_relevance": "relevant",
    "sentiment": "negative",
    "topic": "finance_banking"
  }
}

# AAL audio segment (same schema)
{
  "id": "seg_001",
  "text": "The central bank raised interest rates...",
  "source": "community_radio_interview",
  "date": "2024-01-15",
  "audio_file": "interview.mp3",
  "start_time": 142.5,
  "end_time": 148.3,
  "speaker": "economist_1",
  "annotation": {
    "economic_relevance": "relevant",
    "sentiment": "negative",
    "topic": "finance_banking"
  }
}
```

This means any XENI pipeline can ingest AAL-annotated audio data **without modification** — the `index/` and `experiment/` modules work identically.

---

## Roadmap

| Phase | What | Status |
|-------|------|--------|
| **1** | Core ASR pipeline (Whisper + forced alignment) | 🔜 Planned |
| **2** | LLM annotation on transcripts | 🔜 Planned |
| **3** | Manual annotation UI (Gradio) | 💡 Proposed |
| **4** | Quality control + adjudication | 💡 Proposed |
| **5** | Export layer (JSONL → XENI-compatible) | 🔜 Planned |
| **6** | Multilingual fine-tuning for low-resource ASR | 💡 Proposed |
| **7** | Real-time annotation streaming | 💡 Future |

---

## Dependencies

```
openai-whisper>=20231117    # ASR transcription
faster-whisper>=1.0.0       # Optimized Whisper
torch>=2.0.0                # ML backend
transformers>=4.36.0        # wav2vec2, SeamlessM4T
datasets>=2.14.0            # HuggingFace integration
soundfile>=0.12.0           # Audio I/O
librosa>=0.10.0             # Audio analysis
jiwer>=3.0.0                # WER computation
krippendorff>=0.3.0         # Agreement metrics
numpy>=1.24.0               # Numeric ops
pandas>=2.0.0               # Data handling
pydantic>=2.0.0             # Data validation
gradio>=4.0.0               # Annotation UI (optional)
```

See `requirements.txt` for pinned versions.

---

## Getting Started

```bash
# 1. Install dependencies
pip install -r pipelines/audio-annotation-lab/requirements.txt

# 2. Transcribe audio
python -m pipelines.audio_annotation_lab.asr.transcribe \
    --input my_audio.mp3 \
    --output data/processed/

# 3. Annotate transcripts
python -m pipelines.audio_annotation_lab.annotation.llm_annotate \
    --input data/processed/session.jsonl \
    --schema pipelines/audio-annotation-lab/annotation/schemas/narrative.json \
    --output data/annotations/

# 4. Quality check
python -m pipelines.audio_annotation_lab.quality.agreement \
    --input data/annotations/*.jsonl

# 5. Export for XENI ingestion
python -m pipelines.audio_annotation_lab.export.to_jsonl \
    --input data/annotations/final.jsonl \
    --output data/exports/xeni_ready.jsonl
```

---

## Relation to LILA Lab's Mission

> **"Your language. Your stories. Amplified by AI."**

Audio is the original medium for stories. For communities without written news traditions, spoken narratives carry economic signals, policy debates, and cultural knowledge that text pipelines miss. The Audio Annotation Lab bridges this gap:

| Problem | AAL Solution |
|---------|-------------|
| "My language has no newspapers" | Record community radio, interviews, oral histories |
| "ASR doesn't work for my language" | Fine-tune Whisper on a small sample (1 hour = usable) |
| "I have hours of audio but no annotations" | LLM annotation on transcripts costs cents per hour |
| "I need to build a narrative index" | AAL output feeds directly into XENI pipelines |

---

**Any language, any modality. If someone speaks it, we can measure it.**
