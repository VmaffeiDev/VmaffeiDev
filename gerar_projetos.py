#!/usr/bin/env python3
"""
Gera o painel PROJECTS.LIST (SVG) lendo os repositorios direto da API do GitHub.

Uso:
    python3 gerar_projetos.py --usuario VmaffeiDev
    python3 gerar_projetos.py --usuario VmaffeiDev --limite 6 --saida projects.svg

Dentro do GitHub Actions o token entra sozinho pela variavel GITHUB_TOKEN.
"""

import argparse
import json
import os
import urllib.request

API = "https://api.github.com"

BG       = "#060917"
CARD     = "#0A0F2E"
BORDER   = "#A855F7"
ACCENT   = "#22D3EE"
NAME     = "#C4B5FD"
TEXT     = "#D6DEFF"
DIM      = "#5C6EA8"
MONO     = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

# cores por linguagem (as que faltarem caem no roxo padrao)
CORES = {
    "Python": "#3572A5", "JavaScript": "#F1E05A", "TypeScript": "#3178C6",
    "HTML": "#E34C26", "CSS": "#563D7C", "Dart": "#00B4AB", "C++": "#F34B7D",
    "C": "#555555", "C#": "#178600", "Java": "#B07219", "PHP": "#4F5D95",
    "Shell": "#89E051", "Go": "#00ADD8", "Ruby": "#701516", "Kotlin": "#A97BFF",
    "Swift": "#F05138", "CMake": "#DA3434", "Jupyter Notebook": "#DA5B0B",
    "SQL": "#E38C00", "PowerShell": "#012456", "Vue": "#41B883",
}


def pegar(url):
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "gerar-projetos",
    })
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def repositorios(usuario, limite):
    repos = pegar(f"{API}/users/{usuario}/repos?per_page=100&sort=pushed")
    repos = [r for r in repos if not r["fork"] and not r["archived"]]
    repos.sort(key=lambda r: (r["stargazers_count"], r["pushed_at"]), reverse=True)
    escolhidos = repos[:limite]
    for r in escolhidos:
        try:
            langs = pegar(r["languages_url"])
        except Exception:
            langs = {}
        total = sum(langs.values()) or 1
        r["_langs"] = sorted(
            ((k, v * 100 / total) for k, v in langs.items()),
            key=lambda x: -x[1],
        )[:4]
    return escolhidos


def esc(t):
    return (t or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def quebrar(texto, largura=52, linhas=2):
    palavras = (texto or "").split()
    saida, atual = [], ""
    for p in palavras:
        if len(atual) + len(p) + 1 <= largura:
            atual = f"{atual} {p}".strip()
        else:
            saida.append(atual)
            atual = p
            if len(saida) == linhas:
                break
    if atual and len(saida) < linhas:
        saida.append(atual)
    if len(saida) == linhas and len(" ".join(saida)) < len(texto or ""):
        saida[-1] = saida[-1][:largura - 3] + "..."
    return saida


def donut(cx, cy, pct, cor):
    """Anel de progresso mostrando o peso da linguagem principal."""
    r = 26
    circ = 2 * 3.14159 * r
    traco = circ * pct / 100
    return f"""
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{CARD}" stroke-width="6"/>
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{cor}" stroke-width="6"
            stroke-linecap="round" stroke-dasharray="{traco:.1f} {circ:.1f}"
            transform="rotate(-90 {cx} {cy})"/>
    <text x="{cx}" y="{cy + 5}" font-family="{MONO}" font-size="13" fill="{TEXT}"
          text-anchor="middle">{pct:.0f}%</text>"""


def card(r, x, y, w=560, h=152):
    nome = esc(r["name"])
    inicial = nome[0].upper()
    langs = r["_langs"]
    principal = langs[0] if langs else ("-", 0)
    cor = CORES.get(principal[0], "#A855F7")

    linhas_desc = quebrar(r.get("description") or "Sem descricao ainda.", 40, 2)
    desc = "".join(
        f'<text x="{x + 72}" y="{y + 80 + i * 18}" font-family="{MONO}" '
        f'font-size="12" fill="{DIM}">{esc(l)}</text>'
        for i, l in enumerate(linhas_desc)
    )

    # linha compacta de linguagens no rodape do card
    pecas, cursor = [], x + 72
    for nm, pc in langs[:3]:
        rotulo = f"{nm} {pc:.0f}%"
        pecas.append(
            f'<circle cx="{cursor + 4}" cy="{y + 124}" r="4" '
            f'fill="{CORES.get(nm, "#A855F7")}"/>'
            f'<text x="{cursor + 14}" y="{y + 128}" font-family="{MONO}" '
            f'font-size="11" fill="{TEXT}">{esc(rotulo)}</text>'
        )
        cursor += 26 + len(rotulo) * 6.6
    if r["stargazers_count"]:
        pecas.append(
            f'<text x="{cursor + 6}" y="{y + 128}" font-family="{MONO}" '
            f'font-size="11" fill="{ACCENT}">&#9733; {r["stargazers_count"]}</text>'
        )
    legenda = "".join(pecas)

    return f"""
  <g>
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{CARD}"
          stroke="{BORDER}" stroke-width="1" opacity="0.95"/>
    <circle cx="{x + 40}" cy="{y + 44}" r="18" fill="none" stroke="{cor}" stroke-width="1.5"/>
    <text x="{x + 40}" y="{y + 50}" font-family="{MONO}" font-size="16" fill="{cor}"
          text-anchor="middle">{inicial}</text>
    <text x="{x + 72}" y="{y + 42}" font-family="{MONO}" font-size="16"
          fill="{NAME}">{nome}_</text>
    <text x="{x + 72}" y="{y + 58}" font-family="{MONO}" font-size="10"
          fill="{DIM}">{esc(r["full_name"])}</text>
    {desc}
    {legenda}
    {donut(x + w - 52, y + h / 2, principal[1], cor)}
  </g>"""


def montar(repos):
    cols, cw, ch, gap = 2, 560, 152, 20
    linhas = (len(repos) + cols - 1) // cols
    W = 20 + cols * cw + (cols - 1) * gap + 20
    H = 74 + linhas * ch + (linhas - 1) * gap + 24

    cards = "".join(
        card(r, 20 + (i % cols) * (cw + gap), 74 + (i // cols) * (ch + gap))
        for i, r in enumerate(repos)
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Lista de projetos">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <text x="24" y="42" font-family="{MONO}" font-size="14" fill="{ACCENT}"
        letter-spacing="3">PROJECTS.LIST</text>
  <line x1="24" y1="54" x2="{W - 24}" y2="54" stroke="{BORDER}" stroke-width="1" opacity="0.3"/>
  {cards}
</svg>
"""


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--usuario", required=True)
    p.add_argument("--limite", type=int, default=6)
    p.add_argument("--saida", default="projects.svg")
    a = p.parse_args()

    repos = repositorios(a.usuario, a.limite)
    if not repos:
        raise SystemExit("nenhum repositório público encontrado")
    with open(a.saida, "w", encoding="utf-8") as f:
        f.write(montar(repos))
    print(f"gerado: {a.saida} ({len(repos)} projetos)")


if __name__ == "__main__":
    main()
