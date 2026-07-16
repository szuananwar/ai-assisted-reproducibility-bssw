# Phase 2: External Repository Validation

ReproPilot was evaluated on three repositories representing mature scientific software, HPC tooling, and a domain-specific AI/HPC workflow.

| Repository | Domain | Score | Interpretation |
|---|---|---:|---|
| BuildTest | hpc-simulation | 55/110 (50.0%) | Moderate reproducibility risk |
| NumPy | general | 55/100 (55.0%) | Moderate reproducibility risk |
| Brain Tumor Viskores ViT | biomedical | 30/110 (27.3%) | High reproducibility risk |

## Interpretation

The rubric measures repository readiness signals, not scientific correctness. Scores should be interpreted alongside manual review of documentation, tests, container builds, numerical validation, and domain-specific requirements.

## Detailed findings

### BuildTest

- Purpose: HPC-focused testing framework
- Domain profile: `hpc-simulation`
- Score: **55/110 (50.0%)**

- **Documentation** — PASS (15/15); found: README.rst
- **Dependency specification** — PASS (15/15); found: requirements.txt, pyproject.toml
- **Reproducible environment** — MISSING (0/10); found: none
- **HPC software stack** — MISSING (0/10); found: none
- **Automated tests** — PASS (15/15); found: tests, tox.ini
- **Container recipe** — MISSING (0/15); found: none
- **Experiment/provenance tracking** — MISSING (0/10); found: none
- **License** — PASS (10/10); found: LICENSE
- **Scheduler configuration** — MISSING (0/5); found: none
- **Compiler/runtime metadata** — MISSING (0/5); found: none

### NumPy

- Purpose: Mature scientific Python library
- Domain profile: `general`
- Score: **55/100 (55.0%)**

- **Documentation** — PASS (15/15); found: README.md
- **Dependency specification** — PASS (15/15); found: pyproject.toml
- **Reproducible environment** — PASS (10/10); found: environment.yml
- **HPC software stack** — MISSING (0/10); found: none
- **Automated tests** — PASS (15/15); found: pytest.ini
- **Container recipe** — MISSING (0/15); found: none
- **Experiment/provenance tracking** — MISSING (0/10); found: none
- **License** — MISSING (0/10); found: none

### Brain Tumor Viskores ViT

- Purpose: Domain-specific AI/HPC scientific workflow
- Domain profile: `biomedical`
- Score: **30/110 (27.3%)**

- **Documentation** — PASS (15/15); found: README.md
- **Dependency specification** — PASS (15/15); found: requirements.txt
- **Reproducible environment** — MISSING (0/10); found: none
- **HPC software stack** — MISSING (0/10); found: none
- **Automated tests** — MISSING (0/15); found: none
- **Container recipe** — MISSING (0/15); found: none
- **Experiment/provenance tracking** — MISSING (0/10); found: none
- **License** — MISSING (0/10); found: none
- **Data documentation** — MISSING (0/5); found: none
- **Random seed control** — MISSING (0/5); found: none
