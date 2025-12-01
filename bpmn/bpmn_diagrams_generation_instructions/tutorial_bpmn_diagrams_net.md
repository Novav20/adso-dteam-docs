# Tutorial: Creación Programática de Diagramas BPMN 2.0 con IA (Gemini)

Este tutorial te guiará a través de los distintos objetos BPMN 2.0 disponibles en diagrams.net y cómo puedes representarlos en formato XML para que una IA como Gemini pueda generarlos programáticamente.

## Introducción al Formato XML de diagrams.net (mxGraph)

Los diagramas de diagrams.net se almacenan en un formato XML que describe la estructura y el estilo de cada elemento gráfico. Cada forma o conector se representa como un elemento <mxCell> con atributos clave como `id`, `value` (el texto visible), `style` (que define la apariencia y el tipo de objeto BPMN), `vertex` (1 para formas, 0 para conectores) y `parent` (para la jerarquía).

Al solicitar a una IA que genere un diagrama, puedes proporcionarle estos fragmentos XML para asegurar que los objetos se creen con el estilo y tipo correctos.

## Lista de Objetos BPMN 2.0 y su Representación XML

### Actividad de Llamada

**Descripción:** Actividad de Llamada

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;bpmnShapeType=call;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Actividad de Llamada

**Descripción:** Actividad de Llamada (Subproceso Global)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;bpmnShapeType=call;isLoopSub=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Actividad de Llamada

**Descripción:** Actividad de Llamada

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;bpmnShapeType=call;taskMarker=businessRule;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Actividad de Llamada

**Descripción:** Actividad de Llamada

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;bpmnShapeType=call;taskMarker=manual;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Actividad de Llamada

**Descripción:** Actividad de Llamada

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;bpmnShapeType=call;taskMarker=script;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Actividad de Llamada

**Descripción:** Actividad de Llamada

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;bpmnShapeType=call;taskMarker=user;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Actividad de Llamada

**Descripción:** Actividad de Llamada

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;bpmnShapeType=call;verticalAlign=top;align=left;spacingLeft=5;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Actividad de Transacción

**Descripción:** Actividad de Transacción

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=abstract;bpmnShapeType=transaction;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Actividad de Transacción

**Descripción:** Actividad de Transacción

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=abstract;bpmnShapeType=transaction;isLoopSub=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Almacén de Datos

**Descripción:** Almacén de Datos

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=datastore;html=1;labelPosition=center;verticalLabelPosition=bottom;align=center;verticalAlign=top;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Anotación

**Descripción:** Anotación (Comentario)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="html=1;shape=mxgraph.flowchart.annotation_2;align=left;labelPosition=right;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos ()

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=boundInt;symbol=cancel;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos ()

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=boundInt;symbol=compensation;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Condicional)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=boundInt;symbol=conditional;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos ()

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=boundInt;symbol=error;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos ()

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=boundInt;symbol=escalation;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Mensaje)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=boundInt;symbol=message;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Múltiple)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=boundInt;symbol=multiple;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Múltiple Paralelo)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=boundInt;symbol=parallelMultiple;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Señal)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=boundInt;symbol=signal;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Temporizador)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=boundInt;symbol=timer;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Condicional)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=boundNonint;symbol=conditional;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos ()

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=boundNonint;symbol=escalation;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Mensaje)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=boundNonint;symbol=message;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Múltiple)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=boundNonint;symbol=multiple;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Múltiple Paralelo)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=boundNonint;symbol=parallelMultiple;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Señal)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=boundNonint;symbol=signal;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Temporizador)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=boundNonint;symbol=timer;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Condicional)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=catching;symbol=conditional;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos ()

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=catching;symbol=link;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Mensaje)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=catching;symbol=message;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Múltiple)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=catching;symbol=multiple;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Múltiple Paralelo)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=catching;symbol=parallelMultiple;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Señal)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=catching;symbol=signal;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Temporizador)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=catching;symbol=timer;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos ()

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=end;symbol=cancel;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos ()

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=end;symbol=compensation;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos ()

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=end;symbol=error;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos ()

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=end;symbol=escalation;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos ()

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=end;symbol=general;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Mensaje)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=end;symbol=message;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Múltiple)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=end;symbol=multiple;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Señal)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=end;symbol=signal;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos ()

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=end;symbol=terminate;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos ()

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=eventInt;symbol=compensation;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Condicional)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=eventInt;symbol=conditional;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos ()

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=eventInt;symbol=error;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos ()

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=eventInt;symbol=escalation;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Mensaje)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=eventInt;symbol=message;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Múltiple)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=eventInt;symbol=multiple;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Múltiple Paralelo)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=eventInt;symbol=parallelMultiple;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Señal)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=eventInt;symbol=signal;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Temporizador)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=eventInt;symbol=timer;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Condicional)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=eventNonint;symbol=conditional;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos ()

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=eventNonint;symbol=escalation;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Mensaje)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=eventNonint;symbol=message;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Múltiple)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=eventNonint;symbol=multiple;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Múltiple Paralelo)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=eventNonint;symbol=parallelMultiple;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Señal)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=eventNonint;symbol=signal;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Temporizador)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=eventNonint;symbol=timer;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos ()

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=none;symbol=none;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos ()

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=none;symbol=none;gwType=complex;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos ()

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=none;symbol=none;gwType=exclusive;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos ()

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=none;symbol=none;gwType=parallel;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Condicional)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=standard;symbol=conditional;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos ()

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=standard;symbol=general;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Mensaje)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=standard;symbol=message;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Múltiple)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=standard;symbol=multiple;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Múltiple Paralelo)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=standard;symbol=parallelMultiple;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Señal)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=standard;symbol=signal;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos ()

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=standard;symbol=star;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Temporizador)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=standard;symbol=timer;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos ()

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=throwing;symbol=compensation;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos ()

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=throwing;symbol=escalation;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos ()

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=throwing;symbol=general;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos ()

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=throwing;symbol=link;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Mensaje)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=throwing;symbol=message;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Múltiple)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=throwing;symbol=multiple;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Compuerta Basada en Eventos

