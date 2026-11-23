"""TED-02: grafo ponderado não direcionado e menor caminho com Dijkstra."""
import heapq
import math
import sys

# Cenário fictício: distâncias hipotéticas em quilômetros, não representam rodovias reais.
GRAFO: dict[str, dict[str, int]] = {
    "Aurora": {"Brisa": 4, "Cedro": 3},
    "Brisa": {"Aurora": 4, "Cedro": 1, "Duna": 5},
    "Cedro": {"Aurora": 3, "Brisa": 1, "Duna": 8, "Estrela": 10},
    "Duna": {"Brisa": 5, "Cedro": 8, "Estrela": 2, "Farol": 6},
    "Estrela": {"Cedro": 10, "Duna": 2, "Farol": 3, "Grove": 7},
    "Farol": {"Duna": 6, "Estrela": 3, "Grove": 2},
    "Grove": {"Estrela": 7, "Farol": 2},
}


def validar_grafo(grafo: dict[str, dict[str, int]]) -> None:
    for origem, vizinhos in grafo.items():
        for destino, peso in vizinhos.items():
            if destino not in grafo:
                raise ValueError(f"Nó desconhecido na conexão {origem} -> {destino}")
            if not isinstance(peso, (int, float)) or not math.isfinite(peso) or peso <= 0:
                raise ValueError(f"Peso inválido na conexão {origem} -> {destino}: {peso}")


def dijkstra(grafo: dict[str, dict[str, int]], origem: str, destino: str) -> tuple[list[str], float]:
    validar_grafo(grafo)
    if origem not in grafo or destino not in grafo:
        raise ValueError("Origem ou destino não existe no grafo.")
    distancias = {cidade: math.inf for cidade in grafo}
    anteriores: dict[str, str] = {}
    distancias[origem] = 0
    fila = [(0, origem)]
    while fila:
        distancia_atual, cidade = heapq.heappop(fila)
        if distancia_atual > distancias[cidade]:
            continue
        if cidade == destino:
            break
        for vizinho, peso in grafo[cidade].items():
            nova_distancia = distancia_atual + peso
            if nova_distancia < distancias[vizinho]:
                distancias[vizinho] = nova_distancia
                anteriores[vizinho] = cidade
                heapq.heappush(fila, (nova_distancia, vizinho))
    if math.isinf(distancias[destino]):
        return [], math.inf
    caminho = [destino]
    while caminho[-1] != origem:
        caminho.append(anteriores[caminho[-1]])
    caminho.reverse()
    return caminho, distancias[destino]


def main() -> int:
    print("=== PARTE 2: GRAFOS E DIJKSTRA ===")
    print("Cidades disponíveis:", ", ".join(sorted(GRAFO)))
    origem = sys.argv[1] if len(sys.argv) > 1 else "Aurora"
    destino = sys.argv[2] if len(sys.argv) > 2 else "Grove"
    try:
        caminho, distancia = dijkstra(GRAFO, origem, destino)
    except ValueError as erro:
        print(f"Erro: {erro}", file=sys.stderr)
        return 1
    print(f"Origem: {origem} | Destino: {destino}")
    if not caminho:
        print("Não existe caminho entre as cidades informadas.")
    else:
        print("Menor caminho:", " -> ".join(caminho))
        print(f"Distância total: {distancia:g} km")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
