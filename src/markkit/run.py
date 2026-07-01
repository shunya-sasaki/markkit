"""Entry point of Markkit."""

from markkit.markkit import Markkit


def run():
    """Start the markkit CLI."""
    markkit = Markkit()
    markkit.app()


if __name__ == "__main__":
    run()
