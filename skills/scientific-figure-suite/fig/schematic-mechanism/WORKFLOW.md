# Schematic Mechanism

## Purpose

Design mechanism, workflow, process, method, and conceptual scientific diagrams without inventing unsupported claims.

## Trigger Conditions

Use when the user asks for a mechanism diagram, conceptual figure, workflow diagram, process illustration, study design schematic, experimental design diagram, or method figure.

## Required Inputs

- entities or process steps
- relationship types
- claim status for each relationship: observed, inferred, hypothesized, or illustrative

## Optional Inputs

- target journal
- visual style preference
- palette
- source figure assets
- audience level

## Output Contract

Produce schematic specification, relationship ledger, caption with epistemic-status language, and integrity warnings.

## Procedure

1. Extract entities, processes, states, and outputs.
2. Classify arrows as causal, temporal, data flow, association, inhibition, activation, or conceptual.
3. Mark evidence level for each relationship.
4. Design visual hierarchy with minimal text and clear grouping.
5. Generate diagram instructions or code only from supplied relationships.
6. Use "proposed", "hypothesized", or "conceptual" when evidence is not definitive.

## Quality Gates

- no invented mechanism
- arrow semantics are defined
- hypotheses are labeled
- caption does not overclaim
- icons or metaphors do not imply unsupported biology or clinical effect

## Failure Modes

- user asks to show an unproven mechanism as fact
- entity definitions are missing
- causal arrows lack evidence
- visual metaphor changes the scientific claim

## Memory Integration

If project memory exists, read `shared/submission_memory_runtime.md` and
validate memory before schematic work. Use the visual claim ledger to separate
data-supported mechanisms from hypotheses and design-only elements. Update the
Figure Passport with schematic status and mark unsupported mechanisms as
unverified rather than evidence-backed.

## Agent Role References

- `agents/mechanism_claim_agent.md` for arrow semantics, evidence status, and mechanistic overclaim checks.

## Handoff Rules

Hand off to `graphical-abstract` for full-paper visual summaries, `caption-alttext` for explanatory text, and `figure-auditor` for claim checking.
