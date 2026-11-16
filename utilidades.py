# utilidades.py
# Funciones de cada requerimiento de la Unidad 3 (red de ciudades).
# n = V es la cantidad de ciudades y E la cantidad de carreteras.

import heapq
from collections import deque


# ---------------------------------------------------------------
# R1: modelado del grafo (lista de adyacencia)
# ---------------------------------------------------------------

def agregar_carretera(grafo, ciudad_a, ciudad_b, km):
    """Agrega una carretera de doble sentido entre dos ciudades."""
    # O(1) por carretera (dos append)
    grafo.setdefault(ciudad_a, [])
    grafo.setdefault(ciudad_b, [])
    grafo[ciudad_a].append((ciudad_b, km))
    grafo[ciudad_b].append((ciudad_a, km))


def construir_red(carreteras):
    """Arma el grafo a partir de una lista de tuplas (ciudad_a, ciudad_b, km)."""
    # O(V + E): se recorre cada carretera una vez
    grafo = {}
    for ciudad_a, ciudad_b, km in carreteras:
        agregar_carretera(grafo, ciudad_a, ciudad_b, km)
    return grafo


def grados(grafo):
    """Devuelve {ciudad: grado}, o sea con cuántas ciudades conecta directamente."""
    # O(V): el grado es el largo de la lista de vecinas
    return {ciudad: len(vecinas) for ciudad, vecinas in grafo.items()}


# ---------------------------------------------------------------
# R2: recorrido BFS
# ---------------------------------------------------------------

def bfs_escalas(grafo, origen):
    """BFS desde el origen. Devuelve (escalas, padre).
    escalas = {ciudad: número de tramos desde el origen}
    padre   = {ciudad: ciudad desde la que se descubrió} (sirve para armar la ruta)
    """
    # BFS: O(V + E)
    escalas = {origen: 0}
    padre = {origen: None}
    cola = deque([origen])
    while cola:
        actual = cola.popleft()
        for vecina, _ in grafo[actual]:      # el peso no importa en BFS
            if vecina not in escalas:
                escalas[vecina] = escalas[actual] + 1
                padre[vecina] = actual
                cola.append(vecina)
    return escalas, padre


def ciudades_aisladas(grafo, escalas):
    """Ciudades que el BFS no alcanzó desde el origen."""
    # O(V)
    return [c for c in grafo if c not in escalas]


def ruta_bfs(padre, destino):
    """Reconstruye la ruta de menos escalas caminando hacia atrás por los padres."""
    # O(V) en el peor caso
    if destino not in padre:
        return []
    ruta = []
    actual = destino
    while actual is not None:
        ruta.append(actual)
        actual = padre[actual]
    return ruta[::-1]


# ---------------------------------------------------------------
# R3: Dijkstra
# ---------------------------------------------------------------

# Función entregada por el docente en el enunciado de la Tarea Unidad 3.
# La copié tal cual, sin modificarla.
# Dijkstra: O((V + E) log V). El log V sale del heap: cada heappush y
# heappop cuesta O(log V) y se hacen a lo sumo V + E de ellos.
def dijkstra(grafo, origen):
    """Devuelve {ciudad: distancia_minima_desde_origen}."""
    dist = {ciudad: float('inf') for ciudad in grafo}
    dist[origen] = 0
    heap = [(0, origen)]          # cola de prioridad
    while heap:
        d, u = heapq.heappop(heap)      # el mas cercano pendiente
        if d > dist[u]:
            continue                    # ya teniamos una ruta mejor
        for vecino, peso in grafo[u]:
            if dist[u] + peso < dist[vecino]:    # relajacion
                dist[vecino] = dist[u] + peso
                heapq.heappush(heap, (dist[vecino], vecino))
    return dist


def ciudad_mas_lejana_y_cercana(distancias, origen):
    """Entre las ciudades alcanzables (sin contar el origen) devuelve
    (mas_cercana, mas_lejana), cada una como (ciudad, km). Si no hay ninguna, (None, None)."""
    # O(V)
    alcanzables = {c: d for c, d in distancias.items()
                   if c != origen and d != float('inf')}
    if not alcanzables:
        return None, None
    cercana = min(alcanzables, key=alcanzables.get)
    lejana = max(alcanzables, key=alcanzables.get)
    return (cercana, alcanzables[cercana]), (lejana, alcanzables[lejana])


# ---------------------------------------------------------------
# R4: comparación BFS vs Dijkstra
# ---------------------------------------------------------------

