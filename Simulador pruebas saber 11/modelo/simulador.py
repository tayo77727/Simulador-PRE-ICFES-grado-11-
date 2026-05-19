import random
from modelo.estudiante import Estudiante
from modelo import persistencia

class SimuladorModelo:
    def __init__(self):
        self.estudiante_actual = None
        self.nombre_usuario = ""
        self.area_actual = ""
        self.vista_actual = "login"
        self.dark_mode = False
        
        self.banco_completo = persistencia.cargar_banco_preguntas()
        self.preguntas_filtradas = []  
        self.pregunta_actual_index = 0 
        self.pregunta_en_pantalla = None  
        
        self.areas_disponibles = [
            ("Matemáticas", "📐"), 
            ("Lectura Crítica", "📖"), 
            ("Ciencias Naturales", "🔬"), 
            ("Sociales y Ciudadanas", "⚖️"), 
            ("Inglés", "🌍")
        ]

    def validar_nombre_estudiante(self, nombre):
        if not isinstance(nombre, str):
            raise TypeError("El nombre del estudiante debe ser un texto válido.")
        nombre_limpio = nombre.strip()
        if nombre_limpio == "":
            raise ValueError("El nombre del estudiante no puede estar vacío.")
        if len(nombre_limpio) < 3:
            raise ValueError("El nombre debe contener un mínimo de 3 caracteres.")
        
        self.nombre_usuario = nombre_limpio
        self.estudiante_actual = Estudiante(self.nombre_usuario)

    def preparar_modulo_examen(self, area_name):
        """Filtra las preguntas del área, las mezcla aleatoriamente y toma un bloque de 10."""
        self.area_actual = area_name
        todas_del_area = [p for p in self.banco_completo if p["area"] == area_name]
        
        # Mezclamos el mazo de preguntas completo del área
        random.shuffle(todas_del_area)
        
        # Tomamos el subconjunto de máximo 10 preguntas
        self.preguntas_filtradas = todas_del_area[:10]
        self.pregunta_actual_index = 0
        
        if self.preguntas_filtradas:
            self.pregunta_en_pantalla = self.preguntas_filtradas[self.pregunta_actual_index]
            # Desordenamos las opciones de esta primera pregunta
            random.shuffle(self.pregunta_en_pantalla["options"])
            return self.pregunta_en_pantalla
        return None

    def avanzar_siguiente_pregunta(self):
        """Incrementa el índice y desordena las opciones de la nueva pregunta."""
        self.pregunta_actual_index += 1
        if self.pregunta_actual_index < len(self.preguntas_filtradas):
            self.pregunta_en_pantalla = self.preguntas_filtradas[self.pregunta_actual_index]
            # Desordenamos las opciones de la siguiente pregunta
            random.shuffle(self.pregunta_en_pantalla["options"])
            return True
        self.pregunta_en_pantalla = None
        return False

    def registrar_respuesta_estudiante(self, opcion_seleccionada):
        if self.estudiante_actual and self.pregunta_en_pantalla:
            id_p = self.pregunta_en_pantalla["id"]
            self.estudiante_actual.registrar_respuesta(id_p, opcion_seleccionada)
            self.estudiante_actual.calcular_puntaje(self.preguntas_filtradas)

    def guardar_progreso_final(self):
        if self.estudiante_actual:
            datos = self.estudiante_actual.to_dict()
            persistencia.guardar_resultado_estudiante(datos)

    def obtener_diagnostico(self):
        puntaje = self.estudiante_actual.puntaje_final if self.estudiante_actual else 0
        if puntaje >= 300:
            return {
                "aprobado": True,
                "puntaje": f"{puntaje} / 500",
                "mensaje": "¡Simulación Completada con Éxito!",
                "retroalimentacion": f"Felicitaciones {self.nombre_usuario}, has superado el umbral mínimo requerido para aprobar el componente de {self.area_actual}."
            }
        else:
            return {
                "aprobado": False,
                "puntaje": f"{puntaje} / 500",
                "mensaje": "Resultados de la Evaluación",
                "retroalimentacion": f"Estimado(a) {self.nombre_usuario}, tu puntaje en {self.area_actual} no alcanza el mínimo de 300 puntos. Te recomendamos repasar los temas de este componente."
            }