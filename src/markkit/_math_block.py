"""Build the lines of a single math block."""

from typing import Literal


class _MathBlock:
    """Collect a math block's lines in one output style."""

    def __init__(
        self, math_block_type: Literal["dollar", "code-block", "mdbook"]
    ):
        """Start an empty block of the given style.

        Args:
            math_block_type: Output style, ``dollar``, ``code-block`` or
                ``mdbook``.
        """
        self.contents = []
        self.math_block_type = math_block_type
        self.n_indent_spaces = 0

    def _n_line_top_spaces(self, line: str) -> int:
        """Count the leading spaces of the line.

        Args:
            line: A single line.

        Returns:
            The number of leading spaces.

        Examples:
            >>> _MathBlock("dollar")._n_line_top_spaces("  $$")
            2
            >>> _MathBlock("dollar")._n_line_top_spaces("   $$")
            3
        """
        return len(line) - len(line.lstrip(" "))

    def add_block_begin(self, begin_line: str) -> None:
        """Add the opening marker, keeping the line's indent.

        Args:
            begin_line: The line that opens the block.
        """
        self.n_indent_spaces = self._n_line_top_spaces(begin_line)
        match self.math_block_type:
            case "dollar":
                self.contents.append(" " * self.n_indent_spaces + "$$")
            case "code-block":
                self.contents.append(" " * self.n_indent_spaces + "```math")
            case "mdbook":
                self.contents.append(" " * self.n_indent_spaces + "\\\\[")

    def add_block_end(self) -> None:
        """Add the closing marker with the same indent."""
        match self.math_block_type:
            case "dollar":
                self.contents.append(" " * self.n_indent_spaces + "$$")
            case "code-block":
                self.contents.append(" " * self.n_indent_spaces + "```")
            case "mdbook":
                self.contents.append(" " * self.n_indent_spaces + "\\\\]")

    def add_block_content(self, line: str) -> None:
        """Add one content line, dropping trailing spaces.

        Args:
            line: A line inside the block.
        """
        self.contents.append(line.rstrip())

    def dump(self) -> str:
        """Return the block as a single newline-joined string."""
        return "\n".join(self.contents)
