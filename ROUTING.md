# Custom Workflow and Gstack Routing

## Default Owner

Use the custom `deliver` skill for end-to-end coding work. It selects the lightweight or full workflow, preserves the selected quality gates, and reports completion evidence.

Use custom `best-of-3` only on explicit request for consequential work where comparing three complete implementations justifies roughly triple implementation cost. It is not a default phase of `deliver`.

## Gstack Specialists

- Global `office-hours` and `autoplan`: product discovery and broad planning before coding scope is settled.
- Global `investigate`: systematic root-cause debugging for reported runtime failures.
- Global `plan-eng-review`: additional architecture and test-plan review during the full workflow.
- Global `review`: additional specialist pre-landing review for material changes.
- Global `qa-only`: live web QA without source changes.
- Global `qa`: live web QA with iterative fixes and commits; require user approval first.
- Global `ship`: release automation that may commit, push, and open a pull request; explicit user request only.

## Custom Authorities

- `review-implementation`: request-to-evidence closure, incomplete wiring, duplicate responsibilities, missing consumers, and unnecessary abstraction; completion requires `VERDICT: PASS`.
- Documentation plugin: TOC, handoff, and documentation-consistency artifacts.
- Policy plugin: stable policy IDs, contract-change checks, concept audits, and compliance matrices.

## Conflict Rule

Do not silently run both custom and gstack workflows for the same phase. The `deliver` orchestrator chooses one primary specialist per phase and adds a second review only when risk justifies the cost.
