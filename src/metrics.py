"""Independent single-relevant-item metric and sampling calculations.

Written from the definitions in Krichene & Rendle (IJCAI 2021), not their code.
"""
import numpy as np
from scipy.stats import binom, hypergeom

METRICS = ("AUC", "AP", "NDCG", "Recall@10")


def validate_ranks(ranks, n):
    r = np.asarray(ranks)
    if not isinstance(n, (int, np.integer)) or isinstance(n, bool) or n < 2:
        raise ValueError("catalogue size must be an integer >= 2")
    if r.size == 0 or not np.isfinite(r).all():
        raise ValueError("ranks must be nonempty and finite")
    if np.any(r != np.floor(r)) or np.any((r < 1) | (r > n)):
        raise ValueError("ranks must be integers in [1,n]")
    return r.astype(np.int64)


def metric(ranks, n, name):
    r = validate_ranks(ranks, n)
    if name == "AUC":
        return (n - r) / (n - 1)
    if name == "AP":
        return 1.0 / r
    if name == "NDCG":
        return 1.0 / np.log2(r + 1)
    if name == "Recall@10":
        return (r <= 10).astype(float)
    raise ValueError("unknown metric: " + name)


def distribution(ranks, n, m, mode="with_replacement"):
    r = validate_ranks(ranks, n).reshape(-1)
    if not isinstance(m, (int, np.integer)) or isinstance(m, bool) or m < 1:
        raise ValueError("m must be an integer >=1")
    if mode == "without_replacement" and m > n - 1:
        raise ValueError("cannot draw more distinct negatives than available")
    k = np.arange(m + 1)
    if mode == "with_replacement":
        probabilities = binom.pmf(k[None, :], m, (r[:, None] - 1) / (n - 1))
    elif mode == "without_replacement":
        probabilities = hypergeom.pmf(k[None, :], n - 1, r[:, None] - 1, m)
    else:
        raise ValueError("unknown sampling mode")
    if not np.allclose(probabilities.sum(axis=1), 1, atol=1e-10, rtol=0):
        raise ArithmeticError("probability mass not conserved")
    return k, probabilities


def moments(ranks, n, m, name, mode="with_replacement", correction=False):
    k, probabilities = distribution(ranks, n, m, mode)
    if correction:
        # The source specifies floor in its Eq.9 experiments.
        estimated_rank = 1 + ((n - 1) * k // m)
        values = metric(estimated_rank, n, name)
    else:
        values = metric(k + 1, m + 1, name)
    first = probabilities @ values
    variance = np.maximum(probabilities @ (values ** 2) - first ** 2, 0)
    return first, variance


def macro_moments(ranks, n, m, name, mode="with_replacement", correction=False):
    mean, variance = moments(ranks, n, m, name, mode, correction)
    return float(mean.mean()), float(np.sqrt(variance.sum()) / len(mean))


def monte_carlo(ranks, n, m, repetitions, seed, mode="with_replacement"):
    r = validate_ranks(ranks, n).reshape(-1)
    if repetitions < 2:
        raise ValueError("at least two repetitions required")
    rng = np.random.default_rng(seed)
    if mode == "with_replacement":
        k = rng.binomial(m, (r - 1) / (n - 1), (repetitions, len(r)))
    elif mode == "without_replacement" and 1 <= m <= n - 1:
        k = rng.hypergeometric(r - 1, n - r, m, (repetitions, len(r)))
    else:
        raise ValueError("invalid sampling mode or sample size")
    return {name: metric(k + 1, m + 1, name).mean(axis=1) for name in METRICS}


def draw_rank_from_catalogue(rank, n, m, rng, replace=True, repetitions=1):
    """Independent direct item-index sampler for correctness checks.

    Index 0..n-2 represents negatives, ordered around the excluded positive.
    The first rank-1 negatives beat the positive. Repeated indices count
    repeatedly under replacement, as required by the binomial protocol.
    """
    validate_ranks([rank], n)
    if not isinstance(m, int) or m < 1 or (not replace and m > n - 1):
        raise ValueError("invalid number of negative draws")
    if replace:
        draws = rng.integers(0, n - 1, size=(repetitions, m))
        return 1 + (draws < rank - 1).sum(axis=1)
    return np.array([1 + np.count_nonzero(rng.choice(n - 1, m, replace=False) < rank - 1)
                     for _ in range(repetitions)])
