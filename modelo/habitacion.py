from __future__ import annotations
from typing import List, Optional, Set
from .contenedor import Contenedor
from .elemento_mapa import ElementoMapa
from .formas import Cuadrado, Forma

class Habitacion(Contenedor):

    def __init__(self, numero: int, forma: Optional[Forma]=None):
        super().__init__()
        self.num = numero
        self.numero = numero
        self.forma = forma if forma is not None else Cuadrado(numero)

    def descripcion(self) -> str:
        return f'Habitación {self.num}'

    def GetChildren(self) -> List[ElementoMapa]:
        hijos: List[ElementoMapa] = []
        vistos: Set[int] = set()
        for orientacion in self.forma.orientaciones():
            lado = self.obtener_lado(orientacion)
            if lado is not None and id(lado) not in vistos:
                vistos.add(id(lado))
                hijos.append(lado)
        for hijo in self._children:
            if id(hijo) not in vistos:
                vistos.add(id(hijo))
                hijos.append(hijo)
        return hijos

    def aceptar(self, visitante):
        visitante.visitar_habitacion(self)
