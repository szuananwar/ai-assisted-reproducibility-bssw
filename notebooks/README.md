# AI-Assisted Reproducibility Tutorial Series

**2026 Better Scientific Software Fellowship — Milestone 2 Draft**

This tutorial series accompanies the Best Practices Guide for **Sustainable AI: Best Practices for Reproducible Scientific Software Development**. It is designed for researchers, research software engineers, faculty, students, and HPC/AI practitioners.

The series is broader than ReproPilot. Tutorials 1–6 teach transferable practices; Tutorial 7 uses ReproPilot as one research prototype and case study.

## Learning Path

| Tutorial | Topic | Notebook | Status |
| --- | --- | --- | --- |
| 1 | Reproducibility Foundations | [`Tutorial_01_Reproducibility_Foundations.ipynb`](Tutorial_01_Reproducibility_Foundations.ipynb) | Executable Milestone 2 draft |
| 2 | Environments and Dependencies | [`Tutorial_02_Environments_and_Dependencies.ipynb`](Tutorial_02_Environments_and_Dependencies.ipynb) | Executable Milestone 2 draft |
| 3 | Testing, CI, and Scientific Validation | [`Tutorial_03_Testing_CI_and_Scientific_Validation.ipynb`](Tutorial_03_Testing_CI_and_Scientific_Validation.ipynb) | Executable Milestone 2 draft |
| 4 | Experiment Tracking and Provenance | [`Tutorial_04_Experiment_Tracking_and_Provenance.ipynb`](Tutorial_04_Experiment_Tracking_and_Provenance.ipynb) | Executable Milestone 2 draft |
| 5 | HPC Reproducibility and Portability | [`Tutorial_05_HPC_Reproducibility_and_Portability.ipynb`](Tutorial_05_HPC_Reproducibility_and_Portability.ipynb) | Executable Milestone 2 draft |
| 6 | Responsible AI-Assisted Reproducibility | [`Tutorial_06_Responsible_AI_Assisted_Reproducibility.ipynb`](Tutorial_06_Responsible_AI_Assisted_Reproducibility.ipynb) | Executable Milestone 2 draft |
| 7 | ReproPilot Case Study | [`AI_Assisted_Reproducibility_Checker_GUI.ipynb`](AI_Assisted_Reproducibility_Checker_GUI.ipynb) and [`AI_Assisted_Reproducibility_Checker.ipynb`](AI_Assisted_Reproducibility_Checker.ipynb) | Executable case-study draft |

## What the Tutorials Teach

**Tutorial 1 — Reproducibility Foundations** introduces repository evidence, applicability, artifact quality, and the distinction between reproducibility readiness and successful reproduction.

**Tutorial 2 — Environments and Dependencies** examines dependency declarations, version constraints, environment reconstruction, platform information, and HPC/runtime assumptions.

**Tutorial 3 — Testing, CI, and Scientific Validation** distinguishes unit tests, workflow/integration tests, numerical tolerance checks, scientific validation, and production-scale HPC validation.

**Tutorial 4 — Experiment Tracking and Provenance** builds a structured provenance record connecting a result to source revision, data/model versions, preprocessing, parameters, seed, environment, hardware, and metrics.

**Tutorial 5 — HPC Reproducibility and Portability** records compiler/MPI/accelerator/module and resource context and separates scientifically relevant configuration from site-specific scheduler settings.

**Tutorial 6 — Responsible AI-Assisted Reproducibility** demonstrates evidence grounding, unsupported-claim detection, constrained AI roles, and human-in-the-loop review without requiring an external AI service.

**Tutorial 7 — ReproPilot Case Study** applies the ideas through the ReproPilot research prototype. The GUI notebook includes a static Spack example for GitHub viewers; interactive controls require JupyterLab/Notebook with an active kernel.

## Existing ReproPilot Companion Notebooks

- `AI_Assisted_Reproducibility_Checker.ipynb` — primary self-paced ReproPilot hands-on tutorial.
- `AI_Assisted_Reproducibility_Checker_EXECUTED.ipynb` — executed companion for inspecting representative outputs.
- `AI_Assisted_Reproducibility_Checker_GUI.ipynb` — interactive GUI-oriented Tutorial 7 companion.

These notebooks are supporting case-study materials. They do not define the broader fellowship project.

## Recommended Order

Learners new to research software reproducibility should complete Tutorials 1–7 in order. Experienced practitioners may select a topic-specific notebook and then use Tutorial 7 to examine one implementation of evidence-grounded AI assistance.

## Environment Setup

Tutorials 1–6 intentionally rely primarily on the Python standard library so they remain lightweight and portable. Tutorial 7 uses the repository package and additional dependencies.

From the repository root:

```bash
git clone https://github.com/szuananwar/ai-assisted-reproducibility-bssw.git
cd ai-assisted-reproducibility-bssw

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
jupyter lab
```

Optional local AI demonstration for ReproPilot:

```bash
ollama pull gemma3:1b
ollama serve
```

Tutorials 1–6 do not require Ollama.

## Relationship to the Best Practices Guide

The notebooks correspond to major topics in [`../guide/best-practices-guide.md`](../guide/best-practices-guide.md). Use the guide for conceptual background and the notebooks for practical exercises.

## Beta Testing and Feedback

Milestone 2 materials should be beta-tested before final publication. Reviewers should record:

- clarity of instructions and learning objectives;
- setup difficulty and execution problems;
- technical/scientific accuracy;
- approximate completion time;
- usefulness to scientific software practitioners;
- relevance across AI, HPC, and other scientific domains;
- accessibility for students and new contributors; and
- any statement that overclaims what repository evidence or AI assistance can establish.

Feedback should be documented and incorporated into Milestone 3 revisions.

## Milestone 2 Status

The tutorial series now contains executable draft notebooks for Tutorials 1–6 plus the ReproPilot Tutorial 7 case-study materials. The next phase is beta testing, technical review, refinement of exercises and outputs, and incorporation of documented feedback before final publication.