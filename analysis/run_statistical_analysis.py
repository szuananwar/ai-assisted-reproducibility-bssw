
from __future__ import annotations

from itertools import combinations
from pathlib import Path
import json
import math

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "benchmark/results/phase5_benchmark_results.csv"
OUT = ROOT / "analysis"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(INPUT)

required = {"domain", "presence_percent", "quality_percent"}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Missing required columns: {sorted(missing)}")

def bootstrap_ci(values, confidence=0.95, n_boot=10000, seed=42):
    values = np.asarray(values, dtype=float)
    rng = np.random.default_rng(seed)
    means = np.empty(n_boot)
    for i in range(n_boot):
        means[i] = rng.choice(values, size=len(values), replace=True).mean()
    alpha = 1 - confidence
    return (
        float(np.quantile(means, alpha / 2)),
        float(np.quantile(means, 1 - alpha / 2)),
    )

def holm_adjust(p_values):
    p_values = list(p_values)
    order = np.argsort(p_values)
    adjusted = np.empty(len(p_values), dtype=float)
    running_max = 0.0
    m = len(p_values)
    for rank, idx in enumerate(order):
        value = min((m - rank) * p_values[idx], 1.0)
        running_max = max(running_max, value)
        adjusted[idx] = running_max
    return adjusted.tolist()

def eta_squared(groups):
    all_values = np.concatenate(groups)
    grand_mean = all_values.mean()
    ss_between = sum(len(g) * (g.mean() - grand_mean) ** 2 for g in groups)
    ss_total = sum(((g - grand_mean) ** 2).sum() for g in groups)
    return float(ss_between / ss_total) if ss_total else 0.0

def epsilon_squared_kruskal(h_stat, n, k):
    if n <= k:
        return 0.0
    return float(max((h_stat - k + 1) / (n - k), 0.0))

domains = sorted(df["domain"].dropna().unique())
quality_groups = [
    df.loc[df["domain"] == domain, "quality_percent"].astype(float).to_numpy()
    for domain in domains
]
presence_groups = [
    df.loc[df["domain"] == domain, "presence_percent"].astype(float).to_numpy()
    for domain in domains
]

# Overall correlations
pearson_r, pearson_p = stats.pearsonr(
    df["presence_percent"].astype(float),
    df["quality_percent"].astype(float),
)
spearman_rho, spearman_p = stats.spearmanr(
    df["presence_percent"].astype(float),
    df["quality_percent"].astype(float),
)

# Assumption checks and omnibus tests
quality_shapiro = {
    domain: stats.shapiro(group)._asdict()
    for domain, group in zip(domains, quality_groups)
    if len(group) >= 3
}
quality_levene = stats.levene(*quality_groups, center="median")
quality_anova = stats.f_oneway(*quality_groups)
quality_kruskal = stats.kruskal(*quality_groups)

presence_levene = stats.levene(*presence_groups, center="median")
presence_anova = stats.f_oneway(*presence_groups)
presence_kruskal = stats.kruskal(*presence_groups)

# Descriptive statistics + bootstrap CIs
summary_rows = []
for domain in domains:
    subset = df[df["domain"] == domain]
    for metric in ["presence_percent", "quality_percent"]:
        values = subset[metric].astype(float).to_numpy()
        low, high = bootstrap_ci(values)
        summary_rows.append({
            "domain": domain,
            "metric": metric,
            "n": len(values),
            "mean": round(float(values.mean()), 3),
            "median": round(float(np.median(values)), 3),
            "std": round(float(values.std(ddof=1)), 3) if len(values) > 1 else 0.0,
            "ci95_low": round(low, 3),
            "ci95_high": round(high, 3),
        })

summary_df = pd.DataFrame(summary_rows)
summary_df.to_csv(OUT / "phase53_domain_summary.csv", index=False)

# Pairwise Mann-Whitney U tests on quality
pairwise = []
raw_ps = []
for d1, d2 in combinations(domains, 2):
    x = df.loc[df["domain"] == d1, "quality_percent"].astype(float).to_numpy()
    y = df.loc[df["domain"] == d2, "quality_percent"].astype(float).to_numpy()
    result = stats.mannwhitneyu(x, y, alternative="two-sided")
    raw_ps.append(float(result.pvalue))
    pairwise.append({
        "domain_1": d1,
        "domain_2": d2,
        "u_statistic": round(float(result.statistic), 3),
        "p_raw": float(result.pvalue),
    })

