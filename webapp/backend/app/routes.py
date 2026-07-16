from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.models import AssessmentRequest, AssessmentResponse
from app.services import cloned_repository, create_assessment_id, run_repropilot, write_reports

router = APIRouter(prefix="/api")
REPORT_DIR = Path(__file__).resolve().parents[2] / "results"

@router.post("/assess", response_model=AssessmentResponse)
def assess(request: AssessmentRequest):
    assessment_id = create_assessment_id()
    repository_url = str(request.repository_url)
    try:
        with cloned_repository(repository_url) as (repo_path, repo_name):
            presence, quality, ai = run_repropilot(
                repo_path, request.hpc_applicable, request.use_ai
            )
            html_path, json_path = write_reports(
                REPORT_DIR, assessment_id, repository_url, repo_name,
                presence, quality, ai
            )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Assessment failed: {type(exc).__name__}: {exc}") from exc

    return AssessmentResponse(
        assessment_id=assessment_id,
        repository_url=repository_url,
        repository_name=repo_name,
        presence=presence,
        quality=quality,
        ai=ai,
        html_report_path=f"/api/reports/{assessment_id}.html",
        json_report_path=f"/api/reports/{assessment_id}.json",
    )

@router.get("/reports/{filename}")
def report(filename: str):
    path = REPORT_DIR / Path(filename).name
    if not path.is_file():
        raise HTTPException(status_code=404, detail="Report not found.")
    return FileResponse(path)
