# user_story.md

## 1) Solución propuesta

El material recibido incluye el nombre de la feature —**H-AUTH-04 Eliminar detalles internos y eco de entrada en las respuestas de login**—, pero no contiene el texto completo del Issue, criterios de aceptación detallados ni código del producto. Por tanto, no es posible confirmar la ruta, el método, el formato actual del request, el formato de éxito o los errores que ya devuelve el sistema.

La propuesta se limita al cambio indicado por el título: las respuestas del login no deben incluir valores copiados del request ni detalles internos de implementación. Se debe preservar la autenticación y, en lo posible, el contrato público existente. No se propone cambiar el mecanismo de login, persistencia, proveedor de identidad ni formato de tokens sin revisar el código y el contrato actuales.

Para cumplirlo, la capa de entrada debe construir las respuestas desde datos públicos permitidos, en vez de serializar directamente el request, excepciones internas o modelos de infraestructura. Los errores internos deben traducirse antes de llegar al cliente. Los nombres, códigos, mensajes y estados exactos propuestos abajo son candidatos sujetos a confirmación, no comportamientos existentes verificados.

## 2) Componentes y límites

No se pudo verificar qué componentes existen en el producto. Los siguientes son los límites que debería respetar la solución; no afirman que ya haya clases o archivos con estos nombres.

| Capa hexagonal | Responsabilidad |
|---|---|
| `infrastructure/adapter/input/` | Adaptador REST de login ya existente, si lo hay. Recibe y valida el request según el contrato vigente, invoca el caso de uso y convierte su resultado en una respuesta pública allowlistada. No debe serializar el request completo ni exponer excepciones internas. |
| `application/service/` | Implementación del caso de uso de login. Coordina la autenticación mediante puertos de salida y devuelve un resultado de aplicación; no define formatos HTTP ni mensajes de error de infraestructura. |
| `domain/model/` | Modelos y reglas de dominio necesarios para la autenticación. No importan clases de infraestructura ni contienen detalles de HTTP. |
| `domain/port/input/` | Interfaz del caso de uso que invoca el adaptador de entrada. |
| `domain/port/output/` | Interfaces para los mecanismos de autenticación o datos que requiera el caso de uso. Su existencia y forma actuales no están disponibles para verificar. |
| `infrastructure/adapter/output/` | Adaptadores concretos de los puertos de salida, si existen. Sus errores no deben filtrarse directamente al cliente. |
| `infrastructure/config/` | Configuración necesaria para conectar adaptadores y, si el producto ya usa ese patrón, el manejo centralizado de errores HTTP. |

Las dependencias deben apuntar hacia dentro: infraestructura → aplicación → dominio. El mapeo de excepciones a respuestas HTTP pertenece a la infraestructura de entrada, no al dominio.

## 3) Contrato de API (entradas, respuestas, errores)

### Endpoint y método

**No verificables con la información disponible.** Deben mantenerse la ruta y el método del endpoint de login existentes. No se propone una ruta nueva.

### Entradas

- **Parámetros de ruta, query y headers:** no especificados en el material recibido; conservar los que establezca el contrato existente.
- **Body, campos, tipos y validaciones:** no especificados; conservar el esquema y las validaciones existentes.
- La respuesta no debe copiar valores del body ni de otros datos de entrada. Esto incluye credenciales y cualquier otro valor enviado por el cliente.
- No se puede determinar si el login admite campos adicionales, varios identificadores o formatos específicos. Debe confirmarse con Backend y Frontend.

### Respuestas

**Éxito:** conservar el código de estado y los campos públicos del éxito actual, una vez verificados. Los campos deben construirse desde el resultado público del caso de uso; no desde una serialización indiscriminada del request, entidades internas o modelos de infraestructura. No es posible enumerar el payload de éxito sin ver el contrato actual.

**Errores:** el criterio de la feature exige no exponer detalles internos ni devolver valores del request. Como propuesta pendiente de aprobación, se recomienda usar un error público genérico y estable para fallos de autenticación. Ejemplo de candidato:

- HTTP `401`
- Código público candidato: `AUTHENTICATION_FAILED`
- Mensaje candidato: `No se pudo iniciar sesión.`

Este código y mensaje **no se han verificado como parte del contrato existente**. Tampoco se sabe si el producto distingue otros tipos de error o usa otro envelope.

Para errores de formato o validación, se deben conservar el estado y el contrato actuales, sanitizando el payload. Si se desea un formato unificado, se propone como candidato HTTP `400`, código `INVALID_REQUEST` y mensaje `La solicitud no es válida.`; Backend y Frontend deben confirmar si corresponde adoptarlo.

Para errores inesperados, la respuesta pública no debe incluir stack traces, mensajes de excepciones, SQL, nombres de proveedores ni otros detalles internos. El estado, código y mensaje exactos deben alinearse con el manejo de errores ya existente; no están definidos en la información recibida.

