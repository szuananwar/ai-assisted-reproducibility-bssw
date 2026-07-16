from __future__ import annotations
from pathlib import Path
import csv, json, statistics, sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from checker.quality_assessor import assess_repository_quality
from checker.ai_priority_ranker import ai_priority_labels

MANIFEST = ROOT/"benchmark/repositories.csv"
WORKDIR = ROOT/"benchmark/repos"
OUT = ROOT/"analysis"
OUT.mkdir(exist_ok=True)

def slugify(name):
    return "".join(c.lower() if c.isalnum() else "-" for c in name).strip("-")

def prf(det_labels, ai_labels):
    det, ai = set(det_labels), set(ai_labels)
    tp = len(det & ai)
    precision = tp/len(ai) if ai else 0.0
    recall = tp/len(det) if det else 0.0
    f1 = 2*precision*recall/(precision+recall) if precision+recall else 0.0
    return precision, recall, f1

repos=list(csv.DictReader(MANIFEST.open(encoding="utf-8")))
rows=[]; details=[]

for i, repo in enumerate(repos,1):
    name=repo["name"]; path=WORKDIR/slugify(name)
    print(f"[{i}/{len(repos)}] {name}")
    hpc=repo["hpc_applicable"].strip().lower()=="true"
    quality=assess_repository_quality(path,hpc_applicable=hpc)
    det=[x["label"] for x in quality["priority_actions"]]
    ai_result=ai_priority_labels(quality)
    ai=ai_result.get("priorities",[]) if ai_result.get("ok") else []
    p,r,f1=prf(det,ai)
    overlap=list(dict.fromkeys([x for x in ai if x in det]))
    union=set(det)|set(ai)
    j=len(set(overlap))/len(union) if union else 1.0
    rows.append({
        "repository":name,
        "domain":repo["domain"],
        "ai_valid":bool(ai_result.get("ok")),
        "top1_agreement":int(bool(det) and bool(ai) and det[0]==ai[0]),
        "top3_overlap_count":len(set(overlap)),
        "jaccard_similarity":round(j,4),
        "precision":round(p,4),
        "recall":round(r,4),
        "f1":round(f1,4),
        "deterministic_priorities":" | ".join(det),
        "ai_priorities":" | ".join(ai),
        "error":"" if ai_result.get("ok") else ai_result.get("message","unknown"),
    })
    details.append({"repository":name,"quality":quality,"ai_result":ai_result})

with (OUT/"phase53a_v2_ai_agreement_results.csv").open("w",newline="",encoding="utf-8") as h:
    w=csv.DictWriter(h,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
(OUT/"phase53a_v2_ai_agreement_results.json").write_text(json.dumps(details,indent=2),encoding="utf-8")

valid=[x for x in rows if x["ai_valid"]]
summary={
    "repositories_requested":len(rows),
    "valid_ai_outputs":len(valid),
    "invalid_ai_outputs":len(rows)-len(valid),
    "valid_output_rate":len(valid)/len(rows),
    "top1_agreement_rate":statistics.mean([x["top1_agreement"] for x in valid]) if valid else 0,
    "mean_top3_overlap_count":statistics.mean([x["top3_overlap_count"] for x in valid]) if valid else 0,
    "mean_jaccard_similarity":statistics.mean([x["jaccard_similarity"] for x in valid]) if valid else 0,
    "mean_precision":statistics.mean([x["precision"] for x in valid]) if valid else 0,
    "mean_recall":statistics.mean([x["recall"] for x in valid]) if valid else 0,
    "mean_f1":statistics.mean([x["f1"] for x in valid]) if valid else 0,
}
(OUT/"phase53a_v2_ai_agreement_summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
report=f"""# Phase 5.3A v2 — AI vs. Deterministic Priority Agreement

- Repositories: **{summary['repositories_requested']}**
- Valid AI outputs: **{summary['valid_ai_outputs']}**
- Invalid AI outputs: **{summary['invalid_ai_outputs']}**
- Valid output rate: **{summary['valid_output_rate']:.3f}**
- Top-1 agreement rate: **{summary['top1_agreement_rate']:.3f}**
- Mean Top-3 overlap: **{summary['mean_top3_overlap_count']:.3f}**
- Mean Jaccard similarity: **{summary['mean_jaccard_similarity']:.3f}**
- Mean precision: **{summary['mean_precision']:.3f}**
- Mean recall: **{summary['mean_recall']:.3f}**
- Mean F1: **{summary['mean_f1']:.3f}**

The v2 experiment uses Ollama JSON mode and asks the model only to rank exact allowed finding labels. This avoids conflating JSON-generation ability with prioritization agreement.
"""
(OUT/"phase53a_v2_ai_agreement_report.md").write_text(report,encoding="utf-8")
print("Created Phase 5.3A v2 outputs.")
