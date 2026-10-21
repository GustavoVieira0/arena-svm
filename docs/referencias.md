# Referências selecionadas

Formato ABNT. Os itens 1 a 5 são artigos científicos ou relatórios técnicos revisados; os demais são livros, documentação
e fontes de dados. **Antes de entregar, cada integrante deve abrir as referências que for citar e confirmar os dados.**

## Artigos científicos
1. **CORTES, C.; VAPNIK, V.** Support-vector networks. *Machine Learning*, v. 20, n. 3, p. 273–297, 1995.
   > **Contribuição:** é o artigo que define o SVM com **margem suave** (parâmetro C), exatamente o modelo usado pelo
   > `SVC` do scikit-learn. Fundamenta a explicação de hiperplano, margem e vetores de suporte.

2. **BOSER, B. E.; GUYON, I. M.; VAPNIK, V. N.** A training algorithm for optimal margin classifiers. In: *Proceedings of
   the Fifth Annual Workshop on Computational Learning Theory (COLT '92)*. Pittsburgh: ACM, 1992. p. 144–152.
   > **Contribuição:** introduz o **truque do kernel** no SVM. Justifica o uso do kernel RBF para capturar a interação
   > não linear entre velocidade, força e vantagem de tipo.

3. **KAUFMAN, S.; ROSSET, S.; PERLICH, C.; STITELMAN, O.** Leakage in data mining: formulation, detection, and avoidance.
   *ACM Transactions on Knowledge Discovery from Data*, v. 6, n. 4, p. 15:1–15:21, 2012.
   > **Contribuição:** define formalmente o **vazamento de dados** e mostra como ele infla resultados. Fundamenta a
   > divisão treino/teste por Pokémon (gerações 1–6 × 7–9) e o experimento E4.

4. **PEDREGOSA, F. et al.** Scikit-learn: machine learning in Python. *Journal of Machine Learning Research*, v. 12,
   p. 2825–2830, 2011.
   > **Contribuição:** biblioteca usada na implementação (SVC, Pipeline, StandardScaler, métricas).

5. **HSU, C.-W.; CHANG, C.-C.; LIN, C.-J.** *A practical guide to support vector classification*. Taipei: Department of
   Computer Science, National Taiwan University, 2003 (revisado em 2016). Relatório técnico.
   > **Contribuição:** recomenda padronizar os atributos e buscar C e gamma em grade com validação cruzada. Embasa a
   > preparação dos dados e o experimento E3.

## Complementares
6. **PLATT, J.** Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods.
   In: SMOLA, A. et al. (org.). *Advances in Large Margin Classifiers*. Cambridge: MIT Press, 1999. p. 61–74.
   > Para transformar o score do SVM em "probabilidade de vitória" no protótipo.
7. **YANNAKAKIS, G. N.; TOGELIUS, J.** *Artificial Intelligence and Games*. Cham: Springer, 2018.
   > Contexto da IA aplicada a jogos (relevância do estudo).
8. **POKÉAPI.** PokéAPI: the RESTful Pokémon API, dados em CSV. GitHub, c2013–2023. Disponível em:
   https://github.com/PokeAPI/pokeapi. Acesso em: 20 out. 2026.
   > Fonte dos atributos, tipos, gerações e tabela de eficácia de tipos (licença BSD-3).
9. **BULBAPEDIA.** Damage. Disponível em: https://bulbapedia.bulbagarden.net/wiki/Damage. Acesso em: 20 out. 2026.
   > Documentação comunitária da fórmula de dano usada no simulador.

> Ajustem as datas de acesso para o dia em que consultarem as páginas.
