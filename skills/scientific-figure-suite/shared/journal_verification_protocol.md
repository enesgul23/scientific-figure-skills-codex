# Journal Verification Protocol

Use this protocol for journal and publisher style claims.

## Status Assignment

Set `STYLE_STATUS: VERIFIED` only when one of these is true:

- current official journal guidance was checked in this active task
- the user supplied current journal guidance

Set `STYLE_STATUS: ESTIMATED` when using stored profiles or high-impact defaults.

Set `STYLE_STATUS: UNVERIFIED` when no reliable profile is available.

## Source Recording

Record:

- target journal or publisher
- guideline source: `live_official`, `user_provided`, `stored_estimate`, or `unavailable`
- checked date when verified
- unresolved requirements

## Language Rules

Allowed for non-verified output:

- `Nature-inspired estimated profile`
- `target-journal style estimate pending guideline verification`
- `unverified publisher-format draft`

Forbidden unless verified:

- `[Journal]-compliant`
- `submission-ready for [journal]`
- `meets all [journal] requirements`

## Handoff

`journal-style-translator` produces the style report. `figure-auditor` checks
that the status and language remain consistent. `export-packager` preserves the
same status in the manifest.
