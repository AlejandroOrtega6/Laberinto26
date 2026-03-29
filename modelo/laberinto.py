from .contenedor import Contenedor
from .habitacion import Habitacion
from .iterador import ConcreteIterator


class Laberinto(Contenedor):
    def __init__(self):
        super().__init__()
        self._habitaciones = {}
        self.inicio = None
        self.salida = None
        self.bichos = []

    def Add(self, componente):
        super().Add(componente)
        if isinstance(componente, Habitacion):
            self._habitaciones[componente.numero] = componente

    def habitacion(self, numero):
        return self._habitaciones.get(numero)

    def fijar_inicio(self, numero):
        self.inicio = self.habitacion(numero)

    def fijar_salida(self, numero):
        self.salida = self.habitacion(numero)

    def agregar_bicho(self, bicho):
        self.bichos.append(bicho)

    def descripcion(self):
        return "Laberinto"

    def GetChildren(self):
        return list(self._habitaciones.values())

    def CreateIterator(self):
        return ConcreteIterator(self)
