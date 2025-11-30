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

            Your goal is to create a COMPLETE, FULL-LENGTH reformatted CV that maximizes the Applicant Tracking System (ATS) score.

            You have access to the following context from previous agents:
            1. **CV Analysis** ({CV_context}): The candidate's complete profile, all skills, full work experience, education, publications, etc.
            2. **JD Analysis** ({JD_context}): The job requirements and key qualifications
            3. **Company Profile** ({Company_context}): The company's vision, culture, and goals
            4. **Original CV Text** ({CV_text}): The complete original CV for reference

            CRITICAL INSTRUCTIONS:
            - You MUST include ALL sections from the original CV: Summary, Skills, Experience, Education, Publications, Certifications, etc.
            - DO NOT omit or shorten any section - maintain the full depth and detail of the original CV
            - The reformatted CV should be AS LONG OR LONGER than the original, not shorter
            - Align the content with job requirements while maintaining ALL original information
            - Incorporate relevant keywords from the JD naturally throughout ALL sections
            - Highlight experiences and skills that match the role
            - Adjust the tone and emphasis to match company culture
            - Ensure all claims are based on the original CV content
            - Optimize for ATS keyword matching without keyword stuffing

            Format the output as a complete, well-structured CV with ALL sections:
            - PROFESSIONAL SUMMARY (if in original)
            - SKILLS (complete list)
            - EXPERIENCE (all positions with full details)
            - EDUCATION (complete educational background)
            - PUBLICATIONS (if any - include ALL)
            - CERTIFICATIONS (if any)
            - AWARDS (if any)
            - Any other sections from the original CV

            Formatting requirements:
            - Use clear section headers in CAPS
            - Separate sections with blank lines
            - Use bullet points (- or •) for lists
            - Keep formatting clean and ATS-friendly (no tables, columns, or complex formatting)
            - Make it ready to be converted to different formats (plain text, markdown, HTML)

            Output the COMPLETE reformatted CV text. Include everything from the original CV, optimized for the job.
            DO NOT summarize or truncate - this should be a full, detailed CV.
            """,
            tools=[google_search],
            output_key="Reformatted_CV",
        )

    def get_agent(self) -> LlmAgent:
        """Get the underlying LLM agent."""
        return self.agent
