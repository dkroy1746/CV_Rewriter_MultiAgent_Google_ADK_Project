"""Output formatting module for different file formats."""
from datetime import datetime


def format_output(content: str, format_type: str = "plain") -> str:
    """
    Format the CV output in the specified format.

    Args:
        content: The reformatted CV text
        format_type: Output format (plain, markdown, or html)

    Returns:
        Formatted content string
    """
    if format_type == "markdown":
        return format_as_markdown(content)
    elif format_type == "html":
        return format_as_html(content)
    else:  # plain
        return content


def format_as_markdown(content: str) -> str:
    """
    Format CV content as Markdown.

    Args:
        content: The CV text

    Returns:
        Markdown-formatted CV
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    markdown = f"""# Reformatted CV

*Generated on: {timestamp}*
*Optimized for ATS by CV Formatter*

---

{content}

---

*This CV was optimized using multi-agent AI analysis to maximize compatibility with Applicant Tracking Systems (ATS).*
"""
    return markdown


def format_as_html(content: str) -> str:
    """
    Format CV content as HTML.

    Args:
        content: The CV text

    Returns:
        HTML-formatted CV
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Convert plain text to HTML with basic formatting
    # Preserve line breaks and paragraphs
    paragraphs = content.split('\n\n')
    html_paragraphs = []

    for para in paragraphs:
        if para.strip():
            # Check if it looks like a heading (short line, possibly all caps or title case)
            lines = para.split('\n')
            if len(lines) == 1 and len(para) < 100:
                # Likely a heading
                html_paragraphs.append(f'<h2>{para.strip()}</h2>')
            else:
                # Regular paragraph - preserve line breaks
                formatted = para.replace('\n', '<br>\n')
                html_paragraphs.append(f'<p>{formatted}</p>')

    content_html = '\n'.join(html_paragraphs)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reformatted CV - ATS Optimized</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 40px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            border-bottom: 3px solid #2c3e50;
            margin-bottom: 30px;
            padding-bottom: 20px;
        }}
        h1 {{
            color: #2c3e50;
            margin: 0;
            font-size: 2.5em;
        }}
        .meta {{
            color: #7f8c8d;
            font-size: 0.9em;
            margin-top: 10px;
        }}
        h2 {{
            color: #34495e;
            border-bottom: 2px solid #3498db;
            padding-bottom: 5px;
            margin-top: 30px;
            margin-bottom: 15px;
        }}
        p {{
            margin: 15px 0;
            color: #2c3e50;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ecf0f1;
            text-align: center;
            color: #7f8c8d;
            font-size: 0.85em;
        }}
        @media print {{
            body {{
                background-color: white;
                margin: 0;
                padding: 0;
            }}
            .container {{
                box-shadow: none;
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Reformatted CV</h1>
            <div class="meta">
                Generated on: {timestamp}<br>
                Optimized for ATS by CV Formatter
            </div>
        </div>

        <div class="content">
{content_html}
        </div>

        <div class="footer">
            This CV was optimized using multi-agent AI analysis to maximize compatibility with Applicant Tracking Systems (ATS).
        </div>
    </div>
</body>
</html>
"""
    return html
