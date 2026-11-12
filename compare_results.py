"""Compare a rerun to the archived Windows evidence without changing it."""
import argparse
import json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parent

def main():
    p=argparse.ArgumentParser()
    p.add_argument('rerun',help='Result directory relative to project root')
    a=p.parse_args()
    original=json.loads((ROOT/'results/windows-final/summary.json').read_text())
    rerun=json.loads((ROOT/a.rerun/'summary.json').read_text())
    assert original['protocol_sha256']==rerun['protocol_sha256'],'Protocol changed'
    names=['exact','expected','analytic_sd','monte_carlo_mean','monte_carlo_sd','calibration_mean']
    errors=[]
    for x,y in zip(original['primary'],rerun['primary'],strict=True):
        assert (x['model'],x['metric'])==(y['model'],y['metric'])
        for name in names:
            if not np.isclose(x[name],y[name],rtol=0,atol=1e-12):
                errors.append({'model':x['model'],'metric':x['metric'],'field':name,
                               'reference':x[name],'rerun':y[name]})
    print(json.dumps({'match_within_1e-12':not errors,'differences':errors},indent=2))
    if errors:raise SystemExit(1)

if __name__=='__main__':main()
