---
description: Scope an underspecified scientific figure request before rendering
---

Route to `fig/intake-design/WORKFLOW.md` in scoping mode.

Use when the request names a scientific figure, paper figure, journal-ready
figure, or target-journal style but lacks enough detail to render or export.

Output only a `figure_intake` artifact with:

- scientific message or missing-message question
- data status
- candidate figure types
- target journal/style status
- concrete missing inputs
- selected workflow chain

Do not render files in this mode. If data are absent, mark the result
`NON_DATA_MOCKUP` or `DATA_STATUS: MISSING`.
