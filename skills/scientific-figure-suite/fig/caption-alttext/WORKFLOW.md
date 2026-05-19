# Caption Alt Text

## Purpose

Write figure captions, legends, notes, in-text references, and accessibility alt text that accurately describe only what the figure and data support.

## Trigger Conditions

Use when the user asks for a caption, figure legend, panel legend, note, in-text reference, alt text, accessibility description, or caption audit.

## Required Inputs

- figure specification or visible figure description
- shown variables
- supported key result
- sample sizes when relevant

## Optional Inputs

- journal style
- word limit
- audience level
- statistical method details
- data source statement

## Output Contract

Produce caption title, full caption or legend, notes, in-text reference sentence, alt text, and visual claim ledger alignment.

## Procedure

1. Identify what is visible in each panel.
2. Identify supported descriptive, comparative, predictive, mechanistic, or methodological claims.
3. Write concise title and panel-by-panel caption text.
4. Add sample size, uncertainty, statistical method, and data source notes where needed.
5. Write alt text that conveys figure type, variables, trend, and uncertainty without overclaiming.
6. Remove claims not visible in the figure or supported by the ledger.

## Quality Gates

- caption does not claim unshown or unsupported results
- N, CI, uncertainty, and endpoint definitions are included when relevant
- alt text is useful and not a duplicate of the filename
- caption can stand alone
- style status is not falsely upgraded

## Failure Modes

- caption explains data not shown
- sample size or uncertainty is missing
- visual metaphor is not explained
- causal language appears for correlation-only evidence

## Memory Integration

If project memory exists, read `shared/submission_memory_runtime.md` and
validate memory before caption or alt-text work. Use Figure Passport panels and
visual claim ledger entries to align caption language with encoded evidence.
After captioning, update the Figure Passport and preserve unresolved details in
memory rather than hiding them.

## Agent Role References

- `agents/caption_integrity_agent.md` for claim-aligned captions and notes.
- `agents/alt_text_agent.md` for accessibility alt text and extended descriptions.

## Handoff Rules

Hand off to `figure-auditor` for caption-integrity review and to `export-packager` when final package files are being assembled.
