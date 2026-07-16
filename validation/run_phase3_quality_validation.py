from __future__ import annotations
import csv, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from checker.reproducibility_checker import assess_repository
from checker.quality_assessor import assess_repository_quality

repos = [
    ("BuildTest", ROOT / "validation/repos/buildtest"),
    ("NumPy", ROOT / "validation/repos/numpy"),
    ("Brain Tumor Viskores ViT", ROOT / "validation/repos/brain-tumor-viskores-vit"),
]

rows = []
details = []
for name, path in repos:
    if not path.exists():
        print(f"Skipping missing repository: {path}")
        continue
    presence = assess_repository(path)
    quality = assess_repository_quality(path)
    row = {
        "repository": name,
        "presence_percent": presence["percent"],
        "quality_percent": quality["quality_percent"],
        "quality_band": quality["quality_band"],
    }
    rows.append(row)
    details.append({"repository": name, "presence": presence, "quality": quality})

out = ROOT / "validation"
with (out / "phase3_quality_results.csv").open("w", newline="", encoding="utf-8") as h:
    w = csv.DictWriter(h, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)

(out / "phase3_quality_results.json").write_text(json.dumps(details, indent=2), encoding="utf-8")

lines = [
    "# Phase 3: Presence vs. Quality Assessment",
    "",
    "| Repository | Artifact Presence | Artifact Quality | Interpretation |",
    "|---|---:|---:|---|",
]
for r in rows:
    lines.append(
        f"| {r['repository']} | {r['presence_percent']}% | "
        f"{r['quality_percent']}% | {r['quality_band']} |"
    )
lines += [
    "",
    "Presence answers whether expected artifacts exist. Quality assessment examines whether those artifacts contain actionable reproducibility information.",
]
(out / "phase3_quality_report.md").write_text("\n".join(lines), encoding="utf-8")
print("Created Phase 3 quality results.")
