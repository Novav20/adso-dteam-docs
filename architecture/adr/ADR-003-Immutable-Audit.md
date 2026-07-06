---
date: 2026-07-06
status: Aceptado
author: Juan David Julio Serrano
linked_to: ADM-032 — Sistema de Auditoría Inmutable (Auditoría Trail)
---

# ADR 003: Arquitectura de Auditoría Inmutable mediante Hash Encadenado (Tamper-Evident Logging)

## Contexto
El requisito FR-347 (Historia ADM-032) exige que el rastro de auditoría opere bajo políticas de inmutabilidad técnica para cumplir con ISO 55001 e ISO 27001. En un entorno de producción ideal, esto se logra utilizando bases de datos tipo Ledger (ej. Amazon QLDB) o almacenamiento WORM (Write Once Read Many). 
Para el alcance del MVP y despliegues On-Premise con bases de datos relacionales tradicionales (PostgreSQL/MySQL), un administrador de base de datos (DBA) con acceso Root podría, en teoría, ejecutar sentencias `UPDATE` o `DELETE` directamente en consola, vulnerando la inmutabilidad de la capa de aplicación.

## Decisión
En lugar de implementar una infraestructura Ledger costosa para el MVP, se implementará un enfoque de **Registro Evidente de Manipulación (Tamper-Evident Logging)** utilizando criptografía a nivel de aplicación.

1. **Restricción de Privilegios (DBA):** El usuario de base de datos utilizado por la API de DTEAM tendrá privilegios estrictamente de `INSERT` y `SELECT` sobre la tabla de auditoría. Los comandos `UPDATE` y `DELETE` serán denegados a nivel de motor de base de datos.
2. **Cadena Criptográfica (Blockchain-like):** Cada registro insertado en la tabla de auditoría calculará un hash (SHA-256) que concatenará los datos de la transacción actual con el **hash del registro inmediatamente anterior**.
3. **Validación de Integridad:** Un servicio en segundo plano (Cron Job) recalculará periódicamente la cadena de hashes. 

## Consecuencias

### Positivas
*   **Cumplimiento Normativo:** Satisface los controles de integridad de ISO 27001 sin incurrir en costos de infraestructura especializada.
*   **Detección de Intrusiones:** Si un atacante o DBA malicioso altera un registro directamente en la base de datos, el hash de ese registro cambiará, invalidando toda la cadena subsiguiente y disparando una alerta crítica inmediata.

### Negativas / Deuda Técnica
*   No previene que un usuario con acceso físico al servidor elimine la tabla completa (Drop Table), aunque sí garantiza que ninguna manipulación sutil pase desapercibida.
*   El cálculo del hash añade una ligera sobrecarga computacional (microsegundos) a las operaciones críticas, lo cual es asumible bajo los SLAs actuales.