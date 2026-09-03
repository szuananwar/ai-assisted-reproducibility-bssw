# Best Practices Guide: Sustainable AI and Reproducible Scientific Software

**2026 Better Scientific Software Fellowship — Milestone 2 Draft**

**Author:** Suzan Anwar, Ph.D.  
**Project:** Sustainable AI: Best Practices for Reproducible Scientific Software Development

## 1. Introduction

Scientific software increasingly combines source code, data, machine-learning models, complex dependency stacks, specialized hardware, and high-performance computing (HPC) environments. Reproducing a computational result therefore requires more than preserving source code. Researchers must also capture how software was configured, which dependencies and tools were used, how experiments were executed, and what evidence supports the reported results.

AI-enabled workflows introduce additional challenges. Results may depend on model versions, training parameters, random seeds, preprocessing decisions, accelerator hardware, and rapidly changing software libraries. HPC workflows introduce further dependencies on compilers, MPI implementations, GPU software stacks, environment modules, schedulers, and site-specific configurations.

This guide presents practical best practices for improving the **reproducibility readiness** and sustainability of scientific software, with particular attention to AI-enabled and HPC workflows. It accompanies ReproPilot, an open-source framework developed through the Better Scientific Software Fellowship to assess repository evidence and provide grounded guidance for improvement.

Reproducibility readiness is not the same as successful reproduction. Repository inspection can determine whether important artifacts and documentation are present and whether they contain useful information, but it cannot by itself prove scientific correctness, numerical validity, data availability, hardware equivalence, or successful execution of an entire workflow. Reproducibility assessment should therefore combine automated evidence with expert review and, when possible, runtime validation.

## 2. Core Principles of Reproducible Scientific Software

A reproducible scientific software project should make it possible for another researcher—or the original research team months later—to understand what was done, reconstruct the software environment, execute the intended workflow, and interpret the outputs.

### 2.1 Version control

Use a version-control system such as Git for source code, configuration, documentation, and other text-based project artifacts. Commit changes regularly and use meaningful commit messages. Releases, tags, or commit identifiers should be associated with important experiments and publications so that the exact software state can be recovered.

Large datasets and model artifacts should generally not be stored directly in ordinary Git history. Instead, document their versions and locations and use appropriate data- or artifact-versioning mechanisms when needed.

### 2.2 Documentation

Every repository should provide a clear entry point, normally a `README.md`. At minimum, documentation should explain:

- the purpose and scientific context of the software;
- installation requirements;
- required dependencies;
- how to configure the environment;
- how to execute a basic workflow or example;
- expected inputs and outputs;
- testing instructions;
- HPC requirements when applicable; and
- how to obtain required data or models.

Documentation should be tested as part of the workflow rather than treated as a static description. Commands that no longer work can make an otherwise complete repository difficult to reproduce.

### 2.3 Dependency management

Dependencies should be explicitly declared rather than assumed. Common mechanisms include `requirements.txt`, `pyproject.toml`, `environment.yml`, lock files, and Spack environments.

Record versions when version differences may affect behavior. Overly loose dependencies can make environments change unexpectedly, while excessively rigid dependencies can reduce portability. The appropriate level of pinning depends on the project and should balance repeatability, security updates, and maintainability.

### 2.4 Environment capture

A dependency list alone may not capture the complete execution environment. Scientific workflows can depend on Python or compiler versions, CUDA or ROCm versions, MPI implementations, system libraries, environment modules, and hardware capabilities.

Use environment specifications such as Conda environments, Spack environments, lock files, or containers where appropriate. For HPC workflows, document the site-specific information required to reconstruct or adapt the environment.

### 2.5 Data and model provenance

Document where datasets and pretrained models originate, which versions were used, how they were transformed, and which artifacts correspond to reported experiments. Where licensing or privacy restrictions prevent redistribution, provide instructions for authorized users to obtain the data and document required preprocessing.

## 3. AI-Assisted Reproducibility

AI can help researchers identify reproducibility gaps and translate technical findings into practical remediation steps. However, AI-generated assessments should not replace transparent evidence or human judgment.

ReproPilot follows a separation between **deterministic assessment** and **AI-assisted interpretation**. Deterministic rules inspect repository evidence and remain authoritative for the assessment. The optional local large language model receives verified findings and can prioritize deficiencies or explain possible improvements. It does not independently assign or modify repository scores.

This architecture provides several advantages:

- assessment results remain traceable to repository evidence;
- the same repository state and rubric can be assessed consistently;
- AI recommendations can be constrained to observed deficiencies;
- local inference can support private, restricted, or air-gapped environments; and
- researchers can use deterministic assessment even when an LLM is unavailable.

### 3.1 Grounding AI recommendations

AI recommendations should be grounded in verified evidence. Instead of asking a model to infer repository conditions freely, provide structured findings such as missing tests, incomplete environment specifications, or absent container recipes. The model can then explain why the deficiency matters and suggest an appropriate improvement.

### 3.2 Limitations of AI guidance

