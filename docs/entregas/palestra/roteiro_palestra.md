# Roteiro da palestra: Arena SVM (cerca de 30 minutos + perguntas)

Cada integrante fala por **5 a 7 minutos**. A divisão abaixo é uma sugestão (segue a ordem do Checkpoint 1); dá para
trocar os nomes à vontade, mas **todos devem saber explicar o projeto inteiro**, porque o professor pode perguntar
a qualquer um.

| Tempo | Quem | Parte | Cobre do pedido do professor |
|---|---|---|---|
| 0–4 min | **Alceu** | Abertura e problema | Problema, analogia de abertura |
| 4–9 min | **Luan** | Dados e simulador | Dataset, vazamento, escala |
| 9–14 min | **Anthony** | A ideia do SVM, sem fórmula | Analogia da rua, linear × não linear (intuição) |
| 14–20 min | **Lucas** | Experimentos, comparação e erros | ≥ 3 experimentos, KNN e regressão logística, ≥ 3 erros |
| 20–28 min | **Gustavo** | Protótipo, explicação técnica e Demo Challenge | Explicação técnica (margem, C, kernel, gamma), construtor de personagem, classe prevista, fronteira |
| 28–30 min | **Alceu** | Conclusão e limitações | Limitações, ética |
| depois | todos | Perguntas | |

---

## 1. Alceu: abertura e problema (0–4 min)
**Na tela:** capa dos slides ou card 1 do Instagram (Pikachu × Gyarados).

- **Gancho:** "Quem aqui já jogou Pokémon? Charizard contra Blastoise: quem ganha?" (deixe a plateia responder).
  Charizard é mais rápido, Blastoise tem vantagem de tipo. Não é óbvio.
- **O problema:** são **1.242 Pokémon** e mais de **770 mil confrontos** possíveis. As regras de bolso erram muito:
  "vence o mais rápido" acerta só **68%**; "vence o mais forte" (soma dos atributos), **81%**.
- **A pergunta do projeto:** um SVM, olhando só o que se sabe **antes** da luta, prevê o favorito melhor que essas
  regras, mesmo com Pokémon que **nunca viu**?
- **Analogia de abertura:** "É como um comentarista esportivo que, antes do jogo, olha as estatísticas dos dois
  times e aposta no favorito. Só que o nosso comentarista estudou 30 mil partidas."
- **Passagem:** "Mas para a IA aprender, precisávamos de muitas batalhas. O Luan explica de onde elas vieram."

## 2. Luan: dados e simulador (4–9 min)
**Na tela:** card 3, diagrama do pipeline ou o notebook 01.

- **Fonte:** PokéAPI (dados oficiais dos jogos, licença aberta): atributos, tipos e golpes de 1.242 Pokémon das
  9 gerações. Removemos formas repetidas e cosméticas.
- **Por que um simulador próprio:** o dataset público de batalhas cobre só 6 gerações e não explica como foi gerado.
  Nosso simulador usa a **fórmula de dano** dos jogos, nível 50, golpes que cada Pokémon realmente aprende,
  precisão, prioridade, críticos.
- **Sorte:** cada confronto foi simulado **21 vezes**; o rótulo é quem venceu a **maioria**. Foram **40 mil
  confrontos**, classes equilibradas (~50%).
- **Vazamento de dados (ponto importante):** treino só com Pokémon das **gerações 1 a 6** (30 mil batalhas) e teste
  só com as **gerações 7 a 9** (6 mil), sem nenhum Pokémon em comum. Assim medimos se a IA aprendeu, e não se decorou.
- **As 15 variáveis:** diferença dos 6 atributos, eficácia de tipo de cada lado e, dos golpes: fração do HP tirada
  por turno, golpes para o nocaute e golpe de prioridade.
- **Escala:** os números têm faixas diferentes, então padronizamos (StandardScaler, ajustado só no treino).
- **Passagem:** "Com os dados prontos, como o SVM decide? O Anthony mostra por dentro."

## 3. Anthony: a ideia do SVM, sem fórmula (9–14 min)
**Na tela:** card 4 (a rua com os pontos vermelhos e azuis).

