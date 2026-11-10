"""Arena SVM: servidor do jogo para dois jogadores na mesma rede.

Uso (na pasta arena-svm):
    .venv\\Scripts\\python app\\servidor.py
Depois, abra o endereço mostrado no terminal. O segundo jogador entra pelo link da sala (mesma rede Wi-Fi).
"""
import json
import math
import os
import random
import socket
import string
import sys
import threading
import time
import uuid
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from flask import Flask, jsonify, request, send_from_directory

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(Path(__file__).parent))
from explicacao import Explicador  # noqa: E402
from features import Extrator  # noqa: E402
from simulador import batalha, candidatos, simular_confronto  # noqa: E402

PORTA = int(os.environ.get("PORTA", 5000))
# Endereço público, quando o jogo está hospedado na internet.
# Ordem: variável definida manualmente, endereço do Render e endereço do Hugging Face Spaces.
URL_PUBLICA = (os.environ.get("URL_PUBLICA") or os.environ.get("RENDER_EXTERNAL_URL")
               or (f"https://{os.environ['SPACE_HOST']}" if os.environ.get("SPACE_HOST") else None))
SALA_EXPIRA_S = 2 * 60 * 60        # salas sem atividade por 2 horas são removidas
MAX_SALAS = 500
N_SIMULACOES = 201

pk = pd.read_csv(RAIZ / "data/processed/pokemon.csv")
info = pk.set_index("pokeapi_id")
extrator = Extrator(pk)
modelo = joblib.load(RAIZ / "modelos/svm_duelo_v2.joblib")
COLUNAS = json.load(open(RAIZ / "modelos/svm_duelo_v2.json"))["features"]
batalhas_base = pd.read_csv(RAIZ / "data/processed/batalhas.csv")
explicador = Explicador(modelo, COLUNAS, batalhas_base, info["name"])

# Confrontos que existem na base: (a_id, b_id) -> grupo, vitórias de A e nº de simulações.
# Guarda as duas ordens (A×B e B×A), invertendo as vitórias, para achar o confronto de qualquer lado.
N_SIM_BASE = 21
HISTORICO = {}
for r in batalhas_base.itertuples():
    HISTORICO.setdefault((r.a_id, r.b_id), (r.grupo, r.vitorias_a, False))
    HISTORICO.setdefault((r.b_id, r.a_id), (r.grupo, N_SIM_BASE - r.vitorias_a, True))


def historico(a_id, b_id, favorito_svm):
    """Diz se o confronto estava na base (treino, teste ou misto) e o que aconteceu lá."""
    achado = HISTORICO.get((a_id, b_id))
    if achado is None:
        return {"situacao": "inedita"}
    grupo, vit_a, invertido = achado
    fav = "a" if vit_a > N_SIM_BASE / 2 else "b"
    return {"situacao": grupo, "vitorias_a": int(vit_a), "n": N_SIM_BASE, "favorito": fav,
            "invertido": invertido, "ia_concorda": fav == favorito_svm}

app = Flask(__name__, static_folder=str(Path(__file__).parent / "static"), static_url_path="/static")
salas = {}
trava = threading.Lock()


