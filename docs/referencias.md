# Referências selecionadas

Formato ABNT. Os itens 1 a 4 são **artigos científicos revisados por pares** (dados conferidos em 27/10/2026 nas páginas
oficiais e pelos DOIs); o item 5 é um relatório técnico; os demais são livro, capítulo, documentação e fontes de dados.

## Artigos científicos
1. **CORTES, C.; VAPNIK, V.** Support-vector networks. *Machine Learning*, v. 20, n. 3, p. 273–297, 1995.
   DOI: [10.1007/BF00994018](https://doi.org/10.1007/BF00994018).
   > **Contribuição:** é o artigo que define o SVM com **margem suave** (parâmetro C), exatamente o modelo usado pelo
   > `SVC` do scikit-learn. Fundamenta a explicação de hiperplano, margem e vetores de suporte.

2. **BOSER, B. E.; GUYON, I. M.; VAPNIK, V. N.** A training algorithm for optimal margin classifiers. In: *Proceedings of
   the Fifth Annual Workshop on Computational Learning Theory (COLT '92)*. Pittsburgh: ACM, 1992. p. 144–152.
   DOI: [10.1145/130385.130401](https://doi.org/10.1145/130385.130401).
   > **Contribuição:** introduz o **truque do kernel** no SVM. Justifica o uso do kernel RBF para capturar a interação
   > não linear entre velocidade, força e vantagem de tipo.

3. **KAUFMAN, S.; ROSSET, S.; PERLICH, C.; STITELMAN, O.** Leakage in data mining: formulation, detection, and avoidance.
   *ACM Transactions on Knowledge Discovery from Data*, v. 6, n. 4, p. 15:1–15:21, 2012.
   DOI: [10.1145/2382577.2382579](https://doi.org/10.1145/2382577.2382579).
   > **Contribuição:** define formalmente o **vazamento de dados** e mostra como ele infla resultados. Fundamenta a
   > divisão treino/teste por Pokémon (gerações 1–6 × 7–9) e o experimento E4.

4. **PEDREGOSA, F. et al.** Scikit-learn: machine learning in Python. *Journal of Machine Learning Research*, v. 12,
   n. 85, p. 2825–2830, 2011. Disponível em: https://jmlr.org/papers/v12/pedregosa11a.html (a JMLR não usa DOI).
   > **Contribuição:** biblioteca usada na implementação (SVC, Pipeline, StandardScaler, métricas).

5. **HSU, C.-W.; CHANG, C.-C.; LIN, C.-J.** *A practical guide to support vector classification*. Taipei: Department of
   Computer Science, National Taiwan University, 2003 (revisado em 2016). Relatório técnico. Disponível em:
   https://www.csie.ntu.edu.tw/~cjlin/papers/guide/guide.pdf.
   > **Contribuição:** recomenda padronizar os atributos e buscar C e gamma em grade com validação cruzada. Embasa a
   > preparação dos dados e o experimento E3.

## Complementares
6. **PLATT, J.** Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods.
   In: SMOLA, A. et al. (org.). *Advances in Large Margin Classifiers*. Cambridge: MIT Press, 1999. p. 61–74.
   > Para transformar o score do SVM em "probabilidade de vitória" no protótipo.
7. **YANNAKAKIS, G. N.; TOGELIUS, J.** *Artificial Intelligence and Games*. Cham: Springer, 2018. ISBN 978-3-319-63518-7.
   Disponível em: https://gameaibook.org.
   > Contexto da IA aplicada a jogos (relevância do estudo).
8. **POKÉAPI.** PokéAPI: the RESTful Pokémon API, dados em CSV. GitHub, c2013–2023. Disponível em:
   https://github.com/PokeAPI/pokeapi. Acesso em: 20 out. 2026.
   > Fonte dos atributos, tipos, gerações e tabela de eficácia de tipos (licença BSD-3).
9. **BULBAPEDIA.** Damage. Disponível em: https://bulbapedia.bulbagarden.net/wiki/Damage. Acesso em: 20 out. 2026.
   > Documentação comunitária da fórmula de dano usada no simulador.

> Ajustem as datas de acesso para o dia em que consultarem as páginas.
