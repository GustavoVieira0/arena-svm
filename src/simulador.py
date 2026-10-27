"""Simulador de batalhas 1 contra 1 baseado na fórmula de dano dos jogos principais de Pokémon.

Dois modos de golpes:
- "reais" (padrão): cada Pokémon usa os golpes de dano que aprende de verdade em algum jogo (dados do PokéAPI), com
  poder, tipo, categoria, precisão, prioridade, número de acertos, dano de retorno, roubo de vida, taxa de crítico e
  mudanças de atributo (ex.: Draco Meteor reduz o próprio Sp. Atk em 2 níveis).
- "simples" (versão 1 do projeto): um golpe de 80 de poder por tipo do Pokémon e um golpe Normal de 70.

Regras gerais (simplificações documentadas):
- Nível 50, IV 31, EV 0, natureza neutra. Sem habilidades, itens, clima, status (paralisia, queimadura...),
  confusão, recuo (flinch) nem trocas.
- Golpes que exigem carregar ou recarregar (Solar Beam, Hyper Beam, Roar of Time...), golpes de autodestruição e
  golpes com condição especial (Fake Out, Dream Eater...) são excluídos.
- A cada turno, cada Pokémon escolhe o golpe com maior dano esperado (precisão × dano médio, limitado ao HP
  restante do alvo). Em caso de empate, prefere o golpe com maior prioridade.
- Ordem: maior prioridade primeiro; depois maior Velocidade (com modificadores); empate é sorteado a cada turno.
- Dano = (((2 × Nível / 5 + 2) × Poder × Ataque / Defesa) / 50 + 2) × Aleatório(0,85–1,00) × Crítico(1,5)
         × STAB(1,5) × Eficácia de tipo     (fórmula da 5ª geração em diante)
- Se nenhum golpe afeta o alvo, usa Struggle (50 de poder, sem tipo, perde 1/4 do HP máximo).
"""
import math
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
RAW = RAIZ / "data/raw/pokeapi"
NIVEL = 50
CHANCE_CRITICO = {0: 1 / 24, 1: 1 / 8, 2: 1 / 2}   # por estágio de crítico (3+ = sempre)
MULT_CRITICO = 1.5
STATS = {2: "atk", 3: "df", 4: "spa", 5: "spd", 6: "spe"}

# Golpes excluídos: carregam/recarregam (via flags), autodestruição, condicionais, poder variável ou mecânica
# que o simulador não representa.
EXCLUIDOS = {
    "explosion", "self-destruct", "misty-explosion", "fake-out", "first-impression", "dream-eater", "belch",
    "last-resort", "synchronoise", "focus-punch", "spit-up", "natural-gift", "fling", "future-sight", "doom-desire",
    "shell-trap", "burn-up", "double-shock", "steel-roller", "sky-drop", "bide", "hidden-power", "weather-ball",
    "eruption", "water-spout", "dragon-energy", "outrage", "petal-dance", "thrash", "raging-fury", "rollout",
    "ice-ball", "fury-cutter", "echoed-voice", "uproar", "present", "beat-up", "snore", "sleep-talk", "struggle",
    "round", "pollen-puff", "dream-eater", "spectral-thief", "upper-hand", "poltergeist", "hyperspace-fury",
}
CUSTO_HP = {"mind-blown": 0.5, "steel-beam": 0.5, "chloroblast": 0.5}            # perde 50% do HP máximo
ACERTOS = {"population-bomb": (1, 10)}                                         # golpes sem meta no PokéAPI
PODER_MEDIO_ACERTO = {"triple-axel": 40, "triple-kick": 20}                    # poder cresce a cada acerto


def carregar_tabela_tipos():
    tipos = pd.read_csv(RAW / "types.csv").set_index("id")["identifier"].str.capitalize()
    ef = pd.read_csv(RAW / "type_efficacy.csv")
    return tipos, {(tipos[r.damage_type_id], tipos[r.target_type_id]): r.damage_factor / 100 for r in ef.itertuples()}


NOMES_TIPOS, TABELA_TIPOS = carregar_tabela_tipos()


