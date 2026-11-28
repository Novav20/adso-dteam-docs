#!/usr/bin/env python3
"""
Master repository coherence & cross-seam guardrail verifier entrypoint.

Usage:
    python3 scripts/verify_all.py [--root PATH] [--scope SCOPE] [--rules GRD-01 ...]
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from guardrails.cli import main  # noqa: E402


if __name__ == "__main__":
    sys.exit(main())
