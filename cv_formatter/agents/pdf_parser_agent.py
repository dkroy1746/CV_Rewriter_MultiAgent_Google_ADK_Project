"""PDF Parser Agent for extracting CV text."""
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import FunctionTool, ToolContext

from cv_formatter.parsers import PDFParser


class PDFParserAgent:
    """Agent for parsing PDF files (CVs)."""

    def __init__(self):
        """Initialize PDF Parser Agent."""
        self.parser = PDFParser()
        self.agent = self._create_agent()

    def _extract_using_tika(self, pdf_path: str, context: ToolContext) -> str:
        """
        Extract text from PDF and store in context.

        Args:
            pdf_path: Path to the PDF file
            context: Tool context for storing state

        Returns:
            Extracted text
        """
        text = self.parser.extract_text(pdf_path)
        # Store in context state so other agents can access it
        context.state["CV_text"] = text
        return text

    def _create_agent(self) -> LlmAgent:
        """Create and configure the LLM agent."""
        pdf_extract = FunctionTool(self._extract_using_tika)

        return LlmAgent(
            model=Gemini(model="gemini-2.0-flash-exp"),
            name="PDF_Parser_Agent",
            instruction="""Your job is to extract text from a PDF file (CV).
            From the input, extract the CV path (e.g., /path/to/cv.pdf).
            Use the pdf_extract tool to extract the text from this PDF.
            The tool will automatically store the extracted text in the context for other agents to use.
            """,
            tools=[pdf_extract],
            output_key="CV_text",
        )

    def get_agent(self) -> LlmAgent:
        """Get the underlying LLM agent."""
        return self.agent