def eficacia(tipo_golpe, tipo1, tipo2=None):
    """Multiplicador de tipo de um golpe contra um defensor (0, 0,25, 0,5, 1, 2 ou 4). None = sem tipo."""
    if tipo_golpe is None:
        return 1.0
    m = TABELA_TIPOS.get((tipo_golpe, tipo1), 1.0)
    if isinstance(tipo2, str):
        m *= TABELA_TIPOS.get((tipo_golpe, tipo2), 1.0)
    return m


@dataclass(frozen=True)
class Golpe:
    nome: str
    tipo: str | None
    poder: float
    fisico: bool
    precisao: float = 1.0
    prioridade: int = 0
    acertos: tuple = (1, 1)
    dreno: float = 0.0              # >0 recupera fração do dano causado; <0 dano de retorno
    estagio_critico: int = 0
    muda_usuario: tuple = ()        # ((stat, delta), ...) sempre que acerta
    muda_alvo: tuple = ()           # ((stat, delta), ...) com chance `chance_alvo`
    chance_alvo: float = 0.0
    custo_hp: float = 0.0           # fração do HP máximo perdida ao usar

    @property
    def acertos_medios(self):
        lo, hi = self.acertos
        if (lo, hi) == (2, 5):
            return 3.1                  # distribuição oficial: 35% 2, 35% 3, 15% 4, 15% 5
        return (lo + hi) / 2


STRUGGLE = Golpe("struggle", None, 50, True, custo_hp=0.25)


@lru_cache(maxsize=1)
def _tabela_golpes():
    """Dicionário pokemon_id -> tupla de Golpe (golpes de dano aprendidos em qualquer jogo)."""
    mv = pd.read_csv(RAW / "moves.csv")
    meta = pd.read_csv(RAW / "move_meta.csv").set_index("move_id")
    sc = pd.read_csv(RAW / "move_meta_stat_changes.csv")
    flags = pd.read_csv(RAW / "move_flag_map.csv")
    carrega = set(flags.loc[flags.move_flag_id.isin([2, 3]), "move_id"])        # charge / recharge

    mv = mv[mv.damage_class_id.isin([2, 3]) & mv.power.notna() & ~mv.id.isin(carrega) & ~mv.identifier.isin(EXCLUIDOS)]
    golpes = {}
    for r in mv.itertuples():
        m = meta.loc[r.id] if r.id in meta.index else None
        mudancas = tuple((STATS[s], int(d)) for s, d in sc.loc[sc.move_id == r.id, ["stat_id", "change"]].values
                         if s in STATS)
        cat = None if m is None else m.meta_category_id
        acertos = ACERTOS.get(r.identifier) or (
            (int(m.min_hits), int(m.max_hits)) if m is not None and pd.notna(m.min_hits) else (1, 1))
        golpes[r.id] = Golpe(
            nome=r.identifier,
            tipo=NOMES_TIPOS[r.type_id],
            poder=PODER_MEDIO_ACERTO.get(r.identifier, r.power),
            fisico=r.damage_class_id == 2,
            precisao=1.0 if pd.isna(r.accuracy) else r.accuracy / 100,
            prioridade=int(r.priority),
            acertos=acertos,
            dreno=0.0 if m is None else m.drain / 100,
            estagio_critico=0 if m is None else int(m.crit_rate),
            muda_usuario=mudancas if cat == 7 else (),
            muda_alvo=mudancas if cat == 6 else (),
            chance_alvo=0.0 if m is None else (m.stat_chance or 100) / 100,
            custo_hp=CUSTO_HP.get(r.identifier, 0.0),
        )

    # métodos válidos: nível, ovo, tutor, TM/TR, ovo com Light Ball, troca de forma, Zygarde Cube
    # (exclui Pikachu surfista do Stadium, golpes "sombrios" de Colosseum/XD e o método "train")
    pm = pd.read_csv(RAW / "pokemon_moves.csv", usecols=["pokemon_id", "move_id", "pokemon_move_method_id"])
    pm = pm[pm.pokemon_move_method_id.isin([1, 2, 3, 4, 6, 10, 11]) & pm.move_id.isin(golpes)]
    pm = pm[["pokemon_id", "move_id"]].drop_duplicates()
    por_pokemon = {pid: tuple(golpes[m] for m in g.move_id) for pid, g in pm.groupby("pokemon_id")}

    # formas sem lista própria (ex.: Megas novas) usam os golpes da forma padrão da espécie
    poke = pd.read_csv(RAW / "pokemon.csv")
    padrao = poke[poke.is_default == 1].set_index("species_id")["id"]
    for r in poke.itertuples():
        if r.id not in por_pokemon and padrao.get(r.species_id) in por_pokemon:
            por_pokemon[r.id] = por_pokemon[padrao[r.species_id]]
    return por_pokemon


