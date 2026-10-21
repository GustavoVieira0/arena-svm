# Diário de IA

Registro do uso de ferramentas de IA no projeto. **Não é avaliativo.** Serve para acompanhar como a IA foi usada e o que o
grupo verificou.

> **Para o grupo:** os registros abaixo foram iniciados a partir das sessões do Gustavo com o Claude. Cada integrante deve
> acrescentar as próprias interações (inclusive com outras ferramentas) e revisar se a descrição está fiel.

| Campo | Como preencher |
|---|---|
| Data | dd/mm/aaaa |
| Integrante | quem usou |
| Ferramenta / modelo | ex.: Claude Code (app desktop), modelo Claude Opus 5.5 |
| Prompt (resumo) | o que foi pedido |
| Uso da resposta | usada / modificada / descartada, e por quê |
| Verificação | como o grupo checou se a resposta estava correta |

---

### 06/10/2026: entendimento do tema e definição do projeto
- **Integrante:** Gustavo · **Ferramenta:** Claude Code (app desktop), Claude Opus 5.5
- **Prompts (resumo):** "Resumo do que é SVM"; "O tema sugerido foi arena de personagens, é boa ideia?"; "Preencha o
  canvas no modelo do professor"; "Quais outros projetos com SVM poderíamos fazer?"
- **Uso:** o resumo de SVM foi usado como estudo inicial. A IA sugeriu várias ideias (Pokémon lendário, duelo, Libras,
  pedra-papel-tesoura...) e **o grupo escolheu** a direção. O canvas foi gerado em Word e revisado pelo grupo antes da
  entrega.
- **Verificação:** conceitos de SVM conferidos com o material da disciplina e com Cortes e Vapnik (1995).

### 06/10/2026: análise dos datasets do Kaggle
- **Ferramenta:** Claude Code, Claude Opus 5.5 (executou scripts Python sobre os CSVs baixados pelo grupo).
- **Prompt:** "Analise as bases de Pokémon e Digimon que baixamos."
- **Uso:** identificou que dois arquivos de Pokémon eram a mesma base, que o `tests.csv` não tem rótulo e que há
  rótulos inconsistentes (Pokémon míticos). As descobertas foram usadas na escolha das bases.
- **Verificação:** contagens conferidas abrindo os CSVs; o caso Mew/Celebi/Manaphy foi conferido manualmente na base.

### 06/10/2026: protótipo de pedra-papel-tesoura (exploração descartada como tema)
- **Prompt:** "Monte o protótipo mínimo de pedra-papel-tesoura com SVM."
- **Uso:** protótipo funcional (MediaPipe + Flask + SVM) testado com a webcam. **Descartado como tema principal**; serviu
  para entender o fluxo coleta → treino → previsão em tempo real.
- **Verificação:** testado ao vivo pelo grupo com a câmera.

### 20/10/2026: notebook do Pokémon lendário (exploração)
- **Prompt:** "Monte o notebook do Pokémon lendário."
- **Uso:** resultados exploratórios (o SVM não superou a regra simples do Total). **Motivou a troca do tema** para
  previsão de batalhas.
- **Verificação:** notebook executado do início ao fim; resultados reproduzidos.

### 20/10/2026: busca de dados de todas as gerações e decisão sobre as batalhas
- **Prompts:** "Procure um dataset com as gerações 1 a 9"; "Me dê o link do Kaggle para validar a origem das batalhas";
  "Quão difícil seria gerar nosso próprio dataset de batalhas?"
- **Uso:** a IA não conseguiu validar os datasets do Kaggle (páginas exigem login) e propôs o **PokéAPI** como fonte. O
  grupo leu a descrição do *Pokemon Challenge* no Kaggle e confirmou que as batalhas são geradas por um algoritmo não
  documentado. Com isso, **decidiu gerar o próprio dataset** com a fórmula de dano.
- **Verificação:** descrição do dataset lida pelo grupo na página do Kaggle; licença do PokéAPI conferida (BSD-3); ligação
  das bases conferida (800 de 800 Pokémon encontrados; 4 ligações por atributos conferidas manualmente).

### 20/10/2026: simulador, pipeline e documentação do Checkpoint 1
- **Prompt:** "Preciso entregar o checklist do Checkpoint 1, consegue ajudar?"
- **Uso:** a IA gerou `src/montar_base.py`, `src/simulador.py`, `src/gerar_batalhas.py`, o notebook
  `01_pipeline_duelo_svm.ipynb`, este README e o rascunho do resumo expandido. **O grupo precisa revisar e entender cada
  parte** antes da apresentação.
- **Verificação feita:**
  - simulador testado em confrontos conhecidos (Blastoise vence Charizard; Weavile vence Garchomp por gelo 4×;
    Ditto × Ditto = 50%);
  - checagem de vazamento: 0 Pokémon em comum entre treino e teste;
  - notebook executado do início ao fim sem erros.
- **Verificação pendente (grupo):** conferir a fórmula de dano com a Bulbapedia; conferir as referências; reexecutar o
  pipeline em outra máquina.

---

### Modelo para novos registros
```
### dd/mm/aaaa: <assunto>
- Integrante:            · Ferramenta/modelo:
- Prompt (resumo):
- Uso da resposta (usada/modificada/descartada):
- Verificação:
```
