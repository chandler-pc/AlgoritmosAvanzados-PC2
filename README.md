# Proyecto 7: Dinamización de Bentley-Saxe aplicada a Convex Hull 2D

## Resumen

Este proyecto implementa y analiza la técnica de **Bentley-Saxe** para dinamizar una estructura geométrica estática: la **envolvente convexa (Convex Hull) en 2D**. Permite realizar inserciones y eliminaciones eficientes de puntos, y compara el rendimiento contra el enfoque estático clásico (reconstrucción completa tras cada cambio).

---

## ¿Qué es la técnica de Bentley-Saxe?

La técnica de **Bentley-Saxe** permite transformar estructuras de datos eficientes solo en modo estático (batch) en **estructuras dinámicas**.  
Consiste en mantener varias subestructuras estáticas de tamaños crecientes exponenciales (S₀, S₁, S₂, ...). Las inserciones y eliminaciones disparan reconstrucciones o fusiones de estas subestructuras, permitiendo mantener operaciones dinámicas con buen rendimiento amortizado.

Esto es especialmente útil en estructuras como la **Convex Hull**, donde modificar incrementalmente el conjunto es costoso.

---

## Estructura del Proyecto

- `app/`
  - `convex_hull.py`: Convex Hull estático (Monotone Chain).
  - `dynamic_convex_hull.py`: Implementación dinámica (Bentley-Saxe).
  - `point.py`, `utils.py`: Utilidades para puntos y ayuda general.
- `tests/`: Pruebas automáticas.
- Otros scripts de visualización/benchmark.
- `requirements.txt`: Dependencias.

---

## Cómo ejecutar

### 1. Instalar dependencias

```sh
pip install -r requirements.txt
