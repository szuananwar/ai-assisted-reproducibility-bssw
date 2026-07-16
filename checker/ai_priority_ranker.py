from __future__ import annotations

from typing import Dict, List
import json
import os
import urllib.error
import urllib.request


def ai_priority_labels(
    quality: Dict[str, object],
    model: str | None = None,
    url: str | None = None,
    timeout: int = 90,
) -> Dict[str, object]:
    """Return up to three exact quality-finding labels using Ollama JSON mode."""
    model = model or os.getenv("OLLAMA_MODEL", "gemma3:1b")
    url = url or os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")

    findings = [
        {
            "label": item["label"],
            "earned": item["earned"],
            "possible": item["possible"],
            "evidence": item.get("evidence", []),
            "recommendation": item.get("recommendation", ""),
        }
        for item in quality.get("quality_findings", [])
        if item.get("applicable", True)
    ]
    allowed_labels = [item["label"] for item in findings]

    prompt = f"""
Select the three highest-priority reproducibility-quality issues.

Rules:
- Use ONLY exact labels from ALLOWED_LABELS.
- Return valid JSON only.
- Return exactly one object with key "priorities".
- "priorities" must be a list of up to three unique exact labels.
- Do not include explanations, evidence, markdown, or extra keys.
- Prioritize lower-scoring findings.

ALLOWED_LABELS:
{json.dumps(allowed_labels)}

FINDINGS:
{json.dumps(findings)}
""".strip()

    request = urllib.request.Request(
        url,
        data=json.dumps({
            "model": model,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {"temperature": 0},
        }).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            outer = json.loads(response.read().decode("utf-8"))
        raw = outer.get("response", "")
        parsed = json.loads(raw)
        priorities = parsed.get("priorities", [])

        if not isinstance(priorities, list):
            return {"ok": False, "message": "priorities is not a list", "raw": parsed}

        cleaned: List[str] = []
        for label in priorities:
            if label in allowed_labels and label not in cleaned:
                cleaned.append(label)
            if len(cleaned) == 3:
                break

        if not cleaned:
            return {
                "ok": False,
                "message": "No valid exact labels returned",
                "raw": parsed,
                "allowed_labels": allowed_labels,
            }

        return {
            "ok": True,
            "model": model,
            "priorities": cleaned,
            "raw": parsed,
        }

    except urllib.error.URLError as exc:
        return {"ok": False, "message": f"Local Ollama unavailable: {exc}"}
    except json.JSONDecodeError as exc:
        return {"ok": False, "message": f"Invalid JSON from Ollama: {exc}"}
    except Exception as exc:
        return {"ok": False, "message": f"Unexpected Ollama error: {type(exc).__name__}: {exc}"}
