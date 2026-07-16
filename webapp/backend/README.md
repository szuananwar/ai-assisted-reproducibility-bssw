# ReproPilot Web API — Phase 6.1

Run from the ReproPilot repository root.

```bash
python3 -m venv .venv-web
source .venv-web/bin/activate
python3 -m pip install -r webapp/backend/requirements.txt
PYTHONPATH=. uvicorn webapp.backend.app.main:app --reload
```

Open `http://127.0.0.1:8000/docs`.

Test:

```bash
PYTHONPATH=webapp/backend:. python3 -m pytest webapp/backend/tests -v
```

Example request:

```bash
curl -X POST http://127.0.0.1:8000/api/assess -H "Content-Type: application/json" -d '{"repository_url":"https://github.com/szuananwar/ai-assisted-reproducibility-bssw","hpc_applicable":true,"use_ai":false}'
```
