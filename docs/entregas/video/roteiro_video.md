# Roteiro do vídeo demonstrativo (1 a 3 minutos)

Duração-alvo: **cerca de 2 min 20 s**. Formato sugerido: gravação da tela com narração.

## Antes de gravar
- Inicie o jogo com `jogar.bat` e deixe **duas janelas** prontas: uma normal (jogador 1) e uma **anônima** (jogador 2),
  ou use um celular como segundo jogador.
- Gravação de tela no Windows: **Win + Alt + R** (Xbox Game Bar) ou o OBS Studio. No celular, use o gravador de tela.
- Feche abas e notificações. Use zoom de 110% a 125% no navegador para o texto ficar legível.
- Ensaiem uma vez: a batalha é sorteada, então o resultado pode mudar de uma gravação para outra.
- Confronto sugerido: **Pikachu × Gyarados**. É rápido e mostra a IA errando, o que rende a explicação mais interessante.

## Roteiro
| Tempo | O que aparece na tela | Narração |
|---|---|---|
| **0–10 s** · Problema | Card 1 do Instagram ou a tela inicial da Arena | "São mais de mil Pokémon e centenas de milhares de confrontos possíveis. Antes da batalha, dá para saber quem vai vencer? Nós ensinamos uma IA a fazer essa aposta." |
| **10–30 s** · Ideia da solução | Card 4 (a "rua" do SVM) e card 3 (os dados) | "Criamos um simulador com a fórmula de dano dos jogos e geramos 40 mil confrontos. Com eles, treinamos um SVM, uma técnica que traça a fronteira mais larga possível entre as batalhas que um lado vence e as que o outro vence. O teste usa só Pokémon que a IA nunca viu." |
| **30–55 s** · Protótipo: escolha | Criar sala, mostrar o link, o segundo jogador entrando, a busca, a **roleta** e o botão Pronto | "Esta é a Arena SVM. Um jogador cria a sala e o outro entra pelo link, na mesma rede. Cada um escolhe um Pokémon de qualquer geração, ou gira a roleta." |
| **55–80 s** · Protótipo: batalha | A previsão da IA, a animação da batalha e o resultado | "Antes da luta, a IA aposta no favorito. A batalha acontece com os golpes reais de cada Pokémon. No fim, o jogo mostra se a IA acertou esta batalha e se acertou o favorito." |
| **80–100 s** · Protótipo: explicação | Abrir os tópicos 1, 2 e 4 da explicação | "E a IA explica a aposta: onde a batalha ficou em relação à fronteira e à margem, o que mais pesou e quais batalhas do treino, os vetores de suporte, mais influenciaram." |
| **100–125 s** · Resultado e limitação | Card 5 (gráfico) ou o gráfico final do notebook 02 | "No teste, a IA acertou o favorito em 92,6% das batalhas, contra 68% da regra do mais rápido. O que mais ajudou foi informar os golpes de cada Pokémon. A limitação: nosso simulador é mais simples que o jogo real, e a IA erra quando a sorte decide." |
| **Final (125–140 s)** | Card 6 com o QR Code e os nomes do grupo | "O código, os dados e o jogo estão no GitHub. Aponte a câmera para o QR Code e teste. Projeto de Inteligência Artificial II, Ciência da Computação, FIB." |

## Checklist do vídeo
- [ ] Tem entre 1 e 3 minutos.
- [ ] Mostra o problema, o protótipo funcionando e o principal resultado ou limitação.
- [ ] O QR Code aparece por pelo menos 5 segundos (e foi testado com um celular).
- [ ] O áudio está claro e o texto da tela está legível.
- [ ] O link do vídeo foi colocado no README do repositório.
