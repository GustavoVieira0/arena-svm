"""Coloca dois Pokémon para batalhar: mostra a previsão do SVM treinado e o resultado do simulador.

Uso:
    python src/batalhar.py charizard blastoise
    python src/batalhar.py                    (modo interativo: geração e nome de cada jogador)
    python src/batalhar.py --aleatorio        (sorteia os dois, de qualquer geração)
    python src/batalhar.py --aleatorio 3      (sorteia os dois da geração 3)
    python src/batalhar.py --aleatorio 1 9    (sorteia A da geração 1 e B da geração 9)
"""
import difflib
import sys

import joblib
import numpy as np
import pandas as pd

from simulador import RAIZ, Lutador, batalha, candidatos, eficacia, multiplicador

ATRIBUTOS = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]
N_BATALHAS = 201

pk = pd.read_csv(RAIZ / "data/processed/pokemon.csv").set_index("name")
modelo = joblib.load(RAIZ / "modelos/svm_duelo_v1.joblib")


def melhor_mult(tipos_atk, t1, t2):
    """Mesmo cálculo de feature usado no notebook: multiplicador do melhor golpe (STAB × eficácia)."""
    opcoes = [1.5 * eficacia(t, t1, t2) for t in tipos_atk if isinstance(t, str)]
    if "Normal" not in tipos_atk:
        opcoes.append(eficacia("Normal", t1, t2))
    return max(opcoes) if max(opcoes) > 0 else 1.0


def features(a, b):
    ra, rb = pk.loc[a], pk.loc[b]
    x = {f"dif_{at}": ra[at] - rb[at] for at in ATRIBUTOS}
    x["log_mult_a"] = np.log2(melhor_mult((ra["Type 1"], ra["Type 2"]), rb["Type 1"], rb["Type 2"]))
    x["log_mult_b"] = np.log2(melhor_mult((rb["Type 1"], rb["Type 2"]), ra["Type 1"], ra["Type 2"]))
    return pd.DataFrame([x])


PALAVRAS_SORTEIO = {"", "?", "sorteio", "sortear", "aleatorio", "aleatório", "random"}


def sortear(geracao=None, excluir=None):
    opcoes = pk.index if geracao is None else pk.index[pk.Generation == geracao]
    opcoes = [n for n in opcoes if n != excluir]
    return str(np.random.default_rng().choice(opcoes))


def achar(nome, geracao=None, excluir=None):
    """Nome exato, sorteio (vazio/'sorteio') ou o nome mais parecido, só se a semelhança for alta."""
    nome = nome.strip().lower().replace(" ", "-")
    if nome in PALAVRAS_SORTEIO:
        return sortear(geracao, excluir)
    if nome in pk.index:
        return nome
    parecidos = difflib.get_close_matches(nome, pk.index, n=5, cutoff=0.6)
    if parecidos and difflib.SequenceMatcher(None, nome, parecidos[0]).ratio() >= 0.85:
        print(f"  '{nome}' → usando {parecidos[0]}")
        return parecidos[0]
    print(f"  Pokémon '{nome}' não encontrado." + (f" Você quis dizer: {', '.join(parecidos)}?" if parecidos else ""))
    return None


def perguntar_geracao(jogador):
    while True:
        g = input(f"Jogador {jogador}: geração (1-9, Enter = todas): ").strip()
        if g.lower() == "sair":
            raise KeyboardInterrupt
        if not g:
            return None
        if g.isdigit() and 1 <= int(g) <= 9:
            return int(g)
        print("  Digite um número de 1 a 9 ou deixe vazio.")


def descrever(nome, lut, cands, alvo):
    r = pk.loc[nome]
    tipos = "/".join(t for t in (r["Type 1"], r["Type 2"]) if isinstance(t, str))
    golpes = ", ".join(f"{g.nome} ({g.tipo or 'sem tipo'}, {g.poder:g}, {multiplicador(g, lut, alvo):g}×)" for g in cands[:3])
    return (f"  {nome:<18} gen {r.Generation} | {tipos:<16} | HP {lut.hp:>3} | Vel {lut.spe:>3} no nível 50\n"
            f"  {'':<18} melhores golpes contra {alvo.nome}: {golpes}")


def duelo(a, b, rng=None):
    rng = rng or np.random.default_rng()
    la, lb = Lutador.de_linha(pk.loc[a].to_dict() | {"name": a}), Lutador.de_linha(pk.loc[b].to_dict() | {"name": b})
    ca, cb = candidatos(la, lb), candidatos(lb, la)
    print()
    print(descrever(a, la, ca, lb))
    print(descrever(b, lb, cb, la))

    score = modelo.decision_function(features(a, b))[0]
    fav_svm = a if score > 0 else b
    vit_a = sum(batalha(la, lb, rng, ca, cb) for _ in range(N_BATALHAS))
    fav_sim = a if vit_a > N_BATALHAS / 2 else b

    print(f"\n  SVM (treinado):  favorito = {fav_svm.upper()}  (score {score:+.2f}; quanto mais longe de 0, mais confiante)")
    print(f"  Simulador:       {a} venceu {vit_a}/{N_BATALHAS} ({vit_a / N_BATALHAS:.0%})  → favorito = {fav_sim.upper()}")
    print("  " + ("✔ O SVM acertou o favorito." if fav_svm == fav_sim else "✘ O SVM errou o favorito."))

    narracao = []
    venceu_a = batalha(la, lb, rng, ca, cb, registro=narracao)
    print("\n  Uma batalha narrada:")
    for linha in narracao:
        print("    " + linha)
    print(f"  Vencedor: {(a if venceu_a else b).upper()}\n")


def main():
    args = sys.argv[1:]
    if args and args[0] == "--aleatorio":
        gens = [int(g) for g in args[1:3]]
        ga, gb = (gens + [None, None])[:2] if len(gens) != 1 else (gens[0], gens[0])
        a = sortear(ga)
        duelo(a, sortear(gb, excluir=a))
    elif len(args) == 2:
        a, b = achar(args[0]), achar(args[1])
        if a and b:
            duelo(a, b)
    else:
        print("Arena SVM: para cada jogador, escolha a geração e o Pokémon (nome em inglês, ex.: pikachu,")
        print("charizard-mega-x). Deixe o nome vazio (ou digite 'sorteio') para sortear. Digite 'sair' para fechar.\n")
        while True:
            escolhidos = []
            for jogador in "AB":
                g = perguntar_geracao(jogador)
                nome = None
                while nome is None:
                    entrada = input(f"Jogador {jogador}: Pokémon: ").strip()
                    if entrada.lower() == "sair":
                        return
                    nome = achar(entrada, g, excluir=escolhidos[0] if escolhidos else None)
                gen = pk.loc[nome, "Generation"]
                print(f"  → Jogador {jogador} escolheu {nome.upper()} (geração {gen})\n")
                escolhidos.append(nome)
            duelo(*escolhidos)
            print("-" * 100)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nAté a próxima batalha!")
