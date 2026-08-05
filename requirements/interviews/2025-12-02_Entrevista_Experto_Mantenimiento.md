# 2025-12-02_Entrevista_Experto_Mantenimiento

- Fecha: 02 de diciembre de 2025 (Contexto)
- Participantes:
  - **Juan David** (Entrevistador)
  - **Ingeniero** (Entrevistado – Gerente/Ingeniero de Mantenimiento y Proyectos)

[INICIO DE LA GRABACIÓN]

**Juan David:**
Ya estamos. Le comento las preguntas para no hacerlo perder tiempo. Primero, quiero confirmar: su cargo es Ingeniero de Mantenimiento y Proyectos, y el sector en el que está actualmente se puede catalogar como Oil & Gas y almacenamiento, ¿cierto?

**Ingeniero:**
Así es.

**Juan David:**
La primera pregunta está relacionada con diagnosticar el proceso actual de cómo manejan el mantenimiento y los principales dolores. Quiero que describa el flujo ideal versus el real desde que un operador detecta una falla hasta que el técnico llega al sitio. Es decir, se dañó algún equipo de la planta y se debe comunicar ese fallo hasta el punto donde el técnico llega a planta. Describa los procesos intermedios. Por ejemplo, ¿dónde se pierde más tiempo o información en ese flujo?

**Ingeniero:**
Mira, todos los activos de la terminal están en el software *Infor EAM*. ¿Cómo funcionamos? Cuando un equipo presenta una falla o avería, operaciones hace un reporte formal y se genera una orden de trabajo o un requerimiento para el área de mantenimiento. Todo activo tiene su hoja de vida y trazabilidad. Dependiendo de las fallas y de las órdenes que conlleve la reparación, se genera la solicitud; a eso se le hace una orden de trabajo y tenemos un tiempo de respuesta.

Para eso, dependiendo de la empresa, hay un criterio de criticidad. Se define la criticidad del equipo. Puede ser una urgencia, o que se pueda esperar una semana, un mes, o que no sea crítico. Eso se consigna en la solicitud y llega a la plataforma. Tenemos un Planner (Planner y Programador) que revisa la actividad y, desde ahí, delegamos la reparación. Todo esto tiene una línea de tiempo; la idea es que sea rápido, porque dependiendo del equipo hay que dar una solución pronta para no afectar la disponibilidad en la operación.

**Juan David:**
Listo. Segunda pregunta, relacionada con contratistas externos: cuando se cierra una orden de trabajo, ¿cómo registran hoy el cierre de las órdenes? ¿Usan papel, tablets o lo completan al final del turno?

**Ingeniero:**
Todo equipo tiene una taxonomía y una frecuencia de mantenimiento establecida. Por ejemplo, una bomba en la terminal tiene dos tipos de mantenimiento. *Infor EAM* nos avisa: “Para tal fecha está programada la actividad de mantenimiento tipo A o tipo B”. Programamos al proveedor; él viene y ejecuta. Generamos el permiso. Al terminar, el proveedor genera un reporte en su formato y nos lo envía digital. Luego, el Planner toma la información, la sube a la carpeta, revisamos el reporte y después lo subimos al sistema. Todo esto es manual: hay una persona que hace esa “interfaz”, busca el número de la orden y la sube a *Infor EAM*.

**Juan David:**
Tercera pregunta. Desde su rol de supervisor, ¿cuál es el mayor cuello de botella administrativo que impide cerrar una reparación urgente lo más rápido posible? Por ejemplo, permisos de trabajo o recolección de firmas.

**Ingeniero:**
Para quienes están en supervisión e ingeniería, siempre hay un tema documental que consume tiempo y desgasta el proceso, dependiendo de cómo lo maneje cada empresa. Hay que generar documentación: crear la orden, luego el requerimiento, la orden de compra, después el informe, revisarlo y subirlo al sistema. Eso implica tiempo y, si algún paso no se cumple, se pierde información y la orden queda incompleta, generando reprocesos. La ejecución es rápida; solucionas la bomba. Luego queda la parte documental para mantener la trazabilidad y permitir el análisis de información a futuro, para que el equipo no repita la falla. Es importante, pero termina siendo el cuello de botella.

**Juan David:**
Cuando un técnico está frente a una bomba o a un equipo y necesita revisar el plano o el manual del fabricante en campo, ¿qué tan fácil es acceder a esa información? ¿La tiene físicamente, de forma digital, o debe volver a la oficina?

**Ingeniero:**
Depende de cómo esté establecida la taxonomía de equipos y la digitalización de la información. Si estás en campo y requieres información, en muchas empresas está en documentos, en un PC, en un *Drive*, o en *Infor EAM*; pero en sitio no siempre se puede revisar. En algunas empresas hay tablets con comunicación directa a *Infor EAM*, para revisar en tiempo real, pero son pocas. Es algo más de *Industria 4.0*. La mayoría maneja la información centralizada en PCs o en la nube y hay que ir al escritorio a revisar, lo que implica tiempos de ida y vuelta.

