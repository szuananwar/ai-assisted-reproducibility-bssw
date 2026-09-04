# AI-Assisted Reproducibility in Scientific Software

## Best Practices for Sustainable AI and HPC Workflows

**2026 Better Scientific Software Fellowship-Milestone 2 Draft**

**Author:** Suzan Anwar, Ph.D.  
**Fellowship Project:** *Sustainable AI: Best Practices for Reproducible Scientific Software Development*

## 1. Introduction

Scientific software increasingly combines source code, data, machine-learning models, complex dependency stacks, specialized hardware, and high-performance computing (HPC) environments. Reproducing a computational result therefore requires more than preserving source code. Researchers must also capture how software was configured, which dependencies and tools were used, how experiments were executed, and what evidence supports the reported results.

AI-enabled workflows introduce additional challenges. Results may depend on model versions, training parameters, random seeds, preprocessing decisions, accelerator hardware, and rapidly changing software libraries. At the same time, artificial intelligence can assist researchers with documentation, repository inspection, workflow diagnostics, provenance review, and identification of missing reproducibility information.

This guide presents practical best practices for **AI-assisted reproducibility in scientific software**. Its central premise is that AI should augment established research software engineering practices rather than replace transparent evidence, testing, provenance, or human scientific judgment. The recommendations apply broadly to scientific software while giving particular attention to AI-enabled and HPC workflows.

Reproducibility readiness is not the same as successful reproduction. Repository inspection can identify evidence that supports reproducibility, but it cannot by itself prove scientific correctness, numerical validity, data availability, hardware equivalence, or successful execution of an entire workflow. AI-assisted reproducibility should therefore combine automation with verifiable evidence, expert review, and runtime validation when feasible.

## 2. Reproducibility Challenges in Modern Scientific Software

Scientific workflows often span multiple layers: source code, configuration, dependencies, datasets, trained models, experiment parameters, operating environments, hardware, and execution infrastructure. A failure to preserve any one of these layers can make a published computational result difficult to understand or reproduce.

AI workflows add model versions, stochastic training behavior, hyperparameters, preprocessing pipelines, random seeds, and accelerator-specific software stacks. HPC workflows add compilers, MPI implementations, GPU runtimes, environment modules, schedulers, filesystem assumptions, resource allocations, and architecture-specific optimizations.

These challenges make reproducibility both a technical and organizational problem. Sustainable practices should be incorporated during development rather than reconstructed only when a paper, dataset, or software release is prepared.

## 3. Sustainable Scientific Software Foundations

A reproducible scientific software project should make it possible for another researcher—or the original team months later—to understand what was done, reconstruct an appropriate environment, execute representative workflows, and interpret outputs.

### 3.1 Version control

Use a version-control system such as Git for source code, configuration, documentation, and other text-based project artifacts. Commit changes regularly and use meaningful commit messages. Releases, tags, or commit identifiers should be associated with important experiments and publications so that the software state used for a result can be recovered.

Large datasets and model artifacts should generally not be stored directly in ordinary Git history. Instead, document their versions and locations and use appropriate data- or artifact-versioning mechanisms when needed.

### 3.2 Documentation

Every repository should provide a clear entry point, normally a `README.md`. At minimum, documentation should explain the scientific purpose of the software, installation requirements, dependencies, environment setup, execution instructions, expected inputs and outputs, testing procedures, data/model access, and HPC requirements when applicable.

Documentation should be treated as part of the workflow. Commands that are never tested can quickly become obsolete even when the underlying software remains functional.

### 3.3 Reproducibility as a development practice

Teams should integrate reproducibility into ordinary software development through shared conventions, code review, automated testing, environment management, experiment records, and documentation updates. This reduces the effort required to prepare reproducible releases and improves long-term maintainability.

## 4. Dependency and Environment Management

Dependencies should be explicitly declared rather than assumed. Common mechanisms include `requirements.txt`, `pyproject.toml`, `environment.yml`, lock files, and Spack environments.

Record versions when differences may affect behavior. Overly loose dependencies can allow environments to change unexpectedly, while excessively rigid dependencies can reduce portability. Projects should choose a level of pinning appropriate to their scientific and maintenance needs.

### 4.1 Environment capture

A package list alone may not capture the complete execution environment. Scientific workflows can depend on Python or compiler versions, CUDA or ROCm versions, MPI implementations, system libraries, environment modules, and hardware capabilities.

