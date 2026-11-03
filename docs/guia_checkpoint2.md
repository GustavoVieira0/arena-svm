# Guia do Checkpoint 2 (03/11): experimentos

Notebook: `notebooks/02_experimentos_svm.ipynb`, executado e com todas as saídas.

## Checklist → evidência
| Item do checkpoint | Onde está |
|---|---|
| Pelo menos três experimentos controlados | E1 (kernels), E2 (features de golpes), E3 (C e gamma), E4 (vazamento): só uma variável muda em cada um |
| Hipótese registrada antes de cada experimento | Registradas em 20/10 no notebook 01 (seção 8) e repetidas antes de cada experimento no notebook 02 |
| Comparação com baseline | Seção 3 (classe majoritária, mais rápido, maior total, Regressão Logística) e tabela/gráfico final (seção 6) |
| Métricas justificadas | Seção 2: acurácia (classes equilibradas), F1, ROC-AUC (confiança do score) e teto de acerto |
| Análise de pelo menos três erros ou casos inesperados | Seção 5 (E5): Zacian × Kleavor, Marshadow × Lokix, Nickit × Calyrex-Shadow, erros por faixa de incerteza, duelos de nocaute em 1 golpe. Caso inesperado: E4 |
| Conclusões provisórias e limitações | Seção 7 |

## Resultados principais (teste: gerações 7–9, Pokémon nunca vistos)
| Modelo | Acurácia |
|---|---|
| Vence o mais rápido | 67,8% |
| Vence o maior total | 80,6% |
| Regressão Logística (base) | 85,6% |
| SVM RBF (base), E1 | 86,6% |
| Regressão Logística (base + golpes) | 91,8% |
| **SVM RBF ajustado (base + golpes), E2 + E3** | **92,6%** |

| Experimento | Hipótese | Resultado |
|---|---|---|
| E1: kernel | RBF > linear | ✅ Confirmada, mas fraca (+1 ponto) |
| E2: features de golpes | Recupera a queda de 92% → 87% | ✅ Confirmada: 86,6% → 92,6% |
| E3: C e gamma | Ganho pequeno | ❌ Sem ganho (padrão já perto do ótimo) |
| E4: vazamento | Divisão aleatória infla o resultado | ❌ Refutada: 92,5% × 92,6% (features relativas, sem identidade do Pokémon) |

## Roteiro (10 min)
| Tempo | Quem | O que mostrar |
|---|---|---|
| 0–2 | Alceu | Pergunta de investigação e como as hipóteses foram registradas antes (notebook 01, seção 8) |
| 2–4 | Anthony | E1 e E3: kernels e ajuste de C/gamma (heatmap). Mensagem: o algoritmo mudou pouco |
| 4–6 | Gustavo | E2: features de golpes (+6 pontos) e a retirada de features (o "nocaute" é a mais importante) |
| 6–8 | Luan | E4 (caso inesperado) e E5: onde o modelo erra e os 3 casos (Zacian, Marshadow, Nickit) |
| 8–10 | Lucas | Conclusões, limitações e demo: `.venv\Scripts\python src\batalhar.py nickit calyrex-shadow` |

## Perguntas prováveis
- **"Por que o E4 não mostrou vazamento?"** As features são relativas (diferenças, eficácia, golpes para nocautear) e não
  dizem qual Pokémon é. O modelo não tem como decorar personagens, então aprendeu regras gerais. A divisão por geração
  continua correta, porque simula o uso real.
- **"As features de golpes não são 'trapaça', já que usam a fórmula do simulador?"** Usam só o que se sabe antes da
  batalha (atributos, tipos e lista pública de golpes), sem simular a batalha nem a sorte. Mas é uma limitação: em outro
  simulador, elas precisariam ser recalculadas.
- **"Por que o ajuste de C e gamma não ajudou?"** O padrão do scikit-learn já estava numa região boa. A grade mostra que
  só gamma alto (0,5) piora, por sobreajuste.
- **"Qual o maior problema restante?"** Duelos em que os dois nocauteiam com 1 golpe (13% de erro): depende de quem ataca
  primeiro. A próxima feature é "quem derruba primeiro".
