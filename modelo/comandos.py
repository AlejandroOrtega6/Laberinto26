from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from .direcciones import Orientacion

class Comando(ABC):

    @abstractmethod
    def ejecutar(self, juego):
        pass

@dataclass
class Mover(Comando):
    orientacion: Orientacion

    def ejecutar(self, juego):
        juego.mover(self.orientacion)

@dataclass
class Abrir(Comando):
    orientacion: Orientacion

    def ejecutar(self, juego):
        juego.abrir(self.orientacion)

class Atacar(Comando):

    def ejecutar(self, juego):
        juego.atacar_bicho()

class MostrarMapa(Comando):

    def ejecutar(self, juego):
        juego.mostrar_mapa()

class Salir(Comando):

    def ejecutar(self, juego):
        juego.finalizar()

class Ayuda(Comando):

    def ejecutar(self, juego):
        juego.mostrar_ayuda()

class ComandoNulo(Comando):

    def __init__(self, mensaje: str):
        self.mensaje = mensaje

    def ejecutar(self, juego):
        print(self.mensaje)
