# Reporte IEEE-830 (SRS) — Regenerar PDF

Este documento explica cómo regenerar el PDF final `main_ieee830.pdf` para el reporte "IEEE-830-US-Report".

Requisitos
- `python3` (>=3.8)
- `pdflatex` (TeX Live) — se recomienda `texlive-full` o una instalación que incluya `pdflatex`, `longtable`, `pdfpages`, `xcolor`.
- Permisos de escritura en la carpeta del proyecto.

Pasos (desde la raíz del repo)
```bash
cd adso-gemelo-digital-docs/latex/AP2-Conceptual-Model/Reporte-IEEE-830-US
# Regenerar secciones (scripts generan archivos .tex en ./sections/...)
python3 generate_appendix_tex.py
python3 generate_use_cases_tex.py
python3 generate_user_stories_tex.py

# Compilar el documento (dos pasadas para índices/ referencias)
pdflatex -interaction=nonstopmode -halt-on-error main_ieee830.tex
pdflatex -interaction=nonstopmode -halt-on-error main_ieee830.tex

# Resultado: main_ieee830.pdf en este mismo directorio
ls -l main_ieee830.pdf
```

Notas y solución de problemas
- Si `pdflatex` falla por paquetes faltantes, instale `texlive-full` o los paquetes requeridos (ej.: `texlive-latex-recommended`, `texlive-latex-extra`).
- Los generadores Python escriben archivos .tex en `sections/use_cases`, `sections/user_stories` y `sections/appendices`. Revise esos subdirectorios si falta contenido.
- Si los scripts usan rutas relativas a otra carpeta, ejecútelos desde este directorio para garantizar que las rutas relativas funcionen correctamente.
- El archivo de log de compilación es `main_ieee830.log` (contiene errores y advertencias de LaTeX).

Contacto
- Si necesitas que adapte las rutas o añada plantillas (PlantUML / PlantText / .puml), dímelo y lo preparo.
