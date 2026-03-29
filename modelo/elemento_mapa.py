from abc import ABC, abstractmethod


class ElementoMapa(ABC):
    def __init__(self):
        self._padre = None

    def Add(self, componente):
        raise Exception("Este elemento no admite hijos.")

    def Remove(self, componente):
        raise Exception("Este elemento no admite hijos.")

    def GetChild(self, indice):
        return None

    def GetChildren(self):
        return []

    def SetParent(self, padre):
        self._padre = padre

    def GetParent(self):
        return self._padre

    @abstractmethod
    def entrar(self, juego):
        pass

    @abstractmethod
    def descripcion(self):
        pass

    def recorrer(self, accion, visitados=None):
        if visitados is None:
            visitados = set()

        if id(self) in visitados:
            return

        visitados.add(id(self))
        accion(self)

        for hijo in self.GetChildren():
            hijo.recorrer(accion, visitados)

    def abrir(self):
        return False

    def es_puerta(self):
        return False

    def es_bomba(self):
        return False

    def destino_desde(self, origen):
        return None
