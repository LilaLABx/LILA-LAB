# Research Lab Structure Fine-Tuning Draft

## Request
- User objective: "i want make this an top notch research lab for liguistic exploration for low resource language. eval the repo and make plan for finetuning existing structure"
- Interpretation: evaluate the current repository as a research-lab platform and prepare one decision-complete plan to refine the existing structure, not replace the lab concept.

## Skills
- `omo:ulw-plan`: required because the user explicitly asked to evaluate and make a plan; planner scope only until approval.

## Tier
- HEAVY / Architecture: touches repository structure, research governance, reproducibility, CI, data-release conventions, contribution flows, and multiple top-level domains.
- Subagent note: `multi_agent_v1.spawn_agent` became available only after tool discovery, but its tool contract says to use subagents only if the user explicitly asks for delegation/parallel agent work. The user did not authorize delegation, so exploration was performed locally.

## Current Repository Evaluation

### Strengths
- Clear lab-level mission and public narrative in `README.md`: LILA Lab is positioned as open-source NLP infrastructure for low-resource languages, with BENI as the first proven pipeline and 10 target languages by H1 2027.
- XENI conceptual model is documented in `pipelines/README.md`: language pipelines can produce multiple domain indices; BENI is the reference language pipeline, not just an economic index.
- Collaboration model exists in `docs/COLLABORATION.md`: language extensions, cross-domain extensions, methods, replication, citizen annotation, policy, infrastructure, and teaching are all framed as publishable contributions.
- Linguistic contributor path exists in `docs/LINGUISTIC_CONTRIBUTION_GUIDE.md`: text corpus, annotations, and dialectal expertise have contributor-facing instructions.
- Registry foundation exists in `registry/languages.json` and `registry/schemas.json`.
- Dataset and distribution docs exist for BENI, including dataset cards and platform manifests.
- Basic pytest coverage exists and passes: `python -m pytest -q` collected 4 tests in `pipelines/template/tests/test_structure.py` and passed.

### Structural Gaps
- The repository still reads like a fast-growing multi-purpose monorepo: production pipeline code, paper drafts, data release artifacts, communications strategy, bot infrastructure, website, personal research material, and planning artifacts are all visible at once.
- `api/README.md` and `cli/README.md` are planning stubs, not implementations. They describe important future self-service surfaces but cannot yet validate or scaffold language pipelines.
- Existing `.omo/plans/*.md` are useful conceptual plans but do not satisfy current decision-complete plan requirements: most lack dependency matrices, concrete QA invocations, evidence paths, and per-todo acceptance criteria.
- `docs/archive/RESTRUCTURE_PLAN.md` says the broad reorganization is mostly done, but it is older and does not cover current problems: uppercase pipeline directories, registry drift, CI mismatch, or reproducibility gates.

### Pipeline / Template Gaps
- Target language directories `AENI`, `NENI`, `SENI`, `CENI`, `HENI`, `KIENI`, `VIENI`, `TIENI`, and `IDENI` are almost exact template copies. `diff -qr pipelines/template pipelines/<PIPELINE>` shows only README/config differences plus missing template Dockerfile/Makefile/tests.
- `pipelines/template/README.md` still instructs manual copy/rename steps and does not define a machine-checkable pipeline contract beyond a small structure test.
- `pipelines/README.md` describes shared utility subdirectories like `shared/annotation`, `shared/classifiers`, and `shared/utils`, but the actual `pipelines/shared/` layout is mostly flat modules plus `analysis`, `llm`, `stats`, and `data`.
- `registry/languages.json` marks all target pipelines as framework-ready but not actually explored (`sample/profile/vocabulary/temporal/schema/report` all `not_run`), including BENI.

### Quality / CI Gaps
- `pyproject.toml` excludes `pipelines/BENI/**` and `personal/` from normal Ruff, but `.github/workflows/ci.yml` runs `ruff check pipelines/` and `ruff format --check pipelines/` across the full pipeline tree.
- `make lint` currently fails on scoped lint target `pipelines/shared/ pipelines/template/ infrastructure/ tests/`; observed issues include import ordering, unused imports, bugbear findings in schema validation lambdas, and Discord bot style issues.
- `ruff check pipelines/` currently fails with 54 errors across bootstrapped target pipelines and shared/template code.
- `python -m pytest -q` passes but only validates the template directory shape and JSON object parsing, so test evidence is too narrow for a top-tier research-lab platform.
- CI schema validation searches `**/schemas/*.schema.json`, but actual schema files are named `economic.json` and `health.json`, so schema validation can silently skip the current schemas.

