# Artifact Reproducibility Pattern

A figure package should document configuration and lineage. This is not a byte-level replay guarantee.

## Non-Negotiable Limitations

- LLM outputs are not byte-reproducible.
- Live journal guidelines can change.
- Plotting libraries and fonts can render differently across systems.
- External basemaps, databases, and APIs can change.

## Figure Passport `repro_lock`

```yaml
repro_lock:
  schema_version: "1.0"
  stochasticity_declaration: "LLM and rendering outputs are not byte-reproducible. This lock documents configuration, not deterministic replay."
  suite_version:
  model:
    family:
    id:
    weight_stable: false
  prompts:
    hash_timing: skill-load
    skill_md_hash:
    agents_bundle_hash:
  materials:
    list_hash:
    count:
  external_protocols:
    journal_guideline_snapshot_available: false
    basemap_snapshot_available: false
  rendering:
    software:
    version:
    fonts:
```

## Red Flags

- absolute local paths in released manifest
- missing stochasticity declaration
- style status changed without re-audit
- data/code changed after quality report
- manual figure edits not documented
