from typing import Iterable, Set, Tuple, TypeVar

__all__ = ["intervals_diff", "intervals_intersect"]


TInterval = TypeVar("TInterval", Tuple[float, float], Tuple[int, int])


def _remove_empty(intervals: Iterable[TInterval], space: int) -> Set[TInterval]:
    return {(lower, upper) for lower, upper in intervals if lower < upper + space}


def _interval_diff(i1: TInterval, i2: TInterval, space: int) -> Set[TInterval]:
    # If there is no intersection, one must be left of the other.
    if i1[1] <= i2[0] - space or i2[1] + space <= i1[0]:
        return _remove_empty({i1}, space)

    if i1[0] <= i2[0] and i2[1] <= i1[1]:
        # `i2` is contained in `i1`.
        return _remove_empty({(i1[0], i2[0] - space), (i2[1] + space, i1[1])}, space)

    if i2[0] <= i1[0] and i1[1] <= i2[1]:
        # `i1` is contained in `i2`.
        return set()

    # The result now must be the simple intersection. There are two cases to consider.
    if i1[0] <= i2[0]:
        return _remove_empty({(i1[0], i2[0] - space)}, space)
    else:
        return _remove_empty({(i2[1] + space, i1[1])}, space)


def _space(closed: bool) -> int:
    if closed:
        return 1
    else:
        return 0


def intervals_diff(
    ints1: Set[TInterval], ints2: Set[TInterval], *, closed: bool = False
) -> Set[TInterval]:
    """For two sets of intervals `ints1` and `ints2`, compute the set difference
    `ints1 - ints2`.

    By default, the intervals are assumed to be half-open intervals on the real line.

    Args:
        ints1 (set[:obj:`.TInterval`]): First set of intervals.
        ints2 (set[:obj:`.TInterval`]): Second set of intervals.
        closed (bool, optional): Instead consider closed intervals on the integers.

    Returns:
        set[:obj:`.TInterval`]: `ints1 - ints2`.
    """
    gen = (_interval_diff(i1, i2, _space(closed)) for i1 in ints1 for i2 in ints2)
    return set().union(*gen)


def _interval_intersect(i1: TInterval, i2: TInterval, space: int) -> Set[TInterval]:
    # If there is no intersection, one must be left of the other.
    if i1[1] <= i2[0] - space or i2[1] + space <= i1[0]:
        return set()

    return _remove_empty({(max(i1[0], i2[0]), min(i1[1], i2[1]))}, space)


def intervals_intersect(
    ints1: Set[TInterval], ints2: Set[TInterval], closed: bool = False
) -> Set[TInterval]:
    """For two sets of disjoint intervals `ints1` and `ints2`, compute the intersection
    `ints1 & ints2`.

    By default, the intervals are assumed to be half-open intervals on the real line.

    Args:
        ints1 (set[:obj:`.TInterval`]): First set of intervals.
        ints2 (set[:obj:`.TInterval`]): Second set of intervals.
        closed (bool, optional): Instead consider closed intervals on the integers.

    Returns:
        set[:obj:`.TInterval`]: `ints1 & ints2`.
    """
    gen = (_interval_intersect(i1, i2, _space(closed)) for i1 in ints1 for i2 in ints2)
    return set().union(*gen)
