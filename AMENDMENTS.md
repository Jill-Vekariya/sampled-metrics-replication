# Post-submission amendment record

## 14 November 2026 - Reviewer-readiness and manuscript-quality corrections

- Corrected all known mojibake sequences in the executable manuscript builder and regenerated Markdown/PDF: mathematical inequality (≤), standard deviation (±), square root (√), and scientific-notation multiplication (×). A static test now fails if those corrupted sequences reappear.
- Added a bounded explanation of why independently computed finite distributions, simulation checks and rank reversals constitute a meaningful **partial** replication; this does not claim reproduction of trained models or real datasets.
- Distinguished the historical 40-test original execution from the later expanded regression suite, without modifying the historical experiment log.
- Created `REVIEWER_START_HERE.md` with exact source-paper-to-output mapping, comparison criteria, Linux/Windows commands, historical evidence locations and scope boundaries.
- Added non-mutating manuscript/metadata/reviewer-guide regression tests; clarified the PDF text and refined typography to avoid an orphaned page.
- Preserved a concise and accurate tool-use disclosure in the article. The public record and historical documentation were not rewritten to imply research assistance did not occur.

## 14 November 2026 - Figure 3 fidelity and manuscript rendering

The original submission remains ReScience C issue #158 (submitted 12 November 2026).
This amendment documents a correction to the *independently reconstructed*
metric-shape figure; it does **not** change the frozen protocol or primary
scientific results used for Tables 1-2 and Figure 2.

- Original source Figure 3 employs **Recall@5**, whereas the initial
  reconstruction mistakenly used **Recall@10**. Updated only the Figure 3
  plot-generation layer to compute Recall@5 expectations from the same
  binomial sampled-rank distribution; regenerated the Figure 3 PNG/PDF and
  the derived `results/windows-final/metric_shape.csv`.
- Kept Recall@10 in the frozen main experiment, protocol and archived
  simulation results. The original scientific source snapshot and the
  separately validated later-maintained `src/metrics.py` are preserved
  under the repository's existing provenance checks.
- Added nine Figure 3 regression tests to verify metric selection,
  the Recall@5 threshold, exact binomial expectations and unchanged AP,
  NDCG and AUC curves. The original 40 correctness tests are retained.
- Rebuilt `manuscript/article.pdf` with a caption and note clarifying
  Recall@5 versus Recall@10. Improved the generated `article.md` by
  removing duplicate title/author front matter and normalizing the
  ReportLab paragraph markup into readable Markdown.
- Updated the README and release verification records. The original
  submission release plan and manifest remain separately archived as
  `publication/ORIGINAL_SUBMISSION_RELEASE_PLAN.json` and
  `publication/ORIGINAL_SUBMISSION_MANIFEST.json`.

The source paper is Krichene and Rendle (IJCAI 2021),
DOI: 10.24963/ijcai.2021/651.

**Editorial note:** This is a post-submission fidelity correction, not
a claim to reproduce the original KDD 2020 trained-model experiment.
The new generated PDF and files replace current branch artifacts; the
12 November submission remains recoverable from Git history.
