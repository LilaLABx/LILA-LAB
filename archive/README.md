# Archive — Moved Loose Files

> These files were cluttering the project root. They are retained for reference but have no active role in the current research program.

---

## Contents

| File | Original Location | Why Archived |
|------|-------------------|--------------|
| `BENI_v1_data_paper_osf_dataset_upload.zip` | Root (1.1 GB) | OSF upload zip — superseded by `data-paper/osf_upload_package/` |
| `beni-3-llm-ensemble.log` | Root | Log from a 3-LLM ensemble run — retained for reference |
| `beni-3-llm-ensemble-t4.log` | Root | Log from T4-accelerated ensemble run — retained for reference |
| `hello.txt` | Root | Scratch file |
| `test1.txt` | Root | Scratch file |
| `texput.log` | Root | Orphaned LaTeX build log |

---

## Dependencies

These files have **zero active dependencies**. No script or configuration references them.

They are kept here rather than deleted in case the ensemble logs contain useful runtime metrics (API latency, cost per article, failure rates) that could inform future LLM annotation runs.

---

## For Research Agents

- If you need LLM annotation runtime metrics, check `beni-3-llm-ensemble*.log` for timing and cost data.
- The 1.1 GB OSF zip is superseded by the structured release in `data-paper/osf_upload_package/`.
- These files are **not** git-tracked (they're in .gitignore).
