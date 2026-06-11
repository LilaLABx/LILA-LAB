# LILA Lab Maturity and Structure Fine-Tuning Plan

## TL;DR
> Summary:      Refine the existing LILA Lab monorepo into a mature low-resource-language research lab platform without a disruptive rewrite. The work aligns governance, XENI pipeline contracts, CI, reproducibility, registry/data-release practices, and contributor-facing structure.
> Deliverables:
> - A documented repository ownership map and lab operating model.
> - A machine-checkable XENI pipeline contract with validation tests.
> - Aligned local/CI quality gates.
> - Reproducibility and release checklists based on FAIR, The Turing Way, and dataset-card norms.
> - A minimal CLI validation/status surface before API/dashboard expansion.
> Effort:       Large
> Risk:         Medium - broad repo surface, existing CI failures, and multiple placeholder/planned surfaces.

## Scope
### Must have
- Preserve the current monorepo and its public LILA Lab identity.
- Treat `pipelines/BENI/` as the reference implementation and `pipelines/template/` as the bootstrap source.
- Define clear source-of-truth boundaries for `pipelines/`, `dataset/`, `technical-reports/`, `registry/`, `dist/`, `docs/`, `infrastructure/`, `communications/`, `api/`, and `cli/`.
- Make the XENI pipeline contract machine-checkable across BENI, template, and all target-language scaffold directories.
- Align `pyproject.toml`, `Makefile`, `.pre-commit-config.yaml`, and `.github/workflows/ci.yml` so contributors run the same checks locally and in CI.
- Add reproducibility and release standards for data, code, model outputs, annotation decisions, and research reports.
- Build a small CLI validation/status layer before implementing REST API or dashboards.
- Preserve ignored local secrets and large artifacts, especially `infrastructure/discord-bot/.env`.

### Must NOT have
- Do not fine-tune ML models in this workstream.
- Do not rewrite or relocate the whole repo unless a todo explicitly requires a small, reviewed move.
- Do not delete or weaken tests to pass CI.
- Do not commit ignored local data, `.env`, PDFs, zips, model weights, pycache, or `personal/`.
- Do not claim a language pipeline is operational merely because a template directory exists.
- Do not implement the REST API or dashboard before registry, validation, and release contracts are stable.

## Verification Strategy
> Zero human intervention - all verification is agent-executed.
- Test decision: TDD / characterization for executable tooling and CI changes; tests-after for documentation-only changes.
- QA policy: every todo has command-level or file-content evidence captured under `.omo/evidence/`.
- Evidence: `.omo/evidence/task-<N>-research-lab-structure-finetune.<ext>`
- External standards:
  - FAIR data principles: https://www.nature.com/articles/sdata201618
  - The Turing Way reproducibility guidance: https://book.the-turing-way.org/reproducible-research/reproducible-research/
  - Hugging Face dataset-card conventions: https://huggingface.co/docs/hub/datasets-cards

## Execution Strategy
### Parallel Execution Waves
Wave 1 (no deps): Todos 1, 2, 3, 4, 5.
Wave 2 (after 1-5): Todos 6, 7, 8, 9.
Wave 3 (after 6-9): Todos 10, 11, 12.
Wave 4 (after 10-12): Todo 13 and final verification.
Critical path: Todo 1 -> Todo 2 -> Todo 6 -> Todo 10 -> Todo 13.

### Dependency Matrix
| Todo | Depends on | Blocks | Can parallelize with |
| --- | --- | --- | --- |
| 1 | None | 2, 6, 10, 13 | 3, 4, 5 |
| 2 | 1 | 6, 7, 10, 13 | 3, 4, 5 |
| 3 | None | 8, 13 | 1, 2, 4, 5 |
| 4 | None | 9, 13 | 1, 2, 3, 5 |
| 5 | None | 9, 12, 13 | 1, 2, 3, 4 |
| 6 | 1, 2 | 10, 13 | 7, 8, 9 |
| 7 | 2 | 10, 13 | 6, 8, 9 |
| 8 | 3 | 10, 13 | 6, 7, 9 |
| 9 | 4, 5 | 11, 12, 13 | 6, 7, 8 |
| 10 | 1, 2, 6, 7, 8 | 13 | 11, 12 |
| 11 | 9 | 13 | 10, 12 |
| 12 | 5, 9 | 13 | 10, 11 |
| 13 | 10, 11, 12 | Final verification | None |

