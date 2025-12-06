import re
from typing import Dict, List, Tuple

__all__ = [
    "read_lines",
    "read_board",
    "parse_board",
    "parse_nums",
]


def read_lines(file_name: str, *, strip: bool = True) -> List[str]:
    """Read all lines form a file, properly dealing with newline characters and
    possible additional whitespace.

    Args:
        file_name (str): File name.
        strip (bool): Strip whitespace at the beginning and end of the line and at the
            beginning and end of every line.

    Returns:
        list[str]: All lines in `file_name` without newline characters and possibly
            also without whitespace.
    """
    with open(file_name, "r") as f:
        content = f.read()

    if strip:
        content = content.strip()

    lines = [line.replace("\n", "") for line in content.splitlines()]

    if strip:
        lines = [line.strip() for line in lines]

    return lines


def parse_board(lines: List[str]) -> Tuple[int, int, Dict[Tuple[int, int], str]]:
    """Parse a board.

    Args:
        lines (list[str]): Lines to parse the board from.

    Returns:
        tuple[int, int, dict[tuple[int, int], str]]:
            * Number of rows.
            * Number of columns.
            * The board. A dictionary mapping the position to the value of the board.
    """
    num_rows = len(lines)
    num_cols = len(lines[0])
    return (
        num_rows,
        num_cols,
        {(r, c): lines[r][c] for r in range(num_rows) for c in range(num_cols)},
    )


read_board = parse_board


def parse_nums(lines: List[str]) -> List[List[List[int]]]:
    """Parse sequences of numbers from lines, creating lists of integers.

    For every newline, group the parsed sequences into a new group.

    Args:
        lines (list[str]): Lines to parse the numbers from.

    Returns:
        list[list[list[int]]]: Groups of integer sequences.
    """
    lines = list(lines)
    blocks: List[List[List[int]]] = [[]]
    while lines:
        line = lines.pop(0)
        if not line:
            blocks.append([])
            continue
        blocks[-1].append([int(x) for x in re.split(r"[^\-0-9]+", line) if x])
    return blocks
