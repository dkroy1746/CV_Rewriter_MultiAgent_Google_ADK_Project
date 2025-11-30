"""Main CLI entry point for CV Formatter."""
import argparse
import asyncio
import sys
from pathlib import Path

from cv_formatter import CVFormatterOrchestrator, config


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="CV Formatter - Multi-Agent CV Optimization System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Print to terminal
  python -m cv_formatter.main cv.pdf jd.txt

  # Save to file
  python -m cv_formatter.main cv.pdf jd.txt -o output.txt

  # Save as markdown
  python -m cv_formatter.main cv.pdf jd.txt -o output.md -f markdown

  # Save as HTML
  python -m cv_formatter.main cv.pdf jd.txt -o output.html -f html
        """
    )

    parser.add_argument(
        "cv_path",
        type=Path,
        help="Path to the CV PDF file"
    )

    parser.add_argument(
        "jd_path",
        type=Path,
        help="Path to the Job Description text file"
    )

    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=None,
        help="Output file path (if not specified, prints to terminal)"
    )

    parser.add_argument(
        "-f", "--format",
        type=str,
        choices=["plain", "markdown", "html"],
        default="plain",
        help="Output format (default: plain)"
    )

    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress progress messages (only show final output)"
    )

    return parser.parse_args()


async def main():
    """Main entry point."""
    args = parse_arguments()

    if not args.quiet:
        print("CV Formatter - Multi-Agent CV Optimization System")
        print(f"Using API Key: {'✓ Configured' if config.is_configured else '✗ Missing'}")
        print(f"Model: {config.model_name}\n")

    if not config.is_configured:
        print("ERROR: GOOGLE_API_KEY not found in .env file")
        print("Please create a .env file with: GOOGLE_API_KEY=your_key_here")
        sys.exit(1)

    cv_path = args.cv_path
    jd_path = args.jd_path

    # Validate files
    if not cv_path.exists():
        print(f"ERROR: CV file not found: {cv_path}")
        sys.exit(1)

    if not jd_path.exists():
        print(f"ERROR: JD file not found: {jd_path}")
        sys.exit(1)

    # Run orchestrator
    if not args.quiet:
        print(f"\nProcessing:")
        print(f"  CV: {cv_path.absolute()}")
        print(f"  JD: {jd_path.absolute()}")
        print(f"  Output: {args.output if args.output else 'Terminal'}")
        print(f"  Format: {args.format}")
        print("\nStarting multi-agent workflow...\n")

    orchestrator = CVFormatterOrchestrator()

    try:
        # Run with or without debug based on output destination
        if args.output:
            # Run without debug output, collect result
            reformatted_cv = await orchestrator.format_cv(cv_path, jd_path)
        else:
            # Run in debug mode for visibility
            if args.quiet:
                reformatted_cv = await orchestrator.format_cv(cv_path, jd_path)
            else:
                await orchestrator.format_cv_debug(cv_path, jd_path)
                reformatted_cv = None

        # Format the output if we have content
        if reformatted_cv:
            from cv_formatter.formatter import format_output
            formatted_output = format_output(reformatted_cv, args.format)

            # Save to file or print
            if args.output:
                args.output.parent.mkdir(parents=True, exist_ok=True)
                args.output.write_text(formatted_output, encoding="utf-8")
                if not args.quiet:
                    print(f"\n✓ Reformatted CV saved to: {args.output.absolute()}")
            else:
                print("\n" + "="*80)
                print("REFORMATTED CV")
                print("="*80 + "\n")
                print(formatted_output)

        if not args.quiet:
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
