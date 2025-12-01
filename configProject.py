import os

# Estructura de carpetas del proyecto
folders = [
    "app",
    "app/routes",
    "app/models",
    "app/controllers",
    "app/services",
    "app/utils",
    "config",
    "tests"
]

# Archivos base a generar
files = {
    "app/__init__.py": "# Inicialización del módulo app\n",
    "app/routes/__init__.py": "# Rutas del sistema\n",
    "app/models/__init__.py": "# Modelos de datos\n",
    "app/controllers/__init__.py": "# Controladores del sistema\n",
    "app/services/__init__.py": "# Servicios auxiliares\n",
    "app/utils/__init__.py": "# Utilidades\n",
    "config/settings.py": "DEBUG = True\nDATABASE_URL = 'postgresql://user:pass@localhost:5432/cat'\n",
    "main.py": "from app.routes import *\n\nprint('Sistema CAT inicializado (modo base)')\n",
    "tests/test_placeholder.py": "def test_placeholder():\n    assert True\n"
}

def create_structure():
    print("Creando estructura base del proyecto...\n")

    # Crear carpetas
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"Carpeta creada: {folder}")

    # Crear archivos
    for filepath, content in files.items():
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Archivo creado: {filepath}")

    print("\nEstructura base generada correctamente.")

if __name__ == "__main__":
    create_structure()