**Descripción:** Compuerta Basada en Eventos (Señal)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0.25,0],[0.5,0,0],[0.75,0.25,0],[1,0.5,0],[0.75,0.75,0],[0.5,1,0],[0.25,0.75,0],[0,0.5,0]];shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=rhombusPerimeter;outlineConnect=0;outline=throwing;symbol=signal;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Conversación

**Descripción:** Elemento de Conversación

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.conversation2;perimeter=hexagonPerimeter2;whiteSpace=wrap;html=1;aspect=fixed;bpmnConversationType=conv;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Conversación

**Descripción:** Elemento de Conversación (Subproceso)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.conversation2;perimeter=hexagonPerimeter2;whiteSpace=wrap;html=1;aspect=fixed;bpmnConversationType=conv;isLoopSub=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Fin

**Descripción:** Evento Fin de Cancelación

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=end;symbol=cancel;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Fin

**Descripción:** Evento Fin de Compensación

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=end;symbol=compensation;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Fin

**Descripción:** Evento Fin de 

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=end;symbol=error;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Fin

**Descripción:** Evento Fin de Escalada

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=end;symbol=escalation;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Fin

**Descripción:** Evento Fin de Mensaje

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=end;symbol=message;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Fin

**Descripción:** Evento Fin de Múltiple

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=end;symbol=multiple;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Fin

**Descripción:** Evento Fin de Señal

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=end;symbol=signal;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Fin

**Descripción:** Evento Fin de Terminación (Error)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=end;symbol=terminate2;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Fin

**Descripción:** Evento Fin de Terminación

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=end;symbol=terminate;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Inicio

**Descripción:** Evento Inicio de Condicional

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=standard;symbol=conditional;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Inicio

**Descripción:** Evento Inicio de Genérico

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=standard;symbol=general;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Inicio

**Descripción:** Evento Inicio de Mensaje

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=standard;symbol=message;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Inicio

**Descripción:** Evento Inicio de Múltiple

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=standard;symbol=multiple;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Inicio

**Descripción:** Evento Inicio de Señal

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=standard;symbol=signal;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Inicio

**Descripción:** Evento Inicio de Temporizador

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=standard;symbol=timer;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Intermedio (Captura)

**Descripción:** Evento Intermedio (Captura) de Condicional

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=catching;symbol=conditional;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Intermedio (Captura)

**Descripción:** Evento Intermedio (Captura) de Enlace

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=catching;symbol=link;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Intermedio (Captura)

**Descripción:** Evento Intermedio (Captura) de Mensaje

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=catching;symbol=message;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Intermedio (Captura)

**Descripción:** Evento Intermedio (Captura) de Múltiple

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=catching;symbol=multiple;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Intermedio (Captura)

**Descripción:** Evento Intermedio (Captura) de Múltiple Paralelo

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=catching;symbol=parallelMultiple;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Intermedio (Captura)

**Descripción:** Evento Intermedio (Captura) de Señal

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=catching;symbol=signal;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Intermedio (Captura)

**Descripción:** Evento Intermedio (Captura) de Temporizador

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=catching;symbol=timer;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Intermedio (Interrupción)

**Descripción:** Evento Intermedio (Interrupción) de Compensación

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=eventInt;symbol=compensation;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Intermedio (Interrupción)

