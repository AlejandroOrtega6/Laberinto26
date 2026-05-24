from modelo.juego import Juego, JuegoBombas


def elegir_opcion(maximo, defecto=1):
    texto = input(f'Elige opción [1-{maximo}]: ').strip()
    if not texto:
        return defecto
    try:
        valor = int(texto)
        if 1 <= valor <= maximo:
            return valor
    except ValueError:
        pass
    print('Opción no válida. Se usará la opción por defecto.')
    return defecto


def main():
    print('Laberinto26 - Alejandro Ortega')
    print('1) Juego normal')
    print('2) Juego con bombas')
    opcion = elegir_opcion(2)
    juego = JuegoBombas('Alejandro') if opcion == 2 else Juego('Alejandro')

    mapas = juego.nombresMapas()
    print('\nMapas disponibles:')
    for indice, nombre in enumerate(mapas, start=1):
        print(f'{indice}) {nombre}')
    opcion_mapa = elegir_opcion(len(mapas))
    juego.mapa_seleccionado = mapas[opcion_mapa - 1]

    juego.TemplateMethod()


if __name__ == '__main__':
    main()
