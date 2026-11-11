# Entregas finais

| Entrega | Arquivo | Situação |
|---|---|---|
| Protótipo web | **https://arena-svm.onrender.com** (arena) e **/laboratorio** (construtor de personagem) · código em [`app/`](../../app) · local: `jogar.bat` | Pronto (online) |
| Repositório | [README principal](../../README.md) | Pronto |
| Resumo expandido (2 páginas) | [`../jornada/Resumo_Jornada_2026_Arena_SVM.pdf`](../jornada/Resumo_Jornada_2026_Arena_SVM.pdf) | Falta o e-mail do orientador |
| Folder (8 painéis, dobra em sanfona) | [`folder/Folder_Arena_SVM.pdf`](folder/Folder_Arena_SVM.pdf) | Pronto para imprimir |
| Instagram (carrossel) | [`instagram/`](instagram) · 6 cards + [`legenda.md`](instagram/legenda.md) | Pronto para postar |
| Vídeo (1 a 3 min) | [`video/roteiro_video.md`](video/roteiro_video.md) | Roteiro pronto; falta gravar |
| Model Card (1 página) | [`Model_Card.pdf`](Model_Card.pdf) · [`.docx`](Model_Card.docx) | Pronto |
| Ficha de experimentos | [`Ficha_de_Experimentos.pdf`](Ficha_de_Experimentos.pdf) · [`.docx`](Ficha_de_Experimentos.docx) | Pronto |
| Palestra (~30 min) | [`palestra/Arena_SVM_Palestra.pptx`](palestra/Arena_SVM_Palestra.pptx) · [falas](palestra/falas_por_integrante.md) · [roteiro](palestra/roteiro_palestra.md) | Pronto (falta ensaiar) |

## Como imprimir o folder
Papel A4, orientação **paisagem**, **frente e verso** com virada pela **borda curta**, escala 100% (sem "ajustar à página").
Depois, dobre em **sanfona (zigue-zague)** nas 3 linhas tracejadas, formando 4 partes de 7,4 cm:
a capa ("Uma IA consegue prever quem vence...") fica por fora na frente e o painel **Jogue agora!** (QR do jogo e do
Instagram @arena.svm) fica por fora atrás. Aberto, a frente conta o problema e como a IA aprende; o verso mostra a ideia
do SVM, o resultado (com KNN e regressão logística), o protótipo e quem fez.

## Como regerar o folder e os cards
`python docs/entregas/gerar_materiais.py` recria os arquivos HTML. Para converter, abra cada HTML no Chrome:
o folder com Imprimir → Salvar como PDF (margens "Nenhuma", com gráficos de plano de fundo), e os cards com uma captura
de 1080 × 1350 px.
