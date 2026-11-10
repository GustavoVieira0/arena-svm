"""Gera o folder (A4 paisagem, frente e verso, dobra ao meio) e os 6 cards do Instagram em HTML."""
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]   # pasta docs/
IMG = "../../img"   # caminho relativo às pastas folder/ e instagram/
SPR = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon"
REPO = "github.com/GustavoVieira0/arena-svm"
JOGO = "arena-svm.onrender.com"
FONTES = ('<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Inter:wght@400;600;700;800'
          '&display=swap" rel="stylesheet">')
CORES = """
:root { --fundo:#1b1f2e; --cartao:#262b3f; --borda:#3a4160; --texto:#eef1f8; --suave:#9aa3bf; --amarelo:#ffcb05;
        --azul:#3d7dca; --verde:#3fbf5f; --vermelho:#e2453c; --pixel:"Press Start 2P",monospace; }
* { box-sizing:border-box; margin:0; padding:0; }
body { font-family:Inter,system-ui,sans-serif; }
.px { font-family:var(--pixel); }
img.spr { image-rendering:pixelated; }
"""
MARCA = "Pokémon é marca registrada da Nintendo, Game Freak e Creatures. Projeto acadêmico, sem fins comerciais."

# ------------------------------------------------------------------ SVG: ideia do SVM (rua larga)
def svg_svm(w=520, h=330, claro=False):
    cor_txt = "#1b1f2e" if claro else "#eef1f8"
    a = [(70, 70), (120, 130), (60, 180), (150, 60), (110, 230), (175, 150), (50, 270), (190, 250)]
    b = [(420, 60), (360, 120), (450, 150), (390, 210), (470, 250), (330, 265), (440, 300), (345, 45)]
    sv_a, sv_b = {(175, 150), (190, 250)}, {(360, 120), (330, 265)}
    pts = "".join(f'<circle cx="{x}" cy="{y}" r="11" fill="#e07a5f"/>' +
                  (f'<circle cx="{x}" cy="{y}" r="18" fill="none" stroke="{cor_txt}" stroke-width="3"/>' if (x, y) in sv_a else "")
                  for x, y in a)
    pts += "".join(f'<circle cx="{x}" cy="{y}" r="11" fill="#6c8fd8"/>' +
                   (f'<circle cx="{x}" cy="{y}" r="18" fill="none" stroke="{cor_txt}" stroke-width="3"/>' if (x, y) in sv_b else "")
                   for x, y in b)
    return f'''<svg viewBox="0 0 {w} {h}" width="100%" xmlns="http://www.w3.org/2000/svg">
      <polygon points="215,0 305,0 345,{h} 255,{h}" fill="#ffcb05" opacity=".22"/>
      <line x1="215" y1="0" x2="255" y2="{h}" stroke="#ffcb05" stroke-width="3" stroke-dasharray="10 8"/>
      <line x1="305" y1="0" x2="345" y2="{h}" stroke="#ffcb05" stroke-width="3" stroke-dasharray="10 8"/>
      <line x1="260" y1="0" x2="300" y2="{h}" stroke="#ffcb05" stroke-width="6"/>{pts}</svg>'''


# ------------------------------------------------------------------ gráfico de barras
BARRAS = [("Vence o mais rápido", 67.8, "#7c86a8"), ("Vence o mais forte", 80.6, "#7c86a8"),
          ("IA (atributos e tipos)", 86.6, "#3d7dca"), ("IA + golpes de cada Pokémon", 92.6, "#3fbf5f")]


def barras(altura=58, fonte=26, cor_txt="#eef1f8", trilho="#151927"):
    out = ""
    for nome, v, cor in BARRAS:
        out += f'''<div style="margin-bottom:{altura * .38}px">
          <div style="font-size:{fonte}px;font-weight:600;color:{cor_txt};margin-bottom:6px">{nome}</div>
          <div style="background:{trilho};border-radius:10px;height:{altura}px;position:relative">
            <div style="width:{v}%;height:100%;background:{cor};border-radius:10px;display:flex;align-items:center;
                 justify-content:flex-end;padding-right:14px;font-family:var(--pixel);font-size:{fonte * .8}px;color:#fff">
              {str(v).replace(".", ",")}%</div></div></div>'''
    return out


