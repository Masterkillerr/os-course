---
title: "💾 Windows por Versión y Estructuras de Datos"
sidebar_title: "💾 Windows y Estructuras"
order: 32
unit: null
clase: 2
tema: "Windows por versión y estructuras de datos aplicadas"
profesor: "Fabián Robles"
tags: [windows-versiones, sistemas-archivos, estructuras-datos, clase-2]
prerequisitos: ["Conceptos de sistemas de archivos"]
tiempo_clase: null
---

# 💾 Windows por Versión y Estructuras de Datos

> [!info] Módulo
> **Unidad 2 — Almacenamiento y Arranque**
> **Tema:** Windows por versión y estructuras de datos aplicadas
> **Ver también:** [[02-Sistemas-de-Archivos|💾 Sistemas de archivos]]

---

## Sistemas de archivos según la versión de Windows

> [!info] Desde la Introducción (Clase 1)
> La evolución de los sistemas de archivos refleja la evolución de Windows. Las tablas siguientes
> mapean cada versión con los sistemas de archivos que soporta y el predeterminado/recomendado.

### Escritorio (Desktop)

| Versión de Windows | Año | Sistemas de archivos soportados | Predeterminado / recomendado |
|--------------------|-----|--------------------------------|------------------------------|
| Windows 1.0 | 1985 | FAT12 | FAT12 |
| Windows 2.0 | 1987 | FAT12 | FAT12 |
| Windows 3.0 | 1990 | FAT12, FAT16 | FAT16 |
| Windows 3.1 | 1992 | FAT16 | FAT16 |
| Windows 95 | 1995 | FAT16 | FAT16 |
| Windows 95 OSR2 | 1996 | FAT16, FAT32 | FAT32 |
| Windows 98 | 1998 | FAT16, FAT32 | FAT32 |
| Windows ME | 2000 | FAT16, FAT32 | FAT32 |
| Windows NT 3.1 | 1993 | FAT16, NTFS 1.0 | NTFS |
| Windows NT 4.0 | 1996 | FAT16, FAT32, NTFS | NTFS |
| Windows 2000 | 2000 | FAT16, FAT32, NTFS 3.0 | NTFS |
| Windows XP | 2001 | FAT16, FAT32, NTFS 3.1 | NTFS |
| Windows Vista | 2007 | FAT16, FAT32, NTFS, exFAT | NTFS |
| Windows 7 | 2009 | FAT16, FAT32, NTFS, exFAT | NTFS |
| Windows 8 | 2012 | FAT16, FAT32, NTFS, exFAT, ReFS | NTFS |
| Windows 8.1 | 2013 | FAT16, FAT32, NTFS, exFAT, ReFS | NTFS |
| Windows 10 | 2015 | FAT16, FAT32, NTFS, exFAT, ReFS | NTFS |
| Windows 11 | 2021 | FAT16, FAT32, NTFS, exFAT, ReFS (ReFS en ediciones/escenarios concretos) | NTFS |

### Servidor (Windows Server)

| Versión de Windows Server | Año | Sistemas de archivos soportados | Recomendado |
|---------------------------|-----|--------------------------------|-------------|
| Windows NT Server 3.1 | 1993 | FAT16, NTFS 1.0 | NTFS |
| Windows NT Server 3.5 | 1994 | FAT16, NTFS | NTFS |
| Windows NT Server 3.51 | 1995 | FAT16, NTFS | NTFS |
| Windows NT Server 4.0 | 1996 | FAT16, FAT32, NTFS | NTFS |
| Windows 2000 Server | 2000 | FAT16, FAT32, NTFS 3.0 | NTFS |
| Windows Server 2003 | 2003 | FAT16, FAT32, NTFS 3.1 | NTFS |
| Windows Server 2008 | 2008 | FAT16, FAT32, NTFS, exFAT | NTFS |
| Windows Server 2008 R2 | 2009 | FAT16, FAT32, NTFS, exFAT | NTFS |
| Windows Server 2012 | 2012 | FAT16, FAT32, NTFS, exFAT, ReFS | NTFS / ReFS |
| Windows Server 2012 R2 | 2013 | NTFS, exFAT, ReFS | NTFS / ReFS |
| Windows Server 2016 | 2016 | NTFS, exFAT, ReFS | NTFS / ReFS |
| Windows Server 2019 | 2018 | NTFS, exFAT, ReFS | NTFS / ReFS |
| Windows Server 2022 | 2021 | NTFS, exFAT, ReFS | NTFS / ReFS |
| Windows Server 2025 | 2024 | NTFS, exFAT, ReFS | NTFS / ReFS |

> [!note] Observación
> NTFS se consolidó como predeterminado desde Windows NT. **ReFS** aparece desde Windows 8/Server
> 2012 orientado a servidores y virtualización; en escritorio Windows 11 solo está disponible en
> ediciones y escenarios concretos.

---

## Límites de nombre y longitud de ruta

> [!info] Del laboratorio (Clase 3)
> Hay dos límites relacionados: el **nombre del archivo** y la **longitud total de la ruta**.

