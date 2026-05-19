# Clinical Biomedical

## Purpose

Create clinical, epidemiological, and biomedical figures such as CONSORT diagrams, Kaplan-Meier curves, forest plots, adverse-event charts, timelines, dose-response plots, diagnostic accuracy figures, and risk-of-bias summaries.

## Trigger Conditions

Use when the user mentions clinical trials, cohorts, patients, endpoints, survival, hazard ratios, odds ratios, risk ratios, diagnostic performance, adverse events, or CONSORT/STROBE/PRISMA-style reporting.

## Required Inputs

- sample sizes and denominators
- groups or arms
- endpoint definitions
- effect sizes, counts, rates, or time-to-event data

## Optional Inputs

- censoring data
- subgroup definitions
- target journal
- confidence interval method
- population inclusion/exclusion criteria
- risk-of-bias or safety categories

## Output Contract

Produce a clinically interpretable figure plan or code, caption, denominator notes, uncertainty notes, and audit flags.

## Procedure

1. Identify the clinical question and endpoint.
2. Verify denominators for every group, subgroup, and event category.
3. Select figure type: CONSORT, Kaplan-Meier, forest, adverse event, swimmer, timeline, diagnostic, or baseline balance.
4. Show confidence intervals, censoring, or uncertainty when relevant.
5. Avoid subgroup claims unless the analysis plan supports them.
6. Write caption language with endpoint definitions and time windows.

## Quality Gates

- denominators are shown or stated
- confidence intervals or uncertainty are shown where relevant
- endpoint and time horizon are clear
- absolute and relative effects are not conflated
- clinical overclaiming is avoided

## Failure Modes

- denominators are missing
- censoring is ignored in survival plots
- subgroup fishing is presented as definitive evidence
- endpoint is ambiguous
- adverse-event grades or severity are unspecified

## Memory Integration

If project memory exists, read `shared/submission_memory_runtime.md` and
validate memory before drawing clinical or biomedical figures. Carry denominator,
endpoint, cohort, image provenance, and journal-status unresolved requirements
through the Figure Passport. Append visual claim ledger entries for every
clinical or biological claim that a panel encodes.

## v0.6 Dependency Planning

Inspect clinical tables before rendering. Survival figures should select
`lifelines` by default and reserve `scikit-survival` for specialist model
performance needs because of install risk. External benchmark, registry, or
reference data must pass the external data decision protocol with citation,
license, and contamination-risk review.

## Agent Role References

- `agents/clinical_reporting_agent.md` for endpoint, population, CI, and clinical readability checks.
- `agents/denominator_endpoint_agent.md` for denominators, event windows, and subgroup consistency.

## Handoff Rules

Hand off to `journal-style-translator`, `caption-alttext`, and `figure-auditor`. Use `export-packager` only after mandatory clinical details are resolved.
