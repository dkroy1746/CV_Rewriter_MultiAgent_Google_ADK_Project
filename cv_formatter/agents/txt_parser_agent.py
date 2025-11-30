"""Text Parser Agent for extracting JD text."""
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import FunctionTool, ToolContext

from cv_formatter.parsers import TextParser


class TxtParserAgent:
    """Agent for parsing text files (Job Descriptions)."""

    def __init__(self):
        """Initialize Text Parser Agent."""
        self.parser = TextParser()
        self.agent = self._create_agent()

    def _read_text_file(
        self, file_path: str, tool_context: ToolContext, encoding: str = "utf-8"
    ) -> str:
        """
        Read text file and store in context.

        Args:
            file_path: Path to the text file
            tool_context: Tool context for storing state
            encoding: File encoding

        Returns:
            Extracted text
        """
        text = self.parser.read_file(file_path, encoding)
        # Store in context state so other agents can access it
        tool_context.state["JD_text"] = text
        return text

    def _create_agent(self) -> LlmAgent:
        """Create and configure the LLM agent."""
        txt_extract = FunctionTool(self._read_text_file)

        return LlmAgent(
            model=Gemini(model="gemini-2.5-flash"),
            name="TxtFile_Parser_Agent",
            instruction="""Your job is to extract text from a .txt file (Job Description).
            From the input, extract the JD path (e.g., /path/to/jd.txt).
            Use the txt_extract tool to extract the text from this file.
            The tool will automatically store the extracted text in the context for other agents to use.
            """,
            tools=[txt_extract],
            output_key="JD_text",
        )

    def get_agent(self) -> LlmAgent:
        """Get the underlying LLM agent."""
        return self.agent
