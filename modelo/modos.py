from __future__ import annotations
import random
from abc import ABC, abstractmethod
from collections import deque

class Modo(ABC):

    def actua(self, bicho, juego):
        if not self.puede_actuar(bicho, juego):
            return
        if self.esta_en_la_misma_habitacion(bicho, juego):
            self.atacar(bicho, juego)
            return
        if self.debe_caminar(bicho, juego):
            self.caminar(bicho, juego)
        else:
            self.esperar(bicho, juego)

    def puede_actuar(self, bicho, juego) -> bool:
        return bicho.esta_vivo() and not juego.personaje.esta_muerto()

    def esta_en_la_misma_habitacion(self, bicho, juego) -> bool:
        return bicho.posicion == juego.personaje.posicion

    @abstractmethod
    def debe_caminar(self, bicho, juego) -> bool:
        pass

    def caminar(self, bicho, juego):
        self.caminar_aleatorio(bicho, juego)

    def esperar(self, bicho, juego):
        print(f'{bicho.nombre} vigila la zona y no se mueve.')

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

    def debe_caminar(self, bicho, juego) -> bool:
        return True

    def caminar(self, bicho, juego):
        self.caminar_hacia_personaje(bicho, juego)

    def nombre(self) -> str:
        return 'agresivo'

class Perezoso(Modo):

    def debe_caminar(self, bicho, juego) -> bool:
        return random.random() < 0.45

    def caminar(self, bicho, juego):
        self.caminar_hacia_personaje(bicho, juego)

    def nombre(self) -> str:
        return 'perezoso'
