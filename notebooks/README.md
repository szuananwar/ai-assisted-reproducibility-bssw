# AI-Assisted Reproducibility Tutorial Series

**2026 Better Scientific Software Fellowship — Milestone 2 Draft**

This tutorial series accompanies the Best Practices Guide for the fellowship project **Sustainable AI: Best Practices for Reproducible Scientific Software Development**. The tutorials are designed to help researchers, research software engineers, faculty, students, and HPC/AI practitioners apply reproducibility practices through hands-on activities.

The series is broader than ReproPilot. ReproPilot is used in selected activities as a research prototype and teaching example for evidence-based repository assessment and grounded AI assistance.

## Learning Path

| Tutorial | Topic | Primary learning outcome | Status |
| --- | --- | --- | --- |
| 1 | Reproducibility Foundations | Identify the artifacts and practices needed to make a scientific software project reproducibility-ready. | Draft available |
| 2 | Environments and Dependencies | Create and evaluate dependency/environment specifications for scientific and AI workflows. | Milestone 2 draft activity guide |
| 3 | Testing and Continuous Integration | Distinguish software tests from scientific validation and plan meaningful automated checks. | Milestone 2 draft activity guide |
| 4 | Experiment Tracking and Provenance | Record parameters, data/model provenance, environment information, and source revisions for computational experiments. | Milestone 2 draft activity guide |
| 5 | HPC Reproducibility and Portability | Document compilers, MPI/GPU stacks, schedulers, resources, modules, and site-specific assumptions. | Milestone 2 draft activity guide |
| 6 | Responsible AI-Assisted Reproducibility | Use AI as a grounded assistant while preserving evidence, human oversight, and scientific responsibility. | Draft available in hands-on notebook |
| 7 | Case Study: ReproPilot | Apply an evidence-based assessment, inspect repository evidence, and compare deterministic findings with optional grounded AI guidance. | Draft available |

## Existing Hands-On Notebooks

### `AI_Assisted_Reproducibility_Checker.ipynb`

This is the primary self-paced hands-on notebook. It currently demonstrates repository assessment, evidence inspection, optional local grounded-AI explanation, before-and-after reproducibility improvement, and reflection on the limitations of automated assessment.

For the fellowship, treat ReproPilot in this notebook as a **case study and instructional prototype**, not as the definition of AI-assisted reproducibility.

### `AI_Assisted_Reproducibility_Checker_EXECUTED.ipynb`

Executed companion copy of the checker tutorial. It can be used to inspect representative outputs without rerunning every cell. Because generated outputs can become stale as the prototype changes, the unexecuted notebook remains the primary tutorial source.

### `AI_Assisted_Reproducibility_Checker_GUI.ipynb`

Interactive GUI-oriented companion notebook for learners who benefit from a more guided interface.

## Milestone 2 Activity Guides

The following activities turn the existing materials into a coherent tutorial series while additional standalone notebooks are developed.

### Tutorial 1 — Reproducibility Foundations

**Goal:** Understand reproducibility as a connected scientific software practice rather than a single file or tool.

**Activity:** Select one scientific software repository and identify evidence for documentation, dependencies, environments, tests, licensing, data/model provenance, experiment configuration, and portable execution. For each artifact, record both what its presence supports and what it cannot prove.

**Reflection:** Which reproducibility requirements are general software practices, and which depend on the scientific domain?

### Tutorial 2 — Environments and Dependencies

**Goal:** Understand how dependency declarations and environment capture support repeatable computational work.

**Activity:** Examine `requirements.txt`, `environment.yml`, `pyproject.toml`, lock files, or `spack.yaml` from a scientific software project. Identify unpinned dependencies, missing runtime information, accelerator/compiler assumptions, and information that would be required to reconstruct the environment.

**Deliverable:** Produce or improve one environment specification and document the assumptions it cannot encode.

### Tutorial 3 — Testing and Continuous Integration

**Goal:** Distinguish code correctness checks from scientific validation.

**Activity:** Review an existing test suite or design tests for a small scientific workflow. Include at least one unit test, one workflow/integration test, and one scientifically meaningful assertion or tolerance-based comparison where appropriate.

**Reflection:** What would a passing test suite still fail to prove about the scientific result?

### Tutorial 4 — Experiment Tracking and Provenance

**Goal:** Connect computational results to the artifacts and configurations that produced them.

**Activity:** Create an experiment record containing source revision, dataset/model version, preprocessing, parameters or hyperparameters, random seed, software environment, hardware, and evaluation metrics. An experiment tracker such as MLflow may be used, but a structured provenance record is also acceptable.

**Deliverable:** A reproducibility record sufficient for another researcher to identify the configuration associated with a reported result.

### Tutorial 5 — HPC Reproducibility and Portability

**Goal:** Separate scientifically essential configuration from site-specific HPC settings.

**Activity:** Review or create an HPC execution record containing compiler, MPI implementation, GPU/accelerator information, CUDA/ROCm where applicable, environment modules, scheduler directives, node/process/thread counts, and architecture-specific assumptions.

**Reflection:** Which settings must remain fixed to reproduce the scientific method, and which can be adapted on another HPC system?

### Tutorial 6 — Responsible AI-Assisted Reproducibility

**Goal:** Evaluate where AI assistance is useful and where human verification is required.

**Activity:** Provide an AI assistant with a small set of verified reproducibility findings. Ask it to explain or prioritize the findings. Then classify each response as supported, unsupported, overly generic, or requiring expert review.

**Key rule:** AI-generated text is not itself reproducibility evidence.

### Tutorial 7 — ReproPilot Case Study

**Goal:** Explore one implementation of grounded AI-assisted reproducibility assessment.

Use `AI_Assisted_Reproducibility_Checker.ipynb` to:

1. run deterministic repository checks;
2. inspect the evidence package;
3. interpret reproducibility-readiness findings;
4. optionally generate local AI explanations;
5. compare weak and stronger repository examples; and
6. discuss why repository readiness is not proof of successful scientific reproduction.

## Recommended Order

Learners new to research software reproducibility should work through Tutorials 1–7 in order. Experienced research software engineers may begin with the topic most relevant to their project and use Tutorial 7 as a case study after reviewing the responsible-AI principles.

## Environment Setup

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

Optional local AI demonstration:

```bash
ollama pull gemma3:1b
ollama serve
```

The deterministic portions of the tutorials do not require Ollama.

## Relationship to the Best Practices Guide

The tutorials correspond to the major topics in [`../guide/best-practices-guide.md`](../guide/best-practices-guide.md). Learners are encouraged to use the guide for conceptual background and the tutorial series for practical exercises.

## Beta Testing and Feedback

Milestone 2 requires the tutorial materials to be made available for beta testing and initial feedback. Reviewers should consider:

- clarity of instructions;
- setup difficulty;
- technical correctness;
- expected completion time;
- usefulness to scientific software practitioners;
- relevance across AI, HPC, and other scientific domains;
- accessibility for students and new research software contributors; and
- places where the tutorial depends too heavily on the ReproPilot case study.

Feedback should be documented so it can be incorporated into the Milestone 3 revisions.

## Milestone 2 Status

This tutorial index and activity sequence constitute the organized Milestone 2 draft tutorial series. The next refinement is to convert the activity guides into additional standalone executable notebooks, beta-test them with users, and incorporate the resulting feedback before final publication in Milestone 3.
