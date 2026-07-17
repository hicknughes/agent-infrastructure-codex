---
name: handoff
description: "Write a cross-session handoff brief NOW. Cold-start context for the next agent session — structured, complete, no ambiguity."
---

# /handoff

Trigger: "create a handoff", "write a brief for another session", "hand this off", "prepare a cold-start brief"

## Procedure

1. Ask the user for a **topic** (used in the filename, e.g. "pipeline-refactor").

2. Collect content for each section. Accept free-form input and structure it, or prompt section-by-section:
   - **Status + date** — current state in one line
   - **Goal** — one-paragraph desired outcome
   - **Context** — what's shipped, what state things are in
   - **What needs to ship** — numbered deliverables
   - **Out of scope** — explicit fences
   - **Hard rules / invariants** — things the next session must not violate
   - **Key files to read first** — ordered list of paths
   - **Process** — plan-first, verify-commands, etc.
   - **Pilot batch suggestion** — a safe first move to validate understanding

3. Write to `docs/handoffs/YYYY-MM-DD-<topic>.md` using today's date.

4. Create the `docs/handoffs/` directory if it doesn't exist.

5. Write the file with this template:

```markdown
# Handoff: <Topic>

**Status:** <status> | **Date:** <YYYY-MM-DD>

## Goal
<one paragraph>

## Context
<what's shipped, current state>

## What Needs to Ship
1. <deliverable>
2. <deliverable>

## Out of Scope
- <fence>

## Hard Rules / Invariants
- <rule>

## Key Files to Read First
1. <path>
2. <path>

## Process
<how to approach the work>

## Pilot Batch
<safe first move to validate understanding>
```

6. Confirm creation and print the file path.
