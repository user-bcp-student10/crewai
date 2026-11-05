# Informe de seguridad — H-AUTH-04

## Resumen

La feature busca que las respuestas de login no reproduzcan datos de entrada ni expongan detalles internos. Sin embargo, el material disponible no incluye el endpoint, el contrato aprobado, el código de backend integrado ni pruebas ejecutadas. Backend declara que no realizó cambios; el frontend describe un armazón no integrado.

**No se confirma una vulnerabilidad explotable.** Sí existe un riesgo de verificación: no se puede comprobar que las respuestas actuales del login cumplan el objetivo de seguridad. La severidad asignada a ese riesgo es **Media, provisional**; no representa una vulnerabilidad confirmada.

### Activos, datos y puntos de entrada

- **Activos potencialmente involucrados:** credenciales y otros campos del request de login; identidad de la cuenta; tokens o datos de sesión que pudiera devolver el éxito; mensajes de excepción y metadatos internos.
- **Puntos de entrada:** el endpoint de login existente, cuya ruta, método y esquema no se proporcionaron; el formulario y `buildRequest` de la aplicación anfitriona, según la especificación frontend.
- **Integraciones, archivos y almacenamiento:** no se proporcionó evidencia sobre proveedores de identidad, archivos, persistencia o integraciones externas. No se puede confirmar si participan.

### Evaluación OWASP y áreas solicitadas

| Área | Evaluación con la información disponible |
|---|---|
| Control de acceso y autorización (A01) | No evaluable: faltan el endpoint y su implementación. |
| Autenticación y sesiones (A07) | La feature se refiere al login, pero no se proporcionaron el mecanismo de autenticación ni el manejo de sesiones o tokens. |
| Inyección SQL y de comandos (A03) | Sin hallazgo confirmado; no se proporcionó código de acceso a datos ni de ejecución de comandos. |
| XSS (A03) | Sin hallazgo confirmado. El eco podría ser relevante si datos de entrada se devuelven y luego se renderizan, pero no hay evidencia de que ocurra. El armazón frontend propone no mostrar cuerpos crudos y no consta como integrado. |
| Validación y sanitización | No evaluables: faltan esquema, reglas y código del endpoint. |
| Secretos y credenciales | No se proporcionaron configuración, código ni inventario de secretos; no se puede comprobar su manejo. |
| Exposición de datos en respuestas o logs (A09) | La feature aborda la exposición en respuestas, pero no hay respuestas ni código para inspeccionar. El manejo de logs tampoco está documentado. |
| Dependencias vulnerables (A06) | No evaluable: no se proporcionaron manifiestos ni inventario de dependencias. |
| Configuración, integridad y SSRF (A05, A08, A10) | No hay evidencia suficiente para identificar riesgos en estas áreas. |

## Hallazgos

| ID | Severidad | Descripción y evidencia | Componente afectado | Impacto | Corrección concreta y verificación |
|---|---|---|---|---|---|
| SEC-H-AUTH-04-01 | **Media (provisional; brecha de verificación, no vulnerabilidad confirmada)** | No se puede verificar que las respuestas de login excluyan valores de entrada y detalles internos. La especificación de Backend declara la implementación bloqueada y sin cambios; las pruebas indican que no se recibió código ni se ejecutaron verificaciones. Esto **no demuestra** que el endpoint actual filtre información. | Endpoint de login y mapeo de respuestas/errores del backend; integración frontend pendiente. | Si el endpoint actual refleja datos de entrada o excepciones, podría revelar credenciales u otros datos del request, o información interna. Ese impacto es condicional: no se ha observado una respuesta que lo confirme. | Revisar el endpoint y crear respuestas mediante una lista explícita de campos públicos; traducir excepciones a errores públicos aprobados, sin serializar el request ni la excepción. Añadir pruebas para éxito, rechazo de autenticación, validación y fallo interno controlado. En cada caso, usar valores centinela sintéticos y comprobar que no aparecen en el cuerpo de respuesta; verificar también que los errores no contienen marcadores de excepción o stack trace y que se conserva el contrato aprobado. |

## Recomendaciones

1. **Obtener el contrato y el código reales:** confirmar ruta, método, esquema de entrada, respuestas de éxito y catálogo de errores antes de modificar el comportamiento.
2. **Implementar la respuesta mediante una allowlist:** incluir solo los campos aprobados por el contrato. No serializar directamente el request, entidades internas, excepciones ni modelos de infraestructura.
3. **Traducir errores en el adaptador HTTP:** preservar los estados y formatos acordados, pero no exponer mensajes internos, stack traces ni detalles de proveedores o infraestructura.
4. **Completar criterios de aceptación de seguridad:** exigir ausencia de eco tanto en éxito como en error; definir el comportamiento de errores de autenticación, validación y fallos inesperados; especificar qué campos del éxito son públicos. Confirmar además si deben evitarse diferencias observables que revelen la existencia de cuentas.
5. **Verificar frontend y logs:** una vez integrado, comprobar que la interfaz no muestra respuestas técnicas crudas. Revisar por separado que las credenciales no se registren en logs; no hay evidencia disponible para afirmar que actualmente se registren.
6. **Revisar dependencias y controles generales** al disponer del proyecto y sus manifiestos. No se puede recomendar una actualización concreta sin conocer las dependencias.

Como plantilla de comprobación manual —**no ejecutada y pendiente de adaptar al contrato y endpoint reales**— se puede guardar en `request.json` una solicitud sintética válida para cada escenario y comprobar el cuerpo capturado:

```bash
curl -sS -o response.json -w '%{http_code}\n' \
  -H 'Content-Type: application/json' \
  --data-binary @request.json \
  "$LOGIN_URL"

! grep -F -- 'SEC_CANARY_NO_ECO' response.json
! grep -F -- 'SEC_CANARY_INTERNAL_ERROR' response.json
```

Ejecutar la comprobación para los escenarios de éxito, rechazo, validación y fallo interno controlado, usando centinelas sintéticos. Además de la ausencia de centinelas, la prueba debe comprobar el estado y los campos públicos según el contrato aprobado. No se conoce `LOGIN_URL` ni el formato real del request, por lo que la plantilla no es directamente ejecutable sin adaptarlos. Si el proyecto usa Maven, Backend propone `mvn test` como comando pendiente; el sistema de build no está confirmado.

## Checklist de verificación

- [ ] Obtener el Issue completo, el contrato aprobado y el código del endpoint de login.
- [ ] Confirmar que ninguna respuesta de éxito reproduce campos de entrada no autorizados.
- [ ] Confirmar que rechazos, errores de validación y fallos internos no reproducen la entrada.
- [ ] Comprobar que los errores no exponen excepciones, stack traces ni detalles de infraestructura.
- [ ] Verificar que la respuesta conserva únicamente los campos y estados públicos aprobados.
- [ ] Probar los casos con datos centinela sintéticos y registrar resultados de pruebas ejecutadas.
- [ ] Confirmar que la interfaz no muestra el cuerpo crudo de errores.
- [ ] Inspeccionar el registro de solicitudes y errores para descartar exposición de credenciales.
- [ ] Revisar manifiestos y dependencias cuando se proporcione el repositorio.
- [ ] Documentar explícitamente las áreas restantes como no verificadas si sigue faltando evidencia.