# ------------------------------------------------------------------ Instagram (1080 × 1350)
CSS_IG = CORES + """
body { width:1080px; height:1350px; background:var(--fundo); color:var(--texto); overflow:hidden; }
.card { width:1080px; height:1350px; padding:80px 72px 70px; display:flex; flex-direction:column; position:relative;
        background:linear-gradient(180deg,#1b1f2e 0%,#232a44 100%); }
.topo { display:flex; justify-content:space-between; align-items:center; font-family:var(--pixel); font-size:22px; color:var(--suave); }
.topo b { color:var(--amarelo); }
h1 { font-family:var(--pixel); font-size:58px; line-height:1.6; margin:0 0 40px; }
h1 em { color:var(--amarelo); font-style:normal; }
h2 { font-family:var(--pixel); font-size:40px; line-height:1.6; margin:50px 0 34px; color:var(--amarelo); }
p { font-size:38px; line-height:1.45; margin-bottom:26px; }
p b, li b { color:var(--amarelo); }
.suave { color:var(--suave); }
.caixa { background:var(--cartao); border:4px solid var(--borda); border-radius:22px; padding:34px; }
.num { font-family:var(--pixel); font-size:54px; color:var(--amarelo); display:block; margin-bottom:14px; }
.grade { display:grid; grid-template-columns:1fr 1fr; gap:24px; }
.grade .caixa { font-size:30px; line-height:1.4; }
.miolo { flex:1; display:flex; flex-direction:column; justify-content:center; }
.miolo > h2:first-child, .miolo > h1:first-child { margin-top:0; }
.rodape { display:flex; justify-content:space-between; align-items:flex-end; font-size:22px; color:var(--suave); }
.rodape .px { font-size:18px; color:var(--amarelo); }
.vs { display:flex; align-items:flex-end; justify-content:center; gap:10px; margin:10px 0 0; }
.vs img { width:430px; height:430px; }
.vs span { font-family:var(--pixel); font-size:54px; color:var(--vermelho); padding-bottom:150px; }
"""


def card(n, corpo):
    return f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">{FONTES}<style>{CSS_IG}</style></head>
