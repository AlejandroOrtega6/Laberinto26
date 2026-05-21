from __future__ import annotations
from typing import Dict, List, Optional
from .contenedor import Contenedor
from .elemento_mapa import ElementoMapa
from .habitacion import Habitacion

class Laberinto(Contenedor):

    def __init__(self):
        super().__init__()
        self._habitaciones: Dict[int, Habitacion] = {}
        self.inicio: Optional[Habitacion] = None
        self.salida: Optional[Habitacion] = None
        self.bichos = []

    def Add(self, componente: ElementoMapa):
        super().Add(componente)
        if isinstance(componente, Habitacion):
            self._habitaciones[componente.num] = componente

    def habitacion(self, numero: int) -> Optional[Habitacion]:
        return self._habitaciones.get(numero)

    def fijar_inicio(self, numero: int):
        self.inicio = self.habitacion(numero)

    def fijar_salida(self, numero: int):
        self.salida = self.habitacion(numero)

    def agregar_bicho(self, bicho):
        if bicho not in self.bichos:
            self.bichos.append(bicho)

    def CreateIterator(self):
        from .iterador import ConcreteIterator
        return ConcreteIterator(self)

    def descripcion(self) -> str:
        return f'Laberinto con {len(self._habitaciones)} habitaciones'

    def aceptar(self, visitante):
        visitante.visitar_laberinto(self)
