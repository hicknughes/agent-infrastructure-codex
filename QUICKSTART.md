# Codex Infrastructure Quickstart

## Default workflow

For ordinary coding work, ask Codex to use `engineering-workflow:deliver`. It selects the lightweight or full path from risk, ambiguity, and scope.

```text
Use engineering-workflow:deliver to implement this change: <request>.
```

## Force a workflow size

Use lightweight for bounded, low-risk work with clear local verification:

```text
Use the lightweight engineering-workflow:deliver path to <request>.
```

Use full for cross-cutting, ambiguous, security-sensitive, data-sensitive, architectural, or otherwise costly changes:

```text
Use the full engineering-workflow:deliver path to <request>. Investigate through execution, red-team the plan, implement and test, independently review the implementation, fix material findings, retest, and report evidence.
```

## Specialist routing

- `investigate` — Use gstack's global skill for systematic root-cause debugging of runtime failures.
- `engineering-workflow:red-team` — Challenge a diagnosis, plan, or implementation independently.
- `engineering-workflow:review-implementation` — Find incomplete wiring, duplicate ownership, missed consumers, weak tests, and unnecessary complexity.
- `plan-eng-review` — Add a gstack architecture and test-plan review to a consequential full workflow.
- `review` — Add gstack's material pre-landing structural review.
- `qa-only` — Run report-only live web QA without source changes.
- `qa` — Run web QA that may fix and commit; use only after explicitly approving that behavior.
- `ship` — Commit, push, version, and open a PR; invoke only when you explicitly want to ship.

Do not run overlapping custom and gstack skills for the same phase unless a second independent opinion is intentional.

## Short explanations

Type `$eli10`, `$eli15`, `$eli20`, or `$eli30` and select the matching `explain` skill from the picker. You can also write the name naturally at the start of a request.

- `eli10` — About 10 seconds; 24-30 words.
- `eli15` — About 15 seconds; 36-45 words.
- `eli20` — About 20 seconds; 48-60 words.
- `eli30` — About 30 seconds; 72-90 words.

Each version uses plain language suitable for a typical 10-year-old without sacrificing accuracy or sounding childish.

## Repository setup

From a repository that should use this infrastructure:

```bash
sh /Users/hicknughes/Documents/PersonalVentures/codex-agent-infrastructure/bootstrap/init-repo.sh
```

Review the generated `AGENTS.md`, then tailor repository-specific commands, boundaries, and conventions.

## Useful requests

```text
Investigate this bug with the global gstack investigate skill. Establish the root cause with execution evidence before proposing a fix.
```

```text
Red-team this plan with engineering-workflow:red-team, revise it for material findings, but do not implement yet.
```

```text
Review this completed change with engineering-workflow:review-implementation. Focus on incomplete wiring, duplicate responsibilities, missed consumers, regressions, and test gaps.
```

```text
Run qa-only against <URL or local app>. Report findings and evidence; do not edit or commit.
```

## Operating notes

- Begin a new Codex task after installing or updating plugins so skill discovery refreshes.
- State exact skill names when you want deterministic routing; gstack skills are global while custom skills are plugin-qualified.
- Keep `qa` and `ship` explicit because they can create commits or publish work.
- The custom `deliver` workflow remains the default end-to-end owner; gstack supplies optional specialists.
