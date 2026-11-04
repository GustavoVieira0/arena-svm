"""Explica a previsão do SVM para uma batalha, usando os conceitos do próprio SVM.

Para o kernel RBF, a decisão é
    f(x) = Σ_i (α_i · y_i) · exp(−γ · ‖x_i − x‖²) + b
em que x_i são os VETORES DE SUPORTE (batalhas do treino que definem a fronteira). Portanto:
- score f(x): distância (com sinal) até a fronteira de decisão (hiperplano no espaço do kernel).
  |f(x)| < 1 → a batalha está DENTRO DA MARGEM (zona de dúvida).
- cada vetor de suporte contribui com (α_i · y_i) · K(x_i, x): as batalhas de treino parecidas com a atual
  e com peso alto são as que mais "puxam" a decisão.
- a influência de cada fator é estimada por neutralização: o grupo de features é trocado pela média do treino
  (0 depois da padronização) e mede-se quanto o score muda. É uma aproximação local (o modelo não é linear).
"""
import numpy as np
import pandas as pd

GRUPOS = {
    "Velocidade": ["dif_Speed"],
    "Poder de ataque": ["dif_Attack", "dif_Sp. Atk"],
    "Defesa": ["dif_Defense", "dif_Sp. Def"],
    "HP": ["dif_HP"],
    "Vantagem de tipo": ["log_mult_a", "log_mult_b"],
    "Dano dos golpes": ["frac_a", "frac_b", "nocaute_a", "nocaute_b", "dif_nocaute"],
    "Golpe de prioridade": ["prioridade_a", "prioridade_b"],
}


class Explicador:
    def __init__(self, modelo, colunas, batalhas: pd.DataFrame, nomes: pd.Series):
        self.scaler, self.svc = modelo[0], modelo[-1]
        self.colunas = list(colunas)
        self.gamma = self.svc._gamma                       # valor numérico de gamma usado no treino
        self.sv = self.svc.support_vectors_                # vetores de suporte (já padronizados)
        self.coef = self.svc.dual_coef_[0]                 # α_i · y_i (positivo puxa para "A vence")
        self.b = float(self.svc.intercept_[0])
        # o modelo v2 foi treinado com as batalhas do grupo "treino", nesta ordem (notebook 02)
        treino = batalhas[batalhas.grupo == "treino"].reset_index(drop=True)
        self.sv_batalhas = treino.loc[self.svc.support_, ["a_id", "b_id", "a_vence", "prob_a"]].reset_index(drop=True)
        self.nomes = nomes
        self.idx = {g: [self.colunas.index(c) for c in cols] for g, cols in GRUPOS.items()}

    def _score(self, xs):
        return float(self.svc.decision_function(xs.reshape(1, -1))[0])

    def explicar(self, x: pd.DataFrame, top=4):
        xs = self.scaler.transform(x[self.colunas])[0]
        score = self._score(xs)

        fatores = []
        for grupo, idx in self.idx.items():
            neutro = xs.copy()
            neutro[idx] = 0.0                                  # média do treino
            fatores.append({"fator": grupo, "efeito": round(score - self._score(neutro), 3)})
        fatores.sort(key=lambda f: -abs(f["efeito"]))

        contrib = self.coef * np.exp(-self.gamma * ((self.sv - xs) ** 2).sum(axis=1))
        ordem = np.argsort(-np.abs(contrib))[:top]
        vetores = []
        for i in ordem:
            r = self.sv_batalhas.loc[i]
            vetores.append({
                "a_id": int(r.a_id), "b_id": int(r.b_id),
                "a_nome": self.nomes[r.a_id], "b_nome": self.nomes[r.b_id],
                "vencedor": "a" if r.a_vence else "b", "prob_a": float(r.prob_a),
                "contribuicao": round(float(contrib[i]), 3),
                "semelhanca": round(float(np.exp(-self.gamma * ((self.sv[i] - xs) ** 2).sum())), 3),
            })

        bruto = x[self.colunas].iloc[0]
        comparou = {
            "dif_velocidade": int(bruto["dif_Speed"]),
            "mult_tipo": {"a": round(2 ** bruto["log_mult_a"], 2), "b": round(2 ** bruto["log_mult_b"], 2)},
            "dano_turno": {"a": round(float(bruto["frac_a"]) * 100), "b": round(float(bruto["frac_b"]) * 100)},
            "nocaute": {"a": int(bruto["nocaute_a"]), "b": int(bruto["nocaute_b"])},
            "prioridade": {"a": bool(bruto["prioridade_a"]), "b": bool(bruto["prioridade_b"])},
        }
        return {
            "score": round(score, 3), "dentro_da_margem": abs(score) < 1, "intercepto": round(self.b, 3),
            "n_vetores_suporte": int(len(self.sv)), "fatores": fatores, "vetores": vetores, "comparou": comparou,
        }
