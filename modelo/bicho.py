from __future__ import annotations
from .ente import Ente

class Bicho(Ente):

    def __init__(self, nombre: str, vidas: int, poder: int, modo, posicion):
        super().__init__(vidas, poder)
        self.nombre = nombre
        self.modo = modo
        self.posicion = posicion

    def actua(self, juego):
        if self.esta_vivo():
            self.modo.actua(self, juego)

    def descripcion(self) -> str:
        return f'{self.nombre} [{self.modo.nombre()} | {self.estado.nombre()} | vidas={self.vidas} | poder={self.poder} | H{self.posicion.num}]'