### Data / Reproducibility / Repository Hygiene Gaps
- `.gitignore` excludes data artifacts, pycache, PDFs, zips, `personal/`, and `infrastructure/discord-bot/`; current `git ls-files` shows no tracked pycache or PDFs/zips except `communications/assets/posters/1.xcf`.
- Working tree has many ignored/generated artifacts locally, including 55 `__pycache__` directories and local data/PDF/zip artifacts. These are not tracked but make the workspace noisy.
- `infrastructure/discord-bot/.env` exists locally but is ignored and not tracked. Plan should preserve it and avoid destructive cleanup.
- `dist/README.md` describes `dist/manifests/`, but current tracked files under `dist/` only show `dist/README.md`; manifest availability needs reconciliation before claiming platform maturity.
- `technical-reports/README.md` says paper 2 lives under `dataset/BENI/beni-v1/`, while a `technical-reports/paper2_beni_dataset/README.md` placeholder also exists.

## External Standards Anchors
- FAIR data principles: make research outputs findable, accessible, interoperable, and reusable; the original FAIR paper explicitly applies the principles to data plus the algorithms, tools, and workflows that produce it.
- The Turing Way reproducibility guidance defines reproducibility in data research as making data and code available to fully rerun the analysis.
- Hugging Face dataset cards are a useful publishing norm for documenting dataset contents, creation context, responsible use, and limitations.

## Proposed Planning Direction
Plan a staged "lab maturity and structure fine-tuning" program rather than a wholesale restructure:
1. Establish repo governance and source-of-truth boundaries: what belongs in `pipelines/`, `dataset/`, `technical-reports/`, `registry/`, `dist/`, `docs/`, `infrastructure/`, and what should stay ignored/private.
2. Define a machine-checkable XENI pipeline contract: required directories, schemas, configs, data cards, exploration outputs, validation outputs, and registry records.
3. Convert target language directories from passive template copies into status-aware scaffold entries: keep only meaningful per-language metadata until data/owners exist, or add validation tests that mark them as bootstrapped-not-operational.
4. Align CI, Makefile, pyproject, and pre-commit so local and GitHub checks enforce the same intended scope.
5. Add reproducibility rails: run manifests, dataset cards, deterministic sample data, command recipes, evidence directories, and replication templates.
6. Formalize research governance: contribution ownership, authorship thresholds, review/adjudication protocols, ethics/data-license checks, release checklists.
7. Prioritize self-service tooling: CLI validation/status first, API later, dashboard only after validated outputs exist.

## Assumptions To Confirm
- "finetuning existing structure" means refine the existing monorepo structure and workflow, not fine-tune an ML model.
- Plan should focus on repository architecture and lab-operating system maturity, not writing research manuscripts or launching a web redesign.
- Default test strategy: TDD/characterization for behavior changes in tooling and CI; tests-after for documentation-only changes; every todo still gets agent-executed QA.
- The final plan should be written after approval to `.omo/plans/research-lab-structure-finetune.md`.

## Verification Evidence Captured
- `python -m pytest -q`: PASS, 4 tests passed.
- `ruff check pipelines/shared/ pipelines/template/ infrastructure/ tests/`: FAIL, scoped local lint target currently has errors.
- `ruff check pipelines/`: FAIL, CI-like pipeline lint target currently has 54 errors.
- `diff -qr pipelines/template pipelines/<target>` for all nine target pipelines: each differs by 6 entries, mostly README/config and missing template-only files/tests.
- `git status --short`: only `.omo/drafts/` is untracked during planning.

## Approval Gate Questions
1. Scope: approve a repo-architecture/lab-operations plan, or include actual ML model fine-tuning work too?
2. Depth: approve a comprehensive plan that touches docs, CI, registry, template, CLI validation, dataset/release governance, and cleanup, or a smaller docs/structure-only plan?
3. Test strategy: approve TDD/characterization for executable tooling and tests-after for docs-only work?

## Approval
- User approved "lab maturity and structure fine-tuning".
- Resolved decisions:
  - Scope is repository architecture and lab operations, not ML model fine-tuning.
  - Depth is comprehensive across docs, CI, registry, template, CLI validation, dataset/release governance, and cleanup.
  - Test strategy remains TDD/characterization for executable tooling and tests-after for docs-only changes.
- Final plan path: `.omo/plans/research-lab-structure-finetune.md`.
