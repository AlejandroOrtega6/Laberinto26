from __future__ import annotations

class Visitante:

    def visitar_elemento(self, elemento):
        pass

    def visitar_laberinto(self, laberinto):
        self.visitar_elemento(laberinto)

    def visitar_habitacion(self, habitacion):
        self.visitar_elemento(habitacion)

    def visitar_armario(self, armario):
        self.visitar_elemento(armario)

    def visitar_pared(self, pared):
        self.visitar_elemento(pared)

    def visitar_puerta(self, puerta):
        self.visitar_elemento(puerta)

    def visitar_tunel(self, tunel):
        self.visitar_elemento(tunel)

    def visitar_bomba(self, bomba):
        self.visitar_elemento(bomba)

class ContadorVisitante(Visitante):

    def __init__(self):
        self.contadores = {}

    def visitar_elemento(self, elemento):
        nombre = elemento.__class__.__name__
        self.contadores[nombre] = self.contadores.get(nombre, 0) + 1

    def informe(self) -> str:
        if not self.contadores:
            return 'No hay elementos recorridos.'
        return ', '.join((f'{k}: {v}' for k, v in sorted(self.contadores.items())))
