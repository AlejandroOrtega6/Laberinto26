from __future__ import annotations
from .hoja import Hoja

class Tunel(Hoja):

    def __init__(self, laberinto=None, destino=None):
        super().__init__()
        self.laberinto = laberinto
        self.destino = destino

    def entrar(self, juego):
        if self.destino is None:
            print('El túnel no tiene destino configurado.')
            return
        if hasattr(juego, 'personaje'):
            juego.personaje.posicion = self.destino
        else:
            juego.habitacion_actual = self.destino
        print(f'El túnel te lleva a {self.destino.descripcion()}.')

    def descripcion(self) -> str:
        if self.destino is None:
            return 'Túnel sin destino'
        return f'Túnel hacia H{self.destino.num}'

    def aceptar(self, visitante):
        visitante.visitar_tunel(self)
