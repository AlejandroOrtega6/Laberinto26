from __future__ import annotations
from .comandos import Abrir, Atacar, Ayuda, ComandoNulo, MostrarMapa, Mover, Salir
from .direcciones import orientacion_desde_texto

class InterpreteComandos:

    def interpretar(self, texto: str):
        texto = texto.strip().lower()
        if not texto:
            return ComandoNulo('No has escrito ningún comando.')
        if texto in ('ayuda', 'help', '?'):
            return Ayuda()
        if texto == 'mapa':
            return MostrarMapa()
        if texto == 'atacar':
            return Atacar()
        if texto in ('salir', 'fin'):
            return Salir()
        if texto.startswith('abrir '):
            posible = texto.split(maxsplit=1)[1]
            orientacion = orientacion_desde_texto(posible)
            if orientacion is None:
                return ComandoNulo('No entiendo esa orientación para abrir.')
            return Abrir(orientacion)
        orientacion = orientacion_desde_texto(texto)
        if orientacion is not None:
            return Mover(orientacion)
        return ComandoNulo("Comando no reconocido. Escribe 'ayuda'.")
