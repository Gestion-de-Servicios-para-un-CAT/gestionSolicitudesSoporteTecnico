from fastapi import FastAPI, HTTPException
import json
import os
import datetime

app = FastAPI()

# Archivo donde se guardan las solicitudes
DATA_FILE = "solicitudes.json"

# Si el archivo no existe, crearlo como lista vacía
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

# Estados permitidos en el sistema
ESTADOS_VALIDOS = ["pendiente", "en_proceso", "resuelta", "cerrada"]


@app.put("/solicitudes/{solicitud_id}/estado")
def actualizar_estado(solicitud_id: int, datos: dict):
    """
    Endpoint para actualizar el estado de una solicitud.
    Recibe un JSON con {"estado": "nuevo_estado"}.
    Incluye un historial básico de cambios.
    """

    nuevo_estado = datos.get("estado")

    # Validar que se envía un estado
    if not nuevo_estado:
        raise HTTPException(status_code=400, detail="Debe enviar el campo 'estado'.")

    # Validar que el estado sea permitido
    if nuevo_estado not in ESTADOS_VALIDOS:
        raise HTTPException(
            status_code=400,
            detail=f"Estado '{nuevo_estado}' no válido. Estados permitidos: {ESTADOS_VALIDOS}"
        )

    # Cargar solicitudes existentes
    with open(DATA_FILE, "r") as f:
        solicitudes = json.load(f)

    # Buscar solicitud por ID
    solicitud = next((s for s in solicitudes if s["id"] == solicitud_id), None)

    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada.")

    # Agregar historial si no existe
    solicitud.setdefault("historial", [])

    # Registrar cambio en historal
    solicitud["historial"].append({
        "estado": nuevo_estado,
        "fecha": datetime.datetime.now().isoformat()
    })

    # Actualizar el estado actual
    solicitud["estado"] = nuevo_estado

    # Guardar cambios
    with open(DATA_FILE, "w") as f:
        json.dump(solicitudes, f, indent=4)

    return {
        "mensaje": "Estado actualizado correctamente.",
        "solicitud": solicitud
    }
