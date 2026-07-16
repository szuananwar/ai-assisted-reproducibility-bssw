from __future__ import annotations
import argparse, csv, json, shutil, subprocess, sys
from pathlib import Path

REPOSITORIES = [
    {"name": "BuildTest", "url": "https://github.com/buildtesters/buildtest.git", "domain": "hpc-simulation", "purpose": "HPC-focused testing framework"},
    {"name": "NumPy", "url": "https://github.com/numpy/numpy.git", "domain": "general", "purpose": "Mature scientific Python library"},
    {"name": "Brain Tumor Viskores ViT", "url": "https://github.com/szuananwar/brain-tumor-viskores-vit.git", "domain": "biomedical", "purpose": "Domain-specific AI/HPC scientific workflow"},
]

def run(cmd):
    print("$", " ".join(cmd))
    subprocess.run(cmd, check=True)

def get_value(obj, key, default=None):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)

def normalize_finding(f):
    if isinstance(f, dict):
        return {
            "label": f.get("label", f.get("key", "Unknown")),
            "status": f.get("status", "UNKNOWN"),
            "earned": f.get("earned", 0),
            "possible": f.get("possible", 0),
            "found_paths": f.get("found_paths", []),
            "recommendation": f.get("recommendation", ""),
        }
    return {
        "label": getattr(f, "label", getattr(f, "key", "Unknown")),
        "status": getattr(f, "status", "UNKNOWN"),
        "earned": getattr(f, "earned", 0),
        "possible": getattr(f, "possible", 0),
        "found_paths": getattr(f, "found_paths", []),
        "recommendation": getattr(f, "recommendation", ""),
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--repropilot-root", type=Path, default=Path.cwd())
    p.add_argument("--workdir", type=Path, default=Path("validation/repos"))
    args = p.parse_args()

    project_root = args.repropilot_root.resolve()
    sys.path.insert(0, str(project_root))
    from checker.reproducibility_checker import assess_repository

    workdir = args.workdir.resolve()
    workdir.mkdir(parents=True, exist_ok=True)
    rows, detailed = [], []

    for repo in REPOSITORIES:
        dest = workdir / repo["name"].lower().replace(" ", "-")
        if not dest.exists():
            run(["git", "clone", "--depth", "1", repo["url"], str(dest)])
        else:
            print(f"Using existing clone: {dest}")

        result = assess_repository(dest, repo["domain"])

        findings = [normalize_finding(f) for f in get_value(result, "findings", [])]
        score = get_value(result, "score", 0)
        possible = get_value(result, "possible", 100)
        percent = get_value(result, "percent", round((score / possible) * 100, 1) if possible else 0.0)
        band = get_value(result, "band", "Unknown")

        row = {
            "repository": repo["name"],
            "url": repo["url"],
            "purpose": repo["purpose"],
            "domain": repo["domain"],
            "score": score,
            "possible": possible,
            "percent": percent,
            "band": band,
        }
        rows.append(row)
        detailed.append({**row, "findings": findings})

    out = project_root / "validation"
    out.mkdir(exist_ok=True)

    with (out / "phase2_results.csv").open("w", newline="", encoding="utf-8") as h:
        w = csv.DictWriter(h, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)

    (out / "phase2_results.json").write_text(json.dumps(detailed, indent=2), encoding="utf-8")

    lines = [
        "# Phase 2: External Repository Validation",
        "",
        "ReproPilot was evaluated on three repositories representing mature scientific software, HPC tooling, and a domain-specific AI/HPC workflow.",
        "",
        "| Repository | Domain | Score | Interpretation |",
        "|---|---|---:|---|",
    ]
    for r in rows:
        lines.append(f"| {r['repository']} | {r['domain']} | {r['score']}/{r['possible']} ({r['percent']}%) | {r['band']} |")

    lines += [
        "",
        "## Interpretation",
        "",
        "The rubric measures repository readiness signals, not scientific correctness. Scores should be interpreted alongside manual review of documentation, tests, container builds, numerical validation, and domain-specific requirements.",
        "",
        "## Detailed findings",
        "",
    ]

    for item in detailed:
        lines += [
            f"### {item['repository']}",
            "",
            f"- Purpose: {item['purpose']}",
            f"- Domain profile: `{item['domain']}`",
            f"- Score: **{item['score']}/{item['possible']} ({item['percent']}%)**",
            "",
        ]
        for f in item["findings"]:
            paths = ", ".join(f["found_paths"]) or "none"
            lines.append(f"- **{f['label']}** — {f['status']} ({f['earned']}/{f['possible']}); found: {paths}")
        lines.append("")

    (out / "phase2_report.md").write_text("\n".join(lines), encoding="utf-8")
    print("Created:")
    print(out / "phase2_results.csv")
    print(out / "phase2_results.json")
    print(out / "phase2_report.md")

if __name__ == "__main__":
    main()
