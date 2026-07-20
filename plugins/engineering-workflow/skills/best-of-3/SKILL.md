---
name: best-of-3
description: Run an explicit, high-cost implementation tournament that builds three independent candidates in isolated Git worktrees, evaluates them against verified requirements, and applies only a passing winner. Use only when the user explicitly requests Best-of-3, multiple implementations, or an implementation tournament for consequential work.
---

# Best of 3

Build three independent implementations from the same clean baseline, evaluate them with repository evidence, and apply only a candidate that passes the full definition of done.

## Safety and cost gate

- Run only on explicit user request. Never trigger this workflow merely because a task is difficult.
- Explain that it uses roughly three implementation runs plus an evaluator.
- Require a Git repository with a clean worktree. If tracked or untracked changes exist, stop and ask the user to commit, stash, or choose another baseline.
- Do not push any branch. Candidate-local commits are disposable tournament artifacts; applying the winner must not commit the main worktree.
- Never select the "least bad" candidate. `NO WINNER` is valid when none satisfies the requirements.

## Prepare

1. Investigate the request enough to establish verified context, material assumptions, repository conventions, and baseline behavior.
2. Write a shared definition of done with requirements, consumers, non-goals, and exact validation commands.
3. Run baseline validation before candidates start. Record pre-existing failures separately.
4. Resolve `scripts/best_of_3_worktrees.py` relative to this `SKILL.md`, then run:

   ```bash
   python3 <skill-dir>/scripts/best_of_3_worktrees.py create <repository-root>
   ```

   Preserve the returned manifest path. It is required for status, application, and cleanup.

## Build candidates

Spawn three worker subagents concurrently, one per candidate worktree. Give every candidate the same request, evidence, definition of done, and validation commands. Tell candidates not to inspect one another.

- **Candidate 1 — native/minimal:** Prefer existing repository patterns and the smallest complete change.
- **Candidate 2 — contract-first:** Trace boundaries and consumers first, then implement the cleanest complete contract.
- **Candidate 3 — independent alternative:** Seek a materially different but simple approach; avoid novelty without benefit.

Each candidate must:

1. Read applicable `AGENTS.md` files.
2. Investigate independently rather than trusting the parent diagnosis.
3. Implement the complete request in its assigned worktree.
4. Run the shared validation plus any candidate-specific checks.
5. Search for duplicate responsibility and incomplete wiring.
6. Commit all candidate changes locally with a message beginning `best-of-3 candidate`.
7. Return its commit hash, changed files, commands and outcomes, assumptions, and known limitations.

## Evaluate independently

Use an evaluator subagent that did not implement any candidate. Keep it read-only when possible. Give it the original request, definition of done, baseline evidence, manifest path, and candidate paths—but not a preferred winner.

The evaluator must inspect each worktree and rerun relevant checks. Candidate summaries are leads, not evidence. Score in this order:

1. Correctness and complete requirement coverage
2. End-to-end wiring and consumer coverage
3. Fit with existing ownership boundaries
4. Simplicity and absence of duplicate responsibility
5. Test quality, regression risk, and operational completeness

Return an evidence matrix and exactly one verdict: `WINNER: 1`, `WINNER: 2`, `WINNER: 3`, or `NO WINNER`.

## Apply and verify

If there is a winner, require its worktree to be clean with all changes committed, then apply its diff without committing the main worktree:

```bash
python3 <skill-dir>/scripts/best_of_3_worktrees.py apply <manifest-path> <candidate-number>
```

Then:

1. Inspect the applied diff in the main worktree.
2. Run targeted and repository-level validation again.
3. Use `engineering-workflow:review-implementation` as the request-to-evidence closure gate.
4. Fix material findings and repeat validation and closure review until `VERDICT: PASS`, with a maximum of three review/fix cycles.
5. If the gate still fails, report incomplete work and do not claim success.

If the evaluator returns `NO WINNER`, apply nothing. Summarize why each candidate failed and propose the next investigation step.

## Cleanup

Show tournament status with:

```bash
python3 <skill-dir>/scripts/best_of_3_worktrees.py status <manifest-path>
```

Candidate worktrees preserve evidence by default. Remove clean candidates with `remove`; removing dirty candidates requires both explicit user approval and `--force`:

```bash
python3 <skill-dir>/scripts/best_of_3_worktrees.py remove <manifest-path>
```

Report the manifest path, candidate paths, winner rationale, applied state, closure verdict, tests, remaining worktrees, and whether any commit or push occurred.