A ideia aqui é **explicar com imagens e exemplos do dia a dia**, sem termos técnicos. Os detalhes (C, gamma, score)
ficam para o Gustavo mostrar no protótipo.

- **Cada batalha vira um ponto:** "Imagine que cada batalha é um ponto num mapa. Pontos vermelhos: batalhas que o
  primeiro Pokémon venceu. Azuis: que ele perdeu."
- **A rua mais larga:** o SVM procura a linha que separa os dois grupos deixando **a maior folga possível** dos dois
  lados, como uma rua larga entre dois bairros. Uma rua estreita, colada nas casas, erraria fácil com uma casa nova.
- **Quem decide são os da beira:** só os pontos encostados na calçada (os **vetores de suporte**) definem onde a rua
  passa. Os pontos lá no fundo do bairro poderiam sumir que nada mudaria. "É como um time: quem define a linha de
  impedimento é o último zagueiro, não o goleiro."
- **Longe da rua = certeza; perto = dúvida:** batalha bem dentro do bairro vermelho é aposta segura; perto da rua, é
  quase cara ou coroa.
- **E quando a rua não pode ser reta?** Às vezes os bairros se misturam de um jeito que nenhuma linha reta separa.
  Aí o SVM usa um "truque" (o **kernel**) que deixa a rua **fazer curvas**.
- **Com o que comparamos:** com chutar sempre o mesmo lado (51%), com as regras de bolso (68% e 81%) e com outros dois
  algoritmos, que o Lucas vai mostrar.
- **Passagem:** "E funcionou? O Lucas mostra os experimentos."

## 4. Lucas: experimentos, comparação e erros (14–20 min)
**Na tela:** card 5 (barras + comparação), gráficos do notebook 02/03 ou a Ficha de Experimentos.

- **Protocolo:** hipóteses registradas **antes** de rodar; treino gerações 1–6, teste 7–9.
- **E1 (kernel):** com 8 variáveis (atributos e tipos), SVM RBF 86,6% × modelo linear (regressão logística) 85,6%:
  ganho pequeno do não linear.
- **E2 (golpes):** incluir as variáveis de golpes levou o SVM a **92,6%** (AUC 0,977). **Foi o maior ganho**:
  informação certa vale mais que trocar o algoritmo.
- **E3 (C e gamma):** ajustar os hiperparâmetros não trouxe ganho mensurável.
- **E4 (vazamento):** esperávamos que a divisão aleatória inflasse o resultado, mas deu 92,5%. Hipótese refutada: as
  variáveis descrevem a batalha de forma relativa, então o modelo aprende regras gerais, e não "rostos".
- **E6 (comparação):** com as mesmas 15 variáveis: **SVM 92,6%**, regressão logística 91,8%, KNN (k = 91) 91,1%.
  Sem padronizar, o **KNN cai para 81,5%**, o SVM para 90,4% e a logística fica igual.
- **E5 (erros, 7,3%):** quase todos onde a **sorte** decide. Nos confrontos equilibrados (favorito vence entre 30% e
  70% das simulações) o erro é de 31%. Três casos:
  1. **Zacian × Kleavor:** golpe forte que **custa HP** a quem usa; o modelo não enxerga esse custo.
  2. **Marshadow × Lokix:** golpe que **baixa a própria defesa**; o atacante fica frágil depois.
  3. **Nickit × Calyrex-Shadow:** golpe de **prioridade 4× efetivo**: o "azarão" ataca primeiro e vence.
- **Passagem:** "Tudo isso pode ser visto e testado no nosso protótipo. O Gustavo mostra ao vivo."

## 5. Gustavo: protótipo, explicação técnica e Demo Challenge (20–28 min)
**Na tela:** https://arena-svm.onrender.com (abra uns minutos antes para o servidor acordar).

Aqui entra a parte técnica, **mostrando na tela** cada conceito que o Anthony explicou com a analogia.

- **Arena (2 min):** criar sala, mostrar o **QR Code da sala**, alguém entra pelo celular. Escolher os Pokémon,
  mostrar a **previsão da IA** (classe prevista), a batalha e a explicação.
