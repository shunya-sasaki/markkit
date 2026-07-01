"""Define the Markkit CLI application."""

import re
from pathlib import Path
from typing import Annotated
from typing import Literal

from typer import Argument
from typer import Option
from typer import Typer

from markkit._math_block import _MathBlock


class Markkit:
    """Reformat the math blocks of a markdown file."""

    def __init__(self):
        """Set up the CLI app and block state."""
        self.app = Typer(no_args_is_help=True)
        self.app.command(name="fmt")(self.fmt)
        self._is_in_math_block = False

    def fmt(
        self,
        file_path: Annotated[str, Argument(help="Target file path")],
        math_block_type: Annotated[
            Literal["dollar", "code-block", "mdbook"],
            Option("--math-block-type", "-m", help="Math block type"),
        ] = "dollar",
        write: Annotated[
            bool,
            Option(
                is_flag=True, help="Writes formatted file to a file system"
            ),
        ] = True,
    ):
        """Rewrite each math block in the file to one style.

        Args:
            file_path: Path to the markdown file to format.
            math_block_type: Output style, ``dollar``, ``code-block``
                or ``mdbook``.
            write: Save the result to the file, or print it if False.
        """
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
        r"""Tell whether the line opens a math block.

        Indent is ignored. An opener is ``$$``, the mdBook ``\\\\[``
        marker, or a fence of three or more backticks followed by
        ``math`` (```` ```math ````, ```` ````math ````, ...).

        Args:
            line: A single line.

        Returns:
            True if the line opens a math block.
        """
        if self._is_in_math_block:
            return False
        stripped = line.lstrip()
        return (
            re.match(r"`{3,}math", stripped) is not None
            or stripped.startswith("$$")
            or stripped.startswith("\\\\[")
        )

    def _is_math_block_end(self, line: str) -> bool:
        r"""Tell whether the line closes a math block.

        Indent is ignored. A closer is ``$$``, the mdBook ``\\\\]``
        marker, or a bare fence of three or more backticks
        (```` ``` ````, ```` ```` ````, ...) with no ``math`` marker.

        Args:
            line: A single line.

        Returns:
            True if the line closes a math block.
        """
        if not self._is_in_math_block:
            return False
        stripped = line.strip()
        return (
            re.match(r"`{3,}$", stripped) is not None
            or stripped == "$$"
            or stripped == "\\\\]"
        )
