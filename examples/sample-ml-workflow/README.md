# Local AI-Assisted Reproducibility Assessment with Ollama

This example demonstrates how a local AI model can evaluate a scientific software repository for reproducibility and sustainability.

This implementation uses Ollama with the Gemma model and does not require:
- OpenAI API keys
- Cloud access
- Paid AI services

The goal is to support sustainable and reproducible AI workflows for scientific software and HPC environments.

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

- Python 3
- Ollama installed
- Gemma model

---

# One-Time Setup

## Install Python Dependencies

Install the required Python package:

```bash
pip3 install -r requirements.txt
```

This only needs to be done once when setting up the project.

---

# Install Ollama

Download Ollama from:

https://ollama.com/download

---

# Download Gemma Model

The script can automatically download the model if it is missing, but you may also install it manually:

```bash
ollama pull gemma3:1b
```

You may also use:

```bash
ollama pull gemma3:4b
```

for improved response quality.

---

# Run the Tool

```bash
python3 ai_repo_assessor.py
```

The script will automatically:
- verify Ollama installation,
- check whether the Gemma model exists,
- download the model if missing,
- evaluate the repository,
- generate a reproducibility assessment report.

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
