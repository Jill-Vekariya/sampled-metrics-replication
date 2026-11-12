"""Read-only checks of the complete research release candidate.

Use --public only after the author has actually confirmed the declarations.
No network calls, publication, account changes, or scientific reruns occur.
"""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import zipfile
import yaml

ROOT=Path(__file__).resolve().parent

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--manifest',action='store_true')
    parser.add_argument('--public',action='store_true')
    args=parser.parse_args()
    summary=json.loads((ROOT/'results/windows-final/summary.json').read_text())
    cfg=json.loads((ROOT/'configs/protocol.json').read_text())
    metadata=yaml.safe_load((ROOT/'manuscript/metadata.yaml').read_text())
    citation=yaml.safe_load((ROOT/'CITATION.cff').read_text())
    checks={}
    required=['manuscript/article.pdf','manuscript/article.md','manuscript/metadata.yaml',
              'src/metrics.py','tests/test_metrics.py','configs/protocol.json',
              'README.md','LICENSE','CITATION.cff','publication/issue_body.md',
              'publication/author_declarations.proposed.json','clean_reproduction_report.json']
    checks['required_files_nonempty']=all((ROOT/f).is_file() and (ROOT/f).stat().st_size for f in required)
    checks['scientific_source_hashes_match']=all(digest(ROOT/f)==h for f,h in summary['source_hashes'].items())
    checks['protocol_hash_matches']=digest(ROOT/'configs/protocol.json')==summary['protocol_sha256']
    checks['all_frozen_claim_checks_pass']=all(value for value in summary['checks'].values() if isinstance(value,bool))
    checks['correct_author_and_contact']=(metadata['authors'][0]['name']=='Jill Vekariya' and
        metadata['authors'][0]['email']=='jillvekariya.10@gmail.com' and metadata['authors'][0]['affiliations']=='1,*')
    checks['correct_venue_metadata']=(metadata['type']=='Replication' and metadata['language']=='Python' and
        metadata['domain']=='Machine Learning' and metadata['replication'][3]['doi']=='10.24963/ijcai.2021/651')
    checks['repository_url_populated']=metadata['code'][0]['url']=='https://github.com/Jill-Vekariya/sampled-metrics-replication'
    checks['citation_identity_matches']=(citation['authors'][0]['given-names']=='Jill' and
        citation['authors'][0]['family-names']=='Vekariya' and citation['authors'][0]['email']=='jillvekariya.10@gmail.com')
    report=json.loads((ROOT/'clean_reproduction_report.json').read_text())
    checks['clean_windows_reproduction_identical']=all(report[k] for k in
        ['primary_identical','checks_identical','source_hashes_identical','raw_arrays_identical'])
    members_ok=True
    for name,members in report['member_hashes'].items():
        with zipfile.ZipFile(ROOT/'results/windows-final'/name) as archive:
            members_ok &= all(hashlib.sha256(archive.read(member)).hexdigest()==h for member,h in members.items())
    checks['raw_array_member_hashes_match']=members_ok
    with (ROOT/'results/windows-final/curves.csv').open() as f: curves=list(csv.DictReader(f))
    checks['all_declared_analytical_conditions_retained']=len(curves)==len(cfg['sample_sizes'])*len(cfg['ranks'])*4*2*2
    checks['pdf_has_pdf_header']=(ROOT/'manuscript/article.pdf').read_bytes().startswith(b'%PDF-')
    issue=(ROOT/'publication/issue_body.md').read_text()
    checks['issue_body_has_required_urls']=all(x in issue for x in
        ['**Original article:**','**PDF URL:**','**Metadata URL:**','**Code URL:**',
         '/main/manuscript/article.pdf','/main/manuscript/metadata.yaml'])
    plan=json.loads((ROOT/'publication/release_plan.json').read_text())
    checks['reviewed_file_hashes_match']=all(digest(ROOT/f)==h for f,h in plan['file_hashes'].items())
    if args.manifest:
        manifest=json.loads((ROOT/'RELEASE_MANIFEST.json').read_text())
        checks['release_manifest_matches']=all((ROOT/f).is_file() and digest(ROOT/f)==entry['sha256']
            and (ROOT/f).stat().st_size==entry['bytes'] for f,entry in manifest.items())
    declarations=json.loads((ROOT/'publication/author_declarations.proposed.json').read_text())
    author_confirmed=bool(declarations['author_confirmation_received'])
    release_authorized=bool(declarations['public_release_authorized'])
    if args.public:
        checks['author_confirmed_declarations']=author_confirmed
        checks['public_release_authorized']=release_authorized
    payload={'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,
             'author_confirmation_received':author_confirmed,'public_release_authorized':release_authorized,
             'note':'Offline preflight cannot establish public URL accessibility or actual journal submission.'}
    print(json.dumps(payload,indent=2))
    if not all(checks.values()):raise SystemExit(1)

if __name__=='__main__':main()
