---
name: plan-init
description: Scaffold docs/plan.md for multi-session phenomena tracking. Use when starting a non-trivial project, or when asked to "create a plan", "init plan", "start tracking phenomena", or "set up plan.md".
---

# plan-init

Scaffold a new `docs/plan.md` with the four-section master-plan skeleton.

## Procedure

1. Check if `docs/plan.md` already exists. If it does, STOP. Warn the user and suggest `/plan-append` instead. Do not overwrite.
2. Ask the user for:
   - A 1-3 sentence roadmap describing the arc of work.
   - Initial guiding objectives (or offer sensible defaults based on context).
3. Ask for the project name (or infer from the repo/directory).
4. Write `docs/plan.md` with this exact skeleton, filling in user-provided values:

```markdown
# <Project Name> — Master Plan

## Roadmap
<user-provided 1-3 sentences>

## Guiding Objectives
- <user-provided or defaults>

## Phenomena

| # | Title | Status | Owner |
|---|-------|--------|-------|

<!-- Status vocabulary: pending | in-progress | decided | done | blocked | dispatched -->
<!-- dispatched = subagent owns it; in-progress = you own it -->

## Decisions

<!-- Format: ### P<N> — Title [YYYY-MM-DD | agent-tag] -->
<!-- Body: what shipped, rationale, tradeoffs accepted, residual open items -->
```

5. Confirm creation to the user. Surface the next step: add the first phenomenon.

## Rules

- Never overwrite an existing `docs/plan.md`.
- Keep the roadmap to 1-3 sentences. Push back if the user writes a wall of text.
- Guiding objectives are bullet points — short, opinionated, directional.
- The phenomena table starts empty. Rows are added via `/plan-append` or inline editing.
- Agent tags use format `agent-<date>-<purpose>` e.g. `agent-2026-05-01-cto`.
- Status vocabulary: pending | in-progress | decided | done | blocked | dispatched.
- "dispatched" means a subagent owns it; "in-progress" means you own it.
