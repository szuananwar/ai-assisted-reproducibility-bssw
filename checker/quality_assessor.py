from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, List
import re


IGNORED_PARTS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    ".pytest_cache",
    ".mypy_cache",
    "dist",
    "build",
}

IGNORED_RELATIVE_PREFIXES = {
    Path("benchmark/repos"),
    Path("validation/repos"),
}


def _is_ignored(root: Path, path: Path) -> bool:
    relative = path.relative_to(root)

    if any(part in IGNORED_PARTS for part in relative.parts):
        return True

    return any(
        relative == prefix or prefix in relative.parents
        for prefix in IGNORED_RELATIVE_PREFIXES
    )

def _iter_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if _is_ignored(root, path):
            continue
        if path.is_file():
            yield path

def _read(path: Path, limit: int = 200_000) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:limit]
    except OSError:
        return ""


def _relative(root: Path, paths: Iterable[Path]) -> List[str]:
    return [str(path.relative_to(root)) for path in paths]


def _find_named(root: Path, names: set[str]) -> List[Path]:
    lowered = {name.lower() for name in names}
    return [
        path for path in _iter_files(root)
        if path.name.lower() in lowered and path.stat().st_size > 0
    ]

def _find_globs(root: Path, patterns: Iterable[str]) -> List[Path]:
    found = []
    seen = set()

    for pattern in patterns:
        for path in root.rglob(pattern):
            if _is_ignored(root, path):
                continue

            if path.is_file() and path.stat().st_size > 0:
                resolved = path.resolve()

                if resolved not in seen:
                    seen.add(resolved)
                    found.append(path)

    return found


def _score_item(
    key: str,
    label: str,
    earned: int,
    possible: int,
    evidence: List[str],
    recommendation: str,
    applicable: bool = True,
) -> Dict[str, object]:
    percent = None if not applicable else round((earned / possible) * 100, 1) if possible else 0.0
    return {
        "key": key,
        "label": label,
        "earned": earned,
        "possible": possible,
        "percent": percent,
        "evidence": evidence,
        "recommendation": recommendation,
        "applicable": applicable,
        "status": "N/A" if not applicable else "PASS" if earned == possible else "PARTIAL" if earned > 0 else "MISSING",
    }


def assess_readme_quality(root: Path) -> Dict[str, object]:
    candidates = _find_named(root, {"README.md", "README.rst", "README.txt"})
    if not candidates:
        return _score_item(
            "readme_quality", "README quality", 0, 20, [],
            "Add documentation with installation, execution, testing, citation, and reproducibility instructions."
        )

    text = "\n".join(_read(path) for path in candidates[:10]).lower()
    evidence = _relative(root, candidates[:10])
    earned = 0
    checks = [
        (4, ["install", "installation", "pip install", "conda env", "build from source"], "installation instructions"),
        (4, ["usage", "quick start", "run", "example", "python "], "execution example"),
        (4, ["test", "pytest", "ctest", "validation"], "testing instructions"),
        (4, ["citation", "cite", "doi", "citation.cff"], "citation guidance"),
        (4, ["reproduc", "seed", "environment", "container", "spack", "lock file"], "reproducibility guidance"),
    ]
    for points, terms, label in checks:
        if any(term in text for term in terms):
            earned += points
            evidence.append(label)

    return _score_item(
        "readme_quality", "README quality", earned, 20, evidence,
        "Expand documentation to cover installation, execution, tests, citation, and reproducibility."
    )


