---
name: review-implementation
description: Independently close a completed task by mapping every user requirement to current-state evidence, then reviewing code for incomplete wiring, duplicate responsibilities, regressions, missed consumers, weak tests, and unnecessary complexity. Use after implementation and initial tests, before reporting completion, or when the user suspects half-wired or bloated work.
---

# Review Implementation

Act as the request-to-evidence closure gate. Prefer an independent subagent that did not write the implementation. Do not trust the parent agent's completion claims or candidate summaries; inspect current state.

## Phase A: requirement closure

1. Read the complete user request and material follow-up instructions. Include operational actions, documentation, configuration, Git/GitHub actions, and explicit non-goals—not only code changes.
2. Convert the request and approved plan into a numbered checklist. Mark user-approved scope changes explicitly.
3. Reconstruct the action trace from commands, tool results, files, and external state. Flag failed, skipped, deferred, or claimed-but-unverified actions.
4. Build an evidence matrix mapping every checklist item to current evidence: file and line, command and outcome, test, generated artifact, or verified external state.
5. Treat missing, stale, proxy-only, or contradictory evidence as unresolved. Passing tests do not prove a requirement they do not exercise.

## Phase B: implementation completeness

1. Read applicable `AGENTS.md`, the plan, the implementation diff, and surrounding ownership boundaries.
2. Trace changed behavior end to end from entry point through consumers and side effects.
3. Search for every existing implementation of the same responsibility, including similar names, registrations, adapters, handlers, and configuration paths.
4. Check all consumers, exports, dependency injection, routes, schemas, migrations, feature flags, environment variables, documentation, and operational steps that may require updates.
5. Run focused tests or probes for suspected gaps. Do not rely only on visual review when execution is practical.
6. Evaluate whether new abstractions remove complexity and duplicate ownership or merely add another path.

## Verdict

Report only evidence-backed findings, ordered by severity, with file references and a concrete failure scenario. Use this structure:

```text
## Requirement Checklist
## Evidence Matrix
## Action Trace
## Implementation Findings
## Verification
VERDICT: PASS | VERDICT: FAIL
```

Return `VERDICT: PASS` only when every required item is verified or explicitly removed from scope by the user, required validation succeeds, and no material implementation finding remains. Return `VERDICT: FAIL` for any unresolved requirement, contradictory evidence, incomplete wiring, material regression, or required check that did not run.

When the verdict fails, identify the smallest concrete fixes and checks needed. After fixes, rerun affected tests and the closure gate. A clean result is valid; do not invent objections.
