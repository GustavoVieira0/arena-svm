"""Gera o folder (A4 paisagem, frente e verso, 8 painéis, dobra em sanfona) e os 6 cards do Instagram em HTML."""
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]   # pasta docs/
IMG = "../../img"   # caminho relativo às pastas folder/ e instagram/
SPR = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon"
REPO = "github.com/GustavoVieira0/arena-svm"
JOGO = "arena-svm.onrender.com"
INSTAGRAM = "@arena.svm"
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
<div class="rodape"><span><b style="color:var(--amarelo)">{INSTAGRAM}</b> · Inteligência Artificial II · Ciência da Computação · FIB</span><span class="px">{"arraste →" if n < 6 else ""}</span></div>
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
    <div style="margin:10px 0 0">{barras(altura=50, fonte=24)}</div>
    <p style="font-size:30px;margin:6px 0 16px">E se trocarmos o algoritmo? Com as mesmas informações:</p>
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:18px">
      <div class="caixa" style="padding:22px;border-color:var(--verde)"><span class="num" style="font-size:36px">92,6%</span><span style="font-size:26px">SVM</span></div>
      <div class="caixa" style="padding:22px"><span class="num" style="font-size:36px;color:var(--texto)">91,8%</span><span style="font-size:26px">Regressão logística</span></div>
      <div class="caixa" style="padding:22px"><span class="num" style="font-size:36px;color:var(--texto)">91,1%</span><span style="font-size:26px">KNN</span></div>
    </div>
    <p style="font-size:30px;margin:24px 0 0">O que mais ajudou <b>não foi trocar o algoritmo</b>: foi dar à IA a informação certa
       (os golpes de cada Pokémon).</p>''',

    f'''<h2>O resultado</h2>
    <p>A IA acerta o favorito em <b>92,6%</b> das batalhas entre Pokémon que nunca viu.</p>
    <p class="suave" style="font-size:33px">Onde ela erra? Quando a <b>sorte</b> decide: batalhas equilibradas, golpes críticos e
       azarões com o golpe certo.</p>
    <div class="caixa" style="display:flex;gap:34px;align-items:center;margin-top:8px">
      <img src="{IMG}/qr_jogo.png" style="width:300px;height:300px;border-radius:14px">
      <div><div class="px" style="font-size:26px;line-height:1.7;color:var(--amarelo)">Jogue agora e desafie um amigo</div>
        <p style="font-size:30px;margin:16px 0 6px;font-weight:700">{JOGO}</p>
        <p style="font-size:24px;margin:0 0 8px">Crie uma sala e mande o <b>link</b> ou o <b>QR Code</b> para seu amigo entrar.</p>
        <p class="suave" style="font-size:22px;margin:0">Código: {REPO}</p></div>
    </div>
    <p class="suave" style="font-size:19px;margin-top:22px">{MARCA}</p>''',
]

# ------------------------------------------------------------------ Folder (A4 paisagem, 8 painéis, dobra em sanfona)
# Frente (página 1): A1 capa | A2 problema | A3 como aprende | A4 jogue agora (contracapa)
# Verso  (página 2): B1 ideia do SVM | B2 resultado | B3 protótipo | B4 quem fez
# Impressão frente e verso virando pela borda curta: B4 fica atrás da capa e B1 atrás da contracapa.
INSTAGRAM_URL = "instagram.com/arena.svm"
CSS_FOLDER = CORES + """
@page { size:A4 landscape; margin:0; }
body { width:297mm; color:#1b1f2e; -webkit-print-color-adjust:exact; print-color-adjust:exact; }
.folha { width:297mm; height:210mm; display:flex; page-break-after:always; overflow:hidden; position:relative; }
.painel { width:74.25mm; height:210mm; padding:11mm 7.5mm 9mm; display:flex; flex-direction:column; position:relative; }
.escuro { background:linear-gradient(180deg,#1b1f2e,#232a44); color:var(--texto); }
.claro { background:#fbfaf3; }
.dobra { position:absolute; top:0; bottom:0; width:0; border-left:.25mm dashed rgba(140,140,150,.45); }
.marca-dobra { position:absolute; top:2mm; font:6pt Inter,sans-serif; color:#9aa3bf; transform:translateX(-50%); }
h1 { font-family:var(--pixel); font-size:12.5pt; line-height:1.65; }
h1 em { color:var(--amarelo); font-style:normal; }
h2 { font-family:var(--pixel); font-size:8.6pt; line-height:1.6; color:#2d5fa3; margin:0 0 3mm; }
.escuro h2 { color:var(--amarelo); }
h3 { font-size:9.2pt; font-weight:800; margin:0 0 1mm; }
p { font-size:8.9pt; line-height:1.48; margin-bottom:2.6mm; }
.pq { font-size:7.2pt; line-height:1.45; color:#5b6480; }
.escuro .pq { color:var(--suave); }
.caixa { background:#fff; border:.4mm solid #d8dbe6; border-radius:2.5mm; padding:3mm; margin-bottom:2.6mm; }
.escuro .caixa { background:var(--cartao); border-color:var(--borda); }
.caixa p:last-child { margin-bottom:0; }
.num { font-family:var(--pixel); font-size:20pt; color:#2d5fa3; line-height:1.3; }
.passo { display:flex; gap:2.6mm; align-items:flex-start; }
.passo .n { flex-shrink:0; width:7mm; height:7mm; border-radius:50%; background:#2d5fa3; color:#fff; font-family:var(--pixel);
            font-size:7pt; display:flex; align-items:center; justify-content:center; }
.passo p { margin:0; font-size:8.4pt; }
.barra { margin-bottom:2.2mm; }
.barra .rot { font-size:7.6pt; font-weight:600; margin-bottom:.8mm; }
.barra .trilho { background:#e4e7f0; border-radius:1.5mm; height:5mm; }
.barra .cheio { height:100%; border-radius:1.5mm; display:flex; align-items:center; justify-content:flex-end; padding-right:1.6mm;
                font-family:var(--pixel); font-size:6.4pt; color:#fff; }
table.cmp { width:100%; border-collapse:collapse; font-size:8pt; margin-bottom:2.6mm; }
table.cmp td { padding:1.2mm 1mm; border-bottom:.25mm solid #e1e4ee; }
table.cmp td:last-child { text-align:right; font-weight:700; }
table.cmp tr.svm td { color:#2d5fa3; }
.print { width:100%; border-radius:2mm; border:.4mm solid #1b1f2e; display:block; margin-bottom:2mm; }
.qr { background:#fff; border-radius:2.5mm; padding:2mm; display:inline-block; }
.qr img { display:block; }
.selo { display:inline-block; background:var(--amarelo); color:#1b1f2e; font-family:var(--pixel); font-size:6.4pt;
        padding:1.4mm 2.2mm; border-radius:1.5mm; }
"""


def barras_folder():
    out = ""
    for nome, v, cor in BARRAS:
        out += f'''<div class="barra"><div class="rot">{nome}</div><div class="trilho">
          <div class="cheio" style="width:{v}%;background:{cor}">{str(v).replace(".", ",")}%</div></div></div>'''
    return out


def dobras(rotulo):
    """Linhas tracejadas suaves nas 3 dobras (marcam onde dobrar)."""
    return "".join(f'<div class="dobra" style="left:{74.25 * i}mm"></div>'
                   f'<div class="marca-dobra" style="left:{74.25 * i}mm">{rotulo}</div>' for i in (1, 2, 3))


def folder():
    frente = f'''<div class="folha">
  <!-- A1: capa -->
  <div class="painel escuro" style="justify-content:space-between">
    <div class="px" style="font-size:8pt;color:var(--suave)">ARENA <span style="color:var(--amarelo)">SVM</span></div>
    <div>
      <h1>Uma IA consegue prever <em>quem vence</em> uma batalha Pokémon?</h1>
      <div style="position:relative;height:62mm;margin-top:5mm">
        <img class="spr" src="{SPR}/6.png" style="width:40mm;position:absolute;left:-3mm;top:0">
        <span class="px" style="position:absolute;right:4mm;top:14mm;font-size:14pt;color:var(--vermelho)">VS</span>
        <img class="spr" src="{SPR}/9.png" style="width:40mm;position:absolute;right:-3mm;bottom:0">
      </div>
    </div>
    <div>
      <p style="color:var(--suave)">Ensinamos um computador a apostar no favorito, e ele ainda <b style="color:var(--texto)">explica
        por que</b> escolheu.</p>
      <span class="selo">JOGUE ONLINE</span>
      <p style="margin:1.5mm 0 0;font-weight:700;color:var(--amarelo)">{JOGO}</p>
      <p class="pq" style="margin:3.5mm 0 0">Inteligência Artificial II · Ciência da Computação · FIB · 2026</p>
    </div>
  </div>

  <!-- A2: problema -->
  <div class="painel claro">
    <h2>O problema</h2>
    <p>Existem <b>1.242 Pokémon</b> e mais de <b>770 mil confrontos</b> possíveis. Antes de a batalha começar, dá para
       saber quem leva vantagem?</p>
    <div class="caixa">
      <h3>Regras de bolso ajudam pouco</h3>
      <p>O mais <b>rápido</b> vence só <b>68%</b> das vezes.<br>O mais <b>forte</b> (soma dos atributos), <b>81%</b>.</p>
    </div>
    <p>Uma batalha depende de muita coisa ao mesmo tempo: velocidade, ataque, defesa, <b>vantagem de tipo</b> (água apaga
       fogo) e os <b>golpes</b> que cada um sabe.</p>
    <div class="caixa" style="background:#eef3fb;border-color:#c9d6ee">
      <h3>A nossa pergunta</h3>
      <p>Uma IA que estuda milhares de batalhas aprende a combinar tudo isso melhor do que as regras de bolso?</p>
    </div>
    <p class="pq" style="margin-top:auto">Spoiler: aprende. Acerta <b>92,6%</b>, e o jeito como ela decide cabe em um desenho
       (veja do outro lado).</p>
  </div>

  <!-- A3: como aprende -->
  <div class="painel claro">
    <h2>Como a IA aprende</h2>
    <div class="caixa passo"><div class="n">1</div><p><b>Exemplos.</b> Um simulador com a fórmula de dano do jogo gerou
      <b>40 mil confrontos</b>, cada um repetido 21 vezes. Vence quem ganhar a maioria.</p></div>
    <div class="caixa passo"><div class="n">2</div><p><b>Treino.</b> A IA estuda as batalhas dos Pokémon das
      <b>gerações 1 a 6</b> e procura padrões.</p></div>
    <div class="caixa passo"><div class="n">3</div><p><b>Prova.</b> Depois é testada com Pokémon das <b>gerações 7 a 9</b>,
      que ela <b>nunca viu</b>. Nada de decorar resposta.</p></div>
    <h2 style="margin-top:2mm">O que ela recebe</h2>
    <p>Só o que se sabe <b>antes</b> da luta: <b>15 informações</b> por batalha, como a diferença de velocidade, de ataque, a
       vantagem de tipo e a força do melhor golpe de cada lado.</p>
    <div class="caixa" style="background:#eef3fb;border-color:#c9d6ee"><h3>Por que separar por geração?</h3>
      <p>Se a prova tivesse Pokémon do treino, a IA poderia só reconhecer rostos conhecidos. Separando, medimos se ela
      aprendeu de verdade.</p></div>
    <p class="pq" style="margin-top:auto">Dados: PokéAPI (atributos, tipos e golpes de 1.242 Pokémon).</p>
  </div>

  <!-- A4: contracapa (jogue agora) -->
  <div class="painel escuro" style="text-align:center;align-items:center">
    <h2 style="font-size:10pt">Jogue agora!</h2>
    <div class="qr"><img src="{IMG}/qr_jogo.png" style="width:42mm;height:42mm"></div>
    <p style="margin:2.5mm 0 1mm;font-weight:700;font-size:9.5pt">{JOGO}</p>
    <p class="pq" style="margin-bottom:0">Crie uma sala e mande o <b style="color:var(--texto)">link</b> ou o
      <b style="color:var(--texto)">QR Code da sala</b> para um amigo entrar. A IA aposta e explica cada batalha.</p>
    <div style="border-top:.3mm dashed var(--borda);width:100%;margin:6mm 0 5mm"></div>
    <h2>Siga a gente</h2>
    <div class="qr"><img src="{IMG}/qr_instagram.png" style="width:30mm;height:30mm"></div>
    <p style="margin:2.5mm 0 0;font-weight:700;font-size:9.5pt;color:var(--amarelo)">{INSTAGRAM}</p>
    <p class="pq" style="margin-top:auto">Código, dados e experimentos:<br>{REPO}</p>
  </div>
  {dobras("")}
