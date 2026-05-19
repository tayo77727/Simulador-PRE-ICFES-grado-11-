class SimuladorControlador:
    def __init__(self, modelo):
        self.modelo = modelo
        self.vista = None  

    def asociar_vista(self, vista):
        self.vista = vista

    def obtener_vista_actual(self):
        return self.modelo.vista_actual

    def obtener_modo_oscuro(self):
        return self.modelo.dark_mode

    def procesar_login(self, nombre_ingresado):
        try:
            self.modelo.validar_nombre_estudiante(nombre_ingresado)
            self.modelo.vista_actual = "menu"
            self.vista.mostrar_menu(self.modelo.nombre_usuario, self.modelo.areas_disponibles)
        except ValueError as e:
            self.vista.mostrar_advertencia("Error de Validación", str(e))
        except TypeError as e:
            self.vista.mostrar_advertencia("Error Crítico de Tipo", str(e))

    def procesar_seleccion_area(self, area_name):
        """Inicializa las 10 preguntas correspondientes al módulo académico."""
        self.modelo.vista_actual = "exam"
        # Le dice al modelo que prepare el paquete de 10 preguntas
        self.modelo.preparar_modulo_examen(area_name)
        self.vista.mostrar_examen(area_name)

    def procesar_respuesta(self, opcion_seleccionada):
        """Guarda la respuesta actual y decide si avanza a la siguiente pregunta o finaliza."""
        try:
            # 1. Registrar la respuesta de la pregunta actual
            self.modelo.registrar_respuesta_estudiante(opcion_seleccionada)
            
            # 2. Intentar avanzar el índice a la siguiente pregunta
            tiene_siguiente = self.modelo.avanzar_siguiente_pregunta()
            
            if tiene_siguiente:
                # Si quedan preguntas (ej. va en la 2 de 10), redibujamos el examen con el nuevo contenido
                self.vista.mostrar_examen(self.modelo.area_actual)
            else:
                # Si ya contestó las 10 preguntas, guardamos el historial clínico en JSON y cerramos
                self.modelo.guardar_progreso_final()
                self.modelo.vista_actual = "results"
                datos_reporte = self.modelo.obtener_diagnostico()
                self.vista.mostrar_resultados(datos_reporte)
                
        except Exception as e:
            self.vista.mostrar_advertencia("Error en Flujo", f"Ocurrió un problema al procesar la respuesta: {e}")

    def procesar_cambio_tema(self):
        self.modelo.dark_mode = not self.modelo.dark_mode
        self.vista.actualizar_colores_tema(self.modelo.dark_mode)
        
        if self.modelo.vista_actual == "login":
            self.vista.mostrar_login(self.modelo.nombre_usuario)
        elif self.modelo.vista_actual == "menu":
            self.vista.mostrar_menu(self.modelo.nombre_usuario, self.modelo.areas_disponibles)
        elif self.modelo.vista_actual == "exam":
            self.vista.mostrar_examen(self.modelo.area_actual)
        elif self.modelo.vista_actual == "results":
            self.vista.mostrar_resultados(self.modelo.obtener_diagnostico())

    def procesar_regreso(self):
        self.modelo.vista_actual = "menu"
        self.vista.mostrar_menu(self.modelo.nombre_usuario, self.modelo.areas_disponibles)

    def procesar_cierre_sesion(self):
        self.modelo.vista_actual = "login"
        self.vista.mostrar_login(self.modelo.nombre_usuario)