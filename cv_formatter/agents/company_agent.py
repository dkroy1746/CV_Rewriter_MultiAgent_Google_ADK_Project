"""Company Research Agent for gathering company information."""
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search


class CompanyAgent:
    """Agent for researching company information."""

    def __init__(self):
        """Initialize Company Agent."""
        self.agent = self._create_agent()

    def _create_agent(self) -> LlmAgent:
        """Create and configure the LLM agent."""
        return LlmAgent(
            name="Company_Agent",
            model=Gemini(model="gemini-2.0-flash-exp"),
            instruction="""You are a Company Research Agent.

            When provided with a company name:
            1. Use the google_search tool to find information about the company
            2. Identify the company's vision, mission, and core values
            3. Understand their core business and industry focus
            4. Research their work culture and organizational goals
            5. Summarize what makes this company unique

            Provide a comprehensive understanding of the company to help tailor the CV.
            """,
            tools=[google_search],
            output_key="Company_context",
        )

    def get_agent(self) -> LlmAgent:
        """Get the underlying LLM agent."""
        return self.agent
