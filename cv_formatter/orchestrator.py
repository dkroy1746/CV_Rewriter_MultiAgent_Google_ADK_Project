"""Orchestrator for managing the CV reformatting workflow."""
from pathlib import Path
from typing import Optional

from google.adk.agents import SequentialAgent, LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.genai import types

from cv_formatter.config import config
from cv_formatter.agents import (
    PDFParserAgent,
    TxtParserAgent,
    CVAgent,
    JDAgent,
    CompanyAgent,
    RewriteAgent,
)


class CVFormatterOrchestrator:
    """Orchestrates the multi-agent CV reformatting workflow."""

    def __init__(self):
        """Initialize the orchestrator with all agents."""
        # Initialize all agent instances
        self.pdf_parser = PDFParserAgent()
        self.txt_parser = TxtParserAgent()
        self.cv_agent = CVAgent()
        self.jd_agent = JDAgent()
        self.company_agent = CompanyAgent()
        self.rewrite_agent = RewriteAgent()

        # Create sequential workflows
        self.cv_sequential = SequentialAgent(
            name="CV_Sequential_Agent",
            sub_agents=[
                self.pdf_parser.get_agent(),
                self.cv_agent.get_agent(),
            ],
        )

        self.jd_sequential = SequentialAgent(
            name="JD_Sequential_Agent",
            sub_agents=[
                self.txt_parser.get_agent(),
                self.jd_agent.get_agent(),
            ],
        )

        # Create root orchestrator agent
        self.root_agent = self._create_root_agent()

        # Create services
        self.session_service = InMemorySessionService()
        self.memory_service = InMemoryMemoryService()

        # Create runner
        self.runner = Runner(
            agent=self.root_agent,
            app_name=config.app_name,
            session_service=self.session_service,
            memory_service=self.memory_service,
        )

    def _create_root_agent(self) -> LlmAgent:
        """Create the root orchestrator agent."""
        return LlmAgent(
            name="ROOT_Agent",
            model=Gemini(model=config.model_name),
            instruction="""You are the root orchestrator agent for CV reformatting.

            Follow these steps sequentially:

            1. Extract the CV PDF path and JD text file path from the user input.

            2. Call CV_Sequential_Agent with the PDF path to:
               - Parse the PDF and extract CV text
               - Analyze the CV content

            3. Call JD_Sequential_Agent with the text file path to:
               - Parse the JD text file
               - Analyze the JD requirements

            4. Extract the company name from the JD analysis.

            5. Call Company_Agent with the company name to research the company.

            6. Call Rewrite_Agent to generate the optimized CV using:
               - CV analysis
               - JD requirements
               - Company information

            7. Return the reformatted CV to the user.
            """,
            sub_agents=[
                self.cv_sequential,
                self.jd_sequential,
                self.company_agent.get_agent(),
                self.rewrite_agent.get_agent(),
            ],
        )

    async def format_cv(
        self,
        cv_path: str | Path,
        jd_path: str | Path,
        session_id: str = "default",
    ) -> str:
        """
        Format a CV based on a job description.

        Args:
            cv_path: Path to the CV PDF file
            jd_path: Path to the JD text file
            session_id: Session identifier

        Returns:
            Reformatted CV text
        """
        cv_path = Path(cv_path)
        jd_path = Path(jd_path)

        # Validate paths
        if not cv_path.exists():
            raise FileNotFoundError(f"CV file not found: {cv_path}")
        if not jd_path.exists():
            raise FileNotFoundError(f"JD file not found: {jd_path}")

        # Create query
        query = f"CV at {cv_path.absolute()} ; JD at {jd_path.absolute()}"

        # Create or get session
        try:
            session = await self.session_service.create_session(
                app_name=config.app_name,
                user_id=config.user_id,
                session_id=session_id,
            )
        except:
            session = await self.session_service.get_session(
                app_name=config.app_name,
                user_id=config.user_id,
                session_id=session_id,
            )

        # Prepare query content
        query_content = types.Content(
            role="user", parts=[types.Part(text=query)]
        )

        # Collect response
        reformatted_cv = ""
        async for event in self.runner.run_async(
            user_id=config.user_id,
            session_id=session.id,
            new_message=query_content,
        ):
            if event.is_final_response() and event.content and event.content.parts:
                text = event.content.parts[0].text
                if text and text != "None":
                    reformatted_cv = text

        return reformatted_cv

    async def format_cv_debug(
        self,
        cv_path: str | Path,
        jd_path: str | Path,
        session_id: str = "default",
    ) -> None:
        """
        Format a CV with debug output.

        Args:
            cv_path: Path to the CV PDF file
            jd_path: Path to the JD text file
            session_id: Session identifier
        """
        cv_path = Path(cv_path)
        jd_path = Path(jd_path)

        # Validate paths
        if not cv_path.exists():
            raise FileNotFoundError(f"CV file not found: {cv_path}")
        if not jd_path.exists():
            raise FileNotFoundError(f"JD file not found: {jd_path}")

        # Create query
        query = f"CV at {cv_path.absolute()} ; JD at {jd_path.absolute()}"

        print(f"\n{'='*80}")
        print(f"CV Formatter - Debug Mode")
        print(f"{'='*80}")
        print(f"CV Path: {cv_path.absolute()}")
        print(f"JD Path: {jd_path.absolute()}")
        print(f"{'='*80}\n")

        # Use runner's debug method
        await self.runner.run_debug(
            user_messages=query,
            user_id=config.user_id,
            session_id=session_id,
        )
