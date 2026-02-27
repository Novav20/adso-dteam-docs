# 📘 ADSO: Sistema de Gemelo Digital - Repositorio de Documentación

Bienvenido al repositorio central de documentación técnica del proyecto **Gemelo Digital para Mantenimiento**.

Este repositorio sigue la filosofía **"Docs-as-Code"** (Documentación como Código). Aquí almacenamos los archivos **fuente** y editables de todos nuestros entregables. Las versiones finales (PDFs) y visualizaciones para lectura rápida se encuentran en nuestro **[Notion del Proyecto](https://www.notion.so/novav20/Proyecto-Gemelo-Digital-de-Mantenimiento-2aa87c56a8288088ad13c4c75e9a16c1?source=copy_link)**.

---

## 📂 Estructura del Repositorio

*   **`/bpmn`**: Contiene los diagramas de procesos (BPMN).
    *   *Nota:* Estos archivos son generados programáticamente (ver sección de Flujo de Trabajo).
*   **`/latex`**: Contiene el código fuente `.tex` de los documentos formales entregables.
*   **`/assets`**: Imágenes exportadas (PNG/SVG) listas para incrustar en Notion o documentos y artefactos extras.
*   **`/scripts`**: (Opcional) Scripts de utilidad para la generación de diagramas.
*   **`/prompts`**: Archivos de texto con las descripciones estructuradas que generan los diagramas.

---

## ⚙️ Flujo de Trabajo: Diagramas BPMN

⚠️ **IMPORTANTE:** No editar los archivos `.xml` o `.drawio` manualmente a menos que sea para retoques cosméticos finales.

Utilizamos un flujo de generación asistida por IA para mantener la consistencia técnica:

1.  **La "Fuente" es el Texto:** Los diagramas se definen primero en lenguaje natural estructurado (ubicados en `/prompts` o descripciones de issues).
2.  **Generación:** Se utiliza una herramienta CLI (con definiciones XML de BPMN) para "compilar" ese texto en un diagrama visual.
3.  **Refinamiento:** Se realizan ajustes menores (alineación, colores) en **Draw.io Desktop** y luego se exporta el archivo `.drawio`.
4.  **Subida al repositorio:** Se sube el archivo `.drawio` al repositorio.

**¿Cómo colaborar en un diagrama?**
Si necesitas cambiar la lógica de un proceso (ej. añadir un paso de aprobación):
1.  No edites el dibujo.
2.  Propón el cambio lógico en el texto descriptivo (en `/prompts` o en Notion).
3.  El mantenedor (Juan David) regenerará el diagrama base.

---

## 🛠️ Herramientas Utilizadas

*   **Modelado:** Draw.io (formato XML/Compressed XML).
*   **Documentación:** LaTeX (MikTex / TeXworks) para PDFs de alta calidad.
*   **Control de Versiones:** Git & GitHub.

---

## 🤝 Para el Equipo

1.  **¿Buscas el PDF para subir a Zajuna?** -> Ve al **Drive**.
2.  **¿Quieres ver cómo se hizo el documento o corregir una tilde?** -> Busca el archivo `.tex` en la carpeta `/latex`.
3.  **¿Tienes una nueva versión de un documento word?** -> Pásasela a Juan David para integrarla al sistema o súbela a la carpeta de borradores en Drive/Notion.

> *"La documentación desactualizada es deuda técnica."*