## Todos
> Implementation + Test = ONE todo. Never separate.

- [x] 1. Define the repository operating model
  What to do / Must NOT do:
  Write `docs/REPOSITORY_OPERATING_MODEL.md` that defines each top-level area, what belongs there, what does not, and the source of truth for pipeline status, dataset releases, manuscripts, public docs, infrastructure, and private/local artifacts. Update `README.md` and `CONTRIBUTING.md` to link to it. Do not move files in this todo.
  Parallelization: Can parallel Y | Wave 1 | Blocks 2, 6, 10, 13
  References: `README.md` repository overview; `docs/archive/RESTRUCTURE_PLAN.md:1`; `.gitignore:42`; `CONTRIBUTING.md:7`; `docs/COLLABORATION.md:153`
  Acceptance criteria: `test -f docs/REPOSITORY_OPERATING_MODEL.md && rg "source of truth|Must not contain|registry/languages.json|dataset/|pipelines/" docs/REPOSITORY_OPERATING_MODEL.md README.md CONTRIBUTING.md`
  QA scenarios:
  - Happy: `python - <<'PY'` reads `docs/REPOSITORY_OPERATING_MODEL.md` and asserts every top-level tracked directory from `git ls-files | cut -d/ -f1 | sort -u` is either documented or explicitly excluded; evidence `.omo/evidence/task-1-research-lab-structure-finetune.txt`.
  - Failure: same script asserts `personal/`, `.env`, `__pycache__`, PDFs, and zips are listed as out-of-scope/private/generated; evidence `.omo/evidence/task-1-research-lab-structure-finetune-negative.txt`.
  Commit: Y | `docs(repo): define lab operating model` | `docs/REPOSITORY_OPERATING_MODEL.md`, `README.md`, `CONTRIBUTING.md`

- [x] 2. Create a machine-checkable XENI pipeline contract
  What to do / Must NOT do:
  Add `registry/xeni_pipeline_contract.json` defining required files, directories, config fields, schema rules, status meanings, and release-readiness criteria. Add `tests/test_xeni_pipeline_contract.py` that validates `pipelines/template/`, `pipelines/BENI/`, and all registry-listed pipelines against status-aware rules. Do not require not-started pipelines to have real data.
  Parallelization: Can parallel Y | Wave 1 | Blocks 6, 7, 10, 13
  References: `pipelines/README.md:81`; `pipelines/template/README.md:17`; `registry/languages.json:1`; `registry/schemas.json:1`; `tests/conftest.py:18`
  Acceptance criteria: `python -m pytest tests/test_xeni_pipeline_contract.py -q`
  QA scenarios:
  - Happy: `python -m pytest tests/test_xeni_pipeline_contract.py -q | tee .omo/evidence/task-2-research-lab-structure-finetune.txt` must pass.
  - Failure: temporarily copy one pipeline README to a temp dir without required metadata and run the contract validator in a subprocess expecting nonzero exit; evidence `.omo/evidence/task-2-research-lab-structure-finetune-negative.txt`.
  Commit: Y | `test(pipelines): add xeni contract validation` | `registry/xeni_pipeline_contract.json`, `tests/test_xeni_pipeline_contract.py`

