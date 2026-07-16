from contextlib import contextmanager
from pathlib import Path
from urllib.parse import urlparse
import html, json, shutil, subprocess, tempfile, uuid

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
            check=True, capture_output=True, text=True, timeout=180
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
            ai = {"ok": False, "message": f"AI unavailable: {type(exc).__name__}: {exc}"}
    return presence, quality, ai

def create_assessment_id():
    return uuid.uuid4().hex

def write_reports(output_root, assessment_id, repository_url, repository_name, presence, quality, ai):
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
    return html_path, json_path
