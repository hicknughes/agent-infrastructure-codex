---
name: plan-append
description: "Concurrent-safe append to docs/plan.md. Use when logging decisions, recording phenomena, updating status, or any write to plan.md during multi-session work. Triggers on: 'log this decision', 'add to the plan', 'record this phenomenon', 'update plan.md', 'append to plan', or when a phenomenon closes and needs recording."
---

# /plan-append

Append entries to `docs/plan.md` without clobbering concurrent agents.

## Procedure

1. Re-read `docs/plan.md` fresh. Never use a cached version.
2. Compute the current content hash:
   ```bash
   shasum -a 256 docs/plan.md | awk '{print $1}'
   ```
3. Compare against the hash from your last read of this file in this session.
   - **Match:** proceed to step 4.
   - **Mismatch:** STOP. Show the user what changed since your last read. Do NOT merge. Ask for direction. Exit.
4. Append the new entry using the appropriate format below.
5. Recompute and store the new hash for future comparisons.

## Entry Formats

### Phenomenon

Append a row to the Phenomena table:

```
| P<next-number> | <title> | pending | [YYYY-MM-DD HH:MM | agent-<short-id>] |
```

### Decision

Append under the Decisions section:

```
### P<N> — <title> [YYYY-MM-DD HH:MM | agent-<short-id>]

<what shipped, rationale, tradeoffs, residual items>
```

### Status Change

Append a comment noting the transition, then update the cell:

```
<!-- Status: P<N> pending -> decided [YYYY-MM-DD HH:MM | agent-<short-id>] -->
```

## Rules

- Never delete another agent's entries. Mark superseded if needed; preserve history.
- Always stamp with `[YYYY-MM-DD HH:MM | agent-<short-id>]`.
- Valid statuses: `pending` | `in-progress` | `decided` | `done` | `blocked` | `dispatched`.
- If `docs/plan.md` does not exist, create it with standard sections: Roadmap, Phenomena table, Decisions, Open Questions.
- One append per invocation. Do not batch unrelated entries.

## Conflict Detection

On hash mismatch:

1. Diff current file against your last-known content.
2. Tell the user: "plan.md was edited by another session since my last read."
3. Show the relevant diff.
4. Wait for direction. Do not attempt a merge.
