"""Gera data/processed/batalhas.csv usando o simulador.

Os confrontos são sorteados em três grupos, para permitir avaliar o modelo em Pokémon nunca vistos no treino:
- treino:  os dois Pokémon são das gerações 1–6
- teste:   os dois Pokémon são das gerações 7–9
- misto:   um de cada grupo (reservado para experimentos futuros)

Cada confronto é simulado N_SIMULACOES vezes (número ímpar, sem empate). A variável-alvo `a_vence` indica se A é o
favorito (venceu a maioria das simulações). `prob_a` guarda a fração de vitórias de A, que mostra o quanto a sorte pesa.

Uso:  python src/gerar_batalhas.py              (golpes reais -> batalhas.csv)
      python src/gerar_batalhas.py simples      (golpes genéricos da versão 1 -> batalhas_golpes_simples.csv)
"""
import sys
import time

import numpy as np
import pandas as pd

from simulador import RAIZ, Lutador, simular_confronto

SEED = 42
N_SIMULACOES = 21
N_CONFRONTOS = {"treino": 30000, "teste": 6000, "misto": 4000}


def sortear_pares(ids_a, ids_b, n, rng):
    pares = set()
    while len(pares) < n:
        a, b = rng.choice(ids_a), rng.choice(ids_b)
        if a != b:
            pares.add((int(a), int(b)))
    return sorted(pares)


def main(modo="reais"):
    pk = pd.read_csv(RAIZ / "data/processed/pokemon.csv")
    lutadores = {int(r["pokeapi_id"]): Lutador.de_linha(r, modo) for _, r in pk.iterrows()}
    pk = pk.set_index("pokeapi_id")
    antigos = pk.index[pk.Generation <= 6].to_numpy()
    novos = pk.index[pk.Generation >= 7].to_numpy()
    grupos = {"treino": (antigos, antigos), "teste": (novos, novos), "misto": (antigos, novos)}

    # os pares são sorteados antes e com gerador próprio: os dois modos de golpes usam exatamente os mesmos confrontos
    rng_pares = np.random.default_rng(SEED)
    pares = {}
    for grupo, (ga, gb) in grupos.items():
        pares[grupo] = [(b, a) if grupo == "misto" and rng_pares.random() < 0.5 else (a, b)
                        for a, b in sortear_pares(ga, gb, N_CONFRONTOS[grupo], rng_pares)]

    rng = np.random.default_rng(SEED + 1)
    linhas, t0 = [], time.time()
    for grupo, lista in pares.items():
        for a, b in lista:
            v = simular_confronto(lutadores[a], lutadores[b], rng, N_SIMULACOES)
            linhas.append((a, b, grupo, v))
        print(f"{grupo}: {len(lista)} confrontos ({time.time() - t0:.0f}s)")

    df = pd.DataFrame(linhas, columns=["a_id", "b_id", "grupo", "vitorias_a"])
    df["prob_a"] = (df.vitorias_a / N_SIMULACOES).round(4)
    df["a_vence"] = (df.vitorias_a > N_SIMULACOES / 2).astype(int)
    saida = RAIZ / "data/processed" / ("batalhas.csv" if modo == "reais" else "batalhas_golpes_simples.csv")
    df.to_csv(saida, index=False)
    print(f"[golpes {modo}] {len(df)} confrontos × {N_SIMULACOES} simulações salvos em {saida.relative_to(RAIZ)}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "reais")
