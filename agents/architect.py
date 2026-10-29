"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'architect'
LABEL = 'Arquitecto'
SPEC_FILE = 'user_story.md'
EXTRACT_CODE = False

INSTRUCTIONS = (
    "1. Analiza el Issue, sus criterios de aceptación y las interfaces del producto.\n"
    "2. Define componentes, responsabilidades y límites del cambio.\n"
    "3. Especifica entradas, respuestas y errores de la API, con ejemplos.\n"
    "4. Relaciona cada criterio con el componente que lo resuelve.\n"
    "5. Declara supuestos y preguntas pendientes.\n"
    "6. Entrega user_story.md con componentes, contrato de API y criterios verificables."
)
agent = Agent(role='Arquitecto',
              goal="Diseñar una solución trazable a los criterios de aceptación, con componentes, "
                   "límites y contrato de API explícitos.",
              backstory="Eres el arquitecto del equipo. Lees el Issue y las interfaces existentes "
                        "antes de decidir, y dejas explícitos los supuestos y las preguntas pendientes "
                        "que Datos, Backend y Frontend deben resolver.",
              llm=llm, verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output=(
                    "Documento user_story.md en markdown con las secciones: "
                    "Componentes y responsabilidades; Límites del cambio; Contrato de API "
                    "(endpoint, método, entradas, respuestas y errores con ejemplos JSON); "
                    "Trazabilidad criterio-componente en tabla; Criterios verificables; "
                    "Supuestos y preguntas pendientes."),
                agent=agent)
