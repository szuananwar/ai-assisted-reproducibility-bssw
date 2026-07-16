from __future__ import annotations

import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
results_path = ROOT / "benchmark/results/phase5_benchmark_results.csv"
rows = list(csv.DictReader(results_path.open(encoding="utf-8")))

numeric_fields = [
    "presence_percent", "quality_percent", "readme_quality",
    "dependency_quality", "container_quality", "test_quality",
    "provenance_quality", "file_count", "elapsed_seconds"
]

overall = {}
for field in numeric_fields:
    values = [float(row[field]) for row in rows if row[field] not in ("", "None")]
    overall[field] = {
        "count": len(values),
        "mean": round(statistics.mean(values), 2),
        "median": round(statistics.median(values), 2),
        "min": round(min(values), 2),
        "max": round(max(values), 2),
        "stdev": round(statistics.stdev(values), 2) if len(values) > 1 else 0.0,
    }

by_domain = defaultdict(list)
for row in rows:
    by_domain[row["domain"]].append(row)

domain_stats = {}
for domain, items in sorted(by_domain.items()):
    domain_stats[domain] = {}
    for field in ["presence_percent", "quality_percent"]:
        values = [float(item[field]) for item in items]
        domain_stats[domain][field] = {
            "count": len(values),
            "mean": round(statistics.mean(values), 2),
            "median": round(statistics.median(values), 2),
        }

out = ROOT / "benchmark/results"
(out / "phase5_descriptive_statistics.json").write_text(
    json.dumps({"overall": overall, "by_domain": domain_stats}, indent=2),
    encoding="utf-8"
)

lines = [
    "# Phase 5.1 Descriptive Statistics",
    "",
    "## Domain summary",
    "",
    "| Domain | N | Mean Presence | Mean Quality | Median Quality |",
    "|---|---:|---:|---:|---:|",
]
for domain, stats in domain_stats.items():
    lines.append(
        f"| {domain} | {stats['quality_percent']['count']} | "
        f"{stats['presence_percent']['mean']}% | "
        f"{stats['quality_percent']['mean']}% | "
        f"{stats['quality_percent']['median']}% |"
    )

(out / "phase5_descriptive_statistics.md").write_text(
    "\n".join(lines), encoding="utf-8"
)
print("Created Phase 5 descriptive statistics.")
