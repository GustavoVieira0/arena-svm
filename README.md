# Arena de Personagens: prevendo batalhas Pokémon com SVM

Projeto da disciplina **Inteligência Artificial II** · Ciência da Computação · FIB
Professor: Ronaldo Cesar Dametto

## Problema
Em jogos de batalha, os jogadores escolhem personagens sem saber quem tem vantagem no confronto. Este projeto investiga
se é possível **prever o favorito de uma batalha 1 contra 1** usando apenas as características dos personagens
(atributos e tipos), e **o que realmente decide** o resultado.

**Pergunta de investigação:** um classificador **SVM (Support Vector Machine)**, usando apenas atributos e tipos, consegue
prever o vencedor de batalhas entre **Pokémon que nunca viu no treino**, superando regras simples como "vence o mais
rápido" ou "vence o mais forte"?

**Aplicação prevista:** uma "arena" web em que duas pessoas escolhem (ou sorteiam) um Pokémon de qualquer geração e o
sistema prevê o favorito, mostrando a confiança da previsão.

## Integrantes e responsabilidades
| Integrante | Responsabilidade principal |
|---|---|
| Luan Carlos de Souza Ferreira | Dados e análise exploratória (EDA) |
| Gustavo de Carvalho Vieira | Pré-processamento, base de Pokémon e simulador de batalhas |
| Anthony Gabriel Schirato Lourenço | Experimentos e avaliação dos modelos |
| Lucas Miguel Moreno Rios | Protótipo web (arena para 2 jogadores) |
| Alceu Ferreira dos Santos Neto | Comunicação, resumo expandido, vídeo e materiais |

## Dados
| Arquivo | Origem | Licença |
|---|---|---|
| `data/raw/pokeapi/*.csv` | [PokéAPI](https://github.com/PokeAPI/pokeapi), pasta `data/v2/csv`: atributos, tipos, gerações e tabela de eficácia de tipos | BSD-3-Clause |
| `data/processed/pokemon.csv` | Gerado por `src/montar_base.py`: 1.242 Pokémon jogáveis das gerações 1–9 | derivado do PokéAPI |
| `data/processed/batalhas.csv` | Gerado por `src/gerar_batalhas.py`: 40.000 confrontos com **golpes reais**, cada um simulado 21 vezes | gerado pelo grupo |
| `data/processed/batalhas_golpes_simples.csv` | Mesmos confrontos com golpes genéricos (versão 1), para comparação | gerado pelo grupo |

**Por que um dataset de batalhas próprio?** O dataset público mais usado (*Pokemon Challenge*, Kaggle) cobre só as gerações
1–6, e as batalhas dele foram geradas por um "algoritmo próprio" sem regras documentadas. O nosso simulador
(`src/simulador.py`) usa a **fórmula de dano dos jogos principais** e os **golpes que cada Pokémon realmente aprende**
(poder, precisão, prioridade, acertos múltiplos, dano de retorno, roubo de vida, queda de atributos), escolhendo a cada
turno o golpe de maior dano esperado. As simplificações (sem habilidades, itens, status ou trocas) estão no topo do arquivo.

**Variável-alvo:** `a_vence` (1 se o Pokémon A venceu a maioria das 21 simulações).

**Divisão treino/teste (sem vazamento):** treino com batalhas só entre Pokémon das gerações 1–6 e teste só entre Pokémon das
gerações 7–9. Nenhum Pokémon aparece nos dois conjuntos.

## Técnica
SVM (`sklearn.svm.SVC`, kernel RBF) com padronização (`StandardScaler`) dentro de um `Pipeline`. Features: diferença dos 6
atributos (A − B) e o multiplicador de tipo do melhor golpe de cada lado (em log2).

## Estrutura
```
arena-svm/
├── data/
│   ├── raw/pokeapi/          # CSVs originais do PokéAPI
│   └── processed/            # pokemon.csv e batalhas.csv (gerados)
├── src/
│   ├── montar_base.py        # PokéAPI -> pokemon.csv
│   ├── simulador.py          # regras da batalha (fórmula de dano)
│   ├── gerar_batalhas.py     # pokemon.csv -> batalhas.csv (seed 42)
│   └── batalhar.py           # escolha dois Pokémon: previsão do SVM + simulação narrada
├── notebooks/
│   └── 01_pipeline_duelo_svm.ipynb   # EDA, baselines, SVM e métricas (ponta a ponta)
├── modelos/                  # modelos treinados (.joblib)
└── docs/                     # resumo expandido, referências, diário de IA, guia do checkpoint
```

## Como executar
Requisitos: Python 3.10 ou superior.
```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (Linux/Mac: source .venv/bin/activate)
pip install -r requirements.txt

python src/montar_base.py       # opcional: o resultado já está versionado
python src/gerar_batalhas.py    # opcional: cerca de 1 min, mesmo resultado com a seed 42
```
Para batalhar dois Pokémon no terminal (escolha de geração, sorteio e batalha narrada):
```bash
python src/batalhar.py                     # modo interativo
python src/batalhar.py charizard blastoise
python src/batalhar.py --aleatorio 1 9     # sorteia A da geração 1 e B da geração 9
```
Depois, abra `notebooks/01_pipeline_duelo_svm.ipynb` (VS Code ou Jupyter) e execute todas as células (cerca de 1 min).

**Parâmetros principais:** `SEED = 42`; nível 50; 21 simulações por confronto; 30.000 confrontos de treino, 6.000 de teste
e 4.000 mistos; SVM RBF com `C = 1` e `gamma = "scale"`.

## Resultados preliminares (Checkpoint 1)
Teste com 6.000 batalhas entre Pokémon das gerações 7–9, nunca vistos no treino:

| Modelo | Acurácia | F1 | ROC-AUC |
|---|---|---|---|
| Classe majoritária | 0,510 | 0,000 | 0,500 |
| Vence o mais rápido | 0,678 | 0,675 | 0,713 |
| Vence o maior Total | 0,806 | 0,802 | 0,898 |
| Regressão Logística | 0,856 | 0,853 | 0,936 |
| **SVM RBF (padrão)** | **0,866** | **0,863** | **0,935** |

Com os golpes genéricos da versão 1 do simulador, o mesmo SVM chegava a 0,921. A queda mostra que o modelo ainda não
sabe quais golpes cada Pokémon aprende (ex.: erra Pikachu × Gyarados, que o Pikachu vence com Volt Tackle). Incluir
features de golpes é o experimento E2.

## Próximos passos (Checkpoint 2)
E1: comparação de kernels · E2: features de golpes (melhor golpe que cada um aprende contra o adversário) · E3: ajuste de C e gamma com validação cruzada agrupada por
Pokémon · E4: medir o efeito do vazamento (divisão aleatória × por Pokémon) · E5: análise de erros (limiar de nocaute,
imunidades, Shedinja).

## Uso de IA
O uso de ferramentas de IA está registrado em `docs/diario_ia.md`.

---
Pokémon e os nomes dos personagens são marcas registradas da Nintendo, Game Freak e Creatures. Projeto acadêmico, sem fins
comerciais.
