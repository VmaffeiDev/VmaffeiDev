#!/usr/bin/env python3
"""
Gera o hero banner (dark.svg / light.svg) do README, no estilo
"terminal ao vivo" com painel VISUAL.MAP (dot-art colorido e animado)
e SYSTEM.INFO (linhas com leader pontilhado e revelacao escalonada).

Uso:
    python3 gerar_hero.py --pontos dots.txt

Requer apenas a biblioteca padrao.
"""

import argparse
import re

MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

TITULO_ARQUIVO = "vmaffei.dev@gmail.com"
TERMINAL_CMD = "vmaffei.dev@gmail.com - % ./profile.sh --live"

CAMPOS = [
    ("Subject", "Victor Giuliano Coutinho Maffei"),
    ("Role", "Consultor de vendas → Suporte de TI"),
    ("Origin", "Curitiba, Paraná - Brasil"),
    ("Education", "Análise e Desenvolvimento de Sistemas, Estácio"),
    ("Status", "Aberto a primeira vaga em TI"),
]

STACK = [
    ("Core.Lang", "Python, JavaScript, SQL"),
    ("Core.Front", "HTML, CSS, React"),
    ("Core.Ops", "Windows, Linux, redes, Active Directory"),
    ("Core.Data", "Excel, Power BI, Google Sheets"),
    ("Core.Interest", "Cibersegurança, automação, help desk"),
]

CONTATO = [
    ("Grid.Mail", "vmaffei.dev@gmail.com"),
    ("Grid.Site", "consultordevendasvictormaffei.com"),
    ("Grid.LinkedIn", "in/victor-maffei"),
    ("Grid.GitHub", "@VmaffeiDev"),
]

RODAPE = "> Mais detalhes nos projetos abaixo"

THEMES = {
    "dark": dict(
        bg_outer="#070B16",
        window_bg="#060917",
        panel_top="#0A0F2E",
        panel_bot="#060917",
        titlebar_bg="#0B1024",
        line="rgba(255,255,255,0.10)",
        label="#7DE2F7",
        value="#D6DEFF",
        dim="#5C6EA8",
        leader="rgba(214,222,255,0.28)",
        term_text="#5C6EA8",
        box_stroke="rgba(34,211,238,0.35)",
        box_fill="#0A0F2E",
        chip_fill="rgba(168,85,247,0.12)",
        chip_stroke="#A855F7",
        chip_text="#D6DEFF",
        grad_border=("#A855F7", "#22D3EE", "#7DE2F7"),
        grad_dots=("#60A5FA", "#A855F7", "#22D3EE"),
        live="#F87171",
    ),
    "light": dict(
        bg_outer="#E2E8F0",
        window_bg="#FFFFFF",
        panel_top="#F8FAFC",
        panel_bot="#FFFFFF",
        titlebar_bg="#F1F5F9",
        line="rgba(15,23,42,0.10)",
        label="#7E22CE",
        value="#0F172A",
        dim="#64748B",
        leader="rgba(15,23,42,0.22)",
        term_text="#64748B",
        box_stroke="rgba(124,58,237,0.35)",
        box_fill="#F8FAFC",
        chip_fill="rgba(124,58,237,0.08)",
        chip_stroke="#7C3AED",
        chip_text="#312E81",
        grad_border=("#7C3AED", "#0891B2", "#7E22CE"),
        grad_dots=("#2563EB", "#7C3AED", "#0891B2"),
        live="#DC2626",
    ),
}


def carregar_pontos(caminho):
    txt = open(caminho, encoding="utf-8").read()
    return re.findall(
        r'<circle cx="([\d.]+)" cy="([\d.]+)" r="([\d.]+)" fill="[^"]+" opacity="([\d.]+)"/>',
        txt,
    )


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def linha_info(x, y, label, valor, delay, cor):
    """Uma linha 'Label ..... Valor' com largura total fixa via textLength,
    dentro de um grupo que aparece com fade + leve deslize (efeito de boot)."""
    total_w = 550
    dots = "." * 70
    return (
        f'<g opacity="0">'
        f'<animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{delay:.2f}s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" '
        f'values="-8 0;0 0" dur="0.4s" begin="{delay:.2f}s" fill="freeze"/>'
        f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="13.5" '
        f'textLength="{total_w}" lengthAdjust="spacingAndGlyphs" xml:space="preserve">'
        f'<tspan fill="{cor["label"]}">{esc(label)} </tspan>'
        f'<tspan fill="{cor["leader"]}">{dots}</tspan>'
        f'<tspan fill="{cor["value"]}" font-weight="600"> {esc(valor)}</tspan>'
        f"</text></g>"
    )


