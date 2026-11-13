# ReScience C template comparison and reproducible PDF build

## Reference and compliance boundary

Official ReScience article template: https://github.com/ReScience/template,
commit `0978d0e5d9a86246789fd3468aec6fc71e39c944`.

Compared the actual `rescience.cls`, `header.tex`, and a public journal PDF:
https://zenodo.org/records/4022518/files/article.pdf .
ReScience permits an alternative PDF build provided it adheres to the
proposed manuscript style, and requires the article metadata YAML.
This is a **style adaptation**, not a claim to have compiled the official
LaTeX class or to reproduce its fonts pixel for pixel.

## Template elements matched by the ReportLab build

| Official template | Reproduced local behavior |
|---|---|
| A4 paper | A4 paper |
| Margins: left 4.5 cm, right 3 cm, top 3 cm, bottom 3.5 cm | The same page geometry, verified against the class |
| Upper-left dark-red journal tag, `#CF232B` | Upper-left `RESCIENCE C` tag with that accent |
| Flush-left large sans-serif title, smaller authors and affiliation | Matching title, author, and affiliation hierarchy |
| Black serif body text and sans-serif headings | Licensed DejaVu Serif and Sans, bundled with project |
| Light-gray section numerals | Separate gray numerals in the PDF headings |
| Compact tables and figures within text column | Table widths scaled to available text width; figures keep native proportions and stay with captions |
| Page footer and journal identification | Consistent low-profile journal identification and page numbering |

The official class uses Source Serif Pro and Roboto Condensed. Those are
**not** included or required by this alternative builder. The bundled
DejaVu fonts are a licensed, reproducible substitution, not a precise
font match. The template's conditional peer-review metadata sidebar
is not reproduced because this is a pre-acceptance manuscript and editor,
reviewer, journal DOI and publication dates have not been assigned.
No editorial identity or outcome is invented.

## Reproducible article assets

Executable manuscript source: `../build_manuscript.py` (ReportLab).
Readable manuscript source: `article.md`.
Paper: `article.pdf` (seven A4 pages at this amendment).
Figures: `../plot_results.py` and `../figures/final/`.
Metadata: `metadata.yaml`, populated by the same builder.

Build from the repository root, ideally from a disposable clone:

```bash
python -m pip install -r requirements.txt -r requirements-manuscript.txt
python plot_results.py results/windows-final
python build_manuscript.py
python -m pytest -q
python verify_release.py --public --manifest
```

The generator overwrites derived figures and manuscript files. The
release manifest describes the **committed** artifact bytes; rebuilding
locally may change PDF binary metadata even without changing scientific
content. For a strict package-manifest check, use a clean checkout of the
committed release, not modified generated files.

Scientific scope and original-to-reproduced artifact correspondence are
documented in `../REVIEWER_START_HERE.md`. The original frozen protocol and
primary simulation outputs remain unchanged.