**Descripción:** Evento Intermedio (Interrupción) de 

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=eventInt;symbol=error;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Intermedio (Interrupción)

**Descripción:** Evento Intermedio (Interrupción) de Escalada

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=eventInt;symbol=escalation;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Intermedio (Interrupción)

**Descripción:** Evento Intermedio (Interrupción) de Múltiple Paralelo

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=eventInt;symbol=parallelMultiple;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Intermedio (Lanzamiento)

**Descripción:** Evento Intermedio (Lanzamiento) de Compensación

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=throwing;symbol=compensation;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Intermedio (Lanzamiento)

**Descripción:** Evento Intermedio (Lanzamiento) de Escalada

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=throwing;symbol=escalation;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Intermedio (Lanzamiento)

**Descripción:** Evento Intermedio (Lanzamiento) de Genérico

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=throwing;symbol=general;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Intermedio (Lanzamiento)

**Descripción:** Evento Intermedio (Lanzamiento) de Enlace

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=throwing;symbol=link;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Intermedio (Lanzamiento)

**Descripción:** Evento Intermedio (Lanzamiento) de Mensaje

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=throwing;symbol=message;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Intermedio (Lanzamiento)

**Descripción:** Evento Intermedio (Lanzamiento) de Múltiple

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=throwing;symbol=multiple;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Intermedio (Lanzamiento)

**Descripción:** Evento Intermedio (Lanzamiento) de Señal

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=throwing;symbol=signal;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Intermedio (No Interrupción)

**Descripción:** Evento Intermedio (No Interrupción) de Condicional

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=eventNonint;symbol=conditional;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Intermedio (No Interrupción)

**Descripción:** Evento Intermedio (No Interrupción) de Escalada

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=eventNonint;symbol=escalation;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Intermedio (No Interrupción)

**Descripción:** Evento Intermedio (No Interrupción) de Mensaje

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=eventNonint;symbol=message;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Intermedio (No Interrupción)

**Descripción:** Evento Intermedio (No Interrupción) de Múltiple

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=eventNonint;symbol=multiple;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Intermedio (No Interrupción)

**Descripción:** Evento Intermedio (No Interrupción) de Múltiple Paralelo

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=eventNonint;symbol=parallelMultiple;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Intermedio (No Interrupción)

**Descripción:** Evento Intermedio (No Interrupción) de Señal

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=eventNonint;symbol=signal;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Intermedio (No Interrupción)

**Descripción:** Evento Intermedio (No Interrupción) de Temporizador

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=eventNonint;symbol=timer;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Límite (Interrupción)

**Descripción:** Evento Límite (Interrupción) de Cancelación

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=boundInt;symbol=cancel;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Límite (Interrupción)

**Descripción:** Evento Límite (Interrupción) de Compensación

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=boundInt;symbol=compensation;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Límite (Interrupción)

**Descripción:** Evento Límite (Interrupción) de Condicional

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=boundInt;symbol=conditional;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Límite (Interrupción)

**Descripción:** Evento Límite (Interrupción) de 

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=boundInt;symbol=error;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Límite (Interrupción)

**Descripción:** Evento Límite (Interrupción) de Escalada

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=boundInt;symbol=escalation;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Límite (Interrupción)

**Descripción:** Evento Límite (Interrupción) de Mensaje

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=boundInt;symbol=message;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Límite (Interrupción)

**Descripción:** Evento Límite (Interrupción) de Múltiple

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=boundInt;symbol=multiple;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Límite (Interrupción)

**Descripción:** Evento Límite (Interrupción) de Múltiple Paralelo

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=boundInt;symbol=parallelMultiple;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Límite (Interrupción)

**Descripción:** Evento Límite (Interrupción) de Señal

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=boundInt;symbol=signal;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Límite (Interrupción)

**Descripción:** Evento Límite (Interrupción) de Temporizador

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=boundInt;symbol=timer;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Límite (No Interrupción)

**Descripción:** Evento Límite (No Interrupción) de Condicional

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=boundNonint;symbol=conditional;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Límite (No Interrupción)

**Descripción:** Evento Límite (No Interrupción) de Escalada

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=boundNonint;symbol=escalation;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Límite (No Interrupción)

**Descripción:** Evento Límite (No Interrupción) de Mensaje

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=boundNonint;symbol=message;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Límite (No Interrupción)

**Descripción:** Evento Límite (No Interrupción) de Múltiple

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=boundNonint;symbol=multiple;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Límite (No Interrupción)

**Descripción:** Evento Límite (No Interrupción) de Múltiple Paralelo

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=boundNonint;symbol=parallelMultiple;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Límite (No Interrupción)

**Descripción:** Evento Límite (No Interrupción) de Señal

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=boundNonint;symbol=signal;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Evento Límite (No Interrupción)

