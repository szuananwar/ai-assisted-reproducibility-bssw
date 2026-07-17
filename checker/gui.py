"""Browser-based graphical interface for ReproPilot."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from urllib.parse import urlparse


from checker.quality_assessor import assess_repository_quality
from checker.reproducibility_checker import assess_repository

try:
    from checker.ai_priority_ranker import ai_priority_labels

    AI_AVAILABLE = True
except Exception:
    AI_AVAILABLE = False


DEFAULT_REPOSITORY = (
    "https://github.com/szuananwar/ai-assisted-reproducibility-bssw"
)


def validate_github_url(url: str) -> tuple[str, str]:
    """Validate and normalize a public GitHub repository URL."""

    parsed = urlparse(url.strip())

    if parsed.scheme != "https" or parsed.hostname != "github.com":
        raise ValueError("Enter a public HTTPS GitHub repository URL.")

    parts = [part for part in parsed.path.strip("/").split("/") if part]

    if len(parts) < 2:
        raise ValueError("The URL must include a GitHub owner and repository.")

    owner = parts[0]
    repository = parts[1].removesuffix(".git")

    canonical_url = f"https://github.com/{owner}/{repository}.git"
    return canonical_url, repository


def clone_repository(url: str) -> tuple[Path, Path, str]:
    """Clone a public GitHub repository into a temporary directory."""

    canonical_url, repository_name = validate_github_url(url)

    temporary_root = Path(tempfile.mkdtemp(prefix="repropilot-gui-"))
    destination = temporary_root / repository_name

    try:
        subprocess.run(
            [
                "git",
                "clone",
                "--depth",
                "1",
                "--filter=blob:none",
                canonical_url,
                str(destination),
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=180,
        )
    except subprocess.CalledProcessError as exc:
        shutil.rmtree(temporary_root, ignore_errors=True)
        message = exc.stderr.strip() or exc.stdout.strip()
        raise RuntimeError(f"Git clone failed: {message}") from exc
    except subprocess.TimeoutExpired as exc:
        shutil.rmtree(temporary_root, ignore_errors=True)
        raise RuntimeError("Repository cloning exceeded 180 seconds.") from exc

    return temporary_root, destination, repository_name


def presence_rows(result: dict) -> list[list[str]]:
    """Convert presence findings into rows for the GUI table."""

    rows = []

    for finding in result.get("findings", []):
        rows.append(
            [
                str(finding.get("label", "")),
                str(finding.get("status", "")),
                f"{finding.get('earned', 0)}/{finding.get('possible', 0)}",
                ", ".join(finding.get("found_paths", [])) or "None",
                str(finding.get("recommendation", "")),
            ]
        )

    return rows


def quality_rows(result: dict) -> list[list[str]]:
    """Convert quality findings into rows for the GUI table."""

    rows = []

    for finding in result.get("quality_findings", []):
        applicable = finding.get("applicable", True)

        score = (
            f"{finding.get('earned', 0)}/{finding.get('possible', 0)}"
            if applicable
            else "N/A"
        )

        rows.append(
            [
                str(finding.get("label", "")),
                str(finding.get("status", "")),
                score,
                str(finding.get("percent", "")),
                ", ".join(finding.get("evidence", [])) or "None",
                str(finding.get("recommendation", "")),
            ]
        )

    return rows


def priority_rows(result: dict) -> list[list[str]]:
    """Convert deterministic priorities into display rows."""

    rows = []

    for index, priority in enumerate(result.get("priority_actions", []), start=1):
        if isinstance(priority, dict):
            rows.append(
                [
                    str(index),
                    str(
                        priority.get("category")
                        or priority.get("label")
                        or priority.get("title")
                        or ""
                    ),
                    str(
                        priority.get("recommendation")
                        or priority.get("action")
                        or priority.get("description")
                        or ""
                    ),
                ]
            )
        else:
            rows.append([str(index), "", str(priority)])

    return rows


def assess_github_repository(
    repository_url: str,
    hpc_applicable: bool,
    run_ai: bool,
):
    """Clone and assess a public GitHub repository."""

    temporary_root: Path | None = None
    started = time.perf_counter()

    try:
        temporary_root, repository_path, repository_name = clone_repository(
            repository_url
        )

        presence = assess_repository(repository_path)

        quality = assess_repository_quality(
            repository_path,
            hpc_applicable=hpc_applicable,
        )

        ai_result = None

        if run_ai:
            if not AI_AVAILABLE:
                raise RuntimeError(
                    "The grounded AI component is not available in this installation."
                )

            ai_result = ai_priority_labels(quality)

        elapsed = time.perf_counter() - started

        presence_score = float(presence.get("percent", 0))
        quality_score = float(quality.get("quality_percent", 0))

        summary = f"""
## Assessment completed