def ip_local():
    """IP do computador na rede local (para o segundo jogador entrar)."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except OSError:
        return "127.0.0.1"


def pokemon_publico(pid):
    r = info.loc[pid]
    return {"id": int(pid), "nome": r["name"], "geracao": int(r["Generation"]),
            "tipos": [t for t in (r["Type 1"], r["Type 2"]) if isinstance(t, str)],
            "atributos": {a: int(r[a]) for a in ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]},
            "total": int(r["Total"]), "lendario": bool(r["is_legendary"] or r["is_mythical"])}


LISTA = [pokemon_publico(pid) for pid in info.index]


def endereco_base():
    """Endereço que o outro jogador deve abrir: o público (online) ou o IP da rede local."""
    return URL_PUBLICA or f"http://{ip_local()}:{PORTA}"


def limpar_salas():
    """Remove salas sem atividade (chamar com a trava). Evita acúmulo quando o jogo está público."""
    agora = time.time()
    for c in [c for c, sl in salas.items() if agora - sl["ativa"] > SALA_EXPIRA_S]:
        del salas[c]


def novo_codigo():
    while True:
        c = "".join(random.choices(string.ascii_uppercase.replace("O", "").replace("I", "") + "23456789", k=4))
        if c not in salas:
            return c


def estado_sala(sala, token):
    eu = next((k for k, j in sala["jogadores"].items() if j["token"] == token), None)
    if eu is None and token in sala["espectadores"]:
        eu = "espectador"
    jogadores = {}
    for slot, j in sala["jogadores"].items():
        revelar = slot == eu or sala["batalha"] is not None
        jogadores[slot] = {"nome": j["nome"], "pronto": j["pronto"], "escolheu": j["pokemon"] is not None,
                           "pokemon": pokemon_publico(j["pokemon"]) if (revelar and j["pokemon"]) else None}
    return {"codigo": sala["codigo"], "eu": eu, "jogadores": jogadores, "batalha": sala["batalha"],
            "espectadores": len(sala["espectadores"]), "versao": sala["versao"],
            "link": f"{endereco_base()}/?sala={sala['codigo']}", "online": URL_PUBLICA is not None}


def rodar_batalha(sala):
    """Previsão do SVM + 201 simulações + uma batalha detalhada para animar."""
    a_id, b_id = sala["jogadores"]["a"]["pokemon"], sala["jogadores"]["b"]["pokemon"]
    la, lb = extrator.lutador(a_id), extrator.lutador(b_id)
    x = pd.DataFrame([extrator.linha(a_id, b_id)])[COLUNAS]
    score = float(modelo.decision_function(x)[0])
    rng = np.random.default_rng()
    vitorias_a = simular_confronto(la, lb, rng, N_SIMULACOES)
    eventos = []
    venceu_a = batalha(la, lb, rng, eventos=eventos)
    sala["batalha"] = {
        "id": uuid.uuid4().hex[:8],
        "a": pokemon_publico(a_id) | {"hp_max": la.hp, "golpes": [g.nome for g in candidatos(la, lb)[:4]]},
        "b": pokemon_publico(b_id) | {"hp_max": lb.hp, "golpes": [g.nome for g in candidatos(lb, la)[:4]]},
        "svm": {"favorito": "a" if score > 0 else "b", "score": round(score, 2),
                # confiança apresentada: transformação logística do score (não calibrada)
                "confianca": round(1 / (1 + math.exp(-abs(score) * 1.5)), 2),
                "explicacao": explicador.explicar(x)},
        "historico": historico(a_id, b_id, "a" if score > 0 else "b"),
        "simulador": {"vitorias_a": vitorias_a, "n": N_SIMULACOES,
                      "favorito": "a" if vitorias_a > N_SIMULACOES / 2 else "b"},
        "eventos": eventos,
        "vencedor": "a" if venceu_a else "b",
    }


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.get("/api/pokemon")
def lista_pokemon():
    return jsonify(LISTA)


@app.post("/api/salas")
def criar_sala():
    nome = (request.get_json(silent=True) or {}).get("nome") or "Jogador 1"
    with trava:
        limpar_salas()
        if len(salas) >= MAX_SALAS:
            return jsonify({"erro": "Muitas salas abertas no momento. Tente de novo em alguns minutos."}), 503
        codigo = novo_codigo()
        token = uuid.uuid4().hex
        salas[codigo] = {"codigo": codigo, "criada": time.time(), "ativa": time.time(), "versao": 1, "batalha": None, "espectadores": set(),
                         "jogadores": {"a": {"nome": nome[:20], "token": token, "pokemon": None, "pronto": False}}}
        return jsonify({"codigo": codigo, "token": token, "estado": estado_sala(salas[codigo], token)})


def pegar_sala(codigo):
    sala = salas.get(codigo.upper())
    if sala is None:
        return None, (jsonify({"erro": "Sala não encontrada. Confira o código."}), 404)
    sala["ativa"] = time.time()
    return sala, None


@app.post("/api/salas/<codigo>/entrar")
def entrar(codigo):
    corpo = request.get_json(silent=True) or {}
    with trava:
        sala, erro = pegar_sala(codigo)
        if erro:
            return erro
        token = corpo.get("token")
        if token and (any(j["token"] == token for j in sala["jogadores"].values()) or token in sala["espectadores"]):
            return jsonify({"codigo": sala["codigo"], "token": token, "estado": estado_sala(sala, token)})
        token = uuid.uuid4().hex
        if "b" in sala["jogadores"]:          # sala cheia: entra como espectador
            sala["espectadores"].add(token)
            sala["versao"] += 1
            return jsonify({"codigo": sala["codigo"], "token": token, "estado": estado_sala(sala, token)})
        sala["jogadores"]["b"] = {"nome": (corpo.get("nome") or "Jogador 2")[:20], "token": token,
                                  "pokemon": None, "pronto": False}
        sala["versao"] += 1
        return jsonify({"codigo": sala["codigo"], "token": token, "estado": estado_sala(sala, token)})


@app.get("/api/salas/<codigo>")
def ver_sala(codigo):
    sala, erro = pegar_sala(codigo)
    return erro or jsonify(estado_sala(sala, request.args.get("token")))


def jogador_da_sala(sala, token):
    return next((j for j in sala["jogadores"].values() if j["token"] == token), None)


@app.post("/api/salas/<codigo>/escolher")
def escolher(codigo):
    corpo = request.get_json(silent=True) or {}
    with trava:
        sala, erro = pegar_sala(codigo)
        if erro:
            return erro
        j = jogador_da_sala(sala, corpo.get("token"))
        if j is None:
            return jsonify({"erro": "Jogador não está nesta sala."}), 403
        pid = int(corpo["pokemon_id"])
        if pid not in info.index:
            return jsonify({"erro": "Pokémon inválido."}), 400
        j["pokemon"], j["pronto"] = pid, False
        sala["versao"] += 1
        return jsonify(estado_sala(sala, j["token"]))


@app.post("/api/salas/<codigo>/pronto")
def pronto(codigo):
    corpo = request.get_json(silent=True) or {}
    with trava:
        sala, erro = pegar_sala(codigo)
        if erro:
            return erro
        j = jogador_da_sala(sala, corpo.get("token"))
        if j is None or j["pokemon"] is None:
            return jsonify({"erro": "Escolha um Pokémon antes."}), 400
        j["pronto"] = True
        if len(sala["jogadores"]) == 2 and all(x["pronto"] for x in sala["jogadores"].values()):
            rodar_batalha(sala)
        sala["versao"] += 1
        return jsonify(estado_sala(sala, j["token"]))


@app.post("/api/salas/<codigo>/revanche")
def revanche(codigo):
    """Volta para a escolha mantendo os Pokémon (cada um pode trocar ou confirmar de novo)."""
    corpo = request.get_json(silent=True) or {}
    with trava:
        sala, erro = pegar_sala(codigo)
        if erro:
            return erro
        if jogador_da_sala(sala, corpo.get("token")) is None:
            return jsonify({"erro": "Jogador não está nesta sala."}), 403
        if sala["batalha"] is not None:
            sala["batalha"] = None
            for x in sala["jogadores"].values():
                x["pronto"] = False
            sala["versao"] += 1
        return jsonify(estado_sala(sala, corpo.get("token")))


if __name__ == "__main__":
    ip = ip_local()
    print("\n  Arena SVM rodando!")
    print(f"  Neste computador:            http://localhost:{PORTA}")
    print(f"  Outro aparelho (mesma rede): http://{ip}:{PORTA}")
    print("  Se o Windows perguntar sobre o firewall, permita o acesso em redes privadas.\n")
    app.run(host="0.0.0.0", port=PORTA, debug=False, threaded=True)
