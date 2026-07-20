---
name: deliver
description: Run an evidence-first coding workflow from investigation through verified implementation. Use for feature work, bug fixes, refactors, migrations, or any request to build or change code. Selects a lightweight path for bounded work and a full red-teamed path for large, ambiguous, risky, cross-cutting, auth, schema, migration, or data-sensitive work. Trigger on "deliver this", "build this carefully", "use the full workflow", "lightweight workflow", or equivalent implementation requests.
---

# Deliver

Own the task through verified completion. Do not stop after analysis unless the user asked only for analysis.

## Select the path

When repository state is relevant, resolve `../../scripts/repo_preflight.py` relative to this `SKILL.md` and pass the target repository root explicitly; do not change the working directory to the installed skill directory.

Use **lightweight** when the change is well-bounded, low-risk, and has clear local verification. Use **full** when any of these apply:

- Architecture, authentication, authorization, schema, migration, production data, or external side effects
- Ambiguous cause or requirements
- Cross-cutting changes or multiple consumers
- High regression cost
- The user explicitly requests full workflow or red-teaming

Risk overrides size. Tell the user briefly when escalating to full. Respect an explicit user request for either path unless doing so would be unsafe.

## Route to gstack deliberately

This skill remains the default owner of end-to-end coding delivery. Use installed gstack skills as explicit specialists rather than allowing overlapping workflows to trigger implicitly:

- Use gstack's global `investigate` skill for a reported bug or unclear runtime failure that needs systematic root-cause debugging.
- Use gstack's global `plan-eng-review` skill when a full plan needs an additional architecture, data-flow, edge-case, or test review.
- Use gstack's global `review` skill as an additional pre-landing review for material or high-risk implementations.
- Use gstack's global `qa` skill for live web-application testing and fixes only when the user has approved its commit-producing workflow; use global `qa-only` for report-only testing.
- Use gstack's global `ship` skill only on explicit user request because it can commit, push, and open a pull request.

Keep the custom `review-implementation` check authoritative for request-to-evidence closure, incomplete wiring, duplicate responsibilities, missing consumers, and unnecessary abstraction. Keep custom documentation and policy skills authoritative for their repository artifacts.

## Lightweight path

1. Investigate enough to reproduce or verify the relevant behavior. Execute practical checks; do not rely only on reading.
2. State a brief plan and material assumptions. Validate assumptions that can change the approach.
3. Implement narrowly. Search for existing responsibilities before adding new helpers or abstractions.
4. Run targeted tests, then broader checks appropriate to the repository.
5. Perform a distinct request-to-evidence closure review using `review-implementation`: every user requirement, action trace, wiring, consumers, duplicates, regressions, tests, and docs.
6. Require `VERDICT: PASS`. Fix material findings and re-run affected verification and closure review, with at most three review/fix cycles.
7. If the gate still fails, report incomplete work rather than claiming completion. Otherwise report files changed, commands and outcomes, unresolved limitations, and why the work is complete.

## Full path

1. Use custom `engineering-workflow:investigate` for general execution-first evidence gathering, or gstack's global `investigate` for systematic bug root-cause analysis. Delegate independent read-heavy or experimental questions to subagents when useful.
2. Produce an explicit plan with scope, consumers, risks, verification, and definition of done. Add gstack's global `plan-eng-review` when architecture or integration risk justifies another specialist pass.
3. Use `red-team` to challenge the diagnosis and plan with independent subagents. Revise the plan from evidence.
4. Implement the revised plan. Prefer a focused worker subagent for isolated implementation; keep architecture and integration decisions in the main task.
5. Run targeted and repository-level verification.
6. Use custom `engineering-workflow:review-implementation` with an independent reviewer after initial tests pass. Require a request-to-evidence matrix and `VERDICT: PASS`. Add gstack's global `review` for material or high-risk pre-landing review.
7. Fix material findings, re-test targeted paths, repeat broader verification, and rerun the closure gate, with at most three review/fix cycles.
8. If the gate still fails, report incomplete work. Otherwise report evidence, changes, review findings addressed, and anything not verified.

## Gates

- Do not plan from an untested material assumption when practical verification exists.
- Do not add a function, service, adapter, or configuration path before searching for an existing owner of that responsibility.
- Do not call work complete when registration, consumers, migrations, tests, documentation, or configuration remain unwired.
- Red-team output is input to the plan or implementation, not a raw debate to hand to the user.
- Completion requires a `review-implementation` verdict of `PASS`; test success alone is insufficient.
- If a required check cannot run, state exactly why and what remains uncertain.

Read `references/workflow-gates.md` when deciding whether evidence is sufficient or a phase may close.
