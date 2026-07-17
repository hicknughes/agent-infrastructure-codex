---
name: concept-audit
description: Grep for all implementations of a named concept and flag drift across the codebase. Use when the same logical concept appears in multiple files and may be diverging.
---

# /concept-audit

You grep for all implementations of a named concept and flag drift. When the same idea lives in multiple places, bugs hide in the gaps between them.

Trigger: "audit concept", "check for concept drift", "how many implementations of X exist"

## Steps

1. Take a concept name (e.g. "eligibility", "claim status", "vendor tier").
2. Grep the codebase for all implementations — look for:
   - Function/method names containing the concept
   - Type/interface definitions
   - Constants/enums
   - Comments referencing the concept
3. Group results by location and summarize each implementation's behavior.
4. If multiple implementations exist, flag potential drift:
   - Do they agree on edge cases?
   - Do they share a single source of truth or are they independent?
5. Recommend consolidation into a canonical helper if drift is found.

## Output format

```
Concept: <name>
Implementations found: <count>

1. <file>:<line> — <brief description of what it does>
2. <file>:<line> — <brief description of what it does>

Drift detected: <yes/no>
  - <specific inconsistency if yes>

Recommendation: <consolidate into X / no action needed>
```

## Constraints

- Search broadly: include tests, scripts, config files — not just src/.
- Flag even minor differences (e.g. one implementation trims whitespace, another doesn't).
- If no drift found, say so clearly — don't manufacture concerns.
