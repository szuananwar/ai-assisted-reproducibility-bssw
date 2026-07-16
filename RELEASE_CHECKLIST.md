# Release Checklist

## Before Tagging

- [ ] All pull requests for the release are merged.
- [ ] GitHub Actions is green on `main`.
- [ ] `git status` is clean.
- [ ] `pyproject.toml` version is correct.
- [ ] `CITATION.cff` version and release date are correct.
- [ ] `CHANGELOG.md` contains the release section.
- [ ] Core tests pass.
- [ ] Web tests pass.
- [ ] Package builds successfully.
- [ ] `twine check dist/*` passes.
- [ ] CLI help and one local assessment work.
- [ ] Dashboard starts successfully.

## Release Commands

```bash
git checkout main
git pull
git status

python3 -m pytest tests -v
PYTHONPATH=webapp/backend:. python3 -m pytest webapp/backend/tests -v

python3 -m build
python3 -m twine check dist/*

git tag -a v0.1.0 -m "ReproPilot v0.1.0"
git push origin v0.1.0
```

## Create the GitHub Release

```bash
gh release create v0.1.0   --title "ReproPilot v0.1.0"   --notes-file RELEASE_NOTES_v0.1.0.md   dist/repropilot-0.1.0-py3-none-any.whl   dist/repropilot-0.1.0.tar.gz
```

Do not create the tag until CI is green and the release-readiness pull request
has been merged.