| Límite | FAT (8.3) | FAT16/FAT32 | NTFS |
|--------|-----------|-------------|------|
| Nombre | 8 caracteres + extensión 3 | Hasta 255 (pero la ruta cuenta) | Hasta 255 (pero la ruta cuenta) |
| Ruta completa | — | 260 (predeterminado) | 260 (predeterminado) |
| Ruta larga | — | — | Hasta 32.767 (32 k) vía directiva |

> [!example] El problema del gerente
> La ruta completa `C:\Users\MIFA\Documentos\...` **cuenta** para los 255 caracteres, no solo el nombre. Por eso un archivo "Junta directiva primer semestre 2016 informe final revisado por junta fiscal…" no cabe: la ruta supera el límite. Se resuelve **acortando** el nombre. En NTFS también se puede ampliar el límite a **32.767** habilitando *"Long Paths"* en Directivas de grupo o el Registro (ver [[03-Arranque-y-Seguridad|🛡️ Arranque y seguridad]]).

> [!warning] Errores comunes
> No todo lo que "cabe" en 255 es ruta válida: el Windows antiguo se niega por la longitud total. El 8.3 (`ARCHIV~1`) es el formato heredado de FAT que aún NTFS genera por compatibilidad.

## Sistemas de archivos vs. Estructuras de datos

| Sistema de archivos | Estructura de datos | Aplicación |
|---------------------|---------------------|-------------|
| FAT16/32 | Array indexado | Tabla de asignación |
| NTFS (MFT) | Árbol B+ | Búsqueda eficiente de archivos |
| exFAT | Array + clusters | Tabla simplificada |
| Directorios | Árboles jerárquicos | Rutas de carpetas |
| Asignación de clusters | Listas enlazadas | Encadenamiento de bloques |

Ver detalles en [[04-Estructuras-de-Datos|📊 Estructuras de datos]].

---

## 📝 Autoevaluación

<details>
<summary>📦 Abrir preguntas y respuestas</summary>

### Pregunta 1 — 500 GB vs 465 GiB
¿Por qué 500 GB no son 500 GB en Windows?

```
SOCIEDAD (Base 10)          SISTEMA OPERATIVO (Base 2)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  1 GB = 1,000,000,000 bytes    1 GiB = 1,073,741,824 bytes
     (10⁹)                           (2³⁰)
```

> **Respuesta:** La sociedad usa base 10 (1 GB = 10⁹ bytes) pero el SO usa base 2 (1 GiB = 2³⁰ bytes). Por eso 500 GB ≈ 465 GiB.

---

### Pregunta 2 — Fragmentación interna
¿Qué es la fragmentación interna y cómo se mitiga?

```
CLUSTER DE 32 KB
┌──────────────────────────────┐
│ A (1 byte)                   │
├──────────────────────────────┤
│ 31,999 bytes VACÍOS          │
│ ← FRAGMENTACIÓN INTERNA      │
└──────────────────────────────┘
```

> **Respuesta:** Es el espacio desperdiciado **dentro** de un cluster cuando el archivo es más pequeño que el cluster. Se mitiga eligiendo el tamaño de cluster adecuado al tipo de archivo.

---

### Pregunta 3 — NTFS vs FAT32
¿Qué ventaja tiene NTFS sobre FAT32?

| Característica | FAT32 | NTFS |
|----------------|-------|------|
| Journaling | ❌ | ✅ |
| Permisos granulares | ❌ | ✅ |
| Cifrado EFS | ❌ | ✅ |
| Tamaño máximo archivo | 4 GB | 16 TB |

> **Respuesta:** NTFS tiene journaling, permisos granulares (ACL), compresión y cifrado EFS. FAT32 carece de estas características.

</details>

</details>

---

## 🎯 Próximo paso

> [!info] Continuar con
> **[[03-Arranque-y-Seguridad|🛡️ Arranque y seguridad]]** — Ahora que entiendes cómo se organizan los datos en disco, verás cómo se protege el arranque del sistema.

---

## ⚠️ Errores comunes

> [!warning] Error 1: Confundir MP4 con evolución de MP3
> MP4 no es "mejor MP3". MP4 es un **contenedor** que puede incluir video, audio, subtítulos y metadatos. MP3 es solo audio.

> [!warning] Error 2: Formato rápido = datos borrados
> El formato rápido solo marca la FAT como "libre". Los datos siguen en disco hasta ser sobrescritos. Un forense puede recuperarlos.

> [!warning] Error 3: Un directorio es una "carpeta" especial
> En sistemas tipo UNIX, un directorio **es un archivo** que contiene nombres + inodos. No es un concepto mágico, es una estructura de datos.

> [!warning] Error 4: Cluster = tamaño de archivo
> Un archivo de 1 byte en un cluster de 32 KB **ocupa 32 KB** en disco. El espacio se asigna por cluster, no por byte.

---

## Referencias

> [!info] Recursos externos
> - [Microsoft — Sistemas de archivos](https://learn.microsoft.com/en-us/windows/storage/file-systems/)
> - [Microsoft — NTFS](https://learn.microsoft.com/en-us/windows/storage/file-systems/ntfs)
> - [Microsoft — ReFS](https://learn.microsoft.com/en-us/windows/storage/refs/refs-overview)
> - [Microsoft — Formatos Office](https://learn.microsoft.com/en-us/office/troubleshoot/office-file-format)
