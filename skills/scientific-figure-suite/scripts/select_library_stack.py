from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from _common import load_structured_file, main_error, write_json
from _memory import utc_now
from validate_library_pool import pool_libraries
from validate_render_template_registry import registry_entries


DOMAIN_RULES: dict[str, dict[str, list[str]]] = {
    "tabular": {
        "required": ["pandas", "numpy", "matplotlib"],
        "recommended": [],
        "optional": ["seaborn"],
        "rationale": ["Tabular datasets default to the static, vector-friendly pandas/numpy/matplotlib stack."],
    },
    "large-data": {
        "required": ["polars", "duckdb"],
        "recommended": ["pandas", "numpy", "matplotlib"],
        "optional": ["datashader", "dask"],
        "rationale": ["Large tabular/time-series data should be reduced with polars or duckdb before final static rendering."],
    },
    "geospatial-vector": {
        "required": ["geopandas", "shapely", "pyproj", "matplotlib"],
        "recommended": [],
        "optional": ["cartopy", "contextily"],
        "rationale": ["Vector map data require CRS-aware geospatial handling before publication rendering."],
    },
    "geospatial-raster": {
        "required": ["rasterio", "xarray", "matplotlib"],
        "recommended": [],
        "optional": ["cartopy", "rioxarray"],
        "rationale": ["Raster and gridded geospatial data need raster metadata handling and static rendering."],
    },
    "climate-netcdf": {
        "required": ["xarray", "netCDF4", "matplotlib"],
        "recommended": ["cftime"],
        "optional": ["cartopy", "rioxarray"],
        "rationale": ["NetCDF climate-like data should use labeled multidimensional arrays before rendering."],
    },
    "omics": {
        "required": ["scanpy", "anndata", "matplotlib"],
        "recommended": [],
        "optional": ["squidpy", "decoupler"],
        "rationale": ["AnnData/omics figures require domain-aware matrix and metadata tooling."],
    },
    "survival": {
        "required": ["lifelines", "matplotlib"],
        "recommended": ["pandas", "numpy"],
        "optional": ["scikit-survival"],
        "rationale": ["Survival figures require censoring-aware survival analysis tooling."],
    },
    "network": {
        "required": ["networkx", "matplotlib"],
        "recommended": [],
        "optional": ["graphviz", "pygraphviz"],
        "rationale": ["Network/pathway figures require graph structures before layout rendering."],
    },
    "image": {
        "required": ["pillow", "matplotlib"],
        "recommended": [],
        "optional": ["scikit-image", "opencv-python", "tifffile"],
        "rationale": ["Image or microscopy panels require image IO and integrity-aware processing."],
    },
    "3d": {
        "required": ["pyvista"],
        "recommended": ["trimesh"],
        "optional": ["vedo"],
        "rationale": ["3D scientific assets require a mesh or volume renderer and extra static audit."],
    },
}

CHART_RULES: dict[str, dict[str, list[str]]] = {
    "roc_pr_curve": {
        "required": ["pandas", "numpy", "scikit-learn", "matplotlib"],
        "recommended": [],
        "optional": ["seaborn"],
        "rationale": ["ROC/PR curves require robust metric calculation before static rendering."],
    },
    "parity_scatter": {
        "required": ["pandas", "numpy", "matplotlib"],
        "recommended": [],
        "optional": ["scikit-learn", "seaborn"],
        "rationale": ["Parity scatter is a final static model-performance chart; keep the stack minimal."],
    },
    "clinical_survival": {
        "required": ["lifelines", "matplotlib"],
        "recommended": ["pandas", "numpy"],
        "optional": ["scikit-survival"],
        "rationale": ["Clinical survival plots need event/censoring semantics and survival estimators."],
    },
    "survival_plot": {
        "required": ["lifelines", "matplotlib"],
        "recommended": ["pandas", "numpy"],
        "optional": ["scikit-survival"],
        "rationale": ["Survival plots need event/censoring semantics and survival estimators."],
    },
    "geospatial_raster_map": {
        "required": ["rasterio", "xarray", "matplotlib"],
        "recommended": [],
        "optional": ["cartopy", "rioxarray"],
        "rationale": ["Geospatial raster maps need raster metadata and optional projection support."],
    },
    "omics_umap": {
        "required": ["scanpy", "anndata", "matplotlib"],
        "recommended": [],
        "optional": ["squidpy"],
        "rationale": ["Omics UMAP figures require AnnData/Scanpy-aware embeddings and annotations."],
    },
    "huge_time_series": {
        "required": ["polars", "duckdb", "matplotlib"],
        "recommended": ["pandas", "numpy"],
        "optional": ["datashader", "dask"],
        "rationale": ["Huge time series should be aggregated before publication rendering."],
    },
}


def ordered_unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            ordered.append(value)
    return ordered


def load_environment_status(path: Path | None) -> dict[str, dict[str, Any]]:
    if path is None:
        return {}
    data = load_structured_file(path)
    probe = data.get("environment_probe", data) if isinstance(data, dict) else {}
    libraries = probe.get("libraries", []) if isinstance(probe, dict) else []
    return {str(item.get("library_id")): item for item in libraries if isinstance(item, dict)}


