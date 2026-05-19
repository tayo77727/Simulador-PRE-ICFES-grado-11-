import json
import os

# 1. Definimos la carpeta contenedora
CARPETA_DATOS = "datos"

# 2. Construimos las rutas unificadas apuntando dentro de la carpeta datos
ARCHIVO_PREGUNTAS = os.path.join(CARPETA_DATOS, "preguntas_banco.json")
ARCHIVO_RESULTADOS = os.path.join(CARPETA_DATOS, "datosEstudiantes.json")

def asegurar_carpeta_existente():
    """Verifica si la carpeta 'datos' existe en el directorio, de lo contrario la crea."""
    if not os.path.exists(CARPETA_DATOS):
        os.makedirs(CARPETA_DATOS)

def cargar_banco_preguntas():
    """Carga el banco de preguntas desde la carpeta datos."""
    asegurar_carpeta_existente()
    
    if not os.path.exists(ARCHIVO_PREGUNTAS):
        return []

    with open(ARCHIVO_PREGUNTAS, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_resultado_estudiante(datos_estudiante):
    """Guarda o añade el progreso del estudiante en la carpeta de datos sin borrar anteriores."""
    asegurar_carpeta_existente()
    
    historial = []

    if os.path.exists(ARCHIVO_RESULTADOS):
        try:
            with open(ARCHIVO_RESULTADOS, "r", encoding="utf-8") as f:
                historial = json.load(f)
        except json.JSONDecodeError:
            historial = []

    # Añadimos el nuevo diccionario del estudiante
    historial.append(datos_estudiante)

    # Escribimos los datos de manera limpia en el JSON local
    with open(ARCHIVO_RESULTADOS, "w", encoding="utf-8") as f:
        json.dump(historial, f, indent=4, ensure_ascii=False)