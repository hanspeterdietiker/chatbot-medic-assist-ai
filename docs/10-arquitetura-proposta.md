# Arquitetura proposta

## Fluxo arquitetural

```text
Usuario
  -> Chatbot
  -> Pre-processamento dos dados
  -> Modelo treinado
  -> Classificacao de area e urgencia
  -> Resposta ao paciente
  -> Resumo para triagem humana
```

## Componentes principais

- **Interface do chatbot**: conversa guiada com o paciente.
- **Base de dados**: dataset hospitalar reestruturado e base propria de apoio a triagem.
- **Modulo de pre-processamento**: limpeza, codificacao de variaveis categoricas e separacao treino/teste.
- **Modelo de IA**: algoritmo de classificacao definido pela equipe.
- **Modulo de resposta**: orientacao segura com area recomendada e nivel de urgencia.
- **Relatorio**: resumo dos dados informados e da recomendacao gerada.

## Papel do modelo treinado

O modelo recebe os dados padronizados do paciente e retorna as classes mais provaveis para `area_recomendada` e `nivel_urgencia`.

Essas respostas devem ser usadas como apoio, nao como decisao clinica definitiva.

---

[← Fluxo de funcionamento](09-fluxo-funcionamento.md) | [Entregas e resultados →](11-entregas-resultados.md)
