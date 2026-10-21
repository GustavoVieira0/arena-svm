"""Simulador de batalhas 1 contra 1 baseado na fórmula de dano dos jogos principais de Pokémon.

Regras (simplificações documentadas):
- Os dois Pokémon estão no nível 50, com IV 31, EV 0 e natureza neutra.
- Cada Pokémon tem um golpe de 80 de poder para cada um dos seus tipos (com STAB, bônus de 1,5) e um golpe de
  cobertura do tipo Normal com 70 de poder. A categoria (física ou especial) segue o maior atributo de ataque.
- A cada turno, cada Pokémon usa o golpe que causa mais dano esperado no adversário. Se nenhum golpe afeta o alvo
  (imunidade), usa "Esforço" (50 de poder, sem tipo).
- Quem tem mais Velocidade ataca primeiro. Em caso de empate, a ordem é sorteada a cada turno.
- Dano = (((2 × Nível / 5 + 2) × Poder × Ataque / Defesa) / 50 + 2) × Aleatório(0,85–1,00) × Crítico(1/24 → 1,5)
         × STAB × Eficácia de tipo     (fórmula da 5ª geração em diante, sem itens, habilidades e clima)
- Todos os golpes acertam. Não há status, itens, habilidades, trocas nem mudanças de atributos.
"""
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
NIVEL = 50
PODER_STAB, PODER_COBERTURA, PODER_ESFORCO = 80, 70, 50
CHANCE_CRITICO, MULT_CRITICO = 1 / 24, 1.5


def carregar_tabela_tipos():
    tipos = pd.read_csv(RAIZ / "data/raw/pokeapi/types.csv").set_index("id")["identifier"].str.capitalize()
    ef = pd.read_csv(RAIZ / "data/raw/pokeapi/type_efficacy.csv")
    return {(tipos[r.damage_type_id], tipos[r.target_type_id]): r.damage_factor / 100 for r in ef.itertuples()}


TABELA_TIPOS = carregar_tabela_tipos()


def eficacia(tipo_golpe, tipo1, tipo2=None):
    """Multiplicador de tipo de um golpe contra um defensor (0, 0,25, 0,5, 1, 2 ou 4)."""
    if tipo_golpe is None:
        return 1.0
    m = TABELA_TIPOS.get((tipo_golpe, tipo1), 1.0)
    if isinstance(tipo2, str):
        m *= TABELA_TIPOS.get((tipo_golpe, tipo2), 1.0)
    return m


@dataclass
class Lutador:
    nome: str
    tipos: tuple
    hp: int
    atk: int
    df: int
    spa: int
    spd: int
    spe: int

    @classmethod
    def de_linha(cls, r):
        calc = lambda base: math.floor((2 * base + 31) * NIVEL / 100) + 5
        hp = 1 if r["HP"] == 1 else math.floor((2 * r["HP"] + 31) * NIVEL / 100) + NIVEL + 10  # Shedinja: sempre 1
        tipos = (r["Type 1"],) + ((r["Type 2"],) if isinstance(r["Type 2"], str) else ())
        return cls(r["name"], tipos, hp, calc(r["Attack"]), calc(r["Defense"]), calc(r["Sp. Atk"]),
                   calc(r["Sp. Def"]), calc(r["Speed"]))

    def golpes(self):
        """Lista de (tipo, poder, stab). None = sem tipo."""
        g = [(t, PODER_STAB, 1.5) for t in self.tipos]
        if "Normal" not in self.tipos:
            g.append(("Normal", PODER_COBERTURA, 1.0))
        return g


def melhor_golpe(atacante, defensor):
    """Escolhe o golpe com maior dano esperado. Retorna (dano_base sem aleatoriedade, multiplicador)."""
    fisico = atacante.atk >= atacante.spa
    a = atacante.atk if fisico else atacante.spa
    d = defensor.df if fisico else defensor.spd
    melhor = None
    for tipo, poder, stab in atacante.golpes():
        mult = stab * eficacia(tipo, *defensor.tipos)
        if mult > 0 and (melhor is None or poder * mult > melhor[0] * melhor[1]):
            melhor = (poder, mult)
    if melhor is None:  # nenhum golpe afeta o alvo: Esforço
        melhor = (PODER_ESFORCO, 1.0)
    poder, mult = melhor
    base = math.floor(math.floor(math.floor(2 * NIVEL / 5 + 2) * poder * a / d) / 50) + 2
    return base, mult


def dano(base, mult, rng):
    aleatorio = rng.integers(85, 101) / 100
    critico = MULT_CRITICO if rng.random() < CHANCE_CRITICO else 1.0
    return max(1, math.floor(math.floor(base * aleatorio * critico) * mult))


def batalha(a, b, rng, golpe_a=None, golpe_b=None, max_turnos=500):
    """Simula uma batalha. Retorna True se A vencer."""
    golpe_a = golpe_a or melhor_golpe(a, b)
    golpe_b = golpe_b or melhor_golpe(b, a)
    hp_a, hp_b = a.hp, b.hp
    for _ in range(max_turnos):
        a_primeiro = a.spe > b.spe or (a.spe == b.spe and rng.random() < 0.5)
        if a_primeiro:
            hp_b -= dano(*golpe_a, rng)
            if hp_b <= 0:
                return True
            hp_a -= dano(*golpe_b, rng)
            if hp_a <= 0:
                return False
        else:
            hp_a -= dano(*golpe_b, rng)
            if hp_a <= 0:
                return False
            hp_b -= dano(*golpe_a, rng)
            if hp_b <= 0:
                return True
    return hp_a / a.hp > hp_b / b.hp  # salvaguarda (não deve acontecer)


def simular_confronto(a, b, rng, n=21):
    """Repete a batalha n vezes e retorna quantas A venceu."""
    ga, gb = melhor_golpe(a, b), melhor_golpe(b, a)
    return sum(batalha(a, b, rng, ga, gb) for _ in range(n))
