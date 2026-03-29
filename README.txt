Proyecto de laberinto en Python creado por Alejandro Ortega Mendoza

Estructura:
- modelo/: clases del dominio y de los patrones.
- main.py: punto de entrada.

Ejecución:
    python main.py

Patrones usados:
- Composite: ElementoMapa, Contenedor, Habitacion, Laberinto.
- Decorator: Decorator, Bomba.
- Strategy: Agresivo, Perezoso.
- Abstract Factory + Singleton: AbstractFactory, ConcreteFactory, ConcreteFactoryBombas.
- Factory Method: métodos fabricar_* en Juego/JuegoBombas.
- Builder + Director: Builder, ConcreteBuilder, Director.
- Iterator: Iterator, ConcreteIterator.
- Template Method: AbstractClass.TemplateMethod().
