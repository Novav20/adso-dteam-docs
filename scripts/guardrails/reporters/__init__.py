"""
Audit output formatters (console, JSON, Markdown) in 100% Technical English.
"""

from __future__ import annotations

from .console import render_console
from .json_reporter import render_json
from .markdown_reporter import render_markdown

__all__ = ["render_console", "render_json", "render_markdown"]
