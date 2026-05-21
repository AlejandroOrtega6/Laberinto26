from __future__ import annotations
from typing import Dict, List, Optional
from .direcciones import Orientacion
from .elemento_mapa import ElementoMapa

class Contenedor(ElementoMapa):

    def __init__(self):
        super().__init__()
        self._children: List[ElementoMapa] = []
        self._lados: Dict[Orientacion, ElementoMapa] = {}

    def Add(self, componente: ElementoMapa):
        if componente not in self._children:
            self._children.append(componente)
            componente.SetParent(self)

    def Remove(self, componente: ElementoMapa):
        if componente in self._children:
            self._children.remove(componente)
            componente.SetParent(None)

    def GetChild(self, indice: int) -> Optional[ElementoMapa]:
        if 0 <= indice < len(self._children):
            return self._children[indice]
        return None

    def GetChildren(self) -> List[ElementoMapa]:
        return list(self._children)

    def poner_lado(self, orientacion: Orientacion, elemento: ElementoMapa):
        self._lados[orientacion] = elemento
        self.Add(elemento)

    def obtener_lado(self, orientacion: Orientacion) -> Optional[ElementoMapa]:
        return self._lados.get(orientacion)

    def entrar(self, juego):
        if hasattr(juego, 'personaje'):
            juego.personaje.posicion = self
        else:
            juego.habitacion_actual = self

    def descripcion(self) -> str:
        return self.__class__.__name__
