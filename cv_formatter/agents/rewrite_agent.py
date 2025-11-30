"""CV Rewrite Agent for optimizing CV for ATS."""
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search

from cv_formatter.config import config


class RewriteAgent:
    """Agent for rewriting CVs to match job descriptions."""

    def __init__(self):
        """Initialize Rewrite Agent."""
        self.agent = self._create_agent()

    def _create_agent(self) -> LlmAgent:
        """Create and configure the LLM agent."""
        return LlmAgent(
            name="Rewrite_Agent",
            model=Gemini(model=config.model_name),
            instruction="""You are an intelligent CV Rewriting Agent.

            Your goal is to rewrite/optimize the candidate's CV to maximize the Applicant Tracking System (ATS) score.

            Use ALL of the following information:
            1. **CV Analysis** ({CV_context}): The candidate's skills, profile, and work experience
            2. **JD Analysis** ({JD_context}): The job requirements and key qualifications
            3. **Company Profile** ({Company_context}): The company's vision, culture, and goals

            Instructions:
            - Align the CV content with the job requirements while maintaining truthfulness
            - Incorporate relevant keywords from the JD naturally
            - Highlight experiences and skills that match the role
            - Adjust the tone and emphasis to match company culture
            - Ensure all claims are based on the original CV content
            - Optimize for ATS keyword matching without keyword stuffing

            Format the output as a complete, well-structured CV with clear sections:
            - Use clear section headers (e.g., PROFESSIONAL SUMMARY, SKILLS, EXPERIENCE, EDUCATION)
            - Separate sections with blank lines
            - Use bullet points for lists
            - Keep formatting clean and ATS-friendly (no tables, columns, or complex formatting)
            - Make it ready to be converted to different formats (plain text, markdown, HTML)

            Output the complete reformatted CV text that will maximize ATS score while staying authentic.
            """,
            tools=[google_search],
            output_key="Reformatted_CV",
        )

    def get_agent(self) -> LlmAgent:
        """Get the underlying LLM agent."""
        return self.agent
