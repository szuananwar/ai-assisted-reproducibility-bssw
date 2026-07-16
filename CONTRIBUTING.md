# Contributing to ReproPilot

Thank you for helping improve ReproPilot.

## Ways to Contribute

Contributions may include:

- bug reports and fixes;
- new reproducibility-detection rules;
- new scientific-domain profiles;
- documentation improvements;
- benchmark additions;
- web, notebook, or CLI improvements;
- test coverage and validation;
- accessibility and usability improvements.

## Development Setup

```bash
git clone https://github.com/szuananwar/ai-assisted-reproducibility-bssw.git
cd ai-assisted-reproducibility-bssw

python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -e ".[all]"
```

## Create a Branch

```bash
git checkout main
git pull
git checkout -b feature/brief-description
```

## Run Tests

```bash
python3 -m pytest tests -v
PYTHONPATH=webapp/backend:. python3 -m pytest webapp/backend/tests -v
```

## Code Expectations

- Maintain compatibility with supported Python versions.
- Add or update tests for behavior changes.
- Do not execute code from assessed repositories.
- Preserve evidence-grounded and deterministic scoring behavior.
- Avoid committing generated reports, virtual environments, cloned benchmark repositories, or secrets.
- Keep recommendations traceable to repository evidence.

## Pull Requests

A pull request should include:

1. a clear summary of the change;
2. the reason for the change;
3. tests performed;
4. any limitations or follow-up work;
5. updated documentation when user-facing behavior changes.

## Reporting Problems

Use GitHub Issues for ordinary bug reports and feature requests.

For security-sensitive concerns, follow `SECURITY.md`.
