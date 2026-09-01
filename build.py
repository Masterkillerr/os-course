#!/usr/bin/env python3
"""Rebuild the nav sidebar in index.html and course.json from Robles/*.md.

Usage: python3 build.py

To add a class/topic: drop a new Robles/NN-Topic.md file with frontmatter

    ---
    sidebar_title: "🔥 Emoji Title"
    order: 65
    unit: "Unidad 2 — Almacenamiento y Arranque"   # or null/omitted to
                                                    # continue the previous
                                                    # unit
    parent: "NN-Topic"        # (optional) stem of parent page for subpages
    ---

then rerun. Page order is `order` (ascending); a `unit` value starts a new
sidebar section heading — omit it (or set null) to fall under the previous
page's unit. A `parent` value indents the page under its parent in the nav.
Nothing else needs editing: nav, wikimap, and page count all follow from the
vault automatically.

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

# ponytail: hand-picked subset of Lucide icons (MIT), inlined to avoid a JS dep.
# stroke="currentColor" so they inherit sidebar text color automatically.
_ICON_BODIES = {
    "book-marked": '<path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/><path d="M10 2v8l3-3 3 3V2"/>',
    "folder-open": '<path d="m6 14 1.45-2.9A2 2 0 0 1 9.24 10H20a2 2 0 0 1 1.94 2.5l-1.55 6a2 2 0 0 1-1.94 1.5H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h3.9a2 2 0 0 1 1.69.9l.81 1.2a2 2 0 0 0 1.67.9H18a2 2 0 0 1 2 2v2"/>',
    "brain": '<path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/><path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"/><path d="M15 13a4.5 4.5 0 0 1-3-4 4.5 4.5 0 0 1-3 4"/><path d="M17.599 6.5a3 3 0 0 0 .399-1.375"/><path d="M6.003 5.125A3 3 0 0 0 6.401 6.5"/><path d="M3.477 10.896a4 4 0 0 1 .585-.396"/><path d="M19.938 10.5a4 4 0 0 1 .585.396"/><path d="M6 18a4 4 0 0 1-1.967-.516"/><path d="M19.967 17.484A4 4 0 0 1 18 18"/>',
    "calendar-clock": '<path d="M21 7.5V6a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h3.5"/><path d="M16 2v4"/><path d="M8 2v4"/><path d="M3 10h5"/><path d="M17.5 17.5 16 16.25V14"/><circle cx="16" cy="16" r="6"/>',
    "smartphone": '<rect width="14" height="20" x="5" y="2" rx="2" ry="2"/><path d="M12 18h.01"/>',
    "hard-drive": '<line x1="22" x2="2" y1="12" y2="12"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11"/><line x1="6" x2="6.01" y1="16" y2="16"/><line x1="10" x2="10.01" y1="16" y2="16"/>',
    "chart-column": '<path d="M3 3v16a2 2 0 0 0 2 2h16"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/>',
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>',
    "lock": '<rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "terminal": '<path d="m7 11 2-2-2-2"/><path d="M11 13h4"/><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/>',
    "monitor": '<rect width="20" height="14" x="2" y="3" rx="2"/><line x1="8" x2="16" y1="21" y2="21"/><line x1="12" x2="12" y1="17" y2="21"/>',
    "wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94z"/>',
    "library": '<path d="m16 6 4 14"/><path d="M12 6v14"/><path d="M8 8v12"/><path d="M4 4v16"/>',
}
# emoji -> icon name, based on what's actually used in Robles/*.md frontmatter.
_EMOJI_ICON = {
    "🗂️": "book-marked", "📘": "folder-open", "🧠": "brain", "📅": "calendar-clock",
    "🤖": "smartphone", "💾": "hard-drive", "📊": "chart-column", "🛡️": "shield",
    "🔐": "lock", "⌨️": "terminal", "🪟": "monitor", "🛠️": "wrench", "📚": "library",
}
_EMOJI_RE = re.compile("|".join(re.escape(e) for e in _EMOJI_ICON))


def _svg_icon(name: str) -> str:
    return (f'<svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true">{_ICON_BODIES[name]}</svg>')


def emojis_to_svg(text: str) -> str:
    return _EMOJI_RE.sub(lambda m: _svg_icon(_EMOJI_ICON[m.group()]), text).strip()


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
            "parent": fm.get("parent"),
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
    lines = [f'  <div class="brand">{emojis_to_svg("📚 Sistemas Operativos")}</div>']
    n = 0
    last_unit = None
    for p in pages:
        unit = p.get("unit")
        if unit and unit != last_unit:
            lines.append(f"\n  <h2>{unit}</h2>")
            last_unit = unit
        cls = "nav-item nav-item-child" if p.get("parent") else "nav-item"
        indent = '    ' if p.get("parent") else ''
        title = emojis_to_svg(p["title"])
        lines.append(f'  <a class="{cls}" data-page="{n}">{indent}<span class="num">{n:02d}</span> {title}</a>')
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
