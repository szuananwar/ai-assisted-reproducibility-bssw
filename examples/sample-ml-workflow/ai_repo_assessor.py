import os
import subprocess
import sys
import requests

MODEL = "gemma3:4b"
OLLAMA_URL = "http://localhost:11434/api/generate"


def check_ollama():
    """Check if Ollama is installed."""
    try:
        subprocess.run(
            ["ollama", "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    except Exception:
        print("\nERROR: Ollama is not installed.")
        print("Install from: https://ollama.com/download\n")
        sys.exit(1)


def ensure_model():
    """Check if Gemma model exists, otherwise pull it."""
    result = subprocess.run(
        ["ollama", "list"],
        capture_output=True,
        text=True
    )

    if MODEL not in result.stdout:
        print(f"\nModel {MODEL} not found.")
        print(f"Downloading {MODEL} ...\n")

        subprocess.run(["ollama", "pull", MODEL], check=True)

        print("\nModel installed successfully.\n")


def evaluate_repository(repo_url):

    prompt = f"""
You are an AI assistant evaluating a scientific software repository for reproducibility and sustainability.

Repository URL:
{repo_url}

Use this exact 100-point rubric:

| Category | Item | Points |
|---|---|---|
| Documentation | README with run instructions | 15 |
| Dependencies | requirements.txt | 15 |
| Environment | environment.yml | 10 |
| HPC Environment | spack.yaml | 10 |
| Testing | tests/ folder | 15 |
| Containerization | Dockerfile or Apptainer file | 15 |
| Experiment Tracking | MLflow logs or tracking file | 10 |
| Open Science | LICENSE file | 10 |
| Total |  | 100 |

For each category:
1. State whether the item appears present.
2. Award points.
3. Explain briefly.

Then provide:
- Total score out of 100
- Score interpretation:
  - 85–100: Strong reproducibility
  - 70–84: Good, but improvements needed
  - 50–69: Moderate reproducibility risk
  - Below 50: High reproducibility risk
- Strengths
- Weaknesses
- Recommendations

Format using markdown tables and headings.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    if response.status_code != 200:
        print("\nError communicating with Ollama.\n")
        print(response.text)
        return

    result = response.json()

    print("\n===== AI-Assisted Reproducibility Assessment =====\n")
    print(result["response"])


if __name__ == "__main__":

    check_ollama()
    ensure_model()

    repo_url = input("Enter GitHub repository URL: ")

    evaluate_repository(repo_url)