**Juan David:**
¿Cree que la tendencia es tener esa información menos centralizada en el PC y más disponible de forma multiplataforma (por ejemplo, en una tablet en campo)?

**Ingeniero:**
Sí. La idea es ahorrar tiempo. Hay cuellos de botella por desplazamientos para consultar información. En algunas empresas ya usan códigos QR en los equipos; el técnico escanea con su tablet y ve la hoja de vida y la información. Pero son pocas por costos y por la madurez de la migración tecnológica. Aún prevalece el mantenimiento preventivo/correctivo tradicional. La tendencia es llegar a esas soluciones.

**Juan David:**
Usted menciona que implementa ISO 14224 (manejo de datos de falla). ¿Cómo manejan hoy la actualización de la hoja de vida del equipo? Ya explicó el flujo, pero, específicamente, ¿tienen buena integridad de datos históricos para análisis de confiabilidad?

**Ingeniero:**
La ISO 14224 se enfoca en pilares como la taxonomía de equipos y subequipos: llegar desde el equipo al despiece hasta la última pieza. Tener la data para decir: “En una bomba, tengo la referencia del impeler, la marca, etc.”, incluso hasta el tornillo o el motor eléctrico. En la terminal, *Infor EAM* también se enfoca en la ISO 14224. Subdividimos los equipos hasta el nivel que nos interesa para la data. La idea es crear divisiones para tener más información al hacer análisis causa-raíz, motivos de falla u otras implementaciones de confiabilidad.

**Juan David:**
Si en un futuro tuvieran un gemelo digital de la planta, ¿le vería valor a acceder en campo a un modelo 3D con despiece de componentes para ubicar partes, saber por dónde comenzar y ver la taxonomía relevante? ¿Sería útil en una aplicación de gemelo digital 3D?

**Ingeniero:**
Desde 2018 escuché del gemelo digital, especialmente a *Rockwell Automation*. Tienen una propuesta interesante. Estuve en capacitaciones de gemelo digital y 3D para implementarlo en una planta de proceso, orientado a ver el proceso en tiempo real y a *OEE* (eficiencia global de equipos), analizando fallas. De ahí a hoy lo he escuchado poco, salvo por tu comentario. Me parece interesante: toda herramienta que flexibilice el trabajo de ingeniería es bienvenida, incluyendo las *TIC*. Sería práctico.

**Juan David:**
Para calcular *KPI* como tiempo medio entre fallas (*MTBF*) o tiempo medio para reparar (*MTTR*) en un activo crítico, ¿el sistema lo entrega automáticamente o deben descargar datos a Excel y calcular?

**Ingeniero:**
*Infor EAM* tiene opción de analizar *MTTR* y *MTBF* y da ese cálculo, siempre y cuando se alimente la información de fallas. Si no se registran los fallos, no puede calcular. Pero la opción existe.

**Juan David:**
Sobre gestión de repuestos: ¿cómo es la comunicación con el almacén? Según recuerdo, no hay un almacenista como tal en la terminal. ¿Existe un sistema que avise stock para urgencias o debe consultarse con el Planner?

**Ingeniero:**
No hay un almacén como tal; mantenerlo es costoso. Hemos trabajado en identificar equipos críticos y los repuestos que debemos tener como críticos en la terminal. Por ejemplo, en la báscula hay dos repuestos críticos que debemos tener por si se presenta una falla. Es complejo que una empresa tenga un almacén lleno de repuestos para todo. La clave es el análisis de criticidad para definir repuestos de emergencia. Lo venimos trabajando con el Planner: ya identificamos la báscula, algunos componentes de bombas y otros repuestos de emergencia que debemos tener para resolver contingencias.

**Juan David:**
Última pregunta, más abierta: si pudiera pedir una funcionalidad “mágica” a un software de mantenimiento que hoy no existe, ¿cuál sería? Algo que realmente usaría y compraría.

**Ingeniero:**
Estoy alineado con el *PMO* (plan de optimización de equipos y plan de mantenimiento). Subimos información constantemente; sería interesante que el software sugiriera: “Para el próximo año, mejora con estos equipos”. Muchos reportes dicen que “se encuentra bien”, y puede haber mantenimientos redundantes que no se requieren. Todo mantenimiento preventivo tiene costo. Buscamos disponibilidad y confiabilidad con ahorro en costos. Esa optimización hoy la hacemos las personas. Ojalá el software lo hiciera y dijera: “En estos activos hay oportunidades de mejora”. Luego nosotros validamos y aplicamos. Sería interesante.

**Juan David:**
Como un asistente para optimización en mantenimiento que da un preliminar y usted lo valida.

**Ingeniero:**
Exacto.

**Juan David:**
Eso sería todo por ahora. Muchas gracias por el tiempo. En aproximadamente un año y medio, en fase de ejecución, le muestro el prototipo.

**Ingeniero:**
Dale, Juan David. Cualquier cosa me avisas. Un gusto saludarte.

**Juan David:**
Igualmente. Saludos por allá.

**Ingeniero:**
Igualmente. Chao.

[FIN DE LA GRABACIÓN]
