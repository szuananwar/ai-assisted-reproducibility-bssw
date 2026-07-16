from contextlib import contextmanager
from pathlib import Path
from urllib.parse import urlparse
import html
import json
import shutil
import subprocess
import tempfile
import uuid

from fpdf import FPDF


def validate_repository_url(url: str):
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname != "github.com":
        raise ValueError("Only public HTTPS github.com repositories are supported.")
    parts = [p for p in parsed.path.strip("/").split("/") if p]
    if len(parts) < 2:
        raise ValueError("Repository URL must include owner and repository.")
    owner, repo = parts[0], parts[1].removesuffix(".git")
    return f"https://github.com/{owner}/{repo}.git", repo


@contextmanager
def cloned_repository(url: str):
    canonical, repo_name = validate_repository_url(url)
    temp_root = Path(tempfile.mkdtemp(prefix="repropilot-"))
    destination = temp_root / repo_name
    try:
        subprocess.run(
            ["git", "clone", "--depth", "1", "--filter=blob:none", canonical, str(destination)],
            check=True,
            capture_output=True,
            text=True,
            timeout=180,
        )
        yield destination, repo_name
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("Repository clone timed out.") from exc
    except subprocess.CalledProcessError as exc:
        msg = exc.stderr.strip() or exc.stdout.strip() or "Unknown git error"
        raise RuntimeError(f"Repository clone failed: {msg}") from exc
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)


def run_repropilot(repo_path: Path, hpc_applicable: bool, use_ai: bool):
    from checker.reproducibility_checker import assess_repository
    from checker.quality_assessor import assess_repository_quality

    presence = assess_repository(repo_path)
    quality = assess_repository_quality(repo_path, hpc_applicable=hpc_applicable)
    ai = None
    if use_ai:
        try:
            from checker.ai_priority_ranker import ai_priority_labels

            ai = ai_priority_labels(quality)
        except Exception as exc:
            ai = {
                "ok": False,
                "message": f"AI unavailable: {type(exc).__name__}: {exc}",
            }
    return presence, quality, ai


def create_assessment_id():
    return uuid.uuid4().hex


def _safe_pdf_text(value):
    """Convert values to text supported by the built-in PDF font."""
    return str(value).encode("latin-1", "replace").decode("latin-1")


def _add_pdf_heading(pdf, text, size=14):
    pdf.set_font("Helvetica", "B", size)
    pdf.multi_cell(0, 8, _safe_pdf_text(text))
    pdf.ln(1)


def _add_pdf_paragraph(pdf, text, size=10):
    pdf.set_font("Helvetica", "", size)
    pdf.multi_cell(0, 6, _safe_pdf_text(text))
    pdf.ln(1)


