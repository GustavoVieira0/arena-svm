# Falas da palestra: o que cada integrante diz

Apresentação: [`Arena_SVM_Palestra.pptx`](Arena_SVM_Palestra.pptx) (17 slides, cerca de 30 minutos). As mesmas falas
estão nas **anotações** de cada slide (no PowerPoint: Apresentação de Slides → Usar o Modo de Exibição do Apresentador).

Não precisa decorar palavra por palavra: o texto é um guia. O importante é falar com as próprias palavras e manter o
tempo. Cada slide mostra no canto superior direito o nome de quem fala.

---

## Alceu: abertura e problema (slides 1 a 3 · 0:00 a 4:00)

**Slide 1 (capa).** "Boa tarde! Nós somos o grupo da Arena SVM: Alceu, Anthony, Gustavo, Luan e Lucas. Nosso projeto
tenta responder uma pergunta simples: dá para uma inteligência artificial prever quem vence uma batalha Pokémon antes
de ela começar?"

**Slide 2 (Charizard ou Blastoise).** "Vamos começar com vocês. Charizard contra Blastoise: quem ganha? Quem acha
Charizard levanta a mão... e Blastoise? O Charizard é mais rápido, ataca primeiro. O Blastoise tem vantagem de tipo:
água contra fogo. Não é óbvio. E esse é só um confronto entre centenas de milhares."

**Slide 3 (regras de bolso).** "São 1.242 Pokémon e mais de 770 mil confrontos possíveis. A primeira ideia é usar uma
regra simples. 'O mais rápido vence'? Acerta só 68% das vezes. 'O mais forte vence', somando os atributos? 81%. Ainda
erra uma batalha em cada cinco.

É como um comentarista esportivo que, antes do jogo, olha as estatísticas dos dois times e aposta no favorito. A nossa
pergunta foi: um comentarista que estudou 30 mil partidas, no caso um SVM, acerta mais que essas regras? E acerta com
Pokémon que ele nunca viu?

Mas para a IA aprender, precisávamos de muitas batalhas. O Luan explica de onde elas vieram."

---

## Luan: dados e simulador (slides 4 e 5 · 4:00 a 9:00)

**Slide 4 (de onde vieram as batalhas).** "Os dados dos Pokémon vêm da PokéAPI, uma base aberta com os atributos, os
tipos e os golpes de todos os 1.242 Pokémon.

Existe um conjunto pronto de batalhas na internet, mas ele só tem seis gerações e não explica como foi gerado. Por
isso construímos o nosso próprio simulador. Ele usa a fórmula de dano dos jogos, com todos no nível 50, e cada
Pokémon luta com os golpes que ele realmente aprende.

Batalha tem sorte: golpe crítico, ataque que erra, variação de dano. Então cada confronto foi simulado 21 vezes, e o
favorito é quem venceu a maioria. No total, foram 40 mil confrontos."

**Slide 5 (sem trapaça).** "Aqui tem um cuidado muito importante. Se a gente testasse a IA com Pokémon que ela já viu
no treino, ela poderia simplesmente decorar. Isso se chama vazamento de dados.

Então separamos: o treino usa só Pokémon das gerações 1 a 6, são 30 mil batalhas. A prova usa só as gerações 7 a 9,
6 mil batalhas. Nenhum Pokémon aparece nos dois. É como estudar com a lista de exercícios e fazer a prova com
questões novas.

Para cada batalha, a IA recebe 15 números: a diferença entre os atributos dos dois, a vantagem de tipo de cada lado e
informações dos golpes, como quantos golpes são necessários para nocautear o adversário.

Esses números têm escalas bem diferentes, então colocamos todos na mesma escala. Guardem isso, porque vai fazer
diferença mais à frente.

Com os dados prontos: como o SVM decide? O Anthony explica."

---

## Anthony: a ideia do SVM, sem fórmula (slides 6 e 7 · 9:00 a 14:00)

**Slide 6 (a rua mais larga).** "Vou explicar o SVM sem nenhuma fórmula, só com este desenho.

Imaginem que cada batalha é um ponto num mapa. Os pontos vermelhos são batalhas em que o primeiro Pokémon venceu, e os
azuis, batalhas em que ele perdeu.

O SVM procura a linha que separa os dois grupos deixando a maior folga possível dos dois lados. É como construir a rua
mais larga possível entre dois bairros. Por que larga? Porque uma rua estreita, colada nas casas, erraria fácil
quando chegasse uma casa nova.

