# Sistemas Operativos — Curso

Course site for Fabián Robles' Sistemas Operativos class, built as a static
site (`index.html`) with lazily-fetched per-page Markdown from `Robles/`.

## Adding a class

Drop a new `Robles/NN-Topic.md` with frontmatter:

```yaml
---
sidebar_title: "🔥 Emoji Title"
order: 65
unit: "Unidad 2 — Almacenamiento y Arranque"   # omit/null to continue the previous unit
---
```

Then run `python3 build.py` to regenerate the sidebar nav in `index.html`
and `course.json`. Nothing else needs editing — order, nav, and wikimap all
follow from the vault.

Serve locally with `python3 -m http.server` (fetch() requires HTTP, not
`file://`).
