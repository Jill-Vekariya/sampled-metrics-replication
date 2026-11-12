# Ranking reversals under sampled recommendation metrics

Status: **SUBMITTED - AWAITING EDITORIAL HANDLING**. [Official ReScience C submission #158](https://github.com/ReScience/submissions/issues/158). Research, public release and initial submission are complete. Acceptance and publication remain journal decisions.

This is an independent, scoped computational replication of Tables 1-2 and the expectation-curve findings in Krichene and Rendle, *On Sampled Metrics for Item Recommendation (Extended Abstract)*, IJCAI 2021, pp.4784-4788, DOI [10.24963/ijcai.2021/651](https://doi.org/10.24963/ijcai.2021/651).

The data are the original article's three constructed rank lists for five instances and a 10000-item catalogue. No recommender was trained. No real user dataset was downloaded. This does not reproduce the full KDD 2020 empirical study or Zhao et al.'s twelve-model splitting comparison.

## Actual main finding

Full-catalogue AP: A 0.010000, B 0.010090, C 0.101379.

Expected AP with 99 uniformly sampled negatives and replacement: A 0.636592, B 0.340739, C 0.326169. Thus A versus C reverses in expectation. Expected AUC remains unchanged. All twelve published Table 1 entries match to their printed precision.

## Reproduce the numerical study

Python 3.12 or 3.13 is recommended. Work from this directory. Use a fresh output directory so previous evidence is preserved.

Windows PowerShell:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock-windows.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe run_experiments.py --output results/my-rerun
.\.venv\Scripts\python.exe compare_results.py results/my-rerun
```

Linux/macOS:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q
.venv/bin/python run_experiments.py --output results/my-rerun
.venv/bin/python compare_results.py results/my-rerun
```

The scientific calculation takes about 26-78 seconds on the tested laptop, plus figure creation; this is observed runtime, not a performance guarantee. The first Matplotlib import may build a font cache.

## Regenerate the manuscript

```bash
python -m pip install -r requirements-manuscript.txt
python plot_results.py results/windows-final
python build_manuscript.py
```

Run these with the chosen virtual environment's Python. The builder reads archived Windows evidence, writes `manuscript/article.pdf`, `manuscript/article.md` and `manuscript/metadata.yaml`, and uses the included licensed fonts. The executable manuscript source is `build_manuscript.py`; no TeX installation is required. The published journal template permits a non-LaTeX build; see `manuscript/TEMPLATE_ADAPTATION.md`.

## Evidence map

| Artifact | Purpose |
|---|---|
| `configs/protocol.json`, `protocol.md` | Inputs, frozen design, declared outcomes and exclusions |
| `src/metrics.py`, `tests/test_metrics.py` | Independent implementation and 40 correctness tests |
| `results/windows-final/primary.csv` | Exact and simulated scores, SD, MCSE and original comparisons |
| `results/windows-final/curves.csv` | Every declared sample size, scheme and correction |
| `results/windows-final/*draws.npz` | Saved metric values for 1000 primary and 100000 calibration repetitions |
| `results/windows-clean/` | Clean-environment rerun summaries and tables |
| `results/linux-check/` | Separate Linux run, including raw repeated-evaluation values |
| `clean_reproduction_report.json` | Equality checks and SHA256 of raw array members |
| `experiment_registry.csv`, `logs/`, root `*.log` | Batch provenance, tests, failures and execution logs |
| `source_ledger.md`, `audit/atlas_assessment.md` | Source verification, initial target decision and Atlas inspection |
| `figures/final/` | Three figures in editable-by-code PDF and PNG form |
| `manuscript/` | Article PDF, readable source, metadata, bibliography and fonts |
| `audit_results.md`, `blockers.md`, `NEXT_ACTION.md` | Current audit and precise resumption state |

Windows NPZ archives in this package were repackaged using Linux archive containers after every uncompressed NPY member was verified byte-for-byte against the Windows member SHA256 values. Array contents are identical; archive-container hashes can differ by OS/compression implementation. The original container checksums are preserved in `draw_checksums.json`. The full original Windows files remain on the user's computer.

## Scope and uncertainty

The fixed five-instance design is a counterexample, not a sample of real users. Analytic expectations have no Monte Carlo uncertainty. SD describes one five-instance sampled evaluation; MCSE describes an average across repeated evaluations. No claim is made about deployment, prevalence, causal mechanisms, training performance or novel recommendation algorithms.

The source's three-decimal AP tie between A and B is a rounding tie: unrounded B AP exceeds A AP slightly. Without replacement at all 9999 negatives exactly recovers full-catalogue metrics. The simple floor rank correction reduces AP bias here but does not restore the A-versus-C comparison at m=99.

## Release and authorship

Author: Jill Vekariya, Independent researcher. Correspondence: jillvekariya.10@gmail.com. The author confirmed review and responsibility, no competing interests, no simultaneous journal submission and no close collaboration with the original authors, and authorized public release and submission on 12 November 2026. The original instructions report no external research funding. ORCID was not supplied and remains blank. The confirmation record is in `publication/author_declarations.proposed.json`; its filename is retained for provenance, and its status is now confirmed.

ChatGPT generated and revised code, conducted tool-driven execution and analysis, and drafted the manuscript. The author accepts responsibility for the approved work. Internal audits are simulated AI assessments, not independent human peer review.

Code: MIT (see LICENSE). Manuscript: CC BY 4.0. Dependencies and bundled fonts retain their own licenses. Third-party scientific PDFs, downloaded Atlas code, credentials and Python environments are excluded from the research package.

## Release verification

`publication/issue_body.md` contains the exact journal request. See `submission_status.md` for the actual submission state and official URL when available. An open submission issue does not establish acceptance, publication or assigned peer review.

The release verifier reads YAML metadata. Install `requirements-manuscript.txt`, then run `python verify_release.py --public --manifest`. It checks the frozen scientific evidence, author/contact metadata, authorization and package hashes without rerunning the experiments. A fresh clone of the scientific snapshot passed all 40 tests, manifest checks and manuscript compilation. The numerical source, inputs and results remain unchanged.
