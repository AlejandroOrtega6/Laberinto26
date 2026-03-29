from .hoja import Hoja


class Puerta(Hoja):
    def __init__(self, lado1, lado2, abierta=False):
        super().__init__()
        self.lado1 = lado1
        self.lado2 = lado2
        self.abierta = abierta

    def es_puerta(self):
        return True

    def abrir(self):
        self.abierta = True
        return True

    def destino_desde(self, origen):
        if not self.abierta:
            return None
        if origen == self.lado1:
            return self.lado2
        if origen == self.lado2:
            return self.lado1
        return None

    def entrar(self, juego):
        destino = self.destino_desde(juego.habitacion_actual)
        if destino is None:
            print("La puerta está cerrada.")
            return

        destino.entrar(juego)
        print(f"Has entrado en la habitación {destino.numero}.")

    def descripcion(self):
        estado = "abierta" if self.abierta else "cerrada"
        return f"Puerta ({estado})"