## 4) Ejemplo de petición y respuesta

El siguiente ejemplo es **esquemático**: la ruta y el body reales deben sustituirse por los del endpoint vigente. No se inventan nombres de campos porque no están disponibles.

### Caso de error representativo: credenciales no aceptadas

```http
POST [ruta de login existente, por confirmar]
Content-Type: application/json

[body con el formato de login existente, por confirmar]
```

Respuesta candidata, si Backend y Frontend aprueban el contrato propuesto:

```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
  "code": "AUTHENTICATION_FAILED",
  "message": "No se pudo iniciar sesión."
}
```

La respuesta no reproduce el body ni revela el motivo interno concreto del rechazo. El código y el mensaje son propuestas, no valores confirmados del producto.

### Recorrido de una petición válida

1. El adaptador de entrada existente recibe la petición en su ruta actual y valida el body conforme al esquema vigente.
2. El adaptador invoca el puerto de entrada del caso de uso de login.
3. El servicio de aplicación coordina la operación mediante los puertos de salida correspondientes. Su implementación concreta no puede verificarse sin el código.
4. Si la autenticación tiene éxito, el caso de uso devuelve un resultado de aplicación.
5. El adaptador de entrada construye la respuesta usando únicamente los campos públicos de éxito definidos por el contrato vigente. No añade campos copiados del request.
6. Se responde con el estado y payload de éxito existentes, por confirmar.

### Recorrido del error representativo

1. La petición llega al adaptador de entrada y se procesa según el contrato vigente.
2. El caso de uso no puede completar la autenticación y devuelve o produce el error correspondiente.
3. El adaptador de entrada traduce ese error al error público aprobado; no serializa la excepción ni sus detalles internos.
4. Se devuelve el estado y el envelope aprobados, sin incluir valores de entrada.

## 5) Criterios de aceptación verificables

El material recibido no incluye una lista de criterios de aceptación detallados. Los siguientes son criterios verificables **derivados del título de la feature**, pendientes de confirmación contra el Issue completo:

1. Ninguna respuesta de login contiene valores copiados del request, tanto en éxito como en error.
2. Ninguna respuesta de login expone mensajes de excepciones internas, stack traces ni detalles de infraestructura.
3. El éxito conserva el contrato público vigente, excepto por campos que se demuestre que son eco de entrada o detalles internos y cuya eliminación se apruebe.
4. Los errores usan únicamente el formato público aprobado; los códigos y mensajes internos no llegan al cliente.
5. Las pruebas de contrato cubren al menos una petición válida y un error de autenticación, y verifican que no se filtran datos de entrada ni detalles internos.
6. La ruta, el método, las validaciones y los datos públicos legítimos del login no cambian sin una decisión explícita de compatibilidad.

No se puede confirmar con el material disponible que estos criterios cubran todos los del Issue. Si el Issue contiene criterios adicionales, deben incorporarse antes de cerrar el diseño.

## 6) Supuestos y decisiones pendientes para otros roles

### Pendientes de confirmar con Backend

- Ruta y método del endpoint existente.
- Campos, tipos, validaciones y estados actuales de la petición.
- Payload y estado actuales para éxito.
- Manejo actual de errores, incluido si existe un envelope común.
- Si se aprueban `AUTHENTICATION_FAILED`, `INVALID_REQUEST` y los mensajes candidatos propuestos.
- Qué errores de autenticación deben mapearse a `401` y qué errores inesperados deben conservar otros estados.
- Dónde se realiza hoy la traducción de excepciones y qué campos son actualmente eco de entrada o detalles internos.
- Si el alcance incluye evitar exposición de datos sensibles en logs; no se puede inferir del título que la feature lo requiera.

### Pendientes de confirmar con Frontend

- Contrato de respuesta de éxito y envelope de error que consume actualmente la aplicación.
- Si el frontend depende de códigos o mensajes específicos para mostrar errores o tomar decisiones.
- Si es compatible sustituir mensajes detallados por un mensaje genérico.
- Comportamiento esperado ante los estados HTTP que se confirmen.

### Pendientes de confirmar con Datos

- No se propone ni se infiere un cambio de tablas, persistencia, unicidad o modelo de datos.
- Confirmar si existen restricciones o reglas de datos que afecten el resultado del login solo si el código o el Issue completo muestran que forman parte de esta feature. No hay información suficiente para definirlas aquí.

### Supuestos explícitos

- La feature modifica la **representación de la respuesta**, no la lógica de autenticación.
- El endpoint y el contrato de entrada existentes deben preservarse salvo decisión explícita en contrario.
- Los códigos, mensajes y estados candidatos de esta propuesta no son hechos verificados.
- Sin el Issue completo y el código del producto, no se puede presentar un contrato de API campo por campo ni asegurar compatibilidad. Esos datos son un prerrequisito para cerrar la especificación sin inventar el contrato existente.