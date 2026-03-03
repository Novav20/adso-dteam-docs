#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ -x "$SCRIPT_DIR/../../../../.venv/bin/python" ]]; then
  PYTHON_BIN="$SCRIPT_DIR/../../../../.venv/bin/python"
else
  PYTHON_BIN="python3"
fi

echo "[1/8] Generando casos de uso (.tex)"
"$PYTHON_BIN" "$SCRIPT_DIR/scripts/generate_use_cases_tex.py"

echo "[2/8] Generando historias de usuario (.tex)"
"$PYTHON_BIN" "$SCRIPT_DIR/scripts/generate_user_stories_tex.py"

echo "[3/8] Generando apéndices (.tex)"
"$PYTHON_BIN" "$SCRIPT_DIR/scripts/generate_appendix_tex.py"

echo "[4/8] Generando secciones core desde Markdown (.tex)"
"$PYTHON_BIN" "$SCRIPT_DIR/scripts/generate_core_sections_tex.py" --write

echo "[5/8] Compilación LaTeX (pasada 1)"
cd "$SCRIPT_DIR"
pdflatex -interaction=nonstopmode -halt-on-error main_ieee830.tex

echo "[6/8] Compilación LaTeX (pasada 2)"
pdflatex -interaction=nonstopmode -halt-on-error main_ieee830.tex

echo "[7/8] Compilación LaTeX (pasada 3)"
pdflatex -interaction=nonstopmode -halt-on-error main_ieee830.tex

echo "[8/8] Listo: main_ieee830.pdf actualizado"
