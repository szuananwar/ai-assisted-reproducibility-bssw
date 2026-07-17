"""Tests for the standalone ReproPilot GUI."""

from checker.gui import (
    presence_rows,
    priority_rows,
    quality_rows,
    validate_github_url,
)


def test_validate_github_url():
    url, name = validate_github_url(
        "https://github.com/szuananwar/ai-assisted-reproducibility-bssw"
    )

    assert url.endswith(
        "szuananwar/ai-assisted-reproducibility-bssw.git"
    )
    assert name == "ai-assisted-reproducibility-bssw"


def test_validate_github_url_rejects_non_github_url():
    try:
        validate_github_url("https://example.com/project")
    except ValueError:
        pass
    else:
        raise AssertionError("Non-GitHub URL should be rejected.")


def test_presence_rows():
    result = {
        "findings": [
            {
                "label": "Documentation",
                "status": "present",
                "earned": 15,
                "possible": 15,
                "found_paths": ["README.md"],
                "recommendation": "None",
            }
        ]
    }

    rows = presence_rows(result)

    assert rows[0][0] == "Documentation"
    assert rows[0][2] == "15/15"
    assert rows[0][3] == "README.md"


def test_quality_rows_handles_not_applicable():
    result = {
        "quality_findings": [
            {
                "label": "HPC",
                "status": "not_applicable",
                "applicable": False,
                "earned": 0,
                "possible": 10,
                "percent": 0,
                "evidence": [],
                "recommendation": "",
            }
        ]
    }

    rows = quality_rows(result)

    assert rows[0][2] == "N/A"


def test_priority_rows():
    result = {
        "priority_actions": [
            {
                "category": "Testing",
                "recommendation": "Add automated tests",
            }
        ]
    }

    rows = priority_rows(result)

    assert rows == [["1", "Testing", "Add automated tests"]]
