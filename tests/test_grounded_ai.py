from checker.grounded_ai import (
    build_grounded_ai_evidence,
    compare_priority_rankings,
    _validate_response,
)

def sample_presence():
    return {
        "project_path": "/tmp/repo",
        "score": 50,
        "possible": 100,
        "percent": 50.0,
        "band": "Moderate",
        "findings": [],
    }

def sample_quality():
    return {
        "project_path": "/tmp/repo",
        "quality_score": 40,
        "quality_possible": 100,
        "quality_percent": 40.0,
        "quality_band": "Substantial",
        "quality_findings": [
            {
                "label": "Container quality",
                "earned": 0,
                "possible": 15,
                "evidence": ["none"],
                "recommendation": "Add container.",
            },
            {
                "label": "Test quality",
                "earned": 8,
                "possible": 20,
                "evidence": ["2 test files"],
                "recommendation": "Improve tests.",
            },
        ],
        "priority_actions": [
            {"label": "Container quality", "recommendation": "Add container."},
            {"label": "Test quality", "recommendation": "Improve tests."},
        ],
    }

def test_build_grounded_evidence():
    evidence = build_grounded_ai_evidence(sample_presence(), sample_quality())
    assert evidence["presence_score"]["score"] == 50
    assert evidence["quality_score"]["score"] == 40

def test_validate_rejects_uncited_recommendation():
    evidence = build_grounded_ai_evidence(sample_presence(), sample_quality())
    payload = {
        "recommendations": [
            {
                "priority": 1,
                "label": "Container quality",
                "evidence": [],
                "action": "Add Dockerfile",
                "rationale": "Missing container",
            }
        ]
    }
    result = _validate_response(payload, evidence)
    assert result["ok"] is False

def test_validate_accepts_grounded_recommendation():
    evidence = build_grounded_ai_evidence(sample_presence(), sample_quality())
    payload = {
        "recommendations": [
            {
                "priority": 1,
                "label": "Container quality",
                "evidence": ["none"],
                "action": "Add a Dockerfile",
                "rationale": "The finding has no container evidence.",
            }
        ],
        "limitations": ["Human review required"],
    }
    result = _validate_response(payload, evidence)
    assert result["ok"] is True

def test_priority_comparison():
    deterministic = [
        {"label": "Container quality"},
        {"label": "Test quality"},
        {"label": "README quality"},
    ]
    ai = {
        "recommendations": [
            {"label": "Container quality"},
            {"label": "README quality"},
            {"label": "HPC portability quality"},
        ]
    }
    result = compare_priority_rankings(deterministic, ai)
    assert result["top3_overlap_count"] == 2