adjusted = holm_adjust(raw_ps)
for row, p_adj in zip(pairwise, adjusted):
    row["p_holm"] = round(float(p_adj), 6)
    row["significant_0_05"] = p_adj < 0.05

pairwise_df = pd.DataFrame(pairwise)
pairwise_df.to_csv(OUT / "phase53_pairwise_quality_tests.csv", index=False)

results = {
    "sample_size": int(len(df)),
    "domains": domains,
    "correlations": {
        "pearson": {"r": float(pearson_r), "p": float(pearson_p)},
        "spearman": {"rho": float(spearman_rho), "p": float(spearman_p)},
    },
    "quality": {
        "levene": {"statistic": float(quality_levene.statistic), "p": float(quality_levene.pvalue)},
        "anova": {
            "statistic": float(quality_anova.statistic),
            "p": float(quality_anova.pvalue),
            "eta_squared": eta_squared(quality_groups),
        },
        "kruskal_wallis": {
            "statistic": float(quality_kruskal.statistic),
            "p": float(quality_kruskal.pvalue),
            "epsilon_squared": epsilon_squared_kruskal(
                quality_kruskal.statistic, len(df), len(domains)
            ),
        },
        "shapiro_by_domain": quality_shapiro,
    },
    "presence": {
        "levene": {"statistic": float(presence_levene.statistic), "p": float(presence_levene.pvalue)},
        "anova": {
            "statistic": float(presence_anova.statistic),
            "p": float(presence_anova.pvalue),
            "eta_squared": eta_squared(presence_groups),
        },
        "kruskal_wallis": {
            "statistic": float(presence_kruskal.statistic),
            "p": float(presence_kruskal.pvalue),
            "epsilon_squared": epsilon_squared_kruskal(
                presence_kruskal.statistic, len(df), len(domains)
            ),
        },
    },
}

(OUT / "phase53_statistical_results.json").write_text(
    json.dumps(results, indent=2),
    encoding="utf-8",
)

def sig_text(p):
    return "statistically significant" if p < 0.05 else "not statistically significant"

report = f"""# Phase 5.3 Statistical Analysis

## Dataset

- Repositories analyzed: **{len(df)}**
- Domains: **{len(domains)}**

## Presence–quality association

- Pearson correlation: **r = {pearson_r:.3f}, p = {pearson_p:.4f}**
- Spearman correlation: **rho = {spearman_rho:.3f}, p = {spearman_p:.4f}**

The Pearson association is {sig_text(pearson_p)} at α = 0.05.

## Domain differences in quality scores

- One-way ANOVA: **F = {quality_anova.statistic:.3f}, p = {quality_anova.pvalue:.4f}**
- ANOVA effect size: **η² = {eta_squared(quality_groups):.3f}**
- Kruskal–Wallis: **H = {quality_kruskal.statistic:.3f}, p = {quality_kruskal.pvalue:.4f}**
- Kruskal–Wallis effect size: **ε² = {epsilon_squared_kruskal(quality_kruskal.statistic, len(df), len(domains)):.3f}**

The non-parametric domain comparison is {sig_text(quality_kruskal.pvalue)} at α = 0.05.

## Domain differences in presence scores

- One-way ANOVA: **F = {presence_anova.statistic:.3f}, p = {presence_anova.pvalue:.4f}**
- ANOVA effect size: **η² = {eta_squared(presence_groups):.3f}**
- Kruskal–Wallis: **H = {presence_kruskal.statistic:.3f}, p = {presence_kruskal.pvalue:.4f}**
- Kruskal–Wallis effect size: **ε² = {epsilon_squared_kruskal(presence_kruskal.statistic, len(df), len(domains)):.3f}**

## Outputs

- `phase53_domain_summary.csv`
- `phase53_pairwise_quality_tests.csv`
- `phase53_statistical_results.json`

## Interpretation note

The benchmark uses six repositories per domain. Statistical power is limited, and repository selection was purposive rather than random. Results should be treated as exploratory evidence under the current ReproPilot rubric.
"""

(OUT / "phase53_statistical_report.md").write_text(report, encoding="utf-8")
print("Created Phase 5.3 statistical outputs.")
