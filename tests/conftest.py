import textwrap

import pytest


@pytest.fixture()
def board_path(tmp_path) -> str:
    """str: An example board."""
    path = tmp_path / "input.txt"
    with open(path, "w") as f:
        f.write(
            textwrap.dedent(
                """
                S.....
                .##..#
                .#....
                .#.###
                .#...E
                """
            )
        )
    return str(path)
