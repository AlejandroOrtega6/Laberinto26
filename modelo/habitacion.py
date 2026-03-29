from .contenedor import Contenedor
from .direcciones import TODAS_DIRECCIONES


class Habitacion(Contenedor):
    def __init__(self, numero):
        super().__init__()
        self.numero = numero

    def descripcion(self):
        return f"Habitación {self.numero}"

    def GetChildren(self):
        hijos = []
        vistos = set()
        for direccion in TODAS_DIRECCIONES:
            lado = self.obtener_lado(direccion)
            if lado is not None and id(lado) not in vistos:
                vistos.add(id(lado))
                hijos.append(lado)
        return hijos
