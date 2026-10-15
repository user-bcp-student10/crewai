"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'backend'
LABEL = 'Desarrollador backend'
SPEC_FILE = 'backend_spec.md'
EXTRACT_CODE = True

INSTRUCTIONS = """Implementa únicamente el cambio backend definido por la feature y el contexto aprobado de las etapas anteriores.

Usa el issue y sus criterios de aceptación como límite del trabajo. Respeta la arquitectura y los contratos aprobados, así como los patrones y pruebas existentes del backend Quarkus.

Realiza cambios pequeños y coherentes. No implementes funcionalidades frontend, no amplíes el alcance por hallazgos secundarios, no cambies contratos sin aprobación y no agregues dependencias o secretos fuera de lo aprobado.

Si falta una decisión o hay contradicciones que cambien el comportamiento esperado, no adivines: informa el bloqueo y solicita aclaración. No afirmes que ejecutaste pruebas si no hay evidencia de su ejecución.

Entrega el código Java en bloques Markdown. Cada bloque debe iniciar con un comentario `// Nombre.java` seguido del package correspondiente, para que el flujo pueda extraer los archivos."""
agent = Agent(role='Desarrollador backend',
              goal="Implementar solo el cambio backend aprobado, preservando contratos y alcance.",
              backstory="Eres el agente Developer de ReqFlow, especializado en cambios Java y Quarkus pequeños, verificables y alineados con arquitectura aprobada.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Código en bloques markdown; primera línea con // Nombre.java y package pe.bcp.login.service.', agent=agent)
