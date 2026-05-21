from __future__ import annotations
from abc import ABC
from .estado_ente import Muerto, Vivo

class Ente(ABC):

    def __init__(self, vidas: int, poder: int):
        self.vidas = vidas
        self.poder = poder
        self.estado = Vivo() if vidas > 0 else Muerto()

    def esta_vivo(self) -> bool:
        return self.estado.esta_vivo()

    def esta_muerto(self) -> bool:
        return not self.esta_vivo()

    def recibir_danio(self, cantidad: int):
        if self.esta_muerto():
            return
        self.vidas -= cantidad
        if self.vidas <= 0:
            self.vidas = 0
            self.estado = Muerto()
