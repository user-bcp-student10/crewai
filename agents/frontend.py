"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'frontend'
LABEL = 'Desarrollador frontend'
SPEC_FILE = 'frontend_spec.md'
EXTRACT_CODE = True

INSTRUCTIONS = """Implementa el frontend Angular del feature según los criterios
de aceptación y el contrato de API aprobado.

Define pantallas, campos, validaciones, acciones y mensajes.
Usa servicios tipados; no inventes endpoints ni reglas de negocio.
Gestiona carga, vacío, éxito y errores; bloquea envíos duplicados.
No reintentes operaciones financieras automáticamente ni muestres éxito sin confirmación.
Incluye etiquetas accesibles, navegación por teclado y foco visible.
No expongas credenciales ni datos sensibles en código o logs.
Propón pruebas para los criterios de aceptación, errores de API y doble envío;
distingue pruebas propuestas de ejecutadas.

Entrega frontend_spec.md y código Angular siguiendo la estructura existente.
Respeta los bloques Markdown y comentarios de nombre de archivo exigidos por build_task.
Declara cualquier información faltante que impida implementar el recorrido."""
agent = Agent(role='Desarrollador frontend', goal="Analizar el feature brief recibido y producir una especificación técnica completa: arquitectura, componentes, contrato de API y  criterios de aceptación medibles, alineados a los estándares de seguridad y calidad del BCP.",
              backstory="Eres un desarrollador frontend senior con 10 años de experiencia en banca digital peruana. Conoces PCI-DSS  y las normas de la SBS.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Código en bloques markdown; primera línea con // nombre.service.ts.', agent=agent)
