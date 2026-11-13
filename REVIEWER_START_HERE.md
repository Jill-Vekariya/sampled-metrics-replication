# Reviewer start here — scoped replication

**Submitted article:** [Re] Ranking reversals under sampled recommendation metrics
**ReScience C issue:** https://github.com/ReScience/submissions/issues/158
**Original study:** Krichene and Rendle, IJCAI 2021, DOI https://doi.org/10.24963/ijcai.2021/651
**Type and limits:** Independent **partial replication** of the designed five-instance numerical counterexample. No trained recommender, real-user benchmark, or claim about prevalence is included.

## Fast reproducibility path

Use a fresh clone and Python 3.11–3.13. All code dependencies are freely available.

On Linux/macOS:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt -r requirements-manuscript.txt
.venv/bin/python -m pytest -q
.venv/bin/python verify_release.py --public --manifest
.venv/bin/python run_experiments.py --no-figures --output results/reviewer-run
.venv/bin/python compare_results.py results/reviewer-run
```

On Windows PowerShell (Python 3.12 or 3.13):

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -r requirements-manuscript.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe verify_release.py --public --manifest
.\.venv\Scripts\python.exe run_experiments.py --no-figures --output results/reviewer-run
.\.venv\Scripts\python.exe compare_results.py results/reviewer-run
```

The output directory must not contain an existing `summary.json`; choose another name for a second rerun. The comparison command checks 12 primary result rows at absolute tolerance `1e-12`. The release verifier separately checks archived scientific source, maintained source, source snapshots, input protocol, raw array checksums, and the package manifest. An experimental rerun is also required; the manifest alone cannot substitute for execution. The 14 November 2026 release passed 140 tests locally and all four GitHub Actions jobs (Windows/Linux, Python 3.11/3.12) completed successfully; new submissions should be checked against their corresponding commit. Test counts can change with maintenance.

## Mapping the original publication to the replication

| Original IJCAI result | Reproduced paper evidence | Independently checkable file(s) | Agreement and presentation differences |
|---|---|---|---|
| Table 1 — exact full-catalogue AUC, AP, NDCG, Recall@10 for A/B/C | Manuscript Table 1 | `results/windows-final/primary.csv`; `run_experiments.py` | All twelve entries agree with source at reported three-decimal precision. Rounding in the source hides the small exact AP difference between A and B. |
| Table 2 — sampled AUC, AP, NDCG, Recall@10 (99 negatives) | Manuscript Table 2 and Figure 1 | `results/windows-final/primary.csv`, `results/windows-final/original_comparison.csv`, `results/windows-final/*_primary_draws.npz` | Analytic expectations and one-evaluation SD versus published simulation estimates. Differences from source random means are documented rather than hidden. |
| Figure 2 — effect of negative sample count on metrics | Manuscript Figure 2 | `results/windows-final/curves.csv`, `figures/final/sample_size_sensitivity.png`, `plot_results.py` | Reproduces sampled-metric changes and AP ordering reversals using 23 declared sample sizes; discrete interpolation/plot aesthetics may differ. |
| Figure 3 — metric shape as a function of full-catalogue rank | Manuscript Appendix Figure 3 | `results/windows-final/metric_shape.csv`, `figures/final/metric_shape.png`, `tests/test_figure3.py` | Uses source **Recall@5** specifically for Figure 3 (other tables/Figure 2 use Recall@10); computed on the declared rank grid, not claimed pixel-for-pixel identical. |

### Principal numerical verification

Five relevant items per constructed list, 10,000 catalogue items, 99 sampled negatives with replacement:

| Model | Full-catalogue AP | Analytic expected sampled AP |
|---|---:|---:|
| A | 0.010000 | 0.636592 |
| B | 0.010090 | 0.340739 |
| C | 0.101379 | 0.326169 |

C outranks A on full-catalogue AP, but A outranks C after sampling. The same A-versus-C reversal occurs for NDCG. Expected AUC remains invariant. No training data or model weights are needed to check these mathematical statements.

## Exactly what is and is not replicated

The IJCAI **extended abstract** includes a self-contained numerical counterexample about the effect of sampled evaluation metrics. The implementation independently computes the corresponding finite probability distributions, deterministic moments, and random simulation checks. Exhaustive tests on small catalogues provide separate mathematical correctness oracles. These are distinct routes to the same published behavior; the output is not solely a copied numerical table.

The full empirical trained-model comparison in the longer KDD 2020 article is **not** reproduced. No inference is made about deployment prevalence, real-world recommendation performance, or trained-model robustness. This limit is an explicit part of the submission, not a missing dataset mislabeled as a successful benchmark.

## Evidence preservation and provenance

- `configs/protocol.json`: original frozen protocol, ranks, seeds and sample-size grid.
- `audit/source_snapshot/`: code bytes preserved for the initial executed study; current maintained source is verified separately.
- `results/windows-final/`: archived primary results and raw draws; `results/release-validation/`: later validated maintained-source rerun.
- `RELEASE_MANIFEST.json`, `verify_release.py`: integrity checks. `publication/ORIGINAL_SUBMISSION_*.json` and `audit/original_release_manifest.json`: historical baseline.
- `AMENDMENTS.md`: post-submission Figure 3 fidelity correction.
- `manuscript/article.pdf`: submitted article; `build_manuscript.py` builds the PDF and readable Markdown; `plot_results.py` regenerates figures.
- `.github/workflows/tests.yml`: Linux/Windows automated testing and release integrity checks.

To rebuild figures and PDF after examining the code, run `python plot_results.py results/windows-final` then `python build_manuscript.py`. Those commands rewrite generated artifacts, so use a disposable clone or preserve a clean copy if verifying the committed package hashes.

## Review questions worth evaluating independently

1. Does the binomial model correctly treat repeated negative draws, and does the hypergeometric extension handle sampling without replacement?
2. Do the independent finite sums, direct simulations and small-catalogue oracles agree?
3. Do sample-size curves reproduce the **direction and reversal** of the original fixed-rank counterexample?
4. Are source Table 2 simulation differences adequately distinguished from exact analytical expectations?
5. Is this explicitly limited subset sufficiently substantial for the journal's partial-replication criteria?

ReScience C criteria: https://rescience.github.io/write/ and https://rescience.github.io/edit/ . Journal acceptance and reviewer assignment are not established by the automated checks.

## Authors, responsibility and tools

The human author accepts responsibility for the analysis, interpretation and manuscript. The manuscript contains the tool-use disclosure pertinent to the submitted work. The scientific results are independently verifiable from code and preserved numerical evidence.
