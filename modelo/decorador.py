from .hoja import Hoja


class Decorator(Hoja):
    def __init__(self, em):
        super().__init__()
        self.em = em

    def entrar(self, juego):
        self.em.entrar(juego)

    def descripcion(self):
        return self.em.descripcion()

    def abrir(self):
        return self.em.abrir()

    def es_puerta(self):
        return self.em.es_puerta()

    def destino_desde(self, origen):
        return self.em.destino_desde(origen)