**Descripción:** Evento Límite (No Interrupción) de Temporizador

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.145,0.145,0],[0.5,0,0],[0.855,0.145,0],[1,0.5,0],[0.855,0.855,0],[0.5,1,0],[0.145,0.855,0],[0,0.5,0]];shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=boundNonint;symbol=timer;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Fila de Tabla (Actor Cross-Functional)

**Descripción:** Representa un Actor o Rol en un Diagrama Cross-Functional

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Actor 1" style="shape=tableRow;horizontal=0;swimlaneHead=0;swimlaneBody=0;top=0;left=0;strokeColor=inherit;bottom=0;right=0;dropTarget=0;fontStyle=1;fillColor=none;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;startSize=40;collapsible=0;recursiveResize=0;expand=0;fontSize=16;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="400" height="150" as="geometry" />
</mxCell>
```

### Fila de Tabla (Actor Cross-Functional)

**Descripción:** Representa un Actor o Rol en un Diagrama Cross-Functional

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Actor 2" style="shape=tableRow;horizontal=0;swimlaneHead=0;swimlaneBody=0;top=0;left=0;strokeColor=inherit;bottom=0;right=0;dropTarget=0;fontStyle=1;fillColor=none;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;startSize=40;collapsible=0;recursiveResize=0;expand=0;fontSize=16;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="400" height="150" as="geometry" />
</mxCell>
```

### Fila de Tabla (Actor Cross-Functional)

**Descripción:** Representa un Actor o Rol en un Diagrama Cross-Functional

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Actor 3" style="shape=tableRow;horizontal=0;swimlaneHead=0;swimlaneBody=0;top=0;left=0;strokeColor=inherit;bottom=0;right=0;dropTarget=0;fontStyle=1;fillColor=none;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;startSize=40;collapsible=0;recursiveResize=0;expand=0;fontSize=16;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="400" height="150" as="geometry" />
</mxCell>
```

### Llamada de Conversación

**Descripción:** Elemento de Llamada de Conversación

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.conversation2;perimeter=hexagonPerimeter2;whiteSpace=wrap;html=1;aspect=fixed;bpmnConversationType=call;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Llamada de Conversación

**Descripción:** Elemento de Llamada de Conversación (Subproceso)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.conversation2;perimeter=hexagonPerimeter2;whiteSpace=wrap;html=1;aspect=fixed;bpmnConversationType=call;isLoopSub=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Objeto Genérico

**Descripción:** 

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];rounded=1;arcSize=10;dashed=1;fillColor=none;gradientColor=none;dashPattern=8 3 1 3;strokeWidth=2;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Objeto Genérico

**Descripción:** 

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];rounded=1;dashed=1;dashPattern=5 2 1 2;labelPosition=center;verticalLabelPosition=middle;align=center;verticalAlign=middle;fontSize=8;html=1;whiteSpace=wrap;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Objeto Genérico

**Descripción:** 

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="rounded=1;whiteSpace=wrap;html=1;container=1;collapsible=0;absoluteArcSize=1;arcSize=20;childLayout=stackLayout;horizontal=1;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Objeto Genérico

**Descripción:** 

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="rounded=1;whiteSpace=wrap;html=1;container=1;collapsible=0;absoluteArcSize=1;arcSize=20;childLayout=stackLayout;horizontal=1;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;strokeWidth=8;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Objeto Genérico

**Descripción:** 

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=message;fillColor=#C0C0C0;html=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Objeto Genérico

**Descripción:** 

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=message;html=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Objeto Genérico

**Descripción:** 

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=message;html=1;outlineConnect=0;labelPosition=left;verticalLabelPosition=middle;align=right;verticalAlign=middle;spacingRight=5;labelBackgroundColor=#ffffff;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Objeto Genérico

**Descripción:** 

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=message;html=1;outlineConnect=0;labelPosition=left;verticalLabelPosition=middle;align=right;verticalAlign=middle;spacingRight=5;labelBackgroundColor=#ffffff;fillColor=#C0C0C0;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Objeto Genérico

**Descripción:** Pool

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Pool" style="swimlane;html=1;childLayout=stackLayout;resizeParent=1;resizeParentMax=0;horizontal=0;startSize=20;horizontalStack=0;whiteSpace=wrap;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="400" height="150" as="geometry" />
</mxCell>
```

### Objeto Genérico

**Descripción:** Pool

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Pool" style="swimlane;html=1;childLayout=stackLayout;resizeParent=1;resizeParentMax=0;horizontal=1;startSize=20;horizontalStack=0;whiteSpace=wrap;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="400" height="150" as="geometry" />
</mxCell>
```

### Objeto Genérico

**Descripción:** Pool

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Pool" style="swimlane;html=1;childLayout=stackLayout;resizeParent=1;resizeParentMax=0;startSize=20;horizontal=0;horizontalStack=1;whiteSpace=wrap;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="400" height="150" as="geometry" />
</mxCell>
```