def assess_dependency_quality(root: Path) -> Dict[str, object]:
    candidates = _find_named(root, {
        "requirements.txt", "pyproject.toml", "environment.yml", "environment.yaml",
        "setup.cfg", "setup.py", "poetry.lock", "uv.lock", "conda-lock.yml",
        "package-lock.json", "Pipfile.lock"
    })
    candidates += _find_globs(root, ["requirements/*.txt", "requirements-*.txt"])

    if not candidates:
        return _score_item(
            "dependency_quality", "Dependency quality", 0, 15, [],
            "Add machine-readable dependency metadata with versions or constraints."
        )

    text = "\n".join(_read(path) for path in candidates[:20])
    lower = text.lower()
    evidence = _relative(root, candidates[:20])
    earned = 5

    if re.search(r"(^|\n)\s*[A-Za-z0-9_.-]+\s*(==|~=|>=|<=|!=)\s*[0-9]", text):
        earned += 5
        evidence.append("version constraints detected")
    if any(token in lower for token in ["python_requires", "requires-python", "python=", "python >="]):
        earned += 3
        evidence.append("runtime version declared")
    if any(path.name.lower().endswith("lock") or "lock" in path.name.lower() for path in candidates):
        earned += 2
        evidence.append("lock file detected")

    return _score_item(
        "dependency_quality", "Dependency quality", min(earned, 15), 15, evidence,
        "Constrain key dependencies, declare runtime versions, and provide a lock file where practical."
    )


def assess_container_quality(root: Path) -> Dict[str, object]:
    candidates = _find_named(root, {"Dockerfile", "Containerfile", "apptainer.def", "Singularity"})
    candidates += _find_globs(root, ["Dockerfile.*", ".devcontainer/devcontainer.json"])

    if not candidates:
        return _score_item(
            "container_quality", "Container quality", 0, 15, [],
            "Add a Docker/Podman or Apptainer/Singularity recipe, or mark this category not applicable."
        )

    text = "\n".join(_read(path) for path in candidates[:10])
    lower = text.lower()
    evidence = _relative(root, candidates[:10])
    earned = 5

    if re.search(r"from\s+\S+:[^\s]+", lower) or '"image"' in lower:
        earned += 4
        evidence.append("versioned base image detected")
    if any(x in lower for x in ["requirements.txt", "environment.yml", "pip install", "conda env", "uv sync"]):
        earned += 3
        evidence.append("dependency installation detected")
    if any(x in lower for x in ["entrypoint", "cmd", "%runscript", "postcreatecommand"]):
        earned += 3
        evidence.append("execution entry point detected")

    return _score_item(
        "container_quality", "Container quality", min(earned, 15), 15, evidence,
        "Pin the base image, install declared dependencies, and define a reproducible entry point."
    )


def assess_test_quality(root: Path) -> Dict[str, object]:
    test_files = _find_globs(root, [
        "tests/test_*.py", "test/test_*.py", "**/*_test.py",
        "**/test*.cpp", "**/test*.cxx", "**/test*.c", "**/CTestTestfile.cmake"
    ])
    ci_files = _find_globs(root, [
        ".github/workflows/*.yml", ".github/workflows/*.yaml",
        ".gitlab-ci.yml", "tox.ini", "noxfile.py", "Jenkinsfile"
    ])

    if not test_files and not ci_files:
        return _score_item(
            "test_quality", "Test quality", 0, 20, [],
            "Add executable tests and automated CI validation."
        )

    text = "\n".join(_read(path, 30_000) for path in test_files[:100])
    evidence = _relative(root, test_files[:20] + ci_files[:10])
    earned = 4 if ci_files and not test_files else 8

    if re.search(r"\bassert\b", text) or any(x in text for x in ["EXPECT_", "ASSERT_", "CHECK("]):
        earned += 4
        evidence.append("assertions detected")
    if any(x in text.lower() for x in ["approx", "allclose", "isclose", "tolerance", "rtol", "atol"]):
        earned += 4
        evidence.append("numerical tolerance checks detected")
    if ci_files:
        earned += 4
        evidence.append("automated test execution configuration detected")

    return _score_item(
        "test_quality", "Test quality", min(earned, 20), 20, evidence,
        "Add scientific/numerical correctness tests and run them automatically in CI."
    )


