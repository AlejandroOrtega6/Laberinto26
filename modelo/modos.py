import random
from abc import ABC, abstractmethod


class Modo(ABC):
    @abstractmethod
    def actua(self, un_bicho, juego):
        pass

    @abstractmethod
    def nombre(self):
        pass


class Agresivo(Modo):
    def actua(self, un_bicho, juego):
        if un_bicho.posicion == juego.habitacion_actual:
            print(f"{un_bicho.nombre} te ataca con fuerza {un_bicho.poder}.")
            juego.recibir_danio(un_bicho.poder, un_bicho.nombre)
            return

        vecinos = juego.vecinos_accesibles(un_bicho.posicion)
        if vecinos:
            destino = random.choice(vecinos)
            un_bicho.posicion = destino
            print(f"{un_bicho.nombre} corre hasta la habitación {destino.numero}.")

    def nombre(self):
        return "Agresivo"


class Perezoso(Modo):
    def actua(self, un_bicho, juego):
        if un_bicho.posicion == juego.habitacion_actual and random.random() < 0.4:
            print(f"{un_bicho.nombre} te golpea sin muchas ganas.")
            juego.recibir_danio(un_bicho.poder, un_bicho.nombre)
            return

        if random.random() < 0.6:
            print(f"{un_bicho.nombre} se queda dormido.")
            return

        vecinos = juego.vecinos_accesibles(un_bicho.posicion)
        if vecinos:
            destino = random.choice(vecinos)
            un_bicho.posicion = destino
            print(f"{un_bicho.nombre} se arrastra hasta la habitación {destino.numero}.")

    def nombre(self):
        return "Perezoso"