### Objeto Genérico

**Descripción:** Pool

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Pool" style="swimlane;html=1;childLayout=stackLayout;resizeParent=1;resizeParentMax=0;startSize=20;whiteSpace=wrap;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="400" height="150" as="geometry" />
</mxCell>
```

### Objeto Genérico

**Descripción:** Lane 1

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Lane 1" style="swimlane;html=1;startSize=20;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="400" height="150" as="geometry" />
</mxCell>
```

### Objeto Genérico

**Descripción:** Lane 2

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Lane 2" style="swimlane;html=1;startSize=20;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="400" height="150" as="geometry" />
</mxCell>
```

### Objeto Genérico

**Descripción:** Lane 3

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Lane 3" style="swimlane;html=1;startSize=20;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="400" height="150" as="geometry" />
</mxCell>
```

### Objeto Genérico

**Descripción:** 

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="swimlane;html=1;startSize=20;fontStyle=0;collapsible=0;horizontal=0;swimlaneLine=0;fillColor=none;whiteSpace=wrap;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="400" height="150" as="geometry" />
</mxCell>
```

### Objeto Genérico

**Descripción:** 

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="swimlane;html=1;startSize=20;fontStyle=0;collapsible=0;horizontal=0;swimlaneLine=1;swimlaneFillColor=#ffffff;strokeWidth=2;whiteSpace=wrap;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="400" height="150" as="geometry" />
</mxCell>
```

### Objeto Genérico

**Descripción:** 

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="swimlane;html=1;startSize=20;fontStyle=0;collapsible=0;horizontal=1;swimlaneLine=0;fillColor=none;whiteSpace=wrap;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="400" height="150" as="geometry" />
</mxCell>
```

### Objeto Genérico

**Descripción:** 

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="swimlane;html=1;startSize=20;fontStyle=0;collapsible=0;horizontal=1;swimlaneLine=1;strokeWidth=2;swimlaneFillColor=#ffffff;whiteSpace=wrap;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="400" height="150" as="geometry" />
</mxCell>
```

### Objeto Genérico

**Descripción:** Lane 1

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Lane 1" style="swimlane;html=1;startSize=20;horizontal=0;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="400" height="150" as="geometry" />
</mxCell>
```

### Objeto Genérico

**Descripción:** Lane 2

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Lane 2" style="swimlane;html=1;startSize=20;horizontal=0;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="400" height="150" as="geometry" />
</mxCell>
```

### Objeto Genérico

**Descripción:** Lane 3

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Lane 3" style="swimlane;html=1;startSize=20;horizontal=0;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="400" height="150" as="geometry" />
</mxCell>
```

### Objeto Genérico

**Descripción:** Lane

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Lane" style="swimlane;startSize=20;horizontal=0;html=1;whiteSpace=wrap;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="400" height="150" as="geometry" />
</mxCell>
```

### Objeto Genérico

**Descripción:** Lane

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Lane" style="swimlane;startSize=20;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="400" height="150" as="geometry" />
</mxCell>
```

### Objeto Genérico

**Descripción:** 

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="swimlane;swimlaneHead=0;swimlaneBody=0;fontStyle=1;connectable=0;strokeColor=inherit;fillColor=none;startSize=0;collapsible=0;recursiveResize=0;expand=0;fontSize=16;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="400" height="150" as="geometry" />
</mxCell>
```

### Objeto Genérico

**Descripción:** Phase 1

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Phase 1" style="swimlane;swimlaneHead=0;swimlaneBody=0;fontStyle=1;strokeColor=inherit;connectable=0;fillColor=none;startSize=40;collapsible=0;recursiveResize=0;expand=0;fontSize=16;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="400" height="150" as="geometry" />
</mxCell>
```

### Objeto Genérico

**Descripción:** Phase 2

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Phase 2" style="swimlane;swimlaneHead=0;swimlaneBody=0;fontStyle=1;strokeColor=inherit;connectable=0;fillColor=none;startSize=40;collapsible=0;recursiveResize=0;expand=0;fontSize=16;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="400" height="150" as="geometry" />
</mxCell>
```

### Objeto Genérico

