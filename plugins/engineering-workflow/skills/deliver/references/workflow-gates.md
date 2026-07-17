# Workflow Gates

## Investigation Gate

- Relevant behavior was reproduced or directly probed when practical.
- Material assumptions are marked verified, falsified, or unresolved.
- Existing implementations and likely consumers were searched.
- The proposed cause explains observed evidence, not only source-code intent.

## Plan Gate

- Scope and non-goals are explicit.
- Every affected consumer, registration point, contract, migration, and configuration path is accounted for.
- Verification commands and expected evidence are named.
- Risks and rollback needs are proportionate to the change.

## Implementation Gate

- The implementation follows the verified plan or documents why it changed.
- New abstractions have a single clear responsibility and do not duplicate an existing owner.
- Wiring is complete from entry point through persistence or external effect where applicable.
- Tests cover behavior and meaningful failure paths.

## Completion Gate

- Required tests and checks ran successfully, or limitations are explicit.
- Independent implementation review found no unresolved material issue.
- Documentation and operational steps match changed behavior.
- The report distinguishes verified facts from remaining uncertainty.
