// Arena SVM: interface do jogo (sem frameworks). Sprites: ver sprites.js
const CORES_TIPO = {
  Normal: "#a8a878", Fire: "#f08030", Water: "#6890f0", Electric: "#d8b020", Grass: "#78c850", Ice: "#58c8d0",
  Fighting: "#c03028", Poison: "#a040a0", Ground: "#c8a040", Flying: "#a890f0", Psychic: "#f85888", Bug: "#a8b820",
  Rock: "#b8a038", Ghost: "#705898", Dragon: "#7038f8", Dark: "#705848", Steel: "#a0a0c0", Fairy: "#e888a8",
};
const NOMES_TIPO = {
  Normal: "Normal", Fire: "Fogo", Water: "Água", Electric: "Elétrico", Grass: "Planta", Ice: "Gelo",
  Fighting: "Lutador", Poison: "Veneno", Ground: "Terra", Flying: "Voador", Psychic: "Psíquico", Bug: "Inseto",
  Rock: "Pedra", Ghost: "Fantasma", Dragon: "Dragão", Dark: "Sombrio", Steel: "Aço", Fairy: "Fada",
};
const ATRIB = { HP: "HP", Attack: "Ataque", Defense: "Defesa", "Sp. Atk": "At. Esp.", "Sp. Def": "Def. Esp.", Speed: "Veloc." };
const MAX_GRADE = 120;

const $ = (id) => document.getElementById(id);
const esperar = (ms) => new Promise((r) => setTimeout(r, ms));
const bonito = (n) => n.replace(/-/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());

let LISTA = [], porId = {};
let sala = null, token = null, estado = null;
let selecionado = null, animandoId = null, ultimaVersao = -1;

function badgesTipo(tipos) {
  return `<div class="tipos">${tipos.map((t) => `<span class="tipo" style="background:${CORES_TIPO[t]}">${NOMES_TIPO[t] || t}</span>`).join("")}</div>`;
}

// ---------- API ----------
async function api(caminho, corpo) {
  const r = await fetch(caminho, corpo === undefined ? {} : {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(corpo),
  });
  const dados = await r.json();
  if (!r.ok) throw new Error(dados.erro || "Erro de comunicação");
  return dados;
}
function salvarToken(codigo, tk) { try { localStorage.setItem("arena-svm:" + codigo, tk); } catch {} }
function lerToken(codigo) { try { return localStorage.getItem("arena-svm:" + codigo); } catch { return null; } }

function mostrar(tela) {
  for (const t of ["inicio", "escolha", "arena"]) $("tela-" + t).hidden = t !== tela;
}

// ---------- tela inicial ----------
async function entrarNaSala(dados) {
  sala = dados.codigo; token = dados.token; salvarToken(sala, token);
  history.replaceState(null, "", "/?sala=" + sala);
  $("info-sala").hidden = false; $("codigo-topo").textContent = sala;
  aplicarEstado(dados.estado);
  setInterval(atualizar, 1000);
}

$("btn-criar").onclick = async () => {
  try { await entrarNaSala(await api("/api/salas", { nome: $("nome").value.trim() })); }
  catch (e) { $("erro-inicio").textContent = e.message; }
};
$("nome").addEventListener("keydown", (e) => {
  if (e.key === "Enter") ($("aviso-convite").hidden ? $("btn-criar") : $("btn-entrar")).click();
});
$("btn-entrar").onclick = async () => {
  const codigo = $("codigo").value.trim().toUpperCase();
  if (codigo.length !== 4) { $("erro-inicio").textContent = "Digite o código de 4 letras."; return; }
  try {
    await entrarNaSala(await api(`/api/salas/${codigo}/entrar`, { nome: $("nome").value.trim(), token: lerToken(codigo) }));
  } catch (e) { $("erro-inicio").textContent = e.message; }
};

// ---------- estado da sala ----------
async function atualizar() {
  try { aplicarEstado(await api(`/api/salas/${sala}?token=${token}`)); } catch {}
}

