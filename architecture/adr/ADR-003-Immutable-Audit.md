---
id: ADR-003
title: "Arquitectura de Auditoría Inmutable mediante Hash Encadenado"
date: 2026-07-06
status: Accepted
author: Juan David Julio Serrano
deciders: Arquitecto de Software
linked_to:
  - "[[ADM-032]]"
  - "[[UC-ADM-032]]"
  - "[[TR-001]]"
---

# ADR-003: Arquitectura de Auditoría Inmutable mediante Hash Encadenado

## Contexto
El cumplimiento de la norma ISO 27001 y la trazabilidad de la ISO 55001 exigen que los registros de auditoría no puedan ser alterados. En bases de datos relacionales estándar, un administrador con acceso físico o credenciales superiores puede alterar o eliminar registros, afectando la trazabilidad de la aplicación. Adoptar bases de datos especializadas de registro inmutable introduce costos operativos elevados para la fase MVP.

## Decisión
Se implementa una arquitectura de **Registro Evidente de Manipulación** estructurada en dos capas:

1. **Seguridad a Nivel de Fila en PostgreSQL:** Se configuran las tablas de auditoría con políticas de solo adición. Se deniegan explícitamente los comandos de actualización y eliminación para el usuario de conexión del ORM.
2. **Encadenamiento Criptográfico en la Capa de Aplicación:** Al insertar, el backend calcula un hash que concatena la carga útil actual con el hash de integridad de la transacción inmediatamente anterior.
3. **Meta-Auditoría:** La lectura de registros verifica dinámicamente la cadena y alerta al auditor en caso de discrepancias matemáticas.

## Alternativas Consideradas
* **Bases de datos en la nube especializadas en contabilidad inmutable:** Rechazado por generar dependencia de proveedor y sobrecostos operativos para un MVP.
* **Disparadores y tablas de historial en el motor SQL:** Rechazado. Un disparador puede ser deshabilitado por un atacante con acceso a la base de datos sin dejar un rastro criptográfico evidente.

## Consecuencias

### Positivas
* Asegura el no repudio y detecta alteraciones externas en la base de datos sin herramientas de terceros.
* Almacenamiento eficiente de los estados previo y posterior gracias al uso del formato binario JSON.

### Negativas
* Mayor latencia en escrituras debido al cálculo algorítmico del hash.
* Dificultad para purgar registros individuales por regulaciones de protección de datos sin romper la validación de la cadena.

### Riesgos y Deuda Técnica
* El mecanismo no previene la eliminación completa de la tabla. La protección contra destrucción total recae en las políticas de retención de respaldos a nivel de infraestructura.