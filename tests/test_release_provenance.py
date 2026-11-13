"""Release checks must detect changed code and incompatible rerun evidence."""
import json
from pathlib import Path
import shutil

import pytest

from verify_release import SOURCE_FILES, source_provenance_checks

ROOT = Path(__file__).resolve().parents[1]
VALIDATION = 'results/release-validation/summary.json'


@pytest.fixture
def evidence(tmp_path):
    names = list(SOURCE_FILES) + [
        'audit/source_snapshot/' + name for name in SOURCE_FILES
    ] + [VALIDATION, 'results/release-validation/curves.csv',
         'results/windows-final/curves.csv']
    for name in names:
        destination = tmp_path/name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT/name, destination)
    archived = json.loads((ROOT/'results/windows-final/summary.json').read_text())
    return tmp_path, archived


def test_original_source_and_maintained_rerun_are_verified_separately(evidence):
    root, archived = evidence
    assert all(source_provenance_checks(root, archived).values())
    assert (root/'src/metrics.py').read_bytes() != (
        root/'audit/source_snapshot/src/metrics.py'
    ).read_bytes()


@pytest.mark.parametrize('name', SOURCE_FILES)
def test_changes_after_validation_are_rejected(evidence, name):
    root, archived = evidence
    with (root/name).open('ab') as stream:
        stream.write(b'\n')
    assert not source_provenance_checks(root, archived)['scientific_source_hashes_match']


@pytest.mark.parametrize('name', SOURCE_FILES)
def test_altered_historical_source_is_rejected(evidence, name):
    root, archived = evidence
    with (root/'audit/source_snapshot'/name).open('ab') as stream:
        stream.write(b'\n')
    assert not source_provenance_checks(root, archived)['archived_scientific_sources_preserved']


@pytest.mark.parametrize('change', ['result', 'protocol', 'claim', 'status', 'identity'])
def test_incompatible_validation_is_rejected(evidence, change):
    root, archived = evidence
    path = root/VALIDATION
    validation = json.loads(path.read_text())
    if change == 'result':
        validation['primary'][0]['expected'] += 0.01
    elif change == 'protocol':
        validation['protocol_sha256'] = 'different-protocol'
    elif change == 'claim':
        validation['checks']['auc_invariant'] = False
    elif change == 'status':
        validation['status'] = 'running'
    else:
        validation['primary'][0]['model'] = 'different-model'
    path.write_text(json.dumps(validation))
    assert not source_provenance_checks(root, archived)['current_validation_reproduces_archive']


def test_missing_validation_does_not_pass(evidence):
    root, archived = evidence
    (root/VALIDATION).unlink()
    assert not all(source_provenance_checks(root, archived).values())


@pytest.mark.parametrize('target', ['archived', 'validation'])
def test_empty_source_hashes_do_not_pass(evidence, target):
    root, archived = evidence
    if target == 'archived':
        archived['source_hashes'] = {}
    else:
        path = root/VALIDATION
        validation = json.loads(path.read_text())
        validation['source_hashes'] = {}
        path.write_text(json.dumps(validation))
    assert not source_provenance_checks(root, archived)['scientific_source_hashes_match']


@pytest.mark.parametrize('change', ['missing-row', 'mean', 'sd', 'nonfinite'])
def test_changed_sensitivity_results_do_not_pass(evidence, change):
    root, archived = evidence
    path = root/'results/release-validation/curves.csv'
    lines = path.read_text().splitlines()
    if change == 'missing-row':
        lines.pop()
    else:
        row = lines[1].split(',')
        if change == 'mean':
            row[5] = str(float(row[5]) + 0.01)
        elif change == 'sd':
            row[6] = str(float(row[6]) + 0.01)
        else:
            row[5] = 'nan'
        lines[1] = ','.join(row)
    path.write_text('\n'.join(lines) + '\n')
    assert not source_provenance_checks(root, archived)['current_validation_curves_match_archive']
