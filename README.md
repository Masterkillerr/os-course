# Sistemas Operativos — Curso

Course site for Fabián Robles' Sistemas Operativos class, built as a static
site (`index.html`) with lazily-fetched per-page Markdown from `Robles/`.

Run `python3 build.py` after adding/editing a page to regenerate the nav and
`course.json` manifest. Serve locally with `python3 -m http.server` (fetch()
requires HTTP, not `file://`).
