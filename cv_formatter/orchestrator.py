"""Orchestrator for managing the CV reformatting workflow."""
import warnings
import logging
import sys
import io
from pathlib import Path
from typing import Optional
from contextlib import redirect_stderr

from google.adk.agents import SequentialAgent, ParallelAgent, LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.genai import types

from cv_formatter.config import config

# Suppress expected warnings from dependencies
warnings.filterwarnings("ignore", message="pkg_resources is deprecated")
warnings.filterwarnings("ignore", message=".*non-text parts in the response.*")

# Suppress verbose ADK logging
logging.getLogger("google.adk").setLevel(logging.ERROR)

from cv_formatter.agents import (
    PDFParserAgent,
    TxtParserAgent,
    CVAgent,
    JDAgent,
    CompanyAgent,
    RewriteAgent,
)


class _StderrFilter:
    """Filter to suppress specific ADK warnings printed to stderr."""

    def __init__(self, original_stderr):
        self.original_stderr = original_stderr
        self.suppressed_patterns = [
            "App name mismatch detected",
            "non-text parts in the response",
        ]

    def write(self, text):
        # Only write if text doesn't contain suppressed patterns
        if not any(pattern in text for pattern in self.suppressed_patterns):
            self.original_stderr.write(text)

    def flush(self):
        self.original_stderr.flush()

    def fileno(self):
        return self.original_stderr.fileno()


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

        # Create a parallel agent for CV and JD processing
        self.parallel_processing = ParallelAgent(
            name="Parallel_Processing_Agent",
            sub_agents=[
                self.cv_sequential,
                self.jd_sequential,
            ],
        )

        # Create the complete sequential workflow
        # This will automatically execute all agents in order
        self.root_agent = SequentialAgent(
            name="Complete_CV_Formatter_Workflow",
            sub_agents=[
                self.parallel_processing,  # Process CV and JD in parallel
                self.company_agent.get_agent(),  # Research company
                self.rewrite_agent.get_agent(),  # Generate reformatted CV
            ],
        )

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

        # Collect response - the last agent in the sequence (Rewrite_Agent) produces the final CV
        reformatted_cv = ""

        # Temporarily replace stderr to filter ADK warnings
        original_stderr = sys.stderr
        sys.stderr = _StderrFilter(original_stderr)

        try:
            async for event in self.runner.run_async(
                user_id=config.user_id,
                session_id=session.id,
                new_message=query_content,
            ):
                # Collect all final responses, the last one will be from Rewrite_Agent
                if event.is_final_response() and event.content and event.content.parts:
                    # Extract only text parts, filtering out function_call parts
                    text_parts = [part.text for part in event.content.parts if hasattr(part, 'text') and part.text]
                    if text_parts:
                        text = "".join(text_parts)
                        if text != "None":
                            # Keep updating - the last response is from Rewrite_Agent
                            reformatted_cv = text
        finally:
            # Restore original stderr
            sys.stderr = original_stderr

        if not reformatted_cv:
            raise RuntimeError(
                "No reformatted CV was generated. The workflow may not have completed all steps."
            )

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

        # Temporarily replace stderr to filter ADK warnings
        original_stderr = sys.stderr
        sys.stderr = _StderrFilter(original_stderr)

        try:
            # Use runner's debug method
            await self.runner.run_debug(
                user_messages=query,
                user_id=config.user_id,
                session_id=session_id,
            )
        finally:
            # Restore original stderr
            sys.stderr = original_stderr
