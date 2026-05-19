from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SKILL_DIR = ROOT / "skills" / "scientific-figure-suite"


COMMANDS = [
    ["scripts/validate_skill.py", "."],
    ["scripts/validate_contracts.py", "."],
    ["scripts/validate_figure_spec.py", "tests/sample_figure_spec.yaml"],
    ["scripts/validate_visual_claim_ledger.py", "tests/sample_visual_claim_ledger.yaml"],
    ["scripts/validate_style_tokens.py"],
    ["scripts/validate_render_template_registry.py"],
    ["scripts/validate_library_pool.py"],
    ["scripts/validate_data_acquisition_plan.py", "templates/data_acquisition_plan_template.json"],
    ["scripts/audit_multipanel_layout.py", "--layout", "tests/sample_multipanel_layout.yaml"],
    ["scripts/validate_memory.py", "--memory-dir", "tests/sample_memory/scientific-figure-memory"],
    ["scripts/audit_repro_lock.py", "--memory-dir", "tests/sample_memory/scientific-figure-memory"],
    ["scripts/build_pipeline_dashboard.py", "--memory-dir", "tests/sample_memory/scientific-figure-memory", "--no-update-manifest"],
    ["scripts/validate_handoff_artifact.py", "tests/sample_figure_intake.yaml", "--type", "figure_intake"],
    ["scripts/validate_handoff_artifact.py", "tests/sample_journal_style_report.yaml", "--type", "journal_style_report"],
    ["scripts/validate_handoff_artifact.py", "tests/sample_caption_package.yaml", "--type", "caption_package"],
    ["scripts/validate_handoff_artifact.py", "tests/sample_quality_report.yaml", "--type", "figure_quality_report"],
    ["scripts/validate_handoff_artifact.py", "tests/sample_submission_manifest.json", "--type", "submission_manifest"],
]


