# testing_report.md

## Estado y alcance

**Estado global: NO EJECUTADO.** No se recibió una salida real de comandos ni el repositorio del producto. Este documento separa el diseño de pruebas de cualquier resultado obtenido.

El material disponible identifica la feature como **H-AUTH-04: Eliminar detalles internos y eco de entrada en las respuestas de login**. No incluye el texto completo del Issue, sus criterios de aceptación oficiales, el código existente, el contrato aprobado de API, el modelo de Datos ni la configuración de build y pruebas.

Por eso:

- No es posible confirmar qué comportamiento ya existe ni qué correcciones fueron implementadas.
- Los criterios de la matriz que siguen son **derivados del título**, no criterios oficiales confirmados.
- No se asignan rutas, métodos, campos, estados HTTP ni formatos de respuesta.
- Las pruebas de producto quedan propuestas y bloqueadas hasta recibir los artefactos pendientes.
- El código incluido es un verificador auxiliar de respuestas capturadas; **no invoca el endpoint ni reemplaza las pruebas del proyecto**.

## Comportamiento existente y cambios pendientes de validar

**Comportamiento existente: no verificable.** No se proporcionó código de login ni una respuesta actual del endpoint.

Los entregables anteriores tampoco contienen una implementación:

- **Arquitectura:** propone construir respuestas desde campos públicos permitidos y traducir errores internos en la capa HTTP. Los códigos y mensajes de error sugeridos allí son candidatos, no contratos aprobados.
- **Backend:** declara la implementación bloqueada; no aporta cambios de código.
- **Frontend:** aporta un armazón de integración y propone no mostrar cuerpos técnicos de error. Declara que no fue integrado ni probado.

En consecuencia, no hay una corrección implementada que se pueda validar con evidencia disponible.

## Criterios de prueba y matriz de trazabilidad

Los criterios **AC-D1 a AC-D4** son derivados del nombre de la feature y requieren confirmación contra el Issue completo.

| Criterio | Caso | Tipo | Precondiciones y datos | Pasos | Resultado esperado observable | Estado |
|---|---|---|---|---|---|---|
| AC-D1: las respuestas de login no reproducen valores de entrada no permitidos. | T01 | Positiva; API | Endpoint, esquema y campos no públicos confirmados. Cuenta de prueba válida. Usar un valor centinela no sensible en un campo que el contrato no autorice a devolver. | Enviar una solicitud válida al endpoint contractual y capturar la respuesta HTTP completa. | La autenticación termina según el contrato aprobado; el centinela no aparece en la respuesta. El estado y el payload de éxito coinciden con el contrato aprobado. | **NO EJECUTADO.** Contrato, endpoint y datos pendientes. |
| AC-D1 / AC-D2: un rechazo no devuelve la entrada ni detalles internos. | T02 | Negativa; API | Endpoint y error público aprobados. Credenciales sintéticas inválidas; registrar como valores prohibidos los centinelas que no deban devolverse. | Enviar la solicitud de rechazo y capturar estado, headers y cuerpo. | Respuesta de rechazo conforme al contrato aprobado; no aparecen los valores prohibidos ni detalles internos. No se presupone un estado o mensaje específico. | **NO EJECUTADO.** Contrato pendiente. |
| AC-D1 / AC-D2: la respuesta de validación no refleja el cuerpo ni datos no permitidos. | T03 | Negativa; validación | Esquema y reglas de validación aprobados. Preparar una solicitud inválida conforme a esas reglas, sin asumir campos ni restricciones. | Enviar la solicitud inválida y capturar la respuesta. | Error conforme al contrato vigente; no se devuelven valores centinela ni detalles internos. | **NO EJECUTADO.** Faltan esquema y reglas. |
| AC-D1: comprobar el comportamiento en límites definidos por el contrato. | T04 | Borde | Límites mínimos y máximos, y campos aplicables, definidos por el contrato aprobado. Datos sintéticos en cada límite y fuera de él. | Enviar los casos de límite y los casos inmediatamente inválidos según las reglas aprobadas. | Cada caso produce el resultado de validación especificado por el contrato, sin eco de valores no permitidos. | **NO EJECUTADO.** No se conocen límites ni campos. |
| AC-D2: un error interno no expone información técnica. | T05 | Negativa; integración con fallo controlado | Entorno de prueba aislado y mecanismo aprobado para provocar un error interno. Usar un mensaje y marcador de stack trace sintéticos, exclusivos de la prueba. | Provocar el fallo aguas abajo y llamar al endpoint real de login. Capturar la respuesta pública. | El error se traduce al formato público aprobado; el mensaje, clase, stack trace y marcador internos no aparecen en la respuesta. | **NO EJECUTADO.** Falta implementación, mecanismo de fallo y contrato de errores. |
| AC-D1 / AC-D3: el flujo de éxito integrado no filtra entrada y conserva el contrato. | T06 | Positiva; integración | Backend y dependencias de autenticación de prueba disponibles; endpoint y contrato de éxito aprobados; cuenta sintética. | Invocar el endpoint real y examinar la respuesta capturada. | Autenticación correcta conforme al contrato; campos públicos esperados presentes y valores de entrada no permitidos ausentes. | **NO EJECUTADO.** Sin repositorio ni entorno. |
| AC-D1 / AC-D2 / AC-D4: los errores integrados conservan el contrato público sin filtraciones. | T07 | Negativa; integración | Entorno capaz de reproducir rechazo de autenticación y, si el contrato lo contempla, otros errores; contratos de error aprobados. | Ejecutar cada escenario con entradas sintéticas y capturar las respuestas HTTP. | Estado, envelope y campos públicos coinciden con el contrato aprobado; no aparecen valores prohibidos ni detalles internos. | **NO EJECUTADO.** Escenarios y contratos pendientes. |
| AC-D2, propuesta de Frontend: no presentar al usuario respuestas técnicas crudas. | T08 | Integración de interfaz | Código Frontend integrado, framework de pruebas disponible y contrato de errores acordado. Respuesta simulada con un marcador técnico sintético. | Simular un error del API y revisar el texto visible y los anuncios accesibles del componente. | La interfaz muestra únicamente el mensaje genérico aprobado; el marcador técnico y el cuerpo crudo no se muestran. | **NO EJECUTADO.** No se proporcionó proyecto Frontend ni sus dependencias. |

