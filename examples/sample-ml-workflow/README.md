# Local AI-Assisted Reproducibility Assessment with Ollama

This example demonstrates how a local AI model can evaluate a scientific software repository for reproducibility and sustainability.

This version uses Ollama and the Gemma model. It does not require an OpenAI API key, cloud account, or payment.

## Purpose

The goal is to support sustainable and reproducible AI workflows by showing how AI can help assess scientific software repositories.

The assessment checks:

- README clarity
- Installation instructions
- License availability
- Requirements or environment files
- Documentation quality
- Testing or CI/CD
- Reproducibility of results
- Sustainability and maintainability
## Example Repositories

HPC:
https://github.com/kokkos/kokkos

Package Management:
https://github.com/spack/spack

Scientific Python:
https://github.com/numpy/numpy

Machine Learning:
https://github.com/pytorch/pytorch

## Requirements

- Python 3
- Ollama installed
- Gemma model downloaded

## Install Ollama Model

```bash
ollama pull gemma3:1b
