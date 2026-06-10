# Contributor Quickstart

Get from zero to your first pull request in about five minutes. For the full picture, see [CONTRIBUTING.md](../CONTRIBUTING.md) and [COLLABORATION.md](../COLLABORATION.md).

## 1. Pick your path

| Path | Best if you… | Start here |
|------|--------------|------------|
| **Linguistic** | Speak Bangla, Assamese, Nepali, or another low-resource language | [LINGUISTIC_CONTRIBUTION_GUIDE.md](../LINGUISTIC_CONTRIBUTION_GUIDE.md) |
| **Code** | Write Python, build pipelines, or fix bugs | [pipelines/template/README.md](../pipelines/template/README.md) |
| **Docs** | Improve guides, READMEs, or translations | [CONTRIBUTING.md](../CONTRIBUTING.md) |

No coding required for linguistic contributions — native-language expertise is the core skill.

## 2. Find an issue

Browse [open issues labeled `good first issue`](https://github.com/LilaLABx/LILA-LAB/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22). Good entry points:

- **Docs** — README translations, glossary, contributor guides
- **Linguistic** — annotation templates, dataset card translations
- **Code** — pipeline template improvements, small script fixes

Comment on the issue before you start so maintainers know you're working on it.

## 3. Make your first contribution

```bash
# Fork on GitHub, then:
git clone https://github.com/YOUR_USERNAME/LILA-LAB.git
cd LILA-LAB
git checkout -b my-first-contribution

# Do your work, then:
git add .
git commit -m "docs: describe what you changed"
git push origin my-first-contribution
```

Open a pull request on GitHub. Mention the issue number (e.g. `closes #27`). For linguistic data, add a row to [OWNERS.csv](../technical-reports/contributions/OWNERS.csv) with your name and task.

## 4. What happens next

- **Review** — Maintainers typically respond within a few days. Small PRs merge faster.
- **Credit** — Every merged contribution is recorded in `OWNERS.csv` and acknowledged in publications.
- **Community** — Join [Discord](https://discord.gg/TrrdKbky) for questions, or read [COMMUNITY.md](../communications/COMMUNITY.md).

Questions? Open a [GitHub issue](https://github.com/LilaLABx/LILA-LAB/issues/new) or ask in `#general` on Discord.