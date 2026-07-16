from app.services import validate_repository_url

def test_valid_url():
    canonical, name = validate_repository_url(
        "https://github.com/szuananwar/ai-assisted-reproducibility-bssw"
    )
    assert canonical.endswith(".git")
    assert name == "ai-assisted-reproducibility-bssw"

def test_invalid_host():
    try:
        validate_repository_url("https://example.com/a/b")
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError")
