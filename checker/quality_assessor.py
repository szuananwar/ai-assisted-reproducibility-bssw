from __future__ import annotations

from pathlib import Path
from typing import Dict, List
import json
import re


def _read(path: Path, limit: int = 200_000) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:limit]
    except OSError:
        return ""


def _find_first(root: Path, candidates: List[str]) -> Path | None:
    for rel in candidates:
        path = root / rel
        if path.is_file() and path.stat().st_size > 0:
            return path
    return None


def _score_item(key: str, label: str, earned: int, possible: int,
                evidence: List[str], recommendation: str) -> Dict[str, object]:
    return {
        "key": key,
        "label": label,
        "earned": earned,
        "possible": possible,
        "percent": round((earned / possible) * 100, 1) if possible else 0.0,
        "evidence": evidence,
        "recommendation": recommendation,
    }


def assess_readme_quality(root: Path) -> Dict[str, object]:
    path = _find_first(root, ["README.md", "README.rst"])
    if not path:
        return _score_item("readme_quality", "README quality", 0, 20, [],
                           "Add a README with installation, execution, testing, citation, and reproducibility instructions.")

    text = _read(path).lower()
    earned, evidence = 0, [str(path.relative_to(root))]

    checks = [
        (4, ["install", "installation", "pip install", "conda env"], "installation instructions"),
        (4, ["usage", "run", "example", "python "], "execution example"),
        (4, ["test", "pytest", "validation"], "testing instructions"),
        (4, ["citation", "cite", "doi", "citation.cff"], "citation guidance"),
        (4, ["reproduc", "seed", "environment", "container", "spack"], "reproducibility guidance"),
    ]
    for points, terms, label in checks:
        if any(term in text for term in terms):
            earned += points
            evidence.append(label)

    return _score_item(
        "readme_quality", "README quality", earned, 20, evidence,
        "Expand the README to cover installation, execution, tests, citation, and reproducibility."
    )


def assess_dependency_quality(root: Path) -> Dict[str, object]:
    path = _find_first(root, ["requirements.txt", "pyproject.toml", "environment.yml", "environment.yaml"])
    if not path:
        return _score_item("dependency_quality", "Dependency quality", 0, 15, [],
                           "Add a machine-readable dependency file with versions or constraints.")

    text = _read(path)
    evidence = [str(path.relative_to(root))]
    earned = 5

    pinned = bool(re.search(r"(^|\n)\s*[A-Za-z0-9_.-]+\s*(==|~=|>=|<=)\s*[0-9]", text))
    if pinned:
        earned += 5
        evidence.append("version constraints detected")

    if "python" in text.lower():
        earned += 3
        evidence.append("Python version/runtime declared")

    if any(token in text.lower() for token in ["lock", "sha256", "hash"]):
        earned += 2
        evidence.append("lock/hash evidence detected")

    return _score_item(
        "dependency_quality", "Dependency quality", min(earned, 15), 15, evidence,
        "Pin or constrain key dependencies and declare the supported runtime version."
    )


def assess_container_quality(root: Path) -> Dict[str, object]:
    path = _find_first(root, ["Dockerfile", "Containerfile", "apptainer.def", "Singularity"])
    if not path:
        return _score_item("container_quality", "Container quality", 0, 15, [],
                           "Add a Docker/Podman or Apptainer/Singularity recipe.")

    text = _read(path)
    lower = text.lower()
    earned, evidence = 5, [str(path.relative_to(root))]

    if re.search(r"from\s+\S+:[^\s]+", lower):
        earned += 4
        evidence.append("base image tag detected")
    if any(x in lower for x in ["requirements.txt", "environment.yml", "pip install", "conda env"]):
        earned += 3
        evidence.append("dependency installation detected")
    if any(x in lower for x in ["entrypoint", "cmd", "%runscript"]):
        earned += 3
        evidence.append("execution entry point detected")

    return _score_item(
        "container_quality", "Container quality", min(earned, 15), 15, evidence,
        "Pin the base image, install declared dependencies, and define a reproducible entry point."
    )


def assess_test_quality(root: Path) -> Dict[str, object]:
    test_files = []
    for pattern in ["tests/test_*.py", "test/test_*.py", "**/*_test.py"]:
        test_files.extend(root.glob(pattern))
    test_files = sorted({p.resolve() for p in test_files if p.is_file()})

    if not test_files:
        return _score_item("test_quality", "Test quality", 0, 20, [],
                           "Add executable unit, integration, or numerical validation tests.")

    text = "\n".join(_read(p, 20_000) for p in test_files[:50])
    earned, evidence = 8, [f"{len(test_files)} test files"]

    if re.search(r"\bassert\b", text):
        earned += 4
        evidence.append("assertions detected")
    if any(x in text.lower() for x in ["approx", "allclose", "isclose", "tolerance"]):
        earned += 4
        evidence.append("numerical tolerance checks detected")
    if (root / ".github" / "workflows").is_dir() or (root / "tox.ini").is_file():
        earned += 4
        evidence.append("automated test execution configuration detected")

    return _score_item(
        "test_quality", "Test quality", min(earned, 20), 20, evidence,
        "Add numerical correctness checks and execute tests automatically in CI."
    )


