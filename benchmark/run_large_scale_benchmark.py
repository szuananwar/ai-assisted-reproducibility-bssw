from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path


def run(cmd: list[str]) -> None:
    print("$", " ".join(cmd))
    subprocess.run(cmd, check=True)


def clone_or_update(url: str, dest: Path, refresh: bool) -> None:
    if refresh and dest.exists():
        shutil.rmtree(dest)
    if dest.exists():
        print(f"Using existing clone: {dest}")
        return
    run(["git", "clone", "--depth", "1", url, str(dest)])


def slugify(name: str) -> str:
    return "".join(c.lower() if c.isalnum() else "-" for c in name).strip("-")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--repropilot-root", type=Path, default=Path.cwd())
    p.add_argument("--manifest", type=Path, default=Path("benchmark/repositories.csv"))
    p.add_argument("--workdir", type=Path, default=Path("benchmark/repos"))
    p.add_argument("--output-dir", type=Path, default=Path("benchmark/results"))
    p.add_argument("--refresh", action="store_true")
    p.add_argument("--limit", type=int, default=None)
    args = p.parse_args()

    root = args.repropilot_root.resolve()
    sys.path.insert(0, str(root))

    from checker.reproducibility_checker import assess_repository
    from checker.quality_assessor import assess_repository_quality

    manifest = args.manifest.resolve()
    workdir = args.workdir.resolve()
    output_dir = args.output_dir.resolve()
    workdir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    rows = list(csv.DictReader(manifest.open(encoding="utf-8")))
    if args.limit:
        rows = rows[:args.limit]

    summary = []
    details = []
    failures = []

    for index, repo in enumerate(rows, start=1):
        name = repo["name"]
        domain = repo["domain"]
        url = repo["url"]
        hpc_applicable = repo["hpc_applicable"].strip().lower() == "true"
        dest = workdir / slugify(name)

        print(f"\n[{index}/{len(rows)}] {name}")
        started = time.perf_counter()

        try:
            clone_or_update(url, dest, args.refresh)
            presence = assess_repository(dest)
            quality = assess_repository_quality(dest, hpc_applicable=hpc_applicable)
            elapsed = round(time.perf_counter() - started, 3)
            file_count = sum(1 for pth in dest.rglob("*") if pth.is_file())

            quality_map = {
                item["key"]: item for item in quality["quality_findings"]
            }

            row = {
                "repository": name,
                "domain": domain,
                "url": url,
                "hpc_applicable": hpc_applicable,
                "presence_percent": presence["percent"],
                "quality_percent": quality["quality_percent"],
                "quality_possible": quality["quality_possible"],
                "readme_quality": quality_map["readme_quality"]["percent"],
                "dependency_quality": quality_map["dependency_quality"]["percent"],
                "container_quality": quality_map["container_quality"]["percent"],
                "test_quality": quality_map["test_quality"]["percent"],
                "provenance_quality": quality_map["provenance_quality"]["percent"],
                "hpc_quality": quality_map["hpc_quality"]["percent"],
                "file_count": file_count,
                "elapsed_seconds": elapsed,
                "status": "ok",
            }
            summary.append(row)
            details.append({
                **row,
                "presence": presence,
                "quality": quality,
            })
        except Exception as exc:
            failures.append({
                "repository": name,
                "domain": domain,
                "url": url,
                "error": f"{type(exc).__name__}: {exc}",
            })
            print(f"FAILED: {failures[-1]['error']}")

    if summary:
        csv_path = output_dir / "phase5_benchmark_results.csv"
        with csv_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=summary[0].keys())
            writer.writeheader()
            writer.writerows(summary)

        (output_dir / "phase5_benchmark_results.json").write_text(
            json.dumps(details, indent=2), encoding="utf-8"
        )

    (output_dir / "phase5_failures.json").write_text(
        json.dumps(failures, indent=2), encoding="utf-8"
    )

    report = [
        "# Phase 5.1 Benchmark Collection Report",
        "",
        f"- Repositories requested: {len(rows)}",
        f"- Successful assessments: {len(summary)}",
        f"- Failures: {len(failures)}",
        "",
        "| Repository | Domain | Presence | Quality | Status |",
        "|---|---|---:|---:|---|",
    ]
    for row in summary:
        report.append(
            f"| {row['repository']} | {row['domain']} | "
            f"{row['presence_percent']}% | {row['quality_percent']}% | ok |"
        )
    for row in failures:
        report.append(
            f"| {row['repository']} | {row['domain']} | — | — | failed |"
        )

    (output_dir / "phase5_benchmark_report.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print("\nCreated benchmark outputs in", output_dir)
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