E quando aparece uma batalha nova, a IA só olha de que lado da rua ela caiu."

**Slide 7 (os pontos da beira).** "Tem um detalhe interessante: só os pontos que encostam na calçada decidem onde a rua
passa. Eles se chamam vetores de suporte, são os circulados no desenho. Os pontos lá no fundo do bairro poderiam
sumir, e a rua continuaria no mesmo lugar. É como no futebol: quem define a linha de impedimento é o último zagueiro,
não o goleiro.

Segundo: quanto mais longe da rua, mais certa é a aposta. Uma batalha perto da rua é quase cara ou coroa.

E terceiro: às vezes os bairros se misturam de um jeito que nenhuma linha reta consegue separar. Aí o SVM usa um
truque, chamado kernel, que deixa a rua fazer curvas.

Para saber se isso funciona, comparamos com chutar sempre o mesmo lado, que dá 51%, com as regras de bolso e com
outros dois algoritmos. E funcionou? O Lucas mostra os experimentos."

---

## Lucas: experimentos, comparação e erros (slides 8 a 11 · 14:00 a 20:00)

**Slide 8 (92,6%).** "Este é o resultado principal. As regras de bolso acertam 68% e 81%. O SVM usando só atributos e
tipos chegou a 86,6%. Quando incluímos as informações dos golpes de cada Pokémon, ele foi para 92,6%, e lembrando:
com Pokémon que ele nunca tinha visto.

A maior lição do projeto está aqui: o que mais ajudou não foi mexer no algoritmo, foi dar a ele a informação certa."

**Slide 9 (cinco experimentos).** "Fizemos cinco experimentos controlados, e as hipóteses foram registradas antes de
rodar, para a gente não ajustar a conclusão depois.

No E1, comparamos a rua curva com a rua reta: a curva ganhou, mas por pouco, 86,6% contra 85,6%. No E2, incluímos os
golpes: foi o grande salto. No E3, ajustamos os parâmetros do SVM, e não mudou nada que desse para medir.

O E4 foi o mais curioso. A gente achava que, se embaralhasse treino e teste, misturando as gerações, o resultado ia
inflar. Não inflou: deu 92,5%. Isso mostra que a IA aprendeu regras gerais de batalha, e não decorou Pokémon.
A hipótese foi refutada, e isso também é um resultado."

**Slide 10 (SVM × regressão logística × KNN).** "No E6, comparamos o SVM com outros dois algoritmos, usando exatamente
as mesmas 15 informações. O SVM ficou com 92,6%, a regressão logística com 91,8% e o KNN com 91,1%. O SVM ganhou, mas
por pouco: de novo, as variáveis pesam mais que o algoritmo.

E vejam a barra cinza: é o resultado sem colocar os números na mesma escala. O KNN despenca para 81,5%. Ele decide
pela distância entre batalhas, então um atributo com números grandes domina o cálculo. O SVM também usa distância e
cai um pouco. A regressão logística não muda."

**Slide 11 (onde a IA erra).** "A IA erra 7,3% das batalhas. E quase todos os erros estão nas batalhas equilibradas,
em que a sorte decide: nelas, o erro sobe para 31%.

Três exemplos. Zacian contra Kleavor: um golpe forte que custa vida a quem usa, e a IA não enxerga esse custo.
Marshadow contra Lokix: um golpe que baixa a própria defesa, e o atacante fica frágil depois. E Nickit contra
Calyrex-Shadow: o azarão tem um golpe de prioridade super efetivo, ataca primeiro e vence.

Em comum: são detalhes dos golpes que as nossas 15 informações não capturam.

Tudo isso dá para ver e testar no nosso protótipo. O Gustavo mostra ao vivo."

---

## Gustavo: protótipo, explicação técnica e Demo Challenge (slides 12 a 15 · 20:00 a 28:00)

**Slide 12 (ao vivo).** "Este QR Code abre o jogo, e quem quiser pode jogar junto. Vou mostrar três partes: a Arena, a
explicação da IA e o Laboratório."

> Trocar para o navegador (Alt+Tab), com o site já aberto. O slide 13 é só um guia, não precisa mostrar.

**No site: Arena.** "Eu crio uma sala, e aparece este QR Code. Meu colega aponta a câmera do celular e já entra. Cada
um escolhe um Pokémon, ou gira a roleta. Antes da luta, a IA mostra em quem ela aposta. E a batalha acontece com os
golpes reais de cada Pokémon."

