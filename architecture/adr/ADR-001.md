---
id: ADR-001
title: "Estrategia de Visualización Híbrida (2D Primero, 3D Evolutivo)"
date: 2026-03-18
status: Accepted
author: Juan David Julio Serrano
deciders: Arquitecto de Software
linked_to: 
  - "[[VIS-008]]"
  - "[[VIS-011]]"
  - "[[UC-VIS-033]]"
---

# ADR-001: Estrategia de Visualización Híbrida (2D Primero, 3D Evolutivo)

## Contexto
El Gemelo Digital EAM requiere representar de forma espacial la planta industrial para visualizar telemetría y aplicar la filosofía de seguridad ISA-101 y rutas LOTO. La implementación de un motor 3D exige modelos CAD o STEP procesados, lo cual retrasa la validación de la lógica de seguridad funcional y consume un alto nivel de memoria en dispositivos móviles de campo, afectando el requisito de rendimiento ASR-1.

## Decisión
Se adopta una **Estrategia de Visualización Híbrida**:
1. **MVP (Canvas 2D):** El sistema utilizará representaciones 2D basadas en planos vectoriales SVG escalables embebidos nativamente en componentes Razor. El lienzo opera bajo un modelo híbrido: en el Nivel 1 (L1 - Visión General / COP) actúa como un *Simplified Plot Plan / Process Overview*, mostrando la silueta espacial de los límites de batería y la disposición general; en el Nivel 2 (L2 - Bahía / Subsistema) revela detalles de *P&ID / Lazos de Proceso*. Esto elimina la necesidad de motores gráficos de terceros para la versión inicial, permitiendo la manipulación directa del DOM para las alertas.
2. **Abstracción Arquitectónica:** Las capas de seguridad operarán sobre metadatos espaciales agnósticos. 
3. **Evolución 3D:** El sistema transicionará hacia un motor 3D en fases posteriores, consumiendo la misma lógica de negocio y metadatos sin requerir reescritura del backend. La vinculación se realizará mediante el patrón *Sidecar* y la entidad desacoplada `MeshMapping`: el dominio desconoce el motor gráfico y se vincula mediante identificadores geométricos (`svgElementId` en 2D y `meshUuid` en 3D), mapeados exclusivamente al Nivel 6 de la ISO 14224 (`EquipmentUnit`).

## Alternativas Consideradas
* **Uso de SkiaSharp para 2D:** Rechazado. Genera cuellos de botella por comunicación entre procesos en Blazor Hybrid y errores de compatibilidad de plataforma al no compilar a WebAssembly en el cliente móvil.
* **Integración temprana de WebGL o Three.js:** Rechazado. Alta probabilidad de fallos por agotamiento de memoria en el visor web móvil al cargar mallas complejas.

## Consecuencias

### Positivas
* Latencia de renderizado reducida y menor consumo de batería en dispositivos móviles.
* Interacción nativa entre el estado de los componentes Blazor y los vectores gráficos.

### Negativas
* Los mapas 2D requieren diseño manual y no se generan automáticamente desde la ingeniería de planta.

### Riesgos y Deuda Técnica
* Obliga a refactorizar el componente visual del cliente cuando se habilite el módulo 3D, manteniendo la compatibilidad con las coordenadas 2D mapeadas previamente.