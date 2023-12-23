from typing import (
    Callable,
    Dict,
    Generator,
    Iterable,
    Literal,
    Optional,
    Set,
    Tuple,
    TypeVar,
)

__all__ = ["neighbours", "find_in_board", "turn_right", "visualise_board"]

Node = Tuple[int, int]
BoardValue = TypeVar("BoardValue")


def neighbours(
    board: Optional[Dict[Node, BoardValue]] = None,
    allowed: Optional[Set[BoardValue]] = None,
    nondiagonal: bool = True,
    diagonal: bool = False,
) -> Callable[[Node], Generator[Tuple[Node, Literal[1]], None, None]]:
    """Construct a function that can be given as the argument `nbs` to
    :func:`aoc.graph.shortest_path`.

    Args:
        board (dict[Node, BoardValue], optional): Board.
        allowed (set[BoardValue], optional): Board values that we're allowed to go to.
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

    def _neighbours(n: Node) -> Generator[Tuple[Node, Literal[1]], None, None]:
        r, c = n
        for dr, dc in moves:
            r2, c2 = r + dr, c + dc
            if board and (r2, c2) not in board:
                continue
            if board and allowed and board[r2, c2] not in allowed:
                continue
            yield (r2, c2), 1

    return _neighbours


def find_in_board(
    board: Dict[Node, BoardValue],
    *values: BoardValue,
) -> Tuple[Node, ...]:
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
    found: Dict[int, Node] = {}
    for n, v in board.items():
        if v in values:
            found[values.index(v)] = n
    for i in range(len(values)):
        if i not in found:
            raise AssertionError(f"Could not find `{v}` in board.")
    return tuple(found[i] for i in range(len(values)))


_turn_right: Dict[Tuple[int, int], Tuple[int, int]] = {
    (1, 0): (0, -1),
    (0, -1): (-1, 0),
    (-1, 0): (0, 1),
    (0, 1): (1, 0),
}


def turn_right(dr: int, dc: int) -> Tuple[int, int]:
    """On a board, turn right. We count positions in the following way:

          0123
        0 ....
        1 ....
        2 ....
        3 ....

    Args:
        dr (int): Delta in the row direction.
        dc (int): Delta in the column direction.

    Returns:
        tuple[int, int]:
            * Delta in the row direction after turning right.
            * Delta in the column direction after turning right.
    """
    return _turn_right[dr, dc]


def turn_left(dr: int, dc: int) -> Tuple[int, int]:
    """On a board, turn right. We count positions like we do for :func:`turn_right`.

    Args:
        dr (int): Delta in the row direction.
        dc (int): Delta in the column direction.

    Returns:
        tuple[int, int]:
            * Delta in the row direction after turning left.
            * Delta in the column direction after turning left.
    """
    return _turn_right[-dr, -dc]


def visualise_board(
    board: Dict[Node, str],
    marks: Optional[Dict[str, Iterable[Node]]] = None,
) -> None:
    """Visualise a board.

    Args:
        board (dict[Node, str]): Board to visualise.
        marks (dict[str, Iterable[Node]], optional): Draw markers at particular nodes.
    """
    min_r = min(r for r, _ in board.keys())
    max_r = max(r for r, _ in board.keys())
    min_c = min(c for _, c in board.keys())
    max_c = max(c for _, c in board.keys())

    # Copy the board before mutation.
    if marks:
        board = dict(board)
        for m, nodes in marks.items():
            for n in nodes:
                board[n] = m

    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if (r, c) in board:
                print(board[r, c], end="")
            else:
                print(" ", end="")
        print()
