"""markkit."""

import re
from pathlib import Path
from typing import Annotated
from typing import Literal

from typer import Argument
from typer import Option
from typer import Typer

from markkit._math_block import _MathBlock


class Markkit:
    """Markkit."""

    def __init__(self):
        """Initlaizer of Markkit."""
        self.app = Typer()
        self.app.command("fmt")(self.fmt)
        self._is_in_math_block = False

    def fmt(
        self,
        file_path: Annotated[str, Argument(help="Target file path")],
        math_block_type: Annotated[
            Literal["dollar", "code-block"], Option(help="Math block type")
        ] = "dollar",
        write: Annotated[
            bool,
            Option(
                is_flag=True, help="Writes formatted file to a file system"
            ),
        ] = True,
    ):
        """Format a markdown file."""
        target_filepath = Path(file_path)
        if not target_filepath.exists():
            raise FileNotFoundError()
        lines = target_filepath.read_text().splitlines()
        contents = []
        for line in lines:
            if self._is_math_block_begin(line):
                self._is_in_math_block = True
                math_block = _MathBlock(math_block_type=math_block_type)
                math_block.add_block_begin(line)
            elif self._is_math_block_end(line):
                self._is_in_math_block = False
                math_block.add_block_end()
                contents.append(math_block.dump())
                del math_block
            else:
                if self._is_in_math_block:
                    math_block.add_block_content(line)
                else:
                    contents.append(line.rstrip())
        output = "\n".join(contents)
        if write:
            target_filepath.write_text(output)
        else:
            print(output)

    def _is_math_block_begin(self, line: str) -> bool:
        """Return whether the line begins a math block.

        Leading whitespace at the top of the line is ignored so that
        indented code-fence (```` ```math ````, ```` ````math ````, ...)
        or ``$$`` markers are detected. Any fence with three or more
        backticks followed by ``math`` is recognized.

        Args:
            line: A single line of the markdown file.

        Returns:
            True if the line starts a math block, otherwise False.
        """
        if self._is_in_math_block:
            return False
        stripped = line.lstrip()
        return re.match(
            r"`{3,}math", stripped
        ) is not None or stripped.startswith("$$")

    def _is_math_block_end(self, line: str) -> bool:
        """Return whether the line ends a math block.

        Leading whitespace at the top of the line is ignored so that
        indented closing code-fence (```` ``` ````, ```` ```` ````, ...)
        or ``$$`` markers are detected. A closing fence is three or more
        backticks with no trailing ``math`` marker.

        Args:
            line: A single line of the markdown file.

        Returns:
            True if the line ends a math block, otherwise False.
        """
        if not self._is_in_math_block:
            return False
        stripped = line.strip()
        return re.match(r"`{3,}$", stripped) is not None or stripped == "$$"


def run():
    """CLI entry point of markkit."""
    markkit = Markkit()
    markkit.app()


if __name__ == "__main__":
    run()