Use Conda environments, lock files, Spack environments, containers, or other appropriate mechanisms to capture important environment information. Document assumptions that cannot be encoded directly.

### 4.2 Spack and HPC software stacks

Spack is useful for scientific software stacks involving compilers, MPI libraries, accelerator support, and architecture-specific packages. A `spack.yaml` can document an intended environment, but researchers should also record important compiler, architecture, and variant assumptions because an identical concretization may not be appropriate on every system.

## 5. Testing, Continuous Integration, and Scientific Validation

Testing helps determine whether software changes alter expected behavior and is therefore central to both sustainability and reproducibility.

### 5.1 Unit, integration, and workflow tests

Unit tests should verify small software components. Integration tests should exercise interactions among components, and workflow tests should verify representative end-to-end paths. Small reference datasets can make scientific workflow tests practical for routine execution.

Tests should contain meaningful assertions rather than only checking that software runs without crashing.

### 5.2 Numerical validation

Scientific software may require tolerance-based comparisons instead of exact equality. Projects should document why tolerances are numerically and scientifically appropriate. When results vary across architectures or accelerators, expected floating-point differences should be distinguished from scientifically meaningful changes.

### 5.3 Continuous integration

Continuous integration (CI) can automatically verify installation, execute tests, check representative workflows, and validate documentation or configuration files when software changes.

HPC software may require complementary approaches because production systems are not always available to public CI services. Site-specific test systems and tools such as BuildTest can help validate compiler, scheduler, accelerator, and multi-node configurations.

## 6. Containers and Portable Execution

Containers can package software dependencies and runtime environments into reusable artifacts. Docker is widely used for development and cloud environments, while Apptainer is commonly used on HPC systems.

A useful container definition should identify the base image, dependency installation, application installation, runtime configuration, expected commands, and external data or hardware requirements.

Containers improve portability but do not guarantee complete reproducibility. Host kernels, GPU drivers, processor architectures, distributed runtimes, and external data can still affect results. Container definitions should complement rather than replace environment and workflow documentation.

## 7. HPC Reproducibility and Portability

HPC workflows often require metadata beyond ordinary application dependencies. Relevant information may include scheduler scripts, compiler and version, MPI implementation, GPU accelerator type, CUDA or ROCm version, environment modules, node/process counts, CPU or GPU requests, thread settings, filesystem assumptions, and architecture-specific build options.

Portable HPC documentation should distinguish scientifically essential requirements from settings that are specific to one computing center. Another researcher should be able to understand which choices must be preserved and which can be adapted to a different system.

## 8. Experiment Tracking, Data, and Model Provenance

AI and computational experiments frequently involve many combinations of parameters, datasets, preprocessing steps, model versions, random seeds, and software environments. These should be recorded systematically.

At minimum, retain:

- model architecture or identifier when applicable;
- dataset version and preprocessing procedure;
- train/validation/test split information for ML workflows;
- random seeds;
- important parameters and hyperparameters;
- software environment;
- hardware or accelerator information;
- training and evaluation metrics; and
- links between outputs and the corresponding source-code revision.

Experiment-tracking systems such as MLflow can automate portions of this process. Other provenance mechanisms may be more appropriate in other scientific domains. The important principle is that reported results should be connected to the configurations and artifacts that produced them.

Where licensing, privacy, or security restrictions prevent redistribution of data or models, provide appropriate access instructions and document required preprocessing without exposing restricted material.

## 9. AI-Assisted Reproducibility

AI can support reproducibility work in several ways, including identifying missing documentation, explaining environment problems, reviewing configuration artifacts, suggesting tests, summarizing provenance gaps, and helping researchers prioritize improvements.

However, an AI-generated statement is not reproducibility evidence. AI assistance should operate on inspectable project information whenever possible and should clearly distinguish observed facts from generated recommendations.

### 9.1 Grounding AI assistance

Grounded AI systems should receive verified evidence such as repository files, test outcomes, environment metadata, or structured assessment findings. Recommendations should refer back to that evidence rather than freely inferring project conditions.

For example, if an automated inspection verifies that a repository lacks tests, AI can explain why representative tests would improve reproducibility and suggest appropriate next steps. It should not invent additional missing artifacts that were never observed.

### 9.2 Appropriate roles for AI

