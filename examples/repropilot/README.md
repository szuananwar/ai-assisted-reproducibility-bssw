# ReproPilot: Grounded AI Reproducibility Assessment for Scientific Software

> **Research prototype / case study within the 2026 Better Scientific Software Fellowship project:** *Sustainable AI: Best Practices for Reproducible Scientific Software Development*.

ReproPilot is an open-source research prototype for assessing the reproducibility readiness of scientific software repositories and AI-enabled high-performance computing workflows. It is one implementation developed within the broader fellowship research on **AI-Assisted Reproducibility in Scientific Software**.

ReproPilot combines transparent deterministic assessment, quality-aware repository analysis, optional grounded local large language model recommendations, statistical benchmarking, visualization, and a web-based repository assessment interface.

The prototype is designed to explore how AI can assist reproducibility work while preserving traceability and human oversight. Deterministic assessment remains authoritative; the grounded AI component only prioritizes or explains verified findings and does not independently assign repository scores.

## Key Features

- Deterministic reproducibility artifact assessment
- Quality-aware evaluation of repository artifacts
- Recursive discovery of nested documentation and configuration files
- HPC-aware and applicability-aware scoring
- Local grounded AI prioritization using Ollama
- Evidence-constrained AI outputs
- Automated benchmarking across scientific software repositories
- Statistical analysis and cross-domain comparisons
- Publication-quality figures and tables
- FastAPI web assessment service
- Downloadable JSON and HTML assessment reports

## Framework Architecture

```text
GitHub Repository
        │
        ▼
Artifact Presence Assessment
        │
        ▼
Artifact Quality Assessment
        │
        ▼
Grounded Local AI Prioritization
        │
        ▼
Agreement and Statistical Analysis
        │
        ▼
JSON, HTML, CSV, and Visual Reports
```

## Assessment Categories

### Artifact Presence

The presence checker identifies evidence such as project documentation, dependency specifications, environment definitions, HPC software-stack configuration, automated tests, container recipes, experiment/provenance tracking, licensing, and relevant HPC metadata.

### Artifact Quality

The quality assessor examines factors such as README completeness, installation and execution instructions, dependency pinning, runtime declarations, container reproducibility, test assertions, CI configuration, provenance metadata, and HPC portability information.

## Grounded AI

ReproPilot supports optional local AI prioritization through Ollama. The AI layer receives deterministic findings and is constrained to select from verified assessment labels rather than inventing repository conditions.

The current reference implementation uses `gemma3:1b`. The deterministic assessment can be used independently when a local model is unavailable.

## Benchmark Evaluation

ReproPilot was evaluated on **30 open-source scientific software repositories across five domains**, with six repositories per domain.

| Domain | Repositories |
| --- | ---: |
| High-Performance Computing | 6 |
| Artificial Intelligence and Machine Learning | 6 |
| Computational Biology | 6 |
| Climate and Earth Science | 6 |
| Medical AI | 6 |

The benchmark evaluates artifact-presence scores, artifact-quality scores, category-level quality signals, cross-domain differences, presence-quality correlation, grounded-AI agreement, and assessment reliability.

### Selected Findings

- Artifact presence and quality showed a moderate positive association.
- Pearson correlation: `r = 0.407`, `p = 0.0255`.
- No statistically significant cross-domain differences were detected in the current sample.
- The constrained AI experiment produced valid outputs for 28 of 30 repositories (`93.3%`).
- Top-1 deterministic-AI agreement: `10.7%`.
- Mean Jaccard similarity: `0.313`.
- Mean F1 agreement score: `0.426`.

These findings support treating grounded AI as complementary decision support rather than as a replacement for deterministic assessment. The benchmark is exploratory: the current sample contains only 30 repositories and should not be interpreted as establishing universal differences among scientific software domains.

## Prototype Source Locations

The implementation currently remains in the repository's established root-level directories so existing imports, tests, notebooks, benchmark scripts, and web paths continue to work:

```text
checker/       deterministic, quality-aware, and grounded-AI assessment
validation/    external validation and assessment results
benchmark/     benchmark manifest, scripts, and results
analysis/      statistical and AI-agreement analyses
webapp/        FastAPI backend and interactive frontend
tests/         automated tests
```

This `examples/repropilot/` directory is the documentation home for ReproPilot as a fellowship example/case study. Moving the implementation itself can be considered later as a separate refactoring task.

## Installation

From the repository root:

```bash
git clone https://github.com/szuananwar/ai-assisted-reproducibility-bssw.git
cd ai-assisted-reproducibility-bssw
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

## Run the Deterministic Checker

```bash
python3 - <<'PY'
from checker.reproducibility_checker import assess_repository

result = assess_repository(".")
print(result)
PY
```

## Run the Quality Assessment

```bash
python3 - <<'PY'
from checker.quality_assessor import assess_repository_quality

result = assess_repository_quality(".", hpc_applicable=True)
print(result)
PY
```

## Run Tests

```bash
python3 -m pytest tests -v
```

## Tutorial Notebook

Start Jupyter Lab from the repository root and open:

```text
notebooks/AI_Assisted_Reproducibility_Checker.ipynb
```

## Run Grounded AI Prioritization

Install and start Ollama:

```bash
ollama pull gemma3:1b
ollama serve
```

Then use the grounded-AI scripts in `checker/` or `analysis/`.

## Run the Benchmark

```bash
python3 benchmark/run_large_scale_benchmark.py \
  --repropilot-root . \
  --manifest benchmark/repositories.csv \
  --workdir benchmark/repos \
  --output-dir benchmark/results
```

Generate descriptive statistics with:

```bash
python3 benchmark/summarize_benchmark.py
```

## Statistical Analysis and Figures

```bash
python3 analysis/run_statistical_analysis.py
python3 analysis/generate_publication_figures.py
```

Outputs are written under `analysis/figures/` and `analysis/publication_tables/`.

## Web Dashboard and API

```bash
python3 -m venv .venv-web
source .venv-web/bin/activate
python3 -m pip install -r webapp/backend/requirements.txt
PYTHONPATH=webapp/backend:. python3 -m pytest webapp/backend/tests -v
PYTHONPATH=webapp/backend:. uvicorn app.main:app --reload
```

The local dashboard is available at `http://127.0.0.1:8000/` and interactive API documentation at `http://127.0.0.1:8000/docs`.

## Interpretation of Scores

ReproPilot measures repository **reproducibility readiness** under an explicit indicator-based rubric. It does not guarantee scientific correctness, numerical validity, successful workflow execution, dataset availability, hardware equivalence, or complete experimental reproduction.

Scores and AI recommendations should be interpreted alongside expert review and, where possible, runtime validation.

## Role in the Fellowship

ReproPilot is not the fellowship project itself. It is a prototype and case study used to investigate several broader questions addressed by the fellowship, including:

- how automated evidence can support reproducibility assessment;
- why artifact quality matters in addition to artifact presence;
- how grounded AI can explain or prioritize verified findings;
- where AI and deterministic approaches disagree;
- how human oversight should be incorporated; and
- how AI-assisted reproducibility practices may apply across scientific software and HPC domains.

For the broader fellowship project, return to the [main project README](../../README.md) and the [Best Practices Guide](../../guide/best-practices-guide.md).
