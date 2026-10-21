"""Monta data/processed/pokemon.csv a partir dos CSVs do PokéAPI (data/raw/pokeapi).

Uma linha por Pokémon jogável (espécies + formas alternativas que mudam atributos ou tipos: Mega, Alola, Galar,
Hisui...). Formas apenas cosméticas ou que não são usadas em batalha normal (Gigantamax, Totem, Pikachu com boné...)
são removidas, assim como formas que repetem exatamente os atributos e tipos de outra forma da mesma espécie.

Uso:  python src/montar_base.py
"""
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
RAW = RAIZ / "data" / "raw" / "pokeapi"
SAIDA = RAIZ / "data" / "processed" / "pokemon.csv"

ATRIBUTOS = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]
STAT_IDS = dict(zip(range(1, 7), ATRIBUTOS))
# formas excluídas: cosméticas, exclusivas de eventos/chefes ou que não existem em batalha normal
EXCLUIR = r"gmax|totem|starter|-cap$|cosplay|rock-star|pop-star|belle$|-phd$|libre$|eternamax|power-construct|battle-bond"


def montar():
    poke = pd.read_csv(RAW / "pokemon.csv")
    species = pd.read_csv(RAW / "pokemon_species.csv")
    stats = pd.read_csv(RAW / "pokemon_stats.csv")
    ptypes = pd.read_csv(RAW / "pokemon_types.csv")
    types = pd.read_csv(RAW / "types.csv").set_index("id")["identifier"].str.capitalize()

    st = stats.pivot(index="pokemon_id", columns="stat_id", values="base_stat").rename(columns=STAT_IDS)
    tp = (ptypes.assign(t=ptypes.type_id.map(types))
          .pivot(index="pokemon_id", columns="slot", values="t"))
    tp.columns = ["Type 1", "Type 2"]

    df = (poke.rename(columns={"id": "pokeapi_id", "identifier": "name"})
          .merge(species[["id", "identifier", "generation_id", "is_legendary", "is_mythical"]]
                 .rename(columns={"id": "species_id", "identifier": "species", "generation_id": "Generation"}),
                 on="species_id")
          .join(st, on="pokeapi_id").join(tp, on="pokeapi_id"))

    n_total = len(df)
    df = df[~df["name"].str.contains(EXCLUIR, regex=True)]
    n_cosmeticas = n_total - len(df)
    df = df.drop_duplicates(subset=["species_id", "Type 1", "Type 2", *ATRIBUTOS])
    n_repetidas = n_total - n_cosmeticas - len(df)

    df["Total"] = df[ATRIBUTOS].sum(axis=1)
    df["is_mega"] = df["name"].str.contains("-mega|-primal")
    df["is_forma_alternativa"] = df["is_default"] == 0
    df = df[["pokeapi_id", "name", "species", "species_id", "Generation", "Type 1", "Type 2", "Total", *ATRIBUTOS,
             "is_legendary", "is_mythical", "is_mega", "is_forma_alternativa"]].reset_index(drop=True)

    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(SAIDA, index=False)
    print(f"{n_total} registros no PokéAPI | removidas {n_cosmeticas} formas cosméticas/especiais "
          f"e {n_repetidas} formas repetidas | {len(df)} Pokémon salvos em {SAIDA.relative_to(RAIZ)}")
    return df


if __name__ == "__main__":
    montar()
