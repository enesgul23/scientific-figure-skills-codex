# Journal Style Translator

## Purpose

Translate a figure plan into target journal or publisher style constraints while clearly marking verification status.

## Trigger Conditions

Use when the user asks for Nature-style, Science-style, Lancet-style, journal-ready, submission figure, publisher format, column sizing, DPI, accepted formats, or style compliance.

## Required Inputs

- target journal or publisher
- figure type
- current official guideline or user-provided guideline if verified compliance is requested

## Optional Inputs

- article type
- print or online target
- column width
- color-space requirement
- export format requirement

## Output Contract

Produce a style translation report:

```yaml
journal_style:
  target:
  guideline_source: live_official | user_provided | stored_estimate | unavailable
  status: VERIFIED | ESTIMATED | UNVERIFIED
  checked_at:
  applied_decisions: {}
  unresolved_requirements: []
```

## Procedure

1. Determine whether current official or user-provided guidelines are present.
2. Set status to `VERIFIED`, `ESTIMATED`, or `UNVERIFIED`.
3. Load `references/journal_style_profiles.md` and relevant style token JSON when needed.
   Validate bundled or project style tokens with `scripts/validate_style_tokens.py`
   before treating them as renderer inputs.
4. Apply fallback high-impact defaults when journal rules are unavailable.
5. List unresolved requirements.
6. Prevent false compliance language.

## Quality Gates

- style status is explicit
- source is recorded
- unresolved requirements are listed for `ESTIMATED` or `UNVERIFIED`
- no false compliance claim appears
- target journal name is not used as a substitute for official guidance

## Failure Modes

- current guideline is unavailable
- user-provided instructions conflict with stored estimates
- target journal is ambiguous
- user demands verified compliance without evidence

## Memory Integration

If project memory exists, read `shared/submission_memory_runtime.md` and
validate memory before style translation. Use `journal_targets.json` and
`journal_guideline_verification.jsonl` to decide whether the target journal is
`VERIFIED`, `ESTIMATED`, or `UNVERIFIED`. Append a verification ledger entry
only when current official or user-provided guideline evidence is available.

## Agent Role References

- `agents/journal_policy_agent.md` for verified/estimated/unverified status assignment.
- `agents/style_token_agent.md` for concrete size, font, panel-label, color, and export decisions.

## Handoff Rules

Hand off to `multipanel-composer` for layout constraints, `export-packager` for file formats, and `figure-auditor` for final style-status checks.
