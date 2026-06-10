# Resultados finais

Documento de consolidação das métricas e conclusões do **Medic Assist AI** (B29).

---

## Resumo executivo

O Medic Assist AI é um chatbot de triagem hospitalar que aplica **classificação supervisionada** para sugerir área hospitalar e nível de urgência. O pipeline completo — desde o tratamento do dataset até a integração com o chatbot — foi implementado em scripts Python reproduzíveis, com 103 testes automatizados.

O sistema combina predição de ML com **regras de segurança** para emergências, respeitando limites éticos (sem diagnóstico, sem prescrição).

---

## Métricas do modelo

Fonte: `models/model_metadata.json` e `models/metrics_*.json`

### Comparação de algoritmos

| Algoritmo | Acurácia área | Acurácia urgência | Média |
| --------- | ------------- | ----------------- | ----- |
| Árvore de Decisão | 100% | 100% | **100%** |
| Random Forest | 100% | 100% | **100%** |

**Algoritmo selecionado:** Árvore de Decisão (`decision_tree`) — empate na acurácia; preferido por interpretabilidade (adequado à apresentação A3).

### Features utilizadas

- `Age` (idade)
- `Gender` (gênero codificado)
- `Condition` (condição principal codificada)

Colunas pós-atendimento (`Procedure`, `Cost`, `Outcome`) foram **excluídas** para evitar data leakage na inferência via chatbot.

### Matrizes de confusão

| Alvo | Dimensão da matriz | Diagonal (acertos) |
| ---- | ------------------ | ------------------ |
| area_recomendada | 9×9 | 197/197 (100%) |
| nivel_urgencia | 3×3 | 197/197 (100%) |

Relatórios completos com precision, recall e F1-score disponíveis em:
- `models/metrics_decision_tree.json`
- `models/metrics_random_forest.json`

---

## Conclusões

1. **Aplicabilidade:** o pipeline demonstra como técnicas de classificação supervisionada podem apoiar a organização do atendimento hospitalar inicial.

2. **Integração:** o chatbot converte respostas do paciente em features do modelo, prediz área/urgência e aplica camada de segurança para casos críticos.

3. **Reprodutibilidade:** todo o fluxo é executável via scripts CLI documentados no README.

4. **Qualidade:** 103 testes pytest cobrem dados, modelo, integração e interface visual.

### Limitações reconhecidas

- Rótulos (`area_recomendada`, `nivel_urgencia`) derivados por regras a partir da mesma `Condition` usada como feature — explica acurácia perfeita no teste.
- Apenas 3 variáveis disponíveis na triagem via chatbot.
- Interface limitada ao terminal (sem app web ou mobile).

### Próximos passos sugeridos

- Coletar rótulos clínicos reais (validados por profissionais) para retreinamento
- Adicionar features de sintomas ao modelo (febre, dor, consciência)
- Interface web para uso em recepção hospitalar
- Validação com casos clínicos do professor

---

[← Backlog de desenvolvimento](12-backlog-desenvolvimento.md) | [Doc A3 →](13-trabalho-a3.md)
