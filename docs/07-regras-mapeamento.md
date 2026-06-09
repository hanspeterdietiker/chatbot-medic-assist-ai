# Regras de mapeamento

As colunas `area_recomendada` e `nivel_urgencia` serao criadas a partir de regras de mapeamento baseadas na condicao principal, idade e fatores de risco.

Depois da criacao dessas colunas, elas serao usadas como variaveis alvo para treinar um modelo supervisionado de classificacao.

## Exemplos de regras

| Condicao principal | Area recomendada | Nivel de urgencia sugerido |
| --- | --- | --- |
| Heart Disease / Chest Pain | Cardiologia ou pronto-socorro | Prioritario ou emergencia |
| Stroke / Neurological Issue | Neurologia ou pronto-socorro | Emergencia |
| Fracture / Trauma | Ortopedia ou pronto atendimento | Prioritario |
| Flu / Respiratory Infection | Clinica medica, pneumologia ou pediatria | Baixa ou prioritario |
| Pregnancy Complication | Obstetricia ou pronto-socorro | Emergencia |
| Diabetes / High Glucose | Clinica medica ou endocrinologia | Prioritario |
| Skin Disease | Dermatologia ou clinica medica | Baixa |

## Observacao

As regras devem ser revisadas pela equipe e, quando possivel, validadas com orientacao do professor. Elas servem para adaptar o dataset ao problema de classificacao supervisionada do projeto.

---

[← Campos e colunas alvo](06-campos-colunas-alvo.md) | [Tecnicas de IA →](08-tecnicas-ia.md)