### Cobertura por tipo

- **Positiva:** T01 y T06; pendientes por falta del endpoint y del contrato de éxito.
- **Negativa:** T02, T03, T05 y T07; pendientes por falta del contrato de errores y del mecanismo de fallo.
- **Borde:** T04 aplica, pero no se pueden inventar límites, campos ni resultados esperados específicos.
- **Integración:** T05–T08 son pertinentes; no se pueden ejecutar sin código, entorno y contratos.
- **Persistencia:** no hay un criterio de persistencia confirmado ni un modelo de Datos. No se propone afirmar que el login no usa persistencia ni que el flujo no modifica datos. Si el código demuestra escrituras —por ejemplo, auditoría o estado de acceso—, se deberán añadir verificaciones de integridad conforme al modelo aprobado.

## Revisión de contratos

### API

| Elemento | Evidencia disponible | Consecuencia para las pruebas |
|---|---|---|
| Método y ruta de login | No proporcionados. | No se puede construir una solicitud reproducible al endpoint real. |
| Entradas, tipos y validaciones | No proporcionados. | No se pueden definir requests válidos, inválidos ni límites exactos. |
| Respuesta de éxito | No proporcionada. | No se puede comprobar que se conserve el contrato público. |
| Errores, estados y envelope | No proporcionados. | No se puede afirmar qué estado, código o mensaje es el esperado. |
| Eliminación de eco y detalles internos | Se deriva del título; no hay respuesta ni implementación que inspeccionar. | T01–T07 son verificaciones propuestas, no resultados. |

La propuesta arquitectónica de respuesta genérica de autenticación y los ejemplos de estado, código o mensaje **no se tratan como contrato aprobado**. Las pruebas deben usar los valores definidos por el contrato vigente cuando esté disponible.

### Persistencia

No se recibió el modelo de Datos, esquema, migraciones ni contrato de persistencia. Tampoco se sabe si el flujo actual de login lee o escribe datos. No hay base para proponer cambios de tablas ni para afirmar que no sean necesarios.

