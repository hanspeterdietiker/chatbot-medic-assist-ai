# Medic Assist AI

Chatbot de apoio à triagem hospitalar que utiliza **classificação supervisionada** (Árvore de Decisão e Random Forest) para sugerir as **doenças mais prováveis (top-5)**, a **área hospitalar** e o **nível de urgência**, sem realizar diagnóstico ou prescrever medicamentos.

O paciente informa **múltiplos sintomas** (multi-seleção), um **perfil de saúde** (pressão arterial e colesterol) e **hábitos de vida** (tabagismo e consumo de álcool). O modelo prevê a doença a partir dos sintomas e do perfil; **área e urgência são derivadas da doença prevista** por regras clínicas. Os hábitos são aplicados como **regras pós-modelo** que re-ranqueiam as doenças prováveis e podem escalar a urgência.

> **Nota metodológica:** o dataset não contém colunas de álcool/fumo, por isso esses hábitos não são features de treino — entram como regras clínicas documentadas. Como a doença não é informada pelo paciente (apenas sintomas), o modelo aprende um problema realista; a acurácia **top-1** é naturalmente baixa (muitas doenças, poucos sintomas), sendo a acurácia **top-5** a métrica relevante para "doenças prováveis".

**Trabalho A3 — UC Inteligência Artificial** | Documento completo: [docs/13-trabalho-a3.md](docs/13-trabalho-a3.md)

---

## Integrantes

| Nome               | RA         |
| ------------------ | ---------- |
| Gabriel Silva      | 1272313274 |
| Hanspeter Dietiker | 1272313332 |

---

## Estrutura do projeto

```text
intelligence-ia-a3/
├── dataset/
│   ├── raw/                    # Dataset original do Kaggle
│   └── processed/              # Datasets tratados, codificados e split
├── docs/                       # Documentação por tópico
├── models/                     # Modelos treinados (.joblib) e métricas JSON
├── notebooks/                  # Reservado para notebooks exploratórios
├── poster/                     # Conteúdo do poster A3
├── src/
│   ├── main.py                 # Entry point do chatbot
│   ├── preprocess_dataset.py   # Limpeza e rotulação (B08+B09)
│   ├── encode_dataset.py       # Codificação categórica (B10)
│   ├── split_dataset.py        # Separação treino/teste (B11)
│   ├── train_model.py          # Treinamento e avaliação (B15–B20)
│   └── chatbot/
│       ├── conversation.py     # Fluxo guiado de perguntas
│       ├── terminal_ui.py      # Interface visual (cores, loading, painéis)
│       ├── model_predictor.py  # Predição da doença (top-5) + derivação área/urgência
│       ├── patient_encoder.py  # Conversão chatbot → features do modelo
│       ├── lifestyle_rules.py  # Regras de hábitos (álcool/fumo) pós-modelo
│       ├── messages.py         # Textos de segurança e avisos
│       ├── recommended_area_rules.py
│       └── urgency_triage_rules.py
└── tests/                      # Testes automatizados (pytest)
```

---

## Pré-requisitos

- **Python 3.10+** (mínimo: 3.8)

```bash
python --version
```

---

## Instalação

```bash
# 1. Baixa o código do repositório
git clone git@github.com:hanspeterdietiker/chatbot-medic-assist-ai.git

# 2. Entra na pasta do projeto que acabou de ser criada 
cd chatbot-medic-assist-ai

# 3. Cria o ambiente virtual
python -m venv venv

# 4. Ativa o ambiente virtual
venv\Scripts\activate        # Se estiver usando Windows
# source venv/bin/activate   # Se estiver usando Linux/macOS

# 5. Instala as dependências listadas no projeto
pip install -r requirements.txt
```

| Pacote        | Uso                                      |
| ------------- | ---------------------------------------- |
| pandas        | Leitura e processamento do dataset       |
| scikit-learn  | Modelos de ML, métricas e train/test split |
| rich          | Interface visual do terminal (cores, loading) |
| pytest        | Testes automatizados                     |

