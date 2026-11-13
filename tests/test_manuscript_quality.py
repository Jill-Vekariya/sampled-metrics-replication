"""Static, non-mutating checks for the published manuscript and review package."""
from pathlib import Path
import re

import yaml

ROOT = Path(__file__).resolve().parents[1]
BAD_SEQUENCES = ("Â±", "â‰¤", "âˆš", "Ã—", "â€", "Ã‚")


def read(name):
    return (ROOT / name).read_text(encoding="utf-8")


def test_no_corrupt_mathematics_in_published_source():
    for path in ("build_manuscript.py", "manuscript/article.md"):
        text = read(path)
        assert not any(bad in text for bad in BAD_SEQUENCES), path
    article = read("manuscript/article.md")
    for symbol in ("±", "≤", "√", "×"):
        assert symbol in article, symbol


def test_explicit_scope_and_current_test_history():
    article = read("manuscript/article.md")
    assert "Why this is a partial replication" in article
    assert "140 tests" in article
    assert "40 tests" in article
    assert "trained models" in article or "trained-model" in article
    assert "REVIEWER_START_HERE.md" in article


def test_reviewer_crosswalk_has_original_four_artifacts():
    guide = read("REVIEWER_START_HERE.md")
    assert all(x in guide for x in (
        "Table 1", "Table 2", "Figure 2", "Figure 3",
        "Recall@5", "Recall@10", "run_experiments.py",
        "verify_release.py", "compare_results.py",
        "partial replication",
    ))
    # Original Figure 3 fidelity fix must not silently alter Tables 1-2.
    assert "Tables 1-2" in read("AMENDMENTS.md")


def test_yaml_unfilled_editorial_fields_and_valid_type():
    metadata = yaml.safe_load(read("manuscript/metadata.yaml"))
    assert metadata["type"] == "Replication"
    assert metadata["domain"] == "Machine Learning"
    assert metadata["replication"][3]["doi"] == "10.24963/ijcai.2021/651"
    assert all(not x["name"] for x in metadata["contributors"])
    assert all(not list(x.values())[0] for x in metadata["dates"])
    assert all(not list(x.values())[0] for x in metadata["article"])


def test_manuscript_declares_actual_assistance_not_peer_review():
    article = read("manuscript/article.md")
    assert "Assistance disclosure" in article
    assert "ChatGPT" in article
    assert "author is responsible for all final claims" in article


def test_pdf_present_and_sensible_size():
    pdf = ROOT / "manuscript/article.pdf"
    assert pdf.read_bytes().startswith(b"%PDF-")
    assert 50_000 < pdf.stat().st_size < 5_000_000
