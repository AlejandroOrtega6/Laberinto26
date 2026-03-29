from .hoja import Hoja


class Pared(Hoja):
    def entrar(self, juego):
        print("Te has encontrado con una pared.")

    def descripcion(self):
        return "Pared"
