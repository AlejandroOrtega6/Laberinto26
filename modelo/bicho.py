class Bicho:
    def __init__(self, nombre, vidas, poder, modo, posicion):
        self.nombre = nombre
        self.vidas = vidas
        self.poder = poder
        self.modo = modo
        self.posicion = posicion

    def actua(self, juego):
        if self.esta_vivo():
            self.modo.actua(self, juego)

    def esta_vivo(self):
        return self.vidas > 0

    def recibir_danio(self, cantidad):
        self.vidas -= cantidad
        if self.vidas < 0:
            self.vidas = 0

    def descripcion(self):
        return f"{self.nombre} [{self.modo.nombre()} | vidas={self.vidas} | poder={self.poder}]"
