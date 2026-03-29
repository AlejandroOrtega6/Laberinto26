from abc import ABC, abstractmethod

from .habitacion import Habitacion
from .pared import Pared
from .puerta import Puerta
from .bomba import Bomba
from .bicho import Bicho


class AbstractFactory(ABC):
    @classmethod
    @abstractmethod
    def Instance(cls):
        pass

    @abstractmethod
    def fabricar_habitacion(self, numero):
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


class ConcreteFactory(AbstractFactory):
    _instancia = None

    @classmethod
    def Instance(cls):
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def fabricar_habitacion(self, numero):
        return Habitacion(numero)

    def fabricar_pared(self):
        return Pared()

    def fabricar_puerta(self, lado1, lado2, abierta=False):
        return Puerta(lado1, lado2, abierta)

    def fabricar_bomba(self, em):
        return Bomba(em)

    def fabricar_bicho(self, nombre, vidas, poder, modo, posicion):
        return Bicho(nombre, vidas, poder, modo, posicion)


class ConcreteFactoryBombas(AbstractFactory):
    _instancia = None

    @classmethod
    def Instance(cls):
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def fabricar_habitacion(self, numero):
        return Habitacion(numero)

    def fabricar_pared(self):
        return Pared()

    def fabricar_puerta(self, lado1, lado2, abierta=False):
        return Puerta(lado1, lado2, abierta)

    def fabricar_bomba(self, em):
        return Bomba(em)

    def fabricar_bicho(self, nombre, vidas, poder, modo, posicion):
        return Bicho(nombre, vidas, poder, modo, posicion)
