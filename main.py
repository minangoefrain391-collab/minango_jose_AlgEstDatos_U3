# main.py
# Unidad 3 - Grafos: red de ciudades del Ecuador (modelado, BFS y Dijkstra).
# Autor: José Efraín Minango Morales

from utilidades import (
    construir_red, grados, bfs_escalas, ciudades_aisladas, ruta_bfs,
    dijkstra, ciudad_mas_lejana_y_cercana, comparar_rutas, prueba_utilidades,
)

# Red de ejemplo: ciudad_a, ciudad_b, distancia por carretera en km.
# Los km los tomé de la ruta recomendada por Google Maps en auto (consultado el
# 15/11/2026) y los redondeé al km. Pueden variar un poco según la ruta y el tráfico.
CARRETERAS = [
    ("Quito", "Ambato", 157),
    ("Ambato", "Riobamba", 56),
    ("Riobamba", "Guayaquil", 230),
    ("Riobamba", "Cuenca", 259),
    ("Quito", "Guayaquil", 428),
    ("Guayaquil", "Cuenca", 197),
    ("Guayaquil", "Machala", 184),
    ("Cuenca", "Loja", 211),
    ("Machala", "Loja", 238),
]

# Par de ciudades que uso para el R4 (en esta red las dos rutas son distintas)
R4_ORIGEN = "Quito"
R4_DESTINO = "Cuenca"


def pedir_ciudad(grafo, mensaje, permitir_vacio=False):
    """Pide una ciudad por consola sin importar mayúsculas. Devuelve None si no existe
    (o "" si se permite dejarla vacía y el usuario no escribió nada)."""
    por_minuscula = {c.lower(): c for c in grafo}
    texto = input(mensaje).strip().lower()
    if permitir_vacio and texto == "":
        return ""
    if texto not in por_minuscula:
        print("Esa ciudad no está en la red. Opciones:", ", ".join(grafo))
        return None
    return por_minuscula[texto]


def mostrar_red(grafo):
    """R1: lista de adyacencia y grado de cada ciudad."""
    grado = grados(grafo)
    print("\nRed de ciudades (km por carretera):")
    for ciudad, vecinas in grafo.items():
        texto = ", ".join(f"{v} ({km} km)" for v, km in vecinas)
        print(f"  {ciudad} [grado {grado[ciudad]}]: {texto if texto else 'sin carreteras'}")


def mostrar_bfs(grafo, origen):
    """R2: ciudades alcanzables con sus escalas y chequeo de conectividad."""
    escalas, _ = bfs_escalas(grafo, origen)
    print(f"\nBFS desde {origen}:")
    for ciudad, esc in escalas.items():
        print(f"  {ciudad}: {esc} escala(s)")
    aisladas = ciudades_aisladas(grafo, escalas)
    if aisladas:
        print("La red NO está completamente conectada. Sin alcanzar:", ", ".join(aisladas))
    else:
        print("La red está completamente conectada: se llega a todas las ciudades.")


def mostrar_dijkstra(grafo, origen):
    """R3: distancia mínima en km hasta cada ciudad, más lejana y más cercana."""
    distancias = dijkstra(grafo, origen)
    print(f"\nDijkstra desde {origen} (km mínimos):")
    for ciudad, km in distancias.items():
        print(f"  {ciudad}: {km if km != float('inf') else 'inalcanzable'}")
    cercana, lejana = ciudad_mas_lejana_y_cercana(distancias, origen)
    if cercana is None:
        print("Desde esa ciudad no se llega a ninguna otra.")
    else:
        print(f"Más cercana: {cercana[0]} ({cercana[1]} km)")
        print(f"Más lejana: {lejana[0]} ({lejana[1]} km)")


def mostrar_comparacion(grafo, origen, destino):
    """R4: ruta con menos escalas (BFS) frente a ruta con menos km (Dijkstra)."""
    r = comparar_rutas(grafo, origen, destino)
    print(f"\nComparación {origen} -> {destino}:")
    print(f"  Menos escalas (BFS): {' -> '.join(r['ruta_escalas'])}"
          f" | {len(r['ruta_escalas']) - 1} tramos, {r['km_escalas']} km")
    print(f"  Menos km (Dijkstra): {' -> '.join(r['ruta_km'])}"
          f" | {len(r['ruta_km']) - 1} tramos, {r['km_minimos']} km")
    if r["coinciden"]:
        print("  Las dos rutas coinciden.")
    else:
        print("  Las rutas son distintas: BFS cuenta tramos y Dijkstra suma km.")


def red_con_ciudad_aislada(grafo):
    """Copia de la red con Galápagos sin carreteras, para ver cómo reacciona el BFS."""
    copia = {c: list(v) for c, v in grafo.items()}
    copia["Galapagos"] = []
    return copia


def menu():
    grafo = construir_red(CARRETERAS)
    while True:
        print("\n=== Red de ciudades - Unidad 3 ===")
        print("1. Mostrar la red y el grado de cada ciudad (R1)")
        print("2. Recorrido BFS desde una ciudad (R2)")
        print("3. Distancias mínimas con Dijkstra (R3)")
        print("4. Comparar rutas entre dos ciudades (R4)")
        print("5. Probar con una ciudad aislada (Galápagos)")
        print("6. Correr las pruebas")
        print("0. Salir")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            mostrar_red(grafo)
        elif opcion == "2":
            origen = pedir_ciudad(grafo, "Ciudad de origen: ")
            if origen:
                mostrar_bfs(grafo, origen)
        elif opcion == "3":
            origen = pedir_ciudad(grafo, "Ciudad de origen: ")
            if origen:
                mostrar_dijkstra(grafo, origen)
        elif opcion == "4":
            origen = pedir_ciudad(grafo, "Origen (vacío para el ejemplo): ", permitir_vacio=True)
            if origen == "":
                mostrar_comparacion(grafo, R4_ORIGEN, R4_DESTINO)
            elif origen:
                destino = pedir_ciudad(grafo, "Destino: ")
                if destino:
                    mostrar_comparacion(grafo, origen, destino)
        elif opcion == "5":
            con_isla = red_con_ciudad_aislada(grafo)
            mostrar_bfs(con_isla, "Quito")
            mostrar_dijkstra(con_isla, "Quito")
        elif opcion == "6":
            prueba_utilidades()
        elif opcion == "0":
            print("Hasta luego.")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    menu()