</div>'''

    verso = f'''<div class="folha">
  <!-- B1: ideia do SVM -->
  <div class="painel claro">
    <h2>A ideia do SVM</h2>
    <p>Cada batalha vira um <b>ponto</b>. A técnica <b>Máquina de Vetores de Suporte (SVM)</b> traça a
       <b>rua mais larga possível</b> entre as batalhas que um lado vence e as que o outro vence.</p>
    <div class="caixa" style="padding:2mm 2.5mm">{svg_svm(claro=True)}</div>
    <p>Uma batalha nova é classificada pelo <b>lado da rua</b> em que cai. Quanto mais longe da faixa amarela, mais segura
       a aposta.</p>
    <div class="caixa"><h3>Vetores de suporte</h3><p>Os pontos circulados, na beira da rua, são os únicos que definem a
      decisão. Os outros podem até sumir.</p></div>
    <div class="caixa"><h3>E quando a rua não é reta?</h3><p>Com o <b>kernel RBF</b>, o SVM curva a fronteira para
      seguir os padrões dos dados.</p></div>
  </div>

  <!-- B2: resultado -->
  <div class="painel claro">
    <h2>O resultado</h2>
    <div class="num">92,6%</div>
    <p>de acerto no favorito, em batalhas entre Pokémon que a IA <b>nunca tinha visto</b>.</p>
    {barras_folder()}
    <h3 style="margin-top:1.5mm">E os outros algoritmos?</h3>
    <table class="cmp">
      <tr class="svm"><td>SVM (RBF)</td><td>92,6%</td></tr>
      <tr><td>Regressão logística</td><td>91,8%</td></tr>
      <tr><td>KNN (k = 91)</td><td>91,1%</td></tr>
    </table>
    <p><b>Descoberta:</b> o que mais ajudou não foi trocar o algoritmo, e sim dar a informação certa: os <b>golpes</b>.
       Ela ainda erra quando a <b>sorte</b> decide.</p>
    <div class="caixa" style="margin-top:auto;background:#fff7d6;border-color:#f0dc8a"><h3>Cuidado com a escala</h3>
      <p>Sem padronizar os números, o KNN cai para <b>81,5%</b> e o SVM para <b>90,4%</b>: um atributo de valores grandes
      “grita” mais que os outros.</p></div>
  </div>

  <!-- B3: protótipo -->
  <div class="painel claro">
    <h2>O protótipo</h2>
    <img class="print" src="{IMG}/arena_batalha.png">
    <p><b>Arena:</b> dois jogadores escolhem seus Pokémon, a IA aposta no favorito e a batalha acontece na tela. Depois, ela
       mostra <b>por que</b> apostou assim.</p>
    <img class="print" src="{IMG}/arena_fronteira.png" style="width:78%;margin:0 auto 2mm">
    <p style="margin-bottom:0"><b>Laboratório:</b> monte seu próprio personagem, mexa nos atributos e veja a
       <b>fronteira do SVM</b> se mover ao vivo.</p>
  </div>

  <!-- B4: quem fez (fica atrás da capa) -->
  <div class="painel escuro">
    <h2>Quem fez</h2>
    <p style="line-height:1.7">Alceu Ferreira dos Santos Neto<br>Anthony Gabriel Schirato Lourenço<br>Gustavo de Carvalho Vieira<br>
       Luan Carlos de Souza Ferreira<br>Lucas Miguel Moreno Rios</p>
    <p class="pq">Disciplina de Inteligência Artificial II<br>Ciência da Computação<br>Faculdades Integradas de Bauru (FIB)<br>
       Prof. Ronaldo Cesar Dametto · 2026</p>
    <h2 style="margin-top:5mm">Vale lembrar</h2>
    <p class="pq" style="font-size:7.8pt">As batalhas vêm de um simulador próprio, mais simples que o jogo real (sem
       habilidades, itens ou troca de Pokémon). A IA aprende as regras desse simulador: ela não serve para prever partidas
       competitivas.</p>
    <div style="margin-top:auto;display:flex;gap:3mm;align-items:center">
      <img class="spr" src="{SPR}/25.png" style="width:20mm">
      <p class="pq" style="margin:0">{MARCA}</p>
    </div>
  </div>
  {dobras("")}
</div>'''
    return f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">{FONTES}<style>{CSS_FOLDER}</style></head>
<body>{frente}{verso}</body></html>'''


def main():
    ig = RAIZ / "entregas/instagram"
    for i, corpo in enumerate(CARDS, 1):
        (ig / f"card_{i}.html").write_text(card(i, corpo), encoding="utf-8")
    (RAIZ / "entregas/folder/folder.html").write_text(folder(), encoding="utf-8")
    print("html gerados")


if __name__ == "__main__":
    main()
