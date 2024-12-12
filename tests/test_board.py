from typing import Callable, Dict, Tuple

import aoc

turn_right: Dict[Tuple[int, int], Tuple[int, int]] = {
    (1, 0): (0, -1),
    (0, -1): (-1, 0),
    (-1, 0): (0, 1),
    (0, 1): (1, 0),
}


def test_turn_right() -> None:
    for dr, dc in turn_right:
        assert aoc.turn_right(dr, dc) == turn_right[dr, dc]


def test_turn_left() -> None:
    turn_left = {v: k for k, v in turn_right.items()}
    for dr, dc in turn_left:
        assert aoc.turn_left(dr, dc) == turn_left[dr, dc]


def test_neighbours_boundary(write_file: Callable[[str, str], str]) -> None:
    _, _, board = aoc.read_board(
        aoc.read_lines(
            write_file(
                "input.txt",
                """
                AAAAAA
                AAABBA
                AAABBA
                ABBAAA
                ABBAAA
                AAAAAA
                """,
            )
        )
    )

    region, _ = aoc.shortest_path((0, 0), aoc.neighbours(board, allowed={"A"}))
    nbs = aoc.neighbours_boundary(lambda n: n in region)

    ins = set()
    outs = set()

    start = ((3, 0), (3, 1))
    prev, current = None, start
    while True:
        ins.add(current[0])
        outs.add(current[1])

        # Stop if we made a loop.
        if prev and current == start:
            break

        # Find the next point in the boundary.
        candidates = {b for b, _ in nbs(current) if b != prev}
        if prev is not None:
            assert len(candidates) == 1
        prev, current = current, aoc.first(candidates)

    for n in ins:
        board[n] = "i"
    for n in outs:
        board[n] = "o"

    _, _, target_board = aoc.read_board(
        aoc.read_lines(
            write_file(
                "output.txt",
                """
                AAAiiA
                AAiooi
                Aiiooi
                iooiiA
                iooiAA
                AiiAAA
                """,
            )
        )
    )

    aoc.print_board(board)

    assert board == target_board
