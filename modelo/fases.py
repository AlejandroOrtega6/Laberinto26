from __future__ import annotations
from abc import ABC, abstractmethod

class Fase(ABC):

    @abstractmethod
    def ejecutar(self, juego):
        pass

    @abstractmethod
    def nombre(self) -> str:
        pass

class Inicial(Fase):

    def ejecutar(self, juego):
        juego.preparar()
        juego.fase = Jugando()

    def nombre(self) -> str:
        return 'inicial'

class Jugando(Fase):

    def ejecutar(self, juego):
        juego.mostrar_estado()
        texto = input('Orden: ')
        comando = juego.interprete.interpretar(texto)
        comando.ejecutar(juego)
        juego.comprobar_fin()
        if isinstance(juego.fase, Jugando):
            juego.turno_bichos()
            juego.comprobar_fin()
            juego.turno += 1

    def nombre(self) -> str:
        return 'jugando'

class Final(Fase):

    def ejecutar(self, juego):
        juego.mostrar_final()

    def nombre(self) -> str:
        return 'final'
