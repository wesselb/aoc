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
    Union,
)

from .graph import shortest_path

__all__ = [
    "print_board",
    "visualise_board",
    "find_in_board",
    "neighbours",
    "turn_right",
    "turn_left",
    "neighbours_boundary",
    "dir_to_char",
    "char_to_dir",
]

Node = Tuple[int, int]
BoardValue = TypeVar("BoardValue")


def print_board(
    board: Dict[Node, str],
    marks: Optional[Dict[str, Iterable[Node]]] = None,
    transpose: bool = False,
) -> None:
    """Print a board.

    Args:
        board (dict[Node, str]): Board to visualise.
        marks (dict[str, Iterable[Node]], optional): Draw markers at particular nodes.
    """
    if transpose:
        board = {(c, r): v for (r, c), v in board.items()}
        if marks:
            marks = {m: [(c, r) for (r, c) in marks] for m, marks in marks.items()}

    min_r = min(r for r, _ in board.keys())
    max_r = max(r for r, _ in board.keys())
    min_c = min(c for _, c in board.keys())
    max_c = max(c for _, c in board.keys())

    if marks:
        # Copy the board before mutation.
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


visualise_board = print_board


def find_in_board(
    board: Dict[Node, BoardValue],
    *values: BoardValue,
) -> Tuple[Node, ...]:
    r"""Find the node of certain board values.

    If a value occurs multiple times, any of the corresponding nodes may be returned.

    Args:
        board (dict[Node, BoardValue]): Board.
        \*values (BoardValue): Values to search for.

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


def turn_right(dr: int, dc: int) -> Tuple[int, int]:
    """On a board, turn right.

    We count positions in the following way::

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
    return (dc, -dr)


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
    return (-dc, dr)


BoundaryPoint = Tuple[Node, Node]


