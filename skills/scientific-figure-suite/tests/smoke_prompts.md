# Smoke Prompts

Use these in a fresh Codex conversation after installing the skill.

## 1. Routing: Vague Figure Request

```text
Use $scientific-figure-suite. I need a beautiful Nature-style figure for my paper, but I have not prepared the data yet.
```

Expected:

- route to `intake-design`
- apply figure scoping mode
- ask for data, message, target journal, and figure type
- do not render or export files
- do not produce fake data
- mark `DATA_STATUS: MISSING`

## 2. Statistical Plot

```text
Use $scientific-figure-suite to create a boxplot and scatter overlay for treatment vs control using this table: [provide small table]. Target: high-impact biomedical journal.
```

Expected:

- route to `statistical-plots`
- prefer distribution-revealing plot
- include N and uncertainty where possible

## 3. Nature Style Status

```text
Use $scientific-figure-suite to make this figure Nature-compliant.
```

Expected:

- route to `journal-style-translator`
- ask for or verify current Nature guidelines
- if not available, mark `ESTIMATED` or `UNVERIFIED`, not `VERIFIED`

## 4. Caption Integrity

```text
Use $scientific-figure-suite to write a caption for a figure that shows correlation between rainfall and discharge. Do not claim causation.
```

Expected:

- caption avoids causal language
- visual claim ledger marks descriptive or comparative claims only

## 5. Model Performance

```text
Use $scientific-figure-suite to create model performance panels for observed vs predicted discharge, residuals, and uncertainty intervals.
```

Expected:

- route to `model-performance`
- suggest multi-panel chain
- do not invent metrics

## 6. Clinical Forest Plot

```text
Use $scientific-figure-suite to prepare a Lancet-style forest plot plan from subgroup HRs and 95% CIs.
```

Expected:

- route to `clinical-biomedical` and `journal-style-translator`
- style status is not verified unless guidelines are provided
- denominators and CI requirements are emphasized

## 7. Geospatial Map

```text
Use $scientific-figure-suite to design a flood inundation map figure with DEM background, gauges, and model error overlay.
```

Expected:

- route to `geospatial-maps`
- ask for CRS, data sources, units, legend, and projection

## 8. Graphical Abstract

```text
Use $scientific-figure-suite to design a Science-style graphical abstract for a hydro-AI model that couples groundwater and surface flooding.
```

Expected:

- route to `graphical-abstract` and `schematic-mechanism`
- no unsupported mechanism claims
- `STYLE_STATUS` remains `ESTIMATED` or `UNVERIFIED` unless verified
