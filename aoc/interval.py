from typing import Iterable, Set, Tuple

__all__ = ["intervals_diff", "intervals_intersect"]

Interval = Tuple[float, float]


def _remove_empty(intervals: Iterable[Interval]) -> Set[Interval]:
    return {(lower, upper) for lower, upper in intervals if lower < upper}


def _interval_diff(i1: Interval, i2: Interval) -> Set[Interval]:
    # If there is no intersection, one must be left of the other.
    if i1[1] <= i2[0] or i2[1] <= i1[0]:
        return _remove_empty({i1})

    if i1[0] <= i2[0] and i2[1] <= i1[1]:
        # `i2` is contained in `i1`.
        return _remove_empty({(i1[0], i2[0]), (i2[1], i1[1])})

    if i2[0] <= i1[0] and i1[1] <= i2[1]:
        # `i1` is contained in `i2`.
        return set()

    # The result now must be the simple intersection. There are two cases to consider.
    if i1[0] <= i2[0]:
        return _remove_empty({(i1[0], i2[0])})
    else:
        return _remove_empty({(i2[1], i1[1])})


def intervals_diff(ints1: Set[Interval], ints2: Set[Interval]) -> Set[Interval]:
    """For two sets of disjoint open-closed intervals on the real line `ints1` and
    `ints2`, compute the set difference `ints1 - ints2`.

    Args:
        ints1 (set[:obj:`.Interval`]): First set of intervals.
        ints2 (set[:obj:`.Interval`]): Second set of intervals.

    Returns:
        set[:obj:`.Interval`]: `ints1 - ints2`.
    """
    return set().union(*(_interval_diff(i1, i2) for i1 in ints1 for i2 in ints2))


def _interval_intersect(i1: Interval, i2: Interval) -> Set[Interval]:
    # If there is no intersection, one must be left of the other.
    if i1[1] <= i2[0] or i2[1] <= i1[0]:
        return set()

    return _remove_empty({(max(i1[0], i2[0]), min(i1[1], i2[1]))})


def intervals_intersect(ints1: Set[Interval], ints2: Set[Interval]) -> Set[Interval]:
    """For two sets of disjoint open-closed intervals on the real line `ints1` and
    `ints2`, compute the intersection `ints1 & ints2`.

    Args:
        ints1 (set[:obj:`.Interval`]): First set of intervals.
        ints2 (set[:obj:`.Interval`]): Second set of intervals.

    Returns:
        set[:obj:`.Interval`]: `ints1 & ints2`.
    """
    return set().union(*(_interval_intersect(i1, i2) for i1 in ints1 for i2 in ints2))
