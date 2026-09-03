---
code: DT-ARQ-PAT-DOC-001
version: 1.0
date: 2026-08-05
status: Especificación de Patrones de Diseño Arquitectónicos y de Código
author: Juan David Julio Serrano
standard:
  - GoF (Gang of Four Design Patterns)
  - Domain-Driven Design (DDD)
  - Clean Architecture / Hexagonal Architecture
---

# Catálogo de Patrones de Diseño en la Solución DTEAM

## 1. Patrones Creacionales

### Factory Method (Método de Fábrica)
* **Ubicación:** Raíz de agregado `MaintenancePlan` (`GenerateWorkOrder()`).
* **Propósito:** Centraliza la instanciación de la entidad `WorkOrder` de mantenimiento preventivo. El plan de mantenimiento encapsula todas las reglas e invariantes necesarias (clase de trabajo, criticidad del activo, estimación de Wrench Time e inherencia de puntos LOTO), evitando que la capa de aplicación cree órdenes incompletas.

---

## 2. Patrones Estructurales

### Adapter (Adaptador)
* **Ubicación:** Periferia de la capa de infraestructura (Puertos Secundarios). Ejemplos: `EFCorePostgresAdapter`, `SignalRBroadcaster`.
* **Propósito:** Aplica el principio de inversión de dependencia (DIP). El núcleo del dominio define interfaces abstractas (puertos). La infraestructura implementa los adaptadores concretos, permitiendo cambiar motores de base de datos o conectores de red sin alterar las reglas de negocio de ISO 14224.

### Composite (Objeto Compuesto)
* **Ubicación:** Entidad `FunctionalLocation`.
* **Propósito:** Permite tratar tanto a las ubicaciones individuales (hojas del árbol) como a las agrupadoras (ramas del árbol) bajo una misma interfaz jerárquica de 9 niveles (ISO 14224). Simplifica operaciones de navegación recursiva y validaciones de prevención de ciclos (`ReorganizeTree`).

---

## 3. Patrones de Comportamiento

### Strategy (Estrategia)
* **Ubicación:** Contrato `IRimeCalculator` e implementación `RimeCalculatorService` ([[ADR-002-RIME-MVP-Static-Factors|ADR-002]]).
* **Propósito:** Encapsula el algoritmo de priorización RIME. Permite reemplazar o extender en el futuro el cálculo por uno basado en riesgo financiero o disponibilidad de inventario sin modificar la entidad `WorkRequest` ni las reglas del agregador.

### State (Estado)
* **Ubicación:** Flujo de ejecución de la orden de trabajo (`WorkOrder.currentStatus`).
* **Propósito:** Encapsula las transiciones de estado (`PLANNING` $\to$ `WAITING_PARTS` $\to$ `SCHEDULED` $\to$ `IN_PROGRESS` $\to$ `COMPLETE` $\to$ `CLOSED`). Encapsula precondiciones de seguridad (como bloquear `IN_PROGRESS` si LOTO o PTW no están verificados) dentro de clases de estado dedicadas, eliminando `switch/if-else` anidados.

### Observer (Observador)
* **Ubicación:** Monitoreo reactivo de Energía Cero (`IsolationPoint` como sujeto, `WorkOrder` como observador).
* **Propósito:** Si el adaptador IoT detecta energía activa durante la ejecución de un mantenimiento, el sujeto notifica al observador, invocando de inmediato `SuspendExecution()` sobre la orden de trabajo para proteger al operario.

### Mediator (Mediador / Despachador Nativo)
* **Ubicación:** Puerto `IEventBus` e implementación `Native Event Dispatcher`.
* **Propósito:** Desacopla la comunicación asíncrona inter-módulo. Permite que el módulo de Mantenimiento (`MTTO`) emita el evento `WorkOrderStatusChanged` y el módulo de Inventario (`INV`) lo capture para ejecutar `RecordConsumption` sin compartir dependencias directas en tiempo de ejecución.