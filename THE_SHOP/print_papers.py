#!/usr/bin/env python3
"""
AIIT-THRESI Paper Printer
Converts markdown files to paginated PDFs with headers, footers, and page numbers.
Then sends to printer.

Usage:
  python3 print_papers.py file1.md file2.md ...
  python3 print_papers.py --all          # Print all papers in order
  python3 print_papers.py --pdf-only     # Generate PDFs without printing
"""

import sys
import os
import re
import glob
import subprocess
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

PRINTER = "EPSON_ET_2800_Series"
OUTPUT_DIR = os.path.expanduser("~/Desktop/PRINT_READY")
FOOTER_TEXT = "AIIT-THRESI | Rhet Dillard Wike | Council Hill, Oklahoma | 2026"


def header_footer(canvas, doc, title=""):
    """Draw header and footer on every page."""
    canvas.saveState()
    width, height = letter

    # Header: paper title
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(0.75 * inch, height - 0.5 * inch, title[:80])
    canvas.drawRightString(width - 0.75 * inch, height - 0.5 * inch,
                           f"Page {doc.page}")

    # Header line
    canvas.setStrokeColor(colors.black)
    canvas.setLineWidth(0.5)
    canvas.line(0.75 * inch, height - 0.55 * inch,
                width - 0.75 * inch, height - 0.55 * inch)

    # Footer
    canvas.setFont("Helvetica", 7)
    canvas.drawCentredString(width / 2, 0.4 * inch, FOOTER_TEXT)
    canvas.drawRightString(width - 0.75 * inch, 0.4 * inch,
                           f"{doc.page}")

    # Footer line
    canvas.line(0.75 * inch, 0.5 * inch,
                width - 0.75 * inch, 0.5 * inch)

    canvas.restoreState()


