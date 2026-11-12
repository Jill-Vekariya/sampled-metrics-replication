# Internal audit - simulated AI review

This is a tool-backed self-assessment, not independent human peer review.

## Claim fidelity
PASS within the frozen scope: the primary target is the IJCAI 2021 fixed-rank example. All 12 printed exact entries match; AP/NDCG comparisons reverse as published; AUC invariance error <=1.23e-15. No claim to reproduce learned recommenders or the Zhao aggregate.

## Implementation and mathematics
PASS: 40 cases cover metric boundaries, finite-catalogue exhaustive sequence/subset enumeration, independently sampled item indices, exclusion of positives, repeated draws, binomial AP closed form, AUC identity, exact full sampling, aggregation and deterministic seeds. Timestamp, train/test leakage and model-tuning tests are inapplicable because no time series or trained model is used.

## Statistical audit
PASS with stated limitations: exact conditional expectations; macro SD distinguished from mean MCSE; no population test/CI over the five designed instances. Three independent 100000-repeat calibrations; all standardized differences <1.2. Original Table 2 differences are described as conditional Monte Carlo compatibility, not exact reproduction of an unknown source seed. Rounding nuance A/B retained.

## Reproducibility and output audit
PASS for numerical study and figures: actual primary Windows run, separate Linux run, and fresh Windows virtual environment. 40 tests passed in both Windows environments and Linux. Clean numerical summaries/raw arrays identical; clean figures regenerated. Cross-system values match within 1e-12. PDF compiled and final six pages visually inspected after a page-overflow repair. Every full-catalogue table entry and sampled AP/NDCG expectation was checked against saved evidence. Fresh isolated Linux and Windows environments installed the documented manuscript dependencies and compiled the full PDF successfully; the fresh GitHub clone verification is recorded separately.

## Citation/attribution audit
Three references verified: IJCAI target DOI/pages/authors, related KDD publication identity, and Zhao initial target. The full KDD study was not claimed to have been read or replicated. Source ledger pins fetched bytes and inspected repository commits. No original core implementation is incorporated. Atlas files were read only and excluded from release.

## Licensing/privacy audit
The public release contains original independent code, the attributed numerical fixture and generated evidence. No third-party scientific PDF, Atlas code, private user dataset, credential, environment directory or git history is in the research ZIP. MIT code, CC BY 4.0 manuscript and font licenses are retained. The user confirmed author declarations and authorized public release. Anonymous repository, PDF, metadata and protocol downloads passed HTTP and hash checks. Secret-pattern scan results are in audit/release_scan.json.

## Findings
RESOLVED: author/contact confirmation, final declarations and public-release/submission authorization. The user's exact response and context are recorded. No signature or ORCID was generated.
RESOLVED: public release and ReScience C initial submission. Official open issue: https://github.com/ReScience/submissions/issues/158; author, title and body were verified.
MAJOR scope limitation: only a designed numerical counterexample is replicated. Editorial sufficiency remains the journal's decision.
LIMITATION: no independent external human reproduction/review has yet been confirmed. Editorial assignment, acceptance and publication are not claimed.
RESOLVED: Windows provenance path bug before evaluation; test-only log(0) warning; parent-directory Linux test invocation; PDF orphan-page layout. Scientific protocol unchanged after freezing.

## Historical pre-release internal scorecard
| Criterion | Score /5 | Evidence / remaining limit |
|---|---:|---|
| Published-claim fidelity |4|Exact narrow target; full-paper conclusions excluded|
| Independent implementation |4|Original source and independent oracles; AI generated; author approval now recorded|
| Experimental correctness |4|40 tests, analytic identities, raw evidence; narrow fixture|
| Statistical validity |4|Correct conditional moments/MCSE; no real population inference|
| Reproducibility |4|Fresh Windows numerical/figure rerun; fresh Linux manuscript build passed; no external human reproduction|
| Scientific interpretation |4|Scope/negative limitations explicit|
| Literature/citations |3|Authentic focused sources; overlap search not exhaustive|
| Documentation/code |4|Frozen config, registries, logs, README and resumption state|
| Journal compliance |2|Pre-release score; declarations, public URLs and submission now completed|
| Transparency/ethics |4|AI disclosure, actual failures retained, no fabricated declarations|

Total 37/50, a subjective internal heuristic. This historical score is not peer review or evidence of acceptance.

## Final preparation audit update

Current form and metadata template were re-fetched and matched the previous audit. Metadata has the complete confirmed author/contact, corresponding-author marker, original DOI and intended code/data URLs, with a double-quoted abstract. The exact issue body and author review packet are prepared. The new offline release preflight passes required file, source hash, protocol, frozen claim, metadata, citation, clean reproduction, array member and analytical-condition checks. No public attestation is implied by this PASS.

Final private-repository clone audit: the main-branch snapshot was cloned through the existing authenticated CLI, manifest checks passed, all 40 tests passed and the manuscript compiled with the documented dependencies. Public release and journal submission remain unexecuted.

## Final submission checkpoint

Author-approved release preflight passed on Windows and Linux. Scientific source/protocol/result hashes are unchanged. Official submission https://github.com/ReScience/submissions/issues/158 was created at 2026-11-12T14:49:07Z and read back with matching title, account and body. The public research package and final six-page manuscript are complete. No assigned peer review, acceptance, publication or journal DOI is asserted.
