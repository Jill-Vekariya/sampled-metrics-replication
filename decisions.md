# Decisions
1. Keep all work separate from Atlas; public source inspection only.
2. Primary target considered: Zhao et al. 2022 Figure 6. Twelve models, seven timestamped datasets and exhaustive tuning are outside a bounded laptop replication. A smaller model subset would not establish its rank correlations.
3. Alternative considered: Zhao Table 6 / ML-1M with Pop and ItemKNN. Available repository has configs and scripts but no per-model result artifacts. An average over two models cannot reproduce a twelve-model mean. The timestamp code also needs independent scrutiny (repeated indexed writes); no claim of a confirmed source-code error is made.
4. Selected alternative: Krichene and Rendle, IJCAI 2021, Tables 1-2 and Figures 2-3, Sections 3.1-3.2. This is a published, self-contained numerical counterexample with exact inputs. It permits faithful low-resource independent computation. Related KDD 2020 publication is context, not a claim to reproduce its entire empirical study.
5. ReScience eligibility remains an editorial judgment. A small, well-known illustrative result may be deemed insufficient; do not call this submission-ready merely because code runs.
6. Primary sampling uses replacement as specified by Section 3.2. Without-replacement sampling and floor rank correction are declared secondary analyses before evaluation.
7. No original core code is reused. NumPy/SciPy probability functions are dependencies, checked against exhaustive combinatorics and direct random item sampling.

## Authorized public release and submission, 12 November 2026

The author confirmed the final declarations and explicitly instructed submission. The existing repository was made public after approved file and manifest checks. Anonymous downloads matched the release hashes. The exact prepared issue was created once at https://github.com/ReScience/submissions/issues/158 and read back. Scope, source, protocol and results are unchanged. Open submission is recorded as awaiting editorial handling, without inventing a decision or DOI.