def golpes_simples(tipos, fisico):
    g = [Golpe(f"golpe-{t.lower()}", t, 80, fisico) for t in tipos]
    if "Normal" not in tipos:
        g.append(Golpe("golpe-normal", "Normal", 70, fisico))
    return tuple(g)


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
    golpes: tuple = field(default=(), repr=False)

    @classmethod
    def de_linha(cls, r, golpes="reais"):
        """r: linha de data/processed/pokemon.csv (dict ou Series com 'name', 'pokeapi_id', atributos e tipos)."""
        calc = lambda base: math.floor((2 * base + 31) * NIVEL / 100) + 5
        hp = 1 if r["HP"] == 1 else math.floor((2 * r["HP"] + 31) * NIVEL / 100) + NIVEL + 10  # Shedinja: sempre 1
        tipos = (r["Type 1"],) + ((r["Type 2"],) if isinstance(r["Type 2"], str) else ())
        lut = cls(r["name"], tipos, hp, calc(r["Attack"]), calc(r["Defense"]), calc(r["Sp. Atk"]),
                  calc(r["Sp. Def"]), calc(r["Speed"]))
        if golpes == "simples":
            lut.golpes = golpes_simples(tipos, lut.atk >= lut.spa)
        else:
            lut.golpes = _tabela_golpes().get(int(r["pokeapi_id"]), ())
        return lut


def mult_estagio(e):
    return (2 + e) / 2 if e >= 0 else 2 / (2 - e)


def dano_base(golpe, atacante, defensor, est_atk=None, est_def=None, critico=False):
    """Parte determinística da fórmula (antes de aleatório, crítico, STAB e tipo)."""
    est_atk, est_def = est_atk or {}, est_def or {}
    s_atk, s_def = ("atk", "df") if golpe.fisico else ("spa", "spd")
    e_a, e_d = est_atk.get(s_atk, 0), est_def.get(s_def, 0)
    if critico:  # crítico ignora redução do atacante e aumento do defensor
        e_a, e_d = max(e_a, 0), min(e_d, 0)
    a = getattr(atacante, s_atk) * mult_estagio(e_a)
    d = getattr(defensor, s_def) * mult_estagio(e_d)
    return math.floor(math.floor(math.floor(2 * NIVEL / 5 + 2) * golpe.poder * a / d) / 50) + 2


def multiplicador(golpe, atacante, defensor):
    stab = 1.5 if golpe.tipo in atacante.tipos else 1.0
    return stab * eficacia(golpe.tipo, *defensor.tipos)


def candidatos(atacante, defensor, n=8):
    """Reduz a lista de golpes aos mais promissores contra este adversário (inclui os de prioridade)."""
    opcoes = []
    for g in atacante.golpes:
        mult = multiplicador(g, atacante, defensor)
        if mult > 0:
            nota = dano_base(g, atacante, defensor) * mult * g.precisao * g.acertos_medios
            opcoes.append((nota, g))
    if not opcoes:
        return (STRUGGLE,)
    opcoes.sort(key=lambda x: -x[0])
    melhores = [g for _, g in opcoes[:n]]
    melhores += [g for _, g in opcoes if g.prioridade > 0 and g not in melhores][:2]
    return tuple(melhores)


