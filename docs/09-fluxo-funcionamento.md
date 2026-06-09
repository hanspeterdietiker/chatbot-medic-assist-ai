# Fluxo de funcionamento

O funcionamento do Medic Assist AI pode ser dividido em seis etapas principais.

| Etapa | Nome | Descricao |
| --- | --- | --- |
| 1 | Entrada do paciente | O chatbot coleta idade, genero, condicao principal e informacoes basicas do atendimento. |
| 2 | Padronizacao dos dados | O sistema converte a resposta do usuario para campos estruturados compativeis com o dataset. |
| 3 | Modelo de classificacao | O modelo treinado recebe os dados do paciente e calcula a classe mais provavel. |
| 4 | Resultado do modelo | O sistema retorna area hospitalar recomendada e nivel de urgencia. |
| 5 | Resposta segura | O chatbot orienta o paciente sem diagnosticar e sem indicar medicamentos. |
| 6 | Resumo para triagem | O sistema gera um resumo para a recepcao, triagem humana ou medico da teleconsulta. |

## Saida esperada

Ao final do fluxo, o sistema deve produzir:

- area hospitalar recomendada;
- nivel de urgencia;
- mensagem segura para o paciente;
- resumo estruturado para triagem humana.

---

[← Tecnicas de IA](08-tecnicas-ia.md) | [Arquitetura proposta →](10-arquitetura-proposta.md)
