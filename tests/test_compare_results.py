"""Regression tests for archived-result comparison."""
from copy import deepcopy

import pytest

from compare_results import FIELDS, compare_summaries


def summary():
    row = {"model": "baseline", "metric": "ndcg"}
    row.update(dict.fromkeys(FIELDS, 0.5))
    return {"protocol_sha256": "same-protocol", "primary": [row]}


def test_identical_summaries_match():
    original = summary()
    assert compare_summaries(original, deepcopy(original)) == []


def test_protocol_mismatch_is_rejected():
    rerun = summary()
    rerun["protocol_sha256"] = "different-protocol"
    with pytest.raises(ValueError, match="Protocol changed"):
        compare_summaries(summary(), rerun)


def test_missing_primary_row_is_rejected():
    rerun = summary()
    rerun["primary"] = []
    with pytest.raises(ValueError, match="counts differ"):
        compare_summaries(summary(), rerun)


@pytest.mark.parametrize("field", ["model", "metric"])
def test_identity_mismatch_is_rejected(field):
    rerun = summary()
    rerun["primary"][0][field] = "different"
    with pytest.raises(ValueError, match="model/metric order differs"):
        compare_summaries(summary(), rerun)


@pytest.mark.parametrize("field", FIELDS)
def test_numeric_difference_identifies_field(field):
    rerun = summary()
    rerun["primary"][0][field] = 0.75
    assert compare_summaries(summary(), rerun) == [{
        "model": "baseline", "metric": "ndcg", "field": field,
        "reference": 0.5, "rerun": 0.75,
    }]


def test_roundoff_within_tolerance_matches():
    rerun = summary()
    rerun["primary"][0]["exact"] += 5e-13
    assert compare_summaries(summary(), rerun) == []
