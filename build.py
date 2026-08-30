#!/usr/bin/env python3
"""Rebuild the nav sidebar in index.html and course.json from Robles/*.md.

Usage: python3 build.py

To add a class/topic: drop a new Robles/NN-Topic.md file with frontmatter

    ---
    sidebar_title: "🔥 Emoji Title"
    order: 65
    unit: "Unidad 2 — Almacenamiento y Arranque"   # or null/omitted to
                                                    # continue the previous unit
    ---

then rerun. Page order is `order` (ascending); a `unit` value starts a new
sidebar section heading — omit it (or set null) to fall under the previous
page's unit. Nothing else needs editing: nav, wikimap, and page count all
follow from the vault automatically.

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

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)
FIELD_RE = re.compile(r'^(\w+):\s*(.*)$', re.M)


def parse_frontmatter(md: str) -> dict:
    m = FRONTMATTER_RE.match(md)
    if not m:
        return {}
    fields = {}
    for key, raw in FIELD_RE.findall(m.group(1)):
        raw = raw.strip()
        if raw.startswith('"') and raw.endswith('"'):
            raw = raw[1:-1]
        elif raw == "null" or raw == "":
            raw = None
        fields[key] = raw
    return fields


def load_pages():
    """Scan Robles/*.md for frontmatter, sort by `order`. Files without an
    `order` field (e.g. Obsidian's default Bienvenido.md) are skipped."""
    pages = []
    for path in VAULT.glob("*.md"):
        fm = parse_frontmatter(path.read_text(encoding="utf-8"))
        if "order" not in fm or fm["order"] is None:
            continue
        title = fm.get("sidebar_title") or fm.get("title") or path.stem
        pages.append({
            "stem": path.stem,
            "title": title,
            "unit": fm.get("unit"),
            "order": float(fm["order"]),
        })
    pages.sort(key=lambda p: p["order"])
    for p in pages:
        del p["order"]
    return pages


def slug_key(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def build_nav(pages):
    lines = ['  <div class="brand">📚 Sistemas Operativos</div>']
    n = 0
    for p in pages:
        if p["unit"]:
            lines.append(f"\n  <h2>{p['unit']}</h2>")
        lines.append(f'  <a class="nav-item" data-page="{n}"><span class="num">{n:02d}</span> {p["title"]}</a>')
        n += 1
    lines.append("\n  <h2>Profesor</h2>")
    return "\n".join(lines)


def build_manifest(pages):
    wikimap = {}
    for i, p in enumerate(pages):
        clean_title = re.sub(r"^\s*\d+\s*", "", p["title"]).strip()
        for key in (clean_title, clean_title.replace(" ", "-"), slug_key(clean_title), p["stem"]):
            if key:
                wikimap[key] = i
    return {"pages": pages, "wikimap": wikimap}


def main():
    pages = load_pages()
    if not pages:
        raise SystemExit("No pages found in Robles/ with an `order` frontmatter field.")

    html = HTML.read_text(encoding="utf-8")
    nav_html = f'<nav class="sidebar" id="sidebar">\n{build_nav(pages)}\n</nav>'
    html = re.sub(
        r'<nav class="sidebar" id="sidebar">\n.*?\n</nav>',
        lambda _: nav_html,
        html, count=1, flags=re.S,
    )
    HTML.write_text(html, encoding="utf-8")

    manifest = build_manifest(pages)
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Rebuilt nav in {HTML.name} and {MANIFEST.name} from {len(pages)} pages in Robles/.")


if __name__ == "__main__":
    main()