- [x] 3. Align local and CI quality gates
  What to do / Must NOT do:
  Decide the intended lint scope once and apply it consistently to `pyproject.toml`, `Makefile`, `.pre-commit-config.yaml`, and `.github/workflows/ci.yml`. Either include BENI and fix scoped failures, or keep BENI advisory everywhere. Fix current scoped Ruff failures in `pipelines/shared/`, `pipelines/template/`, `infrastructure/`, and `tests/` without weakening rules.
  Parallelization: Can parallel Y | Wave 1 | Blocks 8, 13
  References: `pyproject.toml:57`; `Makefile:40`; `.github/workflows/ci.yml:14`; `.pre-commit-config.yaml:7`
  Acceptance criteria: `make lint && ruff format pipelines/shared/ pipelines/template/ infrastructure/ tests/ --check`
  QA scenarios:
  - Happy: `make lint | tee .omo/evidence/task-3-research-lab-structure-finetune.txt` exits 0.
  - Failure: `python - <<'PY'` parses `Makefile`, `pyproject.toml`, `.pre-commit-config.yaml`, and `.github/workflows/ci.yml` and asserts the lint scopes mention the same enforced/advisory boundaries; evidence `.omo/evidence/task-3-research-lab-structure-finetune-scope.txt`.
  Commit: Y | `ci: align lint scopes across local and github checks` | `pyproject.toml`, `Makefile`, `.pre-commit-config.yaml`, `.github/workflows/ci.yml`, linted Python files

- [x] 4. Fix schema validation so CI checks real schemas
  What to do / Must NOT do:
  Update CI schema validation and local validation commands to check actual `annotation/schemas/*.json` files, not only `*.schema.json`. Add a small reusable validator script under `infrastructure/scripts/validate_schemas.py` or `registry/validate_schemas.py`. Do not ignore planned schemas with `location: null`; validate only files that exist and registry entries that claim stable locations.
  Parallelization: Can parallel Y | Wave 1 | Blocks 9, 13
  References: `.github/workflows/ci.yml:43`; `registry/schemas.json:1`; `pipelines/BENI/annotation/schemas/economic.json`; `pipelines/template/annotation/schemas/economic.json`
  Acceptance criteria: `python infrastructure/scripts/validate_schemas.py`
  QA scenarios:
  - Happy: `python infrastructure/scripts/validate_schemas.py | tee .omo/evidence/task-4-research-lab-structure-finetune.txt` reports the actual schema count and exits 0.
  - Failure: run validator against a temp invalid JSON schema and assert nonzero exit; evidence `.omo/evidence/task-4-research-lab-structure-finetune-negative.txt`.
  Commit: Y | `ci(schemas): validate actual annotation schemas` | `.github/workflows/ci.yml`, `infrastructure/scripts/validate_schemas.py`, optional tests

- [x] 5. Reconcile data-release and distribution sources of truth
  What to do / Must NOT do:
  Document and validate where dataset cards, release manifests, DOI records, and external platform links live. Create missing `dist/manifests/BENI/` metadata only if authoritative information already exists in `dataset/BENI/` and `dist/README.md`; otherwise mark missing fields as TODO in docs, not as fake published metadata.
  Parallelization: Can parallel Y | Wave 1 | Blocks 9, 12, 13
  References: `dataset/README.md:1`; `dataset/BENI/DATASET_CARD.md`; `dataset/BENI/HUGGINGFACE.md`; `dist/README.md:1`; `technical-reports/README.md:18`
  Acceptance criteria: `python - <<'PY'` verifies every published dataset in `registry/languages.json` has a dataset card or explicit TODO release checklist.
  QA scenarios:
  - Happy: `python - <<'PY' ... PY | tee .omo/evidence/task-5-research-lab-structure-finetune.txt` prints BENI release metadata status and exits 0.
  - Failure: same checker run against a temp registry entry with `dataset_status=complete` and no release metadata must fail; evidence `.omo/evidence/task-5-research-lab-structure-finetune-negative.txt`.
  Commit: Y | `docs(data): reconcile release metadata sources` | `dist/`, `dataset/README.md`, `dataset/BENI/*`, `technical-reports/README.md`

