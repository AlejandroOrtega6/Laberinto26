from modelo.juego import Juego, JuegoBombas

def main():
    print('Laberinto26 - Alejandro Ortega')
    print('1) Juego normal')
    print('2) Juego con bombas')
    opcion = input('Elige opción [1/2]: ').strip()
    juego = JuegoBombas('Alejandro') if opcion == '2' else Juego('Alejandro')
    juego.TemplateMethod()
if __name__ == '__main__':
    main()
