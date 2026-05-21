from __future__ import annotations
from .hoja import Hoja

class Pared(Hoja):

    def entrar(self, juego):
        print('Te has chocado contra una pared.')

    def descripcion(self) -> str:
        return 'Pared'

    def aceptar(self, visitante):
        visitante.visitar_pared(self)
