"""Text file parsing utilities."""
from pathlib import Path


class TextParser:
    """Plain text file parser."""

    def read_file(self, file_path: str | Path, encoding: str = "utf-8") -> str:
        """
        Read a plain text file with proper cleaning.

        Performs:
        - BOM stripping
        - Line ending normalization
        - Whitespace cleanup

        Args:
            file_path: Path to the text file
            encoding: File encoding (default: utf-8)

        Returns:
            Cleaned text content

        Raises:
            FileNotFoundError: If file doesn't exist
            RuntimeError: If reading fails
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            # Read raw text
            with open(file_path, "r", encoding=encoding, errors="replace") as f:
                text = f.read()

            # Strip Unicode BOM (Byte Order Mark)
            if text.startswith("\ufeff"):
                text = text.lstrip("\ufeff")

            # Normalize line endings to '\n'
            text = text.replace("\r\n", "\n").replace("\r", "\n")

            # Clean trailing whitespace on each line
            text = "\n".join(line.rstrip() for line in text.split("\n"))

            # Remove excessive blank lines at beginning and end
            text = text.strip()

            return text

        except Exception as e:
            raise RuntimeError(f"Failed to read text file: {e}") from e
