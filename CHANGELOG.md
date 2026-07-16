# Changelog

All notable changes to ReproPilot will be documented in this file.

The format is based on Keep a Changelog, and the project follows semantic
versioning where practical.

## [Unreleased]

### Planned

- PDF report generation
- Docker Compose deployment
- expanded domain-specific profiles
- hosted deployment guidance
- release automation

## [0.1.0] - 2026-07-16

### Added

- deterministic 100-point reproducibility artifact assessment;
- quality-aware scoring for documentation, dependencies, containers, tests,
  provenance, and HPC portability;
- recursive artifact discovery and false-negative reduction;
- not-applicable handling for non-HPC projects;
- grounded local AI prioritization using Ollama;
- AI-versus-deterministic agreement experiments;
- benchmark evaluation across 30 scientific repositories and five domains;
- descriptive and inferential statistical analysis;
- publication-quality figures and tables;
- interactive Jupyter notebook GUI;
- FastAPI assessment backend;
- browser-based ReproPilot dashboard;
- downloadable HTML and JSON reports;
- standard Python package configuration;
- `repropilot assess` command-line interface;
- GitHub Actions continuous integration across Python 3.9 through 3.12;
- regression tests preventing nested benchmark repositories from contaminating
  assessment evidence.

### Security

- public HTTPS GitHub URL validation;
- shallow temporary cloning;
- automatic temporary-directory cleanup;
- no execution of assessed repository source code.
