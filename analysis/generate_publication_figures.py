from __future__ import annotations

from pathlib import Path
import json
import math

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
BENCHMARK = ROOT / "benchmark/results/phase5_benchmark_results.csv"
DOMAIN_SUMMARY = ROOT / "analysis/phase53_domain_summary.csv"
AI_SUMMARY = ROOT / "analysis/phase53a_v2_ai_agreement_summary.json"
AI_RESULTS = ROOT / "analysis/phase53a_v2_ai_agreement_results.csv"
OUT = ROOT / "analysis/figures"
TABLES = ROOT / "analysis/publication_tables"

OUT.mkdir(parents=True, exist_ok=True)
TABLES.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(BENCHMARK)
domain_summary = pd.read_csv(DOMAIN_SUMMARY)
ai_summary = json.loads(AI_SUMMARY.read_text(encoding="utf-8"))
ai_results = pd.read_csv(AI_RESULTS)

def save(fig, stem):
    fig.tight_layout()
    fig.savefig(OUT / f"{stem}.png", dpi=300, bbox_inches="tight")
    fig.savefig(OUT / f"{stem}.pdf", bbox_inches="tight")
    plt.close(fig)

# Figure 1: architecture
fig, ax = plt.subplots(figsize=(10, 2.6))
ax.axis("off")
labels = [
    "GitHub repository",
    "Presence assessment",
    "Quality assessment",
    "Grounded AI ranking",
    "Agreement evaluation",
    "Reports & recommendations",
]
x = np.linspace(0.07, 0.93, len(labels))
for i, (xi, label) in enumerate(zip(x, labels)):
    ax.text(
        xi, 0.5, label, ha="center", va="center",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="black")
    )
    if i < len(labels) - 1:
        ax.annotate("", xy=(x[i+1]-0.07, 0.5), xytext=(xi+0.07, 0.5),
                    arrowprops=dict(arrowstyle="->", lw=1.5))
ax.set_title("ReproPilot architecture")
save(fig, "figure1_architecture")

# Figure 2: benchmark workflow
fig, ax = plt.subplots(figsize=(9, 2.5))
ax.axis("off")
labels = ["30 repositories", "Clone", "Presence score", "Quality score", "Grounded AI", "Statistics"]
x = np.linspace(0.08, 0.92, len(labels))
for i, (xi, label) in enumerate(zip(x, labels)):
    ax.text(
        xi, 0.5, label, ha="center", va="center",
        bbox=dict(boxstyle="round,pad=0.45", facecolor="white", edgecolor="black")
    )
    if i < len(labels) - 1:
        ax.annotate("", xy=(x[i+1]-0.06, 0.5), xytext=(xi+0.06, 0.5),
                    arrowprops=dict(arrowstyle="->", lw=1.5))
ax.set_title("Benchmark workflow")
save(fig, "figure2_benchmark_workflow")

# Figure 3: domain distribution
counts = df["domain"].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.bar(counts.index, counts.values)
ax.set_ylabel("Repositories")
ax.set_xlabel("Scientific domain")
ax.set_title("Repository distribution by domain")
ax.tick_params(axis="x", rotation=30)
save(fig, "figure3_domain_distribution")

# Figure 4: presence histogram
fig, ax = plt.subplots(figsize=(6, 4.5))
ax.hist(df["presence_percent"], bins=10)
ax.set_xlabel("Presence score (%)")
ax.set_ylabel("Repositories")
ax.set_title("Distribution of artifact-presence scores")
save(fig, "figure4_presence_distribution")

# Figure 5: quality histogram
fig, ax = plt.subplots(figsize=(6, 4.5))
ax.hist(df["quality_percent"], bins=10)
ax.set_xlabel("Quality score (%)")
ax.set_ylabel("Repositories")
ax.set_title("Distribution of quality scores")
save(fig, "figure5_quality_distribution")

# Figure 6: scatter with regression line
xv = df["presence_percent"].to_numpy(dtype=float)
yv = df["quality_percent"].to_numpy(dtype=float)
coef = np.polyfit(xv, yv, 1)
line_x = np.linspace(xv.min(), xv.max(), 100)
line_y = coef[0] * line_x + coef[1]
r = np.corrcoef(xv, yv)[0, 1]

fig, ax = plt.subplots(figsize=(6, 5))
ax.scatter(xv, yv)
ax.plot(line_x, line_y)
ax.set_xlabel("Presence score (%)")
ax.set_ylabel("Quality score (%)")
ax.set_title(f"Presence versus quality (r = {r:.3f})")
save(fig, "figure6_presence_vs_quality")