def md_to_elements(filepath):
    """Parse markdown into reportlab flowable elements."""
    styles = getSampleStyleSheet()

    # Custom styles
    styles.add(ParagraphStyle(
        'PaperTitle', parent=styles['Title'],
        fontSize=16, spaceAfter=6, alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    ))
    styles.add(ParagraphStyle(
        'PaperSubtitle', parent=styles['Normal'],
        fontSize=11, spaceAfter=4, alignment=TA_CENTER,
        fontName='Helvetica-Oblique', textColor=colors.grey
    ))
    styles.add(ParagraphStyle(
        'H1', parent=styles['Heading1'],
        fontSize=14, spaceBefore=16, spaceAfter=8,
        fontName='Helvetica-Bold'
    ))
    styles.add(ParagraphStyle(
        'H2', parent=styles['Heading2'],
        fontSize=12, spaceBefore=12, spaceAfter=6,
        fontName='Helvetica-Bold'
    ))
    styles.add(ParagraphStyle(
        'H3', parent=styles['Heading3'],
        fontSize=10, spaceBefore=8, spaceAfter=4,
        fontName='Helvetica-Bold'
    ))
    styles.add(ParagraphStyle(
        'CodeBlock', parent=styles['Code'],
        fontSize=7.5, fontName='Courier', leftIndent=20,
        rightIndent=20, spaceBefore=4, spaceAfter=4,
        backColor=colors.Color(0.95, 0.95, 0.95)
    ))
    styles.add(ParagraphStyle(
        'Quote', parent=styles['Normal'],
        fontSize=9, fontName='Helvetica-Oblique',
        leftIndent=30, rightIndent=30, spaceBefore=6, spaceAfter=6,
        textColor=colors.Color(0.3, 0.3, 0.3)
    ))
    styles.add(ParagraphStyle(
        'BodyText2', parent=styles['BodyText'],
        fontSize=9, leading=12, spaceBefore=3, spaceAfter=3
    ))

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace ALL unicode with printable ASCII - nuke every non-ASCII character
    import unicodedata
    cleaned = []
    for ch in content:
        if ord(ch) < 128:
            cleaned.append(ch)
        else:
            # Try to get a good ASCII name
            name = unicodedata.name(ch, '').lower()
            # Map by category
            replacements = {
                'multiplication sign': 'x', 'degree sign': ' deg',
                'plus-minus sign': '+/-', 'middle dot': '.',
                'vulgar fraction one half': '1/2',
                'em dash': '--', 'en dash': '-',
                'rightwards arrow': '->', 'leftwards arrow': '<-',
                'upwards arrow': '^', 'downwards arrow': 'v',
                'almost equal': '~=', 'not equal': '!=',
                'less-than or equal': '<=', 'greater-than or equal': '>=',
                'infinity': 'inf', 'integral': 'integral',
                'partial differential': 'd', 'square root': 'sqrt',
                'proportional': '~', 'element of': 'in',
                'planck constant': 'h-bar',
                'dagger': '+', 'check mark': '[x]',
                'black down-pointing': 'v',
                'long left right double arrow': '<==>',
                'mathematical left angle': '<',
                'mathematical right angle': '>',
            }
            greek = {
                'alpha': 'alpha', 'beta': 'beta', 'gamma': 'gamma',
                'delta': 'delta', 'epsilon': 'epsilon', 'zeta': 'zeta',
                'eta': 'eta', 'theta': 'theta', 'iota': 'iota',
                'kappa': 'kappa', 'lamda': 'lambda', 'mu': 'mu',
                'nu': 'nu', 'xi': 'xi', 'omicron': 'omicron',
                'pi': 'pi', 'rho': 'rho', 'sigma': 'sigma',
                'tau': 'tau', 'upsilon': 'upsilon', 'phi': 'phi',
                'chi': 'chi', 'psi': 'psi', 'omega': 'omega',
            }
            found = False
            # Check specific replacements first
            for key, val in replacements.items():
                if key in name:
                    cleaned.append(val)
                    found = True
                    break
            if not found:
                # Check Greek letters
                for key, val in greek.items():
                    if key in name:
                        if 'capital' in name:
                            cleaned.append(val.upper())
                        else:
                            cleaned.append(val)
                        found = True
                        break
            if not found:
                # Subscript/superscript digits
                if 'subscript' in name:
                    for d in '0123456789':
                        if d in name:
                            cleaned.append('_' + d)
                            found = True
                            break
                    if not found and 'plus' in name:
                        cleaned.append('+')
                        found = True
                    elif not found and 'minus' in name:
                        cleaned.append('-')
                        found = True
                elif 'superscript' in name:
                    for d in '0123456789':
                        if d in name:
                            cleaned.append('^' + d)
                            found = True
                            break
                    if not found and 'plus' in name:
                        cleaned.append('^+')
                        found = True
                    elif not found and 'minus' in name:
                        cleaned.append('^-')
                        found = True
            if not found:
                # Box drawing -> simple ASCII
                if 'box drawing' in name or 'light' in name:
                    if 'horizontal' in name:
                        cleaned.append('-')
                    elif 'vertical' in name:
                        cleaned.append('|')
                    else:
                        cleaned.append('+')
                    found = True
            if not found:
                # Accented latin -> base letter
                if 'latin' in name and 'letter' in name:
                    # grab the base letter from the name
                    parts = name.split()
                    for p in parts:
                        if len(p) == 1 and p.isalpha():
                            cleaned.append(p)
                            found = True
                            break
            if not found:
                # Combining characters -> skip
                if 'combining' in name:
                    found = True
            if not found:
                # Last resort: just use ?
                cleaned.append('?')
    content = ''.join(cleaned)

    elements = []
    in_code_block = False
    code_lines = []
    title = os.path.basename(filepath).replace('.md', '').replace('_', ' ')

    for line in content.split('\n'):
        # Code blocks
        if line.strip().startswith('```'):
            if in_code_block:
                # End code block
                code_text = '<br/>'.join(
                    l.replace('<', '&lt;').replace('>', '&gt;').replace(' ', '&nbsp;')
                    for l in code_lines
                )
                if code_text.strip():
                    elements.append(Paragraph(code_text, styles['CodeBlock']))
                code_lines = []
                in_code_block = False
            else:
                in_code_block = True
            continue

        if in_code_block:
            code_lines.append(line)
            continue

        stripped = line.strip()

        # Empty line
        if not stripped:
            elements.append(Spacer(1, 4))
            continue

        # Escape HTML entities
        safe = stripped.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

        # Bold/italic in markdown
        safe = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', safe)
        safe = re.sub(r'\*(.+?)\*', r'<i>\1</i>', safe)
        safe = re.sub(r'`(.+?)`', r'<font face="Courier" size="8">\1</font>', safe)

        # Headings
        if stripped.startswith('# ') and not stripped.startswith('## '):
            text = safe.lstrip('# ').strip()
            title = text  # capture for header
            elements.append(Paragraph(text, styles['PaperTitle']))
        elif stripped.startswith('## '):
            text = safe.lstrip('# ').strip()
            elements.append(Paragraph(text, styles['H1']))
        elif stripped.startswith('### '):
            text = safe.lstrip('# ').strip()
            elements.append(Paragraph(text, styles['H2']))
        elif stripped.startswith('#### '):
            text = safe.lstrip('# ').strip()
            elements.append(Paragraph(text, styles['H3']))
        # Horizontal rule
        elif stripped.startswith('---') or stripped.startswith('==='):
            elements.append(Spacer(1, 6))
        # Block quote
        elif stripped.startswith('>'):
            text = safe.lstrip('>&gt; ').strip()
            elements.append(Paragraph(text, styles['Quote']))
        # Table row (simple)
        elif '|' in stripped and stripped.startswith('|'):
            # Just render as code-like text for now
            elements.append(Paragraph(safe, styles['CodeBlock']))
        # Bullet point
        elif stripped.startswith('- ') or stripped.startswith('* '):
            text = safe[2:].strip()
            elements.append(Paragraph(f"  \u2022  {text}", styles['BodyText2']))
        # Numbered list
        elif re.match(r'^\d+\.', stripped):
            elements.append(Paragraph(f"  {safe}", styles['BodyText2']))
        # Normal text
        else:
            elements.append(Paragraph(safe, styles['BodyText2']))

    return elements, title