function aplicarEstado(novo) {
  estado = novo;
  if (estado.batalha) {
    if (animandoId !== estado.batalha.id) { animandoId = estado.batalha.id; animarBatalha(estado.batalha); }
    return;
  }
  if (animandoId !== null) animandoId = null;     // revanche: volta para a escolha
  if (!$("tela-escolha").hidden && estado.versao === ultimaVersao) return;
  ultimaVersao = estado.versao;
  mostrar("escolha");
  const espectador = estado.eu === "espectador";
  $("aviso-espectador").hidden = !espectador;
  $("cartao-grade").hidden = espectador;
  $("cartao-meu").hidden = espectador;
  if (espectador) {
    $("titulo-adv").textContent = "Jogadores";
    $("adversario").innerHTML = Object.values(estado.jogadores).map((j) =>
      `<div><b>${j.nome}</b> ${j.pronto ? '<span class="ok">pronto ✔</span>' : j.escolheu ? "escolheu" : "escolhendo..."}</div>`).join("") +
      `<div class="dica">${estado.espectadores} pessoa(s) assistindo</div>`;
    $("convite").hidden = true;
    return;
  }
  const eu = estado.jogadores[estado.eu];
  const outro = estado.jogadores[estado.eu === "a" ? "b" : "a"];
  if (eu.pokemon && (!selecionado || selecionado.id !== eu.pokemon.id)) mostrarEscolhido(eu.pokemon);
  $("btn-pronto").disabled = !eu.pokemon || eu.pronto;
  $("btn-pronto").textContent = eu.pronto ? "Aguardando..." : "Pronto!";
  $("adversario").innerHTML = (!outro ? "Aguardando outro jogador entrar..." :
    `<b>${outro.nome}</b> ${outro.pronto ? '<span class="ok">está pronto ✔</span>' : outro.escolheu ? "já escolheu, falta confirmar" : "está escolhendo..."}`) +
    (estado.espectadores ? `<div class="dica">${estado.espectadores} pessoa(s) assistindo</div>` : "");
  $("convite").hidden = !!outro;
  $("link-sala").textContent = estado.link;
  desenharQrSala(estado.link);
  $("convite-texto").textContent = estado.online
    ? "Para o outro jogador entrar, de qualquer lugar, envie o link:"
    : "Para o outro jogador entrar (mesma rede Wi-Fi), envie o link:";
  $("codigo-sala").textContent = estado.codigo;
}

// ---------- escolha ----------
function filtrados() {
  const g = $("filtro-geracao").value, busca = $("filtro-busca").value.trim().toLowerCase().replace(/\s+/g, "-");
  return LISTA.filter((p) => (!g || p.geracao === +g) && (!busca || p.nome.includes(busca)));
}

function desenharGrade() {
  const lista = filtrados();
  $("grade").innerHTML = "";
  for (const p of lista.slice(0, MAX_GRADE)) {
    const d = document.createElement("div");
    d.className = "poke" + (selecionado && selecionado.id === p.id ? " sel" : "");
    d.title = bonito(p.nome);
    const img = document.createElement("img"); img.loading = "lazy";
    colocarSprite(img, p.id, { animado: false });
    d.append(img, bonito(p.nome));
    d.onclick = () => escolher(p);
    $("grade").append(d);
  }
  $("grade-info").textContent = lista.length > MAX_GRADE
    ? `Mostrando ${MAX_GRADE} de ${lista.length}. Use a busca ou a geração para filtrar.`
    : `${lista.length} Pokémon`;
}

function mostrarEscolhido(p) {
  selecionado = p;
  const max = 200;
  $("escolhido").className = "escolhido";
  $("escolhido").innerHTML = `<img id="img-escolhido" alt=""><div class="nome">${bonito(p.nome)}</div>
    ${badgesTipo(p.tipos)}
    <div class="stats">${Object.entries(p.atributos).map(([k, v]) =>
      `<span>${ATRIB[k]}</span><b>${v}</b><div class="b"><div style="width:${Math.min(100, v / max * 100)}%"></div></div>`).join("")}
      <span>Total</span><b>${p.total}</b><span>Geração ${p.geracao}${p.lendario ? " · lendário/mítico" : ""}</span></div>`;
  colocarSprite($("img-escolhido"), p.id);
  document.querySelectorAll(".poke").forEach((el) => el.classList.toggle("sel", el.title === bonito(p.nome)));
}

