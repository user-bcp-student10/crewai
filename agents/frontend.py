"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'frontend'
LABEL = 'Desarrollador frontend'
SPEC_FILE = 'frontend_spec.md'
EXTRACT_CODE = True

INSTRUCTIONS = """Implementa el recorrido del usuario según el contrato de API aprobado.
Define campos, validaciones, acciones y mensajes.
Cubre estados de carga, vacío, éxito y error, y evita envíos duplicados.
Conserva etiquetas accesibles, navegación por teclado y foco visible.
Incluye cómo comprobar el recorrido y sus errores.
Entrega frontend_spec.md y código Angular con el formato de extracción que ya exige build_task."""
agent = Agent(role='Desarrollador frontend', goal="Analizar el feature brief recibido y producir una especificación técnica completa: arquitectura, componentes, contrato de API y  criterios de aceptación medibles, alineados a los estándares de seguridad y calidad del BCP.",
              backstory="Eres un desarrollador frontend senior con 10 años de experiencia en banca digital peruana. Conoces PCI-DSS  y las normas de la SBS.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Código en bloques markdown; primera línea con // nombre.service.ts.', agent=agent)
