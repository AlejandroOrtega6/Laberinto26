from __future__ import annotations
import random
from abc import ABC, abstractmethod
from collections import deque

class Modo(ABC):

    @abstractmethod
    def actua(self, bicho, juego):
        pass

    @abstractmethod
    def nombre(self) -> str:
        pass

    def atacar(self, bicho, juego):
        print(f'{bicho.nombre} ataca a {juego.personaje.nombre}.')
        juego.personaje.recibir_danio(bicho.poder)
        print(f'A {juego.personaje.nombre} le queda(n) {juego.personaje.vidas} vida(s).')
        if juego.personaje.esta_muerto():
            juego.terminar_por_muerte()

    def siguiente_hacia_personaje(self, bicho, juego):
        origen = bicho.posicion
        destino = juego.personaje.posicion
        if origen == destino:
            return origen
        cola = deque([(origen, [])])
        visitadas = {origen}
        while cola:
            actual, camino = cola.popleft()
            for vecino in juego.vecinos_accesibles(actual):
                if vecino in visitadas:
                    continue
                nuevo_camino = camino + [vecino]
                if vecino == destino:
                    return nuevo_camino[0]
                visitadas.add(vecino)
                cola.append((vecino, nuevo_camino))
        return None

    def caminar_aleatorio(self, bicho, juego):
        vecinos = juego.vecinos_accesibles(bicho.posicion)
        if vecinos:
            bicho.posicion = random.choice(vecinos)
            print(f'{bicho.nombre} se mueve a {bicho.posicion.descripcion()}.')
        else:
            print(f'{bicho.nombre} no puede moverse.')

    def caminar_hacia_personaje(self, bicho, juego):
        siguiente = self.siguiente_hacia_personaje(bicho, juego)
        if siguiente is not None and siguiente != bicho.posicion:
            bicho.posicion = siguiente
            print(f'{bicho.nombre} avanza hacia ti y entra en {bicho.posicion.descripcion()}.')
        else:
            self.caminar_aleatorio(bicho, juego)

class Agresivo(Modo):

    def actua(self, bicho, juego):
        if bicho.posicion == juego.personaje.posicion:
            self.atacar(bicho, juego)
        else:
            self.caminar_hacia_personaje(bicho, juego)

    def nombre(self) -> str:
        return 'agresivo'

class Perezoso(Modo):

    def actua(self, bicho, juego):
        if bicho.posicion == juego.personaje.posicion:
            self.atacar(bicho, juego)
        elif random.random() < 0.45:
            self.caminar_hacia_personaje(bicho, juego)
        else:
            print(f'{bicho.nombre} vigila la zona y no se mueve.')

    def nombre(self) -> str:
        return 'perezoso'
