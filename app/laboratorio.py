"""Laboratório: personagem criado pelo usuário × Pokémon, com previsão ao vivo e o corte 2D da fronteira do SVM.

Um "lado" da batalha é descrito por um dicionário:
  {"id": 25}                                     → Pokémon da base (golpes reais)
  {"custom": {"nome": ..., "tipos": [...], "atributos": {...}, "sprite": 25}}
                                                 → personagem criado (golpes genéricos dos seus tipos)
"""
import numpy as np
import pandas as pd

from features import linha_de
from simulador import NOMES_TIPOS, Lutador, batalha, candidatos, simular_confronto

ATRIBUTOS = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]
TIPOS = sorted(set(NOMES_TIPOS.tolist()) - {"Stellar", "Unknown", "Shadow"})
# eixos permitidos no corte 2D: diferenças de atributos (A − B)
EIXOS = {f"dif_{a}": a for a in ATRIBUTOS}
FAIXA, PASSOS = 200, 17          # 17 × 17 pontos (suavizados na tela): leve o bastante para atualizar ao vivo


class ErroEntrada(ValueError):
    pass


def _custom(c):
    """Valida e converte um personagem criado numa linha no formato de pokemon.csv."""
    if not isinstance(c, dict):
        raise ErroEntrada("Personagem inválido.")
    tipos = [t for t in (c.get("tipos") or []) if t]
    if not 1 <= len(tipos) <= 2 or any(t not in TIPOS for t in tipos) or len(set(tipos)) != len(tipos):
        raise ErroEntrada("Escolha um ou dois tipos diferentes.")
    attrs = c.get("atributos") or {}
    try:
        valores = {a: int(attrs[a]) for a in ATRIBUTOS}
    except (KeyError, TypeError, ValueError):
        raise ErroEntrada("Atributos inválidos.")
    if any(not 1 <= v <= 255 for v in valores.values()):
        raise ErroEntrada("Cada atributo deve estar entre 1 e 255.")
    nome = str(c.get("nome") or "Meu personagem").strip()[:20] or "Meu personagem"
    return {"name": nome, "Type 1": tipos[0], "Type 2": tipos[1] if len(tipos) > 1 else None,
            "pokeapi_id": -1, **valores}


class Laboratorio:
    def __init__(self, extrator, modelo, colunas, explicador, info):
        self.extrator, self.modelo, self.colunas = extrator, modelo, list(colunas)
        self.explicador, self.info = explicador, info

    def lado(self, spec):
        """Retorna (linha de atributos, lutador, dados públicos) de um lado da batalha."""
        if not isinstance(spec, dict):
            raise ErroEntrada("Escolha os dois lados da batalha.")
        if "id" in spec:
            pid = int(spec["id"])
            if pid not in self.info.index:
                raise ErroEntrada("Pokémon inválido.")
            r = self.info.loc[pid]
            publico = {"id": pid, "nome": r["name"], "sprite": pid, "criado": False,
                       "tipos": [t for t in (r["Type 1"], r["Type 2"]) if isinstance(t, str)],
                       "atributos": {a: int(r[a]) for a in ATRIBUTOS}}
            return r, self.extrator.lutador(pid), publico
        linha = _custom(spec.get("custom"))
        luta = Lutador.de_linha(linha, golpes="simples")
        sprite = int(spec["custom"].get("sprite") or 0)
        publico = {"id": None, "nome": linha["name"], "sprite": sprite if sprite in self.info.index else None,
                   "criado": True, "tipos": [t for t in (linha["Type 1"], linha["Type 2"]) if t],
                   "atributos": {a: linha[a] for a in ATRIBUTOS}}
        return pd.Series(linha), luta, publico

    def prever(self, spec_a, spec_b, eixo_x="dif_Speed", eixo_y="dif_Attack"):
        if eixo_x not in EIXOS or eixo_y not in EIXOS or eixo_x == eixo_y:
            raise ErroEntrada("Eixos inválidos.")
        ra, la, pa = self.lado(spec_a)
        rb, lb, pb = self.lado(spec_b)
        x = pd.DataFrame([linha_de(ra, rb, la, lb)])[self.colunas]
        score = float(self.modelo.decision_function(x)[0])

        # corte 2D: varia só os dois eixos; as outras 13 variáveis ficam com os valores desta batalha
        valores = np.linspace(-FAIXA, FAIXA, PASSOS)
        gx, gy = np.meshgrid(valores, valores)
        grade = pd.DataFrame(np.repeat(x.values, PASSOS * PASSOS, axis=0), columns=self.colunas)
        grade[eixo_x], grade[eixo_y] = gx.ravel(), gy.ravel()
        scores = self.modelo.decision_function(grade).reshape(PASSOS, PASSOS)

        return {
            "a": pa, "b": pb, "score": round(score, 3), "favorito": "a" if score > 0 else "b",
            "explicacao": self.explicador.explicar(x),
            "golpes": {"a": [g.nome for g in candidatos(la, lb)[:3]], "b": [g.nome for g in candidatos(lb, la)[:3]]},
            "fronteira": {"eixo_x": eixo_x, "eixo_y": eixo_y, "valores": valores.round(1).tolist(),
                          "scores": scores.round(3).tolist(),
                          "ponto": [float(x[eixo_x].iloc[0]), float(x[eixo_y].iloc[0])]},
        }

    def simular(self, spec_a, spec_b, n=201):
        _, la, pa = self.lado(spec_a)
        _, lb, pb = self.lado(spec_b)
        rng = np.random.default_rng()
        vitorias_a = simular_confronto(la, lb, rng, n)
        narracao = []
        venceu_a = batalha(la, lb, rng, registro=narracao)
        return {"vitorias_a": vitorias_a, "n": n, "favorito": "a" if vitorias_a > n / 2 else "b",
                "narracao": narracao[:30], "vencedor_exemplo": "a" if venceu_a else "b"}
