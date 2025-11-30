"""PDF parsing utilities using Apache Tika."""
import logging
import re
from pathlib import Path
from tika import parser


class PDFParser:
    """PDF parser using Apache Tika."""

    def __init__(self):
        """Initialize PDF parser with logging configuration."""
        # Silence Tika logs
        logging.getLogger('tika').setLevel(logging.ERROR)
        logging.getLogger('tika.tika').setLevel(logging.ERROR)

    def extract_text(self, pdf_path: str | Path) -> str:
        """
        Extract clean text from a PDF using Apache Tika.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Cleaned and normalized text content

        Raises:
            FileNotFoundError: If PDF file doesn't exist
            RuntimeError: If extraction fails
        """
        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        try:
            # Extract raw text
            parsed = parser.from_file(str(pdf_path))
            raw = parsed.get("content", "")

            if raw is None:
                return ""

            # Remove leading whitespace/newlines
            text = re.sub(r"^\s+", "", raw)

            # Normalize trailing spaces on each line
            text = "\n".join(line.rstrip() for line in text.splitlines())

            return text

        except Exception as e:
            raise RuntimeError(f"Failed to extract text from PDF: {e}") from e
