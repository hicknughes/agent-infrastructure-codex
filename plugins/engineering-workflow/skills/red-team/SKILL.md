---
name: red-team
description: Run an independent adversarial review of a diagnosis, plan, or implementation. Use on demand or as the pre-implementation and post-implementation checkpoints in the full delivery workflow. Trigger on "red-team this", "challenge this plan", "find flaws", "review adversarially", or high-risk engineering changes.
---

# Red Team

Challenge the artifact with evidence, not performative objections.

## Diagnosis or plan review

Spawn independent subagents in parallel when available:

- **Diagnosis challenger:** seek evidence that the stated cause is wrong; test assumptions and alternative explanations.
- **Plan challenger:** identify missed consumers, contracts, interactions, failure modes, rollback needs, and verification gaps.

Give reviewers the problem evidence and artifact under review, but not the desired verdict. Require file references, commands, or concrete scenarios for material claims.

## Implementation review

Use `review-implementation`, preferably in an independent subagent that did not author the change.

## Consolidation

Classify findings as:

- **Material:** changes the diagnosis, plan, correctness, safety, or completeness
- **Minor:** worthwhile but not blocking
- **Unsupported:** speculative and not backed by repository evidence

Revise the plan or implementation for material findings. Do not manufacture disagreement. A clean result is valid when supported by the checks performed.
