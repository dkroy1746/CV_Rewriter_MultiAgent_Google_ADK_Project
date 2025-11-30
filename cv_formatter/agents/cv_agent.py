"""CV Analysis Agent for understanding candidate profiles."""
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini

from cv_formatter.config import config


class CVAgent:
    """Agent for analyzing CV content."""

    def __init__(self):
        """Initialize CV Agent."""
        self.agent = self._create_agent()

    def _create_agent(self) -> LlmAgent:
        """Create and configure the LLM agent."""
        return LlmAgent(
            name="CV_Agent",
            model=Gemini(model=config.model_name),
            instruction="""You are a CV Comprehension Agent.

            Using the Curriculum Vitae (CV) text provided in {CV_text}:
            1. Analyze the candidate's profile, skills, and experience
            2. Identify key keywords and competencies
            3. Extract the semantic context of their professional background
            4. Summarize their strengths and expertise areas

            The entire CV content is available in {CV_text}.
            Raise an error if {CV_text} is not found or is blank.
            """,
            output_key="CV_context",
        )

    def get_agent(self) -> LlmAgent:
        """Get the underlying LLM agent."""
        return self.agent
