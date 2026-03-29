from .decorador import Decorator


class Bomba(Decorator):
    def __init__(self, em, activa=True):
        super().__init__(em)
        self.activa = activa

    def es_bomba(self):
        return True

    def entrar(self, juego):
        if self.activa:
            print("¡BOOM! Has activado una bomba.")
            self.activa = False
            juego.recibir_danio(1, "una bomba")
            if juego.fin:
                return

        self.em.entrar(juego)

    def descripcion(self):
        estado = "activa" if self.activa else "desactivada"
        return f"Bomba sobre {self.em.descripcion()} ({estado})"