async function escolher(p) {
  mostrarEscolhido(p);
  try { aplicarEstado(await api(`/api/salas/${sala}/escolher`, { token, pokemon_id: p.id })); } catch (e) { alert(e.message); }
}

$("btn-roleta").onclick = async () => {
  const lista = filtrados();
  if (!lista.length) return;
  $("btn-roleta").disabled = true;
  for (let i = 0; i < 14; i++) {                       // gira mostrando Pokémon aleatórios
    mostrarEscolhido(lista[Math.floor(Math.random() * lista.length)]);
    await esperar(60 + i * 12);
  }
  await escolher(lista[Math.floor(Math.random() * lista.length)]);
  $("btn-roleta").disabled = false;
};
$("btn-pronto").onclick = async () => {
  try { aplicarEstado(await api(`/api/salas/${sala}/pronto`, { token })); } catch (e) { alert(e.message); }
};
$("btn-copiar").onclick = async () => {
  try { await navigator.clipboard.writeText($("link-sala").textContent); $("btn-copiar").textContent = "Copiado!"; }
  catch { $("btn-copiar").textContent = "Selecione e copie"; }
  setTimeout(() => ($("btn-copiar").textContent = "Copiar"), 2000);
};

// QR Code com o link da sala (biblioteca qrcode-generator, carregada do CDN)
let qrDesenhado = null;
function desenharQrSala(link) {
  if (qrDesenhado === link || typeof qrcode === "undefined") return;
  const q = qrcode(0, "M"); q.addData(link); q.make();
  $("qr-sala").innerHTML = q.createSvgTag({ cellSize: 4, margin: 2, scalable: true });
  qrDesenhado = link;
}

// No celular, abre o menu de compartilhar do sistema (WhatsApp, Telegram...); no computador, copia o link.
$("btn-compartilhar").onclick = async () => {
  const link = $("link-sala").textContent;
  const texto = "Bora batalhar na Arena SVM? A IA tenta adivinhar quem vence. Entre na minha sala:";
  if (navigator.share) {
    try { await navigator.share({ title: "Arena SVM", text: texto, url: link }); } catch {}
  } else {
    try { await navigator.clipboard.writeText(`${texto} ${link}`); $("btn-compartilhar").textContent = "Convite copiado!"; }
    catch { $("btn-compartilhar").textContent = "Copie o link acima"; }
    setTimeout(() => ($("btn-compartilhar").textContent = "📤 Compartilhar convite"), 2500);
  }
};
$("filtro-geracao").onchange = desenharGrade;
$("filtro-busca").oninput = desenharGrade;

// ---------- arena ----------
function corHp(frac) { return frac > .5 ? "var(--verde)" : frac > .2 ? "var(--amarelo)" : "var(--vermelho)"; }
function definirHp(lado, hp, max) {
  const barra = $("barra-" + lado), frac = Math.max(0, hp) / max;
  barra.style.width = (frac * 100) + "%"; barra.style.background = corHp(frac);
  if (lado === "eu") $("hp-num-eu").textContent = `${Math.max(0, hp)} / ${max}`;
}
async function falar(texto, ms = 1100) {
  const caixa = $("caixa-texto"); caixa.textContent = "";
  for (const ch of texto) { caixa.textContent += ch; await esperar(14); }
  await esperar(ms);
}

