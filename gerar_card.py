#!/usr/bin/env python3
"""
Gera o card SYSTEM.INFO (SVG) do README do GitHub.

Uso:
    python3 gerar_card.py                      # usa a silhueta padrao
    python3 gerar_card.py --foto minha.jpg     # usa a sua foto
    python3 gerar_card.py --foto minha.jpg --saida assets/system-info.svg

Requer: pip install pillow
"""

import argparse
from PIL import Image, ImageDraw, ImageFilter, ImageOps

# ---------------------------------------------------------------- paleta
BG        = "#060917"
PANEL     = "#0A0F2E"
BORDER_A  = "#A855F7"
BORDER_B  = "#22D3EE"
DOT       = "#E4A8FF"
LABEL     = "#7DE2F7"
VALUE     = "#D6DEFF"
DIM       = "#5C6EA8"
MONO      = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

# ---------------------------------------------------------------- conteudo
TITULO_ARQUIVO = "VmaffeiDev / README.md"
BARRA_URL      = "victormaffei.connect"

CAMPOS = [
    ("Subject",         "Victor Giuliano Coutinho Maffei"),
    ("Role",            "Consultor de vendas → Suporte de TI"),
    ("Origin",          "Curitiba, Paraná — Brasil"),
    ("Education",       "Análise e Desenvolvimento de Sistemas, Estácio"),
    ("Status",          "Aberto a primeira vaga em TI"),
    ("ToolChain",       ""),
]

STACK = [
    ("Core.Lang",       "Python, JavaScript, SQL"),
    ("Core.Front",      "HTML, CSS, React"),
    ("Core.Ops",        "Windows, Linux, redes, Active Directory"),
    ("Core.Data",       "Excel, Power BI, Google Sheets"),
    ("Core.Interest",   "Cibersegurança, automação, help desk"),
]

CONTATO = [
    ("Grid.Mail",       "vmaffei.dev@gmail.com"),
    ("Grid.Site",       "consultordevendasvictormaffei.com"),
    ("Grid.LinkedIn",   "in/victor-maffei"),
    ("Grid.GitHub",     "@VmaffeiDev"),
]

RODAPE = "> Mais detalhes nos projetos abaixo"

# ---------------------------------------------------------------- dot art


def silhueta_padrao(tamanho=(300, 380)):
    """Desenha uma silhueta de busto para usar quando nao ha foto."""
    w, h = tamanho
    img = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(img)
    d.ellipse([w * 0.30, h * 0.10, w * 0.70, h * 0.52], fill=255)
    d.ellipse([w * 0.10, h * 0.55, w * 0.90, h * 1.30], fill=255)
    return img.filter(ImageFilter.GaussianBlur(6))


def carregar(foto, tamanho=(300, 380)):
    if not foto:
        return silhueta_padrao(tamanho)
    img = Image.open(foto).convert("L")
    img = ImageOps.autocontrast(img, cutoff=2)
    img = ImageOps.fit(img, tamanho, Image.LANCZOS)
    return img


def gerar_dots(img, cols=48, rows=62, x0=74, y0=120, passo=7.5):
    """Converte a imagem em circulos de raio variavel."""
    small = img.resize((cols, rows), Image.LANCZOS)
    px = small.load()
    saida = []
    for j in range(rows):
        for i in range(cols):
            v = px[i, j] / 255.0
            if v < 0.16:
                continue
            r = round(0.6 + v * 2.1, 2)
            op = round(0.25 + v * 0.75, 2)
            cx = round(x0 + i * passo, 1)
            cy = round(y0 + j * passo, 1)
            saida.append(
                f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{DOT}" opacity="{op}"/>'
            )
    return "\n      ".join(saida)


# ---------------------------------------------------------------- svg


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def linhas_info(x_label, x_value, y0, itens, salto=25):
    out, y = [], y0
    for label, valor in itens:
        out.append(
            f'<text x="{x_label}" y="{y}" font-family="{MONO}" font-size="14" '
            f'fill="{LABEL}">{esc(label)}</text>'
        )
        if valor:
            out.append(
                f'<text x="{x_value}" y="{y}" font-family="{MONO}" font-size="13.5" '
                f'fill="{VALUE}" text-anchor="end">{esc(valor)}</text>'
            )
        y += salto
    return "\n    ".join(out), y


def montar(dots):
    W, H = 1180, 664

    bloco1, y = linhas_info(560, 1120, 176, CAMPOS)
    bloco2, y = linhas_info(560, 1120, y + 10, STACK)
    sep = (
        f'<text x="560" y="{y + 12}" font-family="{MONO}" font-size="13" '
        f'fill="{DIM}">- Contato</text>'
    )
    bloco3, y = linhas_info(560, 1120, y + 42, CONTATO)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Cartao de apresentacao de Victor Maffei">
  <defs>
    <linearGradient id="borda" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{BORDER_A}"/>
      <stop offset="100%" stop-color="{BORDER_B}"/>
    </linearGradient>
    <linearGradient id="fundo" x1="0" y1="0" x2="0.6" y2="1">
      <stop offset="0%" stop-color="{PANEL}"/>
      <stop offset="100%" stop-color="{BG}"/>
    </linearGradient>
    <filter id="brilho" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="6" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <rect width="{W}" height="{H}" fill="{BG}"/>

  <!-- janela -->
  <rect x="16" y="16" width="{W - 32}" height="{H - 32}" rx="18"
        fill="url(#fundo)" stroke="url(#borda)" stroke-width="2" filter="url(#brilho)"/>

  <!-- barra de titulo -->
  <circle cx="52" cy="52" r="7" fill="#FF5F57"/>
  <circle cx="76" cy="52" r="7" fill="#FEBC2E"/>
  <circle cx="100" cy="52" r="7" fill="#28C840"/>
  <text x="{W - 44}" y="57" font-family="{MONO}" font-size="14" fill="{DIM}"
        text-anchor="end">{esc(BARRA_URL)}</text>
  <line x1="34" y1="76" x2="{W - 34}" y2="76" stroke="{BORDER_A}" stroke-width="1" opacity="0.28"/>

  <!-- painel esquerdo -->
  <text x="62" y="104" font-family="{MONO}" font-size="13" fill="{LABEL}"
        letter-spacing="3">VISUAL.MAP</text>
  <rect x="58" y="112" width="400" height="480" rx="6" fill="none"
        stroke="{BORDER_B}" stroke-width="1" opacity="0.35"/>
  <g>
      {dots}
  </g>

  <!-- painel direito -->
  <text x="560" y="104" font-family="{MONO}" font-size="13" fill="{LABEL}"
        letter-spacing="3">SYSTEM.INFO</text>
  <rect x="556" y="116" width="216" height="24" rx="6" fill="none"
        stroke="{BORDER_A}" stroke-width="1"/>
  <text x="570" y="133" font-family="{MONO}" font-size="13"
        fill="{BORDER_A}">{esc(TITULO_ARQUIVO)}</text>

    {bloco1}
    {bloco2}
    {sep}
    {bloco3}

  <text x="560" y="{H - 40}" font-family="{MONO}" font-size="12.5"
        fill="{DIM}">{esc(RODAPE)}</text>
</svg>
"""


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--foto", default=None, help="caminho da sua foto")
    p.add_argument("--saida", default="system-info.svg")
    a = p.parse_args()

    img = carregar(a.foto)
    svg = montar(gerar_dots(img))
    with open(a.saida, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"gerado: {a.saida}")


if __name__ == "__main__":
    main()
