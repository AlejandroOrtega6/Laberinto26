from __future__ import annotations
import json
import random
from pathlib import Path
from .armario import Armario
from .bicho import Bicho
from .bomba import Bomba
from .builder import ConcreteBuilder, Director, DirectorJSON
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
from .proxy import ProxyLaberinto
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

    def fabricarLabConBuilderJSON(self, nombre: str='Mapa definido con Builder JSON') -> Laberinto:
        mapa_json = self.cargar_mapa_json(nombre)
        builder = ConcreteBuilder(self)
        director = DirectorJSON(builder)
        director.Construct(mapa_json)
        return builder.GetProduct()

    def fabricarLabConProxy(self, nombre: str='Mapa definido con Builder JSON'):
        return ProxyLaberinto(lambda: self.fabricarLabConBuilderJSON(nombre))

    def ruta_json_laberintos(self) -> Path:
        return Path(__file__).resolve().parent.parent / 'datos' / 'laberintos.json'

    def cargar_mapa_json(self, nombre: str | None=None) -> dict:
        ruta = self.ruta_json_laberintos()
        if not ruta.exists():
            return self.configuracion_mapa_por_defecto()
        try:
            datos = json.loads(ruta.read_text(encoding='utf-8'))
            mapas = datos.get('mapas', [])
            if not mapas:
                return self.configuracion_mapa_por_defecto()
            if nombre is None:
                return mapas[0]
            for mapa in mapas:
                if mapa.get('nombre') == nombre or mapa.get('id') == nombre:
                    return mapa
            return mapas[0]
        except (json.JSONDecodeError, OSError, TypeError):
            return self.configuracion_mapa_por_defecto()

    def configuracion_mapa_por_defecto(self) -> dict:
        return {
            'id': 'aleatorio_por_defecto',
            'nombre': 'Mapa aleatorio',
            'tipo': 'aleatorio',
            'configuracion': {
                'habitaciones_min': 7,
                'habitaciones_max': 12,
                'bombas_min': 2,
                'bombas_max': 3,
                'bichos_min': 2,
                'bichos_max': 4,
                'porcentaje_conexiones_extra': 0.2,
                'probabilidad_bomba_extra': 0.25,
                'probabilidad_puerta_secundaria_abierta': 0.65
            }
        }

    def nombresMapas(self):
        ruta = self.ruta_json_laberintos()
        if not ruta.exists():
            return ['Mapa aleatorio']
        try:
            datos = json.loads(ruta.read_text(encoding='utf-8'))
            return [mapa.get('nombre', mapa.get('id', 'Mapa sin nombre')) for mapa in datos.get('mapas', [])] or ['Mapa aleatorio']
        except (json.JSONDecodeError, OSError, TypeError):
            return ['Mapa aleatorio']

    def fabricarLaberintoPorNombre(self, nombre: str='Mapa aleatorio ampliado') -> Laberinto:
        mapa_json = self.cargar_mapa_json(nombre)
        if mapa_json.get('tipo') == 'definido':
            return self.fabricarLabConBuilderJSON(nombre)
        return self.fabricarMapaAleatorio(nombre)

    def fabricarMapaClasico(self) -> Laberinto:
        return self.fabricarMapaAleatorio()

    def fabricarMapaAleatorio(self, nombre_mapa: str | None=None) -> Laberinto:
        mapa_base = self.cargar_mapa_json(nombre_mapa)
        config = mapa_base.get('configuracion', {})
        direcciones = [(NORTE, (0, -1)), (SUR, (0, 1)), (ESTE, (1, 0)), (OESTE, (-1, 0))]
        habitaciones_min = int(config.get('habitaciones_min', 7))
        habitaciones_max = int(config.get('habitaciones_max', 12))
        total_habitaciones = random.randint(habitaciones_min, habitaciones_max)
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
                if nueva not in ocupadas and -4 <= nueva[0] <= 4 and -4 <= nueva[1] <= 4:
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
        coord_a_num = {coord: numero for numero, coord in enumerate(ordenadas, start=1)}
        num_a_coord = {numero: coord for coord, numero in coord_a_num.items()}

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

        ruta_edges = {frozenset((ruta_segura[i], ruta_segura[i + 1])) for i in range(len(ruta_segura) - 1)}
        aristas_arbol = [(padre_coord, hijo_coord, frozenset((padre_coord, hijo_coord))) for hijo_coord, padre_coord in padre.items()]
        candidatas_bomba = [arista for arista in aristas_arbol if arista[2] not in ruta_edges]
        if len(candidatas_bomba) < 2:
            candidatas_bomba += [arista for arista in aristas_arbol if arista[2] in ruta_edges and arista[0] != (0, 0)]
        random.shuffle(candidatas_bomba)
        cantidad_bombas = min(
            len(candidatas_bomba),
            random.randint(int(config.get('bombas_min', 2)), int(config.get('bombas_max', 3)))
        )
        aristas_bomba = {arista[2] for arista in candidatas_bomba[:cantidad_bombas]}

        conexiones = set()
        puertas_json = []
        for hijo_coord, padre_coord in padre.items():
            orientacion = orientacion_entre(padre_coord, hijo_coord)
            if orientacion is None:
                continue
            clave = frozenset((padre_coord, hijo_coord))
            conexiones.add(clave)
            puertas_json.append({
                'desde': coord_a_num[padre_coord],
                'orientacion': orientacion.nombre(),
                'hasta': coord_a_num[hijo_coord],
                'orientacion_destino': orientacion.opuesta().nombre(),
                'abierta': bool(clave in ruta_edges or clave in aristas_bomba or random.random() < float(config.get('probabilidad_puerta_secundaria_abierta', 0.65))),
                'bomba': bool(clave in aristas_bomba)
            })

        for coord in list(ocupadas):
            for orientacion, (dx, dy) in direcciones:
                vecino = (coord[0] + dx, coord[1] + dy)
                if vecino not in ocupadas:
                    continue
                clave = frozenset((coord, vecino))
                if clave in conexiones:
                    continue
                if random.random() > float(config.get('porcentaje_conexiones_extra', 0.2)):
                    continue
                conexiones.add(clave)
                puertas_json.append({
                    'desde': coord_a_num[coord],
                    'orientacion': orientacion.nombre(),
                    'hasta': coord_a_num[vecino],
                    'orientacion_destino': orientacion.opuesta().nombre(),
                    'abierta': bool(clave in ruta_edges or random.random() < float(config.get('probabilidad_puerta_secundaria_abierta', 0.65))),
                    'bomba': bool(clave not in ruta_edges and random.random() < float(config.get('probabilidad_bomba_extra', 0.25)))
                })

        habitaciones_ruta = [coord_a_num[c] for c in ruta_segura]
        ruta_intermedia = habitaciones_ruta[1:-1]
        laterales = [coord_a_num[c] for c in coords if coord_a_num[c] not in habitaciones_ruta and c != salida_coord]
        candidatas = []
        if ruta_intermedia:
            candidatas.append(random.choice(ruta_intermedia))
        random.shuffle(laterales)
        candidatas.extend(laterales)
        if len(candidatas) < 2:
            candidatas.extend([n for n in coord_a_num.values() if n not in candidatas and n not in (coord_a_num[(0, 0)], coord_a_num[salida_coord])])

        nombres_bichos = ['Bicho rojo', 'Bicho azul', 'Bicho verde', 'Bicho morado', 'Bicho naranja']
        cantidad_bichos = min(
            len(candidatas),
            random.randint(int(config.get('bichos_min', 2)), int(config.get('bichos_max', 4)))
        )
        bichos_json = []
        for i, numero_habitacion in enumerate(candidatas[:cantidad_bichos]):
            if numero_habitacion in ruta_intermedia:
                modo = 'agresivo'
                vidas = 2
            else:
                modo = 'agresivo' if random.random() < 0.45 else 'perezoso'
                vidas = 2 if modo == 'agresivo' else 1
            bichos_json.append({
                'nombre': nombres_bichos[i % len(nombres_bichos)],
                'vidas': vidas,
                'poder': 1,
                'modo': modo,
                'habitacion': numero_habitacion
            })

        mapa_generado = {
            'id': mapa_base.get('id', 'aleatorio_generado'),
            'nombre': mapa_base.get('nombre', 'Mapa aleatorio'),
            'tipo': 'generado_desde_json',
            'descripcion': mapa_base.get('descripcion', 'Mapa aleatorio construido desde una configuración JSON.'),
            'configuracion': config,
            'inicio': coord_a_num[(0, 0)],
            'salida': coord_a_num[salida_coord],
            'habitaciones': [
                {'numero': numero, 'forma': 'cuadrado'}
                for numero in sorted(num_a_coord)
            ],
            'puertas': puertas_json,
            'armarios': [
                {'habitacion': coord_a_num[(0, 0)], 'nombre': 'Armario del inicio'}
            ],
            'bichos': bichos_json,
            'posiciones_mapa': {str(numero): list(coord) for numero, coord in num_a_coord.items()},
            'ruta_segura': habitaciones_ruta
        }

        builder = ConcreteBuilder(self)
        director = DirectorJSON(builder)
        director.Construct(mapa_generado)
        laberinto = builder.GetProduct()
        laberinto.mapa_json = mapa_generado
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
        nombre_mapa = getattr(self, 'mapa_seleccionado', None)
        self.laberinto = self.fabricarLaberintoPorNombre(nombre_mapa) if nombre_mapa else self.fabricarMapaAleatorio()
        self.personaje.posicion = self.laberinto.inicio
        print(f"Laberinto preparado: {getattr(self.laberinto, 'nombre_mapa', 'Mapa')}.")
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
        print('  cerrar <direccion>')
        print('  entrar <direccion>')
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

    def cerrar(self, orientacion: Orientacion):
        lado = self.personaje.posicion.obtener_lado(orientacion)
        if lado is None:
            print('No hay nada que cerrar en esa orientación.')
            return
        if hasattr(lado, 'cerrar') and lado.cerrar():
            print(f'Has cerrado el lado {orientacion.nombre()}.')
        else:
            print('Ese lado no se puede cerrar.')

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
