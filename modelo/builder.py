from abc import ABC

from .laberinto import Laberinto
from .modos import Agresivo, Perezoso
from .direcciones import NORTE, SUR, ESTE, OESTE


class Builder(ABC):
    def BuildLaberinto(self):
        pass

    def BuildHabitacion(self, numero):
        pass

    def BuildPuerta(self, num1, orientacion1, num2, orientacion2, abierta=False):
        pass

    def BuildPuertaBomba(self, num1, orientacion1, num2, orientacion2, abierta=False):
        pass

    def BuildParedBomba(self, numero, orientacion):
        pass

    def BuildBicho(self, nombre, vidas, poder, modo, numero_habitacion):
        pass

    def BuildInicio(self, numero):
        pass

    def BuildSalida(self, numero):
        pass

    def GetProduct(self):
        pass


class ConcreteBuilder(Builder):
    def __init__(self, creador):
        self.creador = creador
        self.product = None

    def BuildLaberinto(self):
        self.product = Laberinto()

    def BuildHabitacion(self, numero):
        habitacion = self.creador.fabricar_habitacion(numero)
        habitacion.poner_lado(NORTE, self.creador.fabricar_pared())
        habitacion.poner_lado(SUR, self.creador.fabricar_pared())
        habitacion.poner_lado(ESTE, self.creador.fabricar_pared())
        habitacion.poner_lado(OESTE, self.creador.fabricar_pared())
        self.product.Add(habitacion)

    def BuildPuerta(self, num1, orientacion1, num2, orientacion2, abierta=False):
        h1 = self.product.habitacion(num1)
        h2 = self.product.habitacion(num2)
        puerta = self.creador.fabricar_puerta(h1, h2, abierta)
        h1.poner_lado(orientacion1, puerta)
        h2.poner_lado(orientacion2, puerta)

    def BuildPuertaBomba(self, num1, orientacion1, num2, orientacion2, abierta=False):
        h1 = self.product.habitacion(num1)
        h2 = self.product.habitacion(num2)
        puerta = self.creador.fabricar_puerta_bomba(h1, h2, abierta)
        h1.poner_lado(orientacion1, puerta)
        h2.poner_lado(orientacion2, puerta)

    def BuildParedBomba(self, numero, orientacion):
        habitacion = self.product.habitacion(numero)
        habitacion.poner_lado(orientacion, self.creador.fabricar_pared_bomba())

    def BuildBicho(self, nombre, vidas, poder, modo, numero_habitacion):
        habitacion = self.product.habitacion(numero_habitacion)
        bicho = self.creador.fabricar_bicho(nombre, vidas, poder, modo, habitacion)
        self.product.agregar_bicho(bicho)

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

        for numero in range(1, 7):
            self.builder.BuildHabitacion(numero)

        self.builder.BuildPuerta(1, ESTE, 2, OESTE, True)
        self.builder.BuildPuerta(1, SUR, 4, NORTE, True)
        self.builder.BuildPuertaBomba(2, ESTE, 3, OESTE, True)
        self.builder.BuildPuerta(2, SUR, 5, NORTE, True)
        self.builder.BuildPuerta(3, SUR, 6, NORTE, False)
        self.builder.BuildPuerta(4, ESTE, 5, OESTE, True)
        self.builder.BuildPuertaBomba(5, ESTE, 6, OESTE, True)

        self.builder.BuildParedBomba(4, SUR)
        self.builder.BuildParedBomba(6, ESTE)

        self.builder.BuildBicho("Bicho rojo", 2, 1, Agresivo(), 5)
        self.builder.BuildBicho("Bicho azul", 1, 1, Perezoso(), 3)

        self.builder.BuildInicio(1)
        self.builder.BuildSalida(6)
