class Pregunta:
    def __init__(self, id_pregunta, area, enunciado, opciones, correcta):
        try:
            self.id = int(id_pregunta)
            self.area = area.strip()
            self.enunciado = enunciado.strip()
            
            if not isinstance(opciones, list) or len(opciones) != 4:
                raise ValueError("Deben ser exactamente 4 opciones de respuesta.")
                
            self.opciones = opciones  # Atributo lógico interno
            self.correcta = correcta.strip()
            
        except Exception as e:
            raise ValueError(f"Error en la estructura de la pregunta: {e}")

    def to_dict(self):
        """Convierte el objeto pregunta a diccionario mapeando a la clave 'options' del JSON."""
        return {
            "id": self.id,
            "area": self.area,
            "enunciado": self.enunciado,
            "options": self.opciones,  # Sincronizado con el archivo externo
            "correcta": self.correcta
        }

    @staticmethod
    def from_dict(data):
        """Instancia un objeto Pregunta desde un diccionario compatible con 'options'."""
        return Pregunta(
            data["id"], 
            data["area"], 
            data["enunciado"], 
            data["options"],  # Sincronizado con el archivo externo
            data["correcta"]
        )