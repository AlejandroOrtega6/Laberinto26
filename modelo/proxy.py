from __future__ import annotations

class ProxyLaberinto:

    def __init__(self, constructor=None):
        self.constructor = constructor
        self.laberinto = None

    def configurar(self, laberinto):
        self.laberinto = laberinto

    def disponible(self) -> bool:
        return self.laberinto is not None

    def obtener_laberinto(self):
        if self.laberinto is None:
            if self.constructor is None:
                raise RuntimeError('El laberinto todavía no está preparado')
            self.laberinto = self.constructor()
        return self.laberinto

    def CreateIterator(self):
        return self.obtener_laberinto().CreateIterator()

    def habitacion(self, numero):
        return self.obtener_laberinto().habitacion(numero)

    def descripcion(self) -> str:
        return self.obtener_laberinto().descripcion()

    def __getattr__(self, nombre):
        return getattr(self.obtener_laberinto(), nombre)
