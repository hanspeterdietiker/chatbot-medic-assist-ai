# Medic Assist AI — Conteúdo do Poster A3

> Material estruturado para montagem do poster de apresentação.
> Integrantes: Gabriel Silva (1272313274) | Hanspeter Dietiker (1272313332)

---

## 1. Problema e contextualização

Redes hospitalares recebem grande volume de pacientes com diferentes condições clínicas, especialidades e níveis de urgência. Muitas vezes, o paciente não sabe se deve procurar pronto-socorro, clínica médica, cardiologia, ortopedia ou outra área.

**Problema:** encaminhamentos incorretos geram filas, atrasos e risco clínico.

**Solução proposta:** chatbot de triagem inicial com modelo de IA treinado em registros hospitalares, sugerindo área e urgência sem substituir avaliação médica.

---

## 2. Dataset

| Item | Detalhe |
| ---- | ------- |
| Fonte | Kaggle — Hospital Patient Records Dataset |
| Registros | 984 pacientes (após limpeza) |
| Features de entrada | Idade, Gênero, Condição principal |
| Colunas-alvo | `area_recomendada`, `nivel_urgencia` |
| Rotulação | Regras clínicas baseadas em condição e idade |
| Divisão | 80% treino (787) / 20% teste (197) |

---

## 3. Arquitetura do sistema

```text
Paciente
  → Chatbot (terminal_ui + conversation)
  → Codificação (patient_encoder)
  → Modelo treinado (Árvore de Decisão / Random Forest)
  → Camada de segurança (regras de emergência)
  → Resposta ao paciente + resumo para triagem humana
```

**Pipeline de dados:**

```text
CSV bruto → preprocess → encode → split → train → models/
```

---

## 4. Algoritmos de IA

| Algoritmo | Uso | Vantagem |
| --------- | --- | -------- |
| **Árvore de Decisão** | Classificação de área e urgência | Interpretável, regras visíveis |
| **Random Forest** | Comparação e ensemble | Maior robustez em dados ruidosos |

Dois modelos independentes: um para `area_recomendada`, outro para `nivel_urgencia`.

**Algoritmo selecionado para produção:** Árvore de Decisão (`decision_tree`)

---

## 5. Métricas de avaliação

### Árvore de Decisão

| Alvo | Acurácia |
| ---- | -------- |
| area_recomendada | 100% |
| nivel_urgencia | 100% |
| **Média** | **100%** |

### Random Forest

| Alvo | Acurácia |
| ---- | -------- |
| area_recomendada | 100% |
| nivel_urgencia | 100% |
| **Média** | **100%** |

Métricas adicionais registradas: matriz de confusão, precision, recall e F1-score (ver `models/metrics_*.json`).

> Nota: acurácia perfeita reflete que as colunas-alvo foram derivadas por regras determinísticas a partir da mesma condição usada como feature. Em cenário real com rótulos clínicos independentes, métricas seriam menores.

---

## 6. Fluxo do chatbot (6 etapas)

1. Coleta de dados (idade, gênero, condição, sintomas)
2. Padronização para formato do modelo
3. Predição via modelo treinado
4. Camada de segurança (emergências, escalada por sintomas)
5. Resposta segura ao paciente (sem diagnóstico)
6. Resumo estruturado para triagem humana

---

## 7. Resultados e conclusões

- Pipeline completo de IA implementado: dados → modelo → chatbot integrado
- Interface terminal com loading, cores e painéis (`rich`)
- Camada híbrida: ML + regras de segurança para emergências
- 103 testes automatizados cobrindo pipeline, modelo e UX
- Sistema demonstra aplicação realista de classificação supervisionada em contexto hospitalar

**Limitações:** apenas 3 features na triagem; rótulos derivados por regras; não substitui avaliação médica.

---

## 8. Limites éticos

- Não realiza diagnóstico
- Não prescreve medicamentos
- Não substitui profissionais de saúde
- Validação clínica obrigatória
- Emergências: SAMU 192

---

## 9. Referências

- Dataset: Kaggle Hospital Patient Records
- scikit-learn: DecisionTreeClassifier, RandomForestClassifier
- Documentação do projeto: `docs/` e `README.md`
