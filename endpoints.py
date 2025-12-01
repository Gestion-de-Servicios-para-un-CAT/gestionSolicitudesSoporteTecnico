from fastapi import FastAPI
import json
import os

app = FastAPI()

# Archivo donde se almacenarán las solicitudes
DATA_FILE = "solicitudes.json"

# Crear archivo si no existe
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)


@app.post("/solicitudes")
def crear_solicitud(data: dict):
    """
    Endpoint simple que recibe un diccionario con datos mínimos
    y guarda la solicitud en un JSON.
    No incluye validaciones avanzadas.
    """
    # Leer solicitudes existentes
    with open(DATA_FILE, "r") as f:
        solicitudes = json.load(f)

    # Agregar nueva solicitud
    nueva_solicitud = {
        "id": len(solicitudes) + 1,  # ID simple incremental
        "usuario": data.get("usuario"),
        "categoria": data.get("categoria"),
        "descripcion": data.get("descripcion"),
        "estado": "pendiente"
    }

    solicitudes.append(nueva_solicitud)

    # Guardar cambios
    with open(DATA_FILE, "w") as f:
        json.dump(solicitudes, f, indent=4)

    return {
        "mensaje": "Solicitud registrada",
        "solicitud": nueva_solicitud
    }
