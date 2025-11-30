"""Main CLI entry point for CV Formatter."""
import asyncio
import sys
from pathlib import Path

from cv_formatter import CVFormatterOrchestrator, config


async def main():
    """Main entry point."""
    print("CV Formatter - Multi-Agent CV Optimization System")
    print(f"Using API Key: {'✓ Configured' if config.is_configured else '✗ Missing'}\n")

    if not config.is_configured:
        print("ERROR: GOOGLE_API_KEY not found in .env file")
        print("Please create a .env file with: GOOGLE_API_KEY=your_key_here")
        sys.exit(1)

    # Parse command line arguments
    if len(sys.argv) < 3:
        print("Usage: python -m cv_formatter.main <cv_pdf_path> <jd_txt_path>")
        print("\nExample:")
        print("  python -m cv_formatter.main ./my_cv.pdf ./job_description.txt")
        sys.exit(1)

    cv_path = Path(sys.argv[1])
    jd_path = Path(sys.argv[2])

    # Validate files
    if not cv_path.exists():
        print(f"ERROR: CV file not found: {cv_path}")
        sys.exit(1)

    if not jd_path.exists():
        print(f"ERROR: JD file not found: {jd_path}")
        sys.exit(1)

    # Run orchestrator
    print(f"\nProcessing:")
    print(f"  CV: {cv_path.absolute()}")
    print(f"  JD: {jd_path.absolute()}")
    print("\nStarting multi-agent workflow...\n")

    orchestrator = CVFormatterOrchestrator()

    try:
        # Run in debug mode for visibility
        await orchestrator.format_cv_debug(cv_path, jd_path)

        print("\n" + "="*80)
        print("✓ CV formatting completed successfully!")
        print("="*80 + "\n")

    except Exception as e:
        print(f"\n✗ Error during CV formatting: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
