"""Monta em deploy/_pacote/ os arquivos que vão para o Hugging Face Spaces (só o necessário para o jogo).

Uso:  python deploy/montar_pacote.py
O arquivo de golpes (11 MB) é compactado, porque o Spaces limita arquivos comuns a 10 MB.
"""
import gzip
import shutil
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
DESTINO = RAIZ / "deploy" / "_pacote"

ARQUIVOS = ["app/servidor.py", "app/explicacao.py", "src/simulador.py", "src/features.py",
            "data/processed/pokemon.csv", "data/processed/batalhas.csv",
            "modelos/svm_duelo_v2.joblib", "modelos/svm_duelo_v2.json"]
PASTAS = ["app/static"]
RAW = ["moves.csv", "move_meta.csv", "move_meta_stat_changes.csv", "move_flag_map.csv", "pokemon.csv",
       "types.csv", "type_efficacy.csv"]


def main():
    for item in DESTINO.glob("*"):                      # limpa, preservando o .git do pacote
        if item.name != ".git":
            shutil.rmtree(item) if item.is_dir() else item.unlink()
    DESTINO.mkdir(parents=True, exist_ok=True)
    for rel in ARQUIVOS + [f"data/raw/pokeapi/{n}" for n in RAW]:
        (DESTINO / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(RAIZ / rel, DESTINO / rel)
    for rel in PASTAS:
        shutil.copytree(RAIZ / rel, DESTINO / rel)
    with open(RAIZ / "data/raw/pokeapi/pokemon_moves.csv", "rb") as f, \
            gzip.GzipFile(DESTINO / "data/raw/pokeapi/pokemon_moves.csv.gz", "wb", mtime=0) as g:
        shutil.copyfileobj(f, g)
    for nome in ["Dockerfile", "requirements-deploy.txt", "README.md"]:
        shutil.copy2(RAIZ / "deploy/hf" / nome, DESTINO / nome)
    total = sum(p.stat().st_size for p in DESTINO.rglob("*") if p.is_file() and ".git" not in p.parts)
    maior = max((p for p in DESTINO.rglob("*") if p.is_file() and ".git" not in p.parts), key=lambda p: p.stat().st_size)
    print(f"Pacote em {DESTINO}: {total / 1e6:.1f} MB | maior arquivo: {maior.name} ({maior.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
