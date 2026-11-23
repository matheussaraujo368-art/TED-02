"""Testes automatizados, sem dependências externas."""
import math
import sys
import unittest
from pathlib import Path

# Permite executar este arquivo de qualquer pasta, sem depender do diretório atual.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from hash_frequencias import chave_alfabetica, cinco_mais_frequentes, contar_frequencias, obter_texto
from grafo_dijkstra import CIDADES, CONEXOES, construir_grafo, dijkstra, localizar_cidade

GRAFO = construir_grafo(CIDADES, CONEXOES)


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

    def test_frase_direta(self):
        self.assertEqual(obter_texto(["--texto", "dados grafo"]), "dados grafo")
        with self.assertRaises(ValueError):
            obter_texto(["--texto"])


class TesteGrafo(unittest.TestCase):
    def test_conexoes_nos_dois_sentidos(self):
        for cidade, vizinhos in GRAFO.items():
            for vizinho, distancia in vizinhos.items():
                self.assertEqual(GRAFO[vizinho][cidade], distancia)

    def test_nova_conexao_vale_ida_e_volta(self):
        grafo = construir_grafo(CIDADES, CONEXOES + [("Aurora", "Grove", 5)])
        self.assertEqual(dijkstra(grafo, "Aurora", "Grove"), (["Aurora", "Grove"], 5))
        self.assertEqual(dijkstra(grafo, "Grove", "Aurora"), (["Grove", "Aurora"], 5))

    def test_conexoes_invalidas(self):
        invalidas = [("A", "Z", 1), ("A", "A", 1), ("A", "B", 0), ("A", "B", -1), ("A", "B", "3")]
        for conexao in invalidas:
            with self.subTest(conexao=conexao), self.assertRaises(ValueError):
                construir_grafo(["A", "B"], [conexao])

    def test_conexao_repetida(self):
        with self.assertRaises(ValueError):
            construir_grafo(["A", "B"], [("A", "B", 1), ("B", "A", 9)])

    def test_maiusculas_e_minusculas(self):
        self.assertEqual(localizar_cidade(GRAFO, " aURORA "), "Aurora")
        with self.assertRaises(ValueError):
            localizar_cidade(GRAFO, "Lua")


class TesteDijkstra(unittest.TestCase):
    def test_rota_principal(self):
        self.assertEqual(dijkstra(GRAFO, "Aurora", "Grove"),
                         (["Aurora", "Brisa", "Duna", "Estrela", "Farol", "Grove"], 16))

    def test_mesma_cidade(self):
        self.assertEqual(dijkstra(GRAFO, "Aurora", "Aurora"), (["Aurora"], 0))

    def test_sem_caminho(self):
        grafo = construir_grafo(CIDADES + ["Ilha"], CONEXOES)
        self.assertEqual(dijkstra(grafo, "Aurora", "Ilha"), ([], math.inf))

    def test_cidade_inexistente(self):
        with self.assertRaises(ValueError):
            dijkstra(GRAFO, "Cidade Inexistente", "Grove")

    def test_peso_invalido(self):
        with self.assertRaises(ValueError):
            dijkstra({"A": {"B": -1}, "B": {}}, "A", "B")


if __name__ == "__main__":
    unittest.main()
