from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Callable, List, Optional, Set

class ElementoMapa(ABC):

    def __init__(self):
        self._padre: Optional[ElementoMapa] = None

    def Add(self, componente: 'ElementoMapa'):
        raise TypeError(f'{self.__class__.__name__} no admite hijos')

    def Remove(self, componente: 'ElementoMapa'):
        raise TypeError(f'{self.__class__.__name__} no admite hijos')

    def GetChild(self, indice: int) -> Optional['ElementoMapa']:
        return None

    def GetChildren(self) -> List['ElementoMapa']:
        return []

    def SetParent(self, padre: Optional['ElementoMapa']):
        self._padre = padre

    def GetParent(self) -> Optional['ElementoMapa']:
        return self._padre

    @abstractmethod
    def entrar(self, juego):
        pass

    @abstractmethod
    def descripcion(self) -> str:
        pass

    def recorrer(self, unBloque: Callable[['ElementoMapa'], None], visitados: Optional[Set[int]]=None):
        if visitados is None:
            visitados = set()
        if id(self) in visitados:
            return
        visitados.add(id(self))
        unBloque(self)
        for hijo in self.GetChildren():
            hijo.recorrer(unBloque, visitados)

    def aceptar(self, visitante):
        visitante.visitar_elemento(self)

    def abrir(self) -> bool:
        return False

    def es_puerta(self) -> bool:
        return False

    def es_bomba(self) -> bool:
        return False

    def destino_desde(self, origen):
        return None