async function animarBatalha(b) {
  const espectador = estado.eu === "espectador";
  const meu = espectador ? "a" : estado.eu, dele = meu === "a" ? "b" : "a";
  const lado = (slot) => (slot === meu ? "eu" : "op");
  mostrar("arena");
  window.scrollTo({ top: 0 });
  $("resultado").hidden = true; $("acoes").hidden = true;
  for (const [slot, l] of [[meu, "eu"], [dele, "op"]]) {
    const img = $("sprite-" + l);
    img.className = "sprite sprite-" + l;
    img.style.height = "0px";                        // evita mostrar o tamanho errado antes de carregar
    colocarSprite(img, b[slot].id, { costas: l === "eu", aoCarregar: (im) => ajustarSprite(im, $("arena"), l) });
    $("nome-" + l).textContent = bonito(b[slot].nome);
    definirHp(l, b[slot].hp_max, b[slot].hp_max);
  }
  const fav = b[b.svm.favorito], sim = b.simulador, pctA = sim.vitorias_a / sim.n;
  const favSim = pctA >= .5 ? b.a : b.b, pctFav = Math.max(pctA, 1 - pctA);
  $("previsao").innerHTML = `
    <div>A IA (SVM) aposta em</div><div class="grande">${bonito(fav.nome)}</div>
    <div class="conf"><div style="width:${b.svm.confianca * 100}%"></div></div>
    <div class="dica">score do SVM: ${b.svm.score > 0 ? "+" : ""}${b.svm.score} (quanto mais longe de 0, mais confiante)</div>
    <hr style="border-color:var(--borda)">
    <div>Pelo simulador, <b style="text-transform:capitalize">${bonito(favSim.nome)}</b> vence
      <b>${Math.round(pctFav * 100)}%</b> de ${sim.n} batalhas.</div>`;

  mostrarHistorico(b);
  mostrarExplicacao(b);

  await falar(`${estado.jogadores[dele].nome} enviou ${bonito(b[dele].nome)}!`, 700);
  await falar(espectador ? `${estado.jogadores[meu].nome} enviou ${bonito(b[meu].nome)}!` : `Vai, ${bonito(b[meu].nome)}!`, 700);

  for (const ev of b.eventos) {
    const atk = lado(ev.atacante), alvo = atk === "eu" ? "op" : "eu";
    const slotAlvo = ev.atacante === "a" ? "b" : "a";
    await falar(`${bonito(b[ev.atacante].nome)} usou ${bonito(ev.golpe)}!`, 250);
    $("sprite-" + atk).classList.add("ataca-" + atk); await esperar(220);
    $("sprite-" + atk).classList.remove("ataca-" + atk);
    if (ev.errou) { await falar("Mas errou!", 700); continue; }
    $("sprite-" + alvo).classList.add("dano");
    definirHp(alvo, ev.hp[slotAlvo], b[slotAlvo].hp_max);
    await esperar(650);
    $("sprite-" + alvo).classList.remove("dano");
    if (ev.acertos > 1) await falar(`Acertou ${ev.acertos} vezes!`, 500);
    if (ev.criticos > 0) await falar("Golpe crítico!", 500);
    if (ev.eficacia > 1) await falar("É super efetivo!", 600);
    else if (ev.eficacia > 0 && ev.eficacia < 1) await falar("Não é muito efetivo...", 600);
    if (ev.hp_atacante_variou !== 0) {
      definirHp(atk, ev.hp[ev.atacante], b[ev.atacante].hp_max);
      await falar(ev.hp_atacante_variou < 0 ? `${bonito(b[ev.atacante].nome)} sofreu dano de retorno!`
                                              : `${bonito(b[ev.atacante].nome)} recuperou HP!`, 600);
    }
    for (const [slot, l] of [[slotAlvo, alvo], [ev.atacante, atk]]) {
      if (ev.hp[slot] <= 0) { $("sprite-" + l).classList.add("desmaio"); await falar(`${bonito(b[slot].nome)} desmaiou!`, 900); }
    }
  }

  const venc = b[b.vencedor];
  const quem = !espectador && b.vencedor === meu ? "Você venceu!" : `${estado.jogadores[b.vencedor].nome} venceu!`;
  await falar(`${quem} ${bonito(venc.nome)} é o campeão da arena!`, 200);

  // Dois vereditos: a batalha que acabou de acontecer e o favorito (quem vence a maioria das 201 simulações).
  // O modelo foi treinado para prever o favorito; uma batalha isolada também depende de sorte.
  const favSlot = b.simulador.favorito;
  const iaCertaBatalha = b.svm.favorito === b.vencedor, iaCertaFavorito = b.svm.favorito === favSlot;
  const zebra = b.vencedor !== favSlot, apertado = pctFav < 0.65;
  const chanceVenc = b.vencedor === "a" ? pctA : 1 - pctA;
  let nota;
  if (iaCertaFavorito && !zebra) nota = "A IA apostou no favorito, e ele venceu.";
  else if (iaCertaFavorito && zebra) nota = `A aposta da IA estava certa (${bonito(b[favSlot].nome)} vence a maioria das batalhas), mas desta vez deu zebra.`;
  else if (!iaCertaFavorito && zebra) nota = `A IA acertou esta batalha por sorte: o favorito era ${bonito(b[favSlot].nome)}.`;
  else nota = `A IA apostou em ${bonito(fav.nome)}, mas o favorito era ${bonito(b[favSlot].nome)}, que venceu.`;
  if (apertado) nota += ` Confronto equilibrado (${Math.round(pctFav * 100)}% × ${Math.round((1 - pctFav) * 100)}%): quase uma moeda.`;
  const linha = (rotulo, ok) => `<div class="veredito ${ok ? "certo" : "errado"}"><span>${rotulo}</span><b>${ok ? "IA acertou ✔" : "IA errou ✘"}</b></div>`;
  $("resultado").innerHTML = `<div class="vencedor">🏆 ${bonito(venc.nome)} venceu</div>
    ${zebra ? `<div class="dica" style="text-align:center">Zebra! ${bonito(venc.nome)} só venceria ${Math.round(chanceVenc * 100)}% das vezes.</div>` : ""}
    ${linha("Nesta batalha", iaCertaBatalha)}
    ${linha("Favorito (201 batalhas)", iaCertaFavorito)}
    <div class="dica">${nota}</div>`;
  $("resultado").hidden = false; $("acoes").hidden = espectador;
  if (window.matchMedia("(max-width: 900px)").matches)       // celular: mostra o resultado, que fica abaixo da arena
    $("resultado").scrollIntoView({ behavior: "smooth", block: "center" });
}

