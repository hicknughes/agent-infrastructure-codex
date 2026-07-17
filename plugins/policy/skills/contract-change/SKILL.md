---
name: contract-change
description: Enforce the consumer-enumeration checklist when a shared contract changes between frontend and backend. Use whenever a shared API, schema, or interface is modified.
---

# /contract-change

You enforce the consumer-enumeration checklist when a shared contract between frontend and backend changes. No contract change ships without every consumer accounted for.

Trigger: "contract change", "shared type changed", "API shape changed", "FE/BE contract"

## Steps

1. Identify the contract change (API shape, DB column, enum value, route param).
2. Enumerate every consumer in both layers (frontend and backend) by grepping for usage of the changed identifier.
3. For each consumer, confirm it has been updated or flag it as outstanding.
4. Require at least one end-to-end contract test exercising the changed boundary.
5. Require plan gate: the plan must explicitly note "this is a contract change" before proceeding.

## Output format

```
Contract change: <description of what changed>

Consumers found and updated:
  - <file>:<line> ✓
  - <file>:<line> ✓
  - <file>:<line> ✗ NOT UPDATED

Contract test coverage:
  - <test file> — exercises <boundary>

Plan gate: [ ] plan.md notes this as a contract change
```

## Constraints

- Block the change if any consumer is not confirmed updated.
- Block if no contract test exists exercising the boundary.
- Block if the plan does not note the contract change explicitly.
- Surface the full consumer list even if all are updated — visibility matters.