- **A parte técnica, na explicação do jogo (2 min):**
  - **Score = distância até a fronteira** (`decision_function`). Na régua, entre −1 e +1 a batalha está **dentro da
    margem**: é a "batalha perto da rua", aposta incerta.
  - **Vetores de suporte:** o jogo mostra as batalhas do treino que mais pesaram. No modelo são **5.805 de 30 mil**
    (cada uma "vota" com peso α·y·K).
  - **Margem suave (C = 10):** como existe sorte, os grupos se misturam; o C diz o quanto o SVM aceita errar no treino
    para manter a rua larga. C alto = menos tolerante.
  - **Kernel RBF e gamma (0,05):** o kernel mede a semelhança entre duas batalhas; o gamma controla o quanto a
    fronteira pode se curvar. Gamma alto demais = decora o treino.
  - **Escala:** o RBF usa distâncias, por isso padronizamos (StandardScaler).
- **Laboratório (1 min):** montar um personagem (construtor), mexer em velocidade e ataque e mostrar o ponto
  cruzando a **linha amarela** (fronteira) e as tracejadas (margem). "Vejam: a fronteira é curva, é o kernel RBF."
- **Demo Challenge (3 min):** desafio à plateia: "Quem consegue montar um personagem com **total de atributos
  menor** que o do adversário, mas que a IA aposta que vence?" Alguém escaneia o QR do folder, ou sobe para usar o
  computador. Comentar o resultado com a fronteira na tela: o que fez o ponto cruzar a linha amarela?
  (Ensaiem antes para ter um exemplo pronto, caso ninguém da plateia queira participar.)
- **Passagem:** "Para fechar, o Alceu volta com a resposta à nossa pergunta."

## 6. Alceu: conclusão e limitações (28–30 min)
- **Resposta à pergunta:** sim. O SVM acertou **92,6%** em Pokémon nunca vistos, contra 68% e 81% das regras simples.
- **Lição principal:** as variáveis importaram mais que o algoritmo ou o ajuste fino.
- **Limitações:** o simulador não tem habilidades, itens, golpes de status nem trocas; a IA aprende as regras do
  simulador e **não serve para prever partidas competitivas**. A sorte impõe um teto ao acerto.
- **Uso responsável:** está no Model Card (uso didático; Pokémon é marca da Nintendo/Game Freak/Creatures).
- **Fechamento:** "Testem no QR Code do folder e sigam @arena.svm. Obrigado!"

---

## Perguntas prováveis (e quem responde)
| Pergunta | Quem | Resposta curta |
|---|---|---|
| Por que SVM e não uma rede neural? | Gustavo | O tema pedia SVM; com 15 variáveis e 30 mil exemplos ele é forte, e a margem/vetores de suporte permitem explicar a decisão. |
| Os dados são reais? | Luan | Os atributos, tipos e golpes sim (PokéAPI); as batalhas são simuladas, com a fórmula de dano do jogo. |
| Como evitaram vazamento? | Luan | Treino e teste com gerações diferentes, nenhum Pokémon em comum; o scaler é ajustado só no treino. |
| O que são os vetores de suporte? | Anthony | Os pontos na beira da rua: só eles definem a fronteira. |
| Por que a diferença para a regressão logística é pequena? | Lucas | A separação é quase linear depois das variáveis de golpes; o RBF ganha nas interações (velocidade × nocaute). |
| O que é o score que aparece no jogo? | Gustavo | A distância (com sinal) até a fronteira; entre −1 e +1 a batalha está dentro da margem, é incerta. |
| Por que o KNN caiu sem padronizar? | Lucas | Ele decide por distância; sem escala, as variáveis de valores grandes dominam o cálculo. |
| O que fariam a seguir? | Alceu | Simular habilidades e itens e criar uma variável que combine velocidade, prioridade e nocaute. |

## Checklist antes da palestra
- [ ] Slides prontos (podem reaproveitar os cards do Instagram e os gráficos dos notebooks).
- [ ] Site aberto uns minutos antes (o Render "dorme").
- [ ] Um celular de teste já com a sala aberta, caso a internet falhe.
- [ ] Folders impressos para a plateia escanear o QR.
- [ ] Ensaio cronometrado: cada um dentro do seu tempo.
