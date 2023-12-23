import textwrap
from pathlib import Path
from typing import Callable

import pytest


@pytest.fixture()
def write_file(tmp_path: Path) -> Callable[[str, str], str]:
    """Callable[[str, str], str]: A function that takes in a file name and some file
    contents, writes that contents to a temporary file with that name, and which
    returns the full temporary path."""

    def write(name: str, content: str) -> str:
        path = tmp_path / name
        with open(path, "w") as f:
            f.write(textwrap.dedent(content))
        return str(path)

    return write
