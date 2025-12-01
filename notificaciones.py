from fastapi import FastAPI
import json
import os
import datetime

app = FastAPI()

# Archivo donde se almacenarán las notificaciones
NOTIF_FILE = "notificaciones.json"

# Crear archivo si no existe
if not os.path.exists(NOTIF_FILE):
    with open(NOTIF_FILE, "w") as f:
        json.dump([], f, indent=4)


def guardar_notificacion(tipo: str, mensaje: str, usuario: str):
    """
    Función simple para registrar notificaciones dentro de un archivo JSON.
    Se puede llamar desde cualquier módulo/evento del sistema.
    """

    # Cargar notificaciones existentes
    with open(NOTIF_FILE, "r") as f:
        notificaciones = json.load(f)

    nueva_notificacion = {
        "id": len(notificaciones) + 1,
        "tipo": tipo,               # tipo de evento (estado, asignación, creación)
        "mensaje": mensaje,         # texto de la notificación
        "usuario": usuario,         # usuario al que va dirigida
        "fecha": datetime.datetime.now().isoformat()
    }

    notificaciones.append(nueva_notificacion)

    # Guardar notificaciones
    with open(NOTIF_FILE, "w") as f:
        json.dump(notificaciones, f, indent=4)

    return nueva_notificacion


@app.get("/notificaciones")
def listar_notificaciones():
    """Devuelve todas las notificaciones generadas."""
    with open(NOTIF_FILE, "r") as f:
        notificaciones = json.load(f)
    return notificaciones


@app.post("/notificaciones/prueba")
def generar_notificacion_prueba():
    """
    Endpoint para generar una notificación de prueba.
    Útil para validar que el módulo funciona.
    """
    notificacion = guardar_notificacion(
        tipo="prueba",
        mensaje="Esto es una notificación de prueba.",
        usuario="usuario_demo"
    )
    return {"mensaje": "Notificación creada", "notificacion": notificacion}