Useful roles include explanation, prioritization, documentation assistance, remediation suggestions, workflow troubleshooting, and helping researchers navigate complex reproducibility requirements.

AI should not independently establish scientific correctness, certify successful reproduction, choose scientific tolerances without domain justification, or replace expert validation of computational results.

## 10. Risks, Limitations, and Human Oversight

LLMs can generate plausible but unsupported recommendations, vary across model versions or prompts, overlook domain-specific requirements, and create an appearance of certainty that exceeds available evidence.

Responsible AI-assisted reproducibility should therefore emphasize:

- traceable evidence;
- structured and constrained outputs when appropriate;
- explicit uncertainty and limitations;
- deterministic checks for facts that can be verified directly;
- review of important AI recommendations by researchers or research software engineers; and
- runtime validation when claims depend on successful execution.

Local AI may be valuable for private, restricted, or air-gapped environments. Cloud models may provide different capabilities, but their use should consider data governance, security, cost, and institutional requirements.

## 11. Practical Best Practices for Researchers and Teams

Researchers should aim to create a minimum reproducibility package appropriate to their project. A strong package normally includes:

1. a clear README describing the project and scientific workflow;
2. tested installation and execution instructions;
3. explicit dependency information;
4. an environment specification appropriate to the project;
5. automated tests with meaningful assertions;
6. data and model provenance or access instructions;
7. experiment configuration and parameter records;
8. a software license;
9. container or portable execution information when useful; and
10. HPC configuration and job information when applicable.

Teams should establish shared conventions for repository structure, version control, code review, dependency updates, experiment naming, and documentation. New contributors should be able to follow the documented setup process without depending entirely on verbal knowledge from the original developer.

Students should be introduced early to version control, environment management, testing, documentation, and experiment tracking. These practices improve scientific reliability while building transferable research software engineering skills.

## 12. Case Study: ReproPilot as an AI-Assisted Reproducibility Prototype

ReproPilot is one research prototype developed within this fellowship to explore how deterministic repository evidence and grounded AI assistance can be combined. It is a case study supporting the broader fellowship research rather than the fellowship project itself.

The prototype performs deterministic artifact discovery and quality-aware assessment. An optional local LLM receives verified findings and can prioritize or explain deficiencies. The deterministic assessment remains authoritative; AI does not independently calculate or alter repository scores.

The current indicator-based rubric examines eight categories:

| Category | Current Weight | Example Evidence |
|---|---:|---|
| Documentation | 15 | `README.md`, `README.rst` |
| Dependencies | 15 | `requirements.txt`, `pyproject.toml` |
| Environment | 10 | `environment.yml`, lock files |
| HPC software stack | 10 | `spack.yaml`, BuildTest configuration |
| Testing | 15 | `tests/`, `pytest.ini`, `tox.ini` |
| Containers | 15 | `Dockerfile`, `Containerfile`, `apptainer.def` |
| Experiment/provenance tracking | 10 | `MLproject`, `dvc.yaml`, `params.yaml`, provenance metadata |
| Licensing | 10 | `LICENSE`, `LICENSE.md`, `COPYING` |

The weights are explicit methodological choices, not universal measures of reproducibility. Different scientific communities may reasonably prioritize different evidence.

### 12.1 Artifact presence versus artifact quality

The prototype illustrates an important lesson for the broader guide: the existence of an artifact does not establish its usefulness. A README may lack installation instructions, a dependency file may omit important versions, or tests may lack meaningful assertions. Reproducibility practice should therefore consider quality as well as presence.

### 12.2 Interpretation

A ReproPilot score is an indicator of repository reproducibility readiness under the selected rubric. It does not guarantee scientific correctness, numerical validity, successful execution, dataset availability, hardware equivalence, or complete experimental reproduction.

Detailed prototype documentation is maintained under [`examples/repropilot/`](../examples/repropilot/README.md).

## 13. Lessons from the ReproPilot Benchmark

ReproPilot was evaluated on **30 open-source scientific software repositories across five domains**, with six repositories per domain.

| Domain | Repositories |
| --- | ---: |
| High-Performance Computing | 6 |
| Artificial Intelligence and Machine Learning | 6 |
| Computational Biology | 6 |
| Climate and Earth Science | 6 |
| Medical AI | 6 |

