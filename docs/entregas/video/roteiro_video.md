# Roteiro do vídeo demonstrativo (1 a 3 minutos)

Duração-alvo: **cerca de 2 min 45 s**. Formato sugerido: gravação da tela com narração (pode ser uma pessoa só narrando,
ou dividir os trechos entre o grupo).

## Antes de gravar
- Abra **https://arena-svm.onrender.com** uns 2 minutos antes, para o servidor "acordar".
- Deixe **duas janelas** prontas: uma normal (jogador 1) e uma **anônima** (jogador 2). Também dá para usar um celular
  como segundo jogador, entrando pelo **QR Code da sala**, o que fica ótimo no vídeo.
- Deixe aberta também uma aba no **Laboratório** (https://arena-svm.onrender.com/laboratorio).
- Gravação de tela no Windows: **Win + Alt + R** (Xbox Game Bar) ou o OBS Studio. No celular, use o gravador de tela.
- Feche abas e notificações. Use zoom de 110% a 125% no navegador para o texto ficar legível.
- Ensaiem uma vez: a batalha é sorteada, então o resultado pode mudar de uma gravação para outra.
- Confronto sugerido: **Pikachu × Gyarados**. É rápido e pode mostrar a IA errando, o que rende a explicação mais
  interessante.

## Roteiro
| Tempo | O que aparece na tela | Narração |
|---|---|---|
| **0–10 s** · Problema | Card 1 do Instagram ou a tela inicial da Arena | "São mais de mil Pokémon e centenas de milhares de confrontos possíveis. Antes da batalha, dá para saber quem vai vencer? Nós ensinamos uma IA a fazer essa aposta." |
| **10–30 s** · Ideia da solução | Card 3 (os dados) e card 4 (a "rua" do SVM) | "Criamos um simulador com a fórmula de dano dos jogos e geramos 40 mil confrontos. Com eles, treinamos um SVM, uma técnica que traça a rua mais larga possível entre as batalhas que um lado vence e as que o outro vence. O teste usa só Pokémon que a IA nunca viu." |
| **30–50 s** · Protótipo: sala | Criar sala, mostrar o **QR Code da sala**, o celular escaneando e entrando direto; depois a busca, a **roleta** e o botão Pronto | "Esta é a Arena SVM, que está online. Um jogador cria a sala e o outro entra pelo link ou apontando a câmera para o QR Code. Cada um escolhe um Pokémon de qualquer geração, ou gira a roleta." |
| **50–70 s** · Protótipo: batalha | A previsão da IA, a animação da batalha e o resultado | "Antes da luta, a IA aposta no favorito. A batalha acontece com os golpes reais de cada Pokémon. No fim, o jogo mostra se a IA acertou esta batalha e se acertou o favorito." |
| **70–90 s** · Protótipo: explicação | Abrir os tópicos da explicação: régua da margem, o que mais pesou e os vetores de suporte | "E a IA explica a aposta: onde a batalha ficou em relação à fronteira e à margem, o que mais pesou e quais batalhas do treino, os vetores de suporte, mais influenciaram." |
| **90–115 s** · Laboratório | Montar um personagem: mexer no slider de **Velocidade** e de **Ataque** e mostrar o ponto branco atravessando a linha amarela no gráfico da fronteira | "No Laboratório, você cria o seu próprio personagem. Ao aumentar a velocidade ou o ataque, o ponto anda no mapa e, quando cruza a linha amarela, a IA muda de aposta. Essa linha é a fronteira de decisão do SVM, e ela é curva por causa do kernel RBF." |
| **115–145 s** · Resultado e comparação | Card 5 (gráfico de barras e comparação com KNN e regressão logística) | "No teste, a IA acertou o favorito em 92,6% das batalhas, contra 68% da regra do mais rápido. Comparamos com outros algoritmos: a regressão logística chegou a 91,8% e o KNN, a 91,1%. A maior lição: o que mais ajudou não foi trocar o algoritmo, mas informar os golpes de cada Pokémon. E sem padronizar os dados, o KNN caiu para 81,5%." |
| **145–160 s** · Limitação | Card 6 (onde ela erra) | "A limitação: nosso simulador é mais simples que o jogo real, e a IA erra quando a sorte decide a batalha." |
| **Final (160–170 s)** | Card 6 com o QR Code, o @arena.svm e os nomes do grupo | "Aponte a câmera para o QR Code e desafie um amigo. Siga @arena.svm. Projeto de Inteligência Artificial II, Ciência da Computação, FIB." |

## Checklist do vídeo
- [ ] Tem entre 1 e 3 minutos (o roteiro dá cerca de 2 min 50 s; se passar, encurte a parte da batalha).
- [ ] Mostra o problema, o protótipo funcionando (sala, batalha, explicação e Laboratório) e o principal resultado.
- [ ] Mostra a comparação com KNN e regressão logística.
- [ ] O QR Code aparece por pelo menos 5 segundos (e foi testado com um celular).
- [ ] O áudio está claro e o texto da tela está legível.
- [ ] O link do vídeo foi colocado no README do repositório.