- [x] 6. Convert passive target pipelines into honest status-aware scaffolds
  What to do / Must NOT do:
  Update target pipeline READMEs/configs so AENI, NENI, SENI, CENI, HENI, KIENI, VIENI, TIENI, and IDENI clearly state current status, missing data, next contributor action, and validation commands. Keep template-derived code only if contract tests confirm it is intentionally scaffolded. Do not claim operational results.
  Parallelization: Can parallel Y | Wave 2 | Blocks 10, 13
  References: `registry/languages.json:29`; `pipelines/README.md:60`; `dataset/README.md:9`; `technical-reports/extensions/INDEX.md:9`
  Acceptance criteria: `python -m pytest tests/test_xeni_pipeline_contract.py -q`
  QA scenarios:
  - Happy: `python - <<'PY'` verifies every registry pipeline ID has matching `pipelines/<ID>/README.md`, `dataset/<ID>/README.md`, and status text matching `registry/languages.json`; evidence `.omo/evidence/task-6-research-lab-structure-finetune.txt`.
  - Failure: script asserts no non-BENI README contains unsupported result claims like "active", "collected", or numeric accuracy unless registry status supports it; evidence `.omo/evidence/task-6-research-lab-structure-finetune-negative.txt`.
  Commit: Y | `docs(pipelines): clarify scaffold status for target languages` | `pipelines/*/README.md`, `dataset/*/README.md`, optional configs

- [x] 7. Add registry consistency checks
  What to do / Must NOT do:
  Add tests that cross-check `registry/languages.json`, `registry/schemas.json`, `pipelines/`, `dataset/`, and `technical-reports/extensions/INDEX.md` for drift. Use structured JSON parsing and Markdown table parsing where practical; do not rely only on grep.
  Parallelization: Can parallel Y | Wave 2 | Blocks 10, 13
  References: `registry/languages.json:1`; `registry/schemas.json:1`; `technical-reports/extensions/INDEX.md:11`; `dataset/README.md:9`
  Acceptance criteria: `python -m pytest tests/test_registry_consistency.py -q`
  QA scenarios:
  - Happy: `python -m pytest tests/test_registry_consistency.py -q | tee .omo/evidence/task-7-research-lab-structure-finetune.txt` exits 0.
  - Failure: temp-copy registry with mismatched language ID and assert validator fails; evidence `.omo/evidence/task-7-research-lab-structure-finetune-negative.txt`.
  Commit: Y | `test(registry): prevent pipeline metadata drift` | `tests/test_registry_consistency.py`, registry/docs fixes

- [x] 8. Establish reproducible research run manifests
  What to do / Must NOT do:
  Add a standard run manifest template under `docs/research/RUN_MANIFEST_TEMPLATE.md` or `technical-reports/extensions/RUN_MANIFEST_TEMPLATE.md`, then add a BENI example referencing existing commands without inventing outputs. Include software versions, input data references, command sequence, random seeds, output paths, and validation commands.
  Parallelization: Can parallel Y | Wave 2 | Blocks 10, 13
  References: `technical-reports/README.md:1`; `pipelines/BENI/experiment/beni_pilot/README.md`; `README.md` quick start; `docs/ROADMAP.md:1`
  Acceptance criteria: `rg "input data|commands|random seed|output paths|validation|software versions" docs technical-reports`
  QA scenarios:
  - Happy: `python - <<'PY'` parses run manifest Markdown headings and asserts required sections exist; evidence `.omo/evidence/task-8-research-lab-structure-finetune.txt`.
  - Failure: run the parser against a temp incomplete manifest and assert nonzero; evidence `.omo/evidence/task-8-research-lab-structure-finetune-negative.txt`.
  Commit: Y | `docs(repro): add research run manifest standard` | `docs/research/` or `technical-reports/extensions/`, BENI example

- [x] 9. Add FAIR and dataset-card release checklist
  What to do / Must NOT do:
  Create `docs/DATA_RELEASE_CHECKLIST.md` and link it from dataset, dist, and contributor docs. The checklist must cover findability, accessibility, interoperability, reuse/license, dataset-card fields, provenance, limitations/biases, sensitive data, contributor credit, and DOI/platform metadata. Do not fabricate missing DOIs or platform links.
  Parallelization: Can parallel Y | Wave 2 | Blocks 11, 12, 13
  References: `dataset/BENI/DATASET_CARD.md`; `dataset/BENI/HUGGINGFACE.md`; `dist/README.md:21`; `docs/LINGUISTIC_CONTRIBUTION_GUIDE.md:111`
  Acceptance criteria: `rg "FAIR|Findability|Accessibility|Interoperability|Reuse|limitations|bias|license|DOI" docs/DATA_RELEASE_CHECKLIST.md dataset/README.md dist/README.md`
  QA scenarios:
  - Happy: `python - <<'PY'` checks checklist sections against FAIR and dataset-card required headings; evidence `.omo/evidence/task-9-research-lab-structure-finetune.txt`.
  - Failure: checker run against temp checklist missing license/bias sections must fail; evidence `.omo/evidence/task-9-research-lab-structure-finetune-negative.txt`.
  Commit: Y | `docs(data): add fair release checklist` | `docs/DATA_RELEASE_CHECKLIST.md`, `dataset/README.md`, `dist/README.md`, contributor docs

