"""Diff utilities for before/after resume comparison."""
import difflib
import html
import re
from typing import List, Tuple


def compute_text_diff(before: str, after: str) -> List[Tuple[str, str]]:
    """Return list of (change_type, line) tuples."""
    differ = difflib.ndiff(before.splitlines(), after.splitlines())
    result = []
    for line in differ:
        if line.startswith("- "):
            result.append(("removed", line[2:]))
        elif line.startswith("+ "):
            result.append(("added", line[2:]))
        elif line.startswith("  "):
            result.append(("unchanged", line[2:]))
    return result


def generate_diff_html(before: str, after: str) -> str:
    """Generate side-by-side HTML diff with highlights."""
    before_lines = before.splitlines()
    after_lines = after.splitlines()

    before_html = []
    after_html = []

    matcher = difflib.SequenceMatcher(None, before_lines, after_lines)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            for line in before_lines[i1:i2]:
                before_html.append(f"<div>{html.escape(line)}</div>")
            for line in after_lines[j1:j2]:
                after_html.append(f"<div>{html.escape(line)}</div>")
        elif tag == "delete":
            for line in before_lines[i1:i2]:
                before_html.append(
                    f'<div style="background:#ffcdd2;padding:2px 4px;">{html.escape(line)}</div>'
                )
        elif tag == "insert":
            for line in after_lines[j1:j2]:
                after_html.append(
                    f'<div style="background:#c8e6c9;padding:2px 4px;">{html.escape(line)}</div>'
                )
        elif tag == "replace":
            for line in before_lines[i1:i2]:
                before_html.append(
                    f'<div style="background:#ffcdd2;padding:2px 4px;">{html.escape(line)}</div>'
                )
            for line in after_lines[j1:j2]:
                after_html.append(
                    f'<div style="background:#c8e6c9;padding:2px 4px;">{html.escape(line)}</div>'
                )

    return f"""
    <div class="diff-viewer">
        <div class="before-text">
            <strong>Before</strong>
            {''.join(before_html) or '<em>No content</em>'}
        </div>
        <div class="after-text">
            <strong>After</strong>
            {''.join(after_html) or '<em>No content</em>'}
        </div>
    </div>
    """


def highlight_keywords(text: str, keywords: List[str]) -> str:
    result = html.escape(text)
    for keyword in keywords:
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        result = pattern.sub(
            lambda m: f'<mark style="background:#fff59d;">{html.escape(m.group(0))}</mark>',
            result,
        )
    return result
