# Source ledger
Checked 12 November 2026. Files are audit caches, not redistribution permission.

| Role | Source | Verification | SHA256 of retrieved file |
|---|---|---|---|
|Primary numerical target|https://www.ijcai.org/proceedings/2021/0651.pdf|Tables 1-2; Sections 3.1-3.2; Figures 2-3; Eq9 secondary|5f7b49ac4be0d293999cf048d92d28e36651b6c04819feec41fdf915dfe537f8|
|Primary bibliographic record|https://ijcai.org/proceedings/2021/651|DOI 10.24963/ijcai.2021/651, pp.4784-4788; authors Krichene and Rendle|not a byte-pinned download|
|Related KDD publication|https://research.google/pubs/on-sampled-metrics-for-item-recommendation/|KDD 2020; DOI 10.1145/3394486.3403226. Full real-data experiment not replicated|not a byte-pinned download|
|Initial target audited|https://doi.org/10.1145/3545796|Section 5.2; Fig6; Table6. Not the chosen final target|56189edf9e0946be810eb218470665322deae918e5c4a20e534121327bd3e612|
|Initial source repository|https://github.com/RUCAIBox/RecSysEvaluation|commit ffc46aad5d25797b4c47df83a00e9b71c4d25bd2; configs/scripts inspected, never executed|de18e9be60b1a3b43681c4bc91e4ab859a157e4f780acc0eae348b75d2e36937|
|Atlas context|https://github.com/Jill-Vekariya/atlas-recsys|commit 3c83f82f937ab5508b77ddae1a347bc10c5b9daa; public source audit only; no retraining or edits|5bd471f9f6364e369e05d5ae292773eb40f53f594c9d4fe812e702e66040cd1f|
|ReScience scope|https://rescience.github.io/write/|rigor, original source, substantive evidence, public code; partial replication form exists|not a byte-pinned download|
|Current submission form|https://github.com/ReScience/submissions|commit 546f3f9d67e3a3673d588eb7aeb4eba725e98ec3; issue with PDF, metadata, code URLs|98313907d57a78cdb6ea8a72e6008a83ee5230444d0f75e554f0f6a9051c18b3|
|Current official template|https://github.com/ReScience/template|commit 0978d0e5d9a86246789fd3468aec6fc71e39c944; optional LaTeX, mandatory metadata; GPL/Apache/SIL licenses|d933f0cf8da0909113b483fd310290da925c0078d222aede4097441a0af7fa10|
|Submission overlap search|https://api.github.com/repos/ReScience/submissions/issues?state=all&per_page=100|100 issue records plus page2 55 records; case-insensitive title/body search for recommend, sampled metrics, Krichene, DOI. No match; not proof of novelty|3b49e86884947fee86c19e733d186de6d750ecfc046069e6d271b11a5a75e32f|
|Published articles overlap search|https://github.com/ReScience/articles|267 tree entries; filename scan only, search engine queries additionally checked; not exhaustive fulltext literature review|e8dd12a2d393128a262cf09b8a0d7e3c606946e164cf1b580f2db533edc314cf|

Final pre-submission refresh: audit/current_venue/refresh_report.json records current retrieval status and hashes. Current journal form and metadata template matched the original audit. Searches found no ReScience issue naming Krichene and no repository matching the narrow query; this is a limited search and does not establish novelty. The current official FAQ states no publication fees. The source caches and third-party article PDFs are not redistributed in the release package.
