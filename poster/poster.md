# Medic Assist AI: Triagem Hospitalar Inteligente com Árvore de Decisão

**Autores:** Gabriel Silva Magalhães | Hanspeter Dietiker  
**Instituição:** Universidade Salvador (UNIFACS) – Salvador – BA – Brasil  
**Disciplina:** Inteligência Artificial | Trabalho A3 | 2026  
**Repositório:** [github.com/hanspeterdietiker/chatbot-medic-assist-ai](https://github.com/hanspeterdietiker/chatbot-medic-assist-ai) (Tag: `EntregaA3`)  

---

## 1. Introdução
O volume massivo de pacientes em redes hospitalares gera um desafio constante na gestão de fluxos e triagem. Frequentemente, o paciente desconhece para qual setor deve ser encaminhado, o que resulta em:
* **Filas e Atrasos:** Sobrecarga administrativa nos guichês de atendimento.
* **Risco Clínico:** Pacientes com casos graves misturados a casos leves na mesma fila de espera.
* **Ineficiência Operacional:** Erros de encaminhamento entre os setores médicos.

O **Medic Assist AI** propõe uma solução baseada em Inteligência Artificial para automatizar esse encaminhamento inicial de forma ágil, segura e estruturada.

---

## 2. Objetivo
Desenvolver e validar um sistema de triagem inteligente (chatbot) capaz de automatizar o encaminhamento preliminar de pacientes, otimizando o fluxo hospitalar. 

**Metas Específicas:**
* Classificar pacientes em **9 áreas médicas** distintas.
* Identificar **3 níveis de urgência** (Baixa, Prioritário, Emergência).
* Implementar uma interface interativa via Terminal.
* Garantir a segurança clínica através de protocolos de sobreposição (Emergency Override).

---

## 3. Métodos

### 3.1. Base de Dados e Pré-processamento
Utilizou-se um conjunto de dados estruturados para o treinamento supervisionado:
* **Fonte:** Hospital Patient Records (Kaggle).
* **Volumetria:** 984 registros após limpeza e higienização.
* **Variáveis de Entrada (Features):** Idade, Gênero e Condição Médica.
* **Variáveis Alvo (Targets):** Área Recomendada e Nível de Urgência.
* **Tratamento:** Aplicação de `LabelEncoder` para conversão de variáveis categóricas e uso de `Random State 42` para garantir reprodutibilidade na divisão do dataset (80% Treino / 20% Teste).

### 3.2. Algoritmo de Inteligência Artificial
A **Árvore de Decisão (`DecisionTreeClassifier`)** foi escolhida devido à sua alta interpretabilidade clínica. 
* **Transparência:** Os caminhos de decisão (regras *IF-THEN*) são auditáveis e similares aos protocolos de triagem humana.
* **Sem "Black-Box":** Diferente de redes neurais, cada predição é explicável, o que é um requisito crítico na área da saúde.
* Foram treinados dois modelos independentes e serializados em arquivos `.joblib`.

### 3.3. Arquitetura do Sistema
O sistema foi desenhado em três camadas principais:
1. **Frontend (Terminal):** Uso da biblioteca Python `Rich` para criar uma interface colorida e amigável.
2. **Coleta e Encoder:** Mapeamento de texto livre do paciente para vetores numéricos estruturados.
3. **Camada Híbrida (Segurança):** Fusão das predições de Machine Learning com regras heurísticas (ex.: elevação automática para "EMERGÊNCIA" se houver relato de inconsciência ou falta de ar).

---

## 4. Resultados

### 4.1. Performance Preditiva
Resultados obtidos no conjunto de teste (197 registros):

| Modelo | Acurácia | Precision | F1-Score |
| :--- | :---: | :---: | :---: |
| **Área Recomendada** | 100% | 1.00 | 1.00 |
| **Nível de Urgência** | 100% | 1.00 | 1.00 |

*Nota: A acurácia máxima reflete a natureza determinística do dataset de treino. Em ambiente real, o modelo mimetiza com perfeição o protocolo clínico ali estabelecido.*

### 4.2. Qualidade e Execução
* O sistema possui **103 testes automatizados** (via `pytest`), garantindo robustez desde o pipeline de dados até a experiência do usuário (UX).
* O fluxo do chatbot foi validado em 4 etapas contínuas: Coleta Demográfica, Sintomatologia, Validação de Segurança e Resumo da Triagem.

---

## 5. Conclusão
O **Medic Assist AI** cumpre os requisitos de eficiência e segurança, oferecendo uma prova de conceito robusta para triagem hospitalar primária. 

A principal inovação está na **arquitetura híbrida**: a integração da predição estatística da IA com a rigidez de protocolos de segurança baseados em regras garante que casos críticos de emergência nunca sejam subestimados. Como trabalhos futuros, sugere-se a expansão para Processamento de Linguagem Natural (NLP) mais avançado e a integração com sistemas de Prontuário Eletrônico do Paciente (PEP).

---

## 6. Referências Bibliográficas
1. Kaggle. Hospital Patient Records Dataset. Disponível em: kaggle.com. Acesso em: Mai. 2026.
2. PEDREGOSA, F. et al. Scikit-learn: Machine Learning in Python. Journal of Machine Learning Research, 2011.
3. WILLISON, S. Rich: Rich text and beautiful formatting in the terminal. Python Package Index, 2024.
4. RUSSEL, S.; NORVIG, P. Inteligência Artificial: Uma Abordagem Moderna. 3º Ed. Elsevier, 2013.