**Descripción:** Phase 3

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Phase 3" style="swimlane;swimlaneHead=0;swimlaneBody=0;fontStyle=1;strokeColor=inherit;connectable=0;fillColor=none;startSize=40;collapsible=0;recursiveResize=0;expand=0;fontSize=16;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="400" height="150" as="geometry" />
</mxCell>
```

### Objeto Genérico

**Descripción:** Text

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Text" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Objeto Genérico

**Descripción:** 

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="whiteSpace=wrap;connectable=0;html=1;shape=mxgraph.basic.rect;size=10;rectStyle=rounded;bottomRightStyle=square;bottomLeftStyle=square;fillColor=#C0C0C0;part=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Objeto Genérico

**Descripción:** 

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="whiteSpace=wrap;connectable=0;html=1;shape=mxgraph.basic.rect;size=10;rectStyle=rounded;bottomRightStyle=square;bottomLeftStyle=square;part=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Objeto Genérico

**Descripción:** 

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="whiteSpace=wrap;connectable=0;html=1;shape=mxgraph.basic.rect;size=10;rectStyle=rounded;topRightStyle=square;topLeftStyle=square;fillColor=#C0C0C0;part=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Objeto Genérico

**Descripción:** 

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="whiteSpace=wrap;connectable=0;html=1;shape=mxgraph.basic.rect;size=10;rectStyle=rounded;topRightStyle=square;topLeftStyle=square;part=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Objeto de Datos

**Descripción:** Objeto de Datos (None)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.data2;labelPosition=center;verticalLabelPosition=bottom;align=center;verticalAlign=top;size=15;html=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Objeto de Datos

**Descripción:** Objeto de Datos (Input)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.data2;labelPosition=center;verticalLabelPosition=bottom;align=center;verticalAlign=top;size=15;html=1;bpmnTransferType=input;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Objeto de Datos

**Descripción:** Objeto de Datos (Input) (Colección)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.data2;labelPosition=center;verticalLabelPosition=bottom;align=center;verticalAlign=top;size=15;html=1;bpmnTransferType=input;isCollection=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Objeto de Datos

**Descripción:** Objeto de Datos (None) (Colección)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.data2;labelPosition=center;verticalLabelPosition=bottom;align=center;verticalAlign=top;size=15;html=1;bpmnTransferType=none;isCollection=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Objeto de Datos

**Descripción:** Objeto de Datos (Output)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.data2;labelPosition=center;verticalLabelPosition=bottom;align=center;verticalAlign=top;size=15;html=1;bpmnTransferType=output;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Objeto de Datos

**Descripción:** Objeto de Datos (Output) (Colección)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.data2;labelPosition=center;verticalLabelPosition=bottom;align=center;verticalAlign=top;size=15;html=1;bpmnTransferType=output;isCollection=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Pool (Colapsable)

**Descripción:** Pool (Contenedor de Procesos, Colapsable)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.swimlane;html=1;startSize=20;horizontal=0;swimlaneLine=1;collapsible=0;fontStyle=0;swimlaneFillColor=#ffffff;strokeWidth=2;isCollection=1;whiteSpace=wrap;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="400" height="150" as="geometry" />
</mxCell>
```

### Pool (Colapsable)

