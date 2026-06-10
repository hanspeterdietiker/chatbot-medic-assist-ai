# Arquitetura proposta

## Fluxo arquitetural

```text
Usuario
  -> Chatbot (terminal_ui + conversation)
  -> Codificacao do paciente (patient_encoder)
  -> Modelo treinado (model_predictor)
  -> Camada de seguranca (regras de emergencia)
  -> Resposta ao paciente
  -> Resumo para triagem humana
```

## Componentes principais

| Componente | Arquivo | Funcao |
| ---------- | ------- | ------ |
| Interface do chatbot | `conversation.py`, `terminal_ui.py` | Conversa guiada com UX visual (cores, loading, paineis) |
| Base de dados | `dataset/` | Dataset hospitalar bruto, tratado e codificado |
| Pre-processamento | `preprocess_dataset.py`, `encode_dataset.py`, `split_dataset.py` | Limpeza, codificacao e split treino/teste |
| Treinamento | `train_model.py` | Arvore de Decisao + Random Forest, metricas e persistencia |
| Predicao | `model_predictor.py`, `patient_encoder.py` | Integracao chatbot ao modelo com fallback |
| Modulo de resposta | `messages.py`, `terminal_ui.py` | Orientacao segura com area e urgencia |
| Relatorio | `build_triage_summary()` | Resumo estruturado para triagem humana |

## Papel do modelo treinado

O modelo recebe os dados padronizados do paciente (`Age`, `Gender`, `Condition`) e retorna as classes mais provaveis para `area_recomendada` e `nivel_urgencia`.

Regras de seguranca podem sobrescrever ou escalar a urgencia em casos criticos (inconsciencia, dificuldade respiratoria).

Essas respostas devem ser usadas como apoio, nao como decisao clinica definitiva.

---

[← Fluxo de funcionamento](09-fluxo-funcionamento.md) | [Entregas e resultados →](11-entregas-resultados.md)