def _write_pdf_report(
    pdf_path,
    repository_url,
    repository_name,
    presence,
    quality,
    ai,
):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_title("ReproPilot Assessment Report")
    pdf.set_author("ReproPilot")
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 12, "ReproPilot Assessment Report", new_x="LMARGIN", new_y="NEXT")
    _add_pdf_paragraph(pdf, f"Repository: {repository_name}")
    _add_pdf_paragraph(pdf, repository_url)

    _add_pdf_heading(pdf, "Summary", 15)
    summary = (
        f"Presence score: {presence.get('percent', 'N/A')}% | "
        f"Quality score: {quality.get('quality_percent', 'N/A')}% | "
        f"Interpretation: {quality.get('quality_band', 'N/A')}"
    )
    _add_pdf_paragraph(pdf, summary, 11)

    _add_pdf_heading(pdf, "Reproducibility Checklist")
    findings = presence.get("findings", [])
    if findings:
        for index, item in enumerate(findings, start=1):
            label = item.get("label", "Unnamed category")
            status = item.get("status", "unknown")
            earned = item.get("earned", 0)
            possible = item.get("possible", 0)
            evidence = ", ".join(item.get("found_paths", []) or []) or "None"
            recommendation = item.get("recommendation", "")
            _add_pdf_paragraph(
                pdf,
                f"{index}. {label} [{status}] - {earned}/{possible}\n"
                f"Evidence: {evidence}\nRecommendation: {recommendation}",
            )
    else:
        _add_pdf_paragraph(pdf, "No presence findings were returned.")

    _add_pdf_heading(pdf, "Artifact Quality")
    quality_findings = quality.get("quality_findings", [])
    if quality_findings:
        for index, item in enumerate(quality_findings, start=1):
            label = item.get("label", "Unnamed category")
            status = item.get("status", "unknown")
            if item.get("applicable") is False:
                score = "N/A"
            else:
                score = f"{item.get('earned', 0)}/{item.get('possible', 0)}"
            evidence = ", ".join(item.get("evidence", []) or []) or "None"
            recommendation = item.get("recommendation", "")
            _add_pdf_paragraph(
                pdf,
                f"{index}. {label} [{status}] - {score}\n"
                f"Evidence: {evidence}\nRecommendation: {recommendation}",
            )
    else:
        _add_pdf_paragraph(pdf, "No quality findings were returned.")

    _add_pdf_heading(pdf, "Top Deterministic Priorities")
    priorities = quality.get("priority_actions", [])
    if priorities:
        for index, item in enumerate(priorities, start=1):
            if isinstance(item, dict):
                label = item.get("label", "Priority")
                recommendation = item.get("recommendation", "")
                text = f"{index}. {label}: {recommendation}"
            else:
                text = f"{index}. {item}"
            _add_pdf_paragraph(pdf, text)
    else:
        _add_pdf_paragraph(pdf, "No deterministic priorities were returned.")

    _add_pdf_heading(pdf, "Grounded AI")
    if ai is None:
        _add_pdf_paragraph(pdf, "Grounded AI was not requested.")
    else:
        _add_pdf_paragraph(pdf, json.dumps(ai, indent=2))

    _add_pdf_heading(pdf, "Interpretation")
    _add_pdf_paragraph(
        pdf,
        "ReproPilot measures repository reproducibility readiness. "
        "It does not guarantee scientific correctness, numerical validity, "
        "workflow execution, data availability, or hardware equivalence.",
    )

    pdf.output(str(pdf_path))


def write_reports(
    output_root,
    assessment_id,
    repository_url,
    repository_name,
    presence,
    quality,
    ai,
):
    output_root.mkdir(parents=True, exist_ok=True)
    payload = {
        "assessment_id": assessment_id,
        "repository_url": repository_url,
        "repository_name": repository_name,
        "presence": presence,
        "quality": quality,
        "ai": ai,
    }

    json_path = output_root / f"{assessment_id}.json"
    html_path = output_root / f"{assessment_id}.html"
    pdf_path = output_root / f"{assessment_id}.pdf"

    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    page = f"""<!doctype html><html><head><meta charset="utf-8">
    <title>ReproPilot Report</title>
    <style>body{{font-family:Arial;max-width:900px;margin:40px auto;padding:0 20px}}
    .cards{{display:flex;gap:16px;flex-wrap:wrap}}.card{{border:1px solid #ddd;border-radius:10px;padding:16px}}
    pre{{background:#f6f6f6;padding:12px;overflow:auto}}</style></head><body>
    <h1>ReproPilot Assessment Report</h1>
    <p><strong>Repository:</strong> {html.escape(repository_url)}</p>
    <div class="cards">
    <div class="card"><strong>Presence</strong><br>{presence.get("percent","N/A")}%</div>
    <div class="card"><strong>Quality</strong><br>{quality.get("quality_percent","N/A")}%</div>
    <div class="card"><strong>Band</strong><br>{html.escape(str(quality.get("quality_band","N/A")))}</div>
    </div><h2>Presence findings</h2><pre>{html.escape(json.dumps(presence.get("findings",[]),indent=2))}</pre>
    <h2>Quality findings</h2><pre>{html.escape(json.dumps(quality.get("quality_findings",[]),indent=2))}</pre>
    <h2>Grounded AI</h2><pre>{html.escape(json.dumps(ai,indent=2))}</pre>
    </body></html>"""
    html_path.write_text(page, encoding="utf-8")

    _write_pdf_report(
        pdf_path,
        repository_url,
        repository_name,
        presence,
        quality,
        ai,
    )

    return html_path, json_path, pdf_path