def registry_entry_for_chart(registry: dict[str, Any], chart_type: str) -> dict[str, Any] | None:
    for entry in registry_entries(registry):
        if entry.get("chart_type") == chart_type:
            return entry
    return None


def dataset_domains(dataset_profile: dict[str, Any] | None) -> list[str]:
    if not dataset_profile:
        return []
    root = dataset_profile.get("dataset_profile", dataset_profile)
    domains = root.get("suggested_domains", []) if isinstance(root, dict) else []
    return [str(item) for item in domains]


def build_selection(
    chart_type: str | None,
    dataset_profile: dict[str, Any] | None,
    render_registry: dict[str, Any],
    environment: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    required: list[str] = []
    recommended: list[str] = []
    optional: list[str] = []
    rationale: list[str] = []
    selected_stack_ids: list[str] = []
    fallback_renderer = "matplotlib_static"

    if chart_type:
        registry_entry = registry_entry_for_chart(render_registry, chart_type)
        if registry_entry:
            required.extend(str(item) for item in registry_entry.get("required_libraries", []))
            optional.extend(str(item) for item in registry_entry.get("optional_libraries", []))
            selected_stack_ids.extend(str(item) for item in registry_entry.get("library_stack_ids", []))
            fallback_renderer = str(registry_entry.get("dependency_profile") or fallback_renderer)
            rationale.append(f"Render registry selected dependency profile {fallback_renderer} for {chart_type}.")
        chart_rule = CHART_RULES.get(chart_type)
        if chart_rule:
            required.extend(chart_rule["required"])
            recommended.extend(chart_rule["recommended"])
            optional.extend(chart_rule["optional"])
            rationale.extend(chart_rule["rationale"])

    domains = dataset_domains(dataset_profile)
    for domain in domains:
        rule = DOMAIN_RULES.get(domain)
        if not rule:
            continue
        required.extend(rule["required"])
        recommended.extend(rule["recommended"])
        optional.extend(rule["optional"])
        rationale.extend(rule["rationale"])

    if not required:
        required.extend(["pandas", "numpy", "matplotlib"])
        rationale.append("No domain-specific requirement was detected; using the minimal static manuscript stack.")

    required = ordered_unique(required)
    recommended = [item for item in ordered_unique(recommended) if item not in required]
    optional = [item for item in ordered_unique(optional) if item not in required and item not in recommended]
    selected_stack = ordered_unique([*selected_stack_ids, *required, *recommended])

    blocked: list[dict[str, Any]] = []
    warnings: list[str] = []
    if environment:
        for library_id in required:
            status = environment.get(library_id, {}).get("status")
            if status == "MISSING":
                blocked.append({"library_id": library_id, "reason": "required library is missing from current Python environment"})
        for library_id in optional:
            status = environment.get(library_id, {}).get("status")
            if status == "MISSING":
                warnings.append(f"optional library missing: {library_id}")

    notes = [
        "Do not auto-install dependencies; this selection is an auditable plan.",
        "For manuscript final exports, prefer static vector-friendly rendering unless the user asks for an interactive supplement.",
    ]
    if blocked:
        notes.append("Required missing libraries block registry rendering until installed or replaced by a fallback.")

    return {
        "library_stack_selection": {
            "created_at": utc_now(),
            "chart_type": chart_type,
            "detected_domains": domains,
            "selected_stack": selected_stack,
            "required_libraries": required,
            "recommended_libraries": recommended,
            "optional_libraries": optional,
            "blocked_libraries": blocked,
            "warnings": warnings,
            "selection_rationale": ordered_unique(rationale),
            "fallback_renderer": fallback_renderer,
            "reproducibility_notes": notes,
        }
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Select a minimal Python render stack for a scientific figure.")
    parser.add_argument("--skill-dir", default=Path(__file__).resolve().parents[1])
    parser.add_argument("--chart-type", default="")
    parser.add_argument("--dataset-profile", default="")
    parser.add_argument("--environment-probe", default="")
    parser.add_argument("--library-pool", default="assets/library_pool/library_pool.json")
    parser.add_argument("--render-registry", default="assets/render_registry/render_registry.json")
    parser.add_argument("--out", default="")
    args = parser.parse_args()
    try:
        skill_dir = Path(args.skill_dir).resolve()
        library_pool_path = skill_dir / args.library_pool
        pool = load_structured_file(library_pool_path)
        pool_libraries(pool)
        registry = load_structured_file(skill_dir / args.render_registry)
        profile = load_structured_file(args.dataset_profile) if args.dataset_profile else None
        environment = load_environment_status(Path(args.environment_probe)) if args.environment_probe else {}
        selection = build_selection(args.chart_type or None, profile, registry, environment)
        if args.out:
            write_json(Path(args.out), selection)
            print(f"[LIBRARY-STACK] wrote {args.out}")
        else:
            print(json.dumps(selection, indent=2, sort_keys=True))
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
