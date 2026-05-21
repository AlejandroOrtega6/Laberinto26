from __future__ import annotations
from .decorador import Decorator

class Bomba(Decorator):

    def __init__(self, em, activa: bool=True):
        super().__init__(em)
        self.activa = activa

    def es_bomba(self) -> bool:
        return True

    def entrar(self, juego):
        if self.activa:
            print('¡BOOM! Has activado una bomba.')
            self.activa = False
            if hasattr(juego, 'personaje'):
                juego.personaje.recibir_danio(1)
                print(f'Te queda(n) {juego.personaje.vidas} vida(s).')
                if juego.personaje.esta_muerto():
                    juego.terminar_por_muerte()
                    return
            else:
                juego.recibir_danio(1, 'una bomba')
                if getattr(juego, 'fin', False):
                    return
        self.em.entrar(juego)

    def descripcion(self) -> str:
        estado = 'activa' if self.activa else 'desactivada'
        return f'Bomba {estado} sobre {self.em.descripcion()}'

    def aceptar(self, visitante):
        visitante.visitar_bomba(self)
