# backend_spec.md

## Estado

**Implementación bloqueada por falta de contrato y código fuente.** El material disponible identifica la feature como **H-AUTH-04: Eliminar detalles internos y eco de entrada en las respuestas de login**. El historial de Arquitectura confirma que no se recibió el Issue completo ni el código del producto; los formatos y ejemplos mencionados allí son propuestas candidatas, no contratos aprobados.

No se proporcionaron criterios de aceptación completos, archivos del proyecto ni modelo de Datos. Por eso, no es posible identificar qué código existe o qué falta, ni implementar una solución sin inventar rutas, DTOs, clases, estados o formatos de respuesta.

**No se incluyen archivos Java:** con la información disponible, cualquier clase funcional sería especulativa o no estaría conectada al endpoint real. Un archivo vacío o una clase sin integración tampoco cumpliría la feature.

## 1. Resumen de la implementación

No se realizaron cambios de backend. No se puede determinar la ruta ni el método de login, el esquema de entrada, las respuestas de éxito y error, ni la integración actual con el mecanismo de autenticación.

El objetivo derivado del título es que las respuestas de login no incluyan valores copiados de la entrada ni detalles internos. Para implementarlo respetando el contrato vigente, hace falta revisar el endpoint y sus respuestas actuales. No se debe adoptar como definitivo el código, mensaje o estado de error sugerido en el documento de Arquitectura: allí se identifica expresamente como candidato pendiente de aprobación.

No se proponen cambios de persistencia. El modelo de Datos no fue proporcionado y no se puede confirmar si esta feature requiere acceso a datos.

## 2. Clases y responsabilidades

### Inventario disponible

- **Código existente:** no proporcionado; no es posible identificar clases, métodos o capas existentes.
- **Contrato API aprobado:** no proporcionado. La ruta, el método, los DTOs, los estados y el formato de errores no son verificables.
- **Modelo de Datos:** no proporcionado.
- **Arquitectura recibida:** describe límites de capas de forma orientativa, pero no identifica clases existentes ni aprueba un contrato HTTP concreto.

### Capas requeridas para el cambio

No se asignan nombres de clases porque hacerlo sería inventarlos antes de revisar el proyecto.

- **Resource (HTTP):** localizar el recurso de login existente y comprobar cómo construye las respuestas. Debe devolver únicamente campos públicos permitidos por el contrato y no serializar indiscriminadamente la solicitud ni excepciones.
- **Service (lógica de negocio):** localizar el caso de uso existente y verificar qué resultados o errores entrega al resource, sin trasladar detalles de infraestructura a la respuesta pública.
- **Repository (persistencia):** determinar, al inspeccionar el código y el modelo de Datos, si participa en el login. No se propone crear ni modificar repositorios o tablas sin esa verificación.
- **DTOs:** conservar los existentes si corresponden al contrato aprobado. No se pueden definir DTOs nuevos sin conocer el esquema actual.

## 3. Recorrido de un caso válido y uno de error

Los recorridos siguientes describen el comportamiento que se debe comprobar e implementar cuando se disponga del contrato y el código. **No representan flujos verificados del producto.**

### Caso válido — recorrido objetivo

1. El endpoint de login existente recibe una solicitud conforme al esquema vigente.
2. El resource aplica las validaciones de entrada ya establecidas y delega en el servicio.
3. El servicio coordina la autenticación usando los componentes existentes.
4. Si la autenticación tiene éxito, el resource construye la respuesta conforme al contrato público vigente.
5. La respuesta no incorpora valores copiados de la solicitud, entidades internas ni datos de infraestructura que el contrato no permita.

No se conocen la ruta, los campos, el resultado del servicio ni el estado HTTP de éxito; no se pueden precisar sin el contrato.

### Caso de error representativo — rechazo de autenticación

1. La solicitud llega al endpoint existente y se procesa según su contrato.
2. El flujo de autenticación rechaza la solicitud.
3. La capa HTTP convierte el resultado al error público definido por el contrato vigente.
4. La respuesta no reproduce valores de entrada ni expone mensajes de excepción, stack traces o detalles internos.

El estado y el cuerpo exactos no se especifican aquí: el historial de Arquitectura los presenta como candidatos, no como decisiones aprobadas.

## 4. Trazabilidad: criterio de aceptación → código

No se recibió la lista oficial de criterios del Issue. Los criterios de esta tabla son **derivados del título**, no confirmados como criterios de aceptación del Issue.

| Criterio derivado | Cobertura actual |
|---|---|
| Las respuestas de login no devuelven valores copiados de la solicitud, tanto en éxito como en error. | **Sin cubrir.** No se proporcionó el resource, los DTOs ni el contrato de respuestas. |
| Las respuestas no exponen excepciones, stack traces ni detalles internos. | **Sin cubrir.** No se proporcionó el manejo actual de errores ni el código del endpoint. |
| La respuesta de éxito conserva el contrato público aprobado, eliminando únicamente campos no permitidos. | **No verificable.** El contrato aprobado y la respuesta actual no fueron proporcionados. |
| Los errores conservan el estado y formato públicos aprobados, sin incluir datos de entrada o detalles internos. | **No verificable.** No se proporcionaron el contrato de errores ni el Issue completo. |
| Las entradas de login se validan en el servidor según el contrato vigente. | **No verificable.** No se proporcionaron el esquema ni las validaciones actuales. |

No hay clases o métodos concretos que puedan asociarse a estos criterios sin inspeccionar el código existente.

## 5. Comandos de verificación

**NO EJECUTADO.** No se proporcionó el proyecto y no se ejecutaron herramientas.

Si el repositorio usa Maven, los siguientes comandos quedan pendientes de ejecución:

```bash
mvn test
```

```bash
mvn verify
```

No se afirma que estos comandos correspondan al sistema de build del proyecto ni que compilen o pasen las pruebas.

## 6. Supuestos y pendientes para otros roles

### Pendientes para Arquitectura/API

- Proporcionar el contrato aprobado del endpoint de login: ruta, método, entradas, validaciones, respuesta de éxito y errores.
- Confirmar el formato y los estados HTTP permitidos para errores de autenticación, validación y fallos inesperados.
- Confirmar qué campos de entrada o de respuesta son públicos y cuáles deben excluirse.

### Pendientes para Backend

- Proporcionar el código fuente del endpoint de login, el servicio, los DTOs y el manejo de errores para identificar lo que ya existe antes de cambiarlo.
- Proporcionar el sistema de build y las pruebas existentes para preparar la verificación correspondiente.
- Tras recibir esos materiales, implementar el cambio en las capas existentes y añadir o actualizar pruebas que comprueben que las respuestas no incluyen valores de entrada ni detalles internos.

### Pendientes para Datos

- Proporcionar el modelo de Datos solo si el flujo existente de autenticación accede a persistencia y el cambio lo requiere. No se propone modificar tablas ni migraciones.

### Supuestos y límites

- No se asume una ruta, un método, un formato JSON, un código de error ni un mensaje.
- No se asume que el login requiera cambios de persistencia.
- No se presenta la propuesta de error del documento de Arquitectura como contrato aprobado.
- No se recibieron observaciones o errores adicionales que atender.
- No se afirma que haya código implementado, compilado, probado o desplegado.