# Figure 7: quality by domain boxplot
domains = sorted(df["domain"].unique())
vals = [df.loc[df["domain"] == d, "quality_percent"] for d in domains]
fig, ax = plt.subplots(figsize=(8.5, 5))
ax.boxplot(vals, tick_labels=domains)
ax.set_ylabel("Quality score (%)")
ax.set_title("Quality scores by scientific domain")
ax.tick_params(axis="x", rotation=30)
save(fig, "figure7_quality_by_domain")

# Figure 8: category heatmap
category_cols = [
    "readme_quality",
    "dependency_quality",
    "container_quality",
    "test_quality",
    "provenance_quality",
    "hpc_quality",
]
heat = df[category_cols].astype(float).to_numpy()
fig, ax = plt.subplots(figsize=(9, 10))
im = ax.imshow(heat, aspect="auto", vmin=0, vmax=100)
ax.set_yticks(np.arange(len(df)))
ax.set_yticklabels(df["repository"])
ax.set_xticks(np.arange(len(category_cols)))
ax.set_xticklabels(
    ["README", "Dependencies", "Container", "Tests", "Provenance", "HPC"],
    rotation=30, ha="right"
)
ax.set_title("Repository quality signals by category")
fig.colorbar(im, ax=ax, label="Quality score (%)")
save(fig, "figure8_quality_heatmap")

# Figure 9: AI agreement metrics
metric_names = [
    "Top-1 agreement",
    "Jaccard",
    "Precision",
    "Recall",
    "F1",
]
metric_values = [
    ai_summary["top1_agreement_rate"] * 100,
    ai_summary["mean_jaccard_similarity"] * 100,
    ai_summary["mean_precision"] * 100,
    ai_summary["mean_recall"] * 100,
    ai_summary["mean_f1"] * 100,
]
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.bar(metric_names, metric_values)
ax.set_ylabel("Agreement (%)")
ax.set_title("AI versus deterministic priority agreement")
ax.tick_params(axis="x", rotation=25)
save(fig, "figure9_ai_agreement_metrics")

# Figure 10: domain means with 95% CIs
quality_rows = domain_summary[domain_summary["metric"] == "quality_percent"].copy()
quality_rows = quality_rows.sort_values("domain")
means = quality_rows["mean"].to_numpy(dtype=float)
lower = means - quality_rows["ci95_low"].to_numpy(dtype=float)
upper = quality_rows["ci95_high"].to_numpy(dtype=float) - means

fig, ax = plt.subplots(figsize=(8, 4.8))
ax.errorbar(
    quality_rows["domain"], means, yerr=np.vstack([lower, upper]),
    fmt="o", capsize=5
)
ax.set_ylabel("Mean quality score (%)")
ax.set_title("Domain mean quality scores with 95% bootstrap CIs")
ax.tick_params(axis="x", rotation=30)
save(fig, "figure10_domain_confidence_intervals")

# Publication table: domain summary
domain_table = (
    df.groupby("domain")
      .agg(
          n=("repository", "count"),
          mean_presence=("presence_percent", "mean"),
          mean_quality=("quality_percent", "mean"),
          median_quality=("quality_percent", "median"),
      )
      .reset_index()
)
domain_table.to_csv(TABLES / "table1_domain_summary.csv", index=False)
(TABLES / "table1_domain_summary.tex").write_text(
    domain_table.to_latex(index=False, float_format="%.2f"),
    encoding="utf-8",
)

# Publication table: AI agreement summary
ai_table = pd.DataFrame([{
    "valid_output_rate": ai_summary["valid_output_rate"],
    "top1_agreement_rate": ai_summary["top1_agreement_rate"],
    "mean_top3_overlap_count": ai_summary["mean_top3_overlap_count"],
    "mean_jaccard_similarity": ai_summary["mean_jaccard_similarity"],
    "mean_precision": ai_summary["mean_precision"],
    "mean_recall": ai_summary["mean_recall"],
    "mean_f1": ai_summary["mean_f1"],
}])
ai_table.to_csv(TABLES / "table2_ai_agreement_summary.csv", index=False)
(TABLES / "table2_ai_agreement_summary.tex").write_text(
    ai_table.to_latex(index=False, float_format="%.3f"),
    encoding="utf-8",
)

# Figure manifest
manifest = """# Phase 5.4 Publication Figures

1. figure1_architecture
2. figure2_benchmark_workflow
3. figure3_domain_distribution
4. figure4_presence_distribution
5. figure5_quality_distribution
6. figure6_presence_vs_quality
7. figure7_quality_by_domain
8. figure8_quality_heatmap
9. figure9_ai_agreement_metrics
10. figure10_domain_confidence_intervals

Each figure is exported as PNG (300 DPI) and PDF.
"""
(OUT / "FIGURE_MANIFEST.md").write_text(manifest, encoding="utf-8")

print("Created Phase 5.4 publication figures and tables.")
