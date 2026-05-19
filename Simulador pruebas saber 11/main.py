import os
import sys

# Obtiene la ruta del directorio actual donde está main.py y la añade al sistema de búsqueda de Python
ruta_proyecto = os.path.dirname(os.path.abspath(__file__))
if ruta_proyecto not in sys.path:
    sys.path.insert(0, ruta_proyecto)

import tkinter as tk
from modelo.simulador import SimuladorModelo
from controlador.controlador import SimuladorControlador
from vista.interfaz import SimuladorVista

def main():
    root = tk.Tk()
    
    # 1. Instanciar el modelo de datos
    modelo = SimuladorModelo()
    
    # 2. Instanciar el controlador inyectando el modelo
    controlador = SimuladorControlador(modelo)
    
    # 3. Instanciar la vista inyectando la ventana raíz y su controlador
    vista = SimuladorVista(root, controlador)
    
    # 4. Conectar la vista de regreso al controlador (Enlace bidireccional)
    controlador.asociar_vista(vista)
    
    # Lanzar interfaz en la vista inicial de Login
    vista.mostrar_login()
    
    root.mainloop()

if __name__ == "__main__":
    main()