**Descripción:** Pool (Contenedor de Procesos, Colapsable)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.swimlane;html=1;startSize=20;horizontal=1;swimlaneLine=1;collapsible=0;fontStyle=0;strokeWidth=2;swimlaneFillColor=#ffffff;isCollection=1;whiteSpace=wrap;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="400" height="150" as="geometry" />
</mxCell>
```

### Subproceso

**Descripción:** Subproceso con Evento Adjunto (None General)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;arcSize=10;taskMarker=abstract;outline=none;symbol=general;bpmnShapeType=subprocess;isLoopSub=0;verticalAlign=top;align=left;spacingLeft=5;html=1;whiteSpace=wrap;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Subproceso

**Descripción:** Subproceso (Embebido) con Evento Adjunto (Eventint Compensation)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=abstract;bpmnShapeType=subprocess;isLoopSub=1;outline=eventInt;symbol=compensation;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Subproceso

**Descripción:** Subproceso (Embebido) con Evento Adjunto (Eventint Conditional)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=abstract;bpmnShapeType=subprocess;isLoopSub=1;outline=eventInt;symbol=conditional;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Subproceso

**Descripción:** Subproceso (Embebido) con Evento Adjunto (Eventint Error)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=abstract;bpmnShapeType=subprocess;isLoopSub=1;outline=eventInt;symbol=error;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Subproceso

**Descripción:** Subproceso (Embebido) con Evento Adjunto (Eventint Escalation)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=abstract;bpmnShapeType=subprocess;isLoopSub=1;outline=eventInt;symbol=escalation;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Subproceso

**Descripción:** Subproceso (Embebido) con Evento Adjunto (Eventint Message)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=abstract;bpmnShapeType=subprocess;isLoopSub=1;outline=eventInt;symbol=message;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Subproceso

**Descripción:** Subproceso (Embebido) con Evento Adjunto (Eventint Multiple)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=abstract;bpmnShapeType=subprocess;isLoopSub=1;outline=eventInt;symbol=multiple;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Subproceso

**Descripción:** Subproceso (Embebido) con Evento Adjunto (Eventint Parallelmultiple)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=abstract;bpmnShapeType=subprocess;isLoopSub=1;outline=eventInt;symbol=parallelMultiple;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Subproceso

**Descripción:** Subproceso (Embebido) con Evento Adjunto (Eventint Signal)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=abstract;bpmnShapeType=subprocess;isLoopSub=1;outline=eventInt;symbol=signal;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Subproceso

**Descripción:** Subproceso (Embebido) con Evento Adjunto (Eventint Timer)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=abstract;bpmnShapeType=subprocess;isLoopSub=1;outline=eventInt;symbol=timer;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Subproceso

**Descripción:** Subproceso (Embebido) con Evento Adjunto (Eventnonint Conditional)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=abstract;bpmnShapeType=subprocess;isLoopSub=1;outline=eventNonint;symbol=conditional;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Subproceso

**Descripción:** Subproceso (Embebido) con Evento Adjunto (Eventnonint Escalation)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=abstract;bpmnShapeType=subprocess;isLoopSub=1;outline=eventNonint;symbol=escalation;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Subproceso

**Descripción:** Subproceso (Embebido) con Evento Adjunto (Eventnonint Message)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=abstract;bpmnShapeType=subprocess;isLoopSub=1;outline=eventNonint;symbol=message;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Subproceso

**Descripción:** Subproceso (Embebido) con Evento Adjunto (Eventnonint Multiple)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=abstract;bpmnShapeType=subprocess;isLoopSub=1;outline=eventNonint;symbol=multiple;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Subproceso

**Descripción:** Subproceso (Embebido) con Evento Adjunto (Eventnonint Parallelmultiple)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=abstract;bpmnShapeType=subprocess;isLoopSub=1;outline=eventNonint;symbol=parallelMultiple;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Subproceso

**Descripción:** Subproceso (Embebido) con Evento Adjunto (Eventnonint Signal)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=abstract;bpmnShapeType=subprocess;isLoopSub=1;outline=eventNonint;symbol=signal;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Subproceso

**Descripción:** Subproceso (Embebido) con Evento Adjunto (Eventnonint Timer)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=abstract;bpmnShapeType=subprocess;isLoopSub=1;outline=eventNonint;symbol=timer;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tabla (Diagrama Cross-Functional)

**Descripción:** Contenedor para Diagramas Cross-Functional

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Cross-Functional Flowchart" style="shape=table;childLayout=tableLayout;startSize=40;collapsible=0;recursiveResize=0;expand=0;fontSize=16;fontStyle=1" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=abstract;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta (Ad-Hoc)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=abstract;isAdHoc=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta (Ad-Hoc)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=abstract;isAdHoc=1;isLoopSub=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta (Compensación)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=abstract;isLoopComp=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta (Loop Estándar) (Compensación)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=abstract;isLoopComp=1;isLoopStandard=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta (Loop Estándar) (Compensación)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=abstract;isLoopComp=1;isLoopStandard=1;isLoopSub=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta (Multi-Instancia Paralela)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=abstract;isLoopMultiParallel=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta (Multi-Instancia Secuencial)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=abstract;isLoopMultiSeq=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta (Loop Estándar)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=abstract;isLoopStandard=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta (Loop Estándar)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=abstract;isLoopStandard=1;isLoopSub=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=abstract;isLoopSub=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta (Compensación)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=abstract;isLoopSub=1;isLoopComp=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta (Multi-Instancia Paralela)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=abstract;isLoopSub=1;isLoopMultiParallel=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta (Multi-Instancia Secuencial)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=abstract;isLoopSub=1;isLoopMultiSeq=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea de Regla de Negocio

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=businessRule;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Manual

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=manual;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea de Recepción

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=receive;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea de Script

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=script;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea de Envío

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=send;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea de Servicio

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=service;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea de Usuario

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=user;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.task2;arcSize=0;part=1;taskMarker=abstract;connectable=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta (Multi-Instancia Paralela)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.task2;arcSize=0;part=1;taskMarker=abstract;isLoopMultiParallel=1;connectable=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta (Multi-Instancia Secuencial)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.task2;arcSize=0;part=1;taskMarker=abstract;isLoopMultiSeq=1;connectable=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta (Loop Estándar)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.task2;arcSize=0;part=1;taskMarker=abstract;isLoopStandard=1;connectable=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.task2;arcSize=0;part=1;taskMarker=abstract;isLoopSub=1;connectable=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta (Multi-Instancia Paralela)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.task2;arcSize=0;part=1;taskMarker=abstract;isLoopSub=1;isLoopMultiParallel=1;connectable=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta (Multi-Instancia Secuencial)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.task2;arcSize=0;part=1;taskMarker=abstract;isLoopSub=1;isLoopMultiSeq=1;connectable=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta (Loop Estándar)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.task2;arcSize=0;part=1;taskMarker=abstract;isLoopSub=1;isLoopStandard=1;connectable=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.task2;arcSize=0;part=1;taskMarker=abstract;verticalAlign=top;align=left;spacingLeft=5;connectable=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta (Multi-Instancia Paralela)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.task2;arcSize=0;taskMarker=abstract;part=1;isLoopMultiParallel=1;connectable=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta (Multi-Instancia Secuencial)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.task2;arcSize=0;taskMarker=abstract;part=1;isLoopMultiSeq=1;connectable=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta (Loop Estándar)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.task2;arcSize=0;taskMarker=abstract;part=1;isLoopStandard=1;connectable=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.task2;arcSize=0;taskMarker=abstract;part=1;isLoopSub=1;connectable=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta (Multi-Instancia Paralela)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.task2;arcSize=0;taskMarker=abstract;part=1;isLoopSub=1;isLoopMultiParallel=1;connectable=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta (Multi-Instancia Secuencial)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.task2;arcSize=0;taskMarker=abstract;part=1;isLoopSub=1;isLoopMultiSeq=1;connectable=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta (Loop Estándar)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.task2;arcSize=0;taskMarker=abstract;part=1;isLoopSub=1;isLoopStandard=1;connectable=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.task2;part=1;taskMarker=abstract;connectable=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.task2;part=1;taskMarker=abstract;rectStyle=rounded;bottomRightStyle=square;bottomLeftStyle=square;fillColor=#C0C0C0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta (Multi-Instancia Paralela)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.task2;part=1;taskMarker=abstract;rectStyle=rounded;bottomRightStyle=square;bottomLeftStyle=square;verticalAlign=top;isLoopMultiParallel=1;fillColor=#C0C0C0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta (Multi-Instancia Paralela)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.task2;part=1;taskMarker=abstract;rectStyle=rounded;bottomRightStyle=square;bottomLeftStyle=square;verticalAlign=top;isLoopMultiParallel=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.task2;part=1;taskMarker=abstract;rectStyle=rounded;bottomRightStyle=square;bottomLeftStyle=square;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.task2;part=1;taskMarker=abstract;rectStyle=rounded;isLoopSub=0;topLeftStyle=square;topRightStyle=square;fillColor=#C0C0C0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.task2;part=1;taskMarker=abstract;rectStyle=rounded;isLoopSub=0;topLeftStyle=square;topRightStyle=square;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta (Multi-Instancia Paralela)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.task2;part=1;taskMarker=abstract;rectStyle=rounded;topLeftStyle=square;topRightStyle=square;verticalAlign=top;isLoopMultiParallel=1;fillColor=#C0C0C0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta (Multi-Instancia Paralela)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.task2;part=1;taskMarker=abstract;rectStyle=rounded;topLeftStyle=square;topRightStyle=square;verticalAlign=top;isLoopMultiParallel=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta (Multi-Instancia Paralela)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.task2;part=1;taskMarker=abstract;rectStyle=rounded;verticalAlign=top;isLoopMultiParallel=1;topLeftStyle=square;topRightStyle=square;fillColor=#C0C0C0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta (Multi-Instancia Paralela)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.task2;part=1;taskMarker=abstract;rectStyle=rounded;verticalAlign=top;isLoopMultiParallel=1;topLeftStyle=square;topRightStyle=square;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.task2;part=1;taskMarker=abstract;rectStyle=square;fillColor=#C0C0C0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta (Multi-Instancia Paralela)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.task2;part=1;taskMarker=abstract;rectStyle=square;verticalAlign=top;isLoopMultiParallel=1;fillColor=#C0C0C0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta (Multi-Instancia Paralela)

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.task2;part=1;taskMarker=abstract;rectStyle=square;verticalAlign=top;isLoopMultiParallel=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="shape=mxgraph.bpmn.task2;part=1;taskMarker=abstract;rectStyle=square;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

### Tarea

**Descripción:** Tarea Abstracta

**Ejemplo de XML:**
```xml
<mxCell id="uniqueId" value="Nombre del Objeto" style="whiteSpace=wrap;shape=mxgraph.bpmn.task2;part=1;taskMarker=abstract;rectStyle=rounded;bottomRightStyle=square;bottomLeftStyle=square;html=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="100" height="50" as="geometry" />
</mxCell>
```

