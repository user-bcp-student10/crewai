# Estándar de pruebas y reporte

Usa los criterios de aceptación y las entregas aprobadas de Arquitectura,
Backend, Frontend y Datos (si existe el rol) como fuente de verdad. No inventes
reglas de negocio, rutas, campos, códigos HTTP, tablas, constraints ni resultados.
Separa los hechos confirmados de supuestos; si falta un contrato o artefacto,
indica qué se necesita para probarlo.

## Trazabilidad y diseño

- Numera los criterios como `CA-01`, `CA-02`, etc. Incluye el texto de cada uno
  sin alterarlo y relaciónalo con uno o más casos mediante sus IDs.
- Para cada caso indica objetivo, tipo (positivo, negativo, borde o integración),
  preparación, datos concretos, pasos/acción, resultado esperado y criterio
  cubierto.
- Incluye los cuatro tipos de prueba. Si el requisito o el entorno no permite uno,
  documenta el motivo y márcalo `NO EJECUTADO`; no lo presentes como cubierto.
- Agrega casos para regresiones que correspondan a correcciones propuestas:
  describe la falla previa, la corrección, el caso que la evita y su resultado
  esperado. No digas que una corrección existe si no se ve en el código aprobado.

## Contratos que deben comprobarse

- **API:** contrasta método, ruta, autenticación/autorización, parámetros, cuerpo,
  validaciones, códigos HTTP, esquema de respuesta y errores entre la especificación
  aprobada y Backend. Diseña casos válidos, inválidos, límites y falta de permisos
  cuando apliquen. Señala toda discrepancia como hallazgo; no adivines el contrato.
- **Persistencia:** cuando haya contrato de Datos o persistencia en Backend,
  contrasta entidades y columnas, tipos, nulabilidad, claves, unicidad, relaciones,
  restricciones, transacciones y migraciones. Define comprobaciones de integridad,
  reversión y conservación de datos cuando correspondan. No ejecutes ni afirmes
  haber aplicado migraciones sin evidencia.
- Si no hay una API, base de datos o implementación ejecutable, registra la
  verificación como `NO EJECUTADO`, explica el bloqueo y deja comandos concretos
  que se puedan ejecutar cuando el artefacto esté disponible.

## Ejecución honesta y reproducible

Entrega `testing_report.md` con estas secciones: alcance y referencias; preparación
y precondiciones; matriz de trazabilidad; casos detallados; contratos de API y
persistencia; correcciones y regresiones; comandos reproducibles; resultados y
limpieza. No omitas ningún criterio de aceptación.

Por cada ejecución real registra comando exacto, directorio, precondiciones,
resultado (PASSED/FAILED), resumen de salida y limitaciones. Para todo lo que no
se ejecutó usa literalmente `NO EJECUTADO` y explica por qué. Una prueba propuesta
no equivale a una prueba ejecutada; nunca inventes salida, cobertura, datos,
servicios disponibles ni éxito.

Incluye pruebas automatizadas ejecutables adecuadas al repositorio. En las pruebas
JUnit, da a cada bloque de código un nombre de archivo en la primera línea,
por ejemplo `// TransferResourceTest.java`, y proporciona imports, package y
assertions necesarios. Explica las dependencias y comandos de ejecución. Los
comandos de limpieza deben limitarse a los datos o artefactos temporales creados
por estas pruebas y no borrar datos de usuario.
