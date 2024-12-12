from typing import Iterable, TypeVar

__all__ = [
    "first",
    "only",
]

T = TypeVar("T")


def first(xs: Iterable[T]) -> T:
    """Get the first element of an iterable.

    Args:
        xs (Iterable[T]): Iterable.

    Returns:
        T: First element of `xs`.
    """
    return next(iter(xs))


def only(xs: Iterable[T]) -> T:
    """Get the only element of an iterable.

    Args:
        xs (Iterable[T]): Iterable.

    Raises:
        AssertionError: If `xs` contains more than one element.

    Returns:
        T: Only element of `xs`.
    """
    it = iter(xs)
    x = next(it)
    try:
        next(it)
        raise AssertionError("Iterable contains more than one element.")
    except StopIteration:
        pass  # This is what we want!
    return x
