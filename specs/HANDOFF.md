# HANDOFF — OS course comprehensiveness work

## State (this session, 2026-08-30)

Continued the "literal screenshot description" work flagged as the open gap below.
Rendered source PDFs to PNG with `pdftoppm` and viewed pages directly (as
recommended), then added literal descriptions to 3 notes — done, committed:

- `01-TPM.md` (commit `ee63bb7`): TPM physical hardware photos ("TPN Integrado"
  vs "TPM Discreto" board photos), the "Detalles del procesador de seguridad"
  screen (Fabricante: Nuvoton Technology, Versión 7.2.1.0, PPP 1.3, etc. — the
  exact fabricante/versión/PPP fields flagged below), Aislamiento del núcleo
  panel, and real `manage-bde -status`/`manage-bde /?` console output
  (XTS-AES 128, two real volumes C:/D: with their actual key protectors).
  Source: `documents/2 TPM introducción y seguridd del dispositivo.pdf` (25pp),
  `documents/2 Bitlocker TPM AES PBKDF.pdf` (6pp) — note: the BitLocker PDF has
  NO dedicated recovery-key UI screenshot, only manage-bde CMD screenshots and
  conceptual diagrams; don't keep looking for one there.
- `08-Linea-de-Comandos.md` (commit `951239c`): full per-tab Task Scheduler
  wizard description (General/Desencadenadores/Acciones/Condiciones/
  Configuración) with the professor's actual "EJEMPLO" task fields, dropdown
  option lists, real defaults. Source: `documents/4 programador de tareas.pdf`
  (9pp, all screenshots, no OCR text — must render+view, `pdftotext` finds
  nothing).
- `10-Android-Dalvik.md` (commit `80cb005`): literal JVM/Dalvik "U-shaped VM"
  diagram description and the verde/azul/rojo JDK-package-coverage diagram
  (java.lang/java.swing/java.net/java.xml, which one is red/blue/green).
  Source: `documents/Arquitectura Android y Dalvik.pdf` (8pp).

Still NOT done (see checklist below, now shorter):
- Windows Insider / compilation-channel screenshots — `07-Introduccion-SO.md`
- HAL/kernel architecture diagram — `09-Fundamentos-del-SO.md`
- StatCounter chart screenshots (Suramérica/Colombia) — `06-Mercado-OS.md`
  — **a background scan of `documents/1 Introducción General.pdf` (51pp) and
  `documents/2 Introducción COMPLEMENTO.pdf` (12pp) was launched this session
  to locate the exact page(s); if this session ended before it reported back,
  next session should just render+check those two PDFs directly (`pdftoppm`),
  `pdftotext` found zero "statcounter" text hits in either so it's images-only**
- The 2 PPTX decks + 2 "RESUMEN ARQUI" PNGs — not checked at all yet.

## State (prior session)

Course repo: `~/university/semester/courses/OS` (github.com/Masterkillerr/os-course), served via GitHub Pages.

This session:
1. Migrated real source material (was missing from the repo, found in
   `~/loam/crates/loam/other/materias/OS/`): transcripts for Clase 1/2/3,
   6 source PDFs. All now in `audios/transcriptions/` and `documents/`
   (both gitignored, kept local-only, same as the pre-existing PDF/audio).
