---
name: review-implementation
description: Independently review a completed code change for incomplete wiring, duplicate responsibilities, regressions, missing consumers, weak tests, and unnecessary complexity. Use after initial implementation and tests, before reporting completion, or when the user suspects half-wired or bloated code.
---

# Review Implementation

Review the diff and the surrounding responsibility boundaries. Prefer an independent subagent that did not write the implementation.

1. Read applicable `AGENTS.md`, the plan, and the implementation diff.
2. Trace changed behavior end to end from entry point through consumers and side effects.
3. Search for every existing implementation of the same responsibility, including similar names, registrations, adapters, handlers, and configuration paths.
4. Check all consumers, exports, dependency injection, routes, schemas, migrations, feature flags, environment variables, documentation, and operational steps that may require updates.
5. Run focused tests or probes for suspected gaps. Do not rely only on visual review when execution is practical.
6. Evaluate whether new abstractions reduce duplication or merely add another path.
7. Report only evidence-backed findings, ordered by severity, with file references and a concrete failure scenario.

If no material issues remain, state what was checked and why the implementation appears complete. If issues are fixed, re-run affected tests and broader verification before closure.
