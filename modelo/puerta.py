from __future__ import annotations
from .estado_puerta import Abierta, Cerrada, EstadoPuerta
from .hoja import Hoja

class Puerta(Hoja):

    def __init__(self, lado1, lado2, abierta: bool=False):
        super().__init__()
        self.lado1 = lado1
        self.lado2 = lado2
        self.estado: EstadoPuerta = Abierta() if abierta else Cerrada()

    def entrar(self, juego):
        self.estado.entrar(self, juego)

    def abrir(self) -> bool:
        return self.estado.abrir(self)

    def cerrar(self) -> bool:
        return self.estado.cerrar(self)

    def es_puerta(self) -> bool:
        return True

    def destino_desde(self, origen):
        if origen == self.lado1:
            return self.lado2
        if origen == self.lado2:
            return self.lado1
        return None

    def descripcion(self) -> str:
        return f'Puerta {self.estado.nombre()} entre H{self.lado1.num} y H{self.lado2.num}'

    def aceptar(self, visitante):
        visitante.visitar_puerta(self)
