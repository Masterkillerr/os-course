#!/usr/bin/env python3
"""Update order, prev, next fields in all course pages."""
import re
from pathlib import Path

ROOT = Path(__file__).parent
VAULT = ROOT / "Robles"

# Define the new sequential order and prev/next chain.
# This is the nav order (top to bottom).
SEQUENCE = [
    {"stem": "00-Indice",             "order": 0,   "prev": None,                              "next": "07-Introduccion-SO"},
    {"stem": "07-Introduccion-SO",    "order": 10,  "prev": "00-Indice",                        "next": "09-Fundamentos-del-SO"},
    {"stem": "09-Fundamentos-del-SO", "order": 20,  "prev": "07-Introduccion-SO",               "next": "09b-Procesos-Memoria-Kernel"},
    {"stem": "09b-Procesos-Memoria-Kernel", "order": 30, "prev": "09-Fundamentos-del-SO",       "next": "11-Planificacion-Procesos"},
    {"stem": "11-Planificacion-Procesos", "order": 40, "prev": "09b-Procesos-Memoria-Kernel",   "next": "10-Android-Dalvik"},
    {"stem": "10-Android-Dalvik",     "order": 50,  "prev": "11-Planificacion-Procesos",        "next": "02-Sistemas-de-Archivos"},
    {"stem": "02-Sistemas-de-Archivos", "order": 60, "prev": "10-Android-Dalvik",               "next": "04-Estructuras-de-Datos"},
    {"stem": "04-Estructuras-de-Datos", "order": 70, "prev": "02-Sistemas-de-Archivos",         "next": "03-Arranque-y-Seguridad"},
    {"stem": "03-Arranque-y-Seguridad", "order": 80, "prev": "04-Estructuras-de-Datos",         "next": "01-TPM"},
    {"stem": "01-TPM",                "order": 90,  "prev": "03-Arranque-y-Seguridad",          "next": "08-Linea-de-Comandos"},
    {"stem": "08-Linea-de-Comandos",  "order": 100, "prev": "01-TPM",                           "next": "05-Historia-Windows"},
    {"stem": "05-Historia-Windows",   "order": 110, "prev": "08-Linea-de-Comandos",             "next": "06-Mercado-OS"},
    {"stem": "06-Mercado-OS",         "order": 120, "prev": "05-Historia-Windows",              "next": None},
]

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)


def update_page(stem, order, prev, next_):
    path = VAULT / f"{stem}.md"
    if not path.exists():
        print(f"  SKIP {stem}.md — not found")
        return False

    content = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(content)
    if not m:
        print(f"  SKIP {stem}.md — no frontmatter")
        return False

    fm_text = m.group(1)

    # Update or add order
    if re.search(r'^order:\s*', fm_text, re.M):
        fm_text = re.sub(r'^order:\s*\S+', f'order: {order}', fm_text, flags=re.M)
    else:
        fm_text = f'order: {order}\n{fm_text}'

    # Update or add prev
    if re.search(r'^prev:\s*', fm_text, re.M):
        fm_text = re.sub(r'^prev:\s*\S+', f'prev: {prev}', fm_text, flags=re.M)
    else:
        fm_text = f'prev: {prev}\n{fm_text}'

    # Update or add next
    if re.search(r'^next:\s*', fm_text, re.M):
        fm_text = re.sub(r'^next:\s*\S+', f'next: {next_}', fm_text, flags=re.M)
    else:
        fm_text = f'next: {next_}\n{fm_text}'

    new_content = f"---\n{fm_text}\n---\n" + content[m.end():]
    path.write_text(new_content, encoding="utf-8")
    print(f"  OK {stem}.md → order={order}, prev={prev}, next={next_}")
    return True


def main():
    for item in SEQUENCE:
        update_page(item["stem"], item["order"], item["prev"], item["next"])


if __name__ == "__main__":
    main()
