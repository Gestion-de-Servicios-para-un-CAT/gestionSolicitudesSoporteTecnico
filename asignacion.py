from fastapi import FastAPI, HTTPException
import json
import os

app = FastAPI()

# Archivos donde guardaremos datos ficticios
SOLICITUDES_FILE = "solicitudes.json"
TECNICOS_FILE = "tecnicos.json"

# Crear archivos si no existen
if not os.path.exists(SOLICITUDES_FILE):
    with open(SOLICITUDES_FILE, "w") as f:
        json.dump([], f)

if not os.path.exists(TECNICOS_FILE):
    with open(TECNICOS_FILE, "w") as f:
        json.dump(
            [
                {"id": 1, "nombre": "Tecnico A"},
                {"id": 2, "nombre": "Tecnico B"},
                {"id": 3, "nombre": "Tecnico C"}
            ],
            f,
            indent=4
        )


@app.put("/solicitudes/{solicitud_id}/asignar")
def asignar_solicitud(solicitud_id: int, datos: dict):
    """
    Asigna una solicitud a un técnico basado en su ID.
    Recibe un JSON: {"tecnico_id": N}
    No hay validaciones avanzadas, solo lógica mínima.
    """

    tecnico_id = datos.get("tecnico_id")

    # Validar que se envía un técnico
    if not tecnico_id:
        raise HTTPException(status_code=400, detail="Debe enviar 'tecnico_id'.")

    # Cargar solicitudes
    with open(SOLICITUDES_FILE, "r") as f:
        solicitudes = json.load(f)

    # Cargar técnicos
    with open(TECNICOS_FILE, "r") as f:
        tecnicos = json.load(f)

    # Buscar solicitud
    solicitud = next((s for s in solicitudes if s["id"] == solicitud_id), None)
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada.")

    # Buscar técnico
    tecnico = next((t for t in tecnicos if t["id"] == tecnico_id), None)
    if not tecnico:
        raise HTTPException(status_code=404, detail="Técnico no encontrado.")

    # Asignar técnico a la solicitud
    solicitud["tecnico_asignado"] = tecnico_id

    # Guardar cambios
    with open(SOLICITUDES_FILE, "w") as f:
        json.dump(solicitudes, f, indent=4)

    return {
        "mensaje": "Solicitud asignada correctamente.",
        "solicitud": solicitud,
        "tecnico": tecnico
    }