LLMs may produce unsupported, overly generic, or technically inappropriate recommendations. Model behavior can also vary across versions and prompts. AI guidance should therefore be treated as decision support. Important recommendations should be reviewed by researchers or research software engineers before implementation.

## 4. Code Quality, Testing, and Continuous Integration

Testing is essential for sustainable scientific software because it helps determine whether software changes alter expected behavior.

### 4.1 Unit tests

Unit tests should verify small, well-defined software components. Scientific tests should include meaningful assertions rather than only checking that code executes without crashing.

### 4.2 Workflow and integration tests

Integration tests should exercise interactions among components, while workflow tests should verify representative end-to-end paths. Small reference datasets are often useful because they make tests fast enough for routine execution.

### 4.3 Numerical validation

Scientific software may require tolerance-based comparisons rather than exact equality. Document why tolerances are scientifically and numerically appropriate. When results vary across architectures or accelerators, distinguish expected floating-point differences from scientifically meaningful changes.

### 4.4 Continuous integration

Continuous integration (CI) can automatically run tests when code changes. A useful CI workflow may verify installation, run unit and integration tests, check representative workflows, and validate documentation or configuration files.

HPC software may require additional testing strategies because production systems are not always directly available to public CI services. Tools and site-specific test systems can complement conventional CI for compiler, scheduler, accelerator, and multi-node validation.

## 5. Environment and Dependency Management

Scientific software should provide enough information to recreate or approximate its software environment.

### 5.1 Python dependency files

A `requirements.txt` or `pyproject.toml` can describe Python dependencies. Where exact environments matter, consider lock files or documented tested versions.

### 5.2 Conda environments

An `environment.yml` can capture Python packages and non-Python dependencies available through Conda channels. Include the environment name, required channels, and important package versions.

### 5.3 Spack for HPC software stacks

Spack is useful for managing scientific software stacks that depend on compilers, MPI libraries, GPU support, and architecture-specific packages. A `spack.yaml` can document the intended environment and improve portability between HPC systems.

When using Spack, document important compiler, architecture, and variant assumptions rather than assuming that the same concretization will be appropriate everywhere.

## 6. Containers and Portable Execution

Containers can package software dependencies and execution environments into reusable artifacts. Docker is widely used for development and cloud environments, while Apptainer is commonly used on HPC systems.

A useful container definition should document:

- the base image;
- dependency installation;
- application installation;
- runtime configuration;
- expected entry points or commands; and
- any external data or hardware requirements.

Containers improve portability but do not guarantee complete reproducibility. Host kernels, GPU drivers, processor architectures, external data, and distributed runtime environments may still affect results. Container definitions should therefore complement rather than replace ordinary environment documentation.

## 7. HPC Reproducibility and Portability

HPC workflows require additional metadata beyond ordinary application dependencies. Relevant information may include:

- scheduler and job-submission scripts;
- compiler and compiler version;
- MPI implementation;
- GPU accelerator type;
- CUDA or ROCm version;
- environment modules;
- node and process counts;
- CPU or GPU resource requests;
- thread settings;
- filesystem assumptions; and
- architecture-specific build options.

Portable HPC documentation should distinguish requirements that are scientifically essential from settings that are specific to one computing center. A reproducible workflow should make it clear how another user can adapt site-specific configuration without changing the scientific method.

## 8. Tracking AI and Computational Experiments

AI experiments frequently involve many combinations of parameters, datasets, preprocessing steps, model versions, random seeds, and software environments. These should be recorded systematically.

At minimum, retain:

- model architecture or identifier;
- dataset version and preprocessing procedure;
- train/validation/test split information;
- random seeds;
- hyperparameters;
- software environment;
- hardware or accelerator information;
- training and evaluation metrics; and
- links between outputs and the corresponding source-code revision.

Experiment-tracking tools such as MLflow can automate portions of this process. Other provenance mechanisms may be more appropriate for particular domains. The key principle is that reported results should be connected to the configuration and artifacts that produced them.

## 9. ReproPilot Reproducibility-Readiness Assessment

ReproPilot provides an indicator-based assessment of repository reproducibility readiness. The deterministic rubric examines evidence across eight core categories.

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

The weights represent explicit methodological choices and should not be interpreted as universal scientific constants. Different communities may reasonably prioritize different artifacts. Future domain-specific profiles can adapt the rubric while preserving transparency about the criteria used.

### 9.1 Artifact presence versus artifact quality

Finding a file does not mean that the file provides sufficient information. A repository may contain a README that lacks installation instructions, or a test directory containing tests with weak assertions. ReproPilot therefore distinguishes artifact presence from quality-aware evaluation.

Quality assessment considers factors such as documentation completeness, dependency pinning, runtime declarations, container reproducibility, test assertions, CI configuration, provenance metadata, and HPC portability information.

### 9.2 Interpreting the score

A ReproPilot score summarizes evidence found under the selected rubric. It does **not** guarantee:

- scientific correctness;
- numerical validity;
- successful workflow execution;
- dataset availability;
- hardware equivalence; or
- complete experimental reproduction.

