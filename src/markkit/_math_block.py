"""Define _MathBlock."""

from typing import Literal


class _MathBlock:
    def __init__(self, math_block_type: Literal["dollar", "code-block"]):
        self.contents = []
        self.math_block_type = math_block_type
        self.n_indent_spaces = 0

    def _n_line_top_spaces(self, line: str) -> int:
        """Return the number of spaces at the top of the line.

        Args:
            line: A single line of the markdown file.

        Returns:
            The count of leading space characters.

        Examples:
            >>> Markkit()._n_line_top_spaces("  $$")
            2
            >>> Markkit()._n_line_top_spaces("   $$")
            3
        """
        return len(line) - len(line.lstrip(" "))

    def add_block_begin(self, begin_line: str) -> None:
        self.n_indent_spaces = self._n_line_top_spaces(begin_line)
        match self.math_block_type:
            case "dollar":
                self.contents.append(" " * self.n_indent_spaces + "$$")
            case "code-block":
                self.contents.append(" " * self.n_indent_spaces + "```math")

    def add_block_end(self) -> None:
        match self.math_block_type:
            case "dollar":
                self.contents.append(" " * self.n_indent_spaces + "$$")
            case "code-block":
                self.contents.append(" " * self.n_indent_spaces + "```")

    def add_block_content(self, line: str) -> None:
        self.contents.append(line.rstrip())

    def dump(self) -> str:
        return "\n".join(self.contents)
