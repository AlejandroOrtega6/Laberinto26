import random
from abc import ABC, abstractmethod

from .builder import ConcreteBuilder, Director
from .direcciones import TODAS_DIRECCIONES, desde_texto
from .factorias import ConcreteFactory, ConcreteFactoryBombas
from .bomba import Bomba
from .habitacion import Habitacion
from .puerta import Puerta
from .pared import Pared


class Creator(ABC):
    @abstractmethod
    def fabricar_habitacion(self, numero):
        pass

    @abstractmethod
    def fabricar_pared(self):
        pass

    @abstractmethod
    def fabricar_puerta(self, lado1, lado2, abierta=False):
        pass

    @abstractmethod
    def fabricar_pared_bomba(self):
        pass

    @abstractmethod
    def fabricar_puerta_bomba(self, lado1, lado2, abierta=False):
        pass

    @abstractmethod
    def fabricar_bicho(self, nombre, vidas, poder, modo, posicion):
        pass


class AbstractClass(ABC):
    def TemplateMethod(self):
        self.OperacionPreparar()
        self.OperacionIntroduccion()

        while not self.OperacionFin():
            self.OperacionMostrar()
            orden = self.OperacionLeer()
            self.OperacionProcesar(orden)
            if not self.OperacionFin():
                self.OperacionTurnoEnemigos()

        self.OperacionFinal()

    @abstractmethod
    def OperacionPreparar(self):
        pass

    @abstractmethod
    def OperacionIntroduccion(self):
        pass

    @abstractmethod
    def OperacionMostrar(self):
        pass

    @abstractmethod
    def OperacionLeer(self):
        pass

    @abstractmethod
    def OperacionProcesar(self, orden):
        pass

    @abstractmethod
    def OperacionTurnoEnemigos(self):
        pass

    @abstractmethod
    def OperacionFin(self):
        pass

    @abstractmethod
    def OperacionFinal(self):
        pass


