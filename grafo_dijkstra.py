"""TED-02: grafo ponderado não direcionado e menor caminho com Dijkstra."""
import heapq
import math
import sys

# Cenário fictício: distâncias hipotéticas em quilômetros, não representam rodovias reais.
CIDADES: list[str] = ["Aurora", "Brisa", "Cedro", "Duna", "Estrela", "Farol", "Grove"]

# Cada estrada aparece UMA vez: (cidade A, cidade B, distância).
# construir_grafo() cria a ida e a volta. Para incluir uma conexão, basta somar uma linha aqui.
CONEXOES: list[tuple[str, str, float]] = [
    ("Aurora", "Brisa", 4),
    ("Aurora", "Cedro", 3),
    ("Brisa", "Cedro", 1),
    ("Brisa", "Duna", 5),
    ("Cedro", "Duna", 8),
    ("Cedro", "Estrela", 10),
    ("Duna", "Estrela", 2),
    ("Duna", "Farol", 6),
    ("Estrela", "Farol", 3),
    ("Estrela", "Grove", 7),
    ("Farol", "Grove", 2),
]

# Lista de adjacência: cada cidade guarda os seus vizinhos e a distância até eles.
Grafo = dict[str, dict[str, float]]


def construir_grafo(cidades: list[str], conexoes: list[tuple[str, str, float]]) -> Grafo:
    """Monta a lista de adjacência, registrando cada conexão nos dois sentidos."""
    # Toda cidade começa sem vizinhos; assim, cidades isoladas também ficam no grafo.
    grafo: Grafo = {cidade: {} for cidade in cidades}
    for cidade_a, cidade_b, distancia in conexoes:
        for cidade in (cidade_a, cidade_b):
            if cidade not in grafo:
                raise ValueError(f"A cidade '{cidade}' está em CONEXOES, mas não está em CIDADES.")
        if cidade_a == cidade_b:
            raise ValueError(f"A cidade '{cidade_a}' não pode se conectar a ela mesma.")
        if cidade_b in grafo[cidade_a]:
            raise ValueError(f"Conexão repetida entre '{cidade_a}' e '{cidade_b}'.")
        grafo[cidade_a][cidade_b] = distancia
        grafo[cidade_b][cidade_a] = distancia
    validar_grafo(grafo)
    return grafo


def validar_grafo(grafo: Grafo) -> None:
    """Garante que todo vizinho existe e que todo peso é um número positivo."""
    for origem, vizinhos in grafo.items():
        for destino, peso in vizinhos.items():
            if destino not in grafo:
                raise ValueError(f"Nó desconhecido na conexão {origem} -> {destino}")
            # Dijkstra trata como definitiva a distância de uma cidade já visitada;
            # um peso negativo poderia melhorar essa distância depois e daria resultado errado.
            if not isinstance(peso, (int, float)) or not math.isfinite(peso) or peso <= 0:
                raise ValueError(f"Peso inválido na conexão {origem} -> {destino}: {peso}")


def localizar_cidade(grafo: Grafo, nome: str) -> str:
    """Encontra a cidade sem diferenciar maiúsculas de minúsculas."""
    for cidade in grafo:
        if cidade.casefold() == nome.strip().casefold():
            return cidade
    raise ValueError(f"A cidade '{nome}' não existe no grafo.")


def dijkstra(grafo: Grafo, origem: str, destino: str) -> tuple[list[str], float]:
    """Retorna o menor caminho e a distância total; sem caminho, retorna ([], infinito)."""
    validar_grafo(grafo)
    if origem not in grafo or destino not in grafo:
        raise ValueError("Origem ou destino não existe no grafo.")

    # 1. No início só se conhece a distância da origem (zero); as demais são infinitas.
    distancias = {cidade: math.inf for cidade in grafo}
    distancias[origem] = 0
    anteriores: dict[str, str] = {}  # de qual cidade se chegou a cada cidade

    # 2. A fila de prioridade (heap) sempre entrega a cidade com a menor distância.
    fila: list[tuple[float, str]] = [(0, origem)]
    while fila:
        distancia_atual, cidade = heapq.heappop(fila)
        # Registro antigo: já foi encontrado um caminho menor até esta cidade.
        if distancia_atual > distancias[cidade]:
            continue
        # Ao sair da fila, a distância do destino é definitiva e a busca pode parar.
        if cidade == destino:
            break

        # 3. Relaxamento: verifica se passar por esta cidade encurta o caminho dos vizinhos.
        for vizinho, peso in grafo[cidade].items():
            nova_distancia = distancia_atual + peso
            # Com "<", um empate mantém o primeiro caminho encontrado.
            if nova_distancia < distancias[vizinho]:
                distancias[vizinho] = nova_distancia
                anteriores[vizinho] = cidade
                heapq.heappush(fila, (nova_distancia, vizinho))

    # 4. Distância ainda infinita significa que não há caminho até o destino.
    if math.isinf(distancias[destino]):
        return [], math.inf

    # 5. Reconstrói a rota do destino até a origem e inverte a ordem.
    caminho = [destino]
    while caminho[-1] != origem:
        caminho.append(anteriores[caminho[-1]])
    caminho.reverse()
    return caminho, distancias[destino]


def main() -> int:
    print("=== PARTE 2: GRAFOS E DIJKSTRA ===")
    nome_origem = sys.argv[1] if len(sys.argv) > 1 else "Aurora"
    nome_destino = sys.argv[2] if len(sys.argv) > 2 else "Grove"
    try:
        grafo = construir_grafo(CIDADES, CONEXOES)
        print("Cidades disponíveis:", ", ".join(sorted(grafo)), flush=True)
        origem = localizar_cidade(grafo, nome_origem)
        destino = localizar_cidade(grafo, nome_destino)
        caminho, distancia = dijkstra(grafo, origem, destino)
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
