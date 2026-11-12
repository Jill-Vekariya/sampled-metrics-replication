from pathlib import Path
import json,re,hashlib,zipfile,argparse
p=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--output',help='Output ZIP path, relative to the project directory unless absolute')
args=parser.parse_args()
rootfiles=list(p.glob('*.md'))+[p/x for x in ['run_experiments.py','plot_results.py','compare_results.py','build_manuscript.py','verify_release.py']]+list(p.glob('*.txt'))+list(p.glob('*.log'))+[p/'LICENSE',p/'.gitignore',p/'.gitattributes',p/'experiment_registry.csv',p/'clean_reproduction_report.json',p/'CITATION.cff',p/'author_details.json']
# Transfer/export bootstraps are device helpers, not research dependencies.
rootfiles=[x for x in rootfiles if x.name not in ['install_research.py','export_device.py','export_complete.py','device_export.txt']]
files=list(rootfiles)
for directory,patterns in [('src',['*.py']),('tests',['*.py']),('configs',['*.json']),
 ('results',['*.json','*.csv','*.npz']),('figures/final',['*.png','*.pdf']),
 ('manuscript/fonts',['*.ttf','LICENSE.txt']),('publication',['*.md','*.json']),('logs',['*.log'])]:
 for pattern in patterns:files.extend((p/directory).rglob(pattern))
for name in ['article.pdf','article.md','metadata.yaml','bibliography.bib','TEMPLATE_ADAPTATION.md']:
 files.append(p/'manuscript'/name)
for name in ['atlas_assessment.md','dependency_metadata.json','manuscript_consistency.json']:
 files.append(p/'audit'/name)
files.append(p/'audit/current_venue/refresh_report.json')
files.append(p/'audit/package_release.py')
files=list(dict.fromkeys(f for f in files if f.is_file()))
patterns={
'private_key':r'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----',
'github_token':r'\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}\b',
'aws_access_key':r'\bAKIA[A-Z0-9]{16}\b',
'provider_token':r'\bsk-(?:proj-)?[A-Za-z0-9_-]{30,}\b'}
findings=[]
for f in files:
 if f.suffix in ['.py','.json','.csv','.md','.txt','.log','.yaml','.bib']:
  try:t=f.read_text(encoding='utf-8')
  except UnicodeDecodeError:
   try:t=f.read_text(encoding='utf-16')
   except UnicodeDecodeError:continue
  for kind,pattern in patterns.items():
   if re.search(pattern,t):findings.append({'file':f.relative_to(p).as_posix(),'kind':kind})
required=['project_status.md','research_questions.md','protocol.md','source_ledger.md','decisions.md',
'experiment_registry.csv','deviations.md','blockers.md','audit_results.md','reproducibility_checklist.md',
'submission_status.md','NEXT_ACTION.md','manuscript/article.pdf','README.md']
assert all((p/x).is_file() and (p/x).stat().st_size for x in required)
assert all(f.stat().st_size>0 for f in files)
assert not findings,findings
scan={'selected_files':len(files),'secret_pattern_findings':findings,'third_party_pdfs_included':False,
      'environment_directories_included':False,'git_directory_included':False,
      'author_name_verified':True,'corresponding_email_verified':True,'author_declarations_pending':True,'public_release_authorized':False,
      'caveat':'Pattern scanning is not a guarantee; the archive has not been publicly released.'}
(p/'audit/release_scan.json').write_text(json.dumps(scan,indent=2));files.append(p/'audit/release_scan.json')
manifest={f.relative_to(p).as_posix():{'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in files}
(p/'RELEASE_MANIFEST.json').write_text(json.dumps(manifest,indent=2));files.append(p/'RELEASE_MANIFEST.json')
archive=(p/args.output) if args.output else p.parent/'Sampled_Metrics_Research_Review_Package.zip'
archive.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,strict_timestamps=False) as z:
 for f in sorted(files):z.write(f,'sampled-metrics-replication/'+f.relative_to(p).as_posix())
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 print(json.dumps({'archive':str(archive),'bytes':archive.stat().st_size,'files':len(files),'scan':scan}))
