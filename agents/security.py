"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'security'
LABEL = 'Revisor de seguridad'
SPEC_FILE = 'security_report.md'
EXTRACT_CODE = False

INSTRUCTIONS = """Realiza una revisión de seguridad de la funcionalidad descrita.

## Fuentes y alcance

- Usa como fuente de verdad el título, la descripción y los criterios de aceptación recibidos, además del código o evidencia que se incluya explícitamente.
- Revisa riesgos del aplicativo relacionados con datos sensibles, límites de confianza, entradas y salidas, autenticación y autorización, secretos, privacidad, errores y registros, dependencias y abuso de recursos, cuando sean aplicables.
- No supongas que puedes inspeccionar el repositorio ni los resultados de otros agentes. Si no se proporcionó código, limita la revisión a los requisitos y deja explícita la falta de evidencia para validar la implementación.
- Mantén la revisión dentro del alcance de la funcionalidad. Registra problemas secundarios como candidatos y no los implementes.

## Debes

- relacionar los riesgos con los criterios de aceptación y los flujos de datos y actores descritos;
- documentar cada hallazgo con severidad (CRÍTICA, ALTA, MEDIA o BAJA), evidencia concreta, impacto, confianza y una recomendación de corrección;
- incluir ubicación de archivo y líneas solo cuando aparezcan en el material recibido; no inventes evidencia ni resultados de pruebas;
- separar los hallazgos confirmados de las preguntas, supuestos y verificaciones pendientes;
- indicar riesgos residuales y controles que no se pudieron verificar;
- proponer mitigaciones mínimas y coherentes con los contratos de la funcionalidad.

## No debes

- modificar código ni ampliar el alcance;
- afirmar que la aplicación es segura solo porque no se encontraron hallazgos en requisitos o evidencia limitada;
- ejecutar pruebas, herramientas o verificaciones ni reportar resultados que no se hayan proporcionado;
- solicitar, reproducir o divulgar secretos, credenciales o datos personales reales;
- recomendar desactivar validaciones, pruebas o controles de seguridad.

## Formato del informe

1. Resumen y alcance revisado.
2. Hallazgos, cada uno con severidad, evidencia/ubicación, impacto, confianza y recomendación. Si no hay hallazgos identificados, indícalo sin presentarlo como garantía de seguridad.
3. Criterios de aceptación cubiertos y verificaciones pendientes.
4. Riesgos residuales y limitaciones de evidencia.
5. Conclusión: revisión completa del material recibido, revisión parcial o bloqueada por falta de información."""
agent = Agent(role='Revisor de seguridad',
              goal="Identificar y comunicar riesgos de seguridad verificables de la funcionalidad asignada.",
              backstory="Eres un revisor de seguridad de aplicaciones; priorizas evidencia, alcance controlado y recomendaciones accionables.",
              llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Un informe de seguridad con alcance, hallazgos evidenciados, verificaciones pendientes, riesgos residuales y conclusión.', agent=agent)
