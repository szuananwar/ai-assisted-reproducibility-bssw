from pathlib import Path
from checker.reproducibility_checker import assess_repository, build_evidence_package

def write(path: Path, content='x'):
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text(content)

def test_empty_repository_scores_zero(tmp_path):
    result=assess_repository(tmp_path)
    assert result['score']==0 and result['possible']==100

def test_complete_repository_scores_100(tmp_path):
    for rel in ['README.md','requirements.txt','environment.yml','spack.yaml','tests/test_smoke.py','apptainer.def','MLproject','LICENSE']:
        write(tmp_path/rel)
    result=assess_repository(tmp_path)
    assert result['score']==100
    evidence=build_evidence_package(tmp_path,result)
    assert 'README.md' in evidence['file_inventory']

def test_empty_files_do_not_receive_credit(tmp_path):
    (tmp_path/'README.md').touch()
    assert assess_repository(tmp_path)['score']==0