// ---------- esta batalha estava nos dados? (treino, teste ou inédita) ----------
function mostrarHistorico(b) {
  const h = b.historico;
  if (!h) { $("historico").innerHTML = ""; return; }
  const nA = bonito(b.a.nome), nB = bonito(b.b.nome);
  if (h.situacao === "inedita") {
    $("historico").innerHTML = `<div class="historico inedita"><b>🆕 Batalha inédita</b>
      Este confronto não estava nos dados. A IA nunca viu estes dois se enfrentando: está <b>generalizando</b>
      a partir de situações parecidas.</div>`;
    return;
  }
  const fav = h.favorito === "a" ? nA : nB;
  const placar = `${nA} venceu <b>${h.vitorias_a} de ${h.n}</b> simulações (favorito: <b>${fav}</b>)`;
  if (h.situacao === "treino") {
    $("historico").innerHTML = `<div class="historico treino"><b>📚 Esta batalha estava no treino</b>
      Nos dados de treino, ${placar}.<br>
      ${h.ia_concorda
        ? "A IA <b>concorda</b> com o que viu no treino."
        : `A IA <b>discorda</b> do próprio treino: mesmo tendo visto esta batalha, ela aposta em ${b.svm.favorito === "a" ? nA : nB}.`}
      <span class="dica">O SVM não decora resultados: ele aprende regras gerais e aceita errar alguns exemplos do treino
      (margem suave), para não se ajustar demais a casos isolados.</span></div>`;
  } else {
    $("historico").innerHTML = `<div class="historico teste"><b>🧪 Esta batalha estava no conjunto de ${h.situacao === "teste" ? "teste" : "dados extras"}</b>
      Ela existe nos dados (${placar}), mas <b>não foi usada no treino</b>: a IA nunca a viu.
      ${h.ia_concorda ? "Mesmo assim, a IA acertou o favorito." : "A IA apostou diferente do resultado registrado."}</div>`;
  }
}

