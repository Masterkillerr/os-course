#!/usr/bin/env python3
"""Split long pages into focused subpages with proper parent/child hierarchy."""
import re
from pathlib import Path

VAULT = Path(__file__).parent / "Robles"

SPLITS = [
    ("09b-Procesos-Memoria-Kernel", [
        ("09b-Procesos", "🧠 Procesos y Threads", "## Procesos y Threads", "## Gestión de memoria"),
        ("09c-Memoria-y-Sincronizacion", "🧠 Memoria, E/S y Sincronización", "## Gestión de memoria", "## Virtualización"),
        ("09d-Virtualizacion-Kernel", "🧠 Virtualización, Kernel y Conceptos", "## Virtualización", None),
    ]),
    ("02-Sistemas-de-Archivos", [
        ("02a-FAT", "💾 FAT — File Allocation Table", "## FAT = File Allocation Table", "## NTFS = New Technology File System"),
        ("02b-NTFS", "💾 NTFS — New Technology File System", "## NTFS = New Technology File System", "## ReFS = Resilient File System"),
        ("02c-ReFS-y-atributos", "💾 ReFS, Atributos y Conceptos", "## ReFS = Resilient File System", None),
    ]),
    ("08-Linea-de-Comandos", [
        ("08a-CMD", "⌨️ CMD — Comandos esenciales", "## CMD — Comandos esenciales", "## PowerShell — cmdlets y ejemplos"),
        ("08b-PowerShell", "⌨️ PowerShell — cmdlets y ejemplos", "## PowerShell — cmdlets y ejemplos", None),
    ]),
]

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)


def read_file(path):
    return path.read_text(encoding="utf-8")


def extract_section(content, start_marker, end_marker):
    lines = content.split('\n')
    start_idx = None
    end_idx = None
    for i, line in enumerate(lines):
        if line.strip() == start_marker.strip() and start_idx is None:
            start_idx = i
        if end_marker and line.strip() == end_marker.strip() and start_idx is not None:
            end_idx = i
            break
    if start_idx is None:
        return None
    if end_idx is None:
        end_idx = len(lines)
    return '\n'.join(lines[start_idx:end_idx])


def modify_fm(fm_text, child_stem, child_title, child_order, parent_stem):
    """Modify frontmatter: change title, sidebar_title, order, and add parent."""
    subtitle = get_subtitle(child_title)

    # Replace title
    fm_text = re.sub(r'^title:\s*".*"', f'title: "{child_title}"', fm_text, flags=re.M)
    # Replace sidebar_title
    fm_text = re.sub(r'^sidebar_title:\s*".*"', f'sidebar_title: "{subtitle}"', fm_text, flags=re.M)
    # Replace order
    fm_text = re.sub(r'^order:\s*\S+', f'order: {child_order}', fm_text, flags=re.M)
    # Replace tema
    fm_text = re.sub(r'^tema:\s*".*"', f'tema: "{subtitle}"', fm_text, flags=re.M)
    # Add parent field after tiempo_clase or at end
    if re.search(r'^parent:\s*', fm_text, re.M):
        fm_text = re.sub(r'^parent:\s*\S+', f'parent: {parent_stem}', fm_text, flags=re.M)
    else:
        # Add parent before prev
        fm_text = re.sub(r'^(prev:\s*\S+)', f'parent: {parent_stem}\n\\1', fm_text, flags=re.M)

    # Reset prev/next to null (will be fixed later)
    fm_text = re.sub(r'^prev:\s*\S+', 'prev: null', fm_text, flags=re.M)
    fm_text = re.sub(r'^next:\s*\S+', 'next: null', fm_text, flags=re.M)

    return fm_text


def build_child_header(parent_fm_text, child_title, parent_stem):
    """Extract title from frontmatter and build module header."""
    title_match = re.search(r'^title:\s*"(.*?)"', parent_fm_text, re.M)
    parent_title = title_match.group(1) if title_match else "Page"
    tema_match = re.search(r'^tema:\s*"(.*?)"', parent_fm_text, re.M)
    tema = tema_match.group(1) if tema_match else "Temas varios"

    # Extract a clean subtitle: strip emoji prefix, split on — or take first words
    clean_title = re.sub(r'^[^\w]+', '', child_title).strip()  # strip emoji
    if '—' in clean_title:
        subtitle = clean_title.split('—', 1)[-1].strip()
    else:
        subtitle = clean_title

    return (
        f"# {child_title}\n"
        f"\n"
        f"> [!info] Módulo\n"
        f"> **Clase 2** — {tema}\n"
        f"> **Tema:** {child_title}\n"
        f"> **Ver también:** [[{parent_stem}|{parent_title}]]\n"
        f"\n"
        f"> [!tip] Prerrequisitos\n"
        f"> - Conceptos básicos de sistemas operativos\n"
        f"> - [[{parent_stem}|{parent_title}]] — visión general\n"
        f"\n"
        f"---\n"
        f"\n"
        f"> [!info] Anterior\n"
        f"> [[{parent_stem}|{parent_title}]] — visión general\n"
        f"\n"
    )


