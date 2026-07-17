---
name: init-toc
description: "Scaffold docs/TOC.md NOW. The TOC is the boundary index — the first file any agent reads. If the repo lacks one, build it immediately."
---

# /init-toc

Trigger: "create a TOC", "init toc", "set up the doc index", "where should I look for docs"

## Procedure

1. Check if `docs/TOC.md` exists. If yes, warn the user and offer to append rather than overwrite. Wait for confirmation before proceeding.

2. Scan the repo for documentation files:
   - `docs/*.md`
   - `documentation/modules/*.md`
   - `README.md`
   - `docs/adr/*.md`
   - `docs/handoffs/*.md`

3. Generate `docs/TOC.md` with this structure:

```markdown
# Table of Contents — Boundary Index

This is the entry point. Read this first.

## Four-Tier Doc Map

| Tier | Location | Answers |
|------|----------|---------|
| Run | README.md | "How do I run this?" |
| Decisions | docs/adr/ | "Why is this built this way?" |
| Modules | documentation/modules/*.md | "How does module X work?" |
| Plan | docs/plan.md | "What's being decided right now?" |
| Index | docs/TOC.md | "Where do I look?" (this file) |

## Document Registry

| Document | Module/Initiative | Purpose |
|----------|-------------------|---------|
| (scanned entries here) | | |
```

4. Populate the Document Registry table with every file found in step 2. Infer Module/Initiative from the parent directory or filename. Extract purpose from the first H1 or first paragraph.

5. Write the file. Confirm to the user.
