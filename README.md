# TED-02 — Tabelas Hash e Grafos

**Disciplina:** Estruturas de Dados  
**Integrante 1:** Pedro Vitor Rocha Do Val  
**Integrante 2:** Matheus de Brito Araujo  
**Turma:** 4º ano de Sistemas de Informação  
**Professor:** Alex

## Objetivo
Resolver dois problemas em Python: contagem de frequência de palavras com tabela hash (`dict`) e cálculo de menor caminho em grafo ponderado por Dijkstra.

## Estrutura
- `hash_frequencias.py`: normalização, contagem, listagem e cinco palavras mais frequentes.
- `grafo_dijkstra.py`: lista de adjacência, validação e menor caminho.
- `dados/texto_exemplo.txt`: texto de demonstração com 1.097 palavras (465 distintas).
- `testes/testar_solucoes.py`: 10 testes de casos normais e excepcionais.
- `evidencias/`: capturas do terminal e saídas completas em `.txt`.
- `docs/documentacao.pdf`: relatório técnico da atividade (gerado a partir de `docs/documentacao.html`).

## Requisitos
Python 3.9 ou superior. Os programas usam apenas a biblioteca padrão; não é necessário instalar pacotes.

## Execução
No terminal, na pasta raiz do projeto:

```bash
python hash_frequencias.py
python hash_frequencias.py dados/texto_exemplo.txt
python grafo_dijkstra.py
python grafo_dijkstra.py Aurora Grove
python grafo_dijkstra.py Cedro Farol
python -m unittest discover -s testes -v
```

No Linux, pode ser necessário usar `python3` em vez de `python`.

Para usar outro texto, salve um arquivo `.txt` em UTF-8 e passe seu caminho ao primeiro programa. Para testar outras cidades, informe os dois nomes exatamente como aparecem na lista.

## Explicação resumida
A tabela hash utiliza palavras como chaves e suas contagens como valores. A atualização por palavra custa **O(1) em média**, e a varredura completa de *n* palavras custa **O(n) em média**, sem contar a ordenação para exibir o ranking. O ranking é ordenado por frequência decrescente e, em caso de empate, ordem alfabética. A ordem alfabética ignora acentos, para que `água` apareça junto do `a`.

O grafo contém sete cidades fictícias e distâncias positivas hipotéticas. É armazenado como um dicionário de dicionários (lista de adjacência). Dijkstra usa uma fila de prioridade (`heapq`), com complexidade **O((V + E) log V)** como limite usual para a implementação com heap, onde *V* é o número de vértices e *E* o número de arestas.

**Exemplo:** Aurora → Grove: `Aurora → Brisa → Duna → Estrela → Farol → Grove`, **16 km**.

Existe um segundo caminho de 16 km, começando por `Aurora → Cedro → Brisa` (3 + 1 = 4 km, igual ao trecho direto). O programa mantém o primeiro encontrado, pois só substitui uma distância quando a nova é estritamente menor.

## Casos especiais
- Texto sem palavras: retorna contagem vazia.
- Origem/destino inexistente: mensagem de erro e código de saída 1.
- Cidades desconectadas: informa ausência de caminho.
- Pesos nulos, negativos ou não finitos: rejeitados.
