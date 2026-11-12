# Internal audit - simulated AI review

This is a tool-backed self-assessment, not independent human peer review.

## Claim fidelity
PASS within the frozen scope: the primary target is the IJCAI 2021 fixed-rank example. All 12 printed exact entries match; AP/NDCG comparisons reverse as published; AUC invariance error <=1.23e-15. No claim to reproduce learned recommenders or the Zhao aggregate.

## Implementation and mathematics
PASS: 40 cases cover metric boundaries, finite-catalogue exhaustive sequence/subset enumeration, independently sampled item indices, exclusion of positives, repeated draws, binomial AP closed form, AUC identity, exact full sampling, aggregation and deterministic seeds. Timestamp, train/test leakage and model-tuning tests are inapplicable because no time series or trained model is used.

## Statistical audit
PASS with stated limitations: exact conditional expectations; macro SD distinguished from mean MCSE; no population test/CI over the five designed instances. Three independent 100000-repeat calibrations; all standardized differences <1.2. Original Table 2 differences are described as conditional Monte Carlo compatibility, not exact reproduction of an unknown source seed. Rounding nuance A/B retained.

## Reproducibility and output audit
PASS for numerical study and figures: actual primary Windows run, separate Linux run, and fresh Windows virtual environment. 40 tests passed in both Windows environments and Linux. Clean numerical summaries/raw arrays identical; clean figures regenerated. Cross-system values match within 1e-12. PDF compiled and final six pages visually inspected after a page-overflow repair. Every full-catalogue table entry and sampled AP/NDCG expectation was checked against saved evidence. The PDF build itself was not repeated in the clean Windows environment; a fresh isolated Linux manuscript environment subsequently installed the documented dependencies and built the full PDF successfully.

## Citation/attribution audit
Three references verified: IJCAI target DOI/pages/authors, related KDD publication identity, and Zhao initial target. The full KDD study was not claimed to have been read or replicated. Source ledger pins fetched bytes and inspected repository commits. No original core implementation is incorporated. Atlas files were read only and excluded from release.

## Licensing/privacy audit
Private release candidate contains original independent code, attributed numerical fixture and generated evidence. No third-party scientific PDF, Atlas code, private user dataset, credential, environment directory or git credential/history file is included. MIT code license, intended CC BY manuscript release and licensed bundled fonts documented. No public upload has occurred. Secret-pattern scan results are in release_scan.json.

## Findings
UPDATE: author name confirmed as Jill Vekariya. Corresponding email confirmed: jillvekariya.10@gmail.com. BLOCKER under the original user execution protocol: personal author confirmation and the final public-release/submission authorization checkpoint remain outstanding. ORCID may be added if held.
RESOLVED transport uncertainty: cached output confirmed the repository was created successfully and is PRIVATE. Public URL access remains to be checked after the reserved final authorization checkpoint. No public release or journal issue creation was attempted.
MAJOR scope limitation: only a designed numerical counterexample is replicated. ReScience editorial sufficiency is uncertain; do not market this as a full ML study or high-impact new result.
MINOR: no external human reproduction/review yet; public download and journal submission not attempted.
RESOLVED: Windows provenance path bug before evaluation; test-only log(0) warning; parent-directory Linux test invocation; PDF orphan-page layout. Scientific protocol unchanged after freezing.

## Evidence scorecard
| Criterion | Score /5 | Evidence / remaining limit |
|---|---:|---|
| Published-claim fidelity |4|Exact narrow target; full-paper conclusions excluded|
| Independent implementation |4|Original source and independent oracles; AI generated and author review pending|
| Experimental correctness |4|40 tests, analytic identities, raw evidence; narrow fixture|
| Statistical validity |4|Correct conditional moments/MCSE; no real population inference|
| Reproducibility |4|Fresh Windows numerical/figure rerun; fresh Linux manuscript build passed; no external human reproduction|
| Scientific interpretation |4|Scope/negative limitations explicit|
| Literature/citations |3|Authentic focused sources; overlap search not exhaustive|
| Documentation/code |4|Frozen config, registries, logs, README and resumption state|
| Journal compliance |2|Current form/template checked; author declarations/public URLs/final checkpoint unresolved|
| Transparency/ethics |4|AI disclosure, actual failures retained, no fabricated declarations|

Total 37/50, a subjective internal heuristic. This score does not establish submission readiness.

## Final preparation audit update

Current form and metadata template were re-fetched and matched the previous audit. Metadata has the complete confirmed author/contact, corresponding-author marker, original DOI and intended code/data URLs, with a double-quoted abstract. The exact issue body and author review packet are prepared. The new offline release preflight passes required file, source hash, protocol, frozen claim, metadata, citation, clean reproduction, array member and analytical-condition checks. No public attestation is implied by this PASS.
