"""Regression tests for the IJCAI Figure 3 reconstruction.

Figure 3 uses Recall@5, unlike the paper's Tables 1-2 and Figure 2,
which use Recall@10. The frozen primary experiment is unchanged.
"""
import numpy as np
import pytest
from scipy.stats import binom

from plot_results import FIGURE3_METRICS, figure3_metric_values
from src.metrics import METRICS, metric, moments


def test_figure3_uses_source_metric_order():
    assert FIGURE3_METRICS == ("AP", "NDCG", "Recall@5", "AUC")
    assert "Recall@10" in METRICS
    assert "Recall@5" not in METRICS


def test_recall5_exact_boundary():
    ranks = np.array([1, 4, 5, 6, 10, 20])
    _, exact = figure3_metric_values(ranks, 20, 10, "Recall@5")
    np.testing.assert_array_equal(exact, [1, 1, 1, 0, 0, 0])
    np.testing.assert_array_equal(metric([5, 6], 20, "Recall@10"), [1, 1])


@pytest.mark.parametrize("m", [1, 4, 10, 25])
def test_recall5_expectation_matches_independent_binomial_oracle(m):
    n = 100
    ranks = np.array([1, 2, 5, 6, 20, 75, 100])
    expected, _ = figure3_metric_values(ranks, n, m, "Recall@5")
    probabilities = (ranks - 1) / (n - 1)
    # Sampled Recall@5 = 1 exactly when the sampled rank is <= 5,
    # i.e., when at most 4 negatives outrank the relevant item.
    np.testing.assert_allclose(
        expected, binom.cdf(4, m, probabilities), atol=1e-13, rtol=0
    )


@pytest.mark.parametrize("name", ["AUC", "AP", "NDCG"])
def test_other_figure3_metrics_unchanged(name):
    ranks, n, m = np.array([1, 5, 6, 20]), 100, 10
    expected, exact = figure3_metric_values(ranks, n, m, name)
    reference, _ = moments(ranks, n, m, name)
    np.testing.assert_allclose(expected, reference)
    np.testing.assert_allclose(exact, metric(ranks, n, name))
