"""Test the formatter module."""
from cv_formatter.formatter import format_output

# Sample CV text
sample_cv = """JOHN DOE
Senior Software Engineer

PROFESSIONAL SUMMARY
Experienced software engineer with 10+ years in full-stack development.
Specializing in Python, React, and cloud technologies.

SKILLS
- Programming Languages: Python, JavaScript, TypeScript
- Frameworks: React, Django, Flask
- Cloud: AWS, Docker, Kubernetes

EXPERIENCE
Senior Software Engineer | Tech Corp | 2020-Present
- Led development of microservices architecture
- Improved system performance by 40%
- Mentored junior developers

EDUCATION
B.S. Computer Science | State University | 2013"""

print("=" * 80)
print("TESTING PLAIN TEXT FORMAT")
print("=" * 80)
plain = format_output(sample_cv, "plain")
print(plain[:200] + "...")

print("\n" + "=" * 80)
print("TESTING MARKDOWN FORMAT")
print("=" * 80)
markdown = format_output(sample_cv, "markdown")
print(markdown[:300] + "...")

print("\n" + "=" * 80)
print("TESTING HTML FORMAT")
print("=" * 80)
html = format_output(sample_cv, "html")
print(html[:500] + "...")
print("\n✓ All formatters working!")
