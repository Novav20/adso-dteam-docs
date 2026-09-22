---
code: DT-ARQ-DB-DOC-001
version: 1.0
date: 2026-09-10
status: Vigente
author: Juan David Julio Serrano
standard:
  - ISO/IEC 42010:2011 (Arquitectura de Software)
  - PostgreSQL 18.x Documentation
  - ISO 14224:2016 / ISO 55001:2014
---

# Especificación Técnica de Persistencia y Directrices SQL

## 1. Alcance y Propósito
Este documento consolida las directrices técnicas, restricciones físicas y patrones de consulta SQL obligatorios para el motor PostgreSQL 18 en DTEAM. Actúa como el contrato de persistencia para el desarrollo de migraciones en Entity Framework Core y scripts DDL/DML.

---

## 2. Invariantes de Integridad Física y Restricciones

| Regla / Elemento             | Decisión de Implementación                                                                      | Justificación Técnica / Norma                                                                                                                                                                                                                                                                                                        |
| :--------------------------- | :---------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Identificadores PK**       | `UUID DEFAULT uuidv7()`                                                                         | Identificadores secuenciales en el tiempo que evitan la fragmentación de páginas B-Tree en inserciones masivas de telemetría y auditoría.                                                                                                                                                                                            |
| **Indexación de FKs**        | `CREATE INDEX` obligatorio en cada columna de clave foránea.                                    | PostgreSQL **no** indexa automáticamente las FK en tablas hijas. Previene *Full Table Scans* durante eliminaciones o actualizaciones del padre.                                                                                                                                                                                      |
| **Borrado de Activos**       | `ON DELETE RESTRICT` en relaciones con `work_orders`.                                           | **ISO 14224 / ISO 55001:** Prohibición estricta de borrado en cascada sobre órdenes de trabajo e historial de fallas. Los activos se retiran lógicamente (`Decommission`).                                                                                                                                                           |
| **Gestión de Spares**        | Conservar comportamiento estándar `NULLS DISTINCT` en `equipment_units.functional_location_id`. | Permite que múltiples unidades de equipo en almacén (`IN_STORAGE`) tengan valor `NULL` simultáneamente sin violar la unicidad de slot en planta (Principio de Pauli).                                                                                                                                                                |
| **Precisión Numérica**       | `DECIMAL(18,6)` estricto en sensores y `DECIMAL(12,2)` en costos.                               | Prohibición de `DOUBLE PRECISION` / `FLOAT` para evitar errores de redondeo IEEE 754 en la validación determinística de Energía Cero (LOTO).                                                                                                                                                                                         |
| **Esquemas DDD**             | Segregación en 5 esquemas: `tax`, `mtto`, `inv`, `vis`, `adm`.                                  | Aislamiento por *Bounded Context*, eliminación de prefijos en tablas y soporte de defensa en profundidad mediante privilegios `GRANT/REVOKE`.                                                                                                                                                                                        |
| **Indexación Operativa**     | `CREATE INDEX ... WHERE ...` (Parciales)                                                        | Para optimizar el rendimiento de las consultas en el Tablero de Backlog y validaciones LOTO sin saturar la RAM, se exige el uso de **Índices Parciales** sobre registros activos. Se excluyen los registros en estados terminales (ej. `CLOSED`, `COMPLETE`) del árbol B-Tree del índice activo.                                     |
| **Vocabularios Controlados** | `CHECK (col IN (...))` en MVP con ruta de evolución a *Lookup Tables*.                          | En el MVP se utilizan restricciones `CHECK` mapeadas a `enum` de C# para maximizar el rendimiento y evitar JOINs innecesarios. En fases posteriores que requieran parametrización dinámica desde la UI (sin despliegues de código), se migrarán a tablas de catálogo dedicadas administradas por Entity Framework Core (`SeedData`). |

## 3. Directrices de Consulta y Rendimiento DML

### 3.1. Patrón `LEFT JOIN LATERAL` para Última Telemetría ([[VIS-033]])
Para recuperar la última lectura de sensor de cada equipo sin incurrir en agregaciones costosas (`MAX`) sobre tablas de series de tiempo masivas, las consultas de lienzo deben utilizar subconsultas correlacionadas `LATERAL`:

