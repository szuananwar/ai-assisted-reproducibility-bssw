
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
results=ROOT/"benchmark/results/phase5_benchmark_results.csv"
out=ROOT/"analysis"
out.mkdir(exist_ok=True)

df=pd.read_csv(results)

# Histogram Presence
plt.figure(figsize=(6,4))
plt.hist(df["presence_percent"], bins=10)
plt.xlabel("Presence Score (%)")
plt.ylabel("Repositories")
plt.tight_layout()
plt.savefig(out/"presence_histogram.png")
plt.close()

# Histogram Quality
plt.figure(figsize=(6,4))
plt.hist(df["quality_percent"], bins=10)
plt.xlabel("Quality Score (%)")
plt.ylabel("Repositories")
plt.tight_layout()
plt.savefig(out/"quality_histogram.png")
plt.close()

# Scatter
plt.figure(figsize=(5,5))
plt.scatter(df["presence_percent"], df["quality_percent"])
plt.xlabel("Presence (%)")
plt.ylabel("Quality (%)")
plt.tight_layout()
plt.savefig(out/"presence_vs_quality.png")
plt.close()

# Boxplot
plt.figure(figsize=(8,4))
domains=sorted(df["domain"].unique())
vals=[df[df.domain==d]["quality_percent"] for d in domains]
plt.boxplot(vals, tick_labels=domains)
plt.xticks(rotation=30, ha="right")
plt.ylabel("Quality (%)")
plt.tight_layout()
plt.savefig(out/"quality_by_domain_boxplot.png")
plt.close()

corr=df["presence_percent"].corr(df["quality_percent"])

report=dedent(f"""
# Phase 5.2 Analysis

## Correlation

Presence vs Quality Pearson correlation: **{corr:.3f}**

## Figures

- presence_histogram.png
- quality_histogram.png
- presence_vs_quality.png
- quality_by_domain_boxplot.png

## Interpretation

These visualizations summarize the current benchmark dataset. They should be interpreted as measurements under the current ReproPilot rubric rather than absolute measures of software quality.
""")
(out/"phase52_analysis.md").write_text(report)
print("Done")
