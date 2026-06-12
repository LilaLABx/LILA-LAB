# ADR-005: Multi-Language Coordination Protocol

**Status:** Accepted

**Date:** 2026-06-12

## Context

LILA Lab targets 10 emerging-economy languages by H1 2027. Each language runs a separate XENI pipeline (BENI, AENI, NENI, etc.) with its own dataset, annotation schemas, and research outputs. Without a coordination protocol, several failure modes emerge:

- **Version divergence**: Pipelines drift to incompatible schema versions, making cross-language comparison impossible
- **Duplicate effort**: Two pipelines independently solve the same annotation problem (e.g., economic domain schema design)
- **Coordination opacity**: No single source of truth shows which pipelines are active, at what maturity, and on which schemas
- **Publication fragmentation**: Research outputs from individual pipelines are published without cross-reference, obscuring the unified framework

The challenge is to balance **pipeline autonomy** (each language has unique characteristics) with **framework cohesion** (all pipelines are recognizably the same approach).

## Decision

We adopt a **registry-driven coordination model** centered on three machine-readable registries in `registry/`:

### 1. Pipeline Status Registry (`registry/languages.json`)

A single JSON file listing every language pipeline, its status (bootstrapped, feasibility, active), responsible contributors, and schema version. This is the source of truth for pipeline state.

```json
{
  "BENI": {
    "language": "Bangla",
    "status": "active",
    "schema_version": "1.2.0",
    "contributors": ["Ann Naser Nabil"],
    "target_completion": "2027-01-01"
  }
}
```

### 2. Pipeline Contract (`registry/xeni_pipeline_contract.json`)

A machine-readable contract that each pipeline must satisfy to be considered valid. This replaces ad-hoc validation with an enforceable schema:

- Required directory structure
- Required metadata files
- Schema version compatibility
- Minimum documentation requirements

### 3. Schema Registry (`registry/schemas.json`)

Maps each domain + pipeline combination to its current schema version. Enables cross-pipeline schema comparison and drift detection.

### Coordination Rhythm

| Frequency | Activity | Mechanism |
|-----------|----------|-----------|
| Per commit | Validate pipeline structure against contract | `python -m cli validate` + CI |
| Per schema change | Bump version per ADR-004, update registries | Manual + CI validation |
| Per release | Update languages.json, publications.bib | Manual |
| Quarterly | Cross-pipeline schema alignment review | Maintainer review |

### Cross-Pipeline Relationships

```
registry/languages.json  ───── controls ──→ Pipeline existence & status
         │
         ├── references ──→ registry/schemas.json  ──→ Per-pipeline schema versions
         │
         └── references ──→ registry/publications.bib  ──→ All pipeline publications
```

## Consequences

### Positive

- **Single source of truth**: Anyone can check `registry/languages.json` to see the state of all 10 pipelines
- **Automated validation**: The pipeline contract enforces structure without manual review
- **Cross-language research**: Schema version tracking enables identical annotation across languages, supporting cross-lingual narrative index comparison
- **Contributor clarity**: New pipeline contributors know exactly what metadata they need to provide

### Negative

- **Registry maintenance**: Adding a new language requires updating `languages.json` and `xeni_pipeline_contract.json` — handled by the template bootstrap process
- **Validation dependency**: CI must run `python -m cli validate` to enforce the contract; if the CLI tool breaks, all pipeline validation fails
- **Schema alignment cost**: Quarterly alignment reviews require maintainer time — but this is necessary for framework cohesion

### Neutral

- This protocol is designed for 10 languages. If the project grows to 50+, a database-backed registry or dashboard may be needed
- Individual pipelines retain full autonomy over their annotation schemas, experiment code, and publication timeline — the protocol only mandates what is shared
