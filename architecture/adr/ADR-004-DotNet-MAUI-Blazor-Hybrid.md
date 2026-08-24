---
date: 2026-08-24
status: Aceptado
author: Juan David Julio Serrano
supersedes: Frontend React/React Native definido en versiones anteriores de la arquitectura
linked_to:
  - DT-ARQ-CMP-001 — Modelo de componentes
  - DT-ARQ-DEP-001 — Modelo de despliegue
---

# ADR 004: Cliente Frontend con .NET MAUI Blazor Hybrid

## Contexto

El sistema DTEAM requiere un cliente móvil para operación offline-first en campo y un cliente administrativo para supervisión HSEQ, planificación y dashboards. La arquitectura inicial contemplaba clientes separados basados en React y React Native. Esa decisión incrementaba la duplicación de componentes, modelos y lógica de interacción.

## Decisión

El cliente frontend objetivo será **.NET MAUI Blazor Hybrid**. La interfaz se implementará con componentes Razor y lógica en C#, compartiendo modelos y servicios entre las experiencias móvil y administrativa cuando sea técnicamente conveniente.

La comunicación con el backend seguirá utilizando HTTPS/JSON para operaciones de aplicación y SignalR sobre WSS para eventos en tiempo real, incluyendo el heartbeat de seguridad y las actualizaciones de KPIs.

La persistencia local utilizará SQLite mediante una biblioteca compatible con .NET MAUI. La biblioteca concreta deberá quedar registrada en el repositorio de código cuando se implemente el cliente.

## Justificación

- Reduce la duplicación entre clientes móvil y administrativo.
- Alinea el cliente con el backend .NET 10 y permite compartir tipos, validaciones y servicios en C#.
- Mantiene soporte para Android, iOS y otros destinos de .NET MAUI sin exigir dos stacks de UI distintos.
- Permite implementar la interfaz HPHMI y los controles fail-safe como componentes Razor reutilizables.

## Consecuencias

### Positivas

- Unificación del lenguaje principal del producto en el backend y el cliente.
- Reutilización de componentes, contratos, validaciones y pruebas.
- Integración directa con SignalR, EF Core y las bibliotecas del ecosistema .NET.

### Negativas y deuda técnica

- El equipo deberá aprender y mantener .NET MAUI, Blazor Hybrid y sus ciclos de publicación móvil.
- Se debe validar el rendimiento de WebView, el acceso a capacidades nativas y la operación offline en los dispositivos objetivo.
- La sustitución de WatermelonDB requiere seleccionar y probar la solución SQLite compatible con MAUI.

## Trazabilidad

- `TR-002`, `TR-007`: persistencia y sincronización offline-first.
- `TR-010`: sincronización en tiempo real mediante SignalR.
- `TR-011`: filosofía HPHMI.
- `DT-ARQ-CMP-001`: cliente frontend y componentes.
- `DT-ARQ-DEP-001`: nodos móvil y administrativo.
- `DT-ARQ-TECH-001`: matriz consolidada del stack.

## Estado de decisiones anteriores

Las versiones anteriores de los modelos pudieron representar el cliente con tecnologías frontend diferentes. Esas referencias son históricas y no forman parte del stack objetivo vigente. Los artefactos actuales deben referenciar .NET MAUI Blazor Hybrid.
