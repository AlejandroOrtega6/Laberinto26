from __future__ import annotations
from .contenedor import Contenedor

class Armario(Contenedor):

    def __init__(self, nombre: str='Armario'):
        super().__init__()
        self.nombre = nombre

    def descripcion(self) -> str:
        return self.nombre

    def entrar(self, juego):
        print(f'Entras en {self.nombre}. Es un contenedor, pero no cambia de habitación.')

    def aceptar(self, visitante):
        visitante.visitar_armario(self)
