# Phase 5.3 Statistical Analysis

## Dataset

- Repositories analyzed: **30**
- Domains: **5**

## Presence–quality association

- Pearson correlation: **r = 0.407, p = 0.0255**
- Spearman correlation: **rho = 0.360, p = 0.0506**

The Pearson association is statistically significant at α = 0.05.

## Domain differences in quality scores

- One-way ANOVA: **F = 0.693, p = 0.6038**
- ANOVA effect size: **η² = 0.100**
- Kruskal–Wallis: **H = 2.780, p = 0.5953**
- Kruskal–Wallis effect size: **ε² = 0.000**

The non-parametric domain comparison is not statistically significant at α = 0.05.

## Domain differences in presence scores

- One-way ANOVA: **F = 0.894, p = 0.4822**
- ANOVA effect size: **η² = 0.125**
- Kruskal–Wallis: **H = 2.547, p = 0.6363**
- Kruskal–Wallis effect size: **ε² = 0.000**

## Outputs

- `phase53_domain_summary.csv`
- `phase53_pairwise_quality_tests.csv`
- `phase53_statistical_results.json`

## Interpretation note

The benchmark uses six repositories per domain. Statistical power is limited, and repository selection was purposive rather than random. Results should be treated as exploratory evidence under the current ReproPilot rubric.
