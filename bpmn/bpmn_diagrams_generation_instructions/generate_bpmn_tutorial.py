import json
import re

def parse_style_string(style_str):
    properties = {}
    parts = style_str.split(';')
    for part in parts:
        if '=' in part:
            key, value = part.split('=', 1)
            properties[key] = value
    return properties

def get_bpmn_type_and_description(properties, value_str):
    shape = properties.get('shape', '')
    description = ''
    bpmn_type = 'Objeto Genérico'
    
    # Helper for common properties
    is_collection = properties.get('isCollection') == '1'
    is_loop_sub = properties.get('isLoopSub') == '1'
    is_loop_standard = properties.get('isLoopStandard') == '1'
    is_loop_multi_parallel = properties.get('isLoopMultiParallel') == '1'
    is_loop_multi_seq = properties.get('isLoopMultiSeq') == '1'
    is_ad_hoc = properties.get('isAdHoc') == '1'
    is_loop_comp = properties.get('isLoopComp') == '1'

    # Data Objects
    if shape == 'mxgraph.bpmn.data2':
        bpmn_type = 'Objeto de Datos'
        transfer_type = properties.get('bpmnTransferType', 'none')
        description = f'Objeto de Datos ({transfer_type.capitalize()})'
        if is_collection:
            description += ' (Colección)'
    elif shape == 'datastore':
        bpmn_type = 'Almacén de Datos'
        description = 'Almacén de Datos'

    # Pools and Lanes
    elif shape == 'swimlane':
        # Check for specific swimlane types
        if 'childLayout=stackLayout' in properties.get('style', '') or 'childLayout=stackLayout' in properties.get('html', ''):
            bpmn_type = 'Pool'
            description = 'Pool (Contenedor de Procesos)'
        else:
            bpmn_type = 'Carril'
            description = 'Carril (Subdivisión de Pool)'
        if value_str:
            description += f': {value_str}'
    elif shape == 'mxgraph.bpmn.swimlane':
        if properties.get('isCollection') == '1':
            bpmn_type = 'Pool (Colapsable)'
            description = 'Pool (Contenedor de Procesos, Colapsable)'
        else:
            bpmn_type = 'Carril (Colapsable)'
            description = 'Carril (Subdivisión de Pool, Colapsable)'
        if value_str:
            description += f': {value_str}'

    # Tasks / Activities
    elif shape == 'mxgraph.bpmn.task2':
        task_marker = properties.get('taskMarker', 'abstract')
        bpmn_shape_type = properties.get('bpmnShapeType', '')
        
        if bpmn_shape_type == 'transaction':
            bpmn_type = 'Actividad de Transacción'
            description = 'Actividad de Transacción'
        elif bpmn_shape_type == 'subprocess':
            bpmn_type = 'Subproceso'
            description = 'Subproceso'
            if is_loop_sub:
                description += ' (Embebido)'
            # Check for attached events
            outline = properties.get('outline', '')
            symbol = properties.get('symbol', '')
            if outline and symbol:
                description += f' con Evento Adjunto ({outline.capitalize()} {symbol.capitalize()})'
        elif bpmn_shape_type == 'call':
            bpmn_type = 'Actividad de Llamada'
            description = 'Actividad de Llamada'
            if is_loop_sub:
                description += ' (Subproceso Global)'
        else: # Standard tasks
            bpmn_type = 'Tarea'
            description = 'Tarea'
            if task_marker == 'service':
                description = 'Tarea de Servicio'
            elif task_marker == 'send':
                description = 'Tarea de Envío'
            elif task_marker == 'receive':
                description = 'Tarea de Recepción'
            elif task_marker == 'user':
                description = 'Tarea de Usuario'
            elif task_marker == 'manual':
                description = 'Tarea Manual'
            elif task_marker == 'businessRule':
                description = 'Tarea de Regla de Negocio'
            elif task_marker == 'script':
                description = 'Tarea de Script'
            elif task_marker == 'abstract':
                description = 'Tarea Abstracta'
            
            if is_loop_standard:
                description += ' (Loop Estándar)'
            if is_loop_multi_parallel:
                description += ' (Multi-Instancia Paralela)'
            if is_loop_multi_seq:
                description += ' (Multi-Instancia Secuencial)'
            if is_ad_hoc:
                description += ' (Ad-Hoc)'
            if is_loop_comp:
                description += ' (Compensación)'

    # Events
    elif shape == 'mxgraph.bpmn.event':
        outline = properties.get('outline', 'standard')
        symbol = properties.get('symbol', 'general')
        
        event_type = ''
        if outline == 'standard':
            event_type = 'Inicio'
        elif outline == 'throwing':
            event_type = 'Intermedio (Lanzamiento)'
        elif outline == 'catching':
            event_type = 'Intermedio (Captura)'
        elif outline == 'end':
            event_type = 'Fin'
        elif outline == 'eventInt':
            event_type = 'Intermedio (Interrupción)'
        elif outline == 'eventNonint':
            event_type = 'Intermedio (No Interrupción)'
        elif outline == 'boundInt':
            event_type = 'Límite (Interrupción)'
        elif outline == 'boundNonint':
            event_type = 'Límite (No Interrupción)'
        
        symbol_name = ''
        if symbol == 'general': symbol_name = 'Genérico'
        elif symbol == 'message': symbol_name = 'Mensaje'
        elif symbol == 'timer': symbol_name = 'Temporizador'
        elif symbol == 'escalation': symbol_name = 'Escalada'
        elif symbol == 'compensation': symbol_name = 'Compensación'
        elif symbol == 'conditional': symbol_name = 'Condicional'
        elif symbol == 'signal': symbol_name = 'Señal'
        elif symbol == 'multiple': symbol_name = 'Múltiple'
        elif symbol == 'parallelMultiple': symbol_name = 'Múltiple Paralelo'
        elif symbol == 'cancel': symbol_name = 'Cancelación'
        elif symbol == 'terminate': symbol_name = 'Terminación'
        elif symbol == 'terminate2': symbol_name = 'Terminación (Error)' # diagrams.net specific
        elif symbol == 'link': symbol_name = 'Enlace'

        bpmn_type = f'Evento {event_type}'
        description = f'Evento {event_type} de {symbol_name}'

    # Gateways
    elif shape == 'mxgraph.bpmn.gateway2':
        gw_type = properties.get('gwType', 'exclusive')
        
        if gw_type == 'exclusive':
            bpmn_type = 'Compuerta Exclusiva'
            description = 'Compuerta Exclusiva (Basada en Datos o Eventos)'
        elif gw_type == 'parallel':
            bpmn_type = 'Compuerta Paralela'
            description = 'Compuerta Paralela (AND)'
        elif gw_type == 'complex':
            bpmn_type = 'Compuerta Compleja'
            description = 'Compuerta Compleja'
        else: # Inclusive gateway is often represented by a circle inside a rhombus, or specific style
            bpmn_type = 'Compuerta Inclusiva'
            description = 'Compuerta Inclusiva (OR)'
        
        # Check for event-based gateways (they also have outline/symbol)
        outline = properties.get('outline', '')
        symbol = properties.get('symbol', '')
        if outline and symbol:
            symbol_name = ''
            if symbol == 'message': symbol_name = 'Mensaje'
            elif symbol == 'timer': symbol_name = 'Temporizador'
            elif symbol == 'conditional': symbol_name = 'Condicional'
            elif symbol == 'signal': symbol_name = 'Señal'
            elif symbol == 'multiple': symbol_name = 'Múltiple'
            elif symbol == 'parallelMultiple': symbol_name = 'Múltiple Paralelo'
            description = f'Compuerta Basada en Eventos ({symbol_name})'
            bpmn_type = 'Compuerta Basada en Eventos'

    # Conversations
    elif shape == 'mxgraph.bpmn.conversation2':
        conv_type = properties.get('bpmnConversationType', 'conv')
        if conv_type == 'conv':
            bpmn_type = 'Conversación'
            description = 'Elemento de Conversación'
        elif conv_type == 'call':
            bpmn_type = 'Llamada de Conversación'
            description = 'Elemento de Llamada de Conversación'
        if is_loop_sub:
            description += ' (Subproceso)'

    # Other shapes
    elif shape == 'text':
        bpmn_type = 'Texto'
        description = 'Elemento de Texto'
    elif shape == 'mxgraph.flowchart.annotation_2':
        bpmn_type = 'Anotación'
        description = 'Anotación (Comentario)'
    elif shape == 'table':
        bpmn_type = 'Tabla (Diagrama Cross-Functional)'
        description = 'Contenedor para Diagramas Cross-Functional'
    elif shape == 'tableRow':
        bpmn_type = 'Fila de Tabla (Actor Cross-Functional)'
        description = 'Representa un Actor o Rol en un Diagrama Cross-Functional'
    elif shape == 'swimlane;swimlaneHead=0;swimlaneBody=0;fontStyle=1;connectable=0;strokeColor=inherit;fillColor=none;startSize=0;collapsible=0;recursiveResize=0;expand=0;fontSize=16;':
        bpmn_type = 'Fase (Diagrama Cross-Functional)'
        description = 'Representa una Fase en un Diagrama Cross-Functional'
    elif 'rounded=1;dashed=1;dashPattern=5 2 1 2;' in properties.get('style', ''):
        bpmn_type = 'Grupo'
        description = 'Grupo de Elementos (Línea Discontinua)'
    elif 'rounded=1;arcSize=10;dashed=1;fillColor=none;gradientColor=none;dashPattern=8 3 1 3;strokeWidth=2;' in properties.get('style', ''):
        bpmn_type = 'Límite de Compensación'
        description = 'Límite de Compensación (Línea Discontinua Gruesa)'
    
    if not description and value_str:
        description = value_str # Fallback to value if no specific description

    return bpmn_type, description

