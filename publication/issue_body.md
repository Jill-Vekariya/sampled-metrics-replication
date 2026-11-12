**Original article:**
Walid Krichene and Steffen Rendle. *On Sampled Metrics for Item Recommendation (Extended Abstract).* Proceedings of IJCAI 2021, pp. 4784-4788. DOI: https://doi.org/10.24963/ijcai.2021/651

**PDF URL:** https://raw.githubusercontent.com/Jill-Vekariya/sampled-metrics-replication/main/manuscript/article.pdf

**Metadata URL:** https://raw.githubusercontent.com/Jill-Vekariya/sampled-metrics-replication/main/manuscript/metadata.yaml

**Code URL:** https://github.com/Jill-Vekariya/sampled-metrics-replication

**Scientific domain:** Machine Learning

**Programming language:** Python

**Suggested editor:** No preference; editorial assignment is requested.

**Replication scope:** Partial replication of the three constructed rank lists in Tables 1-2 and the expectation-curve findings in Figures 2-3. It does not include the KDD 2020 trained-model experiment. Finite-distribution expectations, independent random simulations, small-catalogue exhaustive checks and a clean Windows reproduction support the AP/NDCG ranking-reversal result; expected AUC remains invariant. Narrow scope and uncertainty are documented in the manuscript.

**Reproduction:** Install requirements.txt, run `python -m pytest -q`, then `python run_experiments.py --output results/reviewer-run` and `python compare_results.py results/reviewer-run`. Manuscript requirements and build instructions are in README.md.

**AI assistance:** ChatGPT assisted with code generation, tool-driven execution, analysis and drafting, as disclosed in the article. Internal assessments are not independent human peer review.
