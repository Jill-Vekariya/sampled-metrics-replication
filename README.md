# Ranking reversals under sampled recommendation metrics

Status: **AWAITING PUBLICATION AUTHORIZATION**. Research and release preparation are complete; author confirmation/access recovery are pending. Not submitted or peer reviewed.

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
| `manuscript/` | PDF draft, readable source, metadata, bibliography and fonts |
| `audit_results.md`, `blockers.md`, `NEXT_ACTION.md` | Current audit and precise resumption state |

Windows NPZ archives in this package were repackaged using Linux archive containers after every uncompressed NPY member was verified byte-for-byte against the Windows member SHA256 values. Array contents are identical; archive-container hashes can differ by OS/compression implementation. The original container checksums are preserved in `draw_checksums.json`. The full original Windows files remain on the user's computer.

## Scope and uncertainty

The fixed five-instance design is a counterexample, not a sample of real users. Analytic expectations have no Monte Carlo uncertainty. SD describes one five-instance sampled evaluation; MCSE describes an average across repeated evaluations. No claim is made about deployment, prevalence, causal mechanisms, training performance or novel recommendation algorithms.

The source's three-decimal AP tie between A and B is a rounding tie: unrounded B AP exceeds A AP slightly. Without replacement at all 9999 negatives exactly recovers full-catalogue metrics. The simple floor rank correction reduces AP bias here but does not restore the A-versus-C comparison at m=99.

## Release and authorship

No public-release command has been executed, no issue submitted, and no declaration signed. The private repository was created successfully and its PRIVATE visibility was verified; nothing is public. The user confirmed the author name as Jill Vekariya; independent-researcher status was supplied in the original instructions. Corresponding email is confirmed as jillvekariya.10@gmail.com. ORCID may be added if held; conflicts, author responsibility and final permission to publish remain to be confirmed. The computer's authenticated GitHub CLI separately identified Jill-Vekariya. No author data is inferred from the GitHub username. AI assistance is explicitly disclosed in the draft. The internal audits are simulated AI reviews, not external peer review.

Code: MIT (see LICENSE). Manuscript: intended CC BY 4.0 upon authorized release. Dependencies and bundled fonts retain their own licenses. Third-party scientific PDFs, downloaded Atlas code, credentials and Python environments are excluded from the review ZIP.

## Final publication preparation

The current ReScience issue form and mandatory YAML schema were rechecked. `publication/issue_body.md` is the exact prepared request; its URLs are intended publication targets and are not yet publicly verified. `publication/PUBLICATION_REVIEW.md` summarizes the concrete release and proposed author declarations. `verify_release.py --manifest` checks the packaged evidence and hashes without rerunning experiments; `--public` additionally requires actual confirmation/authorization.

A fresh isolated Linux environment installed requirements-manuscript.txt and compiled the complete PDF; the record is in publication/manuscript_build_reproduction.json. The saved study source and all results remain unchanged. The computer's latest metadata edits were compiled successfully before its connection stopped responding; the prepared release has now been staged in the verified PRIVATE GitHub repository. The downloadable review package is the current complete checkpoint.

The release verifier reads YAML metadata. Install `requirements-manuscript.txt` before `python verify_release.py --manifest`; the numerical tests and experiments alone require `requirements.txt`. The private staging checkout preserves file bytes and line endings for the manifest checks.
