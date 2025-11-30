"""Quick test to verify all imports work correctly."""
import sys

print("Testing imports...")

try:
    from cv_formatter import config, CVFormatterOrchestrator
    print("✓ Main module imports")
except Exception as e:
    print(f"✗ Main module import failed: {e}")
    sys.exit(1)

try:
    from cv_formatter.parsers import PDFParser, TextParser
    print("✓ Parser imports")
except Exception as e:
    print(f"✗ Parser import failed: {e}")
    sys.exit(1)

try:
    from cv_formatter.agents import (
        PDFParserAgent,
        TxtParserAgent,
        CVAgent,
        JDAgent,
        CompanyAgent,
        RewriteAgent,
    )
    print("✓ Agent imports")
except Exception as e:
    print(f"✗ Agent import failed: {e}")
    sys.exit(1)

try:
    # Test parser initialization
    pdf_parser = PDFParser()
    text_parser = TextParser()
    print("✓ Parser initialization")
except Exception as e:
    print(f"✗ Parser initialization failed: {e}")
    sys.exit(1)

try:
    # Test agent initialization (without ADK dependencies)
    pdf_agent = PDFParserAgent()
    txt_agent = TxtParserAgent()
    cv_agent = CVAgent()
    jd_agent = JDAgent()
    company_agent = CompanyAgent()
    rewrite_agent = RewriteAgent()
    print("✓ Agent initialization")
except Exception as e:
    print(f"✗ Agent initialization failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✓ All import tests passed!")
print("\nNote: To run the full CV formatter, you need to:")
print("1. Set GOOGLE_API_KEY in .env file")
print("2. Run: pixi run python -m cv_formatter.main <cv.pdf> <jd.txt>")
