# Campos e colunas alvo

## Campos usados no projeto

| Campo original ou derivado | Uso no projeto |
| --- | --- |
| `patient_id` | Identificar cada registro de paciente de forma anonima. |
| `age` / `gender` | Usar idade e genero como variaveis de entrada para o modelo. |
| `primary_condition` | Representar a condicao principal informada ou registrada no atendimento. |
| `treatment` / `modality` | Apoiar a analise historica do tipo de atendimento realizado. |
| `length_of_stay` / `outcome` | Ajudar na analise de gravidade e resultado do atendimento. |
| `area_recomendada` | Nova coluna criada para treinar o modelo: cardiologia, neurologia, ortopedia, pediatria, clinica medica, obstetricia etc. |
| `nivel_urgencia` | Nova coluna criada para treinar o modelo: baixa, prioritario ou emergencia. |

## Colunas alvo para treinamento

Para que o modelo possa ser treinado, serao criadas duas colunas alvo:

- `area_recomendada`: area hospitalar sugerida para encaminhamento inicial.
- `nivel_urgencia`: classificacao da prioridade do atendimento.

Essas colunas podem ser preenchidas por regras de mapeamento baseadas na condicao principal do paciente, idade e fatores de risco. Depois disso, elas serao usadas como variaveis alvo para treinar um modelo supervisionado de classificacao.

---

[← Dataset de referencia](05-dataset-referencia.md) | [Regras de mapeamento →](07-regras-mapeamento.md)
