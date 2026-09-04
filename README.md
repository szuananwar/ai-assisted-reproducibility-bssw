# AI-Assisted Reproducibility in Scientific Software

**2026 Better Scientific Software Fellowship Project**

**Fellowship project:** *Sustainable AI: Best Practices for Reproducible Scientific Software Development*  
**Fellow:** Suzan Anwar, Ph.D., Philander Smith University

## Project Overview

This repository supports a 2026 Better Scientific Software (BSSw) Fellowship project investigating how artificial intelligence can assist reproducible and sustainable scientific software development, with particular attention to AI-enabled and high-performance computing (HPC) workflows.

The project is broader than any single software tool. Its primary outputs are a practical best-practices guide, hands-on tutorial materials, reusable reproducibility resources, and research prototypes that demonstrate and evaluate selected approaches to AI-assisted reproducibility.

The central principle is that AI should **support rather than replace transparent reproducibility practices and human scientific judgment**. AI assistance is most useful when it is grounded in verifiable evidence, its recommendations are traceable, and researchers remain responsible for scientific validation.

## Research Motivation

Modern scientific software may depend on source code, datasets, machine-learning models, software environments, compilers, accelerators, HPC schedulers, experiment configurations, and many other artifacts. Reproducing a result therefore requires more than making source code publicly available.

AI introduces both opportunities and risks. It can help researchers identify missing reproducibility information, explain technical gaps, prioritize improvements, assist with documentation, and support workflow debugging. At the same time, AI can generate unsupported recommendations or obscure the evidence behind an assessment if it is used without appropriate constraints.

This fellowship explores practical ways to combine established research software engineering practices with carefully grounded AI assistance.

## Fellowship Goals

The project aims to:

- develop practical best practices for reproducible and sustainable AI-enabled scientific software;
- create hands-on tutorials that researchers and students can reuse;
- examine where AI can responsibly assist reproducibility work;
- emphasize version control, documentation, testing, environment capture, provenance, and portable execution;
- address reproducibility considerations specific to HPC and AI workflows;
- demonstrate human-in-the-loop and evidence-grounded approaches to AI assistance;
- provide reusable templates and examples for the scientific software community; and
- share lessons and outcomes with the BSSw and broader research software engineering communities.

## Fellowship Deliverables

### Best Practices Guide

The Milestone 2 comprehensive draft is available in [`guide/best-practices-guide.md`](guide/best-practices-guide.md). It covers reproducible scientific workflows, software sustainability, testing and continuous integration, environment and dependency management, containers, HPC portability, experiment provenance, responsible AI assistance, practical recommendations, and case studies.

### Tutorial Series

The organized Milestone 2 tutorial series is available in [`notebooks/README.md`](notebooks/README.md). It provides a seven-part learning path covering:

1. reproducibility foundations;
2. environments and dependencies;
3. testing and continuous integration;
4. experiment tracking and provenance;
5. HPC reproducibility and portability;
6. responsible AI-assisted reproducibility; and
7. ReproPilot as a supporting case study.

Executable draft notebooks for Tutorials 1–6 and the Tutorial 7 ReproPilot case-study materials are available in [`notebooks/`](notebooks/). The current Milestone 2 refinement phase focuses on beta testing, technical review, feedback integration, and preparation for final publication.

### Reusable Templates

The [`templates/`](templates/) directory contains example environment, container, HPC, and experiment-tracking artifacts that can be adapted for scientific software projects.

### Feedback and Workshop Planning

Milestone 2 review and beta-testing evidence is organized under [`feedback/`](feedback/), including the [`Milestone 2 feedback log`](feedback/milestone2-feedback.md) and [`tutorial beta-testing plan`](feedback/tutorial-beta-testing.md). Preliminary community workshop planning is documented in [`workshop-planning.md`](workshop-planning.md).

## Examples and Research Prototypes

The fellowship uses practical examples and prototypes to explore selected ideas from the guide. These implementations are supporting research artifacts rather than the overall identity of the fellowship project.

### ReproPilot

**ReproPilot** is a research prototype developed within the fellowship to investigate one approach to AI-assisted reproducibility-readiness assessment. It combines deterministic repository evidence, quality-aware artifact analysis, and optional grounded local AI prioritization.

