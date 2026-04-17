"""
generate_sitemap.py
-------------------
Generates a site map of all documentation pages for use in the Claude desktop
skill `docs-site-context`.

What it does:
  - Scans all .mdx files under pages/ recursively
  - Reads each file's frontmatter (title, description)
  - Detects page status from the title or a "Last update:" line at the bottom
  - Infers page type from the filename prefix
  - Groups results by type and outputs a formatted markdown table

Output:
  - Printed to the terminal
  - Written to .claude/skills/skill-sitemap.md (overwritten each run)

Usage:
  python3 generate_sitemap.py

Run this from the repo root whenever you've made significant local changes and
want to refresh the skill context.
"""

import re
from pathlib import Path

# --- Configuration ---

PAGES_DIR = Path("pages")
OUTPUT_FILE = Path(".claude/skills/skill-sitemap.md")

TYPE_ORDER = ["Overview", "Article", "Conceptual", "Collection", "Reference", "Other"]

PREFIX_TO_TYPE = {
    "index-": "Overview",
    "article-": "Article",
    "extended-mind-": "Conceptual",
    "collection-": "Collection",
    "reference-": "Reference",
}


# --- Parsing ---

def parse_frontmatter(content):
    """Extract title and description from YAML frontmatter."""
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return "", ""
    fm = match.group(1)
    title = ""
    description = ""
    for line in fm.splitlines():
        t = re.match(r'^title:\s*["\']?(.*?)["\']?\s*$', line)
        if t:
            title = t.group(1).strip()
        d = re.match(r'^description:\s*["\']?(.*?)["\']?\s*$', line)
        if d:
            description = d.group(1).strip()
    return title, description


def detect_status(title, content):
    """
    Determine page status. Returns (display_title, status).

    Priority:
    1. Title contains (DRAFT) or (PLACEHOLDER)
    2. Last update: line at the bottom
    3. Unknown
    """
    # Check title for status keywords
    for keyword in ["PLACEHOLDER", "DRAFT"]:
        pattern = rf"\s*\({keyword}\)\s*"
        if re.search(pattern, title, re.IGNORECASE):
            display_title = re.sub(pattern, "", title, flags=re.IGNORECASE).strip()
            return display_title, keyword.capitalize()

    # Check Last update: line
    # Handles: Last update: DRAFT
    #          Last update: YYYY.MM.DD
    #          Last update: YYYY.MM.DD (DRAFT)
    #          Last update: YYYY.MM.DD (PLACEHOLDER)
    #          *Last update: ...*  (italicized variant)
    last_update = re.search(
        r"\*?Last update:\s*(.+?)\*?\s*$",
        content,
        re.MULTILINE | re.IGNORECASE,
    )
    if last_update:
        value = last_update.group(1).strip().rstrip("*").strip()
        if re.search(r"\bPLACEHOLDER\b", value, re.IGNORECASE):
            return title, "Placeholder"
        if re.search(r"\bDRAFT\b", value, re.IGNORECASE):
            return title, "Draft"
        if re.match(r"\d{4}\.\d{2}\.\d{2}", value):
            return title, "Final"

    return title, "Unknown"


def infer_type(filename):
    """Infer page type from filename prefix."""
    for prefix, page_type in PREFIX_TO_TYPE.items():
        if filename.startswith(prefix):
            return page_type
    return "Other"


# --- Main ---

def build_sitemap():
    mdx_files = sorted(PAGES_DIR.glob("**/*.mdx"))

    pages_by_type = {t: [] for t in TYPE_ORDER}

    for path in mdx_files:
        content = path.read_text(encoding="utf-8")
        raw_title, description = parse_frontmatter(content)
        display_title, status = detect_status(raw_title, content)
        page_type = infer_type(path.name)
        pages_by_type[page_type].append({
            "title": display_title or "(no title)",
            "description": description,
            "status": status,
            "file": str(path),
        })

    lines = ["# Docs Site Map\n"]

    for page_type in TYPE_ORDER:
        pages = pages_by_type[page_type]
        if not pages:
            continue
        lines.append(f"## {page_type}\n")
        lines.append("| Title | Description | Status | File |")
        lines.append("|---|---|---|---|")
        for p in pages:
            title = p["title"].replace("|", "\\|")
            desc = p["description"].replace("|", "\\|")
            lines.append(f"| {title} | {desc} | {p['status']} | {p['file']} |")
        lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    output = build_sitemap()
    print(output)
    OUTPUT_FILE.write_text(output, encoding="utf-8")
    print(f"\nWritten to {OUTPUT_FILE}")
