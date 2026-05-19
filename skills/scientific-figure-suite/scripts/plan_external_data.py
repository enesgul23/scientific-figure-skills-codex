from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from _common import load_structured_file, main_error, parse_csv_arg, write_json
from _memory import utc_now


def dataset_domains(dataset_profile_path: str) -> list[str]:
    if not dataset_profile_path:
        return []
    data = load_structured_file(dataset_profile_path)
    root = data.get("dataset_profile", data) if isinstance(data, dict) else {}
    return [str(item) for item in root.get("suggested_domains", [])] if isinstance(root, dict) else []


def make_item(
    usage_role: str,
    data_kind: str,
    justification: str,
    status: str,
    source_name: str | None = None,
    source_url: str | None = None,
    license_name: str | None = None,
    citation: str | None = None,
    contamination_risk: str = "none",
) -> dict[str, Any]:
    return {
        "usage_role": usage_role,
        "data_kind": data_kind,
        "scientific_justification": justification,
        "source_name": source_name,
        "source_url": source_url,
        "license": license_name,
        "citation": citation,
        "accessed_at": None,
        "sha256": None,
        "status": status,
        "contamination_risk": contamination_risk,
    }


def plan_external_data(
    chart_type: str | None,
    domains: list[str],
    goal: str,
    requested_roles: list[str],
    source_name: str | None,
    source_url: str | None,
    license_name: str | None,
    citation: str | None,
) -> dict[str, Any]:
    goal_lower = goal.lower()
    chart_lower = (chart_type or "").lower()
    roles = set(requested_roles)
    items: list[dict[str, Any]] = []
    risks: list[str] = []
    blockers: list[str] = []

    geospatial_need = (
        "geospatial" in chart_lower
        or "map" in chart_lower
        or "choropleth" in chart_lower
        or any(domain in {"geospatial-vector", "geospatial-raster"} for domain in domains)
        or "basemap" in goal_lower
        or "boundary" in goal_lower
    )
    validation_need = "external validation" in goal_lower or "benchmark" in goal_lower or "independent validation" in goal_lower
    omics_annotation_need = (
        "pathway" in goal_lower
        or "ontology" in goal_lower
        or "gene set" in goal_lower
        or "annotation" in roles
        or "omics" in domains
    )

    if geospatial_need:
        items.append(
            make_item(
                "contextual",
                "basemap_or_boundary",
                "Spatial context can improve map interpretation when boundaries, coastline, or basemap context are scientifically relevant.",
                "ready_for_user_approval" if source_url and license_name and citation else "needs_user_source",
                source_name,
                source_url,
                license_name,
                citation,
                "none",
            )
        )
        risks.append("Basemap and boundary layers are contextual unless the figure claim depends on them.")
    if validation_need:
        items.append(
            make_item(
                "benchmark",
                "external_validation_dataset",
                "External benchmark data may test generalization, but must be isolated from training, tuning, and internal validation.",
                "ready_for_user_approval" if source_url and license_name and citation else "needs_user_source",
                source_name,
                source_url,
                license_name,
                citation,
                "high",
            )
        )
        risks.append("External validation data can create train/validation/test contamination if provenance and split boundaries are unclear.")
    if omics_annotation_need:
        items.append(
            make_item(
                "annotation",
                "ontology_pathway_or_gene_set",
                "Annotation data may be required to label biological pathways, gene sets, cell types, or reference metadata.",
                "ready_for_user_approval" if source_url and license_name and citation else "needs_user_source",
                source_name,
                source_url,
                license_name,
                citation,
                "low",
            )
        )
        risks.append("Annotation datasets require citation, version, and license tracking.")

    if not items:
        decision = "NOT_REQUIRED"
        approval_required = False
    else:
        missing_provenance = [item for item in items if item["status"] == "needs_user_source"]
        if missing_provenance:
            decision = "BLOCKED_PENDING_SOURCE"
            blockers.append("External data cannot be downloaded or used until source, license, and citation are specified.")
        else:
            decision = "RECOMMENDED_WITH_APPROVAL"
        approval_required = True

    return {
        "data_acquisition_plan": {
            "created_at": utc_now(),
            "chart_type": chart_type,
            "detected_domains": domains,
            "decision": decision,
            "approval_required": approval_required,
            "download_allowed": False,
            "items": items,
            "risks": risks,
            "blockers": blockers,
            "policy": "No internet data download without explicit user approval and complete provenance.",
        }
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Plan external data needs for a scientific figure without downloading data.")
    parser.add_argument("--chart-type", default="")
    parser.add_argument("--dataset-profile", default="")
    parser.add_argument("--goal", default="")
    parser.add_argument("--role", action="append", default=[], help="Requested external data role. May be repeated or comma-separated.")
    parser.add_argument("--source-name", default="")
    parser.add_argument("--source-url", default="")
    parser.add_argument("--license", default="")
    parser.add_argument("--citation", default="")
    parser.add_argument("--out", default="")
    args = parser.parse_args()
    try:
        roles = []
        for raw in args.role:
            roles.extend(parse_csv_arg(raw))
        plan = plan_external_data(
            args.chart_type or None,
            dataset_domains(args.dataset_profile),
            args.goal,
            roles,
            args.source_name or None,
            args.source_url or None,
            args.license or None,
            args.citation or None,
        )
        if args.out:
            write_json(Path(args.out), plan)
            print(f"[EXTERNAL-DATA-PLAN] wrote {args.out}")
        else:
            print(json.dumps(plan, indent=2, sort_keys=True))
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
