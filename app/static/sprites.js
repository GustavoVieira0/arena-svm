// Sprites dos Pokémon (repositório PokeAPI/sprites), com alternativas e tamanho proporcional.
// Usado pela arena (jogo.js) e pela galeria de validação (galeria.html).
const SPRITES = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon";

// Escala de cada tipo de imagem em relação ao sprite animado (showdown), que é recortado no tamanho do Pokémon.
//  - gif: sprite animado, recortado (tamanho real do Pokémon)
//  - png: sprite estático 96×96 com margem transparente (o Pokémon ocupa só parte do quadro)
//  - arte: arte oficial 475×475, usada só quando não existe sprite
const FATOR_FONTE = { gif: 1, png: 1, arte: 0.2 };
const MARGEM_INFERIOR = { gif: 0, png: 0.14, arte: 0.06 };   // espaço vazio abaixo dos pés, por tipo

function fontesSprite(id, costas, animado) {
  const f = [];
  if (animado) f.push({ url: `${SPRITES}/other/showdown/${costas ? "back/" : ""}${id}.gif`, tipo: "gif" });
  f.push({ url: `${SPRITES}/${costas ? "back/" : ""}${id}.png`, tipo: "png" });
  if (costas) {                                    // sem sprite de costas: usa o de frente espelhado
    if (animado) f.push({ url: `${SPRITES}/other/showdown/${id}.gif`, tipo: "gif", espelhar: true });
    f.push({ url: `${SPRITES}/${id}.png`, tipo: "png", espelhar: true });
  }
  f.push({ url: `${SPRITES}/other/official-artwork/${id}.png`, tipo: "arte", espelhar: costas });
  return f;
}

/** Coloca o sprite no <img>, tentando as alternativas. `aoCarregar(img, fonte)` é chamado com a fonte usada. */
function colocarSprite(img, id, { costas = false, animado = true, aoCarregar = null } = {}) {
  const fontes = fontesSprite(id, costas, animado);
  let i = 0;
  const tentar = () => { img.dataset.fonte = JSON.stringify(fontes[i]); img.src = fontes[i].url; };
  img.onerror = () => { if (++i < fontes.length) tentar(); };
  img.onload = () => aoCarregar && aoCarregar(img, fontes[i]);
  tentar();
}

/**
 * Define a altura do sprite na arena de forma proporcional ao tamanho real do Pokémon.
 * lado: "op" (oponente, de frente, mais distante) ou "eu" (de costas, mais perto).
 */
function ajustarSprite(img, arena, lado) {
  if (!img.naturalHeight) return;
  const fonte = JSON.parse(img.dataset.fonte || "{}");
  const larg = arena.clientWidth, alt = arena.clientHeight;
  const escala = larg / (lado === "eu" ? 300 : 380) * (FATOR_FONTE[fonte.tipo] || 1);
  const limite = alt * (lado === "eu" ? 0.62 : 0.5);
  const h = Math.min(img.naturalHeight * escala, limite);
  img.style.height = h + "px";
  img.style.width = "auto";
  img.style.setProperty("--flip", fonte.espelhar ? -1 : 1);
  img.style.setProperty("--pad", (MARGEM_INFERIOR[fonte.tipo] || 0) * 100 + "%");
  img.classList.toggle("estatico", fonte.tipo !== "gif");
}
