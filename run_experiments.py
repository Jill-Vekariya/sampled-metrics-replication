"""Run the frozen partial replication and write machine-readable evidence."""
import argparse
import csv
import datetime as dt
import hashlib
import json
import platform
import subprocess
import time
from pathlib import Path

import numpy as np
import scipy
from src.metrics import METRICS, macro_moments, metric, monte_carlo, moments

ROOT = Path(__file__).resolve().parent
PUBLISHED_EXACT = {
    'A': [.990,.010,.150,.000], 'B': [.555,.010,.122,.000],
    'C': [.843,.101,.208,.200]}
PUBLISHED_SAMPLED = {
    'A': [[.990,.004],[.630,.129],[.724,.097],[1,.000]],
    'B': [[.555,.014],[.336,.073],[.444,.054],[.400,.000]],
    'C': [[.843,.014],[.325,.050],[.460,.039],[.567,.092]]}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(path, rows):
    with path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='results/final')
    parser.add_argument('--no-figures', action='store_true')
    args = parser.parse_args()
    out = ROOT / args.output
    if (out/'summary.json').exists():
        raise FileExistsError('Use a new output directory to preserve previous evidence')
    out.mkdir(parents=True, exist_ok=True)
    start_time = dt.datetime.now(dt.timezone.utc).isoformat()
    start = time.perf_counter()
    cfg = json.loads((ROOT/'configs/protocol.json').read_text())
    n, m = cfg['n'], cfg['primary_m']
    try:
        commit = subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True,
                                          stderr=subprocess.DEVNULL).strip()
    except (subprocess.SubprocessError, FileNotFoundError):
        commit = None
    source_hashes = {p.relative_to(ROOT).as_posix():sha(p) for p in
                     [ROOT/'run_experiments.py',ROOT/'src/metrics.py',ROOT/'configs/protocol.json']}
    summary = {'protocol_sha256':source_hashes['configs/protocol.json'],
               'start_utc':start_time,'git_commit':commit,'source_hashes':source_hashes,
               'environment':{'python':platform.python_version(),'os':platform.platform(),
                              'cpu':platform.processor(),'numpy':np.__version__,'scipy':scipy.__version__},
               'primary':[],'checks':{},'status':'running'}
    (out/'running.json').write_text(json.dumps(summary, indent=2))
    registry, curves = [], []
    for model_index, (model,ranks) in enumerate(cfg['ranks'].items()):
        seed = cfg['seed'] + model_index
        primary = monte_carlo(ranks,n,m,cfg['primary_repetitions'],seed)
        calibration = monte_carlo(ranks,n,m,cfg['calibration_repetitions'],seed+10000)
        np.savez_compressed(out/f'{model}_primary_draws.npz', **primary)
        np.savez_compressed(out/f'{model}_calibration_draws.npz', **calibration)
        for index,name in enumerate(METRICS):
            exact = float(metric(ranks,n,name).mean())
            expected, sd = macro_moments(ranks,n,m,name)
            observed = float(primary[name].mean())
            observed_sd = float(primary[name].std(ddof=1))
            calmean = float(calibration[name].mean())
            calse = sd / np.sqrt(cfg['calibration_repetitions'])
            z = (calmean-expected)/calse if calse > 1e-14 else 0.
            published,pubsd = PUBLISHED_SAMPLED[model][index]
            combined = np.sqrt((sd**2+pubsd**2)/cfg['primary_repetitions'])
            diag = abs(expected-published) > .0005 + cfg['claim_checks']['published_mean_diagnostic_z']*combined
            row = dict(model=model,metric=name,exact=exact,published_exact=PUBLISHED_EXACT[model][index],
                       expected=expected,analytic_sd=sd,monte_carlo_mean=observed,
                       monte_carlo_sd=observed_sd,monte_carlo_se=sd/np.sqrt(cfg['primary_repetitions']),
                       calibration_mean=calmean,calibration_z=float(z),published_mean=published,
                       published_sd=pubsd,published_mean_diagnostic_flag=bool(diag),
                       exact_rounding_match=bool(abs(exact-PUBLISHED_EXACT[model][index]) <=
                                                 cfg['claim_checks']['table1_absolute_tolerance']))
            summary['primary'].append(row)
        registry.append(dict(experiment_id=f'primary-{model}',model=model,data='published_rank_fixture',
                             method='binomial_monte_carlo',m=m,repetitions=cfg['primary_repetitions'],seed=seed,
                             status='completed',output=str(out.relative_to(ROOT)/f'{model}_primary_draws.npz'),
                             protocol_sha256=summary['protocol_sha256'],git_commit=commit))
        registry.append(dict(experiment_id=f'calibration-{model}',model=model,data='published_rank_fixture',
                             method='binomial_monte_carlo',m=m,repetitions=cfg['calibration_repetitions'],seed=seed+10000,
                             status='completed',output=str(out.relative_to(ROOT)/f'{model}_calibration_draws.npz'),
                             protocol_sha256=summary['protocol_sha256'],git_commit=commit))
        for mode in ['with_replacement','without_replacement']:
            for size in cfg['sample_sizes']:
                for name in METRICS:
                    for correction in [False, True]:
                        value, sd = macro_moments(ranks,n,size,name,mode,correction)
                        curves.append(dict(model=model,metric=name,mode=mode,m=size,
                                           correction=correction,mean=value,sd=sd))
    p = {(r['model'],r['metric']):r for r in summary['primary']}
    checks = summary['checks']
    checks['table1_all_rounded_values_match'] = all(r['exact_rounding_match'] for r in p.values())
    checks['sampled_AP_A_greater_C'] = p['A','AP']['expected'] > p['C','AP']['expected']
    checks['exact_AP_C_greater_A'] = p['C','AP']['exact'] > p['A','AP']['exact']
    checks['sampled_NDCG_A_greater_C'] = p['A','NDCG']['expected'] > p['C','NDCG']['expected']
    checks['exact_NDCG_C_greater_A'] = p['C','NDCG']['exact'] > p['A','NDCG']['exact']
    checks['calibration_within_five_MCSE'] = all(abs(r['calibration_z']) <= 5 for r in p.values())
    auc_error = max(abs(r['mean'] - p[r['model'],'AUC']['exact']) for r in curves
                    if r['metric']=='AUC' and not r['correction'])
    checks['auc_max_absolute_error'] = auc_error
    checks['auc_invariant'] = auc_error <= cfg['claim_checks']['auc_invariance_atol']
    full_error = max(abs(r['mean']-p[r['model'],r['metric']]['exact']) for r in curves
                     if r['mode']=='without_replacement' and r['m']==n-1 and not r['correction'])
    checks['complete_without_replacement_max_error'] = full_error
    checks['complete_without_replacement_equals_exact'] = full_error <= 1e-10
    summary['AP_orders'] = {str(size): sorted(cfg['ranks'],key=lambda model:next(
        r['mean'] for r in curves if r['model']==model and r['metric']=='AP' and
        r['m']==size and r['mode']=='with_replacement' and not r['correction']), reverse=True)
                           for size in [20,200,500,9999]}
    summary['elapsed_seconds'] = time.perf_counter()-start
    summary['end_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
    summary['status'] = 'completed'
    write_csv(out/'primary.csv',summary['primary'])
    write_csv(out/'curves.csv',curves)
    write_csv(out/'experiment_registry.csv',registry)
    write_csv(out/'original_comparison.csv', [dict(model=r['model'],metric=r['metric'],
        exact_delta=r['exact']-r['published_exact'],mean_delta=r['expected']-r['published_mean'],
        sd_delta=r['analytic_sd']-r['published_sd'],diagnostic_flag=r['published_mean_diagnostic_flag'])
        for r in summary['primary']])
    (out/'summary.json').write_text(json.dumps(summary,indent=2,allow_nan=False)+'\n')
    print(json.dumps(summary,indent=2,allow_nan=False),flush=True)
    if not all(v for v in checks.values() if isinstance(v,bool)):
        raise RuntimeError('Predeclared scientific/correctness check failed; preserve results and investigate')
    if not args.no_figures:
        from plot_results import make_figures
        make_figures(out,ROOT/'figures'/out.name)


if __name__ == '__main__': main()
