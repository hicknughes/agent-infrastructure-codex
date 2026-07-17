---
name: init-policy
description: Scaffold policy documents with stable IDs. Use when starting a new policy or governance rule set that needs durable identifiers across documents.
---

# /init-policy

You scaffold policy docs with stable IDs. When someone needs governance rules tracked, you're the starting point.

Trigger: "create a policy doc", "init policy", "set up policy rules", "add compliance rules"

## Steps

1. Ask for the policy doc name and location (default: `docs/policy/<name>.md`).
2. Ask for the first 1–3 rules to include.
3. For each rule, scaffold the four-field template:

```
### <ID> — <short title>

- **Rule:** What the policy says.
- **Why:** The reason behind it.
- **Scope:** Which functional units it applies to.
- **Verification:** The concrete observable that proves compliance (must be mechanically checkable).
```

4. Assign stable IDs using the pattern `<PREFIX>-<number>` (e.g. BP-1, BP-2). These IDs never change meaning once assigned.
5. Write the file with a top-level heading matching the policy name.

## Output format

A markdown file at the chosen path containing all rules in the four-field template, each under a heading with its stable ID.

## Constraints

- IDs are permanent — never reassign or reuse a retired ID.
- Every rule must have all four fields filled. Push back if Verification is vague.
- Prefix defaults to first letters of the policy name (e.g. "Build Process" → BP). Ask to confirm.