def assess_provenance_quality(root: Path) -> Dict[str, object]:
    candidates = ["MLproject", "dvc.yaml", "params.yaml", "provenance.json", "CITATION.cff"]
    found = [rel for rel in candidates if (root / rel).is_file() and (root / rel).stat().st_size > 0]
    earned, evidence = 0, []

    if found:
        earned += 5
        evidence.extend(found)
    content = "\n".join(_read(root / rel) for rel in found)
    if any(x in content.lower() for x in ["parameter", "params", "seed"]):
        earned += 4
        evidence.append("parameter/seed metadata detected")
    if any(x in content.lower() for x in ["metric", "artifact", "output", "result"]):
        earned += 3
        evidence.append("result/artifact metadata detected")
    if any(x in content.lower() for x in ["version", "commit", "doi"]):
        earned += 3
        evidence.append("version/citation metadata detected")

    return _score_item(
        "provenance_quality", "Provenance quality", min(earned, 15), 15, evidence,
        "Record parameters, seeds, outputs, artifacts, and software/data versions."
    )


def assess_hpc_quality(root: Path) -> Dict[str, object]:
    files = []
    for pattern in ["spack.yaml", "spack.lock", "*.slurm", "*.pbs", "*.lsf", "module_list.txt", "compiler_info.txt"]:
        files.extend(root.glob(pattern))
    files = sorted({p.resolve() for p in files if p.is_file() and p.stat().st_size > 0})

    if not files:
        return _score_item("hpc_quality", "HPC portability quality", 0, 15, [],
                           "Add Spack, scheduler, compiler, MPI, accelerator, or module metadata.")

    text = "\n".join(_read(p, 20_000) for p in files[:30]).lower()
    earned, evidence = 5, [str(p.relative_to(root)) for p in files[:8]]

    if any(x in text for x in ["mpi", "openmpi", "mpich"]):
        earned += 3
        evidence.append("MPI metadata detected")
    if any(x in text for x in ["cuda", "rocm", "gpu", "accelerator"]):
        earned += 3
        evidence.append("accelerator metadata detected")
    if any(x in text for x in ["compiler", "gcc", "clang", "oneapi", "cray"]):
        earned += 2
        evidence.append("compiler metadata detected")
    if any(x in text for x in ["partition", "nodes", "ntasks", "walltime"]):
        earned += 2
        evidence.append("scheduler resource metadata detected")

    return _score_item(
        "hpc_quality", "HPC portability quality", min(earned, 15), 15, evidence,
        "Document compiler, MPI, accelerator, scheduler resources, and module/software-stack details."
    )


def assess_repository_quality(project_path: str | Path) -> Dict[str, object]:
    root = Path(project_path).expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"Invalid repository path: {root}")

    findings = [
        assess_readme_quality(root),
        assess_dependency_quality(root),
        assess_container_quality(root),
        assess_test_quality(root),
        assess_provenance_quality(root),
        assess_hpc_quality(root),
    ]
    score = sum(item["earned"] for item in findings)
    possible = sum(item["possible"] for item in findings)
    percent = round(score / possible * 100, 1) if possible else 0.0
    band = (
        "Strong quality signals" if percent >= 85 else
        "Good quality signals" if percent >= 70 else
        "Moderate quality gaps" if percent >= 50 else
        "Substantial quality gaps"
    )
    priorities = sorted(
        findings,
        key=lambda x: (x["earned"] / x["possible"]) if x["possible"] else 1.0
    )[:3]

    return {
        "project_path": str(root),
        "quality_score": score,
        "quality_possible": possible,
        "quality_percent": percent,
        "quality_band": band,
        "quality_findings": findings,
        "priority_actions": [
            {"label": item["label"], "recommendation": item["recommendation"]}
            for item in priorities
        ],
    }


def print_quality_assessment(result: Dict[str, object]) -> None:
    print(
        f"Quality score: {result['quality_score']}/{result['quality_possible']} "
        f"({result['quality_percent']}%)"
    )
    print(f"Interpretation: {result['quality_band']}\n")
    for item in result["quality_findings"]:
        evidence = "; ".join(item["evidence"]) or "none"
        print(
            f"{item['label']:<28} {item['earned']:>2}/{item['possible']:<2} "
            f"Evidence: {evidence}"
        )