<body><div class="card"><div class="topo"><span>ARENA <b>SVM</b></span><span>{n}/6</span></div><div class="miolo">{corpo}</div>
<div class="rodape"><span>Inteligência Artificial II · Ciência da Computação · FIB</span><span class="px">{"arraste →" if n < 6 else ""}</span></div>
</div></body></html>'''


CARDS = [
    f'''<h1>Uma IA consegue prever <em>quem vence</em> uma batalha Pokémon?</h1>
    <div class="vs"><img class="spr" src="{SPR}/25.png"><span>VS</span><img class="spr" src="{SPR}/130.png"></div>
    <p class="suave" style="text-align:center;margin-top:30px;font-size:42px">Ensinamos uma IA a apostar no favorito.<br>Será que ela acerta?</p>''',

    f'''<h2>O problema</h2>
    <p>São <b>1.242 Pokémon</b>, 18 tipos e mais de <b>770 mil confrontos</b> possíveis. Quem leva vantagem?</p>
    <div class="grade">
      <div class="caixa"><span class="num">68%</span>das vezes vence o <b>mais rápido</b></div>
      <div class="caixa"><span class="num">81%</span>das vezes vence o <b>mais forte</b></div>
    </div>
    <div class="caixa" style="margin-top:24px;display:flex;align-items:center;gap:20px">
      <img class="spr" src="{SPR}/6.png" style="width:190px;height:190px">
      <div style="font-size:30px;line-height:1.4;flex:1">Charizard é <b>mais rápido</b>.<br>Blastoise tem <b>vantagem de tipo</b>.<br>Quem vence?</div>
      <img class="spr" src="{SPR}/9.png" style="width:190px;height:190px">
    </div>
    <p style="margin-top:34px">As regras simples erram bastante. Dá para fazer melhor <b>aprendendo com exemplos</b>?</p>''',

    f'''<h2>Os dados</h2>
    <p>Usamos os dados oficiais dos jogos (PokéAPI) e criamos um <b>simulador de batalhas</b> com a fórmula de dano
       do jogo e os golpes que cada Pokémon aprende.</p>
    <div class="grade">
      <div class="caixa"><span class="num">40 mil</span>confrontos diferentes</div>
      <div class="caixa"><span class="num">×21</span>batalhas cada um, porque existe <b>sorte</b></div>
    </div>
    <p style="margin-top:30px">A IA treina com as <b>gerações 1 a 6</b> e é testada com as <b>gerações 7 a 9</b>:
       Pokémon que ela <b>nunca viu</b>.</p>
    <img src="{IMG}/arena_batalha.png" style="width:400px;align-self:center;border-radius:16px;border:4px solid var(--borda)">''',

    f'''<h2>Como a IA decide (SVM)</h2>
    <p>Cada batalha vira um ponto. A IA traça a <b>rua mais larga possível</b> entre as batalhas que um lado vence e as
       que o outro vence.</p>
    <div class="caixa" style="padding:24px 34px">{svg_svm()}</div>
    <p style="margin-top:28px;font-size:34px">A linha do meio é a <b>fronteira</b>. Os pontos na beira da rua (circulados) são os
       <b>vetores de suporte</b>: só eles definem a decisão.</p>''',

    f'''<h2>O experimento</h2>
    <p>Acerto em batalhas de Pokémon que a IA nunca viu:</p>
    <div style="margin:14px 0 10px">{barras()}</div>
    <p style="font-size:34px">O que mais ajudou <b>não foi trocar o algoritmo</b>: foi dar à IA a informação certa
       (os golpes de cada Pokémon).</p>''',

    f'''<h2>O resultado</h2>
    <p>A IA acerta o favorito em <b>92,6%</b> das batalhas entre Pokémon que nunca viu.</p>
    <p class="suave" style="font-size:33px">Onde ela erra? Quando a <b>sorte</b> decide: batalhas equilibradas, golpes críticos e
       azarões com o golpe certo.</p>
    <div class="caixa" style="display:flex;gap:34px;align-items:center;margin-top:8px">
      <img src="{IMG}/qr_jogo.png" style="width:300px;height:300px;border-radius:14px">
      <div><div class="px" style="font-size:26px;line-height:1.7;color:var(--amarelo)">Jogue agora e desafie um amigo</div>
        <p style="font-size:30px;margin:16px 0 6px;font-weight:700">{JOGO}</p>
        <p class="suave" style="font-size:22px;margin:0">Código: {REPO}</p></div>
    </div>
    <p class="suave" style="font-size:19px;margin-top:22px">{MARCA}</p>''',
]

# ------------------------------------------------------------------ Folder (A4 paisagem, 2 páginas, dobra ao meio)
CSS_FOLDER = CORES + """
@page { size:A4 landscape; margin:0; }
body { width:297mm; color:#1b1f2e; -webkit-print-color-adjust:exact; print-color-adjust:exact; }
.folha { width:297mm; height:210mm; display:flex; page-break-after:always; overflow:hidden; }
.painel { width:148.5mm; height:210mm; padding:13mm 12mm; display:flex; flex-direction:column; }
.escuro { background:linear-gradient(180deg,#1b1f2e,#232a44); color:var(--texto); }
.claro { background:#fbfaf3; }
.dobra { border-left:.3mm dashed #c9c9c9; }
h1 { font-family:var(--pixel); font-size:19pt; line-height:1.6; }
h1 em { color:var(--amarelo); font-style:normal; }
h2 { font-family:var(--pixel); font-size:10.5pt; line-height:1.6; color:#2d5fa3; margin:0 0 3mm; }
.escuro h2 { color:var(--amarelo); }
p { font-size:10.5pt; line-height:1.5; margin-bottom:3mm; }
.pq { font-size:8.5pt; color:#5b6480; }
.escuro .pq { color:var(--suave); }
.caixa { background:#fff; border:.5mm solid #d8dbe6; border-radius:3mm; padding:4mm; }
.escuro .caixa { background:var(--cartao); border-color:var(--borda); }
.num { font-family:var(--pixel); font-size:22pt; color:#2d5fa3; }
.passos { display:grid; grid-template-columns:1fr 1fr 1fr; gap:3mm; margin:2mm 0 4mm; }
.passos .caixa { font-size:8.8pt; line-height:1.4; padding:3mm; }
.passos b { display:block; font-family:var(--pixel); font-size:7.5pt; color:#2d5fa3; margin-bottom:1.5mm; line-height:1.5; }
"""


def folder():
    fora = f'''<div class="folha">
  <div class="painel claro">
    <h2>Quem fez</h2>
    <p>Alceu Ferreira dos Santos Neto<br>Anthony Gabriel Schirato Lourenço<br>Gustavo de Carvalho Vieira<br>
       Luan Carlos de Souza Ferreira<br>Lucas Miguel Moreno Rios</p>
    <p class="pq">Disciplina de Inteligência Artificial II · Ciência da Computação<br>Faculdades Integradas de Bauru (FIB) ·
       Prof. Ronaldo Cesar Dametto · 2026</p>
    <h2 style="margin-top:6mm">Quer testar?</h2>
    <div class="caixa" style="display:flex;gap:5mm;align-items:center">
      <img src="{IMG}/qr_jogo.png" style="width:42mm;height:42mm">
      <div><p><b>Aponte a câmera e jogue</b>: desafie um amigo e veja a IA explicar cada aposta.</p>
        <p style="font-size:10pt;margin:0 0 2mm"><b>{JOGO}</b></p>
        <p class="pq" style="margin:0">Código, dados e experimentos: {REPO}</p></div>
    </div>
    <h2 style="margin-top:6mm">Vale lembrar</h2>
    <p class="pq" style="font-size:9pt">As batalhas vêm de um simulador próprio, mais simples que o jogo real (sem habilidades, itens
       ou estratégia). A IA aprende as regras desse simulador: ela não serve para prever partidas competitivas.</p>
    <p class="pq" style="margin-top:auto">{MARCA} Dados: PokéAPI.</p>
  </div>
  <div class="painel escuro dobra" style="justify-content:space-between">
    <div class="px" style="font-size:9pt;color:var(--suave)">ARENA <span style="color:var(--amarelo)">SVM</span></div>
    <div>
      <h1>Uma IA consegue prever <em>quem vence</em> uma batalha Pokémon?</h1>
      <div style="display:flex;justify-content:center;align-items:flex-end;gap:2mm;margin-top:8mm">
        <img class="spr" src="{SPR}/6.png" style="width:52mm"><span class="px" style="font-size:16pt;color:var(--vermelho);padding-bottom:20mm">VS</span>
        <img class="spr" src="{SPR}/9.png" style="width:52mm"></div>
    </div>
    <p style="font-size:11pt;color:var(--suave)">Ensinamos um computador a apostar no favorito, e ele ainda explica por que escolheu.
      <br><span style="color:var(--amarelo)">Jogue em {JOGO}</span></p>
  </div>
