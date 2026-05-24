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


def prueba_estructural_json():
    juego = Juego()
    nombres = juego.nombresMapas()
    assert "Mapa aleatorio ampliado" in nombres
    assert "Mapa definido con Builder JSON" in nombres
    mapa_json = juego.cargar_mapa_json("Mapa aleatorio ampliado")
    assert mapa_json["tipo"] == "aleatorio"
    assert "funcionalidades_nuevas" in mapa_json
    assert mapa_json["configuracion"]["habitaciones_min"] == 7
    print("OK - JSON cargado correctamente")


def prueba_comportamiento_mapa_aleatorio():
    juego = Juego()
    for _ in range(10):
        laberinto = juego.fabricarMapaAleatorio("Mapa aleatorio ampliado")
        assert 7 <= len(laberinto._habitaciones) <= 12
        assert laberinto.mapa_json["tipo"] == "generado_desde_json"
        assert len(laberinto.mapa_json["habitaciones"]) == len(laberinto._habitaciones)
        assert laberinto.inicio is not None
        assert laberinto.salida is not None
        assert laberinto.inicio.num in laberinto.ruta_segura
        assert laberinto.salida.num in laberinto.ruta_segura
        assert len(laberinto.ruta_segura) >= 2
        assert 2 <= len(laberinto.bichos) <= 4
        assert contar_bombas(laberinto) >= 1
    print("OK - mapas aleatorios jugables generados desde JSON con Builder")


def prueba_builder_json_director():
    juego = Juego()
    laberinto = juego.fabricarLabConBuilderJSON("Mapa definido con Builder JSON")
    assert laberinto.nombre_mapa == "Mapa definido con Builder JSON"
    assert len(laberinto._habitaciones) == 4
    assert laberinto.inicio.num == 1
    assert laberinto.salida.num == 4
    assert len(laberinto.bichos) == 2
    assert contar_bombas(laberinto) >= 1
    print("OK - Builder y DirectorJSON construyen el mapa desde JSON")


def prueba_proxy():
    juego = Juego()
    proxy = juego.fabricarLabConProxy("Mapa definido con Builder JSON")
    assert not proxy.disponible()
    assert proxy.descripcion().startswith("Laberinto")
    assert proxy.disponible()
    assert proxy.inicio.num == 1
    print("OK - Proxy carga el laberinto de forma diferida")


def prueba_template_method_modo():
    assert "actua" in Modo.__dict__
    assert "actua" not in Agresivo.__dict__
    assert "actua" not in Perezoso.__dict__
    assert "debe_caminar" in Agresivo.__dict__
    assert "debe_caminar" in Perezoso.__dict__
    print("OK - Template Method corregido en Modo")


def prueba_comandos_base():
    juego = Juego()
    assert type(juego.interprete.interpretar("abrir norte")).__name__ == "Abrir"
    assert type(juego.interprete.interpretar("cerrar norte")).__name__ == "Cerrar"
    assert type(juego.interprete.interpretar("entrar norte")).__name__ == "Entrar"
    print("OK - comandos Abrir, Cerrar y Entrar reconocidos")


if __name__ == "__main__":
    prueba_estructural_json()
    prueba_comportamiento_mapa_aleatorio()
    prueba_builder_json_director()
    prueba_proxy()
    prueba_template_method_modo()
    prueba_comandos_base()
    print("TODAS LAS PRUEBAS HAN PASADO")
