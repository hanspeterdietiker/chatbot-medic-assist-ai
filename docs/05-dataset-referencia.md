# Dataset de referencia

O dataset de referencia e o **Hospital Patient Records Dataset**, disponivel no Kaggle:

[Blueblushed. Hospital Patient Records Dataset](https://www.kaggle.com/datasets/blueblushed/hospital-dataset-for-practice)

O dataset possui registros hospitalares de pacientes e pode ser usado como base de aprendizado. Como ele nao foi criado especificamente para um chatbot de sintomas, sera necessario adaptar seus campos para o contexto do projeto.

## Reestruturacao proposta

A reestruturacao transforma uma base hospitalar de pratica em uma base de classificacao supervisionada. Dessa forma, o modelo aprende a associar perfis e condicoes clinicas a uma area hospitalar e a um nivel de urgencia.

Caso as colunas originais nao possuam `area_recomendada` e `nivel_urgencia`, essas colunas serao derivadas por regras de mapeamento e usadas como alvo no treinamento supervisionado.

## Uso academico

O dataset sera usado para fins academicos e de pratica, dentro do contexto da A3 de Inteligencia Artificial.

---

[← Limite etico e seguranca](04-limite-etico-seguranca.md) | [Campos e colunas alvo →](06-campos-colunas-alvo.md)
