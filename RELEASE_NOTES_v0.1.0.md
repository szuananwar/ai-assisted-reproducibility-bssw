# ReproPilot v0.1.0

ReproPilot v0.1.0 is the first research-software release of the framework.

## Highlights

- deterministic reproducibility-presence assessment;
- artifact-quality assessment;
- HPC-aware scoring;
- grounded local-AI prioritization;
- 30-repository scientific software benchmark;
- statistical analysis and publication figures;
- notebook GUI;
- FastAPI backend and interactive web dashboard;
- installable Python package;
- `repropilot assess` command-line interface;
- automated CI across Python 3.9–3.12.

## Installation

```bash
git clone https://github.com/szuananwar/ai-assisted-reproducibility-bssw.git
cd ai-assisted-reproducibility-bssw
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e ".[all]"
```

## CLI Example

```bash
repropilot assess https://github.com/numpy/numpy --no-hpc
```

## Web Dashboard

```bash
PYTHONPATH=webapp/backend:. uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/
```

## Limitations

ReproPilot measures repository reproducibility readiness. It does not guarantee
scientific correctness, numerical validity, successful workflow execution,
dataset availability, or hardware equivalence.
