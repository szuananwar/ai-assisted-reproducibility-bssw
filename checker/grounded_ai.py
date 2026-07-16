from __future__ import annotations

from pathlib import Path
from typing import Dict, List
import json
import os
import urllib.error
import urllib.request


def build_grounded_ai_evidence(
    presence: Dict[str, object],
    quality: Dict[str, object],
) -> Dict[str, object]:
    return {
        "repository_path": presence.get("project_path") or quality.get("project_path"),
        "presence_score": {
            "score": presence.get("score"),
            "possible": presence.get("possible"),
            "percent": presence.get("percent"),
            "band": presence.get("band"),
        },
        "quality_score": {
            "score": quality.get("quality_score"),
            "possible": quality.get("quality_possible"),
            "percent": quality.get("quality_percent"),
            "band": quality.get("quality_band"),
        },
        "presence_findings": presence.get("findings", []),
        "quality_findings": quality.get("quality_findings", []),
        "deterministic_priority_actions": quality.get("priority_actions", []),
    }


def _validate_response(payload: Dict[str, object], evidence: Dict[str, object]) -> Dict[str, object]:
    recommendations = payload.get("recommendations")
    if not isinstance(recommendations, list):
        return {"ok": False, "message": "AI response is missing a recommendations list.", "raw": payload}

    valid_labels = {
        item.get("label")
        for item in evidence.get("quality_findings", [])
        if isinstance(item, dict)
    }
    validated = []
    for item in recommendations[:3]:
        if not isinstance(item, dict):
            continue
        label = item.get("label")
        cited_evidence = item.get("evidence", [])
        action = item.get("action")
        rationale = item.get("rationale")
        if label not in valid_labels:
            continue
        if not isinstance(cited_evidence, list) or not cited_evidence:
            continue
        if not isinstance(action, str) or not action.strip():
            continue
        if not isinstance(rationale, str) or not rationale.strip():
            continue
        validated.append(
            {
                "label": label,
                "priority": item.get("priority", len(validated) + 1),
                "evidence": cited_evidence,
                "action": action.strip(),
                "rationale": rationale.strip(),
            }
        )

    if not validated:
        return {
            "ok": False,
            "message": "AI recommendations failed evidence-grounding validation.",
            "raw": payload,
        }

    return {
        "ok": True,
        "recommendations": validated,
        "limitations": payload.get("limitations", []),
    }


def grounded_llm_recommendations(
    evidence: Dict[str, object],
    model: str | None = None,
    url: str | None = None,
    timeout: int = 90,
) -> Dict[str, object]:
    model = model or os.getenv("OLLAMA_MODEL", "gemma3:1b")
    url = url or os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")

    schema = {
        "recommendations": [
            {
                "priority": 1,
                "label": "Exact quality finding label",
                "evidence": ["Exact evidence string from the supplied findings"],
                "action": "Specific remediation action",
                "rationale": "Why this action follows from the cited evidence",
            }
        ],
        "limitations": ["One concise limitation"],
    }

    prompt = f"""
You are assisting a research software engineer.

Use only the JSON evidence supplied below.
Do not change or recalculate any deterministic score.
Do not invent files, tests, tools, or capabilities.
Every recommendation must:
1. Use an exact label from quality_findings.
2. Cite one or more exact evidence strings from that finding.
3. Recommend a concrete repository change.
4. Explain why the action follows from the cited evidence.

Return valid JSON only with this schema:
{json.dumps(schema, indent=2)}

Repository evidence:
{json.dumps(evidence, indent=2)[:28000]}
""".strip()

    request = urllib.request.Request(
        url,
        data=json.dumps({"model": model, "prompt": prompt, "stream": False}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
        outer = json.loads(body)
        raw_response = outer.get("response")
        if not raw_response:
            return {"ok": False, "message": "Ollama response did not contain 'response'.", "raw": outer}
        try:
            parsed = json.loads(raw_response)
        except json.JSONDecodeError:
            start = raw_response.find("{")
            end = raw_response.rfind("}")
            if start == -1 or end == -1 or end <= start:
                return {"ok": False, "message": "Model did not return valid JSON.", "raw_text": raw_response}
            parsed = json.loads(raw_response[start:end + 1])
        validated = _validate_response(parsed, evidence)
        validated["model"] = model
        return validated
    except urllib.error.URLError as exc:
        return {"ok": False, "message": f"Local Ollama unavailable: {exc}"}
    except json.JSONDecodeError as exc:
        return {"ok": False, "message": f"Invalid JSON from Ollama: {exc}"}
    except Exception as exc:
        return {"ok": False, "message": f"Unexpected Ollama error: {type(exc).__name__}: {exc}"}


def compare_priority_rankings(
    deterministic_actions: List[Dict[str, object]],
    ai_result: Dict[str, object],
) -> Dict[str, object]:
    deterministic_labels = [
        item.get("label")
        for item in deterministic_actions
        if isinstance(item, dict) and item.get("label")
    ]
    ai_labels = [
        item.get("label")
        for item in ai_result.get("recommendations", [])
        if isinstance(item, dict) and item.get("label")
    ]
    overlap = [label for label in ai_labels if label in deterministic_labels]
    union = set(deterministic_labels) | set(ai_labels)
    jaccard = round(len(set(overlap)) / len(union), 3) if union else 1.0
    return {
        "deterministic_labels": deterministic_labels,
        "ai_labels": ai_labels,
        "overlap_labels": overlap,
        "top3_overlap_count": len(set(overlap)),
        "jaccard_similarity": jaccard,
    }
