from typing import Callable, Generator, Literal, TypeVar

__all__ = ["neighbours", "find_in_board"]

Node = tuple[int, int]
BoardValue = TypeVar("BoardValue")


def neighbours(
    board: dict[Node, BoardValue],
    allowed: set[BoardValue],
    nondiagonal: bool = True,
    diagonal: bool = False,
) -> Callable[[Node], Generator[tuple[Node, Literal[1]], None, None]]:
    """Construct a function that can be given as the argument `nbs` to
    :func:`aoc.graph.shortest_path`.

    Args:
        board (dict[Node, BoardValue]): Board.
        allowed (set[BoardValue]): Board values that we're allowed to go to.
        nondiagonal (bool, optional): Can we make non-diagonal moves? Defaults to
            allowing non-diagonal moves.
        diagonal (bool, optional): Can we make diagonal moves? Defaults to *not*
            allowing diagonal moves.

    Returns:
        Callable[[Node], Generator[tuple[Node, Literal[1]], None, None]]:
            The neighbour function. Takes in a node and generates tuples of neighbours
            and weights of the edges to those neighbours.
    """

    moves = []
    if nondiagonal:
        moves.extend([(1, 0), (-1, 0), (0, 1), (0, -1)])
    if diagonal:
        moves.extend([(1, 1), (-1, 1), (-1, -1), (1, -1)])

    def _neighbours(n: Node) -> Generator[tuple[Node, Literal[1]], None, None]:
        r, c = n
        for dr, dc in moves:
            r2, c2 = r + dr, c + dc
            if (r2, c2) in board and board[r2, c2] in allowed:
                yield (r2, c2), 1

    return _neighbours


def find_in_board(
    board: dict[Node, BoardValue],
    *values: BoardValue,
) -> tuple[Node, ...]:
    """Find the node of certain board values.

    If a value occurs multiple times, any of the corresponding nodes may be returned.

    Args:
        board (dict[Node, BoardValue]): Board.
        \\*values (BoardValue): Values to search for.

    Raises:
        AssertionError: If any of `values` cannot be found.

    Returns:
        tuple[Node, ...]: The nodes corresponding to `values`, in the same order.
    """
    found: dict[int, Node] = {}
    for n, v in board.items():
        if v in values:
            found[values.index(v)] = n
    for i in range(len(values)):
        if i not in found:
            raise AssertionError(f"Could not find `{v}` in board.")
    return tuple(found[i] for i in range(len(values)))