class Juego(AbstractClass, Creator):
    def __init__(self):
        self.abstract_factory = ConcreteFactory.Instance()
        self.laberinto = None
        self.habitacion_actual = None
        self.vidas = 3
        self.fin = False
        self.ganado = False
        self.turno = 0
        random.seed(5)

    def fabricar_habitacion(self, numero):
        return self.abstract_factory.fabricar_habitacion(numero)

    def fabricar_pared(self):
        return self.abstract_factory.fabricar_pared()

    def fabricar_puerta(self, lado1, lado2, abierta=False):
        return self.abstract_factory.fabricar_puerta(lado1, lado2, abierta)

    def fabricar_pared_bomba(self):
        return self.abstract_factory.fabricar_bomba(self.fabricar_pared())

    def fabricar_puerta_bomba(self, lado1, lado2, abierta=False):
        return self.abstract_factory.fabricar_bomba(self.fabricar_puerta(lado1, lado2, abierta))

    def fabricar_bicho(self, nombre, vidas, poder, modo, posicion):
        return self.abstract_factory.fabricar_bicho(nombre, vidas, poder, modo, posicion)

    def OperacionPreparar(self):
        builder = ConcreteBuilder(self)
        director = Director(builder)
        director.Construct()
        self.laberinto = builder.GetProduct()
        self.habitacion_actual = self.laberinto.inicio

    def OperacionIntroduccion(self):
        print("OBJETIVO")
        print("Llegar a la habitación 6 con vida.")
        print("Comandos disponibles:")
        print("  norte/sur/este/oeste  (o n/s/e/o)")
        print("  abrir <direccion>")
        print("  atacar")
        print("  mapa")
        print("  salir")
        print()

    def OperacionMostrar(self):
        print("-" * 60)
        print(f"Turno: {self.turno} | Vidas: {self.vidas}")
        print(f"Habitación actual: {self.habitacion_actual.numero}")
        print(f"Habitación de salida: {self.laberinto.salida.numero}")
        print(f"Bombas activas: {self.contar_bombas_activas()}")
        print(f"Bichos vivos: {self.contar_bichos_vivos()}")
        print()
        print("Lados de la habitación:")
        for direccion in TODAS_DIRECCIONES:
            lado = self.habitacion_actual.obtener_lado(direccion)
            print(f"  {direccion.nombre():<5} -> {lado.descripcion()}")

        presentes = [b for b in self.laberinto.bichos if b.esta_vivo() and b.posicion == self.habitacion_actual]
        if presentes:
            print("\nBichos en esta habitación:")
            for bicho in presentes:
                print(f"  - {bicho.descripcion()}")
        else:
            print("\nNo hay bichos en esta habitación.")
        print()

    def OperacionLeer(self):
        return input("Orden: ").strip().lower()

    def OperacionProcesar(self, orden):
        if orden == "salir":
            self.fin = True
            return

        if orden == "mapa":
            self.mostrar_mapa()
            return

        if orden == "atacar":
            self.atacar_bicho()
            self.comprobar_salida()
            self.turno += 1
            return

        if orden.startswith("abrir "):
            texto_direccion = orden.split(" ", 1)[1]
            direccion = desde_texto(texto_direccion)
            if direccion is None:
                print("Dirección no válida.")
                return

            lado = self.habitacion_actual.obtener_lado(direccion)
            if lado.abrir():
                print(f"Has abierto el lado {direccion.nombre()}.")
            else:
                print("Ese lado no se puede abrir.")
            self.turno += 1
            return

        direccion = desde_texto(orden)
        if direccion is None:
            print("Orden no reconocida.")
            return

        lado = self.habitacion_actual.obtener_lado(direccion)
        lado.entrar(self)
        self.comprobar_salida()
        self.turno += 1

    def OperacionTurnoEnemigos(self):
        if self.fin or self.ganado:
            return

        print("\nTurno de los bichos:")
        hubo_acciones = False
        for bicho in self.laberinto.bichos:
            if bicho.esta_vivo():
                hubo_acciones = True
                bicho.actua(self)
                if self.fin:
                    break

        if not hubo_acciones:
            print("No quedan bichos vivos.")

        self.eliminar_bichos_muertos()
        self.comprobar_salida()
        print()

    def OperacionFin(self):
        return self.fin or self.ganado

    def OperacionFinal(self):
        print("=" * 60)
        if self.ganado:
            print("Has ganado. Has encontrado la salida del laberinto.")
        elif self.vidas <= 0:
            print("Has perdido. Te has quedado sin vidas.")
        else:
            print("Partida terminada.")

    def recibir_danio(self, cantidad, origen):
        self.vidas -= cantidad
        print(f"Recibes {cantidad} punto(s) de daño por {origen}.")
        if self.vidas <= 0:
            self.vidas = 0
            self.fin = True

    def comprobar_salida(self):
        if self.habitacion_actual == self.laberinto.salida and self.vidas > 0:
            self.ganado = True

    def atacar_bicho(self):
        presentes = [b for b in self.laberinto.bichos if b.esta_vivo() and b.posicion == self.habitacion_actual]
        if not presentes:
            print("No hay ningún bicho al que atacar aquí.")
            return

        objetivo = presentes[0]
        objetivo.recibir_danio(1)
        print(f"Has atacado a {objetivo.nombre}. Le queda(n) {objetivo.vidas} vida(s).")
        if not objetivo.esta_vivo():
            print(f"{objetivo.nombre} ha muerto.")

    def eliminar_bichos_muertos(self):
        self.laberinto.bichos = [b for b in self.laberinto.bichos if b.esta_vivo()]

    def vecinos_accesibles(self, habitacion):
        vecinos = []
        for direccion in TODAS_DIRECCIONES:
            lado = habitacion.obtener_lado(direccion)
            if lado is None:
                continue
            destino = lado.destino_desde(habitacion)
            if destino is not None:
                vecinos.append(destino)
        return vecinos

    def contar_bichos_vivos(self):
        return len([b for b in self.laberinto.bichos if b.esta_vivo()])

    def contar_bombas_activas(self):
        contador = 0
        iterator = self.laberinto.CreateIterator()
        iterator.First()

        while not iterator.IsDone():
            actual = iterator.CurrentItem()
            if isinstance(actual, Bomba) and actual.activa:
                contador += 1
            iterator.Next()

        return contador

    def mostrar_mapa(self):
        print("\nRecorrido del laberinto con Iterator:")
        iterator = self.laberinto.CreateIterator()
        iterator.First()

        while not iterator.IsDone():
            actual = iterator.CurrentItem()
            if isinstance(actual, Habitacion):
                print(f"  - {actual.descripcion()}")
            elif isinstance(actual, Bomba):
                print(f"  - {actual.descripcion()}")
            elif isinstance(actual, Puerta):
                print(f"  - {actual.descripcion()}")
            elif isinstance(actual, Pared):
                print(f"  - {actual.descripcion()}")
            iterator.Next()
        print()


class JuegoBombas(Juego):
    def __init__(self):
        super().__init__()
        self.abstract_factory = ConcreteFactoryBombas.Instance()

    def fabricar_pared_bomba(self):
        pared = self.abstract_factory.fabricar_pared()
        return self.abstract_factory.fabricar_bomba(pared)

    def fabricar_puerta_bomba(self, lado1, lado2, abierta=False):
        puerta = self.abstract_factory.fabricar_puerta(lado1, lado2, abierta)
        return self.abstract_factory.fabricar_bomba(puerta)
