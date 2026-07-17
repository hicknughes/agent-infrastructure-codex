---
name: doc-consistency-audit
description: "Audit a doc file against the codebase NOW. Find drift — where docs promise things the code doesn't deliver."
---

# /doc-consistency-audit

Trigger: "audit this doc", "check doc consistency", "does the code match the docs", "doc drift check"

## Procedure

1. Accept a doc file path as input. If not provided, ask for one.

2. Read the doc file. Extract testable claims:
   - Feature descriptions ("users can X", "the system does Y")
   - UI element references (button names, page titles, form fields)
   - API endpoints mentioned (routes, methods)
   - Configuration keys or environment variables referenced
   - CLI commands documented

3. For each claim, grep the codebase for matching implementations:
   - Feature names → search for related function/class names
   - UI elements → search component files for matching text
   - API endpoints → search route definitions
   - Config keys → search .env files and config modules
   - CLI commands → search entry points and arg parsers

4. Classify each claim:
   - **Confirmed** — matching code found (include file:line reference)
   - **Unconfirmed** — no matching code found (potential drift)
   - **Ambiguous** — partial match, needs human review

5. Report results in a table:

```
| Claim | Status | Evidence |
|-------|--------|----------|
| "Users can reset password" | Confirmed | src/auth/reset.py:42 |
| "Dark mode toggle" | Unconfirmed | No match in components/ |
```

6. Flag high-risk drift (unconfirmed claims about user-facing features).