def run_command(command: list[str], env: dict[str, str], expect_success: bool = True) -> tuple[bool, str]:
    display = " ".join(command)
    print(f"[RUN] {display}")
    result = subprocess.run(
        [sys.executable, *command],
        cwd=SKILL_DIR,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    output = "\n".join(part for part in [result.stdout.strip(), result.stderr.strip()] if part)
    if output:
        print(output)
    ok = result.returncode == 0 if expect_success else result.returncode != 0
    if not ok:
        expectation = "success" if expect_success else "failure"
        print(f"[FAIL] expected {expectation} from {display}", file=sys.stderr)
    return ok, output


def write_fixture_csvs(temp_dir: Path) -> dict[str, Path]:
    fixtures = {
        "parity_scatter": (
            "observed,predicted\n"
            "1.0,0.9\n2.0,2.1\n3.0,2.8\n4.0,4.2\n5.0,5.1\n"
        ),
        "roc_pr_curve": (
            "y_true,score\n"
            "1,0.97\n1,0.89\n1,0.73\n1,0.61\n0,0.55\n0,0.41\n0,0.32\n0,0.12\n"
        ),
        "time_series_band": (
            "time,value,lower,upper\n"
            "2026-01-01,10,8,12\n2026-01-02,12,9,14\n2026-01-03,15,12,17\n2026-01-04,13,10,16\n"
        ),
        "raincloud_plot": (
            "group,value\n"
            "A,1.2\nA,1.5\nA,1.8\nA,2.0\nB,2.2\nB,2.4\nB,2.7\nB,2.9\nC,1.7\nC,2.1\nC,2.4\nC,2.8\n"
        ),
    }
    paths: dict[str, Path] = {}
    for chart_type, content in fixtures.items():
        path = temp_dir / f"{chart_type}.csv"
        path.write_text(content, encoding="utf-8")
        paths[chart_type] = path
    return paths


def make_blank_png(path: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(2, 2), dpi=100)
    ax.set_axis_off()
    fig.savefig(path, dpi=100, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def write_multipanel_layouts(temp_dir: Path) -> tuple[Path, Path]:
    good_layout = temp_dir / "multipanel_good.yaml"
    bad_layout = temp_dir / "multipanel_bad.yaml"
    good_layout.write_text(
        (
            "layout_name: smoke_multipanel_good\n"
            "layout_engine: manual_axes\n"
            "manual_axes_fallback: true\n"
            "semantic_color_map:\n"
            "  observed: '#0072B2'\n"
            "  model_a: '#D55E00'\n"
            "canvas:\n"
            "  width_mm: 180\n"
            "  height_mm: 130\n"
            "panels:\n"
            "  - id: a\n"
            "    plot_type: scatter\n"
            "    bbox: {x0: 0.08, y0: 0.56, width: 0.36, height: 0.34}\n"
            "    color_bindings: {observed: '#0072B2', model_a: '#D55E00'}\n"
            "    direct_labels: {count: 2, max_count: 8, policy: controlled, collision_checked: true}\n"
            "  - id: b\n"
            "    plot_type: geospatial_map\n"
            "    bbox: {x0: 0.54, y0: 0.56, width: 0.28, height: 0.34}\n"
            "    color_bindings: {observed: '#0072B2'}\n"
            "    colorbar:\n"
            "      label: Error\n"
            "      short_label: Error\n"
            "      label_overlap_checked: true\n"
            "      label_spacing_checked: true\n"
            "      bbox: {x0: 0.86, y0: 0.58, width: 0.025, height: 0.30}\n"
            "    direct_labels: {count: 0, max_count: 8, policy: controlled, collision_checked: true}\n"
            "  - id: c\n"
            "    plot_type: time_series\n"
            "    bbox: {x0: 0.08, y0: 0.12, width: 0.36, height: 0.34}\n"
            "    color_bindings: {model_a: '#D55E00'}\n"
            "  - id: d\n"
            "    plot_type: forest_plot\n"
            "    bbox: {x0: 0.54, y0: 0.12, width: 0.36, height: 0.34}\n"
        ),
        encoding="utf-8",
    )
    bad_layout.write_text(
        (
            "layout_name: smoke_multipanel_bad\n"
            "layout_engine: constrained_layout\n"
            "semantic_color_map:\n"
            "  observed: '#0072B2'\n"
            "panels:\n"
            "  - id: a\n"
            "    plot_type: scatter\n"
            "    bbox: {x0: 0.08, y0: 0.56, width: 0.40, height: 0.34}\n"
            "    color_bindings: {observed: '#0072B2'}\n"
            "    direct_labels: {count: 18, policy: all, collision_checked: false}\n"
            "  - id: b\n"
            "    plot_type: geospatial_map\n"
            "    bbox: {x0: 0.46, y0: 0.55, width: 0.42, height: 0.30}\n"
            "    color_bindings: {observed: '#D55E00'}\n"
            "    colorbar:\n"
            "      label: Very long hydrologic model residual colorbar label that should be shortened\n"
        ),
        encoding="utf-8",
    )
    return good_layout, bad_layout


def prepare_v04_memory_copy(source: Path, target: Path) -> None:
    shutil.copytree(source, target)
    for filename in [
        "figure_decision_log.jsonl",
        "visual_regression_history.jsonl",
        "multipanel_layout_history.jsonl",
        "dependency_plan_history.jsonl",
        "external_data_plan_history.jsonl",
    ]:
        path = target / filename
        if path.exists():
            path.unlink()
    manifest_path = target / "memory_manifest.json"
    manifest_data = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest = manifest_data["memory_manifest"]
    manifest["schema_version"] = "0.4.0"
    manifest.pop("pipeline_state", None)
    manifest["files"].pop("figure_decision_log", None)
    manifest["files"].pop("visual_regression_history", None)
    manifest["files"].pop("multipanel_layout_history", None)
    manifest["files"].pop("dependency_plan_history", None)
    manifest["files"].pop("external_data_plan_history", None)
    manifest_path.write_text(json.dumps(manifest_data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_runtime_smoke(env: dict[str, str]) -> int:
    failures = 0
    with tempfile.TemporaryDirectory(prefix="sfs-runtime-") as raw_temp:
        temp_dir = Path(raw_temp)
        fixture_csvs = write_fixture_csvs(temp_dir)
        parity_profile = temp_dir / "parity_profile.json"
        env_probe = temp_dir / "environment_probe.json"
        dependency_plan = temp_dir / "dependency_plan.json"

        setup_commands = [
            ["scripts/inspect_dataset.py", "--input", str(fixture_csvs["parity_scatter"]), "--out", str(parity_profile)],
            [
                "scripts/probe_python_environment.py",
                "--library",
                "pandas",
                "--library",
                "numpy",
                "--library",
                "matplotlib",
                "--out",
                str(env_probe),
            ],
            [
                "scripts/select_library_stack.py",
                "--chart-type",
                "parity_scatter",
                "--dataset-profile",
                str(parity_profile),
                "--environment-probe",
                str(env_probe),
                "--out",
                str(temp_dir / "library_stack_selection.json"),
            ],
            [
                "scripts/build_dependency_plan.py",
                "--chart-type",
                "parity_scatter",
                "--dataset-profile",
                str(parity_profile),
                "--environment-probe",
                str(env_probe),
                "--out",
                str(dependency_plan),
            ],
        ]
        for command in setup_commands:
            ok, _ = run_command(command, env)
            failures += 0 if ok else 1

        geojson = temp_dir / "study_area.geojson"
        geojson.write_text(
            '{"type":"FeatureCollection","features":[{"type":"Feature","properties":{"id":1},'
            '"geometry":{"type":"Polygon","coordinates":[[[0,0],[1,0],[1,1],[0,1],[0,0]]]}}]}',
            encoding="utf-8",
        )
        for dataset_path, payload in [
            (geojson, None),
            (temp_dir / "raster_mock.tif", b"mock geotiff metadata fixture"),
            (temp_dir / "climate_mock.nc", b"mock netcdf metadata fixture"),
            (temp_dir / "omics_mock.h5ad", b"mock h5ad metadata fixture"),
        ]:
            if payload is not None:
                dataset_path.write_bytes(payload)
            ok, _ = run_command(
                ["scripts/inspect_dataset.py", "--input", str(dataset_path), "--out", str(temp_dir / f"{dataset_path.stem}_profile.json")],
                env,
            )
            failures += 0 if ok else 1

        for chart_type in ["clinical_survival", "geospatial_raster_map", "omics_umap", "huge_time_series", "roc_pr_curve"]:
            ok, _ = run_command(["scripts/select_library_stack.py", "--chart-type", chart_type, "--out", str(temp_dir / f"{chart_type}_stack.json")], env)
            failures += 0 if ok else 1

        for chart_type, csv_path in fixture_csvs.items():
            outdir = temp_dir / chart_type
            dependency_args = ["--dependency-plan", str(dependency_plan)] if chart_type == "parity_scatter" else []
            ok, _ = run_command(
                ["scripts/render_from_registry.py", "--chart-type", chart_type, "--data", str(csv_path), "--outdir", str(outdir), *dependency_args],
                env,
            )
            failures += 0 if ok else 1
            files = [str(outdir / f"{chart_type}.{suffix}") for suffix in ["pdf", "svg", "png"]]
            ok, _ = run_command(
                [
                    "scripts/audit_render_quality.py",
                    "--figure-id",
                    chart_type,
                    "--expected-formats",
                    "pdf,svg,png",
                    *[item for path in files for item in ["--file", path]],
                ],
                env,
            )
            failures += 0 if ok else 1

        blank = temp_dir / "blank.png"
        make_blank_png(blank)
        for command in [
            ["scripts/audit_render_quality.py", "--figure-id", "blank_case", "--file", str(blank)],
            ["scripts/audit_render_quality.py", "--figure-id", "missing_case", "--file", str(temp_dir / "missing.png")],
        ]:
            ok, _ = run_command(command, env, expect_success=False)
            failures += 0 if ok else 1

        good_layout, bad_layout = write_multipanel_layouts(temp_dir)
        ok, _ = run_command(
            ["scripts/audit_multipanel_layout.py", "--layout", str(good_layout), "--out", str(temp_dir / "multipanel_layout_audit.json")],
            env,
        )
        failures += 0 if ok else 1
        ok, _ = run_command(["scripts/audit_multipanel_layout.py", "--layout", str(bad_layout)], env, expect_success=False)
        failures += 0 if ok else 1
        layout_out = temp_dir / "multipanel-proof"
        ok, _ = run_command(["scripts/export_multipanel.py", "--layout", str(good_layout), "--outdir", str(layout_out), "--formats", "png"], env)
        failures += 0 if ok else 1
        ok, _ = run_command(
            ["scripts/audit_render_quality.py", "--figure-id", "multipanel_layout_proof", "--file", str(layout_out / "smoke_multipanel_good.png")],
            env,
        )
        failures += 0 if ok else 1

        external_plan = temp_dir / "external_data_plan.json"
        ok, _ = run_command(
            [
                "scripts/plan_external_data.py",
                "--chart-type",
                "geospatial_choropleth",
                "--goal",
                "need basemap context",
                "--source-name",
                "Natural Earth",
                "--source-url",
                "https://www.naturalearthdata.com/",
                "--license",
                "public domain",
                "--citation",
                "Natural Earth contributors",
                "--out",
                str(external_plan),
            ],
            env,
        )
        failures += 0 if ok else 1
        ok, _ = run_command(["scripts/validate_data_acquisition_plan.py", str(external_plan)], env)
        failures += 0 if ok else 1

        validation_plan = temp_dir / "external_validation_plan.json"
        ok, _ = run_command(
            [
                "scripts/plan_external_data.py",
                "--chart-type",
                "roc_pr_curve",
                "--goal",
                "external validation benchmark requested",
                "--source-name",
                "User-supplied external test set",
                "--source-url",
                "https://example.org/external-test-set",
                "--license",
                "user provided",
                "--citation",
                "User-provided benchmark citation",
                "--out",
                str(validation_plan),
            ],
            env,
        )
        failures += 0 if ok else 1
        ok, _ = run_command(["scripts/validate_data_acquisition_plan.py", str(validation_plan)], env)
        failures += 0 if ok else 1

        no_external_plan = temp_dir / "no_external_data_plan.json"
        ok, _ = run_command(
            ["scripts/plan_external_data.py", "--chart-type", "parity_scatter", "--goal", "plot supplied predictions", "--out", str(no_external_plan)],
            env,
        )
        failures += 0 if ok else 1
        ok, _ = run_command(["scripts/validate_data_acquisition_plan.py", str(no_external_plan)], env)
        failures += 0 if ok else 1

        invalid_external_plan = temp_dir / "invalid_external_data_plan.json"
        invalid_external_plan.write_text(
            json.dumps(
                {
                    "data_acquisition_plan": {
                        "created_at": "2026-05-19T16:30:00Z",
                        "decision": "RECOMMENDED_WITH_APPROVAL",
                        "approval_required": True,
                        "download_allowed": False,
                        "items": [
                            {
                                "usage_role": "benchmark",
                                "data_kind": "external_validation_dataset",
                                "scientific_justification": "Needed for independent benchmark.",
                                "source_name": "Unspecified",
                                "source_url": None,
                                "license": None,
                                "citation": None,
                                "accessed_at": None,
                                "sha256": None,
                                "status": "ready_for_user_approval",
                                "contamination_risk": "high",
                            }
                        ],
                        "risks": [],
                        "blockers": [],
                    }
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        ok, _ = run_command(["scripts/validate_data_acquisition_plan.py", str(invalid_external_plan)], env, expect_success=False)
        failures += 0 if ok else 1

        memory_copy = temp_dir / "memory-v04"
        prepare_v04_memory_copy(SKILL_DIR / "tests" / "sample_memory" / "scientific-figure-memory", memory_copy)
        for command in [
            ["scripts/migrate_memory.py", "--memory-dir", str(memory_copy)],
            ["scripts/validate_memory.py", "--memory-dir", str(memory_copy)],
            ["scripts/build_pipeline_dashboard.py", "--memory-dir", str(memory_copy), "--no-update-manifest"],
        ]:
            ok, _ = run_command(command, env)
            failures += 0 if ok else 1
        (memory_copy / "visual_regression_history.jsonl").write_text(
            '{"visual_regression_report":{"baseline_dir":null,"blockers":["forced visual regression failure"],"created_at":"2026-05-19T16:30:00Z","figure_id":"fig_01","files":[],"result":"FAIL","warnings":[]}}\n',
            encoding="utf-8",
        )
        ok, output = run_command(
            ["scripts/audit_submission_readiness.py", "--memory-dir", str(memory_copy), "--allow-unverified-journal"],
            env,
            expect_success=False,
        )
        if ok and "latest visual regression/render-quality audit failed" in output:
            print("[PASS] readiness blocks on failed visual regression")
        else:
            print("[FAIL] readiness did not expose failed visual regression blocker", file=sys.stderr)
            failures += 1
        (memory_copy / "visual_regression_history.jsonl").write_text(
            '{"visual_regression_report":{"baseline_dir":null,"blockers":[],"created_at":"2026-05-20T08:30:00Z","figure_id":"fig_01","files":[],"result":"PASS","warnings":[]}}\n',
            encoding="utf-8",
        )
        (memory_copy / "multipanel_layout_history.jsonl").write_text(
            '{"multipanel_layout_audit":{"blockers":["forced multipanel layout failure"],"checks":[],"colorbar_count":1,"created_at":"2026-05-20T08:30:00Z","layout_engine":"constrained_layout","layout_name":"forced_failure","panel_count":2,"result":"FAIL","warnings":[]}}\n',
            encoding="utf-8",
        )
        ok, output = run_command(
            ["scripts/audit_submission_readiness.py", "--memory-dir", str(memory_copy), "--allow-unverified-journal"],
            env,
            expect_success=False,
        )
        if ok and "latest multipanel layout audit failed" in output:
            print("[PASS] readiness blocks on failed multipanel layout audit")
        else:
            print("[FAIL] readiness did not expose failed multipanel layout blocker", file=sys.stderr)
            failures += 1
    return failures


def main() -> int:
    if not SKILL_DIR.is_dir():
        print(f"[FAIL] skill directory not found: {SKILL_DIR}", file=sys.stderr)
        return 2

    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"

    failures = 0
    for command in COMMANDS:
        ok, _ = run_command(command, env)
        failures += 0 if ok else 1
    failures += run_runtime_smoke(env)

    if failures:
        print(f"[FAIL] {failures} validation command(s) failed", file=sys.stderr)
        return 1
    print("[PASS] all validation commands passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
