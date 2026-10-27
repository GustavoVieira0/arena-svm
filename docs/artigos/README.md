# Artigos de referência

Material de estudo do grupo: links oficiais, o que cada artigo apresenta e como ele se relaciona com o projeto.
A lista completa em formato ABNT está em [`../referencias.md`](../referencias.md).

> **PDFs:** os artigos da Springer e da ACM têm direitos das editoras e **não são versionados aqui**. Para guardar PDFs na
> sua máquina, use a pasta `docs/artigos/pdfs/`, que é ignorada pelo git. Para acessar o texto completo, abra o DOI
> conectado à rede da faculdade ou pelo Portal de Periódicos da CAPES, ou procure uma versão dos autores no Google Acadêmico.

| # | Artigo | Tipo | Acesso |
|---|---|---|---|
| 1 | Cortes e Vapnik (1995), *Support-vector networks* | Artigo (revista) | [DOI](https://doi.org/10.1007/BF00994018) · [Google Acadêmico](https://scholar.google.com/scholar?q=%22Support-vector+networks%22+Cortes+Vapnik) |
| 2 | Boser, Guyon e Vapnik (1992), *A training algorithm for optimal margin classifiers* | Artigo (conferência) | [DOI](https://doi.org/10.1145/130385.130401) · [Google Acadêmico](https://scholar.google.com/scholar?q=%22A+training+algorithm+for+optimal+margin+classifiers%22) |
| 3 | Kaufman, Rosset, Perlich e Stitelman (2012), *Leakage in data mining* | Artigo (revista) | [DOI](https://doi.org/10.1145/2382577.2382579) · [Google Acadêmico](https://scholar.google.com/scholar?q=%22Leakage+in+data+mining%3A+formulation%2C+detection%2C+and+avoidance%22) |
| 4 | Pedregosa et al. (2011), *Scikit-learn: machine learning in Python* | Artigo (revista) | [Página](https://jmlr.org/papers/v12/pedregosa11a.html) · [PDF gratuito](https://jmlr.org/papers/volume12/pedregosa11a/pedregosa11a.pdf) |
| 5 | Hsu, Chang e Lin (2003), *A practical guide to support vector classification* | Relatório técnico | [PDF gratuito](https://www.csie.ntu.edu.tw/~cjlin/papers/guide/guide.pdf) |

---

## 1. Cortes e Vapnik (1995): *Support-vector networks*
*Machine Learning*, v. 20, n. 3, p. 273–297. DOI: 10.1007/BF00994018

**O que apresenta:** o SVM na forma usada até hoje.
- A melhor fronteira entre duas classes é a que fica **o mais longe possível** dos exemplos dos dois lados (**margem
  máxima**), o que ajuda a acertar dados novos.
- A fronteira depende só dos exemplos mais próximos dela, os **vetores de suporte**.
- **Margem suave:** permite alguns erros no treino, com penalidade controlada pelo parâmetro **C**, porque dados reais
  raramente são separáveis.
- Combina isso com o truque do kernel e avalia em reconhecimento de dígitos manuscritos.

**No projeto:** é exatamente o modelo do `SVC` usado no notebook. O parâmetro **C** será ajustado no experimento E3.

## 2. Boser, Guyon e Vapnik (1992): *A training algorithm for optimal margin classifiers*
*Proceedings of COLT '92*, p. 144–152. DOI: 10.1145/130385.130401

**O que apresenta:** a base do SVM.
- Algoritmo de treino que encontra a fronteira de **margem máxima**, definida por poucos exemplos.
- **Truque do kernel:** uma função (kernel) calcula de forma implícita e eficiente uma transformação dos dados para um
  espaço em que uma fronteira curva vira um plano.
- Ainda não tem margem suave (exige dados separáveis), limitação resolvida no artigo de 1995.

**No projeto:** justifica o **kernel RBF**, que permite uma fronteira curva para capturar a interação entre velocidade,
força e vantagem de tipo.

## 3. Kaufman et al. (2012): *Leakage in data mining: formulation, detection, and avoidance*
*ACM Transactions on Knowledge Discovery from Data*, v. 6, n. 4, art. 15. DOI: 10.1145/2382577.2382579

**O que apresenta:** o problema do **vazamento de dados** (*data leakage*).
- Vazamento é quando o modelo recebe, no treino, informação que não estaria disponível na hora real de prever. O
  resultado parece ótimo na avaliação e falha na prática.
- Formaliza o conceito e mostra casos reais, inclusive em competições de dados.
- Propõe evitar o problema separando com rigor o que se aprende do que se prevê, e apresenta formas de detectá-lo.

**No projeto:** fundamenta a **divisão por geração** (treino com as gerações 1–6, teste com as 7–9, nenhum Pokémon
nos dois). Medir o efeito de uma divisão com vazamento é o experimento E4.

## 4. Pedregosa et al. (2011): *Scikit-learn: machine learning in Python*
*Journal of Machine Learning Research*, v. 12, n. 85, p. 2825–2830.

**O que apresenta:** a biblioteca scikit-learn: algoritmos de aprendizado de máquina em Python com interface
padronizada (`fit`/`predict`), focada em facilidade de uso, documentação e eficiência, sob licença BSD.

**No projeto:** ferramenta da implementação: `SVC`, `StandardScaler`, `Pipeline`, `LogisticRegression` e métricas.

## 5. Hsu, Chang e Lin (2003): *A practical guide to support vector classification*
Relatório técnico, National Taiwan University (revisado em 2016).

**O que apresenta:** guia prático dos autores do LIBSVM: padronizar os atributos, começar pelo kernel RBF e escolher C e
gamma por busca em grade com validação cruzada.

**No projeto:** embasa a padronização dos dados e o roteiro do experimento E3.

---

### Como explicar na apresentação (os dois principais)
- **Cortes e Vapnik (1995):** "É a base do SVM: busca a fronteira com a maior margem entre as classes e aceita alguns
  erros, controlados pelo C."
- **Kaufman et al. (2012):** "Trata de vazamento de dados. Por causa dele, separamos treino e teste por geração: nenhum
  Pokémon aparece nos dois."

> Os resumos acima são uma síntese do grupo. Antes de citar detalhes, leia pelo menos o *abstract* de cada artigo.
