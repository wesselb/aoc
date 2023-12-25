import pytest

from aoc.interval import _interval_diff, _interval_intersect


@pytest.mark.parametrize(
    "i1, i2, res",
    [
        ((1, 10), (5, 10), {(1, 5)}),
        ((1, 10), (1, 5), {(5, 10)}),
        ((1, 10), (3, 7), {(1, 3), (7, 10)}),
        ((1, 10), (-5, 1), {(1, 10)}),
        ((1, 10), (-5, 5), {(5, 10)}),
        ((1, 10), (11, 15), {(1, 10)}),
        ((1, 10), (5, 15), {(1, 5)}),
        ((1, 10), (-5, 15), set()),
    ],
)
def test_interval_diff(i1, i2, res):
    assert _interval_diff(i1, i2) == res


@pytest.mark.parametrize(
    "i1, i2, res",
    [
        ((1, 10), (5, 10), {(5, 10)}),
        ((1, 10), (1, 5), {(1, 5)}),
        ((1, 10), (3, 7), {(3, 7)}),
        ((1, 10), (-5, 1), set()),
        ((1, 10), (-5, 5), {(1, 5)}),
        ((1, 10), (11, 15), set()),
        ((1, 10), (5, 15), {(5, 10)}),
        ((1, 10), (-5, 15), {(1, 10)}),
    ],
)
def test_interval_intersect(i1, i2, res):
    assert _interval_intersect(i1, i2) == res
