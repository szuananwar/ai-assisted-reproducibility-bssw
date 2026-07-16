from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Tuple
import json, os, urllib.error, urllib.request

@dataclass(frozen=True)
class Rule:
    key: str
    label: str
    points: int
    paths: Tuple[str, ...]
    description: str

BASE_RULES = (
    Rule('documentation','Documentation',15,('README.md','README.rst'),'Add a README with installation and execution instructions.'),
    Rule('dependencies','Dependency specification',15,('requirements.txt','pyproject.toml'),'Add machine-readable dependencies.'),
    Rule('environment','Reproducible environment',10,('environment.yml','environment.yaml','conda-lock.yml','poetry.lock','uv.lock'),'Add a reproducible environment or lock file.'),
    Rule('hpc_stack','HPC software stack',10,('spack.yaml','spack.lock','buildtest.yml','buildtest.yaml'),'Add Spack or BuildTest configuration.'),
    Rule('testing','Automated tests',15,('tests','test','pytest.ini','tox.ini'),'Add executable tests.'),
    Rule('container','Container recipe',15,('Dockerfile','Containerfile','apptainer.def','Singularity'),'Add a Docker/Podman or Apptainer/Singularity recipe.'),
    Rule('tracking','Experiment/provenance tracking',10,('MLproject','mlruns','dvc.yaml','params.yaml','provenance.json'),'Add experiment or provenance tracking.'),
    Rule('license','License',10,('LICENSE','LICENSE.md','COPYING'),'Add a license.'),
)
DOMAIN_RULES = {
    'general': (),
    'biomedical': (
        Rule('data_card','Data documentation',5,('DATA_CARD.md','datasheet.md','data/README.md'),'Document dataset provenance, privacy, and intended use.'),
        Rule('seed_control','Random seed control',5,('config.yaml','config.yml','params.yaml'),'Record random seeds and experiment parameters.'),
    ),
    'climate': (
        Rule('metadata','Units and metadata',5,('metadata.yml','metadata.yaml','cf_metadata.json'),'Document units, coordinates, and metadata.'),
        Rule('provenance','Input data provenance',5,('DATA.md','data/README.md','provenance.json'),'Document input origin and transformations.'),
    ),
    'hpc-simulation': (
        Rule('scheduler','Scheduler configuration',5,('slurm.sh','job.slurm','pbs.sh','lsf.sh'),'Document the batch scheduler configuration.'),
        Rule('runtime','Compiler/runtime metadata',5,('spack.yaml','module_list.txt','compiler_info.txt'),'Record compiler, MPI, accelerator, and module metadata.'),
    ),
}

def discover_project_root(start: Path | None = None) -> Path:
    env = os.getenv('REPRO_PROJECT_PATH')
    if env and Path(env).expanduser().exists():
        return Path(env).expanduser().resolve()
    start = (start or Path.cwd()).resolve()
    for candidate in (start, *start.parents):
        if any((candidate / marker).exists() for marker in ('.git','README.md','pyproject.toml')):
            return candidate
    return start

def _nonempty(root: Path, candidates: Tuple[str,...]) -> List[str]:
    found=[]
    for rel in candidates:
        p=root/rel
        if p.is_file() and p.stat().st_size>0: found.append(rel)
        elif p.is_dir() and any(p.iterdir()): found.append(rel)
    return found

def assess_repository(project_path: str | Path, domain: str='general') -> Dict[str, object]:
    root=Path(project_path).expanduser().resolve()
    if not root.is_dir(): raise ValueError(f'Invalid repository path: {root}')
    findings=[]
    for rule in BASE_RULES + DOMAIN_RULES.get(domain,()):
        found=_nonempty(root,rule.paths)
        findings.append({'key':rule.key,'label':rule.label,'earned':rule.points if found else 0,'possible':rule.points,'found_paths':found,'status':'PASS' if found else 'MISSING','recommendation':f"Keep {', '.join(found)} maintained." if found else rule.description})
    score=sum(x['earned'] for x in findings); possible=sum(x['possible'] for x in findings)
    percent=round(score/possible*100,1) if possible else 0.0
    band='Strong reproducibility' if percent>=85 else 'Good; improvements recommended' if percent>=70 else 'Moderate reproducibility risk' if percent>=50 else 'High reproducibility risk'
    return {'project_path':str(root),'domain':domain,'score':score,'possible':possible,'percent':percent,'band':band,'findings':findings}

def repository_inventory(root: str | Path, max_files: int=250) -> List[str]:
    root=Path(root); ignored={'.git','.venv','venv','__pycache__','node_modules'}; files=[]
    for p in root.rglob('*'):
        if any(part in ignored for part in p.parts): continue
        if p.is_file():
            files.append(str(p.relative_to(root)))
            if len(files)>=max_files: break
    return sorted(files)

def build_evidence_package(project_path: str | Path, assessment: Dict[str,object], max_chars: int=2000) -> Dict[str,object]:
    root=Path(project_path); inventory=repository_inventory(root); snippets={}
    names={'README.md','README.rst','requirements.txt','pyproject.toml','environment.yml','spack.yaml','Dockerfile','apptainer.def','MLproject','dvc.yaml','params.yaml','LICENSE'}
    for rel in inventory:
        p=root/rel
        if p.name in names and p.stat().st_size<=100000:
            snippets[rel]=p.read_text(encoding='utf-8',errors='replace')[:max_chars]
        if len(snippets)>=12: break
    return {'repository_path':str(root),'deterministic_score':{k:assessment[k] for k in ('score','possible','percent','band')},'findings':assessment['findings'],'file_inventory':inventory,'selected_file_snippets':snippets}

def local_llm_recommendations(evidence: Dict[str,object], model: str|None=None, url: str|None=None, timeout: int=60) -> Dict[str,object]:
    model=model or os.getenv('OLLAMA_MODEL','gemma3:1b'); url=url or os.getenv('OLLAMA_URL','http://localhost:11434/api/generate')
    prompt='Use only the evidence below. The deterministic score is authoritative. Explain the three highest-priority gaps, remediation steps, one HPC-specific recommendation, and one limitation.\n\n'+json.dumps(evidence,indent=2)[:24000]
    req=urllib.request.Request(url,data=json.dumps({'model':model,'prompt':prompt,'stream':False}).encode(),headers={'Content-Type':'application/json'},method='POST')
    try:
        with urllib.request.urlopen(req,timeout=timeout) as r: payload=json.loads(r.read().decode())
        if not payload.get('response'): return {'ok':False,'message':"Ollama response did not contain 'response'.",'raw':payload}
        return {'ok':True,'model':model,'response':payload['response']}
    except urllib.error.URLError as exc: return {'ok':False,'message':f'Local Ollama unavailable; static assessment completed: {exc}'}
    except (json.JSONDecodeError,KeyError) as exc: return {'ok':False,'message':f'Invalid Ollama response: {exc}'}

def print_assessment(result: Dict[str,object]) -> None:
    print(f"Repository: {result['project_path']}\nScore: {result['score']}/{result['possible']} ({result['percent']}%)\nInterpretation: {result['band']}\n")
    for item in result['findings']:
        paths=', '.join(item['found_paths']) or 'none'
        print(f"[{item['status']:7}] {item['label']:30} {item['earned']:>2}/{item['possible']:<2} Found: {paths}")
