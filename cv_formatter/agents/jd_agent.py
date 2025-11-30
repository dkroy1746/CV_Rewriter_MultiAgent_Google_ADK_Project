"""JD Analysis Agent for understanding job requirements."""
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini


class JDAgent:
    """Agent for analyzing Job Description content."""

    def __init__(self):
        """Initialize JD Agent."""
        self.agent = self._create_agent()

    def _create_agent(self) -> LlmAgent:
        """Create and configure the LLM agent."""
        return LlmAgent(
            name="JD_Agent",
            model=Gemini(model="gemini-2.5-flash"),
            instruction="""You are a Job Description Comprehension Agent.

            Using the Job Description (JD) text provided in {JD_text}:
            1. Identify key job requirements and responsibilities
            2. Extract required skills, qualifications, and experience levels
            3. Determine critical keywords and competencies
            4. Understand the semantic context of the role

            The entire JD content is available in {JD_text}.
            Raise an error if {JD_text} is not found or is blank.
            """,
            output_key="JD_context",
        )

    def get_agent(self) -> LlmAgent:
        """Get the underlying LLM agent."""
        return self.agent
