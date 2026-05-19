class Estudiante:
    def __init__(self, nombre):
        try:
            if not isinstance(nombre, str):
                raise TypeError("El nombre debe ser un texto válido.")
            
            nombre_limpio = nombre.strip()
            if nombre_limpio == "":
                raise ValueError("El nombre no puede estar vacío.")
                
            self.nombre = nombre_limpio
            self.respuestas_usuario = {}  # Guarda {id_pregunta: opcion_seleccionada}
            self.puntaje_final = 0
            
        except Exception as e:
            raise ValueError(f"Error al registrar estudiante: {e}")

    def registrar_respuesta(self, id_pregunta, opcion):
        """Registra la opción que el estudiante eligió para una pregunta."""
        self.respuestas_usuario[id_pregunta] = opcion

    def calcular_puntaje(self, lista_preguntas):
        """Calcula el puntaje de 0 a 500 adaptado para las 10 preguntas del componente."""
        if not lista_preguntas:
            self.puntaje_final = 0
            return self.puntaje_final

        correctas = 0
        for pregunta in lista_preguntas:
            id_p = pregunta["id"]
            if id_p in self.respuestas_usuario:
                if self.respuestas_usuario[id_p] == pregunta["correcta"]:
                    correctas += 1

        # Mapeo exacto: cada pregunta acertada de las 10 aporta 50 puntos netos (10 * 50 = 500)
        self.puntaje_final = correctas * 50
        return self.puntaje_final

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "respuestas": self.respuestas_usuario,
            "puntaje_final": self.puntaje_final
        }