from __future__ import annotations
import random
from .armario import Armario
from .bicho import Bicho
from .bomba import Bomba
from .builder import ConcreteBuilder, Director
from .direcciones import ESTE, NORTE, NORESTE, NOROESTE, OESTE, SUR, SURESTE, SUROESTE, TODAS_ORIENTACIONES, Orientacion
from .estado_puerta import Abierta
from .factorias import ConcreteFactory, ConcreteFactoryBombas
from .fases import Final, Inicial, Jugando
from .formas import Cuadrado, Forma, Rombo
from .habitacion import Habitacion
from .interprete import InterpreteComandos
from .laberinto import Laberinto
from .modos import Agresivo, Modo, Perezoso
from .pared import Pared
from .personaje import Personaje
from .puerta import Puerta
from .tunel import Tunel

class Juego:

    def __init__(self, nombre_personaje: str='Alejandro'):
        self.abstract_factory = ConcreteFactory.Instance()
        self.laberinto = None
        self.personaje = Personaje(nombre_personaje, vidas=5)
        self.fase = Inicial()
        self.interprete = InterpreteComandos()
        self.turno = 1
        self.ganado = False

    def fabricarLaberinto(self) -> Laberinto:
        return self.abstract_factory.fabricar_laberinto()

    def fabricarHabitacion(self, numero: int, forma: Forma | None=None) -> Habitacion:
        return self.abstract_factory.fabricar_habitacion(numero, forma)

    def fabricarPared(self):
        return self.abstract_factory.fabricar_pared()

    def fabricarParedBase(self) -> Pared:
        return Pared()

    def fabricarPuerta(self, lado1: Habitacion, lado2: Habitacion, abierta: bool=False):
        return self.abstract_factory.fabricar_puerta(lado1, lado2, abierta)

    def fabricarPuertaBase(self, lado1: Habitacion, lado2: Habitacion, abierta: bool=False) -> Puerta:
        return Puerta(lado1, lado2, abierta)

    def fabricarTunel(self, destino=None) -> Tunel:
        return self.abstract_factory.fabricar_tunel(self.laberinto, destino)

    def fabricarBomba(self, em) -> Bomba:
        return self.abstract_factory.fabricar_bomba(em)

    def fabricarBicho(self, nombre: str, vidas: int, poder: int, modo: Modo, posicion: Habitacion) -> Bicho:
        return self.abstract_factory.fabricar_bicho(nombre, vidas, poder, modo, posicion)

    def fabricarPersonaje(self, nombre: str) -> Personaje:
        return Personaje(nombre)

    def fabricarArmario(self, nombre: str='Armario') -> Armario:
        armario = self.abstract_factory.fabricar_armario(nombre)
        armario.poner_lado(NORTE, self.fabricarParedBase())
        armario.poner_lado(SUR, self.fabricarParedBase())
        armario.poner_lado(ESTE, self.fabricarParedBase())
        armario.poner_lado(OESTE, self.fabricarParedBase())
        return armario

    def fabricar_laberinto(self):
        return self.fabricarLaberinto()

    def fabricar_habitacion(self, numero, forma=None):
        return self.fabricarHabitacion(numero, forma)

    def fabricar_pared(self):
        return self.fabricarPared()

    def fabricar_puerta(self, lado1, lado2, abierta=False):
        return self.fabricarPuerta(lado1, lado2, abierta)

    def fabricar_bomba(self, em):
        return self.fabricarBomba(em)

    def fabricar_bicho(self, nombre, vidas, poder, modo, posicion):
        return self.fabricarBicho(nombre, vidas, poder, modo, posicion)

    def fabricar_pared_bomba(self):
        return self.fabricarBomba(self.fabricarParedBase())

    def fabricar_puerta_bomba(self, lado1, lado2, abierta=False):
        return self.fabricarBomba(self.fabricarPuertaBase(lado1, lado2, abierta))

    def ponerParedes(self, habitacion: Habitacion):
        for orientacion in habitacion.forma.orientaciones():
            habitacion.poner_lado(orientacion, self.fabricarPared())

    def conectar(self, h1: Habitacion, orientacion: Orientacion, h2: Habitacion, abierta: bool=False):
        puerta = self.fabricarPuerta(h1, h2, abierta)
        h1.poner_lado(orientacion, puerta)
        h2.poner_lado(orientacion.opuesta(), puerta)
        return puerta

    def conectarConBomba(self, h1: Habitacion, orientacion: Orientacion, h2: Habitacion, abierta: bool=False):
        puerta = self.fabricarBomba(self.fabricarPuertaBase(h1, h2, abierta))
        h1.poner_lado(orientacion, puerta)
        h2.poner_lado(orientacion.opuesta(), puerta)
        return puerta

    def fabricarLab2Hab(self) -> Laberinto:
        laberinto = self.fabricarLaberinto()
        h1 = self.fabricarHabitacion(1, Cuadrado(1))
        h2 = self.fabricarHabitacion(2, Cuadrado(2))
        self.ponerParedes(h1)
        self.ponerParedes(h2)
        self.conectar(h1, ESTE, h2, abierta=False)
        h1.Add(self.fabricarArmario('Armario de la habitación 1'))
        laberinto.Add(h1)
        laberinto.Add(h2)
        laberinto.fijar_inicio(1)
        laberinto.fijar_salida(2)
        laberinto.agregar_bicho(self.fabricarBicho('Bicho verde', 1, 1, Perezoso(), h2))
        return laberinto

    def fabricarLabConBuilder(self) -> Laberinto:
        builder = ConcreteBuilder(self)
        director = Director(builder)
        director.Construct()
        return builder.GetProduct()

    def nombresMapas(self):
        return ['Aleatorio']

    def fabricarLaberintoPorNombre(self, nombre: str='Aleatorio') -> Laberinto:
        return self.fabricarMapaAleatorio()

    def fabricarMapaClasico(self) -> Laberinto:
        return self.fabricarMapaAleatorio()

    def fabricarMapaAleatorio(self) -> Laberinto:
        laberinto = self.fabricarLaberinto()
        direcciones = [(NORTE, (0, -1)), (SUR, (0, 1)), (ESTE, (1, 0)), (OESTE, (-1, 0))]
        total_habitaciones = random.randint(7, 12)
        coords = [(0, 0)]
        ocupadas = {(0, 0)}
        padre = {}
        intentos = 0
        while len(coords) < total_habitaciones and intentos < 500:
            intentos += 1
            base = random.choice(coords)
            random.shuffle(direcciones)
            opciones = []
            for _orientacion, (dx, dy) in direcciones:
                nueva = (base[0] + dx, base[1] + dy)
                if nueva not in ocupadas and -4 <= nueva[0] <= 4 and (-4 <= nueva[1] <= 4):
                    opciones.append(nueva)
            if not opciones:
                continue
            nueva = random.choice(opciones)
            ocupadas.add(nueva)
            coords.append(nueva)
            padre[nueva] = base

        def distancia_al_inicio(coord):
            distancia = 0
            actual = coord
            while actual in padre:
                distancia += 1
                actual = padre[actual]
            return distancia
        salida_coord = max(coords, key=distancia_al_inicio)
        ruta_segura = []
        actual = salida_coord
        while True:
            ruta_segura.append(actual)
            if actual == (0, 0):
                break
            actual = padre[actual]
        ruta_segura.reverse()
        resto = [c for c in coords if c not in ruta_segura]
        random.shuffle(resto)
        ordenadas = ruta_segura + resto
        coord_a_habitacion = {}
        for numero, coord in enumerate(ordenadas, start=1):
            habitacion = self.fabricarHabitacion(numero, Cuadrado(numero))
            self.ponerParedes(habitacion)
            laberinto.Add(habitacion)
            coord_a_habitacion[coord] = habitacion
        ruta_edges = set()
        for i in range(len(ruta_segura) - 1):
            ruta_edges.add(frozenset((ruta_segura[i], ruta_segura[i + 1])))

        def orientacion_entre(origen, destino):
            dx = destino[0] - origen[0]
            dy = destino[1] - origen[1]
            if dx == 1 and dy == 0:
                return ESTE
            if dx == -1 and dy == 0:
                return OESTE
            if dx == 0 and dy == 1:
                return SUR
            if dx == 0 and dy == -1:
                return NORTE
            return None
        conexiones = set()
        aristas_arbol = []
        for hijo_coord, padre_coord in padre.items():
            clave = frozenset((padre_coord, hijo_coord))
            aristas_arbol.append((padre_coord, hijo_coord, clave))
        candidatas_bomba = [arista for arista in aristas_arbol if arista[2] not in ruta_edges]
        if len(candidatas_bomba) < 2:
            candidatas_bomba += [arista for arista in aristas_arbol if arista[2] in ruta_edges and arista[0] != (0, 0)]
        random.shuffle(candidatas_bomba)
        cantidad_bombas = min(len(candidatas_bomba), random.randint(2, 3))
        aristas_bomba = {arista[2] for arista in candidatas_bomba[:cantidad_bombas]}
        for hijo_coord, padre_coord in padre.items():
            h_padre = coord_a_habitacion[padre_coord]
            h_hijo = coord_a_habitacion[hijo_coord]
            orientacion = orientacion_entre(padre_coord, hijo_coord)
            if orientacion is None:
                continue
            clave = frozenset((padre_coord, hijo_coord))
            conexiones.add(clave)
            if clave in aristas_bomba:
                self.conectarConBomba(h_padre, orientacion, h_hijo, abierta=True)
            elif clave in ruta_edges:
                self.conectar(h_padre, orientacion, h_hijo, abierta=True)
            else:
                self.conectar(h_padre, orientacion, h_hijo, abierta=random.random() < 0.65)
        for coord in list(ocupadas):
            for orientacion, (dx, dy) in direcciones:
                vecino = (coord[0] + dx, coord[1] + dy)
                if vecino not in ocupadas:
                    continue
                clave = frozenset((coord, vecino))
                if clave in conexiones:
                    continue
                if random.random() > 0.2:
                    continue
                conexiones.add(clave)
                h1 = coord_a_habitacion[coord]
                h2 = coord_a_habitacion[vecino]
                if clave in ruta_edges:
                    self.conectar(h1, orientacion, h2, abierta=True)
                elif random.random() < 0.25:
                    self.conectarConBomba(h1, orientacion, h2, abierta=True)
                else:
                    self.conectar(h1, orientacion, h2, abierta=random.random() < 0.65)
        def contar_bombas_colocadas():
            total = 0
            vistas = set()
            for habitacion in coord_a_habitacion.values():
                for orientacion, _desplazamiento in direcciones:
                    lado = habitacion.obtener_lado(orientacion)
                    if isinstance(lado, Bomba) and id(lado) not in vistas:
                        vistas.add(id(lado))
                        total += 1
            return total
        coord_a_habitacion[0, 0].Add(self.fabricarArmario('Armario del inicio'))
        habitaciones_ruta = [coord_a_habitacion[c] for c in ruta_segura]
        ruta_intermedia = habitaciones_ruta[1:-1]
        laterales = [h for h in coord_a_habitacion.values() if h not in habitaciones_ruta and h != coord_a_habitacion[salida_coord]]
        candidatas = []
        if ruta_intermedia:
            candidatas.append(random.choice(ruta_intermedia))
        random.shuffle(laterales)
        candidatas.extend(laterales)
        if len(candidatas) < 2:
            candidatas.extend([h for h in coord_a_habitacion.values() if h != coord_a_habitacion[0, 0] and h != coord_a_habitacion[salida_coord] and (h not in candidatas)])
        nombres = ['Bicho rojo', 'Bicho azul', 'Bicho verde', 'Bicho morado', 'Bicho naranja']
        cantidad_bichos = min(len(candidatas), random.randint(2, 4))
        for i, habitacion in enumerate(candidatas[:cantidad_bichos]):
            if habitacion in ruta_intermedia:
                modo = Agresivo()
                vidas = 2
            else:
                modo = Agresivo() if random.random() < 0.45 else Perezoso()
                vidas = 2 if isinstance(modo, Agresivo) else 1
            laberinto.agregar_bicho(self.fabricarBicho(nombres[i % len(nombres)], vidas, 1, modo, habitacion))
        laberinto.fijar_inicio(coord_a_habitacion[0, 0].num)
        laberinto.fijar_salida(coord_a_habitacion[salida_coord].num)
        laberinto.posiciones_mapa = {habitacion.num: coord for coord, habitacion in coord_a_habitacion.items()}
        laberinto.ruta_segura = [coord_a_habitacion[c].num for c in ruta_segura]
        laberinto.nombre_mapa = 'Mapa aleatorio'
        return laberinto

    def fabricarLab4Hab(self) -> Laberinto:
        laberinto = self.fabricarLaberinto()
        habitaciones = [self.fabricarHabitacion(i, Cuadrado(i)) for i in range(1, 5)]
        for habitacion in habitaciones:
            self.ponerParedes(habitacion)
            laberinto.Add(habitacion)
        h1, h2, h3, h4 = habitaciones
        self.conectar(h1, ESTE, h2, abierta=True)
        self.conectar(h1, SUR, h3, abierta=True)
        self.conectar(h2, SUR, h4, abierta=False)
        self.conectar(h3, ESTE, h4, abierta=True)
        h3.poner_lado(OESTE, Tunel(laberinto, h2))
        h1.Add(self.fabricarArmario('Armario pequeño'))
        laberinto.fijar_inicio(1)
        laberinto.fijar_salida(4)
        laberinto.agregar_bicho(self.fabricarBicho('Bicho rojo', 2, 1, Agresivo(), h3))
        laberinto.agregar_bicho(self.fabricarBicho('Bicho azul', 1, 1, Perezoso(), h2))
        return laberinto

    def TemplateMethod(self):
        while True:
            fase_actual = self.fase
            fase_actual.ejecutar(self)
            if isinstance(fase_actual, Final):
                break

    def preparar(self):
        self.laberinto = self.fabricarMapaAleatorio()
        self.personaje.posicion = self.laberinto.inicio
        print('Laberinto preparado.')
        self.mostrar_ayuda()

    def finalizar(self):
        self.fase = Final()

    def terminar_por_muerte(self):
        self.ganado = False
        self.fase = Final()

    def mostrar_ayuda(self):
        print('\nComandos disponibles:')
        print('  norte/sur/este/oeste o n/s/e/o')
        print('  noreste/noroeste/sureste/suroeste o ne/no/se/so')
        print('  abrir <direccion>')
        print('  atacar')
        print('  mapa')
        print('  ayuda')
        print('  salir')

    def mostrar_estado(self):
        h = self.personaje.posicion
        print('-' * 60)
        print(f'Fase: {self.fase.nombre()} | Turno: {self.turno}')
        print(self.personaje.descripcion())
        print(f'Objetivo: llegar a {self.laberinto.salida.descripcion()}')
        print('Lados de la habitación:')
        for orientacion in h.forma.orientaciones():
            lado = h.obtener_lado(orientacion)
            if lado is not None:
                print(f'  {orientacion.nombre():<9} -> {lado.descripcion()}')
        presentes = [b for b in self.laberinto.bichos if b.esta_vivo() and b.posicion == h]
        if presentes:
            print('Bichos en esta habitación:')
            for bicho in presentes:
                print(f'  - {bicho.descripcion()}')
        else:
            print('No hay bichos en esta habitación.')
        print()

    def mover(self, orientacion: Orientacion):
        lado = self.personaje.posicion.obtener_lado(orientacion)
        if lado is None:
            print('No hay nada en esa orientación.')
            return
        lado.entrar(self)

    def abrir(self, orientacion: Orientacion):
        lado = self.personaje.posicion.obtener_lado(orientacion)
        if lado is None:
            print('No hay nada que abrir en esa orientación.')
            return
        if lado.abrir():
            print(f'Has abierto el lado {orientacion.nombre()}.')
        else:
            print('Ese lado no se puede abrir.')

    def atacar_bicho(self):
        presentes = [b for b in self.laberinto.bichos if b.esta_vivo() and b.posicion == self.personaje.posicion]
        if not presentes:
            print('No hay ningún bicho al que atacar aquí.')
            return
        objetivo = presentes[0]
        objetivo.recibir_danio(self.personaje.poder)
        print(f'Atacas a {objetivo.nombre}. Le queda(n) {objetivo.vidas} vida(s).')
        if objetivo.esta_muerto():
            print(f'{objetivo.nombre} ha muerto.')

    def vecinos_accesibles(self, habitacion: Habitacion):
        vecinos = []
        for orientacion in TODAS_ORIENTACIONES:
            lado = habitacion.obtener_lado(orientacion)
            if lado is None:
                continue
            destino = lado.destino_desde(habitacion)
            if destino is None or not lado.es_puerta():
                continue
            elemento = lado.em if isinstance(lado, Bomba) else lado
            if isinstance(elemento, Puerta) and isinstance(elemento.estado, Abierta):
                vecinos.append(destino)
        return vecinos

    def turno_bichos(self):
        vivos = [b for b in self.laberinto.bichos if b.esta_vivo()]
        if not vivos:
            return
        print('\nTurno de los bichos:')
        for bicho in vivos:
            bicho.actua(self)
            if self.personaje.esta_muerto():
                break
        self.laberinto.bichos = [b for b in self.laberinto.bichos if b.esta_vivo()]

    def comprobar_fin(self):
        if self.personaje.esta_muerto():
            self.ganado = False
            self.fase = Final()
            return
        if self.personaje.posicion == self.laberinto.salida:
            self.ganado = True
            self.fase = Final()

    def mostrar_final(self):
        print('=' * 60)
        if self.ganado:
            print('Has ganado. Has llegado a la salida del laberinto.')
        elif self.personaje.esta_muerto():
            print('Has perdido. El personaje ha muerto.')
        else:
            print('Partida terminada.')

    def mostrar_mapa(self):
        print('\nElementos del mapa:')
        iterator = self.laberinto.CreateIterator()
        iterator.First()
        while not iterator.IsDone():
            actual = iterator.CurrentItem()
            print(f'  - {actual.descripcion()}')
            iterator.Next()
        print()

    def OperacionPreparar(self):
        self.preparar()

    def OperacionIntroduccion(self):
        self.mostrar_ayuda()

    def OperacionMostrar(self):
        self.mostrar_estado()

    def OperacionLeer(self):
        return input('Orden: ').strip().lower()

    def OperacionProcesar(self, orden):
        self.interprete.interpretar(orden).ejecutar(self)

    def OperacionTurnoEnemigos(self):
        self.turno_bichos()

    def OperacionFin(self):
        return isinstance(self.fase, Final)

    def OperacionFinal(self):
        self.mostrar_final()

class JuegoBombas(Juego):

    def __init__(self, nombre_personaje: str='Alejandro'):
        super().__init__(nombre_personaje)
        self.abstract_factory = ConcreteFactoryBombas.Instance()
