from pathlib import Path
from checker.quality_assessor import assess_repository_quality

def write(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def test_recursive_license_independent_quality_inputs(tmp_path):
    write(tmp_path, "docs/README.md", "Install, run, pytest, citation, reproducibility.")
    write(tmp_path, "requirements/base.txt", "numpy==2.0.0")
    result = assess_repository_quality(tmp_path, hpc_applicable=False)
    assert result["quality_percent"] > 0

def test_nested_ci_and_tests_are_detected(tmp_path):
    write(tmp_path, "src/tests/test_math.py", "def test_x():\n    assert abs(1.0-1.0) < 1e-8")
    write(tmp_path, ".github/workflows/tests.yml", "name: tests")
    result = assess_repository_quality(tmp_path, hpc_applicable=False)
    test_item = next(x for x in result["quality_findings"] if x["key"] == "test_quality")
    assert test_item["earned"] >= 12

def test_hpc_not_applicable_changes_denominator(tmp_path):
    result = assess_repository_quality(tmp_path, hpc_applicable=False)
    assert result["quality_possible"] == 85
    hpc = next(x for x in result["quality_findings"] if x["key"] == "hpc_quality")
    assert hpc["status"] == "N/A"

def test_recursive_hpc_detection(tmp_path):
    write(tmp_path, "deploy/jobs/run.slurm", "#SBATCH --nodes=2\nmodule load gcc\nsrun app")
    result = assess_repository_quality(tmp_path, hpc_applicable=True)
    hpc = next(x for x in result["quality_findings"] if x["key"] == "hpc_quality")
    assert hpc["earned"] > 0

def test_nested_benchmark_repositories_are_ignored(tmp_path):
    from checker.quality_assessor import assess_repository_quality

    # Main repository
    (tmp_path / "README.md").write_text(
        "# Main repository\n",
        encoding="utf-8",
    )

    # Simulated benchmark repository
    nested = tmp_path / "benchmark" / "repos" / "external-project"
    nested.mkdir(parents=True)

    (nested / "Dockerfile").write_text(
        "FROM python:3.11\n",
        encoding="utf-8",
    )

    (nested / "requirements.txt").write_text(
        "numpy==2.0.0\n",
        encoding="utf-8",
    )

    result = assess_repository_quality(
        tmp_path,
        hpc_applicable=False,
    )

    evidence = []

    for finding in result["quality_findings"]:
        evidence.extend(finding.get("evidence", []))

    assert not any(
        item.startswith("benchmark/repos/")
        for item in evidence
    )
