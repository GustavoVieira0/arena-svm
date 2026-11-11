// Laboratório da Arena SVM: construtor de personagem, previsão ao vivo e corte 2D da fronteira do SVM.
const $ = (id) => document.getElementById(id);
const bonito = (n) => n.replace(/-/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
const ATRIB = [["HP", "HP"], ["Attack", "Ataque"], ["Defense", "Defesa"], ["Sp. Atk", "At. especial"],
               ["Sp. Def", "Def. especial"], ["Speed", "Velocidade"]];
const NOME_EIXO = { dif_HP: "HP", dif_Attack: "Ataque", dif_Defense: "Defesa", "dif_Sp. Atk": "Ataque especial",
                    "dif_Sp. Def": "Defesa especial", dif_Speed: "Velocidade" };
const NOMES_TIPO = { Normal: "Normal", Fire: "Fogo", Water: "Água", Electric: "Elétrico", Grass: "Planta", Ice: "Gelo",
  Fighting: "Lutador", Poison: "Veneno", Ground: "Terra", Flying: "Voador", Psychic: "Psíquico", Bug: "Inseto",
  Rock: "Pedra", Ghost: "Fantasma", Dragon: "Dragão", Dark: "Sombrio", Steel: "Aço", Fairy: "Fada" };
// golpes genéricos dos personagens criados ("golpe-fire") aparecem como "Golpe de Fogo"
const nomeGolpe = (g) => {
  if (!g.startsWith("golpe-")) return bonito(g);
  const t = g.slice(6).charAt(0).toUpperCase() + g.slice(7);
  return "Golpe de " + (NOMES_TIPO[t] || t);
};

let LISTA = [], porNome = {};
const meu = { nome: "Meu personagem", sprite: 25, tipos: ["Electric"],
              atributos: { HP: 80, Attack: 80, Defense: 80, "Sp. Atk": 80, "Sp. Def": 80, Speed: 80 } };
let advId = 130, seq = 0, temporizador = null, ultima = null;

async function api(caminho, corpo) {
  const r = await fetch(caminho, corpo === undefined ? {} : {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(corpo) });
  const d = await r.json();
  if (!r.ok) throw new Error(d.erro || "Erro de comunicação");
  return d;
}

// ---------- construtor ----------
function montarSliders() {
  $("sliders").innerHTML = ATRIB.map(([k, rot]) => `<div class="slider"><span>${rot}</span>
    <input type="range" min="1" max="255" data-k="${k}"><input type="number" min="1" max="255" data-n="${k}"></div>`).join("");
  document.querySelectorAll("#sliders input").forEach((el) => el.addEventListener("input", () => {
    const k = el.dataset.k || el.dataset.n;
    meu.atributos[k] = Math.max(1, Math.min(255, parseInt(el.value) || 1));
    sincronizar(); agendar();
  }));
}
function sincronizar() {
  for (const [k] of ATRIB) {
    document.querySelector(`[data-k="${k}"]`).value = meu.atributos[k];
    const n = document.querySelector(`[data-n="${k}"]`);
    if (document.activeElement !== n) n.value = meu.atributos[k];
  }
  $("total").textContent = Object.values(meu.atributos).reduce((a, b) => a + b, 0);
  $("tipo1").value = meu.tipos[0]; $("tipo2").value = meu.tipos[1] || "";
}
function definirAparencia(id) {
  meu.sprite = id;
  colocarSprite($("sprite-meu"), id, { animado: true });
}
function definirAdversario(id) {
  advId = id;
  const p = LISTA.find((x) => x.id === id);
  colocarSprite($("sprite-adv"), id, { animado: true });
  $("busca-adv").value = bonito(p.nome);
  $("info-adv").innerHTML = `${p.tipos.map((t) => NOMES_TIPO[t] || t).join(" / ")} · total ${p.total}<br>` +
    ATRIB.map(([k, r]) => `${r} ${p.atributos[k]}`).join(" · ");
  agendar();
}
const PRESETS = {
  equilibrar: { HP: 85, Attack: 85, Defense: 85, "Sp. Atk": 85, "Sp. Def": 85, Speed: 85 },
  veloz: { HP: 55, Attack: 120, Defense: 45, "Sp. Atk": 110, "Sp. Def": 50, Speed: 150 },
  tanque: { HP: 150, Attack: 90, Defense: 140, "Sp. Atk": 40, "Sp. Def": 120, Speed: 30 },
};
function aplicarPreset(p) { meu.atributos = { ...p }; sincronizar(); agendar(); }

// ---------- previsão ao vivo ----------
function agendar() {
  clearTimeout(temporizador);
  $("previsao-lab").classList.add("carregando");
  temporizador = setTimeout(prever, 250);
}
async function prever() {
  const minha = ++seq;
  meu.nome = $("nome").value.trim() || "Meu personagem";
  try {
    const r = await api("/api/laboratorio/prever", { a: { custom: meu }, b: { id: advId },
                                                     eixo_x: $("eixo-x").value, eixo_y: $("eixo-y").value });
    if (minha !== seq) return;                  // chegou uma resposta mais nova
    ultima = r;
    mostrarPrevisao(r);
    desenharFronteira(r.fronteira);
    mostrarFatores(r);
    $("resultado-sim").innerHTML = "";
  } catch (e) {
    $("previsao-lab").textContent = e.message;
  } finally {
    if (minha === seq) $("previsao-lab").classList.remove("carregando");
  }
}
function mostrarPrevisao(r) {
  const nA = r.a.nome, nB = bonito(r.b.nome), fav = r.favorito === "a" ? nA : nB;
  const dentro = Math.abs(r.score) < 1;
  $("previsao-lab").innerHTML = `A IA aposta em <span class="grande">${fav}</span><br>
    score ${r.score > 0 ? "+" : ""}${r.score} · ${dentro ? "dentro da margem (zona de dúvida)" : "fora da margem (decisão segura)"}<br>
    <span class="dica">Melhores golpes: ${nA}: ${r.golpes.a.map(nomeGolpe).join(", ")} · ${nB}: ${r.golpes.b.slice(0, 2).map(nomeGolpe).join(", ")}</span>`;
  $("ponto-regua").style.left = (Math.max(-3, Math.min(3, r.score)) + 3) / 6 * 100 + "%";
  $("leg-a").textContent = `${nA} →`; $("leg-b").textContent = `← ${nB}`;
}
function mostrarFatores(r) {
  const f = r.explicacao.fatores, max = Math.max(...f.map((x) => Math.abs(x.efeito)), 0.01);
  const barra = (v, lado) => (lado === "a" ? v > 0 : v < 0) ? `<div style="width:${Math.abs(v) / max * 100}%"></div>` : "";
  $("fatores-lab").innerHTML = `<div class="lados"><span>← ${bonito(r.b.nome)}</span><span>${r.a.nome} →</span></div>` +
    f.map((x) => `<div class="fator"><span class="nome">${x.fator}</span><div class="lado b">${barra(x.efeito, "b")}</div>
      <div class="lado a">${barra(x.efeito, "a")}</div></div>`).join("");
}

// ---------- fronteira 2D ----------
function desenharFronteira(fr) {
  const cv = $("canvas-fronteira"), ctx = cv.getContext("2d");
  const W = cv.width, H = cv.height, M = 46, P = W - M - 10;          // área do gráfico: P × P
  const v = fr.valores, s = fr.scores, n = v.length, min = v[0], max = v[n - 1];
  ctx.fillStyle = "#151927"; ctx.fillRect(0, 0, W, H);

  // score interpolado (bilinear) em cada pixel; o eixo y cresce para cima
  const img = ctx.createImageData(P, P);
  for (let py = 0; py < P; py++) {
    const fy = (1 - py / (P - 1)) * (n - 1), y0 = Math.min(Math.floor(fy), n - 2), ty = fy - y0;
    for (let px = 0; px < P; px++) {
      const fx = px / (P - 1) * (n - 1), x0 = Math.min(Math.floor(fx), n - 2), tx = fx - x0;
      const sc = (s[y0][x0] * (1 - tx) + s[y0][x0 + 1] * tx) * (1 - ty) + (s[y0 + 1][x0] * (1 - tx) + s[y0 + 1][x0 + 1] * tx) * ty;
      const a = Math.min(Math.abs(sc) / 3, 1), i = (py * P + px) * 4;
      let cor = sc > 0 ? [224, 122, 95] : [108, 143, 216];
      const fundo = [29, 34, 52];
      cor = cor.map((c, k) => Math.round(fundo[k] + (c - fundo[k]) * (0.35 + 0.65 * a)));
      if (Math.abs(sc) < 0.06) cor = [255, 203, 5];                                       // fronteira
      else if (Math.abs(Math.abs(sc) - 1) < 0.05 && ((px + py) % 10) < 6) cor = [255, 230, 150]; // margem
      img.data.set([...cor, 255], i);
    }
  }
  ctx.putImageData(img, M, 0);

  // eixos e rótulos
  ctx.fillStyle = "#9aa3bf"; ctx.font = "11px Inter, sans-serif"; ctx.textAlign = "center";
  for (const t of [-200, -100, 0, 100, 200]) {
    const x = M + (t - min) / (max - min) * (P - 1), y = (1 - (t - min) / (max - min)) * (P - 1);
    ctx.fillText(t, x, P + 16); ctx.textAlign = "right"; ctx.fillText(t, M - 6, y + 4); ctx.textAlign = "center";
  }
  ctx.fillStyle = "#eef1f8"; ctx.font = "600 12px Inter, sans-serif";
  ctx.fillText(`${NOME_EIXO[fr.eixo_x]}: você − adversário →`, M + P / 2, P + 34);
  ctx.save(); ctx.translate(12, P / 2); ctx.rotate(-Math.PI / 2);
  ctx.fillText(`${NOME_EIXO[fr.eixo_y]}: você − adversário →`, 0, 0); ctx.restore();

  // ponto da batalha atual
  const clamp = (x) => Math.max(min, Math.min(max, x));
  const px = M + (clamp(fr.ponto[0]) - min) / (max - min) * (P - 1);
  const py = (1 - (clamp(fr.ponto[1]) - min) / (max - min)) * (P - 1);
  ctx.beginPath(); ctx.arc(px, py, 8, 0, 2 * Math.PI); ctx.fillStyle = "#fff"; ctx.fill();
  ctx.lineWidth = 3; ctx.strokeStyle = "#0b0d14"; ctx.stroke();
}

// ---------- simulação ----------
$("btn-simular").onclick = async () => {
  $("btn-simular").disabled = true; $("resultado-sim").textContent = "Simulando 201 batalhas...";
  try {
    const r = await api("/api/laboratorio/simular", { a: { custom: meu }, b: { id: advId } });
    const nA = meu.nome, nB = bonito(LISTA.find((x) => x.id === advId).nome), pct = r.vitorias_a / r.n;
    const favSim = r.favorito === "a" ? nA : nB, ia = ultima && ultima.favorito === r.favorito;
    $("resultado-sim").innerHTML = `<b>${nA}</b> venceu <b>${r.vitorias_a} de ${r.n}</b> (${Math.round(pct * 100)}%).
      Favorito pelo simulador: <b>${favSim}</b>.<br>
      ${ultima ? (ia ? "✔ A IA acertou o favorito." : "✘ A IA errou o favorito.") : ""}
      <div class="narra"><b>Uma das batalhas:</b><br>${r.narracao.join("<br>")}</div>`;
  } catch (e) { $("resultado-sim").textContent = e.message; }
  $("btn-simular").disabled = false;
};

// ---------- inicialização ----------
(async () => {
  LISTA = await api("/api/pokemon");
  porNome = Object.fromEntries(LISTA.map((p) => [bonito(p.nome).toLowerCase(), p.id]));
  $("lista-pokemon").innerHTML = LISTA.map((p) => `<option value="${bonito(p.nome)}">`).join("");
  const tipos = await api("/api/laboratorio/tipos");
  for (const t of tipos) { $("tipo1").add(new Option(NOMES_TIPO[t] || t, t)); $("tipo2").add(new Option(NOMES_TIPO[t] || t, t)); }
  const eixos = Object.entries(NOME_EIXO);
  for (const [k, r] of eixos) { $("eixo-x").add(new Option(r, k)); $("eixo-y").add(new Option(r, k)); }
  $("eixo-x").value = "dif_Speed"; $("eixo-y").value = "dif_Attack";

  montarSliders(); sincronizar(); definirAparencia(meu.sprite);
  $("busca-aparencia").value = "Pikachu";

  $("nome").oninput = agendar;
  $("tipo1").onchange = () => { meu.tipos[0] = $("tipo1").value; if (meu.tipos[1] === meu.tipos[0]) meu.tipos.splice(1); sincronizar(); agendar(); };
  $("tipo2").onchange = () => { const t = $("tipo2").value; meu.tipos = t && t !== meu.tipos[0] ? [meu.tipos[0], t] : [meu.tipos[0]]; sincronizar(); agendar(); };
  $("busca-aparencia").onchange = () => { const id = porNome[$("busca-aparencia").value.trim().toLowerCase()]; if (id) definirAparencia(id); };
  $("btn-aparencia").onclick = () => { const p = LISTA[Math.floor(Math.random() * LISTA.length)]; $("busca-aparencia").value = bonito(p.nome); definirAparencia(p.id); };
  $("busca-adv").onchange = () => { const id = porNome[$("busca-adv").value.trim().toLowerCase()]; if (id) definirAdversario(id); };
  $("btn-adv-aleatorio").onclick = () => definirAdversario(LISTA[Math.floor(Math.random() * LISTA.length)].id);
  $("btn-equilibrar").onclick = () => aplicarPreset(PRESETS.equilibrar);
  $("btn-veloz").onclick = () => aplicarPreset(PRESETS.veloz);
  $("btn-tanque").onclick = () => aplicarPreset(PRESETS.tanque);
  $("btn-aleatorio").onclick = () => {
    const a = {}; for (const [k] of ATRIB) a[k] = 30 + Math.floor(Math.random() * 120); aplicarPreset(a);
    const t = Object.keys(NOMES_TIPO); meu.tipos = [t[Math.floor(Math.random() * t.length)]]; sincronizar(); agendar();
  };
  $("eixo-x").onchange = $("eixo-y").onchange = () => {
    if ($("eixo-x").value === $("eixo-y").value) $("eixo-y").value = $("eixo-x").value === "dif_Attack" ? "dif_Speed" : "dif_Attack";
    agendar();
  };
  definirAdversario(advId);
})();