Antes de añadir pruebas de integración con base de datos se debe confirmar:

1. Si el login accede a persistencia y qué operaciones realiza.
2. El esquema y restricciones aprobados.
3. Qué efectos secundarios son esperados en éxito, rechazo y error interno.

## Preparación del entorno y datos

### Requisitos pendientes para pruebas del producto

Se necesitan los siguientes artefactos antes de ejecutar T01–T08:

- Repositorio y código del endpoint, servicio y manejo de errores.
- Texto completo del Issue y criterios de aceptación oficiales.
- Contrato API aprobado: método, ruta, entradas, validaciones, respuesta de éxito y catálogo de errores.
- Contratos y dependencias de integración de autenticación.
- Sistema de build, framework de pruebas y comandos documentados por el proyecto.
- Configuración segura de un entorno aislado y cuentas sintéticas.
- Si aplica, modelo de Datos y base de pruebas.
- Para T05, forma controlada y reproducible de provocar un error interno.

No se presuponen Maven, Angular, JUnit, Jasmine, pytest, una base de datos ni dependencias instaladas.

### Datos de prueba propuestos

Usar exclusivamente identidades y valores sintéticos del entorno de prueba. No incluir credenciales reales, tokens de producción ni respuestas con secretos en fixtures compartidos.

- **Éxito:** cuenta sintética válida, construida conforme al esquema aprobado.
- **Rechazo:** credenciales sintéticas inválidas, conforme a las reglas de autenticación existentes.
- **Validación y borde:** entradas basadas en campos y límites confirmados por el contrato.
- **Eco:** centinelas únicos en campos que el contrato confirme que no deben devolverse.
- **Error interno:** marcadores sintéticos configurados en el test double o mecanismo de fallo aprobado.

No guardar credenciales ni tokens en archivos de evidencia.

## Comandos reproducibles

No se dispone de comandos confiables para ejecutar pruebas del producto. No se inventan comandos de build o tests para Backend o Frontend.

El siguiente código es un **verificador auxiliar de capturas**, basado únicamente en la biblioteca estándar de Python. No es una dependencia confirmada del proyecto y no llama al API. Requiere que un test de integración del proyecto produzca, de manera segura, el archivo de capturas descrito abajo.

Tras guardar el código en `tests/test_login_response_safety.py` y preparar `testing/fixtures/login_response_exchanges.json`, los comandos para este verificador son:

```bash
python3 --version
LOGIN_EXCHANGES_FILE=testing/fixtures/login_response_exchanges.json \
  python3 -m unittest discover -s tests -p 'test_login_response_safety.py' -v
```

El archivo de capturas es un formato auxiliar de prueba, **no un contrato de API**. Debe ser un arreglo JSON con casos que incluyan:

- `id`: identificador de prueba.
- `type`: uno de `positive`, `negative`, `edge` o `integration`.
- `response`: captura JSON que contenga la respuesta HTTP observada; su forma interna depende del adaptador de pruebas.
- `forbidden_values`: lista de centinelas no sensibles cuya aparición en la respuesta está prohibida.

El verificador comprueba presencia de las cuatro categorías y ausencia literal de los centinelas en la respuesta. No valida estados HTTP esperados, esquema público, ecos transformados/codificados ni detalles internos no incluidos como centinelas. La captura debe obtenerse mediante las pruebas reales del proyecto; introducir respuestas inventadas no constituye evidencia.

**Estado de estos comandos: NO EJECUTADO.** No se ejecutaron comandos ni se proporcionó el archivo de capturas.

## Código de prueba auxiliar

