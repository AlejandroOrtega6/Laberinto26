from abc import ABC, abstractmethod


class Direccion(ABC):
    @abstractmethod
    def nombre(self):
        pass

    @abstractmethod
    def opuesta(self):
        pass

    def __str__(self):
        return self.nombre()


class Norte(Direccion):
    def nombre(self):
        return "norte"

    def opuesta(self):
        return SUR


class Sur(Direccion):
    def nombre(self):
        return "sur"

    def opuesta(self):
        return NORTE


class Este(Direccion):
    def nombre(self):
        return "este"

    def opuesta(self):
        return OESTE


class Oeste(Direccion):
    def nombre(self):
        return "oeste"

    def opuesta(self):
        return ESTE


NORTE = Norte()
SUR = Sur()
ESTE = Este()
OESTE = Oeste()


TODAS_DIRECCIONES = [NORTE, SUR, ESTE, OESTE]


def desde_texto(texto):
    texto = texto.strip().lower()
    equivalencias = {
        "n": NORTE,
        "norte": NORTE,
        "s": SUR,
        "sur": SUR,
        "e": ESTE,
        "este": ESTE,
        "o": OESTE,
        "oeste": OESTE,
    }
    return equivalencias.get(texto)
