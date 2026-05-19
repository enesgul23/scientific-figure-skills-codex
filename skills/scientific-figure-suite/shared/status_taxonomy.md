# Status Taxonomy

Use these status labels consistently across all figure workflows.

## Data Status

| Label | Meaning |
|---|---|
| `PROVIDED` | User supplied data, code, image, or structured results sufficient for the requested figure. |
| `INFERRED` | Some structure was inferred from filenames, columns, or user prose; confirm before final submission use. |
| `MISSING` | Required data or metadata are absent. |
| `MOCKUP` | Output is design-only and must be marked `NON_DATA_MOCKUP`. |

## Style Status

| Label | Meaning |
|---|---|
| `VERIFIED` | Current official guidance was checked in this task, or current user-provided guidance was supplied. |
| `ESTIMATED` | Stored profile or general high-impact style estimate was used. |
| `UNVERIFIED` | No reliable current profile is available. |

## Reproducibility Status

| Label | Meaning |
|---|---|
| `CODED` | Figure can be regenerated from supplied code and data. |
| `DESIGN_ONLY` | No data-derived rendering is claimed. |
| `PARTIAL` | Some assets, manual steps, or external files remain unresolved. |

## Export Status

| Label | Meaning |
|---|---|
| `READY` | Required formats and manifest are available or exact commands are provided. |
| `NEEDS_RENDER` | Design/code exists, but final files were not rendered. |
| `NEEDS_JOURNAL_CHECK` | Export choices depend on unverified journal requirements. |

## Integrity Status

| Label | Meaning |
|---|---|
| `PASS` | Mandatory checks passed for available materials. |
| `PASS_WITH_WARNINGS` | Usable with disclosed limitations. |
| `FAIL` | Must fix before final figure or submission use. |
