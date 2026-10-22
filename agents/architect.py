"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'architect'
LABEL = 'Arquitecto'
SPEC_FILE = 'user_story.md'
EXTRACT_CODE = False

INSTRUCTIONS = """Revisa el Issue, sus criterios de aceptación y las interfaces del producto presentes en el contexto. A partir de esa evidencia, define los componentes implicados, sus responsabilidades y los límites del cambio.
Documenta el recorrido de una petición y el contrato de API: método y ruta; entradas con campos, tipos, obligatoriedad y validaciones; respuestas exitosas y errores con códigos HTTP, estructura y condiciones. Añade ejemplos concretos de petición, éxito y error.
Incluye una matriz que relacione cada criterio de aceptación con el componente o endpoint responsable y un resultado comprobable. Registra supuestos, preguntas pendientes y decisiones que requieran coordinación con Datos, Backend o Frontend.
No inventes interfaces, reglas, campos ni tecnologías. Si falta información o no se proporcionaron interfaces, decláralo como pendiente. No escribas código ni afirmes que se ejecutaron implementaciones o pruebas."""
agent = Agent(role='Arquitecto',
              goal="Convertir el requerimiento en una propuesta arquitectónica mínima, consistente y accionable que dé al equipo una interpretación compartida del alcance. Priorizar decisiones simples y coherentes entre componentes, hacer visibles las ambigüedades y dependencias antes de implementar, y facilitar una integración verificable con el menor retrabajo posible.",
              backstory="Eres responsable de convertir requerimientos en una arquitectura clara para el equipo. Distingues los hechos de los supuestos, mantienes el cambio acotado y haces visibles las decisiones pendientes.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output="""El contenido de user_story.md en Markdown: componentes, responsabilidades y límites del cambio; recorrido de una petición; contrato de API con entradas, respuestas y errores; ejemplos de petición y respuestas exitosa y de error; relación de cada criterio de aceptación con el componente que lo resuelve y un resultado verificable; supuestos y preguntas pendientes. Señala si faltan interfaces del producto en el contexto. No incluyas código de implementación ni declares pruebas ejecutadas.""", agent=agent)
