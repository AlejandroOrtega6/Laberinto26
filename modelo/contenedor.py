from .elemento_mapa import ElementoMapa


class Contenedor(ElementoMapa):
    def __init__(self):
        super().__init__()
        self._children = []
        self._lados = {}

    def Add(self, componente):
        if componente not in self._children:
            self._children.append(componente)
            componente.SetParent(self)

    def Remove(self, componente):
        if componente in self._children:
            self._children.remove(componente)
            componente.SetParent(None)

    def GetChild(self, indice):
        return self._children[indice]

    def GetChildren(self):
        return list(self._children)

    def poner_lado(self, direccion, elemento):
        self._lados[direccion] = elemento
        if elemento not in self._children:
            self._children.append(elemento)

    def obtener_lado(self, direccion):
        return self._lados.get(direccion)

    def entrar(self, juego):
        juego.habitacion_actual = self
