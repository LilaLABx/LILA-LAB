from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Final

REPO_ROOT: Final = Path(__file__).resolve().parents[2]
FORBIDDEN_TRACKED_SUFFIXES: Final = (".pyc", ".pdf", ".zip")
FORBIDDEN_TRACKED_NAMES: Final = (".env", ".env.local")


@dataclass(frozen=True, slots=True)
class AuditResult:
    tracked_forbidden: tuple[str, ...]
    pycache_count: int
    local_env_count: int
    missing_manifest_dirs: tuple[str, ...]


def _git_ls_files(repo_root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=repo_root,
        check=True,
        text=True,
        capture_output=True,
    )
    return [line for line in result.stdout.splitlines() if line]


def audit(repo_root: Path = REPO_ROOT) -> AuditResult:
    tracked = _git_ls_files(repo_root)
    forbidden = []
    for path in tracked:
        name = Path(path).name
        if name in FORBIDDEN_TRACKED_NAMES or path.endswith(FORBIDDEN_TRACKED_SUFFIXES):
            forbidden.append(path)
    pycache_count = sum(1 for _ in repo_root.glob("**/__pycache__"))
    local_env_count = sum(1 for path in repo_root.glob("**/.env") if ".git" not in path.parts)
    missing_manifest_dirs = []
    if not (repo_root / "dist" / "manifests" / "BENI").exists():
        missing_manifest_dirs.append("dist/manifests/BENI")
    return AuditResult(
        tracked_forbidden=tuple(forbidden),
        pycache_count=pycache_count,
        local_env_count=local_env_count,
        missing_manifest_dirs=tuple(missing_manifest_dirs),
    )


def main() -> int:
    result = audit()
    print("Repository hygiene audit")
    print(f"Tracked forbidden artifacts: {len(result.tracked_forbidden)}")
    for path in result.tracked_forbidden:
        print(f"ERROR tracked forbidden: {path}")
    print(f"Ignored/local __pycache__ directories: {result.pycache_count}")
    print(f"Ignored/local .env files: {result.local_env_count}")
    for path in result.missing_manifest_dirs:
        print(f"WARN missing manifest directory: {path}")
    return 1 if result.tracked_forbidden else 0


if __name__ == "__main__":
    raise SystemExit(main())
