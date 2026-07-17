---
name: init-compliance-matrix
description: Scaffold the compliance matrix — a standing dashboard tracking per-rule status across scopes. Use when a project needs governance rules tracked persistently across plans.
---

# /init-compliance-matrix

You scaffold the compliance matrix — a standing dashboard tracking per-rule status across scopes. This is not the plan; plans close. The matrix persists.

Trigger: "create compliance matrix", "init compliance matrix", "set up the compliance dashboard"

## Steps

1. Scan existing policy docs (default: `docs/policy/*.md`) for rule IDs matching `[A-Z]+-\d+`.
2. Ask for scopes — the functional areas of the project (e.g. "frontend", "backend", "infra").
3. Generate the matrix with all rules × all scopes, defaulting every cell to `unchecked`.
4. Write to `docs/policy/compliance-matrix.md`.

## Output format

```markdown
# Compliance Matrix

| Rule | Scope: <scope1> | Scope: <scope2> | Scope: <scope3> |
|------|-----------------|-----------------|-----------------|
| BP-1 | unchecked       | unchecked       | unchecked       |
| BP-2 | unchecked       | unchecked       | unchecked       |
```

## Valid cell values

- `unchecked` — not yet assessed
- `verified` — passes the rule's Verification criterion
- `partial` — some compliance, gaps remain
- `failing` — known non-compliance
- `n/a` — rule does not apply to this scope

## Constraints

- Every rule ID from every policy doc must appear. Run `matrix-lint.py` after generation to confirm.
- Distinguish from plan.md: plan.md = active decisions; compliance-matrix = standing dashboard that survives plans closing.
