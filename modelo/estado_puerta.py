from __future__ import annotations
from abc import ABC, abstractmethod

class EstadoPuerta(ABC):

    @abstractmethod
    def entrar(self, puerta, juego):
        pass

    @abstractmethod
    def abrir(self, puerta) -> bool:
        pass

    @abstractmethod
    def nombre(self) -> str:
        pass

class Abierta(EstadoPuerta):

    def entrar(self, puerta, juego):
        origen = juego.personaje.posicion if hasattr(juego, 'personaje') else juego.habitacion_actual
        destino = puerta.destino_desde(origen)
        if destino is None:
            print('La puerta no conecta con esta habitación.')
            return
        if hasattr(juego, 'personaje'):
            juego.personaje.posicion = destino
        else:
            juego.habitacion_actual = destino
        print(f'Cruzas la puerta y entras en {destino.descripcion()}.')

    def abrir(self, puerta) -> bool:
        return True

    def nombre(self) -> str:
        return 'abierta'

class Cerrada(EstadoPuerta):

    def entrar(self, puerta, juego):
        print('La puerta está cerrada. Usa: abrir <dirección>.')

    def abrir(self, puerta) -> bool:
        puerta.estado = Abierta()
        return True

    def nombre(self) -> str:
        return 'cerrada'