def generate_xml_snippet(style, value):
    # Basic XML structure for a cell
    # We'll use a generic ID and geometry for the snippet
    # The key is to preserve the style and value
    # Use a default size if not specified in style, or extract if possible
    width = 100
    height = 50
    
    # Attempt to extract width and height from style if available
    style_props = parse_style_string(style)
    if 'width' in style_props:
        width = int(float(style_props['width']))
    if 'height' in style_props:
        height = int(float(style_props['height']))

    # For swimlanes/pools, default to larger size
    if 'swimlane' in style:
        width = 400
        height = 150

    xml_snippet = f'''<mxCell id="uniqueId" value="{value}" style="{style}" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="{width}" height="{height}" as="geometry" />
</mxCell>'''
    return xml_snippet

# Load the extracted styles
with open('bpmn_styles.json', 'r', encoding='utf-8') as f:
    unique_elements = json.load(f)

categorized_elements = []
for element in unique_elements:
    style_props = parse_style_string(element['style'])
    bpmn_type, description = get_bpmn_type_and_description(style_props, element['value'])
    xml_snippet = generate_xml_snippet(element['style'], element['value'] if element['value'] else 'Nombre del Objeto')
    
    categorized_elements.append({
        'type': bpmn_type,
        'description': description,
        'style': element['style'], # Keep original style for reference
        'value': element['value'], # Keep original value for reference
        'xml_snippet': xml_snippet
    })