- [x] 10. Implement minimal CLI validation and status commands
  What to do / Must NOT do:
  Turn `cli/` from a stub into a minimal importable CLI, preferably using standard library `argparse` unless a project dependency is already justified. Implement `lila status` and `lila validate` around the contract and registry checks. Wire an optional project script entry in `pyproject.toml` only if packaging supports it cleanly.
  Parallelization: Can parallel Y | Wave 3 | Blocks 13
  References: `cli/README.md:1`; `registry/languages.json:1`; `registry/xeni_pipeline_contract.json`; `tests/test_xeni_pipeline_contract.py`; `tests/test_registry_consistency.py`
  Acceptance criteria: `python -m cli status && python -m cli validate && python -m pytest tests/test_cli.py -q`
  QA scenarios:
  - Happy: `python -m cli status | tee .omo/evidence/task-10-research-lab-structure-finetune-status.txt` prints all registry pipelines and statuses; `python -m cli validate | tee .omo/evidence/task-10-research-lab-structure-finetune-validate.txt` exits 0.
  - Failure: `python -m cli validate --registry /tmp/bad-languages.json` with a bad temp registry exits nonzero and prints the mismatch; evidence `.omo/evidence/task-10-research-lab-structure-finetune-negative.txt`.
  Commit: Y | `feat(cli): add pipeline status and validation commands` | `cli/`, `pyproject.toml`, `tests/test_cli.py`

- [x] 11. Formalize contributor credit, review, and ethics gates
  What to do / Must NOT do:
  Update contributor docs so language data, annotations, dialectal expertise, code, reviews, and papers have explicit review gates and authorship/acknowledgment thresholds. Add a checklist for data license consent, sensitive text handling, and native-speaker review. Do not change contributor credit policy silently; document any proposed threshold as lab policy.
  Parallelization: Can parallel Y | Wave 3 | Blocks 13
  References: `CONTRIBUTING.md:30`; `docs/COLLABORATION.md:195`; `docs/LINGUISTIC_CONTRIBUTION_GUIDE.md:56`; `technical-reports/contributions/OWNERS.csv`
  Acceptance criteria: `rg "authorship|acknowledg|ethics|license|native speaker|review gate|OWNERS.csv" CONTRIBUTING.md docs technical-reports`
  QA scenarios:
  - Happy: `python - <<'PY'` verifies docs mention each contribution type and a review/credit rule; evidence `.omo/evidence/task-11-research-lab-structure-finetune.txt`.
  - Failure: checker run against temp missing annotation-credit section fails; evidence `.omo/evidence/task-11-research-lab-structure-finetune-negative.txt`.
  Commit: Y | `docs(governance): formalize contributor review gates` | `CONTRIBUTING.md`, `docs/COLLABORATION.md`, `docs/LINGUISTIC_CONTRIBUTION_GUIDE.md`, `technical-reports/contributions/`

- [x] 12. Add repository hygiene audit without destructive cleanup
  What to do / Must NOT do:
  Add `infrastructure/scripts/audit_repo_hygiene.py` that reports tracked forbidden artifacts, ignored local noise counts, missing expected manifests, and secret-risk paths without deleting anything. Update `Makefile` with a read-only `audit` target. Do not remove local ignored files or secrets.
  Parallelization: Can parallel Y | Wave 3 | Blocks 13
  References: `.gitignore:8`; `.gitignore:42`; `.gitignore:105`; `.gitignore:109`; `.gitignore:117`; current local evidence: 55 pycache dirs and ignored `.env` exists
  Acceptance criteria: `make audit`
  QA scenarios:
  - Happy: `make audit | tee .omo/evidence/task-12-research-lab-structure-finetune.txt` exits 0 or documented warning status without deleting files.
  - Failure: run audit against a temp tracked-file list containing `.env`/`.pyc` and assert it reports a failure; evidence `.omo/evidence/task-12-research-lab-structure-finetune-negative.txt`.
  Commit: Y | `chore(repo): add read-only hygiene audit` | `infrastructure/scripts/audit_repo_hygiene.py`, `Makefile`, optional tests

