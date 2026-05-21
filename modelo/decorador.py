from __future__ import annotations
from typing import List
from .elemento_mapa import ElementoMapa
from .hoja import Hoja

class Decorator(Hoja):

    def __init__(self, em: ElementoMapa):
        super().__init__()
        self.em = em

    def entrar(self, juego):
        self.em.entrar(juego)

    def descripcion(self) -> str:
        return self.em.descripcion()

    def abrir(self) -> bool:
        return self.em.abrir()

    def es_puerta(self) -> bool:
        return self.em.es_puerta()

    def destino_desde(self, origen):
        return self.em.destino_desde(origen)

    def GetChildren(self) -> List[ElementoMapa]:
        return [self.em]
