"""Read-only checks of the complete research release candidate.

Use --public only after the author has actually confirmed the declarations.
No network calls, publication, account changes, or scientific reruns occur.
"""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import math
import zipfile

from compare_results import compare_summaries

ROOT=Path(__file__).resolve().parent
SOURCE_FILES = ('run_experiments.py', 'src/metrics.py', 'configs/protocol.json')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validation_curves_match(root):
    """Compare means and variances; SD near zero amplifies roundoff on taking sqrt."""
    with (root/'results/windows-final/curves.csv').open(newline='') as stream:
        original = list(csv.DictReader(stream))
    with (root/'results/release-validation/curves.csv').open(newline='') as stream:
        current = list(csv.DictReader(stream))
    if not original or len(original) != len(current):
        return False
    for archived, validated in zip(original, current, strict=True):
        for field in ('model', 'metric', 'mode', 'm', 'correction'):
            if archived[field] != validated[field]:
                return False
        for field in ('mean', 'sd'):
            left, right = float(archived[field]), float(validated[field])
            if not math.isfinite(left) or not math.isfinite(right):
                return False
            if field == 'sd':
                if min(left, right) < 0:
                    return False
                left, right = left**2, right**2
            if not math.isclose(left, right, rel_tol=0, abs_tol=1e-12):
                return False
    return True


def source_provenance_checks(root, archived):
    """Check archived source bytes separately from a later maintained-source rerun."""
    checks = {
        'archived_scientific_sources_preserved': False,
        'scientific_source_hashes_match': False,
        'current_validation_reproduces_archive': False,
        'current_validation_curves_match_archive': False,
    }
    try:
        original_hashes = archived['source_hashes']
        if set(original_hashes) != set(SOURCE_FILES):
            return checks
        checks['archived_scientific_sources_preserved'] = all(
            digest(root/'audit/source_snapshot'/name) == original_hashes[name]
            for name in SOURCE_FILES
        )
        validation = json.loads(
            (root/'results/release-validation/summary.json').read_text(encoding='utf-8')
        )
        current_hashes = validation['source_hashes']
        checks['scientific_source_hashes_match'] = (
            set(current_hashes) == set(SOURCE_FILES)
            and all(digest(root/name) == current_hashes[name] for name in SOURCE_FILES)
        )
        required_claims = {key for key, value in archived['checks'].items()
                           if isinstance(value, bool)}
        checks['current_validation_reproduces_archive'] = (
            validation['status'] == 'completed'
            and bool(required_claims)
            and all(validation['checks'].get(key) is True for key in required_claims)
            and not compare_summaries(archived, validation)
        )
        checks['current_validation_curves_match_archive'] = validation_curves_match(root)
    except (OSError, KeyError, ValueError, TypeError, OverflowError, csv.Error):
        # Missing, malformed or incompatible evidence must fail the release check.
        pass
    return checks


def main():
    import yaml

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
    checks.update(source_provenance_checks(ROOT, summary))
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