// ---------- explicação da previsão com os conceitos do SVM ----------
// Cada tópico é um <details> fechado: só abre quando o jogador clica.
function mostrarExplicacao(b) {
  const e = b.svm.explicacao;
  if (!e) { $("explicacao").innerHTML = ""; return; }
  const nA = bonito(b.a.nome), nB = bonito(b.b.nome);
  const ladoNome = e.score > 0 ? nA : nB;
  const pos = (v) => (Math.max(-3, Math.min(3, v)) + 3) / 6 * 100;
  const maxF = Math.max(...e.fatores.map((f) => Math.abs(f.efeito)), 0.01);
  const barra = (v, lado) => (lado === "a" ? v > 0 : v < 0) ? `<div style="width:${Math.abs(v) / maxF * 100}%"></div>` : "";
  const simNao = (v) => (v ? "sim" : "não");
  const topico = (titulo, conteudo) => `<details class="topico"><summary>${titulo}</summary><div class="bloco">${conteudo}</div></details>`;

  // votos: contribuição > 0 significa que, na batalha de referência, venceu o lado A (mesma posição de nA aqui)
  const votos = { a: 0, b: 0 };
  e.vetores.forEach((v) => { votos[v.contribuicao > 0 ? "a" : "b"]++; });

  $("explicacao").innerHTML = `
    <div class="explica-titulo">Por que a IA apostou em ${ladoNome}? <span class="dica">(clique para abrir)</span></div>

    ${topico("1. Fronteira de decisão e margem", `
      <p class="explica">Cada batalha vira um ponto com ${COLUNAS_EXPLICADAS} números. O SVM separa "${nA} vence" de
        "${nB} vence" por uma <b>fronteira</b> (hiperplano). O <b>score</b> é a distância até ela:
        <b>${e.score > 0 ? "+" : ""}${e.score}</b>, do lado de <b>${ladoNome}</b>.
        ${e.dentro_da_margem ? "Está <b>dentro da margem</b> (entre −1 e +1): zona de dúvida."
                             : "Está <b>fora da margem</b>: decisão segura para o modelo."}</p>
      <div class="regua">
        <div class="eixo"></div>
        <div class="margem" style="left:${pos(-1)}%;width:${pos(1) - pos(-1)}%"></div>
        <div class="hiperplano" style="left:50%"></div>
        <div class="ponto" style="left:${pos(e.score)}%"></div>
      </div>
      <div class="regua-legenda"><span>← ${nB}</span><span>margem</span><span>${nA} →</span></div>`)}

    ${topico("2. O que mais pesou nesta batalha", `
      <p class="explica">Quanto o score muda se cada fator for "neutralizado" (igual para os dois). Barra para a direita favorece
        ${nA}; para a esquerda, ${nB}. É uma estimativa: no kernel RBF os fatores interagem.</p>
      <div class="lados"><span>← ${nB}</span><span>${nA} →</span></div>
      ${e.fatores.map((f) => `<div class="fator"><span class="nome">${f.fator}</span>
        <div class="lado b">${barra(f.efeito, "b")}</div><div class="lado a">${barra(f.efeito, "a")}</div></div>`).join("")}`)}

    ${topico("3. O que a IA comparou", `
      <table class="comparou">
        <tr><th></th><th>${nA}</th><th>${nB}</th></tr>
        <tr><td>Velocidade (base)</td><td>${b.a.atributos.Speed}</td><td>${b.b.atributos.Speed}</td></tr>
        <tr><td>HP (base)</td><td>${b.a.atributos.HP}</td><td>${b.b.atributos.HP}</td></tr>
        <tr><td>Tipo: golpe do próprio tipo contra o outro</td><td>${e.comparou.mult_tipo.a}×</td><td>${e.comparou.mult_tipo.b}×</td></tr>
        <tr><td>Melhor golpe: % do HP do outro por turno</td><td>${e.comparou.dano_turno.a}%</td><td>${e.comparou.dano_turno.b}%</td></tr>
        <tr><td>Golpes para nocautear</td><td>${e.comparou.nocaute.a}</td><td>${e.comparou.nocaute.b}</td></tr>
        <tr><td>Tem golpe de prioridade</td><td>${simNao(e.comparou.prioridade.a)}</td><td>${simNao(e.comparou.prioridade.b)}</td></tr>
      </table>`)}

    ${topico("4. Batalhas de referência (vetores de suporte)", `
      <p class="explica">A IA não decide do zero: ela compara esta batalha com batalhas do treino que guardou como
        <b>referência</b>, os <b>vetores de suporte</b> (${e.n_vetores_suporte.toLocaleString("pt-BR")} no total).
        "Parecida" quer dizer a <b>mesma situação</b> (diferença de velocidade e de força, vantagem de tipo, golpes para
        nocautear), não Pokémon parecidos.</p>
      <p class="explica">Cada referência funciona como um <b>voto</b>: se nela venceu o Pokémon que estava <b>na mesma posição
        de ${nA}</b>, o voto vai para ${nA}; se venceu o que estava na posição de ${nB}, vai para ${nB}. Quanto mais
        parecida, mais o voto pesa. Abaixo, as ${e.vetores.length} que mais pesaram:
        <b class="puxa-a">${votos.a} para ${nA}</b> e <b class="puxa-b">${votos.b} para ${nB}</b>.
        A decisão final é a <b>soma ponderada de todos os votos</b> (não só destes), e ela deu ${ladoNome}.</p>
      ${e.vetores.map((v) => {
        const voto = v.contribuicao > 0 ? "a" : "b";
        const nomeVenc = bonito(v.vencedor === "a" ? v.a_nome : v.b_nome);
        return `<div class="vetor"><img data-id="${v.a_id}"><img data-id="${v.b_id}">
          <div class="txt"><b>${bonito(v.a_nome)}</b> × <b>${bonito(v.b_nome)}</b>
          <span class="dica">(${Math.round(v.semelhanca * 100)}% parecida)</span><br>
          Venceu ${nomeVenc}, que estava na posição de ${voto === "a" ? nA : nB}
          → <b class="puxa-${voto}">voto para ${voto === "a" ? nA : nB}</b></div></div>`;
      }).join("")}`)}`;
  document.querySelectorAll("#explicacao .vetor img").forEach((img) => colocarSprite(img, +img.dataset.id, { animado: false }));
}
const COLUNAS_EXPLICADAS = 15;

