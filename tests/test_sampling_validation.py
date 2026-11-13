"""Sampling counts must be integers, never booleans or fractions."""
import numpy as np
import pytest

from src.metrics import distribution, draw_rank_from_catalogue, monte_carlo

MODES = ("with_replacement", "without_replacement")
BAD_COUNTS = [True, np.bool_(True), 0, -1, 2.5, float("nan"), float("inf"), "3", None]


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("bad", BAD_COUNTS)
def test_invalid_sample_sizes_are_rejected(mode, bad):
    calls = [
        lambda: distribution([2], 10, bad, mode),
        lambda: monte_carlo([2], 10, bad, 3, 7, mode),
        lambda: draw_rank_from_catalogue(
            2, 10, bad, np.random.default_rng(7), mode == "with_replacement", 3),
    ]
    for call in calls:
        with pytest.raises(ValueError, match="m must be an integer"):
            call()


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("bad", BAD_COUNTS)
def test_invalid_repetitions_are_rejected(mode, bad):
    with pytest.raises(ValueError, match="repetitions must be an integer"):
        monte_carlo([2], 10, 3, bad, 7, mode)
    with pytest.raises(ValueError, match="repetitions must be an integer"):
        draw_rank_from_catalogue(
            2, 10, 3, np.random.default_rng(7), mode == "with_replacement", bad)


@pytest.mark.parametrize("mode", MODES)
def test_numpy_integer_counts_match_python_integers(mode):
    ordinary = monte_carlo([2], 10, 3, 4, 7, mode)
    numpy_counts = monte_carlo([2], 10, np.int64(3), np.int64(4), 7, mode)
    for name in ordinary:
        np.testing.assert_array_equal(ordinary[name], numpy_counts[name])
    replace = mode == "with_replacement"
    expected = draw_rank_from_catalogue(2, 10, 3, np.random.default_rng(7), replace, 4)
    actual = draw_rank_from_catalogue(
        2, 10, np.int64(3), np.random.default_rng(7), replace, np.int64(4))
    np.testing.assert_array_equal(actual, expected)


@pytest.mark.parametrize("mode", MODES)
def test_repetition_minimums(mode):
    with pytest.raises(ValueError, match="repetitions must be an integer >= 2"):
        monte_carlo([2], 10, 3, 1, 7, mode)
    actual = draw_rank_from_catalogue(
        2, 10, 3, np.random.default_rng(7), mode == "with_replacement", 1)
    assert actual.shape == (1,)
