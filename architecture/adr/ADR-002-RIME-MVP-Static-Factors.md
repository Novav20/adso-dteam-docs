---
Fecha: 2026-05-14
Estatus: Aceptado
Relacionado con: MTTO-026 — Gestión de Backlog mediante Priorización Objetiva (RIME)
---

# ADR 002: Implementación RIME con Factores Estáticos Configurables para MVP

## Contexto

La historia MTTO-026 define un motor de priorización objetiva RIME (Riesgo, Impacto, Mantenibilidad, Economía) que asigna automáticamente un puntaje a cada solicitud de trabajo del backlog. La implementación completa del motor requiere cruzar datos en tiempo real con otros módulos del sistema:

- **Factor R (Riesgo):** Depende del historial de fallos ISO 14224 y la criticidad configurada del activo (INV-005).
- **Factor I (Impacto):** Requiere cruzar con costos de tiempo de inactividad definidos por la planta (INV-006, datos financieros).
- **Factor M (Mantenibilidad):** Necesita consultar el stock disponible de repuestos en tiempo real (INV-031 — Catálogo de Repuestos).
- **Factor E (Economía):** Requiere la lista de materiales de la OT cruzada con precios de inventario y tasas de mano de obra.

Estas dependencias crean un riesgo de bloqueo secuencial en la AP6: si se optara por la implementación automática desde el inicio, el motor RIME no sería funcional hasta que el módulo de Inventario (INV) esté totalmente terminado y poblado con datos, impidiendo pruebas tempranas de la gestión de backlog.

---

## Decisión

Para el MVP, los factores RIME serán implementados mediante **selectores configurables** que el planificador define al crear o revisar una solicitud de trabajo. Los pesos de cada nivel serán parametrizados por la administración del sistema.

### Modelo de datos MVP

| Factor | Opciones del selector | Peso (configurable) |
|---|---|---|
| **Riesgo (R)** | Crítico / Mayor / Menor | 3 / 2 / 1 |
| **Impacto (I)** | Alto / Medio / Bajo | 3 / 2 / 1 |
| **Mantenibilidad (M)** | Compleja / Moderada / Simple | 3 / 2 / 1 |
| **Economía (E)** | > $5M / $1M–$5M / < $1M | 3 / 2 / 1 |

**Fórmula:** `Score_RIME = R × I × M × E` → Rango: 1–81

El puntaje resultante es objetivo, reproducible y auditable. Solo difiere de la versión final en que el dato de entrada es ingresado por el planificador en lugar de ser calculado automáticamente desde inventario.

---

## Patrón Arquitectónico: Strategy Pattern

Para garantizar que la transición de MVP → Versión 2.0 sea un **intercambio quirúrgico sin reescribir lógica de negocio**, se adoptará el **Strategy Pattern** en la capa de servicios del backend.

### Estructura

```
IRimeCalculator (Interfaz / Contrato)
    └── calculate(requestId: string): RimeScore
    └── getFactorBreakdown(requestId: string): RimeFactors

ManualRimeCalculator (Implementación MVP)
    └── Lee los 4 selectores del formulario de la OT
    └── Multiplica los pesos configurados en la tabla system_config

AutomaticRimeCalculator (Implementación v2.0 — Deuda Técnica)
    └── Consulta INV para stock de repuestos (Factor M)
    └── Consulta historial ISO 14224 del activo (Factor R)
    └── Cruza con tabla de costos de downtime (Factor I)
    └── Calcula costo de materiales y mano de obra (Factor E)
```

### Por qué funciona el intercambio

La historia MTTO-026 solo interactúa con `IRimeCalculator`. El tablero de backlog, el criterio de aceptación *"el sistema calcula y presenta el puntaje"* y los reportes de auditoría nunca saben cuál implementación está activa. Para pasar de MVP a v2.0 basta con:

1. Implementar `AutomaticRimeCalculator`.
2. Cambiar el registro en el contenedor de inyección de dependencias.
3. No tocar ninguna vista, ningún controlador, ningún test de negocio.

### Diagrama de dependencias

```
WorkOrderController
        │
        ▼
  RimeService (usa IRimeCalculator)
        │
        ├─── [MVP]  ManualRimeCalculator
        │               └── Lee OT.riskLevel, OT.impactLevel, etc.
        │
        └─── [v2.0] AutomaticRimeCalculator
                        ├── InventoryRepository
                        ├── FailureHistoryRepository
                        └── CostMatrixRepository
```

---

## Consecuencias

### Positivas
- El MVP se puede entregar aunque los módulos INV no estén finalizados.
- El puntaje sigue siendo objetivo y reproducible (misma entrada → mismo score).
- El contrato `IRimeCalculator` fuerza coherencia entre ambas implementaciones.
- El intercambio a la versión automática no requiere refactoring de negocio.

### Negativas
- La precisión del score depende del criterio del planificador, no de datos duros de inventario.
- Existe riesgo de sesgo humano en la selección de los factores.

### Deuda técnica registrada
- `AutomaticRimeCalculator` queda pendiente hasta que `INV-031` (Catálogo de Repuestos) e `INV-006` (Movimientos de Inventario) estén operativos.
- Se recomienda una validación de campo (comparar scores manuales vs. automáticos en un lote de OTs reales) antes de activar `AutomaticRimeCalculator` en producción.

---

## Referencias

- ISO 55001:2014, Cláusula 6.2.2.1 — *"A risk ranking process can determine which assets have a significant potential to impact on the achievement of the asset management objectives"* (fuente: Cápsula ISO-55000, Risk Planning and Decision Making).
- Wireman, T. (Vol 4) — Cap. 3: *Work Order Priority Rating* como campo esencial del motor CMMS (fuente: Cápsula Wireman Vol4, The Core CMMS Engine).
- Gang of Four — *Design Patterns: Elements of Reusable Object-Oriented Software* (1994), Strategy Pattern, pp. 315–323.