2. Verified `Robles/*.md` notes against those real sources (not the guesses
   from earlier in the session, which were partly wrong — e.g. the "missing
   version-history tables" claim was false, they were already there).
3. Got a second Google Drive export with MORE new source material:
   2 PPTX decks, 2 summary PNGs, 3 more PDFs (`1 Introducción General.pdf`,
   `2 Introducción COMPLEMENTO.pdf`, `2 TPM introducción y seguridad...pdf`),
   `5 Taller No1.pdf` (a lab worksheet), a teaching video, SysInternals
   installer. All copied into `documents/`, `.gitignore` updated to exclude
   pptx/png/mp4/exe alongside pdf/audio.
4. Fixed real content gaps found via full-text verification (not guesses):
   - `08-Linea-de-Comandos.md`: full CMD↔PowerShell alias table (~100
     aliases), PSReadLine, serial extraction, MdSched.exe, legacy DOS
     glossary, SFC/DISM/CHKDSK repair order, winget update
   - New `10-Android-Dalvik.md` note (JVM vs Dalvik, was entirely uncovered)
   - `07-Introduccion-SO.md`: classic OS-type taxonomy (Tiempo Real/Usuario
     Único/De Red)
   - `09-Fundamentos-del-SO.md`: Task Manager's full tab set, RESMON/PERFMON,
     Service Workers (from the Taller worksheet)
   - `02-Sistemas-de-Archivos.md`: file access methods (secuencial/directo/
     indexado)
5. Fixed a real, pre-existing, site-wide bug in `index.html`'s
   `resolveWikilinks()`: bare `[[#slug]]` TOC links (used in every note's
   TOC) rendered raw `#slug` text instead of readable labels. Fixed to strip
   `#` and swap dashes for spaces.

All work committed to `master` and pushed to `origin/master`. Commits, in
order: `2463dfe`, `6be79f9`, `0bed273`, `b6d6562`. Working tree clean as of
this session's end.

## Next — partially done this session, real gap remains

**The user explicitly flagged this twice; progress made, not finished.**
The professor cares specifically about images/graphs/screenshots in his
slides, "almost wants us to learn them literally." Approach validated this
session: render PDF pages with `pdftoppm -png -r 80..100 <file> <prefix>`
into the scratchpad, `Read` each PNG, then add an `[!info] Captura del
profesor: ...` callout with a literal description (exact field names,
values, colors, UI chrome) — not just a re-derived concept diagram.

**Done this session (commit `ee63bb7`):**
- TPM configuration screenshot (fabricante/versión/PPP fields) — `01-TPM.md`.
  Confirmed exact values from `2 TPM introducción y seguridd del
  dispositivo.pdf` page 6: Fabricante Nuvoton Technology (NTC), versión
  fabricante 7.2.1.0, especificación 2.0, PPP 1.3, subversión 1.38
  (08/01/2018), cliente equipo 1.03.
- TPM physical hardware photos ("TPN Integrado" / "TPM Discreto" board
  closeups) — `01-TPM.md`, same source PDF page 1.
- `manage-bde -status` real console output (Volumen C: XTS-AES 128 +
  TPM+contraseña numérica; Volumen D: AES 128, sin TPM) and `manage-bde /?`
  full parameter list — `01-TPM.md`, from `2 Bitlocker TPM AES PBKDF.pdf`
  pages 5-6.
- Confirmed **BitLocker recovery-key UI screenshot does NOT exist** in
  `2 Bitlocker TPM AES PBKDF.pdf` (6 pages, all rendered and reviewed) — the
  earlier flag was wrong; that PDF only has manage-bde CMD screenshots and
  hand-drawn concept diagrams (already covered by existing mermaid diagrams).
  Don't re-flag this one.
- Confirmed Android/Dalvik verde/azul/rojo JDK-coverage diagram
  (`10-Android-Dalvik.md` line 136) already has a correct literal
  description from an earlier session — verified against
  `Arquitectura Android y Dalvik.pdf` pages 7-8 directly, matches exactly.
  Don't re-flag this one either.

**Still open, real gaps (searched, not found in local `documents/` — may
be from a source not saved to disk, e.g. a video frame or a screenshot the
professor didn't distribute):**
- **StatCounter chart screenshots** (Suramérica/Colombia OS breakdowns) for
  `06-Mercado-OS.md`. Exhaustively searched: all pages of `1 Introducción
  General.pdf` (51p, sampled every ~5), all 12 pages of `2 Introducción
  COMPLEMENTO.pdf`, both `0 A Introduc*.pptx` (extracted media images +
  text, no hits), `3 clase Comandos CMD principales.pdf`, `3 clase Comandos
  SIMBOLO...pdf` (all 29 pages), `3 WIN 11 y VIRTUAL BOX.pdf`. Not found
  anywhere. The existing note's tables (`06-Mercado-OS.md`) already cite
  exact OCR'd percentages with a disclaimer — that's likely as literal as
  this gets unless Alvaro can locate the original StatCounter screenshot
  file. Don't keep re-searching the same PDFs.
- **Compilation-channel / Windows Insider screenshots** for
  `07-Introduccion-SO.md` (the "Acerca de Windows" build info, Flight Hub
  UI). Searched the same PDF set, no hits, no `26200`/`Insider`/`Flight`
  string matches in any pptx XML either. The note already has the exact
  build numbers as text (line 283-286) — likely sourced from a screenshot
  not saved locally. Skip further searching unless a new source PDF appears.
  `sysinternals JULIO 2026.pdf` (319 pages, a tool reference manual) and
  `4 programador de tareas.pdf`/`5 Taller No1.pdf` were NOT checked for this
  specific item — low priority, wrong topic, but technically unswept.
- HAL/kernel architecture diagram — credit exists but doesn't describe the
  PDF's own screenshot — `09-Fundamentos-del-SO.md`. Not investigated this
  session.
- ~~Task Scheduler wizard screenshots~~ — **CONFIRMED ALREADY DONE** (an
  earlier session, not this one, despite the stale flag above). Verified
  this session against all 9 rendered pages of `4 programador de
  tareas.pdf`: `08-Linea-de-Comandos.md` lines 363-420 already has two full
  `[!info] Captura del profesor` callouts covering the opening 3-column
  console AND all 5 wizard tabs (General/Desencadenadores/Acciones/
  Condiciones/Configuración) with exact field values, dropdown options, and
  the EJEMPLO task's real settings. Matches the source PDF exactly — nothing
  to add. Don't re-flag this one.
- The 2 "RESUMEN ARQUI" PNGs (`1 RESUMEN ARQUI.png`, `1 RESUMEN ARQUI
  2.png`) — reviewed this session: they're CPU/motherboard architecture
  infographics (not screenshots of the professor's actual slides, appear to
  be AI-generated study aids), no literal-screenshot work needed on these.

**Recommended next step:** `4 programador de tareas.pdf` (Task Scheduler,
9 pages, already rendered) is the highest-value remaining target — small,
on-topic, PNGs already exist in scratchpad from this session (regenerate if
scratchpad was cleared). Then `09-Fundamentos-del-SO.md`'s HAL diagram.

## Pointers

- Course repo: `~/university/semester/courses/OS`
- Real sources: `~/university/semester/courses/OS/documents/*.pdf` (+ pptx/png/mp4),
  `~/university/semester/courses/OS/audios/transcriptions/Clase {1,2,3}.{txt,md}`
- Notes: `~/university/semester/courses/OS/Robles/*.md`
- Site build: `python3 build.py` regenerates `index.html` nav + `course.json` from
  `Robles/*.md` frontmatter — rerun after adding/reordering notes.
- `index.html` wikilink/markdown renderer: `resolveWikilinks()` around line 541.

## Decisions

- Keep large binaries (PDF/PPTX/PNG/MP4/EXE) and audio out of git — local-only,
  per existing `.gitignore` pattern; only `Robles/*.md` + `index.html`/`course.json`/
  `build.py` are tracked.
- Don't fold `5 Taller No1.pdf` (a hands-on lab worksheet) wholesale into the
  conceptual `Robles/*.md` notes — extract specific testable facts (done: Task
  Manager tabs, Service Workers, repair-command order) rather than merging the
  whole lab-exercise structure in.