# Sort by type for better readability in the Markdown
categorized_elements_sorted = sorted(categorized_elements, key=lambda x: x['type'])

# Generate Markdown
markdown_content = """# Tutorial: Creación Programática de Diagramas BPMN 2.0 con IA (Gemini)\n\nEste tutorial te guiará a través de los distintos objetos BPMN 2.0 disponibles en diagrams.net y cómo puedes representarlos en formato XML para que una IA como Gemini pueda generarlos programáticamente.\n\n## Introducción al Formato XML de diagrams.net (mxGraph)\n\nLos diagramas de diagrams.net se almacenan en un formato XML que describe la estructura y el estilo de cada elemento gráfico. Cada forma o conector se representa como un elemento <mxCell> con atributos clave como `id`, `value` (el texto visible), `style` (que define la apariencia y el tipo de objeto BPMN), `vertex` (1 para formas, 0 para conectores) y `parent` (para la jerarquía).\n\nAl solicitar a una IA que genere un diagrama, puedes proporcionarle estos fragmentos XML para asegurar que los objetos se creen con el estilo y tipo correctos.\n\n## Lista de Objetos BPMN 2.0 y su Representación XML\n\n"""

for item in categorized_elements_sorted:
    markdown_content += f"### {item['type']}\n\n"
    markdown_content += f"**Descripción:** {item['description']}\n\n"
    markdown_content += f"**Ejemplo de XML:**\n"
    markdown_content += f"```xml\n{item['xml_snippet']}\n```\n\n"

# Save the Markdown content to a file
with open('bpmn_tutorial.md', 'w', encoding='utf-8') as f:
    f.write(markdown_content)

print('bpmn_tutorial.md generated successfully with bullet points.')