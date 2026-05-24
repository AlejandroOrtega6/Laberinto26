<div align="center">

# 🧩 Laberinto26 - Versión 3.0

### Juego de laberinto en Python aplicando patrones de diseño

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![POO](https://img.shields.io/badge/POO-Programación%20Orientada%20a%20Objetos-orange)
![Diseño](https://img.shields.io/badge/Asignatura-Diseño%20de%20Software-purple)
![Versión](https://img.shields.io/badge/Versión-3.0-success)

**Autor:** Alejandro Ortega Mendoza  
**Asignatura:** Diseño de Software  
**Repositorio:** `Laberinto26`

</div>

---

## Descripción

**Laberinto26** es un juego de laberinto desarrollado en Python. El jugador controla un personaje que debe avanzar por habitaciones hasta llegar a la salida, evitando bombas y enfrentándose a bichos.

El proyecto está dividido en una capa de lógica y una capa de interfaz gráfica. La solución usa varios patrones de diseño trabajados en clase y añade una ampliación basada en JSON.

---

## Versión 3.0

La versión 3.0 actualiza el proyecto para cubrir los patrones pendientes indicados en la revisión y deja la ampliación integrada en el código y en el archivo JSON.

### Cambios principales

- Generación aleatoria de laberintos jugables.
- Configuración de la ampliación desde `datos/laberintos.json`.
- Mapa definido desde JSON usando `Builder` y `DirectorJSON`.
- Corrección del patrón `Template Method` en la clase `Modo`.
- Añadido patrón `Proxy` para carga diferida de laberintos.
- Revisión de `Singleton` mediante el método `Instance()` de las factorías.
- Interfaz gráfica principal renombrada a `interfaz_laberinto26.py`.
- Comandos base `Abrir`, `Cerrar` y `Entrar` disponibles.
- Pruebas de la ampliación en `tests_pruebas_ampliacion.py`.

---

## Funcionalidad base

La funcionalidad base del proyecto incluye:

- Formas: `Cuadrado` y `Rombo`.
- Bichos: `Agresivo` y `Perezoso`.
- Estados en `Ente`, `Puerta` y `Juego`.
- Comandos para puertas: `Abrir`, `Cerrar` y `Entrar`.
- Capas de lógica y GUI.
- Elementos del mapa: habitaciones, paredes, puertas, bombas, túneles y armarios.

---

## Ampliación implementada

### Mapa aleatorio

El juego puede generar un laberinto distinto en cada partida.

Características:

- número variable de habitaciones;
- habitación inicial y habitación de salida;
- ruta principal garantizada;
- salida alejada del inicio;
- bombas colocadas en puertas transitables;
- bichos colocados en ruta y zonas secundarias.

### JSON

La ampliación está incluida en:

```text
/datos/laberintos.json
```

Ese archivo contiene dos tipos de mapa:

1. `Mapa aleatorio ampliado`, usado para generar mapas aleatorios con parámetros configurables.
2. `Mapa definido con Builder JSON`, usado para construir un laberinto completo desde datos JSON usando `Builder` y `DirectorJSON`.

---

## Cómo ejecutar

### Versión gráfica

```bash
python main_gui.py
```

### Versión consola

```bash
python main.py
```

### Pruebas

```bash
python tests_pruebas_ampliacion.py
```

---

## Cómo jugar

Comandos disponibles en consola o en la caja de comandos de la interfaz:

| Comando | Acción |
|---|---|
| `norte` / `n` | Mover al norte |
| `sur` / `s` | Mover al sur |
| `este` / `e` | Mover al este |
| `oeste` / `o` | Mover al oeste |
| `noreste` / `ne` | Mover al noreste |
| `noroeste` / `no` | Mover al noroeste |
| `sureste` / `se` | Mover al sureste |
| `suroeste` / `so` | Mover al suroeste |
| `abrir norte` | Abrir una puerta |
| `cerrar norte` | Cerrar una puerta |
| `entrar norte` | Entrar por una dirección |
| `atacar` | Atacar a un bicho |
| `mapa` | Mostrar información del mapa |
| `ayuda` | Mostrar ayuda |
| `salir` | Terminar la partida |

---

## Estructura del proyecto

```text
Laberinto26/
├── datos/
│   └── laberintos.json
├── interfaz/
│   ├── __init__.py
│   └── interfaz_laberinto26.py
├── modelo/
│   ├── armario.py
│   ├── bicho.py
│   ├── bomba.py
│   ├── builder.py
│   ├── comandos.py
│   ├── contenedor.py
│   ├── decorador.py
│   ├── direcciones.py
│   ├── elemento_mapa.py
│   ├── ente.py
│   ├── estado_ente.py
│   ├── estado_puerta.py
│   ├── factorias.py
│   ├── fases.py
│   ├── formas.py
│   ├── habitacion.py
│   ├── hoja.py
│   ├── interprete.py
│   ├── iterador.py
│   ├── juego.py
│   ├── laberinto.py
│   ├── modos.py
│   ├── pared.py
│   ├── personaje.py
│   ├── proxy.py
│   ├── puerta.py
│   ├── tunel.py
│   └── visitante.py
├── main.py
├── main_gui.py
├── tests_pruebas_ampliacion.py
├── README.md
└── .gitignore
```

---

## Patrones de diseño usados

### Composite

Representa la estructura del mapa.

- `ElementoMapa`
- `Contenedor`
- `Hoja`
- `Laberinto`
- `Habitacion`
- `Armario`

Una habitación puede contener elementos y el laberinto contiene habitaciones.

### Decorator

Permite añadir comportamiento a un elemento del mapa.

- `Decorator`
- `Bomba`

La bomba envuelve una puerta o una pared y añade el efecto de daño.

### State

Gestiona objetos cuyo comportamiento cambia según su estado.

- `EstadoPuerta`: `Abierta`, `Cerrada`.
- `EstadoEnte`: `Vivo`, `Muerto`.
- `Fase`: `Inicial`, `Jugando`, `Final`.

### Strategy

Permite cambiar el comportamiento de los bichos.

- `Agresivo`
- `Perezoso`

Cada modo decide cómo actúa el bicho.

### Template Method

Aplicado en `Modo`.

La clase base `Modo` define el algoritmo general de actuación:

1. comprobar si el bicho puede actuar;
2. comprobar si está en la habitación del jugador;
3. atacar, moverse o esperar.

Las subclases `Agresivo` y `Perezoso` solo redefinen pasos concretos como `debe_caminar()` y `caminar()`.

### Factory Method / Abstract Factory

La creación de objetos se centraliza mediante métodos de fabricación.

- `fabricarLaberinto`
- `fabricarHabitacion`
- `fabricarPuerta`
- `fabricarBomba`
- `fabricarBicho`

Las factorías permiten crear familias de objetos normales o con bombas.

### Builder

Construye laberintos paso a paso.

- `Builder`
- `ConcreteBuilder`
- `Director`
- `DirectorJSON`

`DirectorJSON` lee la estructura del mapa desde JSON y ordena al builder crear habitaciones, puertas, bombas, túneles, bichos, inicio y salida.

### Singleton

Las factorías usan `Instance()` para mantener una única instancia compartida.

- `ConcreteFactory.Instance()`
- `ConcreteFactoryBombas.Instance()`

### Proxy

`ProxyLaberinto` permite retrasar la creación real del laberinto hasta que se necesita.

Esto se usa como ejemplo de acceso controlado al objeto real.

### Command

Representa acciones del jugador como objetos.

- `Abrir`
- `Cerrar`
- `Entrar`
- `Mover`
- `Atacar`
- `MostrarMapa`
- `Salir`

### Interpreter

Convierte el texto escrito por el jugador en comandos ejecutables.

Ejemplos:

```text
abrir este
cerrar norte
entrar sur
atacar
mapa
```

### Facade

La clase `Juego` actúa como punto principal de acceso al sistema.

Centraliza la creación del laberinto, el personaje, los bichos, los comandos y el control general de la partida.

---

## Pruebas incluidas

El archivo `tests_pruebas_ampliacion.py` comprueba:

- que el JSON se carga correctamente;
- que el mapa aleatorio genera habitaciones, bichos y bombas;
- que `Builder` y `DirectorJSON` construyen un mapa desde JSON;
- que `ProxyLaberinto` carga el laberinto de forma diferida;
- que `Template Method` está en la clase base `Modo`;
- que los comandos `Abrir`, `Cerrar` y `Entrar` son reconocidos.

---

## Autor

**Alejandro Ortega Mendoza**  
Grado en Ingeniería Informática  
Universidad de Castilla-La Mancha
