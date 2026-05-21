from __future__ import annotations
from abc import ABC, abstractmethod
from .direcciones import ESTE, NORTE, OESTE, SUR
from .formas import Cuadrado, Rombo
from .modos import Agresivo, Perezoso

class Builder(ABC):

    @abstractmethod
    def BuildLaberinto(self):
        pass

    @abstractmethod
    def BuildHabitacion(self, numero, forma=None):
        pass

    @abstractmethod
    def BuildPuerta(self, num1, orientacion1, num2, orientacion2=None, abierta=False):
        pass

    @abstractmethod
    def BuildPuertaBomba(self, num1, orientacion1, num2, orientacion2=None, abierta=False):
        pass

    @abstractmethod
    def BuildParedBomba(self, numero, orientacion):
        pass

    @abstractmethod
    def BuildBicho(self, nombre, vidas, poder, modo, numero_habitacion):
        pass

    @abstractmethod
    def BuildArmario(self, numero_habitacion, nombre='Armario'):
        pass

    @abstractmethod
    def BuildTunel(self, numero_habitacion, orientacion, destino):
        pass

    @abstractmethod
    def BuildInicio(self, numero):
        pass

    @abstractmethod
    def BuildSalida(self, numero):
        pass

    @abstractmethod
    def GetProduct(self):
        pass

class ConcreteBuilder(Builder):

    def __init__(self, creador):
        self.creador = creador
        self.product = None

    def BuildLaberinto(self):
        self.product = self.creador.fabricarLaberinto()

    def BuildHabitacion(self, numero, forma=None):
        habitacion = self.creador.fabricarHabitacion(numero, forma)
        self.creador.ponerParedes(habitacion)
        self.product.Add(habitacion)

    def BuildPuerta(self, num1, orientacion1, num2, orientacion2=None, abierta=False):
        h1 = self.product.habitacion(num1)
        h2 = self.product.habitacion(num2)
        puerta = self.creador.fabricarPuerta(h1, h2, abierta)
        h1.poner_lado(orientacion1, puerta)
        h2.poner_lado(orientacion2 if orientacion2 is not None else orientacion1.opuesta(), puerta)
        return puerta

    def BuildPuertaBomba(self, num1, orientacion1, num2, orientacion2=None, abierta=False):
        h1 = self.product.habitacion(num1)
        h2 = self.product.habitacion(num2)
        puerta = self.creador.fabricarBomba(self.creador.fabricarPuertaBase(h1, h2, abierta))
        h1.poner_lado(orientacion1, puerta)
        h2.poner_lado(orientacion2 if orientacion2 is not None else orientacion1.opuesta(), puerta)
        return puerta

    def BuildParedBomba(self, numero, orientacion):
        habitacion = self.product.habitacion(numero)
        habitacion.poner_lado(orientacion, self.creador.fabricarBomba(self.creador.fabricarParedBase()))

    def BuildBicho(self, nombre, vidas, poder, modo, numero_habitacion):
        habitacion = self.product.habitacion(numero_habitacion)
        bicho = self.creador.fabricarBicho(nombre, vidas, poder, modo, habitacion)
        self.product.agregar_bicho(bicho)
        return bicho

    def BuildArmario(self, numero_habitacion, nombre='Armario'):
        habitacion = self.product.habitacion(numero_habitacion)
        armario = self.creador.fabricarArmario(nombre)
        habitacion.Add(armario)
        return armario

    def BuildTunel(self, numero_habitacion, orientacion, destino):
        habitacion = self.product.habitacion(numero_habitacion)
        destino_hab = self.product.habitacion(destino)
        tunel = self.creador.fabricarTunel(destino_hab)
        habitacion.poner_lado(orientacion, tunel)
        return tunel

    def BuildInicio(self, numero):
        self.product.fijar_inicio(numero)

    def BuildSalida(self, numero):
        self.product.fijar_salida(numero)

    def GetProduct(self):
        return self.product

class Director:

    def __init__(self, builder):
        self.builder = builder

    def Construct(self):
        self.builder.BuildLaberinto()
        self.builder.BuildHabitacion(1, Cuadrado(1))
        self.builder.BuildHabitacion(2, Cuadrado(2))
        self.builder.BuildHabitacion(3, Cuadrado(3))
        self.builder.BuildHabitacion(4, Rombo(4))
        self.builder.BuildPuerta(1, ESTE, 2, OESTE, True)
        self.builder.BuildPuerta(1, SUR, 3, NORTE, True)
        self.builder.BuildPuerta(2, SUR, 4, NORTE, False)
        self.builder.BuildPuerta(3, ESTE, 4, OESTE, True)
        self.builder.BuildParedBomba(3, SUR)
        self.builder.BuildArmario(1, 'Armario de la habitación 1')
        self.builder.BuildTunel(3, OESTE, 2)
        self.builder.BuildBicho('Bicho rojo', 2, 1, Agresivo(), 3)
        self.builder.BuildBicho('Bicho azul', 1, 1, Perezoso(), 2)
        self.builder.BuildInicio(1)
        self.builder.BuildSalida(4)
