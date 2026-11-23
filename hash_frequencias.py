"""TED-02: contagem de palavras com tabela hash (dict)."""
from pathlib import Path
import re
import sys
import unicodedata


def contar_frequencias(texto: str) -> dict[str, int]:
    """Normaliza palavras Unicode e contabiliza ocorrências em um dicionário."""
    # casefold() iguala maiúsculas e minúsculas; a expressão regular captura só letras e
    # números (aceitando apóstrofo no meio), o que descarta a pontuação.
    palavras = re.findall(r"[^\W_]+(?:['’][^\W_]+)*", texto.casefold(), flags=re.UNICODE)

    # Tabela hash: a palavra é a chave e a contagem é o valor.
    frequencias: dict[str, int] = {}
    for palavra in palavras:
        # get() devolve 0 na primeira ocorrência. Buscar e atualizar custam O(1) em média,
        # portanto contar n palavras custa O(n) em média.
        frequencias[palavra] = frequencias.get(palavra, 0) + 1
    return frequencias


def chave_alfabetica(palavra: str) -> tuple[str, str]:
    """Ignora acentos ao ordenar, para que 'água' fique junto do 'a' e não depois do 'z'."""
    # NFD separa a letra do acento ("á" vira "a" + acento); depois o acento é descartado.
    decomposta = unicodedata.normalize("NFD", palavra)
    sem_acento = "".join(letra for letra in decomposta if not unicodedata.combining(letra))
    return sem_acento, palavra


def cinco_mais_frequentes(frequencias: dict[str, int]) -> list[tuple[str, int]]:
    """Ordena por frequência decrescente; em caso de empate, por ordem alfabética."""
    # O sinal negativo coloca as maiores contagens primeiro.
    return sorted(frequencias.items(), key=lambda item: (-item[1], chave_alfabetica(item[0])))[:5]


def exibir_resultados(frequencias: dict[str, int]) -> None:
    """Mostra o total, todas as frequências e o ranking."""
    total = sum(frequencias.values())
    print("=== PARTE 1: TABELA HASH ===")
    print(f"Total de palavras: {total} | Palavras distintas: {len(frequencias)}")
    print("\nFrequências (ordem alfabética):")
    for palavra, quantidade in sorted(frequencias.items(), key=lambda item: chave_alfabetica(item[0])):
        print(f"  {palavra:<20} {quantidade}")
    print("\nCinco palavras mais frequentes:")
    for posicao, (palavra, quantidade) in enumerate(cinco_mais_frequentes(frequencias), 1):
        print(f"  {posicao}. {palavra}: {quantidade}")
    if not frequencias:
        print("  Nenhuma palavra encontrada.")


def obter_texto(argumentos: list[str]) -> str:
    """Obtém o texto de: --texto "frase", um arquivo informado ou o arquivo de exemplo."""
    if argumentos and argumentos[0] == "--texto":
        if len(argumentos) < 2:
            raise ValueError('Informe a frase depois de --texto. Exemplo: --texto "dados grafo dados"')
        return " ".join(argumentos[1:])
    if argumentos:
        caminho = Path(argumentos[0])
    else:
        caminho = Path(__file__).parent / "dados" / "texto_exemplo.txt"
    return caminho.read_text(encoding="utf-8")


def main() -> int:
    try:
        texto = obter_texto(sys.argv[1:])
    except (OSError, UnicodeError) as erro:
        print(f"Erro ao ler o arquivo: {erro}", file=sys.stderr)
        return 1
    except ValueError as erro:
        print(f"Erro: {erro}", file=sys.stderr)
        return 1
    exibir_resultados(contar_frequencias(texto))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
