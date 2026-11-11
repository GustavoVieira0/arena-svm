"""Features de uma batalha A × B, usadas no notebook e na demo (batalhar.py).

Conjuntos:
- BASE (v1, Checkpoint 1): diferença dos 6 atributos + eficácia de tipo dos golpes do próprio tipo (log2).
- GOLPES (E2, Checkpoint 2): informação sobre os golpes que cada Pokémon realmente aprende contra o adversário:
  fração do HP do adversário que o melhor golpe tira por turno, golpes necessários para nocautear e se há
  golpe de prioridade. Tudo é conhecido antes da batalha (lista pública de golpes), sem simular nada.
"""
import math

import numpy as np
import pandas as pd

from simulador import Lutador, candidatos, dano_base, eficacia, multiplicador

ATRIBUTOS = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]
COLS_BASE = [f"dif_{a}" for a in ATRIBUTOS] + ["log_mult_a", "log_mult_b"]
COLS_GOLPES = ["frac_a", "frac_b", "nocaute_a", "nocaute_b", "dif_nocaute", "prioridade_a", "prioridade_b"]


def melhor_mult_tipo(tipos_atk, t1, t2):
    """Multiplicador do melhor golpe do próprio tipo (STAB 1,5 × eficácia) ou golpe Normal; imunidade total = 1."""
    opcoes = [1.5 * eficacia(t, t1, t2) for t in tipos_atk if isinstance(t, str)]
    if "Normal" not in tipos_atk:
        opcoes.append(eficacia("Normal", t1, t2))
    return max(opcoes) if max(opcoes) > 0 else 1.0


def _base(ra, rb):
    x = {f"dif_{a}": ra[a] - rb[a] for a in ATRIBUTOS}
    x["log_mult_a"] = math.log2(melhor_mult_tipo((ra["Type 1"], ra["Type 2"]), rb["Type 1"], rb["Type 2"]))
    x["log_mult_b"] = math.log2(melhor_mult_tipo((rb["Type 1"], rb["Type 2"]), ra["Type 1"], ra["Type 2"]))
    return x


def _melhor_golpe(atk, dfs):
    """Fração do HP do defensor que o melhor golpe tira em média por turno, e se há golpe de prioridade útil."""
    melhor, prioridade = 0.0, 0
    for g in candidatos(atk, dfs):
        esperado = dano_base(g, atk, dfs) * 0.925 * multiplicador(g, atk, dfs) * g.precisao * g.acertos_medios
        melhor = max(melhor, esperado / dfs.hp)
        if g.prioridade > 0 and esperado > 0:
            prioridade = 1
    return min(melhor, 3.0), prioridade


def _golpes(la, lb):
    fa, pa = _melhor_golpe(la, lb)
    fb, pb = _melhor_golpe(lb, la)
    na, nb = min(math.ceil(1 / max(fa, 1e-3)), 10), min(math.ceil(1 / max(fb, 1e-3)), 10)
    return {"frac_a": fa, "frac_b": fb, "nocaute_a": na, "nocaute_b": nb, "dif_nocaute": na - nb,
            "prioridade_a": pa, "prioridade_b": pb}


def linha_de(ra, rb, la, lb, golpes=True):
    """Features de A × B a partir das linhas de atributos/tipos (ra, rb) e dos lutadores (la, lb).
    Serve também para personagens criados no Laboratório, que não estão na base."""
    x = _base(ra, rb)
    if golpes:
        x |= _golpes(la, lb)
    return x


class Extrator:
    """Calcula as features para pares de pokeapi_id, com cache dos lutadores."""

    def __init__(self, pokemon: pd.DataFrame):
        self.info = pokemon.set_index("pokeapi_id")
        self._lut = {}

    def lutador(self, pid):
        if pid not in self._lut:
            self._lut[pid] = Lutador.de_linha(self.info.loc[pid].to_dict() | {"pokeapi_id": pid})
        return self._lut[pid]

    def linha(self, a_id, b_id, golpes=True):
        return linha_de(self.info.loc[a_id], self.info.loc[b_id], self.lutador(a_id), self.lutador(b_id), golpes)

    def tabela(self, batalhas: pd.DataFrame, golpes=True):
        return pd.DataFrame([self.linha(a, b, golpes) for a, b in zip(batalhas.a_id, batalhas.b_id)],
                            index=batalhas.index)
