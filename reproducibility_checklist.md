# Reproducibility checklist

- [x] Frozen source inputs and protocol SHA256 preserved.
- [x] 40 tests passed on primary Windows environment.
- [x] Real Windows primary run completed; all declared directional/rounding checks passed.
- [x] Saved primary and 100000-repeat calibration metric arrays.
- [x] Every declared analytical grid row retained.
- [x] Linux implementation run and all 40 tests completed.
- [x] Windows clean virtual environment installed exact dependency lock.
- [x] Clean tests: 40 passed.
- [x] Clean full numerical experiment completed. Primary summaries and raw arrays identical.
- [x] Clean figure regeneration completed, FIGURE_EXIT=0.
- [x] Cross-system primary comparison passed at absolute tolerance 1e-12.
- [x] Tables and figures generated from saved artifacts.
- [x] PDF source compiles using ReportLab with bundled licensed fonts; manuscript numerical consistency checked.
- [x] Final PDF pages visually reviewed after layout repair.
- [x] Manuscript dependencies installed and the entire PDF compiled in a fresh isolated Linux environment; see publication/manuscript_build_reproduction.json.
- [ ] Clean Windows manuscript build: not performed; Windows numerical/figure reproduction passed and the later author metadata PDF compiled in the original Windows environment.
- [ ] External human reproduction: not performed.
- [ ] Public download URL test: not applicable before release authorization.

NPZ-container portability: archived Windows array members were matched byte-for-byte to the independent Linux streams and repackaged; original device container hashes remain recorded. This does not claim identical ZIP container bytes across platforms.

- [x] A fresh clone from the private GitHub repository passed manifest checks, all 40 tests and manuscript compilation using the isolated Windows reproduction environment. See publication/clone_verification_receipt.json.
