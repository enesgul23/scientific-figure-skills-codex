from __future__ import annotations

import argparse
import runpy
from pathlib import Path

from _common import parse_csv_arg


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a Python figure script and export open Matplotlib figures.")
    parser.add_argument("--input", required=True, help="Python script that creates a Matplotlib figure")
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--formats", default="pdf,svg,png")
    parser.add_argument("--dpi", type=int, default=300)
    parser.add_argument("--basename", default="")
    args = parser.parse_args()

    import matplotlib.pyplot as plt

    input_path = Path(args.input)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    runpy.run_path(str(input_path), run_name="__main__")

    figure_numbers = plt.get_fignums()
    if not figure_numbers:
        raise SystemExit("[FAIL] input script did not leave an open Matplotlib figure")

    formats = parse_csv_arg(args.formats)
    basename = args.basename or input_path.stem
    written: list[str] = []
    for index, figure_number in enumerate(figure_numbers, start=1):
        fig = plt.figure(figure_number)
        suffix = "" if len(figure_numbers) == 1 else f"_{index:02d}"
        for fmt in formats:
            output = outdir / f"{basename}{suffix}.{fmt}"
            save_kwargs = {"bbox_inches": "tight", "facecolor": "white"}
            if fmt.lower() in {"png", "tif", "tiff", "jpg", "jpeg"}:
                save_kwargs["dpi"] = args.dpi
            fig.savefig(output, **save_kwargs)
            written.append(str(output))

    for path in written:
        print(f"[PASS] wrote {path}")


if __name__ == "__main__":
    main()