def make_pdf(md_path, output_path=None):
    """Convert a markdown file to a paginated PDF with headers and page numbers."""
    if output_path is None:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        basename = os.path.basename(md_path).replace('.md', '.pdf')
        output_path = os.path.join(OUTPUT_DIR, basename)

    elements, title = md_to_elements(md_path)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    def on_page(canvas, doc):
        header_footer(canvas, doc, title=title)

    doc.build(elements, onFirstPage=on_page, onLaterPages=on_page)
    return output_path


def send_to_printer(pdf_path):
    """Send a PDF to the printer."""
    result = subprocess.run(
        ["lp", "-d", PRINTER, "-o", "media=letter", "-o", "fit-to-page", pdf_path],
        capture_output=True, text=True
    )
    return result.stdout.strip()


def find_all_papers():
    """Find all papers in order on the Desktop."""
    desktop = os.path.expanduser("~/Desktop")
    papers = []

    # Search all subdirectories for PAPER_XX files
    for f in glob.glob(f"{desktop}/**/PAPER_*.md", recursive=True):
        if "BACKUP" in f:
            continue
        basename = os.path.basename(f)
        # Extract paper number
        match = re.match(r'PAPER_(\d+)', basename)
        if match:
            num = int(match.group(1))
            papers.append((num, basename, f))

    # Deduplicate by (number, basename), keeping first found
    seen = set()
    unique = []
    for num, name, path in sorted(papers):
        key = (num, name)
        if key not in seen:
            seen.add(key)
            unique.append((num, name, path))

    return unique


def find_all_proofs():
    """Find all proof files."""
    desktop = os.path.expanduser("~/Desktop")
    proofs = []
    for f in glob.glob(f"{desktop}/**/PROOF_*.md", recursive=True):
        if "BACKUP" in f:
            continue
        proofs.append((os.path.basename(f), f))
    return sorted(set(proofs))


def find_study_files():
    """Find files in the study folder."""
    study = os.path.expanduser("~/Desktop/**STUDY** materials")
    if os.path.isdir(study):
        return [(os.path.basename(f), f) for f in glob.glob(f"{study}/*.md")]
    return []


if __name__ == "__main__":
    args = sys.argv[1:]
    pdf_only = "--pdf-only" in args
    if pdf_only:
        args.remove("--pdf-only")

    if "--all" in args:
        print("=" * 60)
        print("  AIIT-THRESI COMPLETE PRINT RUN")
        print("  Paginated PDFs with headers and page numbers")
        print("=" * 60)
        print()

        # Study folder first
        print("--- STUDY MATERIALS ---")
        for name, path in find_study_files():
            print(f"  Converting: {name}")
            pdf = make_pdf(path)
            print(f"  -> {pdf}")
            if not pdf_only:
                job = send_to_printer(pdf)
                print(f"  Printed: {job}")
        print()

        # All papers in order
        print("--- PAPERS (in order) ---")
        for num, name, path in find_all_papers():
            print(f"  [{num:02d}] Converting: {name}")
            pdf = make_pdf(path)
            print(f"       -> {pdf}")
            if not pdf_only:
                job = send_to_printer(pdf)
                print(f"       Printed: {job}")
        print()

        # All proofs
        print("--- PROOFS ---")
        for name, path in find_all_proofs():
            print(f"  Converting: {name}")
            pdf = make_pdf(path)
            print(f"  -> {pdf}")
            if not pdf_only:
                job = send_to_printer(pdf)
                print(f"  Printed: {job}")
        print()

        print("=" * 60)
        print("  DONE. God is good. All the time.")
        print("=" * 60)

    elif args:
        for filepath in args:
            if filepath.endswith('.md') and os.path.exists(filepath):
                print(f"Converting: {filepath}")
                pdf = make_pdf(filepath)
                print(f"-> {pdf}")
                if not pdf_only:
                    job = send_to_printer(pdf)
                    print(f"Printed: {job}")
            else:
                print(f"Skipping: {filepath}")
    else:
        print("Usage:")
        print("  python3 print_papers.py file1.md file2.md ...")
        print("  python3 print_papers.py --all              # Everything in order")
        print("  python3 print_papers.py --all --pdf-only   # PDFs only, no print")
