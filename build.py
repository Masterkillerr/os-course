#!/usr/bin/env python3
"""Rebuild the nav sidebar in index.html and course.json from Robles/*.md.

Usage: python3 build.py

To add a class/topic: drop a new Robles/NN-Topic.md file (Obsidian frontmatter
optional, stripped client-side), add its filename + emoji title + unit to
PAGES below, then rerun. Everything else (nav, wikimap, page count) follows.

Page markdown itself is NOT embedded into index.html — the browser fetches
Robles/<stem>.md lazily per page (see index.html's loadPage()). This script
only needs to update the sidebar links and the course.json manifest that
supplies titles/wikimap to the client.
"""
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).parent
VAULT = ROOT / "Robles"
HTML = ROOT / "index.html"
MANIFEST = ROOT / "course.json"

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


def slug_key(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


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


def build_manifest(pages):
    entries = []
    wikimap = {}
    for i, (stem, title, unit) in enumerate(pages):
        clean_title = re.sub(r"^\s*\d+\s*", "", title).strip()
        entries.append({"stem": stem, "title": clean_title, "unit": unit})
        for key in (clean_title, clean_title.replace(" ", "-"), slug_key(clean_title), stem):
            if key:
                wikimap[key] = i
    return {"pages": entries, "wikimap": wikimap}


def main():
    html = HTML.read_text(encoding="utf-8")

    nav_html = f'<nav class="sidebar" id="sidebar">\n{build_nav(PAGES)}\n</nav>'
    html = re.sub(
        r'<nav class="sidebar" id="sidebar">\n.*?\n</nav>',
        lambda _: nav_html,
        html, count=1, flags=re.S,
    )
    HTML.write_text(html, encoding="utf-8")

    manifest = build_manifest(PAGES)
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for stem, _, _ in PAGES:
        if not (VAULT / f"{stem}.md").exists():
            print(f"warning: {stem}.md not found in Robles/")

    print(f"Rebuilt nav in {HTML.name} and {MANIFEST.name} from {len(PAGES)} pages.")


if __name__ == "__main__":
    main()
