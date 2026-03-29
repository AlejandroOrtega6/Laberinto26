from abc import ABC, abstractmethod
from .elemento_mapa import ElementoMapa


class Iterator(ABC):
    @abstractmethod
    def First(self):
        pass

    @abstractmethod
    def Next(self):
        pass

    @abstractmethod
    def IsDone(self):
        pass

    @abstractmethod
    def CurrentItem(self):
        pass


class ConcreteIterator(Iterator):
    def __init__(self, raiz):
        self._elementos = []
        self._indice = 0
        self._recoger(raiz, set())

    def _recoger(self, elemento, visitados):
        if id(elemento) in visitados:
            return
        visitados.add(id(elemento))
        self._elementos.append(elemento)

        if isinstance(elemento, ElementoMapa):
            for hijo in elemento.GetChildren():
                self._recoger(hijo, visitados)

    def First(self):
        self._indice = 0

    def Next(self):
        self._indice += 1

    def IsDone(self):
        return self._indice >= len(self._elementos)

    def CurrentItem(self):
        if self.IsDone():
            return None
        return self._elementos[self._indice]
