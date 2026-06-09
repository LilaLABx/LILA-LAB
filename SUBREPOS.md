# Integrating External Repositories via Git Submodules

> For contributors who want their research extension to remain in their own repository while being linked from this project.

---

## Why Use a Submodule?

- **You keep full control** of your repository, license, and contribution history
- **Your work stays discoverable** as part of this research collective
- **We cross-reference** each other's work — your extension is listed in our registry, we cite it in our papers
- **No merge conflicts** — your repo evolves independently

---

## How to Request Submodule Integration

### Step 1: Prepare Your Repository

Your repository should have:

```
your-extension/
├── README.md           ← Describe your extension, its research question, and findings
├── data/               ← Your data (or instructions to access it)
├── scripts/            ← Your code
├── manuscript/         ← Your paper draft (if applicable)
├── results/            ← Your outputs
└── CONTRIBUTORS.md     ← Who worked on this
```

Recommended structure mirrors `papers/extensions/EXTENSION_TEMPLATE.md`.

### Step 2: Open an Issue

In this repository, open an issue with:

- **Title**: `Extension request: [your extension name]`
- **Link**: URL of your repository
- **Description**: What your extension does, what language/domain, what it found
- **Status**: In development / Complete / Published

### Step 3: We Add the Submodule

```bash
# We run this on our end:
git submodule add https://github.com/your-username/your-extension.git papers/extensions/your-extension
git submodule update --init --recursive
```

Your repository is now linked as a submodule at `papers/extensions/your-extension/`.

### Step 4: We Update the Registry

Your extension gets a row in `papers/extensions/INDEX.md` with the submodule path, status, and lead contributor.

---

## Updating Your Extension

Your repository stays independent. When you push changes, collaborators can update the submodule reference:

```bash
git submodule update --remote papers/extensions/your-extension
```

We periodically sync active extensions.

---

## Removing a Submodule

If you want to unlink your repository, open an issue requesting removal. Your data and history remain in your repository — only the link is removed from this project.

---

## Complete Example: Submodule-Based Language Extension

### Your Repo: `github.com/your-username/assamese-narrative-index`

```bash
assamese-narrative-index/
├── README.md
├── data/
│   ├── corpus/            # 10,000 Assamese news articles
│   └── annotations/       # 1,000 human-annotated articles
├── scripts/
│   ├── adapt_pipeline.py  # BENI pipeline adapted for Assamese
│   └── run_index.py       # Build and validate the index
├── results/
│   ├── narrative_index.csv
│   └── validation_report.md
└── manuscript/
    └── paper_draft.md
```

### Linked from this repo as:

`papers/extensions/assamese-narrative-index` → `github.com/your-username/assamese-narrative-index`

### Registered in `papers/extensions/INDEX.md`:

```markdown
| asm-001 | Assamese Narrative Index | Language Extension | Your Name | published | 2026-07-15 |
```

---

## FAQ

**Q: Can I have private repo and still be linked?**
A: Yes, but the submodule link will only work for collaborators with access. We recommend public repos for academic credit.

**Q: Do I need to match your license?**
A: No. Your repo can have its own license. We will note it in the registry.

**Q: What if both our repos have the same files?**
A: Submodules avoid duplication — your files live only in your repo. We reference them.

**Q: Can I be in the registry without a submodule?**
A: Yes — open an issue with your repository URL and we will list it as an external reference instead of a submodule.
