---
id: ADR-004
title: "Cliente Frontend unificado con .NET MAUI Blazor Hybrid y Blazor Web"
date: 2026-08-25
status: Accepted
author: Juan David Julio Serrano
deciders: Arquitecto de Software
supersedes: ADRs y diseños que indicaban React Web, React Native y WatermelonDB
linked_to:
  - DT-ARQ-CMP-001
  - DT-ARQ-DEP-001
  - DT-ARQ-TECH-001
---

# ADR-004: Cliente Frontend unificado con .NET MAUI Blazor Hybrid y Blazor Web

## Contexto
El sistema requiere un cliente móvil robusto para la ejecución en campo con soporte para operación sin conexión y un portal web administrativo. Mantener dos ecosistemas separados impone una carga de mantenimiento alta para un único desarrollador, requiriendo la gestión de múltiples gestores de paquetes, duplicación de modelos de transferencia de datos y traducción constante de la lógica de negocio.

## Decisión
Se unifica la pila de tecnologías del frontend bajo el ecosistema .NET utilizando una topología de entorno dual y una librería de clases Razor compartida:

1. **Cliente Web Administrativo:** Aplicación web Blazor.
2. **Cliente Móvil de Campo:** .NET MAUI Blazor Hybrid.
3. **Librería de Componentes:** Las interfaces de alto desempeño, formularios ISO 14224 y lógica de estado se desarrollarán una única vez en un proyecto compartido.
4. **Persistencia Móvil:** Se empleará la librería `sqlite-net-pcl` integrada con cifrado SQLCipher. Se descarta Entity Framework Core en el cliente móvil para evitar penalizaciones de arranque en frío por uso de reflexión y conflictos con el compilador nativo en iOS.

## Alternativas Consideradas
* **Aplicación web React más React Native y WatermelonDB:** Rechazado. Genera fragmentación de lenguajes, fricción en la generación de clientes de interfaz de programación y sobrecarga de mantenimiento por dependencias inestables.
* **Entity Framework Core sobre SQLite para persistencia móvil:** Rechazado. Causa alto consumo de memoria y latencia al inicializar el contexto de base de datos en hardware industrial de bajas especificaciones.

## Consecuencias

### Positivas
* Mayor eficiencia de desarrollo: los modelos de dominio, validaciones y cálculos fluyen desde el backend hasta el frontend sin duplicación de código.
* La librería seleccionada para SQLite permite inserciones transaccionales rápidas sin la carga del rastreador de cambios de un ORM pesado, protegiendo el hilo de seguridad LOTO.

### Negativas
* Mayor peso del binario final en aplicaciones móviles debido a la inclusión del tiempo de ejecución nativo de .NET.
* La sincronización requerirá el diseño manual de una tabla de cola de mutaciones sin conexión, prescindiendo de los sincronizadores automáticos de otras herramientas.

### Riesgos y Deuda Técnica
* El rendimiento de la interacción en listas extensas puede disminuir debido a la renderización dentro de un visor web en lugar de utilizar componentes puramente nativos. Requiere paginación estricta y virtualización de componentes en la interfaz.