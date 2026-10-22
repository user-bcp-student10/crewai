"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from pathlib import Path

from crewai import Agent, Task

from crew.llm_config import llm

KEY = 'testing'
LABEL = 'Ingeniero de pruebas'
SPEC_FILE = 'testing_report.md'
EXTRACT_CODE = True

INSTRUCTIONS = (
    "Diseña pruebas trazables y reproducibles para la funcionalidad. "
    "Sigue el estándar de testing y el formato de informe incluidos a continuación. "
    "No inventes ejecución, resultados, contratos ni artefactos."
)
agent = Agent(role='Ingeniero de pruebas', goal="Completar la tarea asignada.",
              backstory="Eres un integrante del equipo.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    guide = Path(__file__).with_name("testing_guide.md").read_text(encoding="utf-8")
    return Task(description=INSTRUCTIONS + "\n\n" + guide
                + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output=(
                    "Informe Markdown completo llamado testing_report.md que relacione "
                    "cada criterio con casos y resultados esperados, preparación, datos, "
                    "comandos y limpieza; incluya verificaciones de contratos API y "
                    "persistencia y pruebas Java en bloques con primera línea "
                    "// NombreTest.java. Use NO EJECUTADO si no hay salida real."
                ),
                agent=agent)
