from typing import Callable

import aoc


def test_shortest_path(write_file: Callable[[str, str], str]) -> None:
    _, _, board = aoc.read_board(
        aoc.read_lines(
            write_file(
                "input.txt",
                """
                S.....
                .##..#
                .#....
                .#.###
                .#...E
                """,
            )
        )
    )
    start, end = aoc.find_in_board(board, "S", "E")
    nbs = aoc.neighbours(board, allowed={".", "S", "E"})
    dist, prev = aoc.shortest_path(start, nbs)

    # Check distance.
    assert dist[end] == 11

    # Check whole path.
    path: list[tuple[int, int]] = []
    n = end
    while n != start:
        path.insert(0, n)
        n = prev[n]
    assert path == [
        (0, 1),
        (0, 2),
        (0, 3),
        (1, 3),
        (2, 3),
        (2, 2),
        (3, 2),
        (4, 2),
        (4, 3),
        (4, 4),
        (4, 5),
    ]


def test_reduce_edges(write_file: Callable[[str, str], str]) -> None:
    _, _, board = aoc.read_board(
        aoc.read_lines(
            write_file(
                "input.txt",
                """
                S.....
                .##..#
                .#....
                .#.###
                .#...E
                """,
            )
        )
    )
    start, end = aoc.find_in_board(board, "S", "E")
    nbs = aoc.neighbours(board, allowed={".", "S", "E"})
    nodes = {n for n, v in board.items() if v in {".", "S", "E"}}
    _, nbs, aoc.reduce_edges(nodes, {start, end}, nbs)
    dist, prev = aoc.shortest_path(start, nbs)

    # Check distance.
    assert dist[end] == 11