def escolher(cands, atacante, defensor, est_a, est_d, hp_alvo):
    def valor(g):
        esperado = dano_base(g, atacante, defensor, est_a, est_d) * 0.925 * multiplicador(g, atacante, defensor)
        return (g.precisao * min(esperado * g.acertos_medios, hp_alvo), g.prioridade)
    return max(cands, key=valor)


def _sortear_acertos(g, rng):
    lo, hi = g.acertos
    if (lo, hi) == (1, 1):
        return 1
    if (lo, hi) == (2, 5):
        return int(rng.choice([2, 3, 4, 5], p=[.35, .35, .15, .15]))
    return int(rng.integers(lo, hi + 1))


def usar_golpe(g, atacante, defensor, est_a, est_d, rng):
    """Executa o golpe. Retorna (dano causado no alvo, variação de HP do atacante); dano None = errou."""
    hp_atacante = -math.floor(atacante.hp * g.custo_hp)
    if rng.random() >= g.precisao:
        return None, hp_atacante
    mult = multiplicador(g, atacante, defensor)
    total = 0
    for _ in range(_sortear_acertos(g, rng)):
        crit = g.estagio_critico >= 3 or rng.random() < CHANCE_CRITICO[min(g.estagio_critico, 2)]
        base = dano_base(g, atacante, defensor, est_a, est_d, crit)
        d = math.floor(math.floor(base * rng.integers(85, 101) / 100 * (MULT_CRITICO if crit else 1)) * mult)
        total += max(1, d)
    if g.dreno:
        hp_atacante += math.floor(total * g.dreno) if g.dreno > 0 else -max(1, math.floor(total * -g.dreno))
    for stat, delta in g.muda_usuario:
        est_a[stat] = max(-6, min(6, est_a.get(stat, 0) + delta))
    if g.muda_alvo and rng.random() < g.chance_alvo:
        for stat, delta in g.muda_alvo:
            est_d[stat] = max(-6, min(6, est_d.get(stat, 0) + delta))
    return total, hp_atacante


def batalha(a, b, rng, cand_a=None, cand_b=None, max_turnos=200, registro=None):
    """Simula uma batalha. Retorna True se A vencer. `registro` (lista) recebe a narração turno a turno."""
    cand_a = cand_a or candidatos(a, b)
    cand_b = cand_b or candidatos(b, a)
    hp = {"a": a.hp, "b": b.hp}
    est = {"a": {}, "b": {}}
    lut = {"a": a, "b": b}
    cands = {"a": cand_a, "b": cand_b}
    outro = {"a": "b", "b": "a"}
    for turno in range(1, max_turnos + 1):
        escolha = {k: escolher(cands[k], lut[k], lut[outro[k]], est[k], est[outro[k]], hp[outro[k]]) for k in "ab"}
        vel = {k: lut[k].spe * mult_estagio(est[k].get("spe", 0)) for k in "ab"}
        chave = {k: (escolha[k].prioridade, vel[k]) for k in "ab"}
        primeiro = "a" if chave["a"] > chave["b"] or (chave["a"] == chave["b"] and rng.random() < 0.5) else "b"
        for k in (primeiro, outro[primeiro]):
            alvo = outro[k]
            dano, dhp = usar_golpe(escolha[k], lut[k], lut[alvo], est[k], est[alvo], rng)
            hp[alvo] -= dano or 0
            hp[k] = min(lut[k].hp, hp[k] + dhp)
            if registro is not None:
                efeito = "errou!" if dano is None else f"{dano} de dano"
                registro.append(f"T{turno}: {lut[k].nome} usa {escolha[k].nome} → {efeito} "
                                f"({lut[alvo].nome}: {max(hp[alvo], 0)}/{lut[alvo].hp} HP)")
            if hp[alvo] <= 0:
                return alvo == "b"
            if hp[k] <= 0:       # nocauteado pelo próprio golpe (retorno/custo)
                return k == "b"
    return hp["a"] / a.hp > hp["b"] / b.hp  # salvaguarda


def simular_confronto(a, b, rng, n=21):
    """Repete a batalha n vezes e retorna quantas A venceu."""
    ca, cb = candidatos(a, b), candidatos(b, a)
    return sum(batalha(a, b, rng, ca, cb) for _ in range(n))
