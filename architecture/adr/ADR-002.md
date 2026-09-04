---
id: ADR-002
title: "Patrón de Estrategia para Motor de Priorización RIME"
date: 2026-08-25
status: Accepted
author: Juan David Julio Serrano
deciders: Arquitecto de Software
linked_to: 
  - "[[MTTO-026]]"
  - "[[UC-MTTO-026]]"
---

# ADR-002: Patrón de Estrategia para Motor de Priorización RIME

## Contexto
La gestión del backlog exige una priorización objetiva de acuerdo con la norma ISO 55001. El estándar del MVP definió un modelo matemático de dos factores, calculando el puntaje mediante la multiplicación de la criticidad por la clase de trabajo. Sin embargo, en operaciones industriales complejas, el departamento de mantenimiento podría adaptar el modelo RIME incorporando factores económicos, impacto de inventario y mantenibilidad. Programar estáticamente la fórmula de dos factores acopla el dominio y dificulta la personalización comercial del sistema.

## Decisión
Se adopta el **Patrón de Estrategia** para aislar el algoritmo de cálculo RIME de las entidades de solicitud de trabajo y elementos del backlog. 

Se define la interfaz de dominio `IRimeCalculator`. Para el MVP, se inyectará la estrategia estándar basada en una fórmula de 2 factores con un rango de 1 a 100. La arquitectura quedará abierta para registrar dinámicamente estrategias personalizadas a través del contenedor de inyección de dependencias sin modificar los controladores ni las entidades.

## Alternativas Consideradas
* **Cálculo embebido en la entidad `WorkRequest`:** Rechazado. Viola el Principio de Abierto/Cerrado y obliga a modificar la raíz de agregado cada vez que un cliente industrial solicite cambiar los pesos de la matriz RIME.
* **Cálculo en base de datos mediante procedimientos almacenados:** Rechazado. Provoca fuga de la lógica de dominio a la capa de persistencia.

## Consecuencias

### Positivas
* Permite al MVP operar de forma determinística e independiente del estado de completitud del módulo de inventario.
* Satisface el requerimiento de extensibilidad comercial al permitir matrices de riesgo personalizadas.

### Negativas
* Añade una capa de abstracción al flujo de admisión del backlog.
* Los reportes de indicadores clave deben diseñarse tolerantes a diferentes escalas de prioridad según la estrategia activa.

### Riesgos y Deuda Técnica
* La implementación de una estrategia extendida dependerá del rendimiento de las consultas cruzadas con el módulo de inventario en tiempo real.