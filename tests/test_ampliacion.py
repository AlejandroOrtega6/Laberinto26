from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import unittest

from modelo.bomba import Bomba
from modelo.juego import Juego
from modelo.modos import Agresivo, Modo, Perezoso


def contar_bombas(laberinto):
    vistas = set()
    total = 0
    for habitacion in laberinto._habitaciones.values():
        for lado in habitacion._lados.values():
            if isinstance(lado, Bomba) and id(lado) not in vistas:
                vistas.add(id(lado))
                total += 1
    return total


class PruebasAmpliacion(unittest.TestCase):

    def test_json_cargado(self):
        juego = Juego()
        nombres = juego.nombresMapas()
        self.assertIn('Mapa aleatorio ampliado', nombres)
        self.assertIn('Mapa definido con Builder JSON', nombres)
        mapa_json = juego.cargar_mapa_json('Mapa aleatorio ampliado')
        self.assertEqual(mapa_json['tipo'], 'aleatorio')
        self.assertIn('funcionalidades_nuevas', mapa_json)
        self.assertEqual(mapa_json['configuracion']['habitaciones_min'], 7)

    def test_mapa_aleatorio_desde_json_y_builder(self):
        juego = Juego()
        for _ in range(10):
            laberinto = juego.fabricarMapaAleatorio('Mapa aleatorio ampliado')
            self.assertGreaterEqual(len(laberinto._habitaciones), 7)
            self.assertLessEqual(len(laberinto._habitaciones), 12)
            self.assertEqual(laberinto.mapa_json['tipo'], 'generado_desde_json')
            self.assertEqual(len(laberinto.mapa_json['habitaciones']), len(laberinto._habitaciones))
            self.assertIsNotNone(laberinto.inicio)
            self.assertIsNotNone(laberinto.salida)
            self.assertIn(laberinto.inicio.num, laberinto.ruta_segura)
            self.assertIn(laberinto.salida.num, laberinto.ruta_segura)
            self.assertGreaterEqual(len(laberinto.ruta_segura), 2)
            self.assertGreaterEqual(len(laberinto.bichos), 2)
            self.assertLessEqual(len(laberinto.bichos), 4)
            self.assertGreaterEqual(contar_bombas(laberinto), 1)

    def test_builder_json_director(self):
        juego = Juego()
        laberinto = juego.fabricarLabConBuilderJSON('Mapa definido con Builder JSON')
        self.assertEqual(laberinto.nombre_mapa, 'Mapa definido con Builder JSON')
        self.assertEqual(len(laberinto._habitaciones), 4)
        self.assertEqual(laberinto.inicio.num, 1)
        self.assertEqual(laberinto.salida.num, 4)
        self.assertEqual(len(laberinto.bichos), 2)
        self.assertGreaterEqual(contar_bombas(laberinto), 1)

    def test_proxy(self):
        juego = Juego()
        proxy = juego.fabricarLabConProxy('Mapa definido con Builder JSON')
        self.assertFalse(proxy.disponible())
        self.assertTrue(proxy.descripcion().startswith('Laberinto'))
        self.assertTrue(proxy.disponible())
        self.assertEqual(proxy.inicio.num, 1)

    def test_template_method_modo(self):
        self.assertIn('actua', Modo.__dict__)
        self.assertNotIn('actua', Agresivo.__dict__)
        self.assertNotIn('actua', Perezoso.__dict__)
        self.assertIn('debe_caminar', Agresivo.__dict__)
        self.assertIn('debe_caminar', Perezoso.__dict__)

    def test_comandos_base(self):
        juego = Juego()
        self.assertEqual(type(juego.interprete.interpretar('abrir norte')).__name__, 'Abrir')
        self.assertEqual(type(juego.interprete.interpretar('cerrar norte')).__name__, 'Cerrar')
        self.assertEqual(type(juego.interprete.interpretar('entrar norte')).__name__, 'Entrar')


if __name__ == '__main__':
    unittest.main()
