from typing import Any, Dict, Optional

from pydantic import BaseModel, HttpUrl


class AssessmentRequest(BaseModel):
    repository_url: HttpUrl
    hpc_applicable: bool = True
    use_ai: bool = False


class AssessmentResponse(BaseModel):
    assessment_id: str
    repository_url: str
    repository_name: str
    presence: Dict[str, Any]
    quality: Dict[str, Any]
    ai: Optional[Dict[str, Any]] = None
    html_report_path: str
    json_report_path: str
    pdf_report_path: str
