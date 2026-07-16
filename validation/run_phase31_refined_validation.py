from __future__ import annotations
import csv, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from checker.reproducibility_checker import assess_repository
from checker.quality_assessor import assess_repository_quality

repos = [
    ("BuildTest", ROOT / "validation/repos/buildtest", True),
    ("NumPy", ROOT / "validation/repos/numpy", False),
    ("Brain Tumor Viskores ViT", ROOT / "validation/repos/brain-tumor-viskores-vit", True),
]

rows, details = [], []
for name, path, hpc_applicable in repos:
    if not path.exists():
        print(f"Skipping missing repository: {path}")
        continue
    presence = assess_repository(path)
    quality = assess_repository_quality(path, hpc_applicable=hpc_applicable)
    row = {
        "repository": name,
        "presence_percent": presence["percent"],
        "quality_percent": quality["quality_percent"],
        "quality_possible": quality["quality_possible"],
        "quality_band": quality["quality_band"],
        "hpc_applicable": hpc_applicable,
    }
    rows.append(row)
    details.append({"repository": name, "presence": presence, "quality": quality})

out = ROOT / "validation"
with (out / "phase31_quality_results.csv").open("w", newline="", encoding="utf-8") as h:
    writer = csv.DictWriter(h, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

(out / "phase31_quality_results.json").write_text(json.dumps(details, indent=2), encoding="utf-8")

lines = [
    "# Phase 3.1: Refined Quality Assessment",
    "",
    "| Repository | Presence | Refined Quality | Denominator | HPC Applicable | Interpretation |",
    "|---|---:|---:|---:|---|---|",
]
for row in rows:
    lines.append(
        f"| {row['repository']} | {row['presence_percent']}% | "
        f"{row['quality_percent']}% | {row['quality_possible']} | "
        f"{row['hpc_applicable']} | {row['quality_band']} |"
    )

lines += [
    "",
    "Phase 3.1 adds recursive discovery, broader artifact names, CI detection, and not-applicable handling to reduce false negatives.",
]
(out / "phase31_quality_report.md").write_text("\n".join(lines), encoding="utf-8")
print("Created Phase 3.1 refined quality results.")