def neighbours_boundary(
    in_region: Optional[Callable[[Node], bool]] = None, walk_thin_corners: bool = False
) -> Callable[[BoundaryPoint], Generator[Tuple[BoundaryPoint, Literal[1]], None, None]]:
    """Construct a function that finds all neighbouring boundary points.

    A boundary point is represented as a two-node tuple, where the first point is
    inside the region and the second point outside. The normal vector for this boundary
    point is the second node minus the first.

    The algorithm to find all neighbouring boundary points works as follows. First,
    the boundary is moved orthogonally to the normal vector. This amounts to an
    _extension_ of the boundary. Second, the algorithm explores all possible _folds_.
    These are generated by fixing either the first or second node, and rotating
    the non-fixed node around the fixed node by 90 degrees in any direction. During
    the rotation, one node must remain inside the region, to ensure that we don't
    leave the boundary. It might happen that, at 45 degrees, both points are inside
    the region. This algorithm should work in any number of dimensions, but is here
    only implemented for grids.

    This function can be given as the argument `nbs` to :func:`aoc.graph.shortest_path`.

    Args:
        in_region (Callable[[Node], bool], optional): A function that checks whether
            a node is in the region of the boundary.
        walk_thin_corners (bool, optional): If set to `True`, then the algorithm
            may leave the region while rotating 90 degrees.

    Returns:
        Callable[[BoundaryPoint], Generator[tuple[BoundaryPoint, One], None, None]]:
            The neighbour function for boundary points. Takes in a boundary point and
            generates tuples of boundary points and weights. The weights are always
            equal to one.
    """

    def _neighbours(
        b: BoundaryPoint,
    ) -> Generator[Tuple[BoundaryPoint, Literal[1]], None, None]:
        if in_region:
            in1, in2 = in_region(b[0]), in_region(b[1])
            if not (in1 ^ in2):
                raise ValueError("Given point is not in the boundary.")

        def in_boundary(b2: BoundaryPoint) -> bool:
            """Check whether `b2` is in the boundary."""
            if not in_region:
                # Just return all possibilities.
                return True
            return in_region(b2[0]) == in1 and in_region(b2[1]) == in2

        (r1, c1), (r2, c2) = b

        # Extend edge in both ways.
        dr, dc = r2 - r1, c2 - c1
        if dc == 0:
            # In the same column, so vector is vertical, meaning that we need to move
            # it left and right.
            assert abs(dr) == 1
            b2 = (r1, c1 - 1), (r2, c2 - 1)
            if in_boundary(b2):
                yield b2, 1
            b2 = (r1, c1 + 1), (r2, c2 + 1)
            if in_boundary(b2):
                yield b2, 1
        else:
            # In the same row, so vector is horizontal, meaning that we need to move
            # it up and down.
            assert abs(dc) == 1
            b2 = (r1 - 1, c1), (r2 - 1, c2)
            if in_boundary(b2):
                yield b2, 1
            b2 = (r1 + 1, c1), (r2 + 1, c2)
            if in_boundary(b2):
                yield b2, 1

        # Attempt to turn around coordinate 1, so coordinate 1 stays.
        dr, dc = r2 - r1, c2 - c1
        for dr2, dc2 in [turn_right(dr, dc), turn_left(dr, dc)]:
            bm = (r1, c1), (r1 + (dr2 + dr), c1 + (dc2 + dc))
            b2 = (r1, c1), (r1 + dr2, c1 + dc2)
            if in_boundary(b2):
                # If this coordinate is not in the region, then the middle point must
                # also be in the boundary. Otherwise, we might leave the boundary and
                # come back. If we are walking thin corners, then this is allowd.
                if in_region and not in1:
                    if walk_thin_corners:
                        yield b2, 1
                    else:
                        if in_boundary(bm):
                            yield b2, 1

                # If the coordinate is in the region, then we do not need to check the
                # middle point. However, if we are walking thin corners, then a similar
                # situation occurs, so then we do need to check.
                elif in_region and in1:
                    if walk_thin_corners:
                        if in_boundary(bm):
                            yield b2, 1
                    else:
                        yield b2, 1

                else:
                    yield b2, 1

        # Attempt to turn around coordinate 2, so coordinate 2 stays.
        dr, dc = r1 - r2, c1 - c2
        for dr2, dc2 in [turn_right(dr, dc), turn_left(dr, dc)]:
            bm = (r2 + (dr2 + dr), c2 + (dc2 + dc)), (r2, c2)
            b2 = (r2 + dr2, c2 + dc2), (r2, c2)
            if in_boundary(b2):
                if in_region and not in2:
                    if walk_thin_corners:
                        yield b2, 1
                    else:
                        if in_boundary(bm):
                            yield b2, 1
                elif in_region and in2:
                    if walk_thin_corners:
                        if in_boundary(bm):
                            yield b2, 1
                    else:
                        yield b2, 1
                else:
                    yield b2, 1

    return _neighbours


def find_boundary(
    region: Union[Set[Node], Dict[Node, str]],
) -> Tuple[frozenset[Node], frozenset[Node]]:
    """Find the inner and outer boundary of a region on a board.

    Args:
        region (set[Node] or dict[Node, str]): Region, which is a collection of nodes
            on a board.

    Returns:
        tuple[set[Node], set[Node]]:
            A tuple containing respectively the inner boundary and outer boundary.
    """
    try:
        r, _ = next(iter(region))
    except StopIteration:
        raise ValueError("Board must have at least one node.")

    # Find one coordinate inside and one coordinate outside.
    c = min(c for _, c in region) - 1
    while (r, c + 1) not in region:
        c += 1
    inside = r, c + 1
    outside = r, c

    # Walk the boundary.
    nbs = neighbours_boundary(lambda n: n in region)
    boundary, _ = shortest_path((inside, outside), nbs)

    # Isolate the inner and outer boundary.
    inner = frozenset(n_in for n_in, _ in boundary)
    outer = frozenset(n_out for _, n_out in boundary)
    return inner, outer


dir_to_char: Dict[Tuple[int, int], str] = {
    (-1, 0): "^",
    (0, 1): ">",
    (1, 0): "v",
    (0, -1): "<",
}

char_to_dir: Dict[str, Tuple[int, int]] = {v: k for k, v in dir_to_char.items()}
