"""Regenerate all figures from saved results and the frozen rank fixture."""
import csv
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src.metrics import METRICS, metric, moments, distribution

ROOT = Path(__file__).resolve().parent
COLORS = {'A':'#2864b4','B':'#c87920','C':'#16806a'}

FIGURE3_METRICS = ('AP', 'NDCG', 'Recall@5', 'AUC')


def figure3_metric_values(ranks, n, m, name):
    """Figure 3 uses Recall@5; the primary Tables 1-2 use Recall@10.

    Reuse the frozen sampled-rank distribution without changing the
    originally evaluated metrics, protocol, or source hashes.
    """
    if name == 'Recall@5':
        k, probabilities = distribution(ranks, n, m)
        expected = probabilities @ (k < 5).astype(float)
        exact = (np.asarray(ranks) <= 5).astype(float)
        return expected, exact
    expected, _ = moments(ranks, n, m, name)
    return expected, metric(ranks, n, name)


def make_figures(out, destination):
    out,destination = Path(out),Path(destination)
    destination.mkdir(parents=True,exist_ok=True)
    summary = json.loads((out/'summary.json').read_text())
    cfg = json.loads((ROOT/'configs/protocol.json').read_text())
    with (out/'curves.csv').open() as f: rows = list(csv.DictReader(f))
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,
                         'axes.spines.right':False,'savefig.bbox':'tight'})
    def save(fig, name):
        fig.savefig(destination/(name+'.pdf'))
        fig.savefig(destination/(name+'.png'),dpi=170)
        plt.close(fig)
    fig,axes = plt.subplots(2,2,figsize=(9.2,6.4))
    for ax,name in zip(axes.flat,METRICS):
        for model in cfg['ranks']:
            r = [x for x in rows if x['model']==model and x['metric']==name and
                 x['mode']=='with_replacement' and x['correction']=='False']
            ax.plot([int(x['m']) for x in r],[float(x['mean']) for x in r],
                    color=COLORS[model],label=model,lw=1.9)
            exact = next(x['exact'] for x in summary['primary'] if x['model']==model and x['metric']==name)
            ax.axhline(exact,color=COLORS[model],ls=':',lw=1,alpha=.65)
        ax.set(xscale='log',title=name,xlabel='Sampled negatives, m',ylabel='Expected metric')
        ax.grid(alpha=.16); ax.legend(frameon=False,ncol=3)
    fig.tight_layout();save(fig,'sample_size_sensitivity')
    fig,axes=plt.subplots(1,3,figsize=(9.2,3.2))
    for ax,name in zip(axes,['AP','NDCG','Recall@10']):
        x=np.arange(3); width=.25
        for j,kind in enumerate(['exact','expected','monte_carlo_mean']):
            vals=[next(r[kind] for r in summary['primary'] if r['model']==model and r['metric']==name)
                  for model in cfg['ranks']]
            ax.bar(x+(j-1)*width,vals,width,label=['Full catalogue','Sampled expectation','1000-run mean'][j],
                   color=['#56657a','#337ab7','#86b9a8'][j])
        ax.set(xticks=x,xticklabels=list(cfg['ranks']),title=name,ylabel='Metric value')
    axes[0].legend(frameon=False,fontsize=8)
    fig.tight_layout();save(fig,'rank_reversal')
    fig,axes=plt.subplots(2,2,figsize=(9.2,6.4))
    ranks=np.array(cfg['curve_rank_grid'])
    curve_rows=[]
    for ax,name in zip(axes.flat,FIGURE3_METRICS):
        for size in [1,10,100,1000]:
            values,exact=figure3_metric_values(ranks,cfg['n'],size,name)
            ax.plot(ranks,values,label=f'm={size}')
            curve_rows.extend(dict(rank=int(r),m=size,metric=name,expected=float(v))
                              for r,v in zip(ranks,values))
        ax.plot(ranks,exact,'k--',label='Exact',lw=1.4)
        ax.set(xlim=(1,1000),title=name,xlabel='Full-catalogue rank',ylabel='Expected metric')
        ax.grid(alpha=.16)
    axes[0,0].legend(frameon=False,fontsize=8,ncol=2)
    fig.tight_layout();save(fig,'metric_shape')
    with (out/'metric_shape.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(curve_rows[0]),lineterminator='\n');w.writeheader();w.writerows(curve_rows)
    print('Figures regenerated in',destination,flush=True)


if __name__=='__main__':
    import sys
    make_figures(ROOT/(sys.argv[1] if len(sys.argv)>1 else 'results/final'),ROOT/'figures/final')
