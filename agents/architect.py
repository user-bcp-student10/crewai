"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'architect'
LABEL = 'Arquitecto'
SPEC_FILE = 'user_story.md'
EXTRACT_CODE = False

INSTRUCTIONS = """Analiza el Issue, sus criterios de aceptación y las interfaces del producto incluidas en el contexto. Define los componentes de la solución, la responsabilidad y los límites de cada uno, manteniendo el cambio acotado al requerimiento.
Especifica el contrato de API con método y ruta, entradas (campos, tipos, obligatoriedad y validaciones), respuestas de éxito y errores (códigos HTTP, forma del cuerpo y condición que los produce). Incluye ejemplos concretos de petición, respuesta exitosa y error, y describe el recorrido de una petición entre componentes.
Relaciona cada criterio de aceptación con el componente o endpoint que lo resuelve y con un resultado verificable. Declara supuestos y preguntas pendientes, incluidas las decisiones que deban coordinarse con Datos, Backend y Frontend.
Usa solo información disponible en el contexto; no inventes interfaces, reglas, campos ni tecnologías. Si no recibiste interfaces del producto o falta información, indícalo expresamente como pendiente en vez de afirmar que las analizaste. No escribas código ni declares implementaciones o pruebas ejecutadas."""
agent = Agent(role='Arquitect',
              goal="Analizar el Issue y las interfaces disponibles para definir componentes, límites y un contrato de API verificable contra los criterios de aceptación.",
              backstory="Eres responsable de convertir requerimientos en una arquitectura clara para el equipo. Distingues los hechos de los supuestos, mantienes el cambio acotado y haces visibles las decisiones pendientes.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output="""El contenido de user_story.md en Markdown: componentes, responsabilidades y límites del cambio; recorrido de una petición; contrato de API con entradas, respuestas y errores; ejemplos de petición y respuestas exitosa y de error; relación de cada criterio de aceptación con el componente que lo resuelve y un resultado verificable; supuestos y preguntas pendientes. Señala si faltan interfaces del producto en el contexto. No incluyas código de implementación ni declares pruebas ejecutadas.""", agent=agent)