```python
# archivo: tests/test_login_response_safety.py
"""Verifica propiedades de seguridad en capturas JSON de respuestas de login.

Este módulo no invoca el producto ni valida su contrato HTTP. Las capturas deben
provenir de pruebas reales del proyecto. Solo se buscan centinelas literales
incluidos en `forbidden_values`.
"""

import json
import os
import unittest
from pathlib import Path


DEFAULT_EXCHANGES_FILE = "testing/fixtures/login_response_exchanges.json"
REQUIRED_TYPES = {"positive", "negative", "edge", "integration"}


class LoginResponseSafetyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        exchanges_path = Path(
            os.environ.get("LOGIN_EXCHANGES_FILE", DEFAULT_EXCHANGES_FILE)
        )

        if not exchanges_path.is_file():
            raise unittest.SkipTest(
                f"No existe el archivo de capturas: {exchanges_path}. "
                "Debe generarse desde pruebas reales del proyecto."
            )

        try:
            cls.cases = json.loads(exchanges_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise AssertionError(
                f"No se pudo leer el archivo de capturas {exchanges_path}: {exc}"
            ) from exc

        if not isinstance(cls.cases, list) or not cls.cases:
            raise AssertionError(
                "El archivo de capturas debe contener un arreglo JSON no vacío."
            )

        ids = []
        for index, case in enumerate(cls.cases):
            if not isinstance(case, dict):
                raise AssertionError(f"El caso en índice {index} no es un objeto.")

            for required_key in ("id", "type", "response", "forbidden_values"):
                if required_key not in case:
                    raise AssertionError(
                        f"El caso en índice {index} no contiene {required_key!r}."
                    )

            if not isinstance(case["id"], str) or not case["id"].strip():
                raise AssertionError(f"El caso en índice {index} tiene un id inválido.")

            if case["type"] not in REQUIRED_TYPES:
                raise AssertionError(
                    f"Tipo no reconocido en el caso {case['id']!r}: {case['type']!r}."
                )

            if not isinstance(case["forbidden_values"], list):
                raise AssertionError(
                    f"forbidden_values no es una lista en {case['id']!r}."
                )

            if not case["forbidden_values"]:
                raise AssertionError(
                    f"El caso {case['id']!r} debe indicar los centinelas "
                    "prohibidos aplicables."
                )

            for value in case["forbidden_values"]:
                if not isinstance(value, str) or not value:
                    raise AssertionError(
                        f"Centinela vacío o no textual en el caso {case['id']!r}."
                    )

            ids.append(case["id"])

        if len(ids) != len(set(ids)):
            raise AssertionError("Los id de los casos deben ser únicos.")

    def test_fixture_covers_positive_negative_edge_and_integration(self):
        observed_types = {case["type"] for case in self.cases}
        missing_types = REQUIRED_TYPES - observed_types
        self.assertFalse(
            missing_types,
            f"Faltan capturas para los tipos: {sorted(missing_types)}",
        )

    def test_responses_do_not_contain_forbidden_values(self):
        for case in self.cases:
            serialized_response = json.dumps(
                case["response"],
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            )

            for forbidden_value in case["forbidden_values"]:
                with self.subTest(
                    case_id=case["id"],
                    forbidden_value=forbidden_value,
                ):
                    self.assertNotIn(
                        forbidden_value,
                        serialized_response,
                        msg=(
                            f"La respuesta capturada del caso {case['id']!r} "
                            "contiene un valor marcado como prohibido."
                        ),
                    )


if __name__ == "__main__":
    unittest.main()
```

## Limpieza

Después de ejecutar las pruebas con datos sintéticos:

```bash
rm -f testing/fixtures/login_response_exchanges.json
unset LOGIN_EXCHANGES_FILE
```

Eliminar también las cuentas de prueba o restaurar la base de datos únicamente según el procedimiento del entorno cuando este sea proporcionado. No se indican comandos de limpieza de base de datos porque su tecnología y modelo no se conocen.

## Limitaciones y resultados reales

- **NO EJECUTADO:** no hay salida real de pruebas, compilación ni comandos.
- No puede determinarse qué comportamiento existe en el producto.
- No puede verificarse ningún criterio oficial, pues no se recibió el Issue completo.
- No pueden verificarse método, ruta, payload, estados, respuestas ni errores de la API.
- No puede verificarse persistencia, integridad ni restricciones sin los artefactos de Datos.
- No pueden validarse las correcciones propuestas por Backend o Frontend: los entregables indican que no hubo implementación integrada.
- El verificador incluido comprueba centinelas literales en capturas; por sí solo no prueba que una respuesta provenga del endpoint, que cumpla el contrato aprobado o que no filtre valores transformados.