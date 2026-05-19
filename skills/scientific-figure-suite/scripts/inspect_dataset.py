from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

from _common import main_error, write_json
from _memory import utc_now


TABULAR_SUFFIXES = {".csv", ".tsv"}
EXCEL_SUFFIXES = {".xls", ".xlsx"}
GEOJSON_SUFFIXES = {".geojson"}
SHAPEFILE_SUFFIXES = {".shp"}
RASTER_SUFFIXES = {".tif", ".tiff"}
NETCDF_SUFFIXES = {".nc", ".netcdf"}
ANNDATA_SUFFIXES = {".h5ad"}


def import_optional(name: str) -> Any | None:
    try:
        return __import__(name)
    except Exception:
        return None


def shallow_json_columns(value: Any) -> list[str]:
    if isinstance(value, list) and value and isinstance(value[0], dict):
        keys: set[str] = set()
        for row in value[:20]:
            if isinstance(row, dict):
                keys.update(str(key) for key in row)
        return sorted(keys)
    if isinstance(value, dict):
        for candidate in ["data", "records", "rows"]:
            if isinstance(value.get(candidate), list):
                return shallow_json_columns(value[candidate])
    return []


def bbox_from_coords(coords: Any, acc: list[float]) -> None:
    if isinstance(coords, list) and coords and all(isinstance(item, (int, float)) for item in coords[:2]):
        acc[0] = min(acc[0], float(coords[0]))
        acc[1] = min(acc[1], float(coords[1]))
        acc[2] = max(acc[2], float(coords[0]))
        acc[3] = max(acc[3], float(coords[1]))
        return
    if isinstance(coords, list):
        for item in coords:
            bbox_from_coords(item, acc)


def inspect_csv(path: Path) -> dict[str, Any]:
    pandas = import_optional("pandas")
    delimiter = "\t" if path.suffix.lower() == ".tsv" else ","
    if pandas is not None:
        frame = pandas.read_csv(path, sep=delimiter)
        return {
            "path": str(path),
            "format": path.suffix.lower().lstrip("."),
            "rows": int(len(frame)),
            "columns": [str(item) for item in frame.columns],
            "dtypes": {str(key): str(value) for key, value in frame.dtypes.items()},
            "missing_counts": {str(key): int(value) for key, value in frame.isna().sum().items()},
            "requires_library": None,
        }
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=delimiter)
        rows = sum(1 for _ in reader)
        columns = reader.fieldnames or []
    return {
        "path": str(path),
        "format": path.suffix.lower().lstrip("."),
        "rows": rows,
        "columns": columns,
        "dtypes": {},
        "missing_counts": {},
        "requires_library": "pandas_for_full_profile",
    }


def inspect_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(value, dict) and value.get("type") == "FeatureCollection":
        return inspect_geojson_value(path, value)
    columns = shallow_json_columns(value)
    return {
        "path": str(path),
        "format": "json",
        "rows": len(value) if isinstance(value, list) else None,
        "columns": columns,
        "dtypes": {},
        "missing_counts": {},
        "requires_library": None,
    }


def inspect_excel(path: Path) -> dict[str, Any]:
    pandas = import_optional("pandas")
    if pandas is None:
        return {"path": str(path), "format": "excel", "requires_library": "pandas_openpyxl", "columns": []}
    frame = pandas.read_excel(path, nrows=200)
    return {
        "path": str(path),
        "format": "excel",
        "rows_profiled": int(len(frame)),
        "columns": [str(item) for item in frame.columns],
        "dtypes": {str(key): str(value) for key, value in frame.dtypes.items()},
        "missing_counts": {str(key): int(value) for key, value in frame.isna().sum().items()},
        "requires_library": None,
    }


def inspect_geojson_value(path: Path, value: dict[str, Any]) -> dict[str, Any]:
    features = value.get("features", [])
    geometry_types: set[str] = set()
    bbox = [float("inf"), float("inf"), float("-inf"), float("-inf")]
    for feature in features if isinstance(features, list) else []:
        geometry = feature.get("geometry") if isinstance(feature, dict) else None
        if isinstance(geometry, dict):
            geometry_types.add(str(geometry.get("type")))
            bbox_from_coords(geometry.get("coordinates"), bbox)
    bbox_value = None if bbox[0] == float("inf") else bbox
    return {
        "path": str(path),
        "format": "geojson",
        "feature_count": len(features) if isinstance(features, list) else None,
        "geometry_types": sorted(geometry_types),
        "bbox": bbox_value,
        "columns": [],
        "requires_library": None,
    }


def inspect_geojson(path: Path) -> dict[str, Any]:
    return inspect_geojson_value(path, json.loads(path.read_text(encoding="utf-8")))


def inspect_shapefile(path: Path) -> dict[str, Any]:
    geopandas = import_optional("geopandas")
    if geopandas is None:
        return {"path": str(path), "format": "shapefile", "requires_library": "geopandas", "columns": []}
    try:
        frame = geopandas.read_file(path)
    except Exception as exc:
        return {"path": str(path), "format": "shapefile", "requires_library": "valid_geospatial_file", "profile_error": str(exc), "columns": []}
    return {
        "path": str(path),
        "format": "shapefile",
        "feature_count": int(len(frame)),
        "columns": [str(item) for item in frame.columns],
        "crs": str(frame.crs) if frame.crs else None,
        "geometry_types": sorted(str(item) for item in frame.geometry.geom_type.dropna().unique()),
        "requires_library": None,
    }


def inspect_raster(path: Path) -> dict[str, Any]:
    rasterio = import_optional("rasterio")
    if rasterio is None:
        return {"path": str(path), "format": "geotiff", "requires_library": "rasterio", "columns": []}
    try:
        with rasterio.open(path) as src:
            return {
                "path": str(path),
                "format": "geotiff",
                "width": int(src.width),
                "height": int(src.height),
                "count": int(src.count),
                "crs": str(src.crs) if src.crs else None,
                "bounds": list(src.bounds),
                "requires_library": None,
            }
    except Exception as exc:
        return {"path": str(path), "format": "geotiff", "requires_library": "valid_geotiff", "profile_error": str(exc), "columns": []}


def inspect_netcdf(path: Path) -> dict[str, Any]:
    xarray = import_optional("xarray")
    if xarray is None:
        return {"path": str(path), "format": "netcdf", "requires_library": "xarray", "columns": []}
    try:
        dataset = xarray.open_dataset(path)
    except Exception as exc:
        return {"path": str(path), "format": "netcdf", "requires_library": "valid_netcdf", "profile_error": str(exc), "columns": []}
    try:
        return {
            "path": str(path),
            "format": "netcdf",
            "variables": sorted(str(item) for item in dataset.data_vars),
            "coordinates": sorted(str(item) for item in dataset.coords),
            "dimensions": {str(key): int(value) for key, value in dataset.sizes.items()},
            "requires_library": None,
        }
    finally:
        dataset.close()


def inspect_anndata(path: Path) -> dict[str, Any]:
    anndata = import_optional("anndata")
    if anndata is None:
        return {"path": str(path), "format": "h5ad", "requires_library": "anndata", "columns": []}
    try:
        adata = anndata.read_h5ad(path, backed="r")
    except Exception as exc:
        return {"path": str(path), "format": "h5ad", "requires_library": "valid_h5ad", "profile_error": str(exc), "columns": []}
    try:
        return {
            "path": str(path),
            "format": "h5ad",
            "n_obs": int(adata.n_obs),
            "n_vars": int(adata.n_vars),
            "obs_columns": [str(item) for item in adata.obs.columns],
            "var_columns": [str(item) for item in adata.var.columns],
            "requires_library": None,
        }
    finally:
        if getattr(adata, "file", None) is not None:
            adata.file.close()


def inspect_path(path: Path) -> dict[str, Any]:
    suffix = path.suffix.lower()
    if not path.exists():
        return {"path": str(path), "format": "missing", "error": "file_missing", "columns": []}
    if suffix in TABULAR_SUFFIXES:
        return inspect_csv(path)
    if suffix == ".json":
        return inspect_json(path)
    if suffix in GEOJSON_SUFFIXES:
        return inspect_geojson(path)
    if suffix in EXCEL_SUFFIXES:
        return inspect_excel(path)
    if suffix in SHAPEFILE_SUFFIXES:
        return inspect_shapefile(path)
    if suffix in RASTER_SUFFIXES:
        return inspect_raster(path)
    if suffix in NETCDF_SUFFIXES:
        return inspect_netcdf(path)
    if suffix in ANNDATA_SUFFIXES:
        return inspect_anndata(path)
    return {"path": str(path), "format": suffix.lstrip(".") or "unknown", "requires_library": None, "columns": []}


def derive_domains(files: list[dict[str, Any]]) -> tuple[list[str], list[str], list[str]]:
    domains: set[str] = set()
    chart_families: set[str] = set()
    questions: list[str] = []
    for item in files:
        fmt = item.get("format")
        rows = item.get("rows") or item.get("feature_count") or 0
        if fmt in {"csv", "tsv", "json", "excel"}:
            domains.add("tabular")
            chart_families.update(["scatter", "line", "distribution", "bar"])
        if isinstance(rows, int) and rows > 1000000:
            domains.add("large-data")
            chart_families.add("large-time-series")
        if fmt in {"geojson", "shapefile"}:
            domains.add("geospatial-vector")
            chart_families.update(["choropleth", "vector-map"])
            questions.append("Does the map require contextual basemap or administrative boundary data?")
        if fmt == "geotiff":
            domains.add("geospatial-raster")
            chart_families.add("raster-map")
            questions.append("Does the raster need external boundary, basemap, or projection context?")
        if fmt == "netcdf":
            domains.add("climate-netcdf")
            chart_families.update(["gridded-map", "time-series"])
        if fmt == "h5ad":
            domains.add("omics")
            chart_families.update(["umap", "heatmap", "dotplot"])
            questions.append("Does the omics figure require external ontology, pathway, or gene-set annotations?")
    if not domains:
        domains.add("unknown")
    return sorted(domains), sorted(chart_families), questions


def inspect_dataset(paths: list[Path]) -> dict[str, Any]:
    files = [inspect_path(path.resolve()) for path in paths]
    formats = sorted({str(item.get("format")) for item in files})
    domains, chart_families, questions = derive_domains(files)
    return {
        "dataset_profile": {
            "created_at": utc_now(),
            "files": files,
            "detected_formats": formats,
            "suggested_domains": domains,
            "candidate_chart_families": chart_families,
            "external_data_questions": questions,
        }
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect user-provided dataset files for figure planning.")
    parser.add_argument("--input", action="append", required=True, help="Dataset path. May be repeated.")
    parser.add_argument("--out", default="")
    args = parser.parse_args()
    try:
        profile = inspect_dataset([Path(item) for item in args.input])
        if args.out:
            write_json(Path(args.out), profile)
            print(f"[DATASET-PROFILE] wrote {args.out}")
        else:
            print(json.dumps(profile, indent=2, sort_keys=True))
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
