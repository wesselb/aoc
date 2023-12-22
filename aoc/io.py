__all__ = ["read_lines", "read_board"]


def read_lines(file_name: str) -> list[str]:
    """Read all lines form a file, properly dealing with newline characters and
    possible additional whitespace.

    Args:
        file_name (str): File name.

    Returns:
        list[str]:
            All lines in `file_name` without any empty lines at the beginning,
            empty lines at the end, or newline characters.
    """
    with open(file_name, "r") as f:
        return [line.strip() for line in f.read().strip().splitlines()]


def read_board(file_name: str) -> tuple[int, int, dict[tuple[int, int], str]]:
    """Read a board.

    Args:
        file_name (str): File name.

    Returns:
        tuple[int, int, dict[tuple[int, int], str]]:
            * Number of rows.
            * Number of columns.
            * The board. A dictionary mapping the position to the value of the board.
    """
    lines = read_lines(file_name)
    num_rows = len(lines)
    num_cols = len(lines[0])
    return (
        num_rows,
        num_cols,
        {(r, c): lines[r][c] for r in range(num_rows) for c in range(num_cols)},
    )
