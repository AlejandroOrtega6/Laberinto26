from __future__ import annotations
from .ente import Ente

class Personaje(Ente):

    def __init__(self, nombre: str, vidas: int=3, poder: int=1):
        super().__init__(vidas, poder)
        self.nombre = nombre
        self.posicion = None

    def descripcion(self) -> str:
        pos = self.posicion.descripcion() if self.posicion is not None else 'sin posición'
        return f'{self.nombre} [{self.estado.nombre()} | vidas={self.vidas} | poder={self.poder} | {pos}]'