**Repository:** `{repository_name}`  
**Presence score:** {presence_score:.1f}%  
**Artifact quality score:** {quality_score:.1f}%  
**HPC-specific checks:** {"Enabled" if hpc_applicable else "Disabled"}  
**Grounded local AI:** {"Enabled" if run_ai else "Disabled"}  
**Assessment time:** {elapsed:.1f} seconds
"""

        report = {
            "repository_url": repository_url,
            "repository_name": repository_name,
            "presence": presence,
            "quality": quality,
            "ai": ai_result,
        }

        report_directory = Path.cwd() / "repropilot_reports"
        report_directory.mkdir(parents=True, exist_ok=True)

        safe_name = repository_name.replace("/", "_")
        report_path = report_directory / f"{safe_name}_assessment.json"
        report_path.write_text(
            json.dumps(report, indent=2, default=str),
            encoding="utf-8",
        )

        ai_text = (
            json.dumps(ai_result, indent=2, default=str)
            if ai_result is not None
            else "Grounded local AI was not requested."
        )

        return (
            summary,
            presence_rows(presence),
            quality_rows(quality),
            priority_rows(quality),
            ai_text,
            str(report_path),
        )

    except Exception as exc:
        error_message = (
            f"## Assessment failed\n\n"
            f"**{type(exc).__name__}:** {exc}"
        )

        return error_message, [], [], [], "No AI results.", None

    finally:
        if temporary_root is not None:
            shutil.rmtree(temporary_root, ignore_errors=True)


def create_gui():
    """Construct and return the ReproPilot Gradio application."""

    try:
        import gradio as gr
    except ImportError as exc:
        raise RuntimeError(
            'The GUI dependencies are not installed. '
            'Install them with: python -m pip install -e ".[gui]"'
        ) from exc

    with gr.Blocks(title="ReproPilot Repository Assessor") as application:
        gr.Markdown(
            """
# ReproPilot Interactive Repository Assessor

Paste a public GitHub repository URL, select the assessment options,
and click **Assess Repository**.
"""
        )

        with gr.Row():
            repository_url = gr.Textbox(
                value=DEFAULT_REPOSITORY,
                label="Public GitHub repository URL",
                placeholder="https://github.com/owner/repository",
                scale=4,
            )

        with gr.Row():
            hpc_applicable = gr.Checkbox(
                value=True,
                label="Apply HPC-specific checks",
            )

            run_ai = gr.Checkbox(
                value=False,
                label="Run grounded local AI",
                interactive=AI_AVAILABLE,
            )

        assess_button = gr.Button(
            "Assess Repository",
            variant="primary",
        )

        summary = gr.Markdown()

        gr.Markdown("## Reproducibility checklist results")

        presence_table = gr.Dataframe(
            headers=[
                "Category",
                "Status",
                "Score",
                "Evidence",
                "Recommendation",
            ],
            datatype=["str", "str", "str", "str", "str"],
            interactive=False,
            wrap=True,
        )

        gr.Markdown("## Artifact quality results")

        quality_table = gr.Dataframe(
            headers=[
                "Category",
                "Status",
                "Score",
                "Percent",
                "Evidence",
                "Recommendation",
            ],
            datatype=["str", "str", "str", "str", "str", "str"],
            interactive=False,
            wrap=True,
        )

        gr.Markdown("## Top deterministic priorities")

        priorities_table = gr.Dataframe(
            headers=["Priority", "Category", "Recommended action"],
            datatype=["str", "str", "str"],
            interactive=False,
            wrap=True,
        )

        with gr.Accordion("Grounded AI priorities", open=False):
            ai_output = gr.Code(
                label="AI output",
                language="json",
            )

        report_file = gr.File(
            label="Download JSON assessment report",
            interactive=False,
        )

        assess_button.click(
            fn=assess_github_repository,
            inputs=[
                repository_url,
                hpc_applicable,
                run_ai,
            ],
            outputs=[
                summary,
                presence_table,
                quality_table,
                priorities_table,
                ai_output,
                report_file,
            ],
        )

    return application


def launch_gui(
    share: bool = False,
    server_name: str = "127.0.0.1",
    port: int = 7860,
) -> None:
    """Launch ReproPilot in the default web browser."""

    application = create_gui()

    application.launch(
        share=share,
        inbrowser=True,
        server_name=server_name,
        server_port=port,
    )


def main() -> None:
    """Terminal entry point for the ReproPilot GUI."""

    parser = argparse.ArgumentParser(
        description="Launch the ReproPilot graphical interface."
    )

    parser.add_argument(
        "--share",
        action="store_true",
        help="Create a temporary public Gradio sharing link.",
    )

    parser.add_argument(
        "--server-name",
        default="127.0.0.1",
        help="Server address. Use 0.0.0.0 for remote/container access.",
    )

    parser.add_argument(
        "--port",
        type=int,
        default=7860,
        help="Port on which the GUI will run.",
    )

    arguments = parser.parse_args()

    launch_gui(
        share=arguments.share,
        server_name=arguments.server_name,
        port=arguments.port,
    )


if __name__ == "__main__":
    main()