def ruta_dijkstra(grafo, distancias, origen, destino):
    """Reconstruye la ruta de menor distancia usando solo el diccionario de
    distancias (la función dijkstra provista no devuelve padres y no quise tocarla).
    Se parte del destino y en cada paso se busca la vecina que explica su distancia."""
    # O(V + E) en el peor caso: cada ciudad de la ruta revisa sus vecinas una vez
    if distancias.get(destino, float('inf')) == float('inf'):
        return []
    ruta = [destino]
    actual = destino
    while actual != origen:
        for vecina, peso in grafo[actual]:
            if distancias[vecina] + peso == distancias[actual]:
                actual = vecina
                break
        ruta.append(actual)
    return ruta[::-1]


def km_de_ruta(grafo, ruta):
    """Suma los km de una ruta (lista de ciudades)."""
    # O(L * grado) con L = largo de la ruta; en la práctica es muy pequeño
    total = 0
    for a, b in zip(ruta, ruta[1:]):
        for vecina, peso in grafo[a]:
            if vecina == b:
                total += peso
                break
    return total


def comparar_rutas(grafo, origen, destino):
    """Devuelve un diccionario con la ruta de menos escalas (BFS) y la de menos km (Dijkstra)."""
    escalas, padre = bfs_escalas(grafo, origen)
    ruta_a = ruta_bfs(padre, destino)
    distancias = dijkstra(grafo, origen)
    ruta_b = ruta_dijkstra(grafo, distancias, origen, destino)
    return {
        "ruta_escalas": ruta_a,
        "km_escalas": km_de_ruta(grafo, ruta_a),
        "ruta_km": ruta_b,
        "km_minimos": distancias[destino],
        "coinciden": ruta_a == ruta_b,
    }


# ---------------------------------------------------------------
# Pruebas
# ---------------------------------------------------------------

def prueba_utilidades():
    """Casos de prueba con assert, incluyendo casos límite."""

    # red chica y conocida para poder verificar a mano
    #   A -2- B -2- C   y además A -10- C directo
    chica = construir_red([("A", "B", 2), ("B", "C", 2), ("A", "C", 10)])
    assert grados(chica) == {"A": 2, "B": 2, "C": 2}

    # R2: BFS cuenta tramos, el camino directo A-C tiene 1 solo
    escalas, padre = bfs_escalas(chica, "A")
    assert escalas == {"A": 0, "B": 1, "C": 1}
    assert ruta_bfs(padre, "C") == ["A", "C"]
    assert ciudades_aisladas(chica, escalas) == []

    # R3: Dijkstra suma km, A-B-C (4 km) le gana al directo (10 km)
    dist = dijkstra(chica, "A")
    assert dist == {"A": 0, "B": 2, "C": 4}
    assert ruta_dijkstra(chica, dist, "A", "C") == ["A", "B", "C"]

    # R4: las dos rutas NO coinciden en esta red
    r = comparar_rutas(chica, "A", "C")
    assert r["ruta_escalas"] == ["A", "C"] and r["km_escalas"] == 10
    assert r["ruta_km"] == ["A", "B", "C"] and r["km_minimos"] == 4
    assert r["coinciden"] is False

    # caso límite: una sola ciudad sin carreteras
    sola = {"X": []}
    assert grados(sola) == {"X": 0}
    escalas, padre = bfs_escalas(sola, "X")
    assert escalas == {"X": 0}
    assert dijkstra(sola, "X") == {"X": 0}
    assert ciudad_mas_lejana_y_cercana(dijkstra(sola, "X"), "X") == (None, None)

    # caso límite: ciudad aislada (no alcanzable)
    con_isla = construir_red([("A", "B", 5)])
    con_isla["Isla"] = []
    escalas, padre = bfs_escalas(con_isla, "A")
    assert ciudades_aisladas(con_isla, escalas) == ["Isla"]
    dist = dijkstra(con_isla, "A")
    assert dist["Isla"] == float("inf")
    assert ruta_bfs(padre, "Isla") == []
    assert ruta_dijkstra(con_isla, dist, "A", "Isla") == []
    cerca, lejos = ciudad_mas_lejana_y_cercana(dist, "A")
    assert cerca == ("B", 5) and lejos == ("B", 5)   # la isla no cuenta

    # caso límite: origen igual a destino
    assert ruta_bfs(bfs_escalas(chica, "B")[1], "B") == ["B"]
    assert ruta_dijkstra(chica, dijkstra(chica, "B"), "B", "B") == ["B"]

    # caso límite: dos rutas con los mismos km y mismas escalas (empate)
    cuadro = construir_red([("A", "B", 1), ("A", "C", 1), ("B", "D", 1), ("C", "D", 1)])
    dist = dijkstra(cuadro, "A")
    assert dist["D"] == 2
    assert ruta_dijkstra(cuadro, dist, "A", "D")[0] == "A"
    assert km_de_ruta(cuadro, ruta_dijkstra(cuadro, dist, "A", "D")) == 2

    print("Todas las pruebas pasaron.")


if __name__ == "__main__":
    prueba_utilidades()