```sql
SELECT a.tag_number, tel.value AS current_vibration, tel.timestamp
FROM tax.equipment_units a
LEFT JOIN LATERAL (
    SELECT s.value, s.timestamp
    FROM vis.telemetry_signals s
    WHERE s.equipment_unit_id = a.id
    ORDER BY s.timestamp DESC
    LIMIT 1
) tel ON TRUE;
```

### 3.2. Agregaciones Condicionales con Cláusula `FILTER` ([[MTTO-026]], [[INV-006]])
Para métricas consolidadas en una sola lectura de tabla, se prohíbe el uso de `SUM(CASE ...)` en favor de la cláusula estándar `FILTER (WHERE ...)`:

```sql
-- Ejemplo: Consolidación de Backlog RIME por bandas de severidad en una sola pasada
SELECT 
    COUNT(*) AS total_solicitudes,
    COUNT(*) FILTER (WHERE priority_score >= 80) AS do_first_emergencia,
    COUNT(*) FILTER (WHERE priority_score BETWEEN 50 AND 79) AS schedule_alta
FROM mtto.backlog_items;
```

### 3.3. Prohibición de `NOT IN` con Subconsultas
Para prevenir que la presencia de un valor `NULL` invalide todo el resultado por lógica trivalente (3VL), se prohíbe `NOT IN (SELECT ...)` en consultas de dominio. Se debe utilizar exclusivamente:
* `NOT EXISTS (SELECT 1 FROM ... WHERE ...)`
* `LEFT JOIN ... WHERE <tabla_derecha>.id IS NULL`

### 3.4. Evaluación Segura en Cláusulas `WHERE`
Debido a que PostgreSQL no garantiza cortocircuito estricto de izquierda a derecha en el `WHERE`, cualquier cálculo propenso a división por cero o error aritmético debe encapsularse en una expresión `CASE WHEN <divisor> != 0 THEN ... ELSE NULL END`.

### 3.5. Resolución de Jerarquías ISO 14224 ([[INV-027]])
Para la navegación y validación del árbol de activos (Ubicaciones Funcionales L1-L5), el modelo relacional implementa un patrón de Lista de Adyacencia (`parent_id`). Las consultas que requieran reconstruir la ruta del activo (breadcrumbs) o validar ciclos de re-parenting deben implementarse utilizando **CTEs Recursivos (`WITH RECURSIVE`)**. Se prohíbe la carga en memoria de toda la tabla para armar el árbol en la capa de aplicación (.NET).

### 3.6. Ingesta Idempotente para Colas Offline ([[TR-007]])
Para garantizar la resiliencia en la sincronización desde clientes móviles, las operaciones de escritura diferida (ej. cierre de órdenes o registro de telemetría) que ingresen a través del `Background Sync Worker` deben ejecutarse como operaciones *Upsert* atómicas. Se utilizará la cláusula nativa **`INSERT ... ON CONFLICT (id) DO UPDATE`** para prevenir excepciones de llaves duplicadas si la red móvil retransmite el mismo paquete de datos.

### 3.7. Bloqueos Pesimistas para Aislamiento LOTO ([[VIS-011]], [[DT-ARQ-ASR-001#2. Seguridad LOTO en Tiempo Real y Falla Segura|ASR-2]])
Para garantizar el cumplimiento de la norma de Energía Cero (Falla Segura), la validación de inicio de órdenes de trabajo críticas no debe utilizar lecturas sucias ni control optimista exclusivo. El servicio de dominio debe ejecutar la validación de estados de energía envolviendo las consultas en bloqueos explícitos y no bloqueantes de base de datos (`SELECT ... FOR UPDATE NOWAIT`). Si la fila se encuentra bloqueada por el proceso asíncrono de inyección de telemetría IoT, la transacción debe abortar inmediatamente devolviendo un estado de "Seguridad Indeterminada" al usuario, evitando que el hilo se congele (prevenir thread pool starvation).

### 3.8. Indexación GIN para Auditoría Inmutable JSONB ([[ADM-032]])
Para garantizar búsquedas eficientes sobre el rastro de auditoría masivo, las columnas `previous_state` y `new_state` (tipo `JSONB`) de la tabla `adm.audit_logs` deben indexarse utilizando la clase de operador **`jsonb_path_ops`** (Índice GIN). Las consultas de búsqueda histórica desde la aplicación .NET se deben implementar utilizando el operador de contención nativo (`@>`) para aprovechar la optimización de la estructura de rutas (hash paths).