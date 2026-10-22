"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from pathlib import Path

from crewai import Agent, Task

from crew.llm_config import llm

KEY = 'testing'
LABEL = 'Ingeniero de pruebas'
SPEC_FILE = 'testing_report.md'
EXTRACT_CODE = True

INSTRUCTIONS = (
    "Diseña pruebas trazables y reproducibles para la funcionalidad y para los casos NO funcionales. "
    "Sigue el estándar de testing y el formato de informe incluidos a continuación. "
    "No inventes ejecución, resultados, contratos ni artefactos."
    "Incluye pruebas de rendimiento, seguridad y usabilidad cuando corresponda."
    "Asegúrate de que todas las pruebas sean reproducibles y estén bien documentadas."
    "Documenta claramente los pasos de configuración, ejecución y limpieza de cada prueba."
    "Incluye también la validación de resultados esperados y manejo de errores."
    "Asegúrate de que los informes sean claros y comprensibles para otros miembros del equipo."
    "Incluye referencias a la documentación relevante y a los requisitos del sistema cuando sea necesario."
    "Asegúrate de que todas las pruebas sean consistentes con los estándares de calidad del proyecto."
    "Revisa y actualiza las pruebas según sea necesario para reflejar cambios en la funcionalidad o en los requisitos."
    "Asegúrate de que todas las pruebas estén alineadas con los objetivos del proyecto y las expectativas del cliente."
    "Prioriza la automatización de pruebas siempre que sea posible para mejorar la eficiencia y la cobertura."
    "Asegúrate de que todas las pruebas automatizadas sean mantenibles y fáciles de entender."
    "Incluye la integración de pruebas automatizadas en el flujo de desarrollo continuo cuando sea posible."
    "Asegúrate de que todas las pruebas estén correctamente versionadas y rastreables en el sistema de control de versiones."
)
agent = Agent(role='Ingeniero de pruebas especialista en backend, pruebas de performance, pruebas funcionales y no funcionales', 
              goal="Completar la tarea asignada. Solo enfocado en los issues que te comparte el equipo.",
              backstory="Eres el tester especialista en backend, el cual conoce toda la funcionalidad y el giro de negocio.", llm=llm,
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