</div>'''
    dentro = f'''<div class="folha">
  <div class="painel claro">
    <h2>O problema</h2>
    <p>Existem <b>1.242 Pokémon</b> e mais de <b>770 mil confrontos</b> possíveis. Antes da batalha, como saber quem leva
       vantagem? Regras simples ajudam pouco: o mais rápido vence só <b>68%</b> das vezes, e o mais forte, <b>81%</b>.</p>
    <h2 style="margin-top:3mm">Como a IA aprende</h2>
    <div class="passos">
      <div class="caixa"><b>1. Exemplos</b>Um simulador com a fórmula de dano do jogo gerou 40 mil confrontos, cada um repetido 21 vezes.</div>
      <div class="caixa"><b>2. Treino</b>A IA estuda as batalhas dos Pokémon das gerações 1 a 6 e descobre padrões.</div>
      <div class="caixa"><b>3. Prova</b>Ela é testada com Pokémon das gerações 7 a 9, que nunca viu.</div>
    </div>
    <h2>A ideia do SVM</h2>
    <div style="display:flex;gap:5mm;align-items:center">
      <div class="caixa" style="width:62mm;flex-shrink:0;padding:2mm 3mm">{svg_svm(claro=True)}</div>
      <p style="font-size:9.8pt;margin:0">Cada batalha vira um ponto. A técnica, chamada <b>Máquina de Vetores de Suporte (SVM)</b>,
        traça a <b>rua mais larga possível</b> separando as batalhas que um lado vence das que o outro vence. Uma batalha nova
        é classificada pelo lado da rua em que cai. Os pontos na beira da rua (circulados) são os únicos que definem a decisão.</p>
    </div>
    <p class="pq" style="margin-top:auto">A IA recebe só o que se sabe antes da luta: atributos, tipos e golpes de cada Pokémon.</p>
  </div>
  <div class="painel claro dobra">
    <h2>O resultado</h2>
    <div style="display:flex;gap:5mm;align-items:center;margin-bottom:4mm">
      <div class="num">92,6%</div>
      <p style="margin:0">de acerto no favorito, em batalhas entre Pokémon que a IA <b>nunca tinha visto</b>.</p>
    </div>
    <div style="margin-bottom:2mm">{barras(altura=18, fonte=9.5, cor_txt="#1b1f2e", trilho="#e4e7f0").replace("px", "pt").replace("10pt;height", "2mm;height")}</div>
    <p style="font-size:9.8pt"><b>Descoberta:</b> o que mais melhorou a IA não foi trocar o algoritmo, e sim dar a ela a informação certa:
       os golpes que cada Pokémon aprende. Ela ainda erra quando a <b>sorte</b> decide a batalha.</p>
    <h2 style="margin-top:2mm">O protótipo: Arena SVM</h2>
    <div style="display:flex;gap:4mm;align-items:center">
      <img src="{IMG}/arena_batalha.png" style="width:64mm;border-radius:2mm;border:.5mm solid #1b1f2e">
      <p style="font-size:9.5pt;margin:0">Dois jogadores escolhem seus Pokémon, a IA aposta no favorito e a batalha acontece na tela.
        Depois, o jogo mostra <b>por que</b> a IA apostou assim: a fronteira, o que mais pesou e as batalhas em que ela se baseou.</p>
    </div>
  </div>
</div>'''
    return f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">{FONTES}<style>{CSS_FOLDER}</style></head>
<body>{fora}{dentro}</body></html>'''


def main():
    ig = RAIZ / "entregas/instagram"
    for i, corpo in enumerate(CARDS, 1):
        (ig / f"card_{i}.html").write_text(card(i, corpo), encoding="utf-8")
    (RAIZ / "entregas/folder/folder.html").write_text(folder(), encoding="utf-8")
    print("html gerados")


if __name__ == "__main__":
    main()