- [x] 13. Final integration and documentation map
  What to do / Must NOT do:
  Add or update `docs/README.md` to make the lab navigation unambiguous: researchers, linguistic contributors, data releasers, infrastructure contributors, and maintainers each get a short path. Re-run all validation commands and record evidence. Do not introduce new broad scope.
  Parallelization: Can parallel N | Wave 4 | Blocks final verification
  References: `docs/README.md`; `README.md`; all new docs/tests from Todos 1-12
  Acceptance criteria: `make lint && make test && make audit && python -m cli validate`
  QA scenarios:
  - Happy: `make lint && make test && make audit && python -m cli validate | tee .omo/evidence/task-13-research-lab-structure-finetune.txt` exits 0.
  - Failure: `python - <<'PY'` verifies `docs/README.md` links to operating model, pipeline contract, data release checklist, contribution guide, and CLI validation docs; missing link fails; evidence `.omo/evidence/task-13-research-lab-structure-finetune-links.txt`.
  Commit: Y | `docs: add lab navigation and final verification map` | `docs/README.md`, `README.md`, final small doc fixes

## Final Verification Wave
> Runs in parallel where possible. ALL must APPROVE. Surface results and wait for the user's explicit okay before declaring implementation complete.
- [x] F1. Plan compliance audit: `python - <<'PY'` checks every todo evidence file exists, every planned acceptance command is represented, and all files touched are in the planned scope.
- [x] F2. Code quality review: `make lint`, `ruff format --check pipelines/shared/ pipelines/template/ infrastructure/ tests/ cli/`, and `python -m pytest -q`.
- [x] F3. Real manual QA: command-line surface `python -m cli status` and `python -m cli validate` driven through the actual CLI with stdout captured under `.omo/evidence/final-cli.txt`.
- [x] F4. Scope fidelity: `git diff --stat` and `git diff --name-only` checked against this plan; no ML model fine-tuning, API implementation, dashboard implementation, or destructive cleanup occurred.

## Commit Strategy
- Use one conventional commit per logical wave or per todo when changes are independent.
- Prefer these atomic commits:
  - `docs(repo): define lab operating model`
  - `test(pipelines): add xeni contract validation`
  - `ci: align lint scopes across local and github checks`
  - `ci(schemas): validate actual annotation schemas`
  - `docs(data): reconcile release metadata sources`
  - `docs(pipelines): clarify scaffold status for target languages`
  - `test(registry): prevent pipeline metadata drift`
  - `docs(repro): add research run manifest standard`
  - `docs(data): add fair release checklist`
  - `feat(cli): add pipeline status and validation commands`
  - `docs(governance): formalize contributor review gates`
  - `chore(repo): add read-only hygiene audit`
  - `docs: add lab navigation and final verification map`
- Do not commit automatically unless the user explicitly asks.
- If committing later, include footer: `Plan: .omo/plans/research-lab-structure-finetune.md`.

## Success Criteria
- The repo has a documented operating model and clear top-level source-of-truth boundaries.
- Every XENI pipeline has a status-aware validation contract.
- CI, Makefile, pyproject, and pre-commit enforce consistent quality boundaries.
- Actual annotation schema files are validated.
- Dataset release metadata is reconciled with registry and distribution docs.
- Reproducibility manifests and FAIR/data-card release checklists exist and are linked.
- Contributor credit, ethics, and review gates are explicit.
- CLI `status` and `validate` commands provide a self-service contributor surface.
- `make lint`, `make test`, `make audit`, and `python -m cli validate` pass, or any pre-existing unavoidable failure is documented with exact command output and reason.
