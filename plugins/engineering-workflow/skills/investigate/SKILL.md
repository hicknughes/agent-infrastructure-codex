---
name: investigate
description: Diagnose code behavior through execution, reproduction, targeted probes, and explicit assumption tracking. Use when a bug is unclear, a plan depends on uncertain behavior, code reading may be misleading, or the user asks for robust investigation, root cause, reproduction, or evidence before planning.
---

# Investigate

Determine what the system actually does.

1. Define the observed symptom, expected behavior, and the smallest reproducible boundary.
2. Inspect repository instructions, relevant code, tests, configuration, recent changes, and existing implementations.
3. List material hypotheses and the evidence that would distinguish them.
4. Execute the cheapest decisive checks: existing tests, focused test cases, function probes, controlled scripts, logs, fixtures, or read-only data queries.
5. Delegate independent hypotheses to explorer or worker subagents when parallel evidence gathering materially helps. Ask each for commands, observations, and falsification criteria.
6. Track each material assumption as verified, falsified, or unresolved.
7. Conclude with the best-supported explanation, confidence, and what would change the conclusion.

Do not accept source-code intent as proof of runtime behavior. Do not modify production data, call paid services, or trigger external side effects merely to investigate without appropriate approval.

Return:

- Commands or probes run
- Observed results
- Hypotheses eliminated
- Root cause or bounded conclusion
- Remaining uncertainty
