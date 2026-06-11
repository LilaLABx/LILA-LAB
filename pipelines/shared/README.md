# LILA Lab — Shared Pipeline Utilities

Language-agnostic tools imported by all XENI pipelines. Keep these generic — any language- or domain-specific logic belongs in the pipeline itself.

## Modules

| Module | Description |
|--------|-------------|
| `llm/` | LLM client wrappers (Anthropic, OpenAI, Google) + response parsing |
| `analysis/` | Narrative index construction, correlation, time-series tools |
| `stats/` | Inter-annotator agreement, statistical tests |
| `config.py` | Configuration loading (YAML, env vars) |
| `data.py` | Data loading, splitting, preprocessing |
| `eval.py` | Classification evaluation metrics |
| `io.py` | File I/O (JSON, CSV, JSONL) |
| `models.py` | Classifier definitions (TF-IDF, BERT wrappers) |

## Usage

```python
from shared.llm import LLMClient
from shared.stats.agreement import krippendorff_alpha

client = LLMClient(model="claude-3-5-sonnet")
response = client.annotate(article_text, schema=economic_schema)
```

## Adding a New Utility

1. Add your module to the appropriate subdirectory
2. Export public API in `__init__.py`
3. Write tests in `tests/`
4. Import via `from shared.<module> import <thing>`

## Related

- `pipelines/template/` — Uses shared utilities as the default
- `pipelines/BENI/` — Reference implementation that exercises all shared modules
