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

            Using the COMPLETE Curriculum Vitae (CV) text provided in {CV_text}:

            Perform a COMPREHENSIVE analysis covering ALL sections and details:
            1. Candidate's complete profile, name, contact information, summary/objective
            2. ALL technical and soft skills mentioned
            3. COMPLETE work experience (all positions, responsibilities, achievements)
            4. Full educational background (all degrees, institutions, dates)
            5. Publications, research, papers (if any - list ALL)
            6. Certifications, licenses, awards (if any)
            7. Key keywords and competencies throughout
            8. Semantic context of their professional background
            9. Strengths and expertise areas

            IMPORTANT: Your analysis should capture EVERYTHING from the CV.
            Do not summarize or omit details - the Rewrite_Agent needs complete information.
            Reference the full original CV text in {CV_text}.

            Raise an error if {CV_text} is not found or is blank.
            """,
            output_key="CV_context",
        )

    def get_agent(self) -> LlmAgent:
        """Get the underlying LLM agent."""
        return self.agent
