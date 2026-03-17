# ADR 001: Estrategia de Visualización Híbrida (2D Primero, 3D Evolutivo)

**Fecha:** 18 de marzo de 2026
**Estatus:** Aceptado
**Contexto:**
El proyecto del Gemelo Digital EAM tiene como objetivo final la visualización 3D avanzada. Sin embargo, las restricciones de tiempo y recursos para la versión inicial (MVP) requieren una implementación rápida y funcional.

**Decisión:**
Se decide implementar una **Estrategia de Visualización Híbrida**:
1.  **Fase Inicial:** El sistema utilizará representaciones **2D basadas en planos técnicos (SVG)** y mapas de calor dinámicos. Esto garantiza compatibilidad multiplataforma inmediata y menor latencia de desarrollo.
2.  **Historias de Usuario (VIS-008, VIS-011):** Se mantienen como "MUST" con visión 3D en la documentación, pero su implementación técnica para la versión inicial se realizará mediante una "Capa de Abstracción 2D" que emule la lógica de seguridad (LOTO y Permisos) sobre planos.
3.  **Arquitectura:** El código debe ser diseñado para permitir el reemplazo del visor 2D por un visor 3D ( p.ej., Three.js/WebGL) en el futuro sin reescribir la lógica de negocio.

**Consecuencias:**
*   **Positivas:** Entrega del MVP en tiempos competitivos, menor carga computacional para dispositivos móviles (tablets de técnicos).
*   **Negativas:** Necesidad de mantener dos versiones de diagramas de actividad (una conceptual 3D y una operativa 2D) durante la fase de transición.
*   **Riesgos:** Asegurar que la lógica de "Energía Cero" sea igual de rigurosa en el plano 2D que en el 3D.
