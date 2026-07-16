from __future__ import annotations
import csv, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from checker.reproducibility_checker import assess_repository
from checker.quality_assessor import assess_repository_quality
from checker.grounded_ai import (
    build_grounded_ai_evidence,
    grounded_llm_recommendations,
    compare_priority_rankings,
)

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
    evidence = build_grounded_ai_evidence(presence, quality)
    ai_result = grounded_llm_recommendations(evidence)
    comparison = compare_priority_rankings(quality["priority_actions"], ai_result) if ai_result.get("ok") else {
        "deterministic_labels": [x["label"] for x in quality["priority_actions"]],
        "ai_labels": [],
        "overlap_labels": [],
        "top3_overlap_count": 0,
        "jaccard_similarity": 0.0,
    }
    row = {
        "repository": name,
        "quality_percent": quality["quality_percent"],
        "ai_ok": ai_result.get("ok", False),
        "top3_overlap_count": comparison["top3_overlap_count"],
        "jaccard_similarity": comparison["jaccard_similarity"],
    }
    rows.append(row)
    details.append({
        "repository": name,
        "presence": presence,
        "quality": quality,
        "ai_result": ai_result,
        "priority_comparison": comparison,
    })

out = ROOT / "validation"
with (out / "phase4_grounded_ai_results.csv").open("w", newline="", encoding="utf-8") as h:
    writer = csv.DictWriter(h, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

(out / "phase4_grounded_ai_results.json").write_text(json.dumps(details, indent=2), encoding="utf-8")

lines = [
    "# Phase 4: Grounded AI Prioritization",
    "",
    "| Repository | Quality Score | AI Valid | Top-3 Overlap | Jaccard Similarity |",
    "|---|---:|---|---:|---:|",
]
for row in rows:
    lines.append(
        f"| {row['repository']} | {row['quality_percent']}% | "
        f"{row['ai_ok']} | {row['top3_overlap_count']} | {row['jaccard_similarity']} |"
    )

lines += [
    "",
    "The AI layer is accepted only when each recommendation uses an exact deterministic finding label and cites evidence from that finding.",
]
(out / "phase4_grounded_ai_report.md").write_text("\n".join(lines), encoding="utf-8")
print("Created Phase 4 grounded AI results.")
