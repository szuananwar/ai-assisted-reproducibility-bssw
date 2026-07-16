from __future__ import annotations
from pathlib import Path
import csv, json, statistics, sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from checker.reproducibility_checker import assess_repository
from checker.quality_assessor import assess_repository_quality
from checker.grounded_ai import build_grounded_ai_evidence, grounded_llm_recommendations, compare_priority_rankings

MANIFEST = ROOT / "benchmark/repositories.csv"
WORKDIR = ROOT / "benchmark/repos"
OUT = ROOT / "analysis"
OUT.mkdir(exist_ok=True)

def slugify(name):
    return "".join(c.lower() if c.isalnum() else "-" for c in name).strip("-")

def prf(det_labels, ai_labels):
    det, ai = set(det_labels), set(ai_labels)
    tp = len(det & ai)
    precision = tp / len(ai) if ai else 0.0
    recall = tp / len(det) if det else 0.0
    f1 = 2*precision*recall/(precision+recall) if precision+recall else 0.0
    return precision, recall, f1

repos = list(csv.DictReader(MANIFEST.open(encoding="utf-8")))
rows, details, failures = [], [], []

for i, repo in enumerate(repos, 1):
    name = repo["name"]
    path = WORKDIR / slugify(name)
    print(f"[{i}/{len(repos)}] {name}")
    if not path.exists():
        failures.append({"repository": name, "error": "Repository clone not found"})
        continue
    try:
        hpc_applicable = repo["hpc_applicable"].strip().lower() == "true"
        presence = assess_repository(path)
        quality = assess_repository_quality(path, hpc_applicable=hpc_applicable)
        evidence = build_grounded_ai_evidence(presence, quality)
        ai_result = grounded_llm_recommendations(evidence)

        det_labels = [x["label"] for x in quality.get("priority_actions", [])]
        ai_labels = [x["label"] for x in ai_result.get("recommendations", [])] if ai_result.get("ok") else []
        comparison = compare_priority_rankings(quality.get("priority_actions", []), ai_result) if ai_result.get("ok") else {
            "overlap_labels": [], "top3_overlap_count": 0, "jaccard_similarity": 0.0
        }
        precision, recall, f1 = prf(det_labels, ai_labels)
        top1 = int(bool(det_labels) and bool(ai_labels) and det_labels[0] == ai_labels[0])

        row = {
            "repository": name,
            "domain": repo["domain"],
            "ai_valid": bool(ai_result.get("ok")),
            "top1_agreement": top1,
            "top3_overlap_count": comparison["top3_overlap_count"],
            "jaccard_similarity": comparison["jaccard_similarity"],
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
            "deterministic_priority_1": det_labels[0] if det_labels else "",
            "ai_priority_1": ai_labels[0] if ai_labels else "",
        }
        rows.append(row)
        details.append({**row, "deterministic_labels": det_labels, "ai_labels": ai_labels, "overlap_labels": comparison["overlap_labels"], "ai_result": ai_result})
    except Exception as exc:
        failures.append({"repository": name, "error": f"{type(exc).__name__}: {exc}"})

if not rows:
    raise RuntimeError("No AI agreement results generated.")

with (OUT / "phase53a_ai_agreement_results.csv").open("w", newline="", encoding="utf-8") as h:
    w = csv.DictWriter(h, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)

(OUT / "phase53a_ai_agreement_results.json").write_text(json.dumps(details, indent=2), encoding="utf-8")
(OUT / "phase53a_ai_agreement_failures.json").write_text(json.dumps(failures, indent=2), encoding="utf-8")

valid = [r for r in rows if r["ai_valid"]]
summary = {
    "repositories_requested": len(repos),
    "repositories_with_valid_ai": len(valid),
    "repositories_failed_or_invalid": len(repos)-len(valid),
    "top1_agreement_rate": statistics.mean([r["top1_agreement"] for r in valid]) if valid else 0.0,
    "mean_top3_overlap_count": statistics.mean([r["top3_overlap_count"] for r in valid]) if valid else 0.0,
    "mean_jaccard_similarity": statistics.mean([r["jaccard_similarity"] for r in valid]) if valid else 0.0,
    "mean_precision": statistics.mean([r["precision"] for r in valid]) if valid else 0.0,
    "mean_recall": statistics.mean([r["recall"] for r in valid]) if valid else 0.0,
    "mean_f1": statistics.mean([r["f1"] for r in valid]) if valid else 0.0,
}
(OUT / "phase53a_ai_agreement_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

report = f"""# Phase 5.3A AI vs. Deterministic Agreement

- Repositories requested: **{summary['repositories_requested']}**
- Valid grounded-AI outputs: **{summary['repositories_with_valid_ai']}**
- Invalid or failed AI outputs: **{summary['repositories_failed_or_invalid']}**
- Top-1 agreement rate: **{summary['top1_agreement_rate']:.3f}**
- Mean Top-3 overlap count: **{summary['mean_top3_overlap_count']:.3f}**
- Mean Jaccard similarity: **{summary['mean_jaccard_similarity']:.3f}**
- Mean precision: **{summary['mean_precision']:.3f}**
- Mean recall: **{summary['mean_recall']:.3f}**
- Mean F1: **{summary['mean_f1']:.3f}**

AI recommendations are accepted only when they use exact deterministic finding labels and cite repository evidence.
"""
(OUT / "phase53a_ai_agreement_report.md").write_text(report, encoding="utf-8")
print("Created Phase 5.3A AI agreement outputs.")
