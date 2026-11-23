"""Testes automatizados, sem dependências externas."""
import math
import sys
import unittest
from pathlib import Path

# Permite executar este arquivo de qualquer pasta, sem depender do diretório atual.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from hash_frequencias import chave_alfabetica, cinco_mais_frequentes, contar_frequencias
from grafo_dijkstra import GRAFO, dijkstra


class TesteHash(unittest.TestCase):
    def test_exemplo_enunciado(self):
        self.assertEqual(contar_frequencias("dados estrutura dados grafo estrutura dados"),
                         {"dados": 3, "estrutura": 2, "grafo": 1})

    def test_normalizacao(self):
        self.assertEqual(contar_frequencias("Olá, OLÁ! Python; python."), {"olá": 2, "python": 2})

    def test_texto_vazio(self):
        self.assertEqual(contar_frequencias("!!!"), {})

    def test_ordem_alfabetica_com_acentos(self):
        self.assertEqual(sorted(["zero", "água", "ainda", "único", "a"], key=chave_alfabetica),
                         ["a", "água", "ainda", "único", "zero"])

    def test_ranking_com_empate(self):
        self.assertEqual(cinco_mais_frequentes(contar_frequencias("zebra é é bola água zebra dado faca")),
                         [("é", 2), ("zebra", 2), ("água", 1), ("bola", 1), ("dado", 1)])


class TesteDijkstra(unittest.TestCase):
    def test_rota_principal(self):
        self.assertEqual(dijkstra(GRAFO, "Aurora", "Grove"),
                         (["Aurora", "Brisa", "Duna", "Estrela", "Farol", "Grove"], 16))

    def test_mesma_cidade(self):
        self.assertEqual(dijkstra(GRAFO, "Aurora", "Aurora"), (["Aurora"], 0))

    def test_sem_caminho(self):
        grafo = {"A": {"B": 2}, "B": {"A": 2}, "C": {}}
        self.assertEqual(dijkstra(grafo, "A", "C"), ([], math.inf))

    def test_cidade_inexistente(self):
        with self.assertRaises(ValueError):
            dijkstra(GRAFO, "Cidade Inexistente", "Grove")

    def test_peso_invalido(self):
        with self.assertRaises(ValueError):
            dijkstra({"A": {"B": -1}, "B": {}}, "A", "B")


if __name__ == "__main__":
    unittest.main()
