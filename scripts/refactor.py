import re

with open('scripts/generate_terminal_case_study.py', 'r') as f:
    code = f.read()

# 1. Update Layers
code = code.replace('"L-CIVIL"', '"L-CIVL-BOTM"')
code = code.replace('"dt-layer-civil"', '"dt-layer-civil-botm"')
code = code.replace('"L-STRUCT"', '"L-STRUCT-TMP"') # Will merge into MECH or CIVL
code = code.replace('"dt-layer-struct"', '"dt-layer-struct-tmp"')
code = code.replace('"L-MECH"', '"L-MECH-EQPM"')
code = code.replace('"dt-layer-mech"', '"dt-layer-mech-eqpm"')
code = code.replace('"L-PIPE"', '"L-PIPE-PROC"')
code = code.replace('"dt-layer-pipe"', '"dt-layer-pipe-proc"')
code = code.replace('"L-FIRE"', '"L-FIRE-PROT"')
code = code.replace('"dt-layer-fire"', '"dt-layer-fire-prot"')
code = code.replace('"L-ANNO"', '"L-ANNO-TEXT"')
code = code.replace('"dt-layer-anno"', '"dt-layer-anno-text"')

# Add new layers in the list
code = code.replace('CIV, STR, MEC, PIP, FIR, ANN = [], [], [], [], [], []', 'CIV, MEC, PIP, INS, FIR, HAZ, ANN = [], [], [], [], [], [], []')
code = code.replace('layer("L-STRUCT-TMP", "dt-layer-struct-tmp", STR),', '') # Removing STR layer output entirely, appending to CIV later
code = code.replace('layer("L-MECH-EQPM", "dt-layer-mech-eqpm", MEC)', 'layer("L-MECH-EQPM", "dt-layer-mech-eqpm", MEC), layer("L-INSP-INST", "dt-layer-insp-inst", INS)')
code = code.replace('layer("L-FIRE-PROT", "dt-layer-fire-prot", FIR)', 'layer("L-FIRE-PROT", "dt-layer-fire-prot", FIR), layer("L-ELEC-HAZ", "dt-layer-elec-haz", HAZ)')

code = code.replace('STR.append(', 'CIV.append(') # Move struct to civil bottom

# Fix assert
code = code.replace('["L-CIVL-BOTM", "L-STRUCT-TMP", "L-MECH-EQPM", "L-PIPE-PROC", "L-FIRE-PROT", "L-ANNO-TEXT"]', '["L-CIVL-BOTM", "L-MECH-EQPM", "L-PIPE-PROC", "L-INSP-INST", "L-FIRE-PROT", "L-ELEC-HAZ", "L-ANNO-TEXT"]')

# 2. Update Root SVG
old_svg_header = 'svg_header = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" class="dt-canvas zoom-l1"\n  data-doc-id="PLOT-IRREGULAR-01" data-scale-meters-per-unit="{M_PER_UNIT}">"""'
new_svg_header = 'svg_header = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" class="dt-canvas zoom-l1"\n  data-moc-id="MOC-2026-0042" data-rev-number="2.0" data-checksum-sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"\n  data-scale-ratio="{M_PER_UNIT}" data-units="meters">"""'
code = code.replace(old_svg_header, new_svg_header)

# 3. Update Tanks (MEC.append(...) inside tank generation)
# Look for data-cmp-id="CMP-EQP-TANK" data-tag="{tid}"
old_tank_bind = 'data-cmp-id="CMP-EQP-TANK" data-tag="{tid}"'
new_tank_bind = 'data-cmp-id="CMP-EQP-TANK" data-func-loc="TFA-CSS-{tid}" data-equip-id="EQ-{tid}-A" data-status="E" data-shell-diam-m="{M(r*2)}" data-tank-height-m="14.0" data-design-std="API-650"'
code = code.replace(old_tank_bind, new_tank_bind)

# 4. Update Dikes
# Dikes are drawn in draw_dikes() 
code = code.replace('class="bund-wall"', 'class="bund-wall" data-dike-vol-m3="14500.0" data-dike-height-m="1.80" data-submerged-vol-m3="1200.0"')

# 5. Calibration Vector
old_anno_end = 'ANN.append(f\'</g>\')'
new_anno_end = 'ANN.append(f\'<line id="CALIBRATION-VECTOR" x1="100" y1="1400" x2="600" y2="1400" stroke="{STEEL}" stroke-width="2" data-real-meters="100.0" />\\n</g>\')'
code = code.replace(old_anno_end, new_anno_end)

with open('scripts/generate_terminal_case_study.py', 'w') as f:
    f.write(code)

print("Refactor complete")