The evaluation examined artifact presence, artifact quality, category-level signals, cross-domain comparisons, presence-quality association, grounded-AI output validity, and agreement between deterministic and AI-selected priorities.

Selected findings from the current benchmark include:

- Pearson presence-quality correlation: **r = 0.407, p = 0.0255**;
- no statistically significant cross-domain differences detected in the current sample;
- valid constrained-AI outputs for **28 of 30 repositories (93.3%)**;
- top-1 deterministic-AI agreement of **10.7%**;
- mean Jaccard similarity of **0.313**; and
- mean F1 agreement of **0.426**.

The moderate presence-quality relationship reinforces the need to examine artifact content rather than merely count files. The relatively low deterministic-AI priority agreement reinforces the broader fellowship recommendation that AI should be treated as complementary decision support rather than a replacement for transparent evidence-based assessment.

These results are exploratory. Thirty repositories—six per domain—are not sufficient to establish universal differences among scientific software communities. The benchmark is useful as a case study and source of empirical observations, while broader validation remains future work.

## 14. Key Design Tradeoffs

AI-assisted reproducibility involves several important tradeoffs.

**Artifact presence versus artifact quality.** Automated discovery is scalable, but an artifact's existence does not establish that it contains sufficient information.

**Deterministic verification versus flexible AI guidance.** Rules provide repeatability and traceability; AI can provide contextual explanations but introduces variability.

**General practices versus domain-specific requirements.** Common principles improve consistency, while individual scientific communities may require specialized provenance, validation, data, or hardware information.

**Automation versus human verification.** Automation reduces effort but cannot determine every scientific or methodological requirement.

**Portability versus HPC specialization.** Optimized workflows may depend on architecture-specific features. Documentation should preserve essential choices while explaining what can be adapted.

**Local AI versus cloud AI.** Local inference can improve privacy and support restricted systems; cloud systems may offer different capabilities. The appropriate choice depends on security, infrastructure, governance, cost, and research requirements.

**Repository evidence versus actual reproduction.** A repository can appear well prepared while still failing at runtime. Artifact assessment and execution-based validation answer different questions and should not be conflated.

## 15. Practical Reproducibility Checklist

Before sharing or publishing scientific software, verify the following:

- [ ] The project purpose and scientific context are documented.
- [ ] Installation instructions have been tested.
- [ ] Dependencies are explicitly declared.
- [ ] Important dependency and runtime versions are recorded.
- [ ] A reproducible environment specification is available.
- [ ] Representative automated tests are included.
- [ ] Tests contain meaningful scientific or numerical assertions where appropriate.
- [ ] Data sources and preprocessing steps are documented.
- [ ] AI model versions, parameters, seeds, and metrics are recorded when applicable.
- [ ] Important experiments can be linked to source-code revisions.
- [ ] Container definitions are provided when they improve portability.
- [ ] HPC compiler, module, scheduler, accelerator, and resource information is documented when applicable.
- [ ] A software license is included.
- [ ] Documentation explains how to reproduce at least one representative workflow.
- [ ] AI-generated recommendations are grounded in inspectable evidence.
- [ ] Important AI recommendations have been reviewed by a human.
- [ ] Reproducibility-readiness indicators are not presented as proof of successful reproduction.

## 16. Future Directions

Future work in AI-assisted reproducibility should investigate stronger integration between repository evidence and executable workflow validation. Important directions include runtime validation, automated container execution, continuous reproducibility monitoring, domain-specific assessment profiles, provenance-aware AI assistance, assessment history and trend analysis, expanded scientific-software benchmarks, and evaluation of additional local and cloud language models.

AI may eventually support increasingly automated remediation, but self-healing workflows require safeguards. Automated changes to scientific software should be reviewable, testable, reversible, and linked to evidence. Human researchers must remain responsible for scientific decisions and validation.

## 17. Conclusion

Reproducible scientific software requires more than source-code availability. Sustainable workflows depend on documentation, explicit dependencies, environment capture, testing, provenance, portable execution, and domain-appropriate configuration.

AI can make reproducibility work more accessible by helping researchers inspect evidence, understand gaps, prioritize improvements, and troubleshoot complex workflows. Its value is greatest when it is grounded in verifiable information and embedded within established research software engineering practices.

The central recommendation of this guide is therefore not to automate reproducibility judgment with AI, but to use AI carefully as an assistant to transparent, evidence-based, human-validated scientific software practice.

---
