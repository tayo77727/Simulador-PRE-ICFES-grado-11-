import tkinter as tk
from tkinter import messagebox

class SimuladorVista:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador  
        
        self.root.title("Software de Simulación Adaptativa - Saber 11°")
        self.root.geometry("1100x800")
        
        # Paletas de colores dinámicas
        self.themes = {
            "light": {
                "bg": "#F8F9FA", "fg": "#212529", "card": "#FFFFFF",
                "accent": "#0D6EFD", "secondary": "#6C757D", "btn_fg": "white"
            },
            "dark": {
                "bg": "#121212", "fg": "#E0E0E0", "card": "#1E1E1E",
                "accent": "#BB86FC", "secondary": "#2D2D2D", "btn_fg": "black"
            }
        }
        self.current_theme = self.themes["light"]
        
        self.container = tk.Frame(self.root, bg=self.current_theme["bg"])
        self.container.pack(fill="both", expand=True)

    def clear_container(self):
        """Limpia la pantalla para el cambio de escena."""
        for widget in self.container.winfo_children():
            widget.destroy()

    def actualizar_colores_tema(self, es_oscuro):
        """Actualiza el diccionario de temas basándose en el estado del modelo."""
        self.current_theme = self.themes["dark"] if es_oscuro else self.themes["light"]
        self.container.configure(bg=self.current_theme["bg"])

    def crear_barra_navegacion(self, titulo, mostrar_regresar=True):
        """Genera el header adaptativo de la app."""
        t = self.current_theme
        nav_bar = tk.Frame(self.container, bg=t["card"], height=60, pady=10)
        nav_bar.pack(fill="x", side="top")

        if mostrar_regresar and self.controlador.obtener_vista_actual() != "login":
            btn_back = tk.Button(nav_bar, text="⬅ Regresar", font=("Arial", 10, "bold"),
                                 bg=t["secondary"], fg="white", bd=0, padx=15, 
                                 command=self.controlador.procesar_regreso, cursor="hand2")
            btn_back.pack(side="left", padx=20)

        tk.Label(nav_bar, text=titulo, font=("Helvetica", 14, "bold"), 
                 bg=t["card"], fg=t["fg"]).pack(side="left", padx=20)

        btn_text = "☀️ Modo Claro" if self.controlador.obtener_modo_oscuro() else "🌙 Modo Oscuro"
        theme_btn = tk.Button(nav_bar, text=btn_text, command=self.controlador.procesar_cambio_tema,
                              bg=t["accent"], fg=t["btn_fg"], font=("Arial", 10, "bold"),
                              relief="flat", padx=15, pady=5, cursor="hand2")
        theme_btn.pack(side="right", padx=20)

    # --- PANTALLA 1: LOGIN ---
    def mostrar_login(self, nombre_previo=""):
        self.clear_container()
        t = self.current_theme
        self.crear_barra_navegacion("Acceso al Sistema", mostrar_regresar=False)
        
        login_card = tk.Frame(self.container, bg=t["card"], padx=50, pady=50)
        login_card.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(login_card, text="Simulador Saber 11°", font=("Helvetica", 24, "bold"), 
                 bg=t["card"], fg=t["fg"]).pack(pady=(0, 10))
        
        tk.Label(login_card, text="Nombre del Estudiante:", font=("Helvetica", 11), 
                 bg=t["card"], fg=t["secondary"]).pack(anchor="w")
        
        self.entry_user = tk.Entry(login_card, font=("Helvetica", 14), width=30, bd=1, 
                                   bg=t["bg"], fg=t["fg"], insertbackground=t["fg"])
        self.entry_user.pack(pady=15)
        self.entry_user.insert(0, nombre_previo)
        
        tk.Button(login_card, text="COMENZAR", bg=t["accent"], fg=t["btn_fg"], 
                  font=("Helvetica", 12, "bold"), width=25, pady=12, 
                  command=lambda: self.controlador.procesar_login(self.entry_user.get()), 
                  relief="flat", cursor="hand2").pack(pady=20)

    # --- PANTALLA 2: MENÚ DE ÁREAS ---
    def mostrar_menu(self, nombre_estudiante, areas):
        self.clear_container()
        t = self.current_theme
        self.crear_barra_navegacion(f"Panel Académico - Estudiante: {nombre_estudiante}", mostrar_regresar=False)
        
        main_frame = tk.Frame(self.container, bg=t["bg"])
        main_frame.pack(expand=True, fill="both", padx=50, pady=20)

        tk.Label(main_frame, text="Selecciona el área de evaluación", font=("Helvetica", 18), 
                 bg=t["bg"], fg=t["fg"]).pack(pady=20)
        
        buttons_container = tk.Frame(main_frame, bg=t["bg"])
        buttons_container.pack()

        for area, icon in areas:
            tk.Button(buttons_container, text=f"{icon}  {area}", 
                      font=("Helvetica", 14, "bold"), width=35, pady=20,
                      bg=t["card"], fg=t["fg"], relief="flat",
                      highlightbackground=t["accent"], highlightthickness=1,
                      cursor="hand2", 
                      command=lambda a=area: self.controlador.procesar_seleccion_area(a)).pack(pady=10)

        tk.Button(main_frame, text="Cerrar Sesión", font=("Helvetica", 11, "underline"), bg=t["bg"], 
                  fg="red", bd=0, command=self.controlador.procesar_cierre_sesion, cursor="hand2").pack(pady=20)

    # --- PANTALLA 3: CUESTIONARIO (EXAMEN CONTINUO) ---
    def mostrar_examen(self, area_name):
        self.clear_container()
        t = self.current_theme
        
        # Consultamos el estado actual del paquete de preguntas en el modelo
        pregunta_data = self.controlador.modelo.pregunta_en_pantalla
        num_preg = self.controlador.modelo.pregunta_actual_index + 1
        
        self.crear_barra_navegacion(f"Examen de {area_name} ({num_preg} de 10)", mostrar_regresar=True)
        
        exam_frame = tk.Frame(self.container, bg=t["bg"], pady=40)
        exam_frame.pack(fill="both", expand=True)

        if pregunta_data:
            tk.Label(exam_frame, text=pregunta_data["enunciado"], font=("Helvetica", 14, "bold"), 
                     bg=t["bg"], fg=t["fg"], wraplength=800).pack(pady=30)
            
            # Recorremos el arreglo de opciones mapeado del JSON
            for opt in pregunta_data["options"]:
                tk.Button(exam_frame, text=opt, font=("Helvetica", 12), width=60, pady=12, 
                          bg=t["card"], fg=t["fg"], relief="flat", anchor="w", padx=30,
                          command=lambda o=opt: self.controlador.procesar_respuesta(o), cursor="hand2").pack(pady=8)
        else:
            tk.Label(exam_frame, text="No hay preguntas disponibles en este momento.", 
                     font=("Helvetica", 12, "italic"), bg=t["bg"], fg="red").pack(pady=50)

    # --- PANTALLA 4: RESULTADOS PEDAGÓGICOS ---
    def mostrar_resultados(self, datos_reporte):
        self.clear_container()
        t = self.current_theme
        self.crear_barra_navegacion("Resultados Finales", mostrar_regresar=True)
        
        res_card = tk.Frame(self.container, bg=t["card"], padx=60, pady=40, relief="flat")
        res_card.place(relx=0.5, rely=0.5, anchor="center")
        
        if datos_reporte["aprobado"]:
            color_titulo = t["accent"]
            color_puntaje = "#198754" 
        else:
            color_titulo = "#DC3545"  
            color_puntaje = "#6C757D" 

        tk.Label(res_card, text=datos_reporte["mensaje"], font=("Helvetica", 22, "bold"), 
                 bg=t["card"], fg=color_titulo).pack(pady=10)
        
        tk.Label(res_card, text=datos_reporte["retroalimentacion"], font=("Helvetica", 12), 
                 bg=t["card"], fg=t["fg"], wraplength=500).pack()
        
        tk.Label(res_card, text="Puntaje Obtenido:", font=("Helvetica", 14), 
                 bg=t["card"], fg=t["secondary"]).pack(pady=(20, 0))
        
        tk.Label(res_card, text=datos_reporte["puntaje"], font=("Helvetica", 48, "bold"), 
                 bg=t["card"], fg=color_puntaje).pack(pady=10)
        
        tk.Button(res_card, text="Finalizar y Salir", bg=t["accent"], fg=t["btn_fg"], 
                  font=("Helvetica", 12, "bold"), width=20, pady=10, 
                  command=self.controlador.procesar_cierre_sesion, relief="flat", cursor="hand2").pack(pady=20)

    def mostrar_advertencia(self, titulo, mensaje):
        messagebox.showwarning(titulo, mensaje)