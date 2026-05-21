from __future__ import annotations
import contextlib
import io
import math
import tkinter as tk
from tkinter import messagebox, ttk
from modelo.bomba import Bomba
from modelo.estado_puerta import Abierta, Cerrada
from modelo.fases import Final, Jugando
from modelo.formas import Rombo
from modelo.juego import Juego, JuegoBombas
from modelo.puerta import Puerta
from modelo.tunel import Tunel

class InterfazLaberinto:
    BG = '#0f172a'
    PANEL = '#111827'
    PANEL_2 = '#1f2937'
    PANEL_3 = '#0b1220'
    TEXT = '#e5e7eb'
    MUTED = '#94a3b8'
    ACCENT = '#22c55e'
    ACCENT_2 = '#38bdf8'
    WARNING = '#f59e0b'
    DANGER = '#ef4444'
    BORDER = '#334155'
    GOLD = '#fbbf24'

    def __init__(self, root: tk.Tk, con_bombas: bool=True):
        self.root = root
        self.root.title('Laberinto26 - Edición Visual')
        self.root.minsize(1280, 780)
        self.root.configure(bg=self.BG)
        self.con_bombas = con_bombas
        self.juego: Juego | JuegoBombas | None = None
        self.cartel_muerte = None
        self.posiciones: dict[int, tuple[int, int]] = {}
        self._configurar_estilos()
        self._crear_variables()
        self._crear_widgets()
        self.nueva_partida()

    def _configurar_estilos(self):
        style = ttk.Style()
        with contextlib.suppress(Exception):
            style.theme_use('clam')
        style.configure('Root.TFrame', background=self.BG)
        style.configure('Panel.TFrame', background=self.PANEL)
        style.configure('Card.TFrame', background=self.PANEL_2)
        style.configure('TLabelframe', background=self.PANEL, foreground=self.TEXT, bordercolor=self.BORDER)
        style.configure('TLabelframe.Label', background=self.PANEL, foreground=self.TEXT, font=('Segoe UI', 11, 'bold'))
        style.configure('Title.TLabel', background=self.BG, foreground='white', font=('Segoe UI', 24, 'bold'))
        style.configure('SubTitle.TLabel', background=self.BG, foreground=self.MUTED, font=('Segoe UI', 10))
        style.configure('CardTitle.TLabel', background=self.PANEL_2, foreground=self.MUTED, font=('Segoe UI', 9, 'bold'))
        style.configure('CardValue.TLabel', background=self.PANEL_2, foreground='white', font=('Segoe UI', 18, 'bold'))
        style.configure('Body.TLabel', background=self.PANEL, foreground=self.TEXT, font=('Segoe UI', 10))
        style.configure('Muted.TLabel', background=self.PANEL, foreground=self.MUTED, font=('Segoe UI', 9))
        style.configure('Chip.TLabel', background=self.PANEL_2, foreground=self.ACCENT_2, font=('Segoe UI', 9, 'bold'), padding=6)
        style.configure('Accent.TButton', font=('Segoe UI', 10, 'bold'), padding=8)
        style.map('Accent.TButton', foreground=[('active', 'white')], background=[('!disabled', self.ACCENT), ('active', '#16a34a')])

    def _crear_variables(self):
        self.var_fase = tk.StringVar(value='-')
        self.var_turno = tk.StringVar(value='0')
        self.var_vidas = tk.StringVar(value='♡♡♡')
        self.var_poder = tk.StringVar(value='1')
        self.var_habitacion = tk.StringVar(value='-')
        self.var_salida = tk.StringVar(value='-')
        self.var_modo = tk.StringVar(value='Con bombas')
        self.var_hab_info = tk.StringVar(value='-')
        self.var_forma_info = tk.StringVar(value='-')
        self.var_enemigos = tk.StringVar(value='Sin enemigos')
        self.var_rutas = tk.StringVar(value='Sin rutas')
        self.var_elementos = tk.StringVar(value='Sin elementos especiales')

    def _crear_widgets(self):
        self.root.columnconfigure(0, weight=7)
        self.root.columnconfigure(1, weight=4)
        self.root.rowconfigure(1, weight=1)
        self._crear_cabecera()
        self._crear_zona_mapa()
        self._crear_barra_lateral()

    def _crear_cabecera(self):
        cabecera = ttk.Frame(self.root, style='Root.TFrame', padding=(18, 16, 18, 10))
        cabecera.grid(row=0, column=0, columnspan=2, sticky='ew')
        cabecera.columnconfigure(0, weight=1)
        cabecera.columnconfigure(1, weight=0)
        izquierda = ttk.Frame(cabecera, style='Root.TFrame')
        izquierda.grid(row=0, column=0, sticky='w')
        ttk.Label(izquierda, text='🧩 Laberinto26', style='Title.TLabel').grid(row=0, column=0, sticky='w')
        ttk.Label(izquierda, text='Mapa aleatorio • panel de estado, mapa interactivo y registro de eventos', style='SubTitle.TLabel').grid(row=1, column=0, sticky='w', pady=(2, 0))
        derecha = ttk.Frame(cabecera, style='Root.TFrame')
        derecha.grid(row=0, column=1, sticky='e')
        self.lbl_modo = tk.Label(derecha, text='MODO BOMBAS', bg='#052e16', fg='#86efac', font=('Segoe UI', 10, 'bold'), padx=12, pady=6)
        self.lbl_modo.grid(row=0, column=0, padx=(0, 8))
        self.lbl_objetivo = tk.Label(derecha, text='OBJETIVO: ESCAPAR', bg='#3b0764', fg='#e9d5ff', font=('Segoe UI', 10, 'bold'), padx=12, pady=6)
        self.lbl_objetivo.grid(row=0, column=1)

    def _crear_zona_mapa(self):
        izquierda = ttk.Frame(self.root, style='Root.TFrame', padding=(18, 4, 10, 18))
        izquierda.grid(row=1, column=0, sticky='nsew')
        izquierda.rowconfigure(0, weight=7)
        izquierda.rowconfigure(1, weight=2)
        izquierda.columnconfigure(0, weight=1)
        mapa = ttk.LabelFrame(izquierda, text='Mapa del laberinto', padding=10)
        mapa.grid(row=0, column=0, sticky='nsew')
        mapa.rowconfigure(0, weight=1)
        mapa.columnconfigure(0, weight=1)
        self.canvas = tk.Canvas(mapa, bg='#07111f', highlightthickness=1, highlightbackground='#1e293b', bd=0)
        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.canvas.bind('<Configure>', lambda _e: self.dibujar_mapa())
        info = ttk.LabelFrame(izquierda, text='Información de la habitación actual', padding=10)
        info.grid(row=1, column=0, sticky='nsew', pady=(12, 0))
        for i in range(3):
            info.columnconfigure(i, weight=1)
        self._crear_tarjeta_info(info, 0, 0, 'Habitación', self.var_hab_info)
        self._crear_tarjeta_info(info, 0, 1, 'Forma', self.var_forma_info)
        self._crear_tarjeta_info(info, 0, 2, 'Enemigos', self.var_enemigos)
        self._crear_tarjeta_info(info, 1, 0, 'Rutas disponibles', self.var_rutas)
        self._crear_tarjeta_info(info, 1, 1, 'Elementos', self.var_elementos)
        leyenda = tk.Label(info, text='🟢 Jugador   🟡 Salida   🔴 Bicho   🟠 Bomba   🔵 Túnel   — Puerta abierta   - - Puerta cerrada', bg=self.PANEL, fg=self.MUTED, font=('Segoe UI', 9), anchor='w')
        leyenda.grid(row=1, column=2, sticky='ew', padx=8, pady=8)

    def _crear_tarjeta_info(self, parent, row, col, titulo, variable):
        frame = ttk.Frame(parent, style='Card.TFrame', padding=10)
        frame.grid(row=row, column=col, sticky='nsew', padx=6, pady=6)
        parent.rowconfigure(row, weight=1)
        ttk.Label(frame, text=titulo, style='CardTitle.TLabel').pack(anchor='w')
        tk.Label(frame, textvariable=variable, bg=self.PANEL_2, fg='white', font=('Segoe UI', 12, 'bold'), justify='left', anchor='w', wraplength=220).pack(anchor='w', pady=(6, 0), fill='x')

    def _crear_barra_lateral(self):
        derecha = ttk.Frame(self.root, style='Root.TFrame', padding=(10, 4, 18, 18))
        derecha.grid(row=1, column=1, sticky='nsew')
        for i in range(7):
            derecha.rowconfigure(i, weight=0)
        derecha.rowconfigure(6, weight=1)
        derecha.columnconfigure(0, weight=1)
        self._crear_panel_estado(derecha)
        self._crear_panel_movimiento(derecha)
        self._crear_panel_acciones(derecha)
        self._crear_panel_comandos(derecha)
        self._crear_panel_log(derecha)

    def _crear_panel_estado(self, parent):
        panel = ttk.LabelFrame(parent, text='Panel de estado', padding=10)
        panel.grid(row=0, column=0, sticky='ew')
        for i in range(3):
            panel.columnconfigure(i, weight=1)
        cards = [('Fase', self.var_fase), ('Turno', self.var_turno), ('Vidas', self.var_vidas), ('Poder', self.var_poder), ('Tu posición', self.var_habitacion), ('Salida', self.var_salida)]
        for idx, (titulo, var) in enumerate(cards):
            row, col = divmod(idx, 3)
            frame = ttk.Frame(panel, style='Card.TFrame', padding=10)
            frame.grid(row=row, column=col, sticky='nsew', padx=6, pady=6)
            ttk.Label(frame, text=titulo, style='CardTitle.TLabel').pack(anchor='w')
            tk.Label(frame, textvariable=var, bg=self.PANEL_2, fg='white', font=('Segoe UI', 16, 'bold'), anchor='w').pack(anchor='w', pady=(6, 0))

    def _crear_panel_movimiento(self, parent):
        panel = ttk.LabelFrame(parent, text='Control de movimiento', padding=10)
        panel.grid(row=1, column=0, sticky='ew', pady=(12, 0))
        for i in range(3):
            panel.columnconfigure(i, weight=1)
        botones = [('↖\nNO', 'noroeste', 0, 0), ('↑\nN', 'norte', 0, 1), ('↗\nNE', 'noreste', 0, 2), ('←\nO', 'oeste', 1, 0), ('⚔\nAtacar', 'atacar', 1, 1), ('→\nE', 'este', 1, 2), ('↙\nSO', 'suroeste', 2, 0), ('↓\nS', 'sur', 2, 1), ('↘\nSE', 'sureste', 2, 2)]
        for texto, comando, fila, columna in botones:
            btn = tk.Button(panel, text=texto, command=lambda c=comando: self.ejecutar_texto(c), bg='#1e293b', fg='white', activebackground='#334155', activeforeground='white', relief='flat', font=('Segoe UI', 10, 'bold'), padx=10, pady=10, cursor='hand2')
            btn.grid(row=fila, column=columna, padx=4, pady=4, sticky='ew')

    def _crear_panel_acciones(self, parent):
        panel = ttk.LabelFrame(parent, text='Acciones rápidas', padding=10)
        panel.grid(row=2, column=0, sticky='ew', pady=(12, 0))
        panel.columnconfigure(0, weight=1)
        panel.columnconfigure(1, weight=1)
        panel.columnconfigure(2, weight=1)
        ttk.Button(panel, text='🗺 Ver mapa', command=lambda: self.ejecutar_texto('mapa')).grid(row=0, column=0, padx=4, pady=4, sticky='ew')
        ttk.Button(panel, text='❓ Ayuda', command=lambda: self.ejecutar_texto('ayuda')).grid(row=0, column=1, padx=4, pady=4, sticky='ew')
        ttk.Button(panel, text='🎲 Nuevo mapa', command=self.nueva_partida).grid(row=0, column=2, padx=4, pady=4, sticky='ew')
        abrir_frame = ttk.LabelFrame(panel, text='Puertas de esta habitación', padding=8)
        abrir_frame.grid(row=1, column=0, columnspan=3, sticky='ew', pady=(8, 0))
        abrir_frame.columnconfigure(0, weight=1)
        self.lbl_puertas = tk.Label(abrir_frame, text='', bg=self.PANEL, fg=self.MUTED, font=('Segoe UI', 9), anchor='w', justify='left')
        self.lbl_puertas.grid(row=0, column=0, columnspan=3, sticky='ew', pady=(0, 6))
        self.combo_abrir = ttk.Combobox(abrir_frame, state='readonly', values=[])
        self.combo_abrir.grid(row=1, column=0, sticky='ew', padx=(0, 6))
        self.btn_abrir = ttk.Button(abrir_frame, text='🚪 Abrir puerta', command=self.abrir_seleccion)
        self.btn_abrir.grid(row=1, column=1, padx=(0, 6))
        ttk.Button(abrir_frame, text='⏹ Salir', command=lambda: self.ejecutar_texto('salir')).grid(row=1, column=2)

    def _crear_panel_comandos(self, parent):
        panel = ttk.LabelFrame(parent, text='Consola de comandos', padding=10)
        panel.grid(row=3, column=0, sticky='ew', pady=(12, 0))
        panel.columnconfigure(0, weight=1)
        self.entrada = tk.Entry(panel, bg='#0f172a', fg='white', insertbackground='white', relief='flat', font=('Consolas', 11))
        self.entrada.grid(row=0, column=0, sticky='ew', padx=(0, 6), ipady=6)
        self.entrada.bind('<Return>', lambda _event: self.ejecutar_desde_entrada())
        ttk.Button(panel, text='Ejecutar', command=self.ejecutar_desde_entrada).grid(row=0, column=1)
        chips = ttk.Frame(panel, style='Panel.TFrame')
        chips.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(8, 0))
        sugerencias = ['norte', 'abrir este', 'atacar', 'mapa', 'ayuda']
        for i, texto in enumerate(sugerencias):
            chip = tk.Button(chips, text=texto, command=lambda t=texto: self.ejecutar_texto(t), bg='#172554', fg='#bfdbfe', relief='flat', cursor='hand2', font=('Segoe UI', 9, 'bold'), padx=10, pady=4)
            chip.grid(row=0, column=i, padx=3, pady=2, sticky='w')

    def _crear_panel_log(self, parent):
        panel = ttk.LabelFrame(parent, text='Registro de eventos', padding=10)
        panel.grid(row=6, column=0, sticky='nsew', pady=(12, 0))
        panel.rowconfigure(0, weight=1)
        panel.columnconfigure(0, weight=1)
        self.txt_salida = tk.Text(panel, width=44, height=18, wrap='word', state='disabled', bg='#020617', fg='#e2e8f0', insertbackground='white', relief='flat', font=('Consolas', 10), padx=10, pady=10)
        self.txt_salida.grid(row=0, column=0, sticky='nsew')
        scroll = ttk.Scrollbar(panel, orient='vertical', command=self.txt_salida.yview)
        scroll.grid(row=0, column=1, sticky='ns')
        self.txt_salida.configure(yscrollcommand=scroll.set)
        self.txt_salida.tag_configure('prompt', foreground='#38bdf8')
        self.txt_salida.tag_configure('system', foreground='#cbd5e1')
        self.txt_salida.tag_configure('good', foreground='#86efac')
        self.txt_salida.tag_configure('warn', foreground='#fbbf24')
        self.txt_salida.tag_configure('bad', foreground='#fca5a5')

    def nueva_partida(self):
        self._cerrar_cartel_muerte()
        self.juego = JuegoBombas('Alejandro') if self.con_bombas else Juego('Alejandro')
        self.juego.laberinto = self.juego.fabricarMapaAleatorio()
        self.juego.personaje.posicion = self.juego.laberinto.inicio
        self.juego.fase = Jugando()
        self.juego.turno = 1
        self.juego.ganado = False
        self.var_modo.set('Con bombas' if self.con_bombas else 'Normal')
        self.lbl_modo.configure(text='MODO BOMBAS' if self.con_bombas else 'MODO NORMAL', bg='#052e16' if self.con_bombas else '#172554', fg='#86efac' if self.con_bombas else '#bfdbfe')
        self.limpiar_salida()
        habitaciones = len(self.juego.laberinto._habitaciones)
        salida = self.juego.laberinto.salida.num
        bombas = self.contar_bombas_visibles()
        self.escribir(f'[Sistema] Nuevo mapa aleatorio generado con {habitaciones} habitaciones.\n', 'good')
        self.escribir(f'[Sistema] Objetivo: llegar hasta la habitación H{salida}.\n', 'system')
        self.escribir(f'[Sistema] Bombas colocadas en el mapa: {bombas}. No están en todas las puertas.\n', 'system')
        self.actualizar_interfaz()

    def contar_bombas_visibles(self):
        if self.juego is None or self.juego.laberinto is None:
            return 0
        total = 0
        vistos = set()
        for habitacion in self.juego.laberinto._habitaciones.values():
            for orientacion in habitacion.forma.orientaciones():
                lado = habitacion.obtener_lado(orientacion)
                if isinstance(lado, Bomba) and id(lado) not in vistos:
                    vistos.add(id(lado))
                    total += 1
        return total

    def abrir_seleccion(self):
        direccion = self.combo_abrir.get().strip()
        if not direccion:
            self.escribir('[Sistema] No hay ninguna puerta cerrada que abrir en esta habitación.\n', 'warn')
            return
        self.ejecutar_texto(f'abrir {direccion}')

    def ejecutar_desde_entrada(self):
        texto = self.entrada.get().strip()
        self.entrada.delete(0, tk.END)
        self.ejecutar_texto(texto)

    def ejecutar_texto(self, texto: str):
        if self.juego is None:
            return
        if isinstance(self.juego.fase, Final):
            messagebox.showinfo('Partida finalizada', "La partida ya ha terminado. Pulsa 'Nueva' para volver a jugar.")
            return
        texto = texto.strip()
        if not texto:
            return
        self.escribir(f'> {texto}\n', 'prompt')
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida):
            comando = self.juego.interprete.interpretar(texto)
            comando.ejecutar(self.juego)
            self.juego.comprobar_fin()
            if not isinstance(self.juego.fase, Final) and texto not in ('mapa', 'ayuda', 'help', '?'):
                self.juego.turno_bichos()
                self.juego.comprobar_fin()
                self.juego.turno += 1
        generado = salida.getvalue().strip()
        if generado:
            tag = self._inferir_tag(generado)
            self.escribir(generado + '\n', tag)
        if isinstance(self.juego.fase, Final):
            final = io.StringIO()
            with contextlib.redirect_stdout(final):
                self.juego.mostrar_final()
            texto_final = final.getvalue().strip()
            if texto_final:
                self.escribir(texto_final + '\n', 'good' if self.juego.ganado else 'bad')
            if self.juego.ganado:
                messagebox.showinfo('Victoria', '¡Has ganado! Has llegado a la salida del laberinto.')
            elif self.juego.personaje.esta_muerto():
                self.mostrar_cartel_muerte()
        self.actualizar_interfaz()

    def _inferir_tag(self, texto: str) -> str:
        t = texto.lower()
        if any((p in t for p in ['has ganado', 'partida iniciada', 'abierto'])):
            return 'good'
        if any((p in t for p in ['muerto', 'perdido', 'daño'])):
            return 'bad'
        if any((p in t for p in ['bomba', 'cerrada', 'no hay', 'no se puede', 'comando no reconocido'])):
            return 'warn'
        return 'system'

    def actualizar_interfaz(self):
        self.actualizar_estado()
        self.actualizar_info_habitacion()
        self.actualizar_opciones_abrir()
        self.dibujar_mapa()

    def actualizar_estado(self):
        if self.juego is None or self.juego.personaje.posicion is None:
            return
        personaje = self.juego.personaje
        self.var_fase.set(self.juego.fase.nombre().capitalize())
        self.var_turno.set(str(self.juego.turno))
        self.var_vidas.set('❤' * personaje.vidas + '·' * max(0, 3 - personaje.vidas))
        self.var_poder.set(str(personaje.poder))
        self.var_habitacion.set(f'H{personaje.posicion.num}')
        salida = self.juego.laberinto.salida.num if self.juego.laberinto and self.juego.laberinto.salida else '?'
        self.var_salida.set(f'H{salida}')

    def actualizar_opciones_abrir(self):
        if self.juego is None or self.juego.personaje.posicion is None:
            return
        h = self.juego.personaje.posicion
        puertas_cerradas = []
        puertas_abiertas = []
        for orientacion in h.forma.orientaciones():
            lado = h.obtener_lado(orientacion)
            if lado is None:
                continue
            elemento = lado.em if isinstance(lado, Bomba) else lado
            if not isinstance(elemento, Puerta):
                continue
            destino = elemento.destino_desde(h)
            destino_txt = f'H{destino.num}' if destino is not None else '?'
            etiqueta = f'{orientacion.nombre()} → {destino_txt}'
            if isinstance(elemento.estado, Cerrada):
                puertas_cerradas.append(orientacion.nombre())
            else:
                puertas_abiertas.append(etiqueta)
        self.combo_abrir.configure(values=puertas_cerradas)
        if puertas_cerradas:
            if self.combo_abrir.get() not in puertas_cerradas:
                self.combo_abrir.set(puertas_cerradas[0])
            self.combo_abrir.configure(state='readonly')
            self.btn_abrir.configure(state='normal')
            self.lbl_puertas.configure(text='Puertas cerradas: ' + ', '.join(puertas_cerradas))
        else:
            self.combo_abrir.set('')
            self.combo_abrir.configure(state='disabled')
            self.btn_abrir.configure(state='disabled')
            if puertas_abiertas:
                self.lbl_puertas.configure(text='No hay puertas cerradas. Abiertas: ' + ', '.join(puertas_abiertas))
            else:
                self.lbl_puertas.configure(text='No hay puertas en esta habitación.')

    def actualizar_info_habitacion(self):
        if self.juego is None or self.juego.personaje.posicion is None:
            return
        h = self.juego.personaje.posicion
        self.var_hab_info.set(f'Habitación {h.num}')
        self.var_forma_info.set(h.forma.__class__.__name__)
        bichos = [b for b in self.juego.laberinto.bichos if b.esta_vivo() and b.posicion == h]
        if bichos:
            self.var_enemigos.set(', '.join((f'{b.nombre} ({b.modo.nombre()}, {b.vidas}V)' for b in bichos)))
        else:
            self.var_enemigos.set('Sin enemigos')
        rutas = []
        elementos = []
        for orientacion in h.forma.orientaciones():
            lado = h.obtener_lado(orientacion)
            if lado is None:
                continue
            destino = lado.destino_desde(h)
            elemento = lado.em if isinstance(lado, Bomba) else lado
            extra = ''
            if isinstance(elemento, Puerta):
                extra = 'abierta' if isinstance(elemento.estado, Abierta) else 'cerrada'
            elif isinstance(elemento, Tunel):
                extra = 'túnel'
            elif destino is None:
                extra = elemento.descripcion()
            etiqueta = orientacion.nombre()
            if destino is not None:
                etiqueta += f' → H{destino.num}'
            if extra:
                etiqueta += f' ({extra})'
            rutas.append(etiqueta)
            if isinstance(lado, Bomba):
                elementos.append(f'Bomba en {orientacion.nombre()}')
        for hijo in h.GetChildren():
            if hijo not in [h.obtener_lado(o) for o in h.forma.orientaciones() if h.obtener_lado(o) is not None]:
                elementos.append(hijo.descripcion())
        self.var_rutas.set('\n'.join(rutas) if rutas else 'Sin rutas')
        self.var_elementos.set('\n'.join(elementos) if elementos else 'Sin elementos especiales')

    def dibujar_mapa(self):
        if self.juego is None or self.juego.laberinto is None:
            return
        self.canvas.delete('all')
        ancho = max(self.canvas.winfo_width(), 760)
        alto = max(self.canvas.winfo_height(), 540)
        self._dibujar_fondo_mapa(ancho, alto)
        habitaciones = list(self.juego.laberinto._habitaciones.values())
        self.posiciones = self._calcular_posiciones(habitaciones, ancho, alto)
        self._dibujar_conexiones(habitaciones)
        for habitacion in habitaciones:
            self._dibujar_habitacion(habitacion)
        self._dibujar_bombas_pared(habitaciones)
        self._dibujar_bichos()
        self._dibujar_personaje()

    def _dibujar_fondo_mapa(self, ancho: int, alto: int):
        self.canvas.create_rectangle(0, 0, ancho, alto, fill='#07111f', outline='')
        paso = 40
        for x in range(0, ancho, paso):
            self.canvas.create_line(x, 0, x, alto, fill='#0f1a2e')
        for y in range(0, alto, paso):
            self.canvas.create_line(0, y, ancho, y, fill='#0f1a2e')
        self.canvas.create_text(18, 18, anchor='w', text='Vista táctica del laberinto', fill='#64748b', font=('Segoe UI', 10, 'bold'))

    def _calcular_posiciones(self, habitaciones, ancho: int, alto: int):
        if self.juego is not None and hasattr(self.juego.laberinto, 'posiciones_mapa'):
            coords = self.juego.laberinto.posiciones_mapa
            xs = [coord[0] for coord in coords.values()]
            ys = [coord[1] for coord in coords.values()]
            min_x, max_x = (min(xs), max(xs))
            min_y, max_y = (min(ys), max(ys))
            margen_x = max(90, int(ancho * 0.12))
            margen_y = max(80, int(alto * 0.14))
            ancho_util = max(1, ancho - 2 * margen_x)
            alto_util = max(1, alto - 2 * margen_y)
            rango_x = max(1, max_x - min_x)
            rango_y = max(1, max_y - min_y)
            posiciones = {}
            for num, (gx, gy) in coords.items():
                x = margen_x + int((gx - min_x) / rango_x * ancho_util)
                y = margen_y + int((gy - min_y) / rango_y * alto_util)
                posiciones[num] = (x, y)
            return posiciones
        posiciones_base = {1: (int(ancho * 0.22), int(alto * 0.25)), 2: (int(ancho * 0.58), int(alto * 0.25)), 3: (int(ancho * 0.22), int(alto * 0.66)), 4: (int(ancho * 0.58), int(alto * 0.62)), 5: (int(ancho * 0.42), int(alto * 0.46)), 6: (int(ancho * 0.8), int(alto * 0.46))}
        posiciones: dict[int, tuple[int, int]] = {}
        extra = []
        for habitacion in habitaciones:
            if habitacion.num in posiciones_base:
                posiciones[habitacion.num] = posiciones_base[habitacion.num]
            else:
                extra.append(habitacion)
        if extra:
            cx, cy = (ancho // 2, alto // 2)
            radio = min(ancho, alto) // 3
            for i, habitacion in enumerate(extra):
                angulo = 2 * math.pi * i / max(1, len(extra))
                posiciones[habitacion.num] = (int(cx + radio * math.cos(angulo)), int(cy + radio * math.sin(angulo)))
        return posiciones

    def _dibujar_conexiones(self, habitaciones):
        dibujadas = set()
        for habitacion in habitaciones:
            x1, y1 = self.posiciones[habitacion.num]
            for orientacion in habitacion.forma.orientaciones():
                lado = habitacion.obtener_lado(orientacion)
                if lado is None:
                    continue
                destino = lado.destino_desde(habitacion)
                if destino is None or destino.num not in self.posiciones:
                    continue
                clave = (min(habitacion.num, destino.num), max(habitacion.num, destino.num), id(lado))
                if clave in dibujadas:
                    continue
                dibujadas.add(clave)
                x2, y2 = self.posiciones[destino.num]
                elemento = lado.em if isinstance(lado, Bomba) else lado
                color = self.WARNING if isinstance(lado, Bomba) else '#64748b'
                dash = ()
                texto = ''
                etiqueta_color = '#cbd5e1'
                if isinstance(elemento, Puerta):
                    abierta = isinstance(elemento.estado, Abierta)
                    texto = 'Puerta abierta' if abierta else 'Puerta cerrada'
                    dash = () if abierta else (7, 5)
                    etiqueta_color = '#a7f3d0' if abierta else '#fca5a5'
                elif isinstance(elemento, Tunel):
                    color = self.ACCENT_2
                    texto = 'Túnel'
                    dash = (2, 3)
                self.canvas.create_line(x1, y1, x2, y2, width=4, fill=color, dash=dash)
                mx, my = ((x1 + x2) // 2, (y1 + y2) // 2)
                if texto:
                    self.canvas.create_text(mx, my - 14, text=texto, fill=etiqueta_color, font=('Segoe UI', 9, 'bold'))
                if isinstance(lado, Bomba):
                    self.canvas.create_text(mx, my + 12, text='BOMBA', fill=self.WARNING, font=('Segoe UI', 8, 'bold'))

    def _dibujar_habitacion(self, habitacion):
        x, y = self.posiciones[habitacion.num]
        r = 54
        es_actual = habitacion == self.juego.personaje.posicion
        es_salida = habitacion == self.juego.laberinto.salida
        self._crear_sombra(x, y, r)
        relleno = '#d1fae5' if es_actual else '#e2e8f0'
        borde = self.GOLD if es_salida else '#0f172a'
        grosor = 5 if es_salida else 3
        if isinstance(habitacion.forma, Rombo):
            puntos = [x, y - r, x + r, y, x, y + r, x - r, y]
            self.canvas.create_polygon(puntos, fill=relleno, outline=borde, width=grosor)
        else:
            self._round_rect(x - r, y - r, x + r, y + r, radius=16, fill=relleno, outline=borde, width=grosor)
        if es_salida:
            self.canvas.create_text(x, y - 32, text='⭐ SALIDA', fill=self.GOLD, font=('Segoe UI', 10, 'bold'))
        self.canvas.create_text(x, y - 8, text=f'H{habitacion.num}', font=('Segoe UI', 16, 'bold'), fill='#111827')
        self.canvas.create_text(x, y + 16, text=habitacion.forma.__class__.__name__, font=('Segoe UI', 9), fill='#334155')

    def _dibujar_personaje(self):
        h = self.juego.personaje.posicion
        if h is None or h.num not in self.posiciones:
            return
        x, y = self.posiciones[h.num]
        self.canvas.create_oval(x - 17, y + 34, x + 17, y + 68, fill=self.ACCENT, outline='#166534', width=3)
        self.canvas.create_text(x, y + 51, text='TÚ', fill='white', font=('Segoe UI', 8, 'bold'))

    def _dibujar_bombas_pared(self, habitaciones):
        desplazamientos = {'norte': (0, -78), 'sur': (0, 78), 'este': (78, 0), 'oeste': (-78, 0)}
        for habitacion in habitaciones:
            if habitacion.num not in self.posiciones:
                continue
            x, y = self.posiciones[habitacion.num]
            for orientacion in habitacion.forma.orientaciones():
                lado = habitacion.obtener_lado(orientacion)
                if not isinstance(lado, Bomba):
                    continue
                elemento = lado.em
                if isinstance(elemento, Puerta):
                    continue
                dx, dy = desplazamientos.get(orientacion.nombre(), (0, 0))
                bx, by = (x + dx, y + dy)
                self.canvas.create_oval(bx - 15, by - 15, bx + 15, by + 15, fill=self.WARNING, outline='#78350f', width=2)
                self.canvas.create_text(bx, by, text='!', fill='#111827', font=('Segoe UI', 14, 'bold'))

    def _dibujar_bichos(self):
        for bicho in self.juego.laberinto.bichos:
            if not bicho.esta_vivo() or bicho.posicion.num not in self.posiciones:
                continue
            x, y = self.posiciones[bicho.posicion.num]
            desplazamiento = -24 if bicho.modo.nombre() == 'agresivo' else 24
            self.canvas.create_oval(x - 15 + desplazamiento, y - 68, x + 15 + desplazamiento, y - 38, fill=self.DANGER, outline='#7f1d1d', width=3)
            self.canvas.create_text(x + desplazamiento, y - 53, text='B', fill='white', font=('Segoe UI', 9, 'bold'))

    def _crear_sombra(self, x, y, r):
        self.canvas.create_oval(x - r + 8, y - r + 8, x + r + 8, y + r + 8, fill='#020617', outline='')

    def _round_rect(self, x1, y1, x2, y2, radius=14, **kwargs):
        points = [x1 + radius, y1, x2 - radius, y1, x2, y1, x2, y1 + radius, x2, y2 - radius, x2, y2, x2 - radius, y2, x1 + radius, y2, x1, y2, x1, y2 - radius, x1, y1 + radius, x1, y1]
        return self.canvas.create_polygon(points, smooth=True, splinesteps=20, **kwargs)

    def escribir(self, texto: str, tag: str='system'):
        self.txt_salida.configure(state='normal')
        self.txt_salida.insert(tk.END, texto, (tag,))
        self.txt_salida.see(tk.END)
        self.txt_salida.configure(state='disabled')

    def limpiar_salida(self):
        self.txt_salida.configure(state='normal')
        self.txt_salida.delete('1.0', tk.END)
        self.txt_salida.configure(state='disabled')

    def _cerrar_cartel_muerte(self):
        if self.cartel_muerte is not None:
            try:
                self.cartel_muerte.grab_release()
                self.cartel_muerte.destroy()
            except tk.TclError:
                pass
            self.cartel_muerte = None

    def mostrar_cartel_muerte(self):
        if self.cartel_muerte is not None:
            try:
                if self.cartel_muerte.winfo_exists():
                    return
            except tk.TclError:
                self.cartel_muerte = None
        cartel = tk.Toplevel(self.root)
        self.cartel_muerte = cartel
        cartel.title('Has muerto')
        cartel.configure(bg='#111827')
        cartel.resizable(False, False)
        cartel.transient(self.root)
        cartel.grab_set()
        contenedor = tk.Frame(cartel, bg='#111827', padx=36, pady=28)
        contenedor.pack(fill='both', expand=True)
        tk.Label(contenedor, text='☠', bg='#111827', fg='#fca5a5', font=('Segoe UI', 42, 'bold')).pack(pady=(0, 4))
        tk.Label(contenedor, text='HAS MUERTO', bg='#111827', fg='#ffffff', font=('Segoe UI', 28, 'bold')).pack()
        tk.Label(contenedor, text='El personaje se ha quedado sin vidas.', bg='#111827', fg='#cbd5e1', font=('Segoe UI', 11)).pack(pady=(8, 18))
        tk.Button(contenedor, text='Volver a jugar', command=self.nueva_partida, bg='#22c55e', fg='white', activebackground='#16a34a', activeforeground='white', relief='flat', cursor='hand2', font=('Segoe UI', 12, 'bold'), padx=24, pady=10).pack()
        cartel.update_idletasks()
        ancho = 420
        alto = 260
        x = self.root.winfo_x() + self.root.winfo_width() // 2 - ancho // 2
        y = self.root.winfo_y() + self.root.winfo_height() // 2 - alto // 2
        cartel.geometry(f'{ancho}x{alto}+{max(0, x)}+{max(0, y)}')
        cartel.protocol('WM_DELETE_WINDOW', self.nueva_partida)

def lanzar_interfaz(con_bombas: bool=True):
    root = tk.Tk()
    InterfazLaberinto(root, con_bombas=con_bombas)
    root.mainloop()
