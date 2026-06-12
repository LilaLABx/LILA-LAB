# ADR-004: LLM Annotation Schema Versioning

**Status:** Accepted

**Date:** 2026-06-12

## Context

The BENI pipeline uses multi-LLM annotation (Claude, GPT-4o, Gemini) to label news articles across economic narrative domains. The annotation schemas — domain definitions, label taxonomies, prompt templates, and adjudication rules — evolve as research progresses. Without explicit versioning, three failure modes occur:

1. **Schema drift**: Old annotations become incomparable with new ones when schemas change without a version marker
2. **Replicability failure**: A researcher running `llm_annotate.py` next month may get different labels for the same article because the schema changed silently
3. **Cross-pipeline confusion**: When AENI or NENI adopt the same annotation framework, they need to know which schema version they are targeting

The BENI annotation pipeline had reached a point where schema changes were frequent enough (new domains, refined label definitions, improved prompts) that implicit versioning through Git commits was insufficient — researchers needed explicit, machine-readable schema version declarations.

Several alternatives were considered: (a) rely on Git commit hashes as de facto versions, (b) use a single global version number for all schemas, (c) version each domain schema independently. Git hashes are not human-readable for cross-reference; a single version number conflates unrelated schema changes; independent domain versions add complexity.

## Decision

We adopt **semantic versioning for annotation schemas**, with each schema file declaring its own version:

### Schema Version Format

Each annotation schema JSON file (`annotation/schemas/*.json`) must include a `"version"` field following SemVer:

```json
{
  "version": "1.2.0",
  "domain": "economic",
  "pipeline": "BENI",
  "labels": [...],
  "prompt_template": "...",
  "adjudication_rules": {...}
}
```

### Version Semantics

| Component | Change triggers |
|-----------|----------------|
| **MAJOR** (1.x.x) | Incompatible label set changes, domain redefinition, prompt restructuring that breaks backward compatibility |
| **MINOR** (x.2.x) | New labels added, prompt refinements, adjudication rule additions — backward compatible |
| **PATCH** (x.x.3) | Typo fixes, example clarifications, metadata updates — no behavioral change |

### Schema Registry

All active schemas are registered in `registry/schemas.json` with their current version. The `validate_schemas.py` CI check enforces:
- Every schema file has a version field
- No duplicate versions for the same domain-pipeline combination
- Version bumps follow SemVer rules

### Annotation Output

Every annotation output record includes the schema version used:

```json
{
  "article_id": "...",
  "schema_version": "1.2.0",
  "annotations": [...],
  "llm_model": "claude-3-opus-20240229"
}
```

### When to Bump

- **Bump MAJOR** when removing or renaming labels
- **Bump MINOR** when adding labels or refining prompts
- **Bump PATCH** for non-functional corrections

## Consequences

### Positive

- **Replicability**: Any annotation output records exactly which schema version produced it
- **Cross-pipeline coordination**: AENI/NENI can reference BENI's schema version when adopting the same framework
- **CI-enforceable**: Version checks are automated via `validate_schemas.py`
- **Clear upgrade path**: Downstream consumers (index builders, analysis scripts) can detect schema version changes programmatically

### Negative

- **Ongoing maintenance**: Schema authors must remember to bump versions on changes — mitigated by CI validation
- **Version proliferation**: Many minor versions may accumulate; periodic major version consolidation is recommended
- **Coordination overhead**: When schemas are shared across pipelines, a version bump in BENI may require validation in AENI

### Neutral

- This ADR does not mandate a specific version control workflow — schema files remain in the monorepo and version bumps happen as part of regular commits
- The full schema change history is still tracked via Git
