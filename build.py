#!/usr/bin/env python3
"""Rebuild OS-course.html from Robles/*.md.

Usage: python3 build.py

To add a class/topic: drop a new Robles/NN-Topic.md file (Obsidian frontmatter
optional, stripped automatically), add its filename + emoji title + unit to
PAGES below, then rerun. Everything else (nav, wikimap, page count) follows.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
VAULT = ROOT / "Robles"
HTML = ROOT / "OS-course.html"

# (filename stem in Robles/, sidebar title, unit heading). Index 0 is always
# the Índice and has no unit heading.
PAGES = [
    ("00-Indice", "🗂️ Índice", None),
    ("07-Introduccion-SO", "📘 Introducción a los S.O.", "Unidad 1 — Fundamentos"),
    ("09-Fundamentos-del-SO", "🧠 Fundamentos del SO", None),
    ("02-Sistemas-de-Archivos", "💾 Sistemas de Archivos", "Unidad 2 — Almacenamiento y Arranque"),
    ("04-Estructuras-de-Datos", "📊 Estructuras de Datos", None),
    ("03-Arranque-y-Seguridad", "🛡️ Arranque y Seguridad", None),
    ("01-TPM", "🔐 TPM", None),
    ("08-Linea-de-Comandos", "⌨️ Línea de comandos", "Unidad 3 — Herramientas"),
    ("05-Historia-Windows", "🪟 Historia de Windows", "Unidad 4 — Contexto de Industria"),
    ("06-Mercado-OS", "📊 Mercado de OS", None),
]

FRONTMATTER_RE = re.compile(r"^---\n.*?\n---\n\s*", re.S)


def strip_frontmatter(md: str) -> str:
    return FRONTMATTER_RE.sub("", md, count=1)


def build_nav(pages):
    lines = ['  <div class="brand">📚 Sistemas Operativos</div>',
             '  <a class="nav-item" data-page="0"><span class="num">00</span> 🗂️ Índice</a>']
    n = 1
    for i, (_, title, unit) in enumerate(pages):
        if i == 0:
            continue
        if unit:
            lines.append(f"\n  <h2>{unit}</h2>")
        lines.append(f'  <a class="nav-item" data-page="{i}"><span class="num">{n:02d}</span> {title}</a>')
        n += 1
    lines.append("\n  <h2>Profesor</h2>")
    return "\n".join(lines)


def build_md_scripts(pages):
    out = []
    for i, (stem, _, _) in enumerate(pages):
        md = strip_frontmatter((VAULT / f"{stem}.md").read_text(encoding="utf-8")).strip()
        out.append(f'<script type="text/markdown" id="md-{i}" data-file="{stem}">\n{md}\n</script>')
    return "\n".join(out)


def main():
    html = HTML.read_text(encoding="utf-8")

    nav_html = f'<nav class="sidebar" id="sidebar">\n{build_nav(PAGES)}\n</nav>'
    html = re.sub(
        r'<nav class="sidebar" id="sidebar">\n.*?\n</nav>',
        lambda _: nav_html,
        html, count=1, flags=re.S,
    )

    md_html = build_md_scripts(PAGES)
    html = re.sub(
        r'<script type="text/markdown" id="md-0".*?</script>(\n<script type="text/markdown".*?</script>)*',
        lambda _: md_html,
        html, count=1, flags=re.S,
    )

    HTML.write_text(html, encoding="utf-8")
    print(f"Rebuilt {HTML.name} from {len(PAGES)} pages in Robles/.")


if __name__ == "__main__":
    main()
