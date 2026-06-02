# Backlog de desenvolvimento

Este backlog organiza as atividades do projeto **Medic Assist IA**. A divisao considera um fluxo simples: preparar os dados, treinar o modelo, criar o chatbot, validar os resultados e organizar a entrega da A3.

## Sprint 1 - Preparacao do projeto e dataset

| ID | Tarefa | Prioridade | Criterio de aceite |
| --- | --- | --- | --- |
| B01 | Criar estrutura inicial de pastas do projeto | Alta | Projeto possui pastas para `dataset`, `notebooks`, `src`, `models` e `docs`. |
| B02 | Baixar o dataset do Kaggle | Alta | Dataset esta salvo em `dataset` e documentado em `docs/05-dataset-referencia.md`. |
| B03 | Analisar colunas originais do dataset | Alta | Existe um resumo das colunas disponiveis e dos campos uteis para o modelo. |
| B04 | Definir regras iniciais para `area_recomendada` | Alta | Regras foram documentadas com base em `primary_condition` ou campo equivalente. |
| B05 | Definir regras iniciais para `nivel_urgencia` | Alta | Classes baixa, prioritario e emergencia foram mapeadas. |
| B06 | Criar roteiro da conversa do chatbot | Alta | Fluxo de perguntas iniciais esta definido: idade, genero, condicao principal e dados basicos. |
| B07 | Definir mensagens de seguranca do chatbot | Alta | Chatbot possui avisos de que nao diagnostica e nao prescreve medicamentos. |

## Sprint 2 - Tratamento dos dados e prototipo do chatbot

| ID | Tarefa | Prioridade | Criterio de aceite |
| --- | --- | --- | --- |
| B08 | Criar script ou notebook de limpeza do dataset | Alta | Dataset tratado e salvo em `data/processed`. |
| B09 | Criar colunas derivadas `area_recomendada` e `nivel_urgencia` | Alta | Dataset tratado contem as duas colunas alvo. |
| B10 | Codificar variaveis categoricas | Media | Dados estao prontos para uso em modelo de classificacao. |
| B11 | Separar dados em treino e teste | Alta | Conjuntos de treino e teste foram gerados com proporcao definida. |
| B12 | Criar prototipo inicial do chatbot | Alta | Usuario consegue informar dados basicos em uma conversa guiada. |
| B13 | Padronizar entrada do usuario para o formato do modelo | Alta | Respostas do chatbot sao convertidas para campos estruturados. |
| B14 | Criar template de resumo para triagem humana | Media | Sistema gera resumo com dados informados, area sugerida e urgencia. |

## Sprint 3 - Modelo de IA e integracao

| ID | Tarefa | Prioridade | Criterio de aceite |
| --- | --- | --- | --- |
| B15 | Treinar modelo com Arvore de Decisao | Alta | Modelo treinado gera predicoes para area e urgencia. |
| B16 | Treinar modelo com Random Forest | Media | Resultado pode ser comparado com Arvore de Decisao. |
| B17 | Avaliar modelo com acuracia | Alta | Acuracia foi calculada para as saidas previstas. |
| B18 | Gerar matriz de confusao | Alta | Matriz de confusao foi produzida para analise do modelo. |
| B19 | Gerar relatorio de classificacao | Media | Precisao, recall e F1-score foram registrados. |
| B20 | Salvar modelo treinado | Alta | Modelo final esta salvo em `models` ou pasta equivalente. |
| B21 | Integrar chatbot ao modelo treinado | Alta | Chatbot envia dados ao modelo e recebe previsao. |
| B22 | Exibir resposta segura ao paciente | Alta | Resposta mostra area recomendada e nivel de urgencia sem diagnosticar. |

## Sprint 4 - Validacao, entrega e apresentacao

| ID | Tarefa | Prioridade | Criterio de aceite |
| --- | --- | --- | --- |
| B23 | Criar casos de teste simulados | Alta | Existem exemplos para cardiologia, neurologia, ortopedia, clinica medica e obstetricia. |
| B24 | Validar predicoes com os casos simulados | Alta | Modelo retorna respostas coerentes para os exemplos principais. |
| B25 | Revisar limites eticos nas respostas | Alta | Nenhuma resposta informa diagnostico ou medicamento. |
| B26 | Melhorar experiencia de uso do chatbot | Media | Fluxo esta claro, com perguntas objetivas e respostas compreensiveis. |
| B27 | Criar README principal do projeto | Alta | README possui instalacao, execucao, treinamento e teste. |
| B28 | Preparar conteudo do poster | Alta | Poster inclui problema, dataset, arquitetura, algoritmo, metricas, fluxo e resultados. |
| B29 | Documentar resultados finais | Alta | Metricas e conclusoes estao registradas em documento ou notebook. |
| B30 | Revisar documentacao final | Media | Arquivos em `docs` estao consistentes e sem informacoes duplicadas. |

## Prioridades gerais

| Prioridade | Itens |
| --- | --- |
| Alta | Dataset tratado, colunas alvo, modelo treinado, chatbot funcional, respostas seguras e metricas. |
| Media | Comparacao entre algoritmos, melhoria de UX, relatorio detalhado e documentacao final. |
| Baixa | Melhorias visuais, historico de atendimentos, exportacao avancada de relatorios e expansao de regras. |

## Definition of Done

Uma tarefa sera considerada concluida quando:

- estiver implementada;
- puder ser demonstrada;
- tiver resultado verificavel;
- estiver documentada quando necessario;
- respeitar o limite etico do projeto;
- nao bloquear a execucao do fluxo principal do MediAssist IA.
