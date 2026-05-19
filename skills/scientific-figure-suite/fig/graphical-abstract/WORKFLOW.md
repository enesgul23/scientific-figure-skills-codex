# Graphical Abstract

## Purpose

Create innovative but scientifically constrained graphical abstracts that summarize a study's question, method, evidence, and implication without inventing claims.

## Trigger Conditions

Use when the user asks for a graphical abstract, visual summary, journal visual abstract, cover-like concept, high-impact visual explanation, or single-screen research story.

## Required Inputs

- study question
- main finding
- method or workflow
- evidence status
- target audience

## Optional Inputs

- target journal
- visual style preference
- approved icons or images
- word limit
- article type

## Output Contract

Produce graphical abstract concept, layout, visual hierarchy, caption or short legend, alt text, and integrity warnings.

## Procedure

1. Identify the one-message story.
2. Separate method, data/evidence, and interpretation.
3. Choose a left-to-right, top-to-bottom, or center-out narrative.
4. Use minimal text and restrained color hierarchy.
5. Avoid decorative misinformation and unsupported outcome claims.
6. Mark any data-free concept as `NON_DATA_MOCKUP`.

## Quality Gates

- visual narrative is clear
- unsupported claims are absent or labeled as hypotheses
- text load is minimal
- colors are accessible
- journal style status is explicit

## Failure Modes

- too many concepts compete
- visual metaphor is misleading
- image assets are unavailable
- user asks for data-derived outcome without data
- journal-specific graphical abstract rules are unverified

## Memory Integration

If project memory exists, read `shared/submission_memory_runtime.md` and
validate memory before graphical abstract work. Use project profile and author
visual style only as soft constraints below evidence, accessibility, and journal
requirements. Update Figure Passport entries and claim ledger records for every
visual message carried into the abstract.

## Agent Role References

- `agents/visual_narrative_agent.md` for one-message graphical abstract structure.
- `agents/evidence_boundary_agent.md` for evidence-derived vs illustrative element separation.

## Handoff Rules

Hand off to `schematic-mechanism` for relationship semantics, `journal-style-translator` for target style, `caption-alttext` for text, and `figure-auditor` for integrity.
