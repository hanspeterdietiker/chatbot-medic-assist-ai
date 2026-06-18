# Dataset de referencia

O dataset de referencia e o **Disease Symptoms and Patient Profile Dataset**, disponivel no Kaggle:

[Disease Symptoms and Patient Profile Dataset](https://www.kaggle.com/datasets/uom190346a/disease-symptoms-and-patient-profile-dataset)

O dataset relaciona sintomas e perfil do paciente a uma doenca. Possui **349 registros** e **116 doencas** distintas, com as colunas: `Disease`, `Fever`, `Cough`, `Fatigue`, `Difficulty Breathing` (cada uma Yes/No), `Age`, `Gender`, `Blood Pressure`, `Cholesterol Level` (Low/Normal/High) e `Outcome Variable` (Positive/Negative).

Para baixar: faca login no Kaggle, baixe o CSV e salve em `dataset/raw/disease-symptoms-patient-profile.csv`.

## Como o dataset e usado

O alvo do modelo de Machine Learning e a coluna **`disease`** (doenca provavel). As features sao sintomas e perfil de saude:

`age`, `gender`, `fever`, `cough`, `fatigue`, `difficulty_breathing`, `blood_pressure`, `cholesterol_level`.

A **area recomendada** e o **nivel de urgencia** nao sao alvos do modelo: sao **derivados da doenca prevista** por regras de mapeamento (ver [07-regras-mapeamento.md](07-regras-mapeamento.md)). Isso mantem o foco em triagem e permite que **habitos de vida** (alcool/fumo) influenciem doenca, area e urgencia de forma coerente, via regras pos-modelo.

> **Habitos (alcool/fumo):** o dataset nao traz essas colunas. Por isso, alcool e tabagismo sao coletados no chatbot e aplicados como **regras clinicas pos-modelo** (re-ranqueamento das doencas provaveis e escalada de urgencia), sem dados sinteticos no treino. Pressao arterial e colesterol funcionam como **proxies de saude** entre as features.

## Limitacao conhecida

Com 116 doencas e poucas amostras por classe, a acuracia **top-1** e naturalmente baixa; a metrica relevante para "doencas provaveis" e a acuracia **top-5**. Como a doenca nao e informada pelo paciente (apenas sintomas), o problema aprendido e realista — diferente de versoes anteriores em que a condicao era feature e gerava acuracia artificial.

## Uso academico

O dataset sera usado para fins academicos e de pratica, dentro do contexto da A3 de Inteligencia Artificial.

---

[← Limite etico e seguranca](04-limite-etico-seguranca.md) | [Campos e colunas alvo →](06-campos-colunas-alvo.md)
