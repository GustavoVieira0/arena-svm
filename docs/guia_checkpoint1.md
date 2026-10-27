# Guia do Checkpoint 1 (27/10): o que mostrar e onde está cada evidência

## Roteiro de 10 minutos
| Tempo | Quem (sugestão) | O que mostrar | Onde |
|---|---|---|---|
| 0–2 min | Alceu | **Problema e pergunta:** "Dá para prever o favorito de uma batalha entre Pokémon que o modelo nunca viu, melhor que regras simples?" | README / notebook, seção 1 |
| 2–4 min | Luan | **Dataset + 3 descobertas:** (1) o mais rápido vence só 70%; (2) o tipo pesa muito (82% × 18% nos extremos), mas golpes de cobertura reduzem a desvantagem; (3) 71% dos confrontos têm sempre o mesmo vencedor, e 5,7% são equilibrados (teto de acerto) | notebook, seções 2–3 |
| 4–6 min | Anthony | **Baseline e 1º resultado:** "vence o mais rápido" 67,8%, "maior Total" 80,6%, Regressão Logística 85,6%, **SVM 86,6%** | notebook, seções 5–6 |
| 6–8 min | Gustavo | **Pipeline ponta a ponta:** `montar_base.py` → `gerar_batalhas.py` → notebook "Run All" → modelo salvo | terminal + notebook |
| 8–10 min | Lucas | **Próximo passo (03/11):** E1 kernels, E2 features de golpes (o SVM erra Pikachu × Gyarados porque não sabe do Volt Tackle), E3 C/gamma, E4 efeito do vazamento + demo `batalhar.py` | notebook, seção 8 |

> O professor pode perguntar a **qualquer integrante**. Todos devem saber explicar o projeto inteiro.

## Mapa do checklist → evidência
| Item | Evidência |
|---|---|
| **Entregas** | GitHub (publicar!) · `docs/Resumo_Expandido_Rascunho.docx` · `docs/referencias.md` · este guia · `docs/diario_ia.md` |
| **A. Problema** | Seção 1 do notebook e README: problema, usuário (jogadores/fãs, app de 2 jogadores) e pergunta comparativa (SVM × regras simples, em Pokémon nunca vistos) |
| **B. Dataset** | Fonte rastreável (PokéAPI + simulador com golpes reais e seed). 1.242 Pokémon × 18 colunas; 40.000 confrontos × 6 colunas. Ausentes: só `Type 2` (esperado). Duplicatas/formas cosméticas removidas (109). Outliers: Shedinja (HP 1), Blissey, Megas. Classes equilibradas (~50%). Escala: StandardScaler. **Vazamento:** divisão por geração, 0 Pokémon em comum |
| **C. EDA** | 4 gráficos, cada um com uma pergunta no título; 5 descobertas interpretadas no fim da seção 3 |
| **D. Preparação** | Limpeza justificada em `montar_base.py`; tipos (categóricos) transformados em multiplicador de eficácia; scaler dentro do Pipeline (ajustado só no treino) |
| **E. Baseline** | 4 baselines com justificativa (tabela da seção 5) + métricas (acurácia, F1, ROC-AUC) |
| **F. Pipeline** | Executa sem edição manual; seed fixa; `requirements.txt`; parâmetros no README |
| **G. GitHub** | README completo; nomes organizados; dados versionados (licença permite); sem chaves/senhas |
| **H. Referências** | 9 referências (5 artigos/relatórios técnicos) com a contribuição de cada uma; citadas no resumo |
| **I. Divisão** | Tabela no README |
| **J. Diário de IA** | `docs/diario_ia.md` |

## Pendências do grupo antes de terça
- [ ] **Criar o repositório no GitHub e fazer o push** (instruções abaixo); deixar público ou adicionar o professor.
- [ ] **Cada integrante fazer pelo menos um commit** (ex.: revisar uma seção, ajustar o README ou o diário). O professor
      olha a participação no histórico.
- [ ] Todos rodarem o notebook na própria máquina pelo menos uma vez.
- [ ] Ler as referências 1 e 3 (Cortes e Vapnik; Kaufman et al.) para saber explicar a contribuição delas.
- [ ] Revisar o resumo expandido e passar para o template oficial da Jornada Científica, se houver.
- [ ] Cada um acrescentar seus próprios registros no Diário de IA.

## Publicar no GitHub
1. No github.com, crie um repositório **vazio** chamado `arena-svm` (sem README, sem .gitignore).
2. Na pasta do projeto:
```bash
git remote add origin https://github.com/<usuario>/arena-svm.git
git push -u origin main
```
3. Em *Settings → Collaborators*, adicione os outros integrantes (e o professor, se o repositório for privado).

## Perguntas prováveis (e respostas curtas)
- **"Por que gerar o próprio dataset?"** O público cobre só as gerações 1–6, e as regras dele são desconhecidas. O nosso usa
  a fórmula de dano oficial e os golpes que cada Pokémon realmente aprende, tem regras documentadas e cobre as 9 gerações.
- **"Os golpes são reais?"** Sim: vêm da lista oficial de golpes aprendidos (PokéAPI), com poder, precisão, prioridade e
  efeitos. Ficam de fora habilidades, itens e golpes de status.
- **"Então o modelo não está só reaprendendo a regra de vocês?"** Ele recebe só atributos e tipos, não a fórmula nem a
  sorte. A pergunta é se o SVM consegue aproximar o resultado de um processo não linear e com aleatoriedade, em Pokémon
  nunca vistos. Regras simples como "o mais rápido vence" acertam só 68%.
- **"Como evitaram vazamento?"** Treino com gerações 1–6 e teste com 7–9. Nenhum Pokémon aparece nos dois.
- **"Por que acurácia?"** As classes estão equilibradas (cerca de 50%). Usamos também F1 e ROC-AUC.
- **"O SVM é muito melhor que a Regressão Logística?"** Ainda não: 86,6% contra 85,6%. Investigar se a não linearidade
  compensa é exatamente o experimento E1 do próximo checkpoint.
- **"Por que caiu de 92% para 87% com golpes reais?"** O modelo só vê atributos e tipos, não os golpes. Um Pokémon com
  um golpe de cobertura ou muito forte (Volt Tackle, Overheat) surpreende o modelo. Incluir isso é o experimento E2.
- **"Qual o teto de acerto?"** Cerca de 5,7% dos confrontos são equilibrados (A vence entre 30% e 70%). Nesses, nenhum
  modelo acerta sempre, e o SVM erra cerca de 47% deles, como esperado.
