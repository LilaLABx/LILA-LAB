# Annotation Schemas

## Purpose

Each domain you want to measure gets its own annotation schema. The schema defines what categories the LLM annotator will classify articles into.

## Schema Format

Each schema is a JSON file defining:

```json
{
  "domain": "economic",
  "version": "1.0",
  "description": "Economic narrative annotation schema",
  "fields": [
    {
      "name": "economic_relevance",
      "type": "binary",
      "values": ["Economic", "Not Economic"],
      "description": "Whether the article discusses economic topics"
    },
    {
      "name": "sentiment",
      "type": "ordinal",
      "values": ["negative", "neutral", "positive"],
      "description": "Overall economic sentiment"
    }
  ]
}
```

## Included Schemas

| File | Domain | Description |
|------|--------|-------------|
| `economic.json` | Economics | Economic narrative categories (reference from BENI) |
| `health.json` | Health | Health discourse categories (template) |

## Instructions

1. **Copy an existing schema** or create from scratch
2. **Define fields relevant to your domain**:
   - `binary` fields for relevance filtering
   - `multiclass` fields for topic classification
   - `ordinal` fields for sentiment/scale
3. **Name the file `{domain}.json`** — this name becomes the index subdirectory name
4. **Test with `llm_annotate.py`** — run a small batch to validate the schema works

## Deliverable

- `{domain}.json` — A validated annotation schema for each domain
- At least one domain schema must be complete before annotation can begin
