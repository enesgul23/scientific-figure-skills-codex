# Figure Quality Gates

Mandatory and conditional gates for audits, revisions, and final packaging.

## Gate Results

Use:

- `PASS`: evidence is adequate for available materials.
- `PASS_WITH_WARNINGS`: usable with explicit limitations.
- `FAIL`: required fix before final figure or submission use.
- `NOT_APPLICABLE`: gate does not apply.
- `NOT_VERIFIABLE`: materials are insufficient to judge.

## Mandatory Gates

| Gate | Requirement | Typical reviewer |
|---|---|---|
| G1 Data provenance | Data source or explicit data absence is recorded. | `visual_integrity_reviewer_agent` |
| G2 Visual claim ledger | Evidence-bearing elements map to data, computation, or design-only status. | `visual_integrity_reviewer_agent` |
| G3 Chart appropriateness | Plot type fits the scientific question. | `chart_selection_agent` |
| G4 Statistical honesty | Sample size, uncertainty, intervals, correction, and scale choices are clear. | `statistical_reviewer_agent` |
| G5 Axis and unit integrity | Axes, labels, units, and transformations are visible. | `statistical_reviewer_agent` |
| G6 Caption integrity | Caption does not claim more than the figure supports. | `caption_integrity_agent` |
| G7 Accessibility | Color, contrast, text size, redundancy, and alt text are considered. | `accessibility_reviewer_agent` |
| G8 Journal style status | `VERIFIED`, `ESTIMATED`, or `UNVERIFIED` is explicit. | `journal_policy_agent` |
| G9 Export readiness | Formats, DPI, fonts, and manifest fit the use case. | `export_manifest_agent` |
| G10 Reproducibility | Code/data/manifest or design-only status is clear. | `reproducibility_packager_agent` |

## Conditional Gates

| Gate | Applies when | Requirement |
|---|---|---|
| G11 Image integrity | Scientific images are used | Raw provenance limits and manipulation risks are stated. |
| G12 Geospatial integrity | Maps or spatial overlays are used | CRS, projection, units, scale, legend, and source are present. |
| G13 Clinical reporting | Patient/trial/clinical claims are shown | Denominators, endpoints, uncertainty, and time windows are clear. |
| G14 Omics correction | Many-test omics inference is shown | Normalization, thresholds, and correction status are stated. |
| G15 Model validation | Model performance is shown | Splits, metrics, calibration/uncertainty, and leakage risk are addressed. |
| G16 Mechanism status | Schematics imply mechanisms | Evidence/hypothesis status is labeled. |

## Blocking Conditions

Return `FAIL` when:

- data-derived numeric claims lack supplied data or computation source
- target-journal compliance is claimed without verified guidance
- clinical rates or risks lack denominators
- maps lack CRS/projection when a scientific map is requested
- omics significance lacks correction status
- captions make unsupported causal or mechanistic claims
- a final package lacks code/data traceability and is not marked design-only

## Report Format

```markdown
## Gate Results
| Gate | Result | Evidence | Required Fix |
|---|---|---|---|
| G1 Data provenance | PASS | data/analysis_data.xlsx |  |
| G8 Journal style status | PASS_WITH_WARNINGS | stored Nature estimate | Verify current guidance before submission |
```