**No site: explicação técnica (slide 14, se a internet falhar).** "O Anthony explicou a rua; agora dá para ver a rua
funcionando. Este score é a distância da batalha até a fronteira. Entre −1 e +1, a batalha está dentro da margem: é
aquela batalha perto da rua, uma aposta incerta.

Aqui estão os vetores de suporte. Das 30 mil batalhas do treino, 5.805 ficaram na beira da rua, e o jogo mostra quais
delas mais pesaram nesta decisão.

Dois parâmetros controlam a rua. O C diz quanto o SVM aceita errar no treino para manter a rua larga: como existe
sorte, os grupos se misturam um pouco, e usamos C igual a 10. E o gamma do kernel RBF controla o quanto a rua pode
curvar: usamos 0,05. Um gamma alto demais faria a IA decorar o treino.

E como o kernel RBF mede distâncias, colocar os números na mesma escala é obrigatório, como o Lucas mostrou com o KNN."

**No site: Laboratório (slide 15).** "No Laboratório, qualquer um cria o seu próprio personagem. Vejam: se eu aumento
a velocidade, o ponto branco anda no mapa, e quando ele cruza a linha amarela, a IA muda de aposta. Essa linha é a
fronteira de decisão do SVM, e ela é curva por causa do kernel RBF. As linhas tracejadas são a margem."

**Demo Challenge.** "Agora um desafio para vocês: quem consegue montar um personagem com total de atributos menor que
o do adversário, mas que a IA aposte que vence? Pode ser pelo celular, pelo QR Code, ou aqui no computador."

> Comentar o resultado com a fronteira na tela: o que fez o ponto cruzar a linha? Ter um exemplo ensaiado, caso
> ninguém queira participar.

"Para fechar, o Alceu volta com a resposta à nossa pergunta."

---

## Alceu: conclusão (slides 16 e 17 · 28:00 a 30:00)

**Slide 16 (respondendo à pergunta).** "Voltando à pergunta do começo: sim. O SVM acerta o favorito em 92,6% das
batalhas entre Pokémon que ele nunca viu, bem acima dos 68% e 81% das regras de bolso.

A principal lição: dar a informação certa para a IA importou mais do que trocar ou ajustar o algoritmo.

E as limitações: o nosso simulador é mais simples que o jogo real, não tem habilidades, itens nem trocas de Pokémon.
A IA aprende as regras do simulador, então ela não serve para prever partidas competitivas. E a sorte impõe um limite:
algumas batalhas são realmente cara ou coroa."

**Slide 17 (obrigado).** "Testem pelo QR Code e sigam o @arena.svm no Instagram. Muito obrigado! Ficamos à disposição
para perguntas."

---

## Perguntas prováveis (e quem responde)
| Pergunta | Quem | Resposta curta |
|---|---|---|
| Por que SVM e não uma rede neural? | Gustavo | O tema pedia SVM; com 15 variáveis e 30 mil exemplos ele é forte, e a margem e os vetores de suporte permitem explicar a decisão. |
| Os dados são reais? | Luan | Os atributos, tipos e golpes sim (PokéAPI); as batalhas são simuladas com a fórmula de dano do jogo. |
| Como evitaram vazamento? | Luan | Gerações diferentes no treino e no teste, sem Pokémon em comum; a padronização é calculada só no treino. |
| O que são vetores de suporte? | Anthony | Os pontos na beira da rua: só eles definem onde a fronteira passa. |
| Por que a diferença para a regressão logística é pequena? | Lucas | Com as variáveis de golpes, a separação fica quase linear; o kernel ganha nas combinações (por exemplo, velocidade e nocaute). |
| Por que o KNN caiu sem padronizar? | Lucas | Ele decide por distância; sem escala, as variáveis com valores grandes dominam. |
| O que fariam a seguir? | Alceu | Simular habilidades e itens e criar uma variável que junte velocidade, prioridade e nocaute. |

## Antes do dia
- [ ] Cada um ler a sua parte em voz alta e cronometrar (a meta é ficar dentro do tempo da tabela).
- [ ] Um ensaio completo com a apresentação e o site.
- [ ] Abrir o site uns 5 minutos antes (o servidor gratuito "dorme").
- [ ] Um celular pronto para entrar na sala durante a demonstração.
- [ ] Ensaiar um exemplo para o Demo Challenge.
