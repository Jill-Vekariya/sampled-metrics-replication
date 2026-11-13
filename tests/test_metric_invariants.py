"""Bounds, ranking direction and deterministic sampling boundaries."""
import numpy as np
import pytest

from src.metrics import METRICS, distribution, metric


@pytest.mark.parametrize("name", METRICS)
def test_metrics_are_bounded_and_nonincreasing(name):
    ranks = np.arange(1, 21)
    values = metric(ranks, 20, name)
    assert np.isfinite(values).all()
    assert np.all((values >= 0) & (values <= 1))
    assert np.all(np.diff(values) <= 0)


@pytest.mark.parametrize("name", METRICS)
def test_metric_catalogue_endpoints(name):
    n = 20
    expected_last = {
        "AUC": 0.0,
        "AP": 1.0 / n,
        "NDCG": 1.0 / np.log2(n + 1),
        "Recall@10": 0.0,
    }
    np.testing.assert_allclose(
        metric([1, n], n, name), [1.0, expected_last[name]],
        rtol=0, atol=1e-14,
    )


@pytest.mark.parametrize("mode", ["with_replacement", "without_replacement"])
@pytest.mark.parametrize("m", [1, 3, 7])
def test_extreme_ranks_have_deterministic_distributions(mode, m):
    k, probabilities = distribution([1, 8], 8, m, mode)
    np.testing.assert_array_equal(k, np.arange(m + 1))
    assert probabilities.shape == (2, m + 1)
    expected = np.zeros((2, m + 1))
    expected[0, 0] = 1.0
    expected[1, m] = 1.0
    np.testing.assert_allclose(probabilities, expected, rtol=0, atol=1e-14)
