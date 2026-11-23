"""TED-02: contagem de palavras com tabela hash (dict)."""
from pathlib import Path
import re
import sys
import unicodedata


def contar_frequencias(texto: str) -> dict[str, int]:
    """Normaliza palavras Unicode e contabiliza ocorrências em um dicionário."""
    palavras = re.findall(r"[^\W_]+(?:['’][^\W_]+)*", texto.casefold(), flags=re.UNICODE)
    frequencias: dict[str, int] = {}
    for palavra in palavras:
        frequencias[palavra] = frequencias.get(palavra, 0) + 1
    return frequencias


def chave_alfabetica(palavra: str) -> tuple[str, str]:
    """Ignora acentos ao ordenar, para que 'água' fique junto do 'a' e não depois do 'z'."""
    decomposta = unicodedata.normalize("NFD", palavra)
    sem_acento = "".join(letra for letra in decomposta if not unicodedata.combining(letra))
    return sem_acento, palavra


def cinco_mais_frequentes(frequencias: dict[str, int]) -> list[tuple[str, int]]:
    """Ordena por frequência decrescente; em caso de empate, por ordem alfabética."""
    return sorted(frequencias.items(), key=lambda item: (-item[1], chave_alfabetica(item[0])))[:5]


def exibir_resultados(frequencias: dict[str, int]) -> None:
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


def main() -> int:
    caminho = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "dados" / "texto_exemplo.txt"
    try:
        texto = caminho.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as erro:
        print(f"Erro ao ler o arquivo: {erro}", file=sys.stderr)
        return 1
    exibir_resultados(contar_frequencias(texto))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
