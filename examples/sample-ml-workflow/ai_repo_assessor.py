import subprocess

repo_url = input("Enter GitHub repository URL: ")

prompt = f"""
You are evaluating a scientific software repository for reproducibility and sustainability.

Repository URL:
{repo_url}

Evaluate the repository using this rubric:

1. README clarity
2. Installation instructions
3. License availability
4. Requirements or environment file
5. Documentation quality
6. Testing or CI/CD
7. Reproducibility of results
8. Sustainability and maintainability

Give:
- A score from 1 to 10
- Strengths
- Weaknesses
- Recommendations for improvement
"""

result = subprocess.run(
    ["ollama", "run", "gemma3:1b"],
    input=prompt,
    text=True,
    capture_output=True
)

print("\n===== Local AI Reproducibility Assessment =====\n")
print(result.stdout)

if result.stderr:
    print("\nErrors:\n")
    print(result.stderr)
