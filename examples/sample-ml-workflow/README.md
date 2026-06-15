# Local AI-Assisted Reproducibility Assessment with Ollama

This example demonstrates how a local AI model can evaluate a scientific software repository for reproducibility and sustainability.

This implementation uses Ollama with the Gemma model and does not require:
- OpenAI API keys
- Cloud access
- Paid AI services

The goal is to support sustainable and reproducible AI workflows for scientific software and HPC environments.

---

> Note: Many HPC centers, research labs, and preconfigured development environments may already provide Python, Ollama, and AI models. In these environments, users can often run the tool immediately without additional installation steps.

---

# Purpose

This example demonstrates how AI can assist researchers and developers in evaluating scientific software repositories using a reproducibility and sustainability rubric.

The assessment evaluates:

- README clarity
- Installation instructions
- Dependency management
- Environment reproducibility
- HPC configuration support
- Testing practices
- Containerization support
- Experiment tracking
- Open science compliance
- Sustainability and maintainability

---

# Reproducibility Checklist & Scoring Rubric

| Category | Item | Points |
|---|---|---|
| Documentation | README with run instructions | 15 |
| Dependencies | requirements.txt | 15 |
| Environment | environment.yml | 10 |
| HPC Environment | spack.yaml | 10 |
| Testing | tests/ folder | 15 |
| Containerization | Dockerfile or Apptainer file | 15 |
| Experiment Tracking | MLflow logs or tracking file | 10 |
| Open Science | LICENSE file | 10 |
| Total |  | 100 |

## Score Interpretation

- **85–100:** Strong reproducibility
- **70–84:** Good, but improvements needed
- **50–69:** Moderate reproducibility risk
- **Below 50:** High reproducibility risk

---
## Why This Rubric?

The rubric focuses on practical indicators of software reproducibility and sustainability that are commonly recommended in scientific software engineering and HPC communities. The criteria were selected because they can be evaluated consistently and provide actionable guidance for improving repository quality.

---

# Example Repositories

## HPC

https://github.com/kokkos/kokkos

## Package Management

https://github.com/spack/spack

## Scientific Python

https://github.com/numpy/numpy

## Machine Learning

https://github.com/pytorch/pytorch

---

# Requirements

* Python 3
* Ollama
* Gemma model (automatically downloaded if missing)

---

# Quick Start

Many researchers and HPC users already have Python, Ollama, and the required model installed in their environment.

If Python, Ollama, and the Gemma model are already installed, simply run:

```bash
python3 ai_repo_assessor.py
```

The script will automatically:

* Verify that Ollama is installed
* Check whether the required Gemma model is available
* Download the model if it is missing
* Generate a reproducibility assessment report

No additional setup is required.

---

# One-Time Setup for New Environments

If you are using a new system that does not already have the required software installed:

## Install Python Dependencies

```bash
pip3 install -r requirements.txt
```

## Install Ollama

Download and install Ollama from:

https://ollama.com/download

## Download the Gemma Model

The script can automatically download the model if it is missing, but you may also install it manually:

```bash
ollama pull gemma3:4b
```

---

# Run the Tool

```bash
python3 ai_repo_assessor.py
```

---

# Example Input

```text
https://github.com/kokkos/kokkos
```

---

# Connection to BSSw Fellowship Project

This example supports the BSSw Fellowship project:

**"Sustainable AI: Best Practices for Reproducible Scientific Software Development"**

by demonstrating how local AI models can assist in evaluating reproducibility and sustainability practices for scientific software and HPC workflows.

