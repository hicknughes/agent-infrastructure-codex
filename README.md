# Codex Agent Infrastructure

Codex-native, modular engineering workflows derived selectively from the adjacent Claude agent infrastructure. The repositories are intentionally independent.

## Plugins

- **Engineering Workflow** — Lightweight and full delivery paths, execution-first investigation, adversarial plan review, implementation review, and planning logs.
- **Documentation** — Documentation indexes, cold-start handoffs, and doc-to-code consistency audits.
- **Policy** — Stable policy rules, contract consumer checks, concept-drift audits, and compliance matrices.
- **Explain** — Plain-language ELI10 explanations sized for 10, 15, 20, or 30-second reads.

Hooks, custom worktree coordination, automatic permission mutation, and Claude compatibility shims are intentionally excluded from the initial system.

## Gstack Coexistence

Gstack is installed separately as namespaced global Codex skills. The custom `deliver` workflow owns end-to-end coding changes and routes deliberately to gstack specialists:

| Need | Default |
|---|---|
| Coding change | Custom `deliver` |
| Runtime bug investigation | Gstack global `investigate` |
| Additional engineering-plan review | Gstack global `plan-eng-review` |
| Wiring and duplication review | Custom `review-implementation` |
| Material pre-landing review | Gstack global `review` |
| Live web QA | Gstack global `qa` or report-only `qa-only` |
| Commit, push, and PR | Explicitly requested gstack global `ship` |

Custom documentation and policy plugins remain authoritative for their repository artifacts.

## Install for Codex Desktop

```bash
codex plugin marketplace add /Users/hicknughes/Documents/PersonalVentures/codex-agent-infrastructure
codex plugin add engineering-workflow@codex-agent-toolkit
codex plugin add documentation@codex-agent-toolkit
codex plugin add policy@codex-agent-toolkit
codex plugin add explain@codex-agent-toolkit
```

Restart Codex Desktop and begin a new task after installation.

## Daily Use

See [QUICKSTART.md](QUICKSTART.md) for lightweight and full workflow prompts, specialist routing, and safety boundaries around `qa` and `ship`.

## Initialize a Repository

From a target repository:

```bash
sh /Users/hicknughes/Documents/PersonalVentures/codex-agent-infrastructure/bootstrap/init-repo.sh
```

The script creates `AGENTS.md` only when one does not already exist and scaffolds standard planning and handoff directories.

## Validate

```bash
python3 scripts/validate_toolkit.py
python3 -m unittest discover -s tests -v
```
