from __future__ import annotations
from abc import ABC, abstractmethod
from .armario import Armario
from .bicho import Bicho
from .bomba import Bomba
from .habitacion import Habitacion
from .laberinto import Laberinto
from .pared import Pared
from .puerta import Puerta
from .tunel import Tunel

class AbstractFactory(ABC):

    @classmethod
    @abstractmethod
    def Instance(cls):
        pass

    @abstractmethod
    def fabricar_laberinto(self):
        pass

    @abstractmethod
    def fabricar_habitacion(self, numero, forma=None):
        pass

    @abstractmethod
    def fabricar_pared(self):
        pass

    @abstractmethod
    def fabricar_puerta(self, lado1, lado2, abierta=False):
        pass

    @abstractmethod
    def fabricar_bomba(self, em):
        pass

    @abstractmethod
    def fabricar_bicho(self, nombre, vidas, poder, modo, posicion):
        pass

    def fabricar_armario(self, nombre='Armario'):
        return Armario(nombre)

    def fabricar_tunel(self, laberinto=None, destino=None):
        return Tunel(laberinto, destino)

class ConcreteFactory(AbstractFactory):
    _instancia = None

    @classmethod
    def Instance(cls):
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def fabricar_laberinto(self):
        return Laberinto()

    def fabricar_habitacion(self, numero, forma=None):
        return Habitacion(numero, forma)

    def fabricar_pared(self):
        return Pared()

    def fabricar_puerta(self, lado1, lado2, abierta=False):
        return Puerta(lado1, lado2, abierta)

    def fabricar_bomba(self, em):
        return Bomba(em)

    def fabricar_bicho(self, nombre, vidas, poder, modo, posicion):
        return Bicho(nombre, vidas, poder, modo, posicion)

class ConcreteFactoryBombas(ConcreteFactory):
    _instancia = None

    @classmethod
    def Instance(cls):
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def fabricar_pared(self):
        return Pared()

    def fabricar_puerta(self, lado1, lado2, abierta=False):
        return Puerta(lado1, lado2, abierta)
