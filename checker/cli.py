from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional, Sequence, Tuple
from urllib.parse import urlparse

from checker.quality_assessor import assess_repository_quality
from checker.reproducibility_checker import assess_repository


def _github_clone_url(value: str) -> Tuple[str, str]:
    parsed = urlparse(value.strip())
    if parsed.scheme != "https" or parsed.hostname != "github.com":
        raise ValueError(
            "Only public HTTPS GitHub URLs are supported, for example "
            "https://github.com/owner/repository."
        )
    parts = [part for part in parsed.path.strip("/").split("/") if part]
    if len(parts) < 2:
        raise ValueError("The GitHub URL must include both owner and repository.")
    owner, repository = parts[0], parts[1]
    if repository.endswith(".git"):
        repository = repository[:-4]
    return f"https://github.com/{owner}/{repository}.git", repository


def _prepare_repository(source: str) -> Tuple[Path, Optional[Path], str]:
    local_path = Path(source).expanduser()
    if local_path.is_dir():
        resolved = local_path.resolve()
        return resolved, None, resolved.name

    clone_url, repository_name = _github_clone_url(source)
    temporary_root = Path(tempfile.mkdtemp(prefix="repropilot-cli-"))
    destination = temporary_root / repository_name
    try:
        subprocess.run(
            ["git", "clone", "--depth", "1", "--filter=blob:none", clone_url, str(destination)],
            check=True,
            capture_output=True,
            text=True,
            timeout=180,
        )
    except subprocess.TimeoutExpired as exc:
        shutil.rmtree(temporary_root, ignore_errors=True)
        raise RuntimeError("Repository cloning timed out after 180 seconds.") from exc
    except subprocess.CalledProcessError as exc:
        shutil.rmtree(temporary_root, ignore_errors=True)
        message = exc.stderr.strip() or exc.stdout.strip() or "Unknown Git error"
        raise RuntimeError(f"Repository cloning failed: {message}") from exc
    return destination, temporary_root, repository_name


def _build_report(source: str, project_path: Path, repository_name: str, domain: str, hpc_applicable: bool) -> Dict[str, Any]:
    presence = assess_repository(project_path, domain=domain)
    quality = assess_repository_quality(project_path, hpc_applicable=hpc_applicable)
    return {
        "source": source,
        "repository_name": repository_name,
        "presence": presence,
        "quality": quality,
    }


def _print_summary(report: Dict[str, Any]) -> None:
    presence = report["presence"]
    quality = report["quality"]
    print("ReproPilot Assessment")
    print("=" * 72)
    print(f"Repository: {report['repository_name']}")
    print(f"Presence:   {presence['score']}/{presence['possible']} ({presence['percent']:.1f}%) — {presence['band']}")
    print(f"Quality:    {quality['quality_score']}/{quality['quality_possible']} ({quality['quality_percent']:.1f}%) — {quality['quality_band']}")
    print("\nPresence checklist")
    print("-" * 72)
    for item in presence.get("findings", []):
        evidence = ", ".join(item.get("found_paths", [])) or "none"
        print(f"[{item.get('status',''):<7}] {item.get('label',''):<30} {item.get('earned',0):>2}/{item.get('possible',0):<2} {evidence}")
    print("\nTop priority actions")
    print("-" * 72)
    priorities = quality.get("priority_actions", [])
    if not priorities:
        print("No priority actions returned.")
    else:
        for index, item in enumerate(priorities, start=1):
            print(f"{index}. {item.get('label','Unlabeled priority')}: {item.get('recommendation','')}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="repropilot",
        description="Assess reproducibility artifact presence and quality for a local repository or public GitHub repository.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    assess_parser = subparsers.add_parser("assess", help="Assess a repository.")
    assess_parser.add_argument("source", help="Local repository path or public HTTPS GitHub URL.")
    assess_parser.add_argument(
        "--domain",
        default="general",
        choices=["general", "biomedical", "climate", "hpc-simulation"],
        help="Presence-scoring domain profile. Default: general.",
    )
    hpc_group = assess_parser.add_mutually_exclusive_group()
    hpc_group.add_argument("--hpc", dest="hpc_applicable", action="store_true", help="Include HPC portability checks.")
    hpc_group.add_argument("--no-hpc", dest="hpc_applicable", action="store_false", help="Mark HPC portability checks as not applicable.")
    assess_parser.set_defaults(hpc_applicable=True)
    assess_parser.add_argument("--output", type=Path, help="Write the complete assessment to a JSON file.")
    assess_parser.add_argument("--json", action="store_true", help="Print the complete JSON report instead of the summary.")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    temporary_root: Optional[Path] = None
    try:
        project_path, temporary_root, repository_name = _prepare_repository(args.source)
        report = _build_report(args.source, project_path, repository_name, args.domain, args.hpc_applicable)
        if args.output:
            output_path = args.output.expanduser().resolve()
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
            if not args.json:
                print(f"JSON report saved to: {output_path}")
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            _print_summary(report)
        return 0
    except (ValueError, RuntimeError, OSError) as exc:
        print(f"ReproPilot error: {exc}", file=sys.stderr)
        return 2
    finally:
        if temporary_root is not None:
            shutil.rmtree(temporary_root, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
