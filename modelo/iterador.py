from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional, Set
from .elemento_mapa import ElementoMapa

class Iterator(ABC):

    @abstractmethod
    def First(self):
        pass

    @abstractmethod
    def Next(self):
        pass

    @abstractmethod
    def IsDone(self) -> bool:
        pass

    @abstractmethod
    def CurrentItem(self) -> Optional[ElementoMapa]:
        pass

class ConcreteIterator(Iterator):

    def __init__(self, raiz: ElementoMapa):
        self._elementos: List[ElementoMapa] = []
        self._indice = 0
        self._recoger(raiz, set())

    def _recoger(self, elemento: ElementoMapa, visitados: Set[int]):
        if id(elemento) in visitados:
            return
        visitados.add(id(elemento))
        self._elementos.append(elemento)
        for hijo in elemento.GetChildren():
            self._recoger(hijo, visitados)

    def First(self):
        self._indice = 0

    def Next(self):
        self._indice += 1

    def IsDone(self) -> bool:
        return self._indice >= len(self._elementos)

    def CurrentItem(self) -> Optional[ElementoMapa]:
        if self.IsDone():
            return None
        return self._elementos[self._indice]