def montar(tema_nome, pontos):
    cor = THEMES[tema_nome]
    W, H = 1180, 664

    # ---- VISUAL.MAP: dots recoloridos com gradiente animado + revelacao (clip) ----
    dot_svg = []
    for cx, cy, r, op in pontos:
        dot_svg.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#dotsGrad)" opacity="{op}"/>')
    dots_markup = "\n      ".join(dot_svg)

    # ---- SYSTEM.INFO: linhas com leader pontilhado, revelacao escalonada ----
    y = 190
    delay = 0.75
    linhas = []
    for label, valor in CAMPOS:
        linhas.append(linha_info(576, y, label, valor, delay, cor))
        y += 25
        delay += 0.10
    y += 12
    for label, valor in STACK:
        linhas.append(linha_info(576, y, label, valor, delay, cor))
        y += 25
        delay += 0.10
    sep_y = y + 12
    y += 42
    for label, valor in CONTATO:
        linhas.append(linha_info(576, y, label, valor, delay, cor))
        y += 25
        delay += 0.10
    rodape_y = H - 40

    blocos = "\n  ".join(linhas)

    accent_a, accent_b, accent_c = cor["grad_border"]
    dot_a, dot_b, dot_c = cor["grad_dots"]

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{MONO}" role="img" aria-label="Victor Maffei -- profile.sh --live">
<defs>
  <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{accent_a}"><animate attributeName="stop-color" values="{accent_a};{accent_b};{accent_c};{accent_a}" dur="10s" repeatCount="indefinite"/></stop>
    <stop offset="0.5" stop-color="{accent_b}"><animate attributeName="stop-color" values="{accent_b};{accent_c};{accent_a};{accent_b}" dur="10s" repeatCount="indefinite"/></stop>
    <stop offset="1" stop-color="{accent_c}"><animate attributeName="stop-color" values="{accent_c};{accent_a};{accent_b};{accent_c}" dur="10s" repeatCount="indefinite"/></stop>
  </linearGradient>
  <linearGradient id="dotsGrad" x1="0" y1="0" x2="0" y2="{H}" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{dot_a}"/>
    <stop offset="0.5" stop-color="{dot_b}"/>
    <stop offset="1" stop-color="{dot_c}"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="0 -140; 0 140; 0 -140" dur="9s" repeatCount="indefinite"/>
  </linearGradient>
  <linearGradient id="panelGrad" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{cor['panel_top']}"/>
    <stop offset="1" stop-color="{cor['panel_bot']}"/>
  </linearGradient>
  <filter id="glow6" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="6"/></filter>
  <filter id="txtGlow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="0.8" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <clipPath id="winClip"><rect x="16" y="16" width="{W - 32}" height="{H - 32}" rx="18"/></clipPath>
  <clipPath id="mapReveal">
    <rect x="58" y="112" width="400" height="0" >
      <animate attributeName="height" values="0;480" dur="1.6s" begin="0.15s" fill="freeze" calcMode="spline" keySplines=".4 0 .2 1"/>
    </rect>
  </clipPath>
</defs>

<rect width="{W}" height="{H}" fill="{cor['bg_outer']}"/>

<g clip-path="url(#winClip)">
  <rect x="16" y="16" width="{W - 32}" height="{H - 32}" fill="url(#panelGrad)"/>

  <!-- barra de titulo -->
  <rect x="16" y="16" width="{W - 32}" height="46" fill="{cor['titlebar_bg']}"/>
  <line x1="16" y1="62" x2="{W - 16}" y2="62" stroke="{cor['line']}"/>
  <circle cx="52" cy="39" r="7" fill="#FF5F57"/>
  <circle cx="76" cy="39" r="7" fill="#FEBC2E"/>
  <circle cx="100" cy="39" r="7" fill="#28C840"/>
  <text x="{W / 2}" y="43" text-anchor="middle" font-size="12" fill="{cor['term_text']}">{esc(TERMINAL_CMD)}</text>

  <!-- painel esquerdo -->
  <text x="62" y="90" font-size="13" letter-spacing="3" fill="{cor['label']}">VISUAL.MAP</text>
  <rect x="58" y="112" width="400" height="480" rx="10" fill="{cor['box_fill']}" stroke="{cor['box_stroke']}" stroke-width="1.5"/>
  <g clip-path="url(#mapReveal)">
    {dots_markup}
  </g>

  <!-- painel direito -->
  <text x="576" y="90" font-size="13" letter-spacing="3" fill="{cor['label']}" filter="url(#txtGlow)">SYSTEM.INFO</text>
  <text x="{W - 44}" y="90" text-anchor="end" font-size="12" font-weight="700" fill="{cor['live']}">
    <tspan>&#9679;</tspan> LIVE
    <animate attributeName="opacity" values="1;0.25;1" dur="1.6s" repeatCount="indefinite"/>
  </text>
  <rect x="576" y="102" width="252" height="24" rx="6" fill="{cor['chip_fill']}" stroke="{cor['chip_stroke']}"/>
  <text x="588" y="119" font-size="13" font-weight="700" fill="{cor['chip_text']}">{esc(TITULO_ARQUIVO)}</text>

  {blocos}

  <text x="576" y="{sep_y}" font-size="13" fill="{cor['dim']}">- Contato</text>

  <text x="576" y="{rodape_y}" font-size="12.5" fill="{cor['dim']}" xml:space="preserve">{esc(RODAPE)} <tspan fill="{cor['label']}">&#9646;<animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></tspan></text>

  <rect x="16" y="16" width="{W - 32}" height="{H - 32}" rx="18" fill="none" stroke="url(#accent)" stroke-width="2" filter="url(#glow6)" opacity="0.75"/>
</g>
<rect x="16" y="16" width="{W - 32}" height="{H - 32}" rx="18" fill="none" stroke="url(#accent)" stroke-width="1.5"/>
</svg>
"""


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--pontos", default="dots.txt")
    p.add_argument("--saida-dark", default="dark.svg")
    p.add_argument("--saida-light", default="light.svg")
    a = p.parse_args()

    pontos = carregar_pontos(a.pontos)

    with open(a.saida_dark, "w", encoding="utf-8") as f:
        f.write(montar("dark", pontos))
    print(f"gerado: {a.saida_dark}")

    with open(a.saida_light, "w", encoding="utf-8") as f:
        f.write(montar("light", pontos))
    print(f"gerado: {a.saida_light}")


if __name__ == "__main__":
    main()
