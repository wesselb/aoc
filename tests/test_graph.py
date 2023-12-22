import aoc


def test_shortest_path(board_path: str) -> None:
    _, _, board = aoc.read_board(board_path)
    start, end = aoc.find_in_board(board, "S", "E")
    dist, prev = aoc.shortest_path(start, aoc.neighbours(board, allowed={".", "E"}))

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
