# Proyecto 7: Dinamización de Bentley–Saxe aplicada a Convex Hull 2D

## Descripción y Motivación Teórica

Este proyecto aborda la dinamización de la envolvente convexa (Convex Hull) en 2D mediante la técnica de Bentley–Saxe, una estrategia diseñada para convertir estructuras estáticas eficientes en estructuras dinámicas.

### ¿Por qué dinamizar?

Las estructuras geométricas como la envolvente convexa suelen construirse de forma estática (batch). Sin embargo, cuando el conjunto de puntos cambia frecuentemente (inserciones/eliminaciones), reconstruir desde cero se vuelve ineficiente. Bentley–Saxe permite mantener eficiencia amortizada con una estructura jerárquica de subestructuras estáticas.

### Fundamento de Bentley–Saxe

- Se mantienen subestructuras S₀, S₁, S₂, ... que contienen 2^i elementos o están vacías.
- Las inserciones provocan fusiones binarias hasta encontrar una posición vacía, similar a un heap binario.
- Las eliminaciones invalidan puntos y disparan reconstrucciones perezosas.
- Las consultas se resuelven combinando los resultados de las subestructuras activas.

## Estructura del Proyecto

```
AlgoritmosAvanzados-PC2/
│
├── app/
│   ├── convex_hull.py          # Implementación estática con Monotone Chain
│   ├── dynamic_convex_hull.py  # Dinamización con Bentley–Saxe
│   ├── point.py                # Clase Point con comparaciones y orientación
│   ├── utils.py                # Funciones auxiliares para geometría
│   └── config.py               # Parámetros globales del sistema
│
├── tests/
│   ├── test_convex_hull.py     # Pruebas unitarias para Convex Hull estático
│   └── test_dynamic_convex_hull.py # Pruebas para estructura dinámica
│
├── main.py                     # Script de ejemplo/visualización
├── benchmark_convex_hull.ipynb                     # Benchmark, profiling/
└── requirements.txt            # Dependencias del entorno
```

## Instrucciones de Instalación y Ejecución

### 1. Preparación del entorno

```bash
git clone <repositorio>
cd AlgoritmosAvanzados-PC2
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Ejecutar pruebas

```bash
python -m unittest discover -s tests
```

### 3. Ejecutar el script principal

```bash
python main.py
```

### 3. Profiling, gráficas y performance

Ejecutar el archivo llamado `benchmark_convex_hull.ipynb`

## Documentación de la API

### Clase Point

```python
Point(x: float, y: float)
```

Representa un punto en el plano. Métodos importantes:

- `__eq__, __lt__`: Comparación lexicográfica.
- `cross(p1, p2, p3)`: Producto cruzado de tres puntos.

### Clase ConvexHull

```python
ConvexHull()
```

Implementación estática mediante el algoritmo de Monotone Chain.

Métodos públicos:
- `insert(Point)`: Agrega un punto a la lista.
- `calculate()`: Calcula la envolvente convexa.
- `get_hull()`: Devuelve los puntos en la envolvente convexa.

Manejo de errores:
- Si hay menos de tres puntos, se devuelve la lista sin modificación.

### Clase DynamicConvexHull

```python
DynamicConvexHull()
```

Implementa la técnica de Bentley–Saxe para mantener múltiples subestructuras.

Métodos:
- `insert(p: Point)`: Inserta un nuevo punto.
- `delete(p: Point)`: Elimina un punto (lazy deletion).
- `is_inside(p: Point) -> bool`: Verifica si un punto pertenece a la envolvente convexa.

Manejo de errores:
- Eliminar puntos no existentes no lanza excepciones.

### utils.py

Contiene funciones auxiliares:
- `is_point_in_polygon(point, polygon)`: Verifica inclusión mediante orientación.
- `remove_duplicates(points)`: Elimina puntos duplicados.
- `sort_points(points)`: Ordena los puntos lexicográficamente.

## Diseño de la API

La interfaz pública se limita a los métodos insert, delete e is_inside para la clase DynamicConvexHull. El diseño oculta detalles internos como las subestructuras individuales, y promueve la encapsulación. Todos los métodos relevantes incluyen documentación en formato docstring.

### Estructuras de datos implementadas


#### `class ConvexHull`

```plaintext
class ConvexHull {
    append_point(x: float, y: float) -> None
        // Agrega un nuevo punto al conjunto. Lanza ValueError si las coordenadas no son numéricas.

    calculate_monotone_chain() -> List[Point]
        // Calcula la envolvente convexa con el algoritmo Monotone Chain.
        // Si hay errores en la comparación de puntos o producto cruzado, se manejan y se retorna una copia de los puntos originales.

    remove_point(point: Point) -> bool
        // Elimina un punto si está presente. Retorna False si no existe o si ocurre un error inesperado.

    is_inside_convex_hull(point: Point) -> bool
        // Verifica si un punto se encuentra dentro de la envolvente convexa.
        // Devuelve False ante errores de cálculo interno o si la envolvente es inválida.

    get_hull() -> List[Point]
        // Retorna la envolvente convexa. Calcula si es necesario.
        // Devuelve el estado actual incluso si ocurre una excepción durante el cálculo.

    clear() -> None
        // Elimina todos los puntos y reinicia el estado.

    __str__() -> str
        // Representación textual de la envolvente. Si ocurre un error, lo incluye en el string.
}
```

#### `class DynamicConvexHull`

```plaintext
class DynamicConvexHull {
    insert(point: Point) -> None
        // Inserta un punto y actualiza subestructuras mediante fusiones.
        // Si ocurre un error al crear o combinar estructuras, el punto se omite silenciosamente.

    delete(point: Point) -> bool
        // Marca un punto como eliminado. Si supera el 50% de eliminaciones en una subestructura, esta se reconstruye.
        // Si el punto no se encuentra, retorna False. Si hay errores durante la reconstrucción, se recupera con copia directa de los puntos.

    get_hull() -> List[Point]
        // Retorna la envolvente convexa global. Si está desactualizada, la recalcula.
        // Si ocurre un error en la combinación, retorna todos los puntos válidos sin garantía de convexidad.

    is_inside(point: Point) -> bool
        // Verifica si el punto está dentro de la envolvente global.
        // Si ocurre un error en la verificación, retorna False.
}
```
