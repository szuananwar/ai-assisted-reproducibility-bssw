from pathlib import Path

from app.services import write_reports


def test_write_reports_creates_html_json_and_pdf(tmp_path: Path):
    presence = {
        "percent": 50,
        "findings": [
            {
                "label": "README",
                "status": "pass",
                "earned": 10,
                "possible": 10,
                "found_paths": ["README.md"],
                "recommendation": "Keep documentation current.",
            }
        ],
    }
    quality = {
        "quality_percent": 75,
        "quality_band": "Good",
        "quality_findings": [
            {
                "label": "Documentation",
                "status": "pass",
                "earned": 15,
                "possible": 20,
                "evidence": ["README.md"],
                "recommendation": "Add a complete worked example.",
                "applicable": True,
            }
        ],
        "priority_actions": [
            {"label": "Documentation", "recommendation": "Add a worked example."}
        ],
    }

    html_path, json_path, pdf_path = write_reports(
        tmp_path,
        "test-assessment",
        "https://github.com/example/project",
        "project",
        presence,
        quality,
        None,
    )

    assert html_path.is_file()
    assert json_path.is_file()
    assert pdf_path.is_file()
    assert pdf_path.read_bytes().startswith(b"%PDF")
    assert pdf_path.stat().st_size > 500
