# Tecnicas de IA

Com o dataset reestruturado, o projeto passa a ser um problema de **classificacao supervisionada**.

## Algoritmos utilizados

| Algoritmo | Papel no projeto |
| --------- | ---------------- |
| **Arvore de Decisao** | Modelo principal — interpretavel, adequado para apresentacao A3 |
| **Random Forest** | Comparacao — ensemble de arvores para avaliar robustez |

Dois modelos independentes sao treinados para cada alvo:
- `area_recomendada` (area hospitalar sugerida)
- `nivel_urgencia` (baixa, prioritario, emergencia)

## Algoritmo selecionado

Apos comparacao de acuracia media no conjunto de teste, o chatbot utiliza **Arvore de Decisao** (`decision_tree`). Em caso de empate, a Arvore e preferida por permitir visualizar regras de classificacao.

Detalhes em `models/model_metadata.json` e [Resultados finais](14-resultados-finais.md).

## Features de entrada

Apenas variaveis disponiveis na triagem via chatbot:
- `Age`, `Gender`, `Condition`

## Metricas de avaliacao

O modelo foi avaliado com:

- acuracia (B17);
- matriz de confusao (B18);
- relatorio de classificacao — precision, recall, F1-score (B19);
- comparacao entre Arvore de Decisao e Random Forest (B16).

Arquivos: `models/metrics_decision_tree.json`, `models/metrics_random_forest.json`

---

[← Regras de mapeamento](07-regras-mapeamento.md) | [Fluxo de funcionamento →](09-fluxo-funcionamento.md)