def assess_provenance_quality(root: Path) -> Dict[str, object]:
    candidates = _find_named(root, {
        "MLproject", "dvc.yaml", "params.yaml", "provenance.json",
        "CITATION.cff", "codemeta.json", "zenodo.json", ".zenodo.json"
    })
    if not candidates:
        return _score_item(
            "provenance_quality", "Provenance quality", 0, 15, [],
            "Record parameters, seeds, outputs, software/data versions, and citation metadata."
        )

    text = "\n".join(_read(path) for path in candidates[:20]).lower()
    evidence = _relative(root, candidates[:20])
    earned = 5
    if any(x in text for x in ["parameter", "params", "seed"]):
        earned += 4
        evidence.append("parameter/seed metadata detected")
    if any(x in text for x in ["metric", "artifact", "output", "result"]):
        earned += 3
        evidence.append("result/artifact metadata detected")
    if any(x in text for x in ["version", "commit", "doi", "release"]):
        earned += 3
        evidence.append("version/citation metadata detected")

    return _score_item(
        "provenance_quality", "Provenance quality", min(earned, 15), 15, evidence,
        "Record parameters, seeds, outputs, artifacts, and software/data versions."
    )


def assess_hpc_quality(root: Path, hpc_applicable: bool = True) -> Dict[str, object]:
    if not hpc_applicable:
        return _score_item(
            "hpc_quality", "HPC portability quality", 0, 15, [],
            "Not applicable for this repository.", applicable=False
        )

    candidates = _find_named(root, {
        "spack.yaml", "spack.lock", "module_list.txt", "compiler_info.txt",
        "CMakePresets.json"
    })
    candidates += _find_globs(root, [
        "**/*.slurm", "**/*.pbs", "**/*.lsf", "**/spack.yaml", "**/spack.lock",
        "**/module*.txt", "**/compiler*.txt"
    ])

    if not candidates:
        return _score_item(
            "hpc_quality", "HPC portability quality", 0, 15, [],
            "Add Spack, scheduler, compiler, MPI, accelerator, or module metadata."
        )

    text = "\n".join(_read(path, 30_000) for path in candidates[:30]).lower()
    evidence = _relative(root, candidates[:20])
    earned = 5
    if any(x in text for x in ["mpi", "openmpi", "mpich"]):
        earned += 3
        evidence.append("MPI metadata detected")
    if any(x in text for x in ["cuda", "rocm", "gpu", "accelerator"]):
        earned += 3
        evidence.append("accelerator metadata detected")
    if any(x in text for x in ["compiler", "gcc", "clang", "oneapi", "cray"]):
        earned += 2
        evidence.append("compiler metadata detected")
    if any(x in text for x in ["partition", "nodes", "ntasks", "walltime", "sbatch"]):
        earned += 2
        evidence.append("scheduler resource metadata detected")

    return _score_item(
        "hpc_quality", "HPC portability quality", min(earned, 15), 15, evidence,
        "Document compiler, MPI, accelerator, scheduler resources, and module/software-stack details."
    )


def assess_repository_quality(
    project_path: str | Path,
    hpc_applicable: bool = True,
) -> Dict[str, object]:
    root = Path(project_path).expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"Invalid repository path: {root}")

    findings = [
        assess_readme_quality(root),
        assess_dependency_quality(root),
        assess_container_quality(root),
        assess_test_quality(root),
        assess_provenance_quality(root),
        assess_hpc_quality(root, hpc_applicable=hpc_applicable),
    ]

    applicable = [item for item in findings if item["applicable"]]
    score = sum(item["earned"] for item in applicable)
    possible = sum(item["possible"] for item in applicable)
    percent = round(score / possible * 100, 1) if possible else 0.0

    band = (
        "Strong quality signals" if percent >= 85 else
        "Good quality signals" if percent >= 70 else
        "Moderate quality gaps" if percent >= 50 else
        "Substantial quality gaps"
    )

    priorities = sorted(
        applicable,
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
        score = "N/A" if not item["applicable"] else f"{item['earned']}/{item['possible']}"
        print(f"{item['label']:<28} {score:<7} Evidence: {evidence}")
