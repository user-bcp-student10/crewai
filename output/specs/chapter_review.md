# Revisión final — H-AUTH-04

## Resumen

**Veredicto: RECHAZADO.** Las entregas disponibles no contienen una implementación de backend: Backend declara el trabajo bloqueado y no aporta cambios de código. El frontend presenta un armazón no integrado. No se adjuntan resultados reales de pruebas y no se proporcionó el contrato aprobado del endpoint de login ni el Issue completo.

Por tanto, no hay evidencia de que las respuestas de login hayan dejado de reflejar datos de entrada o de exponer detalles internos. Los criterios de esta revisión se derivan del título y de las propuestas de los entregables; no sustituyen los criterios oficiales, que no fueron proporcionados. No se confirma una vulnerabilidad explotable ni una incompatibilidad efectiva entre capas, pero tampoco es posible verificarlas.

## Matriz de criterios

*Los criterios siguientes son derivados del título y de las entregas; la lista oficial del Issue no está disponible.*

| Criterio | Estado | Evidencia |
|---|---|---|
| Las respuestas de login no reproducen valores de entrada no autorizados, tanto en éxito como en error. | **Sin cubrir** | Arquitectura propone construir respuestas desde campos públicos permitidos; Backend declara que no implementó cambios. El informe de pruebas registra T01/T02 como no ejecutadas y sin contrato ni endpoint. |
| Las respuestas no exponen excepciones, stack traces ni detalles internos. | **Sin cubrir** | Arquitectura recomienda traducir los errores antes de responder, pero Backend no aporta implementación. Pruebas T05/T07 no ejecutadas. |
| El éxito conserva el contrato público aprobado, excluyendo eco o detalles internos. | **Sin cubrir** | No se proporcionó el contrato de éxito. Backend no implementó cambios; Testing indica que T01/T06 están pendientes. |
| Los errores mantienen el formato público aprobado y no incluyen valores de entrada ni detalles internos. | **Sin cubrir** | No hay contrato de errores aprobado. Los códigos y mensajes de Arquitectura son candidatos; Testing T02/T03/T05/T07 está pendiente. |
| La interfaz no presenta al usuario el cuerpo técnico crudo de errores. | **Parcial** | `frontend_spec.md` propone mensajes genéricos y no mostrar el cuerpo crudo, pero declara que el armazón no está integrado. T08 no fue ejecutada. |
| La validación y los casos límite siguen el contrato sin reflejar datos no permitidos. | **Sin cubrir** | No se proporcionaron esquema ni reglas. Backend no confirma validación; Testing T03/T04 no se ejecutaron y no tienen resultados esperados contractuales. |

## Hallazgos

### H1 — La protección principal de la feature no está implementada ni verificada
**Severidad: Media.**  
**Ubicación:** Backend (`backend_spec.md`, estado e implementación); pruebas (`testing_report.md`, T01–T07); seguridad (`Informe de seguridad`, SEC-H-AUTH-04-01).

Backend declara expresamente que no realizó cambios. Las pruebas no incluyen resultados reales, y Seguridad identifica una brecha de verificación, no una vulnerabilidad confirmada. Así, no hay evidencia de que el endpoint elimine el eco de entrada o los detalles internos.

**Corrección concreta:** con el código y contrato reales, implementar en el adaptador HTTP respuestas construidas mediante una lista explícita de campos públicos y traducir errores internos al formato aprobado. Añadir pruebas para éxito, rechazo, validación y fallo interno controlado, usando centinelas sintéticos y comprobando tanto la ausencia de filtraciones como la conformidad del estado y payload.

### H2 — Contrato de API ausente; coherencia entre capas no verificable
**Severidad: Media.**  
**Ubicación:** Contrato descrito por Arquitectura (`user_story.md`); Backend (`backend_spec.md`); mapeo HTTP de Frontend (`frontend_spec.md`).

No están especificados la ruta, método, DTOs, campos, respuesta de éxito, estados ni envelope de errores. El frontend propone mensajes para distintos estados HTTP, pero el propio documento los califica de genéricos y pendientes de confirmación. No se puede afirmar que exista una incompatibilidad, pero tampoco que el frontend consuma un contrato compatible con backend.

**Corrección concreta:** aprobar y documentar el contrato real de login; contrastar contra él el endpoint, DTOs, errores y consumo frontend. Ajustar el mapeo de errores del frontend a los estados y semántica aprobados.

### H3 — Pruebas propuestas, no ejecutadas
**Severidad: Media.**  
**Ubicación:** `testing_report.md`, estado global y matriz T01–T08; comandos propuestos por Backend y Frontend.

No se adjuntan salidas reales de pruebas, compilación ni integración. Los comandos `mvn test`, `mvn verify`, `ng test` y `ng build` son propuestas condicionales: no se confirmó que correspondan a los proyectos entregados. Los casos positivo, negativo, de borde e integración siguen pendientes.

**Corrección concreta:** confirmar los sistemas de build y comandos del repositorio, ejecutar las pruebas pertinentes y adjuntar sus salidas. Completar los casos de éxito, rechazo, validación, límites y error interno una vez aprobado el contrato.

### H4 — Revisión del código y de la arquitectura efectiva no posible
**Severidad: Baja.**  
**Ubicación:** Backend (`backend_spec.md`); Frontend (`frontend_spec.md`); Arquitectura (`user_story.md`).

No se aportó código backend ni una integración frontend verificable. La arquitectura describe límites hexagonales recomendados, pero no evidencia su implementación. No es posible revisar nombres, separación efectiva de responsabilidades, duplicación, validaciones, manejo de errores ni buenas prácticas concretas de Quarkus o Angular.

**Corrección concreta:** integrar cambios sobre los componentes reales y proporcionar el diff o código correspondiente para revisar que HTTP y el mapeo de errores permanezcan en infraestructura, que aplicación y dominio no filtren detalles internos y que el frontend no muestre respuestas técnicas crudas.

### H5 — Riesgos de despliegue y dependencias sin evaluar
**Severidad: Baja.**  
**Ubicación:** Entregas de Backend, Frontend y Seguridad.

No se proporcionaron manifiestos de dependencias, configuración de despliegue ni evidencia sobre logs, almacenamiento o integraciones del login. Seguridad declara esas áreas no evaluables. Tampoco se sabe si la autenticación usa persistencia o si esta feature la afecta.

**Corrección concreta:** con el repositorio disponible, revisar dependencias y configuración operativa; inspeccionar los registros para descartar exposición de credenciales y confirmar si hay impactos en persistencia. No introducir cambios de datos sin evidencia de que sean necesarios.

## Pendientes antes de integrar

- **Arquitectura/API:** aportar el Issue completo y aprobar ruta, método, esquema de entrada, validaciones, éxito y catálogo de errores.
- **Backend:** implementar el cambio en el endpoint real, conservando el contrato aprobado y evitando serializar el request o excepciones internas.
- **Frontend:** integrar el formulario y el endpoint contractuales; alinear los mensajes y estados de error con Backend; confirmar que no se muestra la respuesta cruda.
- **Pruebas/QA:** añadir y ejecutar pruebas de éxito, rechazo, validación, límites y fallo interno controlado; adjuntar salidas reales de tests y build.
- **Seguridad:** verificar ausencia de eco y detalles internos en respuestas, y revisar por separado logs y exposición de credenciales.
- **Datos:** confirmar, tras inspeccionar el flujo y el modelo, si la feature afecta persistencia; no hay una entrega de Datos disponible para esta revisión.

VEREDICTO: RECHAZADO