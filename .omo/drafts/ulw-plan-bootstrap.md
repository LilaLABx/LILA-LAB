# ulw-plan Bootstrap

## Request
- User invoked `$ulw-plan` without a concrete task objective.
- Planner role only: read/search/run read-only analysis and write planning artifacts under `.omo/`.

## Skills
- `omo:ulw-plan`: required because the user explicitly invoked `$ulw-plan`; use the explore-first planning workflow and wait for approval before writing a final plan.

## Tier
- LIGHT bootstrap: no product code change requested yet; current work is only establishing the planning objective.

## Repository Facts
- No `AGENTS.md` found under `/mnt/data/Projects/nabilox` or `/mnt/data/Projects`.
- Project is `lila-lab`, a Python 3.10+ low-resource NLP pipeline repository.
- Key surfaces:
  - `pyproject.toml`: package metadata, optional dependencies, Ruff, pytest config.
  - `Makefile`: `make lint`, `make format`, `make test`, install tasks.
  - `pipelines/shared/`: shared Python pipeline library.
  - `pipelines/template/`: template XENI pipeline implementation and tests.
  - `pipelines/BENI/`: advisory-linted production pilot pipeline.
  - `.omo/plans/`: existing plans for BENI, dataset exploration, dashboard work.
- Worktree status was clean at bootstrap.

## Current Unknowns
- Core objective is missing. A decision-complete plan cannot be generated until the user names the desired feature, bugfix, refactor, research plan, or plan artifact.
- Scope boundaries, test strategy, and approval brief are blocked on the objective.

## Default Assumptions If User Skips Details
- Plan target should be the current `/mnt/data/Projects/nabilox` repository.
- Test strategy default: TDD for behavior changes; characterization-first for refactors; no new tests for documentation-only work.
- QA default: agent-executed command-level evidence for CLI/data work, browser/computer-use evidence only for browser or GUI surfaces.

## Next Question
Ask the user for the planning objective, with a default that the plan should target this repository and produce one `.omo/plans/<slug>.md` after approval.