Scores should be interpreted alongside repository findings, expert judgment, and runtime validation when feasible.

## 10. Case Study: Assessing a Scientific AI Repository

A typical ReproPilot workflow begins with a scientific software repository and performs deterministic artifact discovery followed by quality-aware assessment. For example, a repository may include source code, a README, and dependency specifications but lack automated tests, containerization, and experiment tracking.

The deterministic assessment records these findings. The optional grounded AI layer can then prioritize verified gaps and suggest practical actions, such as adding representative tests, recording experiment parameters, or providing a container definition. Because AI operates on verified assessment findings, its recommendations remain separated from the authoritative score.

The researcher can implement selected improvements and reassess the repository. This before-and-after process makes reproducibility work incremental: teams can identify gaps, prioritize feasible improvements, and document progress rather than attempting to solve every reproducibility issue at once.

## 11. Recommended Repository Structure

There is no single correct structure for all scientific software, but a repository may include:

```text
project/
├── README.md
├── LICENSE
├── pyproject.toml or requirements.txt
├── environment.yml
├── spack.yaml
├── Dockerfile or apptainer.def
├── src/
├── tests/
├── scripts/
├── configs/
├── data/ or data-access documentation
├── notebooks/
├── docs/
└── experiment/provenance metadata
```

Only include artifacts that are relevant to the project. For example, an HPC-specific Spack environment should not be required for software that has no HPC use case. Reproducibility assessment should be applicability-aware rather than rewarding files simply for existing.

## 12. Minimum Reproducibility Package

Before releasing scientific software or computational results, researchers should aim to provide a minimum reproducibility package containing:

1. a clear README describing the project and workflow;
2. installation and execution instructions;
3. explicit dependency information;
4. an environment specification appropriate to the project;
5. automated tests with meaningful assertions;
6. data and model provenance or access instructions;
7. experiment configuration and parameter records;
8. a software license;
9. container or portable execution information when useful; and
10. HPC configuration and job information when applicable.

The exact package should reflect the scientific domain, software architecture, and intended audience.

## 13. Best Practices for Research Teams and Students

Reproducibility is easier when it is integrated into everyday development rather than added immediately before publication.

Teams should establish shared conventions for repository structure, version control, code review, dependency updates, experiment naming, and documentation. New contributors should be able to follow the documented setup process without relying entirely on verbal instructions from the original developer.

Students should be introduced early to version control, environment management, testing, documentation, and experiment tracking. These practices improve both scientific reliability and workforce preparation by treating research software as a maintained scholarly product.

## 14. Key Design Tradeoffs

Reproducibility engineering involves tradeoffs rather than one universal solution.

**Artifact presence versus artifact quality.** Automated discovery is scalable, but the existence of an artifact does not establish that it is useful.

**Deterministic assessment versus flexible AI guidance.** Rules provide repeatability and traceability; AI can provide contextual explanations but introduces variability and must remain grounded.

**General indicators versus domain-specific requirements.** A common rubric enables comparison, while specialized domains may require additional provenance, hardware, data, or validation evidence.

**Automation versus human verification.** Automated assessment reduces effort but cannot determine every scientific or methodological requirement.

**Portability versus HPC specialization.** Highly optimized workflows may depend on architecture-specific features. Reproducibility documentation should preserve those choices while explaining how workflows may be adapted.

**Local AI versus cloud AI.** Local models can improve privacy and support restricted systems, while larger cloud models may offer additional capabilities. The appropriate choice depends on security, infrastructure, cost, and research requirements.

## 15. Practical Reproducibility Checklist

Before sharing or publishing a scientific software repository, verify the following:

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
- [ ] Automated assessment findings have been reviewed by a human.

## 16. Future Directions

Future work in AI-assisted reproducibility should move beyond static repository inspection toward stronger validation of executable workflows. Important directions include runtime validation, automated container execution, continuous reproducibility monitoring, domain-specific assessment profiles, assessment history and trend analysis, expanded scientific-software benchmarks, and evaluation of additional local language models.

AI may also support increasingly automated remediation, but self-healing workflows require careful safeguards. Automated changes to scientific software should be reviewable, testable, and linked to evidence. Human researchers must remain responsible for scientific decisions and validation.

## 17. Conclusion

Reproducible scientific software requires more than source-code availability. Sustainable workflows depend on documentation, explicit dependencies, environment capture, testing, provenance, portable execution, and domain-appropriate configuration. AI can help researchers understand and prioritize reproducibility improvements, but it should complement transparent deterministic evidence rather than replace it.

ReproPilot demonstrates one approach to combining reproducibility-readiness assessment, artifact-quality evaluation, HPC-aware indicators, and grounded local AI guidance. The broader goal is to make reproducibility practices practical, incremental, and accessible to scientific software teams while preserving the expert judgment required for trustworthy computational research.

---

## Milestone 2 Draft Status

This document is the comprehensive draft of the Best Practices Guide prepared for Milestone 2 of the 2026 Better Scientific Software Fellowship. It is intended for technical review and community feedback before final revision and publication during Milestone 3.
