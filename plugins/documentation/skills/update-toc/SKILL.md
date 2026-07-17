---
name: update-toc
description: "Re-scan and update docs/TOC.md NOW. New docs get appended. Deleted docs get flagged. Hand-edited entries are never overwritten."
---

# /update-toc

Trigger: "update toc", "refresh the doc index", "sync toc", or after any significant doc changes

## Procedure

1. Read `docs/TOC.md`. If it doesn't exist, tell the user to run `/init-toc` first and stop.

2. Parse the existing Document Registry table entries into a set of known paths.

3. Scan the repo for doc files:
   - `docs/*.md`
   - `documentation/modules/*.md`
   - `README.md`
   - `docs/adr/*.md`
   - `docs/handoffs/*.md`

4. Identify **new files** — present on disk but not in the TOC. Append them to the Document Registry table.

5. Identify **missing files** — listed in the TOC but no longer on disk. Do NOT remove them. Instead, add a `[MISSING]` flag next to the entry.

6. Show the user the diff (additions and flags) before writing.

7. Wait for user confirmation. Then write the updated `docs/TOC.md`.