---

## Pipeline completo

Execute na ordem abaixo na primeira vez (ou após alterar o dataset):

```bash
# 1. Limpeza e criação das colunas-alvo
python src/preprocess_dataset.py

# 2. Codificação de variáveis categóricas
python src/encode_dataset.py

# 3. Separação treino/teste (80/20)
python src/split_dataset.py

# 4. Treinamento dos modelos e geração de métricas
python src/train_model.py

# 5. Chatbot interativo com modelo integrado
python src/main.py
```

### Entradas e saídas do pipeline

| Script                  | Entrada                              | Saída principal                          |
| ----------------------- | ------------------------------------ | ---------------------------------------- |
| preprocess_dataset.py   | dataset/raw/disease-symptoms-patient-profile.csv | dataset/processed/hospital-data-labeled.csv |
| encode_dataset.py       | hospital-data-labeled.csv            | hospital-data-encoded.csv, encoding_maps.json |
| split_dataset.py        | hospital-data-encoded.csv            | hospital-data-train.csv, hospital-data-test.csv |
| train_model.py          | train + test CSVs                    | models/*_disease.joblib, metrics_*.json (top-1/top-5) |
| main.py                 | Entrada interativa do usuário        | Top-5 doenças prováveis + área + urgência |

> **Dataset:** [Disease Symptoms and Patient Profile Dataset (Kaggle)](https://www.kaggle.com/datasets/uom190346a/disease-symptoms-and-patient-profile-dataset) — baixe o CSV e salve em `dataset/raw/disease-symptoms-patient-profile.csv`.
>
> **Features do modelo (8):** `age`, `gender`, `fever`, `cough`, `fatigue`, `difficulty_breathing`, `blood_pressure`, `cholesterol_level`. **Alvo:** `disease`.

---

## Testes automatizados

```bash
pytest tests/ -v
```

| Arquivo de teste          | O que cobre                                           |
| ------------------------ | ----------------------------------------------------- |
| test_preprocess_dataset.py | Integridade do dataset processado                     |
| test_encode_dataset.py   | Codificação categórica e mapeamentos                  |
| test_split_dataset.py    | Separação treino/teste 80/20                          |
| test_train_model.py      | Artefatos e métricas (top-1/top-5) do modelo de doença |
| test_model_predictor.py  | Integração chatbot ↔ modelo, encoder e top-N          |
| test_terminal_ui.py      | Interface visual (cores, painéis, loading)            |
| test_area_rules.py       | Regras de roteamento por doença e faixa etária        |
| test_urgency_rules.py    | Escalada de nível de urgência                         |
| test_lifestyle_rules.py  | Re-ranqueamento e escalada por hábitos (álcool/fumo)  |

---

## Documentação

| Documentos Principais | Conteúdo |
| --------- | -------- |
| [docs/01-visao-geral.md](docs/01-visao-geral.md) | Visão geral do projeto |
| [docs/14-resultados-finais.md](docs/14-resultados-finais.md) | Métricas e conclusões |
| [docs/12-backlog-desenvolvimento.md](docs/12-backlog-desenvolvimento.md) | Backlog com status das tarefas |
| [poster/CONTEUDO_POSTER.md](poster/poster.md) | Conteúdo do poster A3 |

---

## Variáveis de ambiente

O projeto **não utiliza variáveis de ambiente** obrigatórias. Todos os caminhos são relativos à raiz do projeto.

Opcional: `NO_COLOR=1` desativa cores no terminal (acessibilidade).

---

## Limitações e avisos éticos

- O sistema **não realiza diagnóstico médico** e **não prescreve medicamentos**.
- As **doenças prováveis (top-5)** são apenas possibilidades de apoio à triagem, **não um diagnóstico**.
- A recomendação é apenas apoio para triagem inicial.
- A decisão clínica final cabe a profissionais de saúde.
- Em emergências, ligue **192 (SAMU)**.
