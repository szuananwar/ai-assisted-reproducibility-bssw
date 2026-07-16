from pathlib import Path
from checker.quality_assessor import assess_repository_quality

def write(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def test_empty_repo_scores_zero(tmp_path):
    result = assess_repository_quality(tmp_path)
    assert result["quality_score"] == 0

def test_quality_repo_scores_high(tmp_path):
    write(tmp_path, "README.md", "# Demo\nInstall with pip install.\nRun python app.py.\nUse pytest.\nCitation DOI.\nReproducibility seed container.")
    write(tmp_path, "requirements.txt", "numpy==2.0.0\npytest==8.0.0\npython>=3.11\n")
    write(tmp_path, "Dockerfile", "FROM python:3.11-slim\nCOPY requirements.txt .\nRUN pip install -r requirements.txt\nCMD [\"python\", \"app.py\"]\n")
    write(tmp_path, "tests/test_demo.py", "import numpy as np\n\ndef test_x():\n    assert np.isclose(1.0, 1.0)\n")
    write(tmp_path, ".github/workflows/tests.yml", "name: tests\n")
    write(tmp_path, "MLproject", "parameters: seed\nmetrics: accuracy\nartifact: model\nversion: 1\n")
    write(tmp_path, "spack.yaml", "spack:\n  specs:\n  - openmpi\n  - cuda\n  compiler: gcc\n")
    result = assess_repository_quality(tmp_path)
    assert result["quality_percent"] >= 80

def test_priority_actions_are_returned(tmp_path):
    write(tmp_path, "README.md", "# Minimal")
    result = assess_repository_quality(tmp_path)
    assert len(result["priority_actions"]) == 3
