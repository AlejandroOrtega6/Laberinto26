from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from .direcciones import ESTE, NORTE, NORESTE, NOROESTE, OESTE, ORIENTACIONES_CUADRADAS, ORIENTACIONES_ROMBO, SUR, SURESTE, SUROESTE, Orientacion

class Forma(ABC):

    def __init__(self, num: int):
        self.num = num

    @abstractmethod
    def orientaciones(self) -> List[Orientacion]:
        pass

    def __str__(self) -> str:
        return f'{self.__class__.__name__}({self.num})'

class Cuadrado(Forma):

    def orientaciones(self) -> List[Orientacion]:
        return ORIENTACIONES_CUADRADAS

    def norte(self) -> Orientacion:
        return NORTE

    def sur(self) -> Orientacion:
        return SUR

    def este(self) -> Orientacion:
        return ESTE

    def oeste(self) -> Orientacion:
        return OESTE

class Rombo(Forma):

    def orientaciones(self) -> List[Orientacion]:
        return ORIENTACIONES_ROMBO

    def ne(self) -> Orientacion:
        return NORESTE

    def no(self) -> Orientacion:
        return NOROESTE

    def se(self) -> Orientacion:
        return SURESTE

    def so(self) -> Orientacion:
        return SUROESTE
