from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional

class Orientacion(ABC):

    @abstractmethod
    def nombre(self) -> str:
        pass

    @abstractmethod
    def opuesta(self) -> 'Orientacion':
        pass

    def __str__(self) -> str:
        return self.nombre()

class Norte(Orientacion):

    def nombre(self) -> str:
        return 'norte'

    def opuesta(self) -> Orientacion:
        return SUR

class Sur(Orientacion):

    def nombre(self) -> str:
        return 'sur'

    def opuesta(self) -> Orientacion:
        return NORTE

class Este(Orientacion):

    def nombre(self) -> str:
        return 'este'

    def opuesta(self) -> Orientacion:
        return OESTE

class Oeste(Orientacion):

    def nombre(self) -> str:
        return 'oeste'

    def opuesta(self) -> Orientacion:
        return ESTE

class Noreste(Orientacion):

    def nombre(self) -> str:
        return 'noreste'

    def opuesta(self) -> Orientacion:
        return SUROESTE

class Noroeste(Orientacion):

    def nombre(self) -> str:
        return 'noroeste'

    def opuesta(self) -> Orientacion:
        return SURESTE

class Sureste(Orientacion):

    def nombre(self) -> str:
        return 'sureste'

    def opuesta(self) -> Orientacion:
        return NOROESTE

class Suroeste(Orientacion):

    def nombre(self) -> str:
        return 'suroeste'

    def opuesta(self) -> Orientacion:
        return NORESTE
NORTE = Norte()
SUR = Sur()
ESTE = Este()
OESTE = Oeste()
NORESTE = Noreste()
NOROESTE = Noroeste()
SURESTE = Sureste()
SUROESTE = Suroeste()
ORIENTACIONES_CUADRADAS = [NORTE, SUR, ESTE, OESTE]
ORIENTACIONES_ROMBO = [NORESTE, NOROESTE, SURESTE, SUROESTE]
TODAS_ORIENTACIONES = ORIENTACIONES_CUADRADAS + ORIENTACIONES_ROMBO
TODAS_DIRECCIONES = ORIENTACIONES_CUADRADAS

def orientacion_desde_texto(texto: str) -> Optional[Orientacion]:
    texto = texto.strip().lower()
    equivalencias = {'n': NORTE, 'norte': NORTE, 's': SUR, 'sur': SUR, 'e': ESTE, 'este': ESTE, 'o': OESTE, 'oeste': OESTE, 'ne': NORESTE, 'noreste': NORESTE, 'no': NOROESTE, 'noroeste': NOROESTE, 'se': SURESTE, 'sureste': SURESTE, 'so': SUROESTE, 'suroeste': SUROESTE}
    return equivalencias.get(texto)

def desde_texto(texto: str) -> Optional[Orientacion]:
    return orientacion_desde_texto(texto)