def get_subtitle(child_title):
    """Extract a clean subtitle from a child title."""
    clean_title = re.sub(r'^[^\w]+', '', child_title).strip()
    if '—' in clean_title:
        return clean_title.split('—', 1)[-1].strip()
    return clean_title


def main():
    for parent_stem, children in SPLITS:
        parent_path = VAULT / f"{parent_stem}.md"
        if not parent_path.exists():
            print(f"  SKIP {parent_stem} — not found")
            continue

        content = read_file(parent_path)
        fm_match = FRONTMATTER_RE.match(content)
        if not fm_match:
            print(f"  WARN {parent_stem} — no frontmatter")
            continue

        base_order = int(re.search(r'^order:\s*(\d+)', fm_match.group(1), re.M).group(1))
        parent_fm_text = fm_match.group(1)
        content_after_fm = content[fm_match.end():]

        # Extract each child section and create the file
        for idx, (child_stem, child_title, start_marker, end_marker) in enumerate(children):
            section = extract_section(content_after_fm, start_marker, end_marker)
            if section is None:
                print(f"  WARN {child_stem} — section {start_marker} not found")
                continue

            child_order = base_order + idx + 1
            child_fm = modify_fm(parent_fm_text, child_stem, child_title, child_order, parent_stem)
            child_header = build_child_header(parent_fm_text, child_title, parent_stem)

            # Remove the ## heading from section content since it's now the title
            lines = section.split('\n')
            while lines and lines[0].startswith('## '):
                lines = lines[1:]
            body = '\n'.join(lines).lstrip('\n')

            child_file = f"---\n{child_fm}\n---\n\n" + child_header + body + '\n'
            out_path = VAULT / f"{child_stem}.md"
            out_path.write_text(child_file, encoding="utf-8")
            print(f"  CREATED {child_stem}.md (order={child_order})")

        # Update parent: keep content before first child section, add child links
        lines = content_after_fm.split('\n')
        first_child_start = None
        for i, line in enumerate(lines):
            for _, _, start_marker, _ in children:
                if line.strip() == start_marker.strip():
                    if first_child_start is None:
                        first_child_start = i
                    break

        if first_child_start is None:
            print(f"  WARN {parent_stem} — no child sections found")
            continue

        parent_lines = lines[:first_child_start]
        while parent_lines and parent_lines[-1].strip() == '':
            parent_lines.pop()

        parent_lines.append('')
        parent_lines.append('---')
        parent_lines.append('')
        parent_lines.append('> [!info] Temas relacionados')
        for stem, title, _, _ in children:
            parent_lines.append(f'- [[{stem}|{title}]]')
        parent_lines.append('')

        new_content = '\n'.join(parent_lines) + '\n'
        new_parent_file = content[:fm_match.end()] + new_content
        parent_path.write_text(new_parent_file, encoding="utf-8")
        print(f"  UPDATED {parent_stem}.md")

    # Fix prev/next links for ALL pages based on order
    print("\n--- Fixing prev/next ---")
    all_pages = []
    for f in sorted(VAULT.glob('*.md')):
        content = read_file(f)
        m = FRONTMATTER_RE.match(content)
        if m:
            fm_text = m.group(1)
            order_match = re.search(r'^order:\s*(\d+)', fm_text, re.M)
            if order_match:
                order = int(order_match.group(1))
                all_pages.append((f.stem, order))
    all_pages.sort(key=lambda x: x[1])

    for i, (stem, order) in enumerate(all_pages):
        path = VAULT / f"{stem}.md"
        content = read_file(path)
        m = FRONTMATTER_RE.match(content)
        fm_text = m.group(1)
        prev_stem = all_pages[i - 1][0] if i > 0 else 'null'
        next_stem = all_pages[i + 1][0] if i < len(all_pages) - 1 else 'null'

        fm_text = re.sub(r'^prev:\s*\S+', f'prev: {prev_stem}', fm_text, flags=re.M)
        fm_text = re.sub(r'^next:\s*\S+', f'next: {next_stem}', fm_text, flags=re.M)

        new_file = f'---\n{fm_text}\n---\n' + content[m.end():]
        path.write_text(new_file, encoding="utf-8")
        print(f"  {stem}: prev={prev_stem}, next={next_stem}")


if __name__ == "__main__":
    main()