The deterministic assessment remains authoritative. The AI component is constrained to work from verified findings and is used as complementary decision support rather than as an independent reproducibility judge.

ReproPilot has also served as an experimental platform for studying artifact presence versus artifact quality, cross-domain repository characteristics, and agreement between deterministic findings and grounded AI prioritization.

Detailed ReproPilot documentation is available in [`examples/repropilot/README.md`](examples/repropilot/README.md).

## Repository Organization

```text
ai-assisted-reproducibility-bssw/
├── README.md                  # Fellowship project landing page
├── guide/                     # Best Practices Guide
├── notebooks/                 # Tutorial series and executable notebooks
│   └── README.md              # Tutorial learning path
├── feedback/                  # Milestone 2 review and beta-testing records
├── workshop-planning.md       # Preliminary community workshop plan
├── templates/                 # Reusable reproducibility templates
├── examples/                  # Examples and research prototypes
│   ├── repropilot/            # ReproPilot documentation
│   └── sample-ml-workflow/    # Example scientific/ML workflow
├── checker/                   # ReproPilot prototype implementation
├── validation/                # Prototype validation artifacts
├── benchmark/                 # Prototype benchmark evaluation
├── analysis/                  # Statistical and agreement analysis
├── tests/                     # Automated tests
└── webapp/                    # Prototype web interface
```

The ReproPilot source directories remain at the repository root for now to preserve working imports, tests, notebooks, benchmark scripts, and web-application paths. Reorganizing implementation code can be considered separately after the fellowship deliverables are stabilized.

## Milestone Progress

### Milestone 1 — Guide Outline and Prototype Tutorial

Initial guide organization and prototype tutorial materials established the foundation for the fellowship work.

### Milestone 2 — Complete Drafts and Feedback

Current work includes:

- a comprehensive Best Practices Guide draft;
- a seven-part tutorial series with executable draft notebooks for Tutorials 1–6 and ReproPilot case-study materials for Tutorial 7;
- documented environment/setup instructions for tutorial users;
- dedicated logs and procedures for technical feedback and tutorial beta testing; and
- a preliminary community workshop plan with a tentative audience, format, learning outcomes, agenda, and candidate collaborators.

The remaining Milestone 2 work is to **collect actual reviewer and beta-tester feedback and record the resulting revisions** in the repository logs.

### Milestone 3 — Final Publication and Dissemination

The final phase will revise and publish the guide and tutorials, support community dissemination, prepare the fellowship webinar, and communicate project outcomes through BSSw channels.

## Guiding Principles

Across the fellowship materials, several principles are emphasized:

- **Evidence before automation:** AI recommendations should be connected to observable evidence.
- **Human oversight:** researchers remain responsible for scientific and methodological decisions.
- **Reproducibility readiness is not proof of reproduction:** repository artifacts can indicate preparedness but cannot guarantee scientific correctness or successful execution.
- **Quality matters as well as presence:** having a README, test directory, environment file, or container recipe does not necessarily mean that the artifact is complete or useful.
- **Applicability matters:** not every scientific software project requires the same artifacts, especially across HPC and non-HPC settings.
- **Sustainability and reproducibility reinforce one another:** documentation, testing, version control, provenance, and maintainable environments improve both immediate reproducibility and long-term software health.

## Community and Feedback

The Milestone 2 materials are intended for collaborator, mentor, researcher, and community feedback. Review activity and revisions are tracked in [`feedback/milestone2-feedback.md`](feedback/milestone2-feedback.md), while tutorial usability testing is tracked in [`feedback/tutorial-beta-testing.md`](feedback/tutorial-beta-testing.md). Feedback will be used to improve technical accuracy, relevance, tutorial usability, and final recommendations before Milestone 3 publication.

## Fellowship Acknowledgment

This work is being conducted as part of the **2026 Better Scientific Software Fellowship** project:

**Sustainable AI: Best Practices for Reproducible Scientific Software Development**

## License

This project is distributed under the terms provided in the repository's [`LICENSE`](LICENSE) file.

## Author

**Suzan Anwar, Ph.D.**  
Department of Computer Science  
Philander Smith University  
Little Rock, Arkansas, USA