$("btn-revanche").onclick = async () => {
  try { aplicarEstado(await api(`/api/salas/${sala}/revanche`, { token })); } catch (e) { alert(e.message); }
};

window.addEventListener("resize", () => {
  for (const l of ["eu", "op"]) ajustarSprite($("sprite-" + l), $("arena"), l);
});

// ---------- inicialização ----------
(async function iniciar() {
  for (let g = 1; g <= 9; g++) $("filtro-geracao").add(new Option(`Geração ${g}`, g));
  LISTA = await api("/api/pokemon");
  porId = Object.fromEntries(LISTA.map((p) => [p.id, p]));
  desenharGrade();
  const codigo = new URLSearchParams(location.search).get("sala");
  if (codigo) {
    $("codigo").value = codigo;
    const tk = lerToken(codigo.toUpperCase());
    if (tk) {                                          // já estava nesta sala (recarregou a página)
      try { await entrarNaSala(await api(`/api/salas/${codigo}/entrar`, { token: tk })); return; } catch {}
    }
    // chegou por um convite (link ou QR Code): destaca a entrada na sala e esconde "Criar sala"
    $("aviso-convite").hidden = false;
    $("codigo-convite").textContent = codigo.toUpperCase();
    for (const id of ["subtitulo-inicio", "btn-criar", "ou-inicio"]) $(id).hidden = true;
    $("btn-entrar").classList.add("principal");
    $("btn-entrar").textContent = "Entrar na sala " + codigo.toUpperCase();
  }
  mostrar("inicio");
  if (codigo) $("nome").focus();
})();
