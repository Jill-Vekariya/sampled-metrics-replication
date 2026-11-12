"""Analytic identities and independent exhaustive/item-level oracles."""
import itertools
import math
import numpy as np
import pytest
from src.metrics import (metric, distribution, moments, macro_moments,
                         monte_carlo, draw_rank_from_catalogue, METRICS)


@pytest.mark.parametrize("name,expected", [
    ("AUC", [1, .5, 0]), ("AP", [1, 1/3, .2]),
    ("NDCG", [1, .5, 1/np.log2(6)]), ("Recall@10", [1, 1, 1])])
def test_hand_calculated(name, expected):
    np.testing.assert_allclose(metric([1, 3, 5], 5, name), expected)


def test_recall_boundary():
    np.testing.assert_array_equal(metric([10, 11], 20, "Recall@10"), [1, 0])


@pytest.mark.parametrize("bad", [[], [0], [11], [1.5], [float('nan')], [float('inf')]])
def test_reject_invalid_rank(bad):
    with pytest.raises(ValueError): metric(bad, 10, "AP")


@pytest.mark.parametrize("mode", ["with_replacement", "without_replacement"])
@pytest.mark.parametrize("r", [1, 2, 4, 6])
def test_exhaustive_distribution(mode, r):
    n, m = 6, 3
    outcomes = (itertools.product(range(n - 1), repeat=m) if mode == "with_replacement"
                else itertools.combinations(range(n - 1), m))
    counts = np.zeros(m + 1)
    for selection in outcomes:
        counts[sum(x < r - 1 for x in selection)] += 1
    _, probability = distribution([r], n, m, mode)
    np.testing.assert_allclose(counts / counts.sum(), probability[0], atol=1e-14)


@pytest.mark.parametrize("name", METRICS)
def test_complete_catalogue(name):
    r = [1, 10, 99]
    mean, variance = moments(r, 99, 98, name, "without_replacement")
    np.testing.assert_allclose(mean, metric(r, 99, name), atol=1e-13)
    np.testing.assert_allclose(variance, 0, atol=1e-14)


@pytest.mark.parametrize("mode", ["with_replacement", "without_replacement"])
@pytest.mark.parametrize("m", [1, 9, 99])
def test_auc_invariance(mode, m):
    r = [1, 2, 42, 99, 100]
    mean, _ = moments(r, 100, m, "AUC", mode)
    np.testing.assert_allclose(mean, metric(r, 100, "AUC"), atol=1e-13)


def test_ap_closed_form():
    n, m = 10000, 99
    ranks = np.array([1, 2, 100, 9999, 10000])
    p = (ranks - 1) / (n - 1)
    expected = np.ones(len(ranks))
    positive = (p > 0) & (p < 1)
    expected[positive] = -np.expm1((m + 1) * np.log1p(-p[positive])) / ((m + 1) * p[positive])
    expected[p == 1] = 1 / (m + 1)
    actual, _ = moments(ranks, n, m, "AP")
    np.testing.assert_allclose(actual, expected, atol=1e-13)


def test_one_negative_affine():
    r, n = np.array([1, 100, 9000, 10000]), 10000
    p = (r - 1) / (n - 1)
    for name in METRICS:
        a, b = metric([1, 2], 2, name)
        mean, _ = moments(r, n, 1, name)
        np.testing.assert_allclose(mean, (1-p)*a+p*b)


@pytest.mark.parametrize("mode", ["with_replacement", "without_replacement"])
def test_actual_item_sampler(mode):
    n, r, m, repetitions = 15, 7, 9, 30000
    sampled = draw_rank_from_catalogue(r, n, m, np.random.default_rng(314159),
                                       mode == "with_replacement", repetitions)
    for name in METRICS:
        values = metric(sampled, m + 1, name)
        mean, var = moments([r], n, m, name, mode)
        assert abs(values.mean() - mean[0]) <= 6 * math.sqrt(var[0] / repetitions) + 1e-12


def test_duplicate_draws_count_and_positive_excluded():
    # Only negative in a 2-item catalogue; all draws must outrank rank 2.
    sampled = draw_rank_from_catalogue(2, 2, 20, np.random.default_rng(1), True, 10)
    np.testing.assert_array_equal(sampled, np.full(10, 21))
    np.testing.assert_array_equal(draw_rank_from_catalogue(1, 2, 20,
                                  np.random.default_rng(1), True, 10), np.ones(10))


def test_macro_sd_uses_independence_and_mean():
    single_mean, single_var = moments([3], 10, 3, "AP")
    mean, sd = macro_moments([3]*5, 10, 3, "AP")
    assert mean == pytest.approx(single_mean[0])
    assert sd == pytest.approx(np.sqrt(single_var[0] / 5))


def test_correction_floor():
    n, m, rank = 10, 3, 5
    _, probability = distribution([rank], n, m)
    # Exact integer arithmetic avoids floating boundary errors.
    oracle = sum(float(probability[0,k]) / math.floor(1+9*k/3) for k in range(4))
    actual, _ = moments([rank], n, m, "AP", correction=True)
    assert actual[0] == pytest.approx(oracle)


def test_same_seed_reproducible():
    a = monte_carlo([2, 4], 10, 5, 100, 7)
    b = monte_carlo([2, 4], 10, 5, 100, 7)
    for name in METRICS: np.testing.assert_array_equal(a[name], b[name])


@pytest.mark.parametrize("mode,m", [("without_replacement",10),("other",2),("with_replacement",0)])
def test_invalid_candidate_rules(mode,m):
    with pytest.raises(ValueError): distribution([2],10,m,mode)
