# Campos e colunas alvo

## Features do modelo

O modelo de classificacao usa 8 features, todas disponiveis na triagem via chatbot:

| Campo | Tipo | Uso no projeto |
| --- | --- | --- |
| `age` | inteiro | Idade do paciente. |
| `gender` | binario (Female=0, Male=1) | Genero. |
| `fever` | binario (No=0, Yes=1) | Sintoma — febre. |
| `cough` | binario (No=0, Yes=1) | Sintoma — tosse. |
| `fatigue` | binario (No=0, Yes=1) | Sintoma — fadiga. |
| `difficulty_breathing` | binario (No=0, Yes=1) | Sintoma — dificuldade respiratoria (tambem aciona regra de seguranca). |
| `blood_pressure` | ordinal (Low=0, Normal=1, High=2) | Proxy de saude — pressao arterial. |
| `cholesterol_level` | ordinal (Low=0, Normal=1, High=2) | Proxy de saude — colesterol. |

O paciente seleciona **multiplos sintomas** (multi-selecao, ate 5). "Dor intensa / no peito" e coletada para as regras clinicas, mas nao e coluna do dataset (nao e feature do modelo).

## Coluna alvo

- `disease`: **doenca provavel** (alvo unico do modelo). Codificada com LabelEncoder; o chatbot exibe as **top-5** doencas com probabilidade (`predict_proba`).

## Derivadas por regras (nao sao alvo do modelo)

- `area_recomendada`: area hospitalar sugerida, **derivada da doenca prevista** por regras de mapeamento por palavras-chave.
- `nivel_urgencia`: prioridade (`baixa`, `prioritario`, `emergencia`), derivada da doenca + escalada por sintomas e por habitos de vida.

## Habitos de vida (regras pos-modelo)

`smokes` e `drinks_alcohol` sao coletados no chatbot e **nao** sao features de treino. Eles re-ranqueiam as doencas provaveis (fumo → respiratorio/cardiaco; alcool → hepatico/gastrointestinal) e podem escalar a urgencia em 1 nivel. Ver [07-regras-mapeamento.md](07-regras-mapeamento.md).

---

[← Dataset de referencia](05-dataset-referencia.md) | [Regras de mapeamento →](07-regras-mapeamento.md)
