# Red de ciudades en Python (Unidad 3: Grafos)

Deber de desarrollo de Algoritmos y Estructuras de Datos (Ciencia de Datos, Universidad Politécnica Salesiana). Autor: José Efraín Minango Morales.

Programa de consola que modela una red de siete ciudades del Ecuador conectadas por carreteras y responde preguntas sobre ella con los algoritmos de la Unidad 3: lista de adyacencia, BFS y Dijkstra. Solo usa diccionarios, listas y módulos de la librería estándar (`collections` y `heapq`).

## Cómo ejecutarlo

Necesita Python 3 y no instala nada extra. Desde la carpeta del repositorio:

```
python main.py
```

En macOS o Linux, si el comando `python` no existe, se usa `python3 main.py`.

La red ya viene cargada, así que todas las opciones del menú se pueden probar sin escribir datos. Para correr solo los casos de prueba:

```
python utilidades.py
```

También están en el menú, opción 6.

## Archivos

| Archivo | Qué contiene |
|---|---|
| `main.py` | Menú de consola y la red de ejemplo |
| `utilidades.py` | Las funciones de cada requerimiento y los casos de prueba |

## La red

Siete ciudades y nueve carreteras de doble sentido. Los kilómetros salen de la ruta que Google Maps recomienda en auto entre cada par de ciudades (consultado el 15/11/2026), redondeados al kilómetro, y pueden variar un poco según la ruta y el tráfico. Cada arista es el tramo completo por carretera, aunque pase por pueblos que no están en la red.

| Tramo | km |
|---|---|
| Quito – Ambato | 157 |
| Ambato – Riobamba | 56 |
| Riobamba – Guayaquil | 230 |
| Riobamba – Cuenca | 259 |
| Quito – Guayaquil | 428 |
| Guayaquil – Cuenca | 197 |
| Guayaquil – Machala | 184 |
| Cuenca – Loja | 211 |
| Machala – Loja | 238 |

## Qué hace cada requerimiento

**R1: Modelado del grafo.** La red es un diccionario donde la clave es la ciudad y el valor es una lista de tuplas `(ciudad_vecina, km)`. Como las carreteras son de doble sentido, cada una se guarda en las dos ciudades. La opción 1 del menú muestra la red y el grado de cada ciudad, que es con cuántas ciudades conecta directamente.

**R2: Recorrido BFS.** Desde una ciudad de origen recorre la red por niveles con una cola y un diccionario de escalas. Lista las ciudades alcanzables con su número de tramos desde el origen y avisa si la red está completamente conectada o si alguna ciudad queda aislada. La opción 5 del menú agrega Galápagos sin carreteras para ver ese aviso en acción.

**R3: Ruta más barata con Dijkstra.** La función `dijkstra` la entregó el docente en el enunciado y está copiada sin cambios. El programa la integra, muestra la distancia mínima en km hasta cada ciudad y señala la más cercana y la más lejana. Las ciudades inalcanzables salen como `inalcanzable` y no cuentan para esas dos.

**R4: Comparación.** Compara la ruta con menos escalas (BFS) y la de menos kilómetros (Dijkstra) entre dos ciudades. Con Quito y Cuenca las rutas son distintas:

- BFS: Quito → Guayaquil → Cuenca, 2 tramos y 625 km.
- Dijkstra: Quito → Ambato → Riobamba → Cuenca, 3 tramos y 472 km.

El BFS solo cuenta tramos y trata igual a todas las carreteras, así que se queda con el atajo por Guayaquil, que usa la carretera más larga de la red (428 km). Dijkstra suma km y prefiere tres tramos cortos. Como la función provista no devuelve los padres, la ruta de Dijkstra se reconstruye caminando hacia atrás desde el destino, buscando en cada paso la vecina cuya distancia más el peso de la carretera da la distancia de la ciudad actual.

## Complejidad de las operaciones

V es el número de ciudades y E el de carreteras.

| Req. | Función | Tiempo | Justificación |
|---|---|---|---|
| R1 | `construir_red` | O(V + E) | Se recorre cada carretera una vez. |
| R1 | `grados` | O(V) | El grado es el largo de la lista de cada ciudad. |
| R2 | `bfs_escalas` | O(V + E) | Cada ciudad entra una vez a la cola y cada carretera se mira dos veces. |
| R3 | `dijkstra` | O((V + E) log V) | Hasta V + E operaciones sobre el heap, cada una de O(log V). |
| R4 | `comparar_rutas` | O((V + E) log V) | Manda Dijkstra; las rutas se rearman en O(V + E). |

El factor logarítmico de Dijkstra viene del heap: cada `heappush` y cada `heappop` cuestan O(log V). El espacio usado es O(V + E) por la lista de adyacencia.

## Pruebas

`prueba_utilidades()` usa `assert` y cubre una red chica que se verifica a mano (donde el BFS y Dijkstra dan rutas distintas), una sola ciudad sin carreteras, una ciudad aislada, origen igual a destino y un empate entre dos rutas de los mismos km.

## Limitaciones

- Los datos viven en memoria y se pierden al cerrar el programa.
- Las distancias son aproximadas y de un día concreto; si cambia la ruta recomendada, cambian los km.
- El BFS y Dijkstra devuelven una sola ruta aunque haya empates.

## Bibliografía

Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to Algorithms* (4.ª ed.). MIT Press.

Google. (2026). *Google Maps* [Aplicación web]. https://www.google.com/maps

Sedgewick, R., & Wayne, K. (2011). *Algorithms* (4.ª ed.). Addison-Wesley Professional.
