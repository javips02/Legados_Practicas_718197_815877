class Programa:
    def __init__(self, nombre="", tipo="", registro=""):
        self.nombre = nombre
        self.tipo = tipo
        self.registro = registro
    def __repr__(self):
        return f"Programa(nombre={self.nombre}, categoria={self.tipo}, registro={self.registro})"
    def to_dict(self):
        return {
            "nombre": self.nombre,
            "tipo": self.tipo,
            "registro": self.registro
        }