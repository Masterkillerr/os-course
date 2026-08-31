---
title: "💾 Sistemas de Archivos"
sidebar_title: "💾 Sistemas de Archivos"
order: 30
unit: "Unidad 2 — Almacenamiento y Arranque"
clase: 2
tema: "Sistemas de Archivos (FAT, NTFS, ReFS, exFAT)"
profesor: "Fabián Robles"
tags: [sistemas-archivos, fat, ntfs, refs, cluster, clase-2, sistemas-operativos]
prerequisitos: ["Conceptos de almacenamiento", "Qué es un byte/bit"]
tiempo_clase: "18:18 - 46:33"
---

# 💾 Sistemas de Archivos

> [!info] Módulo
> **Unidad 2 — Almacenamiento y Arranque**
> **Tema:** Sistemas de Archivos (FAT, NTFS, ReFS, exFAT)
> **Ver también:** [[01-TPM|🔐 TPM]], [[03-Arranque-y-Seguridad|🛡️ Arranque y seguridad]]

> [!tip] Prerrequisitos
> - Conceptos de almacenamiento (disco, SSD, USB)
> - Qué es un byte / bit
> - Conceptos básicos de matemáticas (potencias de 2)

---

## 📋 Tabla de contenidos

- [[#Estructura-de-un-medio-de-almacenamiento]]
- [[#¿Por-qué-500-GB-no-son-500-GB]]
- [[#Evolución-de-sistemas-de-archivos]]
- [[#FAT-=-File-Allocation-Table]]
- [[#NTFS-=-New-Technology-File-System]]
- [[#ReFS-=-Resilient-File-System]]
- [[#Atributos-de-archivos]]
- [[#Tamaño-de-unidad-de-asignación-(Cluster)]]
- [[#Formato-rápido-vs.-Formato-completo]]
- [[#Nombres-de-archivo-y-extensiones]]

---

## Estructura de un medio de almacenamiento

```mermaid
graph TD
    A[Disco Duro / SSD / Pendrive] --> B[Sector de Arranque]
    A --> C[Sistema de Archivos]
    A --> D[Espacio Libre]
    
    B --> B1[MBR / GPT]
    B --> B2[Bootloader]
    
    C --> C1[FAT / NTFS / exFAT / ReFS]
    C --> C2[Directorio Root]
    C --> C3[Datos de usuario]
    
    style A fill:#ff6b6b
    style C fill:#4ecdc4
    style D fill:#95a5a6
```

### Métodos de acceso a archivos

| Método | Cómo funciona |
|---|---|
| **Secuencial** | Se lee/escribe en orden, desde el principio, byte a byte o registro a registro (ej. cintas magnéticas, logs). |
| **Directo (aleatorio)** | Se accede directamente a cualquier posición del archivo sin recorrer las anteriores (posible gracias a que el disco es direccionable por bloque). |
| **Indexado** | Un índice separado guarda punteros a bloques del archivo, permitiendo búsquedas rápidas sin recorrerlo completo (ej. bases de datos). |

---

## ¿Por qué 500 GB no son 500 GB?

> [!info] Sociedad vs Sistema Operativo
> La sociedad usa **base 10**, pero los sistemas operativos usan **base 2**.
>
> | Unidad | Cálculo | Valor |
> |--------|---------|-------|
> | 1 GB (fabricante) | $10^9$ | 1,000,000,000 bytes |
> | 1 GiB (SO) | $2^{30}$ | 1,073,741,824 bytes |
>
> Por eso un SSD de 500 GB se muestra como **~465 GiB** en Windows.

$$ \text{Espacio visible} = \frac{\text{Capacidad fabricante}}{2^{30}} $$

> [!tip] Regla mnemotécnica
> La sociedad piensa en decimal (10 dedos), el SO en binario (bits). Mientras la sociedad odie el Wii, nosotros trabajamos en base 2.

---

## Evolución de sistemas de archivos

```mermaid
timeline
    title Evolución de Sistemas de Archivos en Windows
    section 1980s
        1980 : FAT12
        1984 : FAT16
    section 1990s
        1993 : NTFS
        1996 : FAT32
    section 2000s
        2006 : exFAT
    section 2010s
        2012 : ReFS
```

### Comparativa rápida

| Sistema | Año | Cluster mínimo | Permisos | Journaling | Uso actual |
|---------|-----|---------------|----------|------------|------------|
| **FAT12** | 1980 | — | ❌ | ❌ | Floppies |
| **FAT16** | 1984 | 512 B | ❌ | ❌ | USB viejos |
| **FAT32** | 1996 | 512 B | ❌ | ❌ | USB, compatibilidad |
| **exFAT** | 2006 | 4 KB | ❌ | ❌ | USB grandes |
| **NTFS** | 1993 | 512 B | ✅ | ✅ | Discos internos |
| **ReFS** | 2012 | 64 KB | ✅ | ✅ | Servidores |

---

## FAT = File Allocation Table

```mermaid
graph LR
    DIR[Entrada del directorio<br/>primer cluster: 4] --> FAT["Tabla FAT<br/>4 → 7 → 9 → 12 → EOF"]
    FAT --> K4[(Cluster 4)]
    FAT --> K7[(Cluster 7)]
    FAT --> K9[(Cluster 9)]
    FAT --> K12[(Cluster 12)]
```
> Cada entrada de directorio apunta al **primer cluster**; la FAT guarda la cadena de clusters siguientes hasta `EOF`. Recorrer un archivo = seguir la cadena en la tabla.

> [!note] FAT
> **File Allocation Table** — Tabla de Asignación de Archivos.
>
> La tabla es un índice que registra en qué clusters está almacenado cada archivo. Si se corrompe la FAT, se pierde la capacidad de leer los archivos.

```
CÓMO FUNCIONA LA FAT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Archivo: "foto.jpg" (3 clusters)
  
  FAT Table:
  ┌──────┬───────────┐
  │ 0    │ Libre     │
  │ 1    │ Libre     │
  │ 2    │ Ocupado ──┼──► Cluster 2 en disco
  │ 3    │ Ocupado ──┼──► Cluster 5 en disco
  │ 4    │ Ocupado ──┼──► Cluster 9 en disco
  │ 5    │ Fin (EOF) │
  └──────┴───────────┘
  
  Para leer "foto.jpg": FAT → [2 → 5 → 9 → fin]
```

> [!warning] Problema
> Si se corrompe la FAT, se pierden todos los punteros.

> [!important] Resumen: FAT
> - **Ventaja:** Simple, rápido, compatible con todo.
> - **Desventaja:** Sin journaling, sin permisos, se fragmenta fácilmente.
> - **Uso actual:** USB de poca capacidad, compatibilidad con dispositivos antiguos.

---

## NTFS = New Technology File System

```mermaid
graph TD
    A[Volumen NTFS] --> B[Sector de arranque]
    A --> C[MFT Master File Table]
    A --> D[Área de datos clusters]
    
    C --> C1[MFT registro 0 - la propia MFT]
    C --> C2[MFTMirr - copia espejo]
    C --> C3[LogFile - journaling]
    C --> C4[Volume - info del volumen]
    C --> C5[Archivos de usuario]
    
    style A fill:#ff6b6b
    style C fill:#4ecdc4
```

> [!info] Características clave
> - **Journaling**: Registra cambios antes de escribirlos → recuperación ante fallos.
> - **Permisos granulares**: ACL (Access Control Lists) por archivo/carpeta.
> - **Compresión transparente**: El SO comprime/descomprime al vuelo.
> - **Cifrado EFS**: Encrypting File System por usuario.

> [!important] Resumen: NTFS
> - **Ventaja:** Robusto, seguro, con journaling y permisos granulares.
> - **Desventaja:** Más complejo, overhead de rendimiento.
> - **Uso actual:** Discos internos de Windows, servidores.

---

## ReFS = Resilient File System

```mermaid
graph TD
    A[Disco con 3 copias] --> B[Copia 1]
    A --> C[Copia 2]
    A --> D[Copia 3]
    
    B --> B1[✅ Correcto]
    C --> C1[❌ Corrupto]
    D --> D1[✅ Correcto]
    
    E[ReFS detecta corrupción] --> F[Repara automáticamente<br>desde copia válida]
    
    style C1 fill:#ff6b6b
    style F fill:#4ecdc4
```

> [!quote] Filosofía
> "Si un miembro falla, el sistema es capaz de devolverse a un estado anterior válido."

---

## Atributos de archivos

### En consola (CMD / PowerShell)

| Atributo | Símbolo | Significado |
|----------|---------|-------------|
| Archive | `A` | Modificado desde último backup |
| Read-only | `R` | Solo lectura |
| Hidden | `H` | Oculto |
| System | `S` | Protegido por el sistema |
| Not indexed | `I` | No indexado por Windows Search |

### Directorios = Archivos especiales

```
EN UNIX/LINUX TODO ES ARCHIVO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  /home/usuario/
  ├── 📄 tesis.docx        ← archivo regular
  ├── 🖼️ foto.jpg          ← archivo regular
  ├── 📁 Documentos/       ← archivo especial (directorio)
  │   ├── 📄 informe.pdf
  │   └── 📄 presupuesto.xlsx
  └── 📁 .config/          ← archivo oculto (directorio)
      └── ⚙️ settings.conf
```

> [!info] ¿Por qué?
> Un directorio es un archivo que contiene nombres + números de inodo/cluster + permisos. Esto permite rutas jerárquicas como `/home/usuario/documento.txt`.

---

## Tamaño de unidad de asignación (Cluster)

```mermaid
graph TD
    subgraph CL["Cluster de 32 KB (unidad mínima de asignación)"]
        F[📄 Archivo de 1 byte<br/>⬛ ocupa el cluster entero]
        W["⬜ 31.99 KB desperdiciados<br/>(fragmentación interna)"]
    end
```
> El espacio se asigna por cluster completo aunque el archivo ocupe menos: un archivo de 1 byte en un cluster de 32 KB **ocupa 32 KB** en disco.

### Problema del cluster grande

```
PENDRIVE DE 8 GB, CLUSTER DE 32 KB
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Si guardas 1 archivo de 1 byte:
  
  ┌──────────────────────────────────┐
  │  Cluster de 32 KB                │
  │  ┌────────────────────────────┐  │
  │  │ A (1 byte)                 │  │
  │  │                           │  │
  │  │ 31,999 bytes VACÍOS       │  │
  │  │  ← desperdicio            │  │
  │  └────────────────────────────┘  │
  └──────────────────────────────────┘
```

$$ \text{Desperdicio} = \frac{\text{cluster} - \text{tamaño\_archivo}}{\text{cluster}} \times 100\% $$

> [!example] Analogía del profesor
> Alquilar un auditorio de 32,000 puestos para que habite una sola estudiante.

### Cluster óptimo por tipo de archivo

| Tipo de archivo | Cluster recomendado |
|-----------------|---------------------|
| Documentos de texto | 4 KB |
| Fotos, música | 32–64 KB |
| Videos, imágenes grandes | 128–256 KB |

> [!important] Resumen: Cluster size
> - **Cluster pequeño (4 KB):** Mejor para documentos pequeños, más operaciones I/O.
> - **Cluster grande (128-256 KB):** Mejor para videos, menos desperdicio en archivos grandes.
> - **Regla de oro:** Mientras más pequeño el archivo promedio, más pequeño el cluster.

---

## Formato rápido vs. Formato completo

```mermaid
graph TD
    F[Format C:] --> R[Rápido: borra solo la tabla FAT/MFT<br/>los datos QUEDAN en disco y son recuperables]
    F --> C[Completo: escribe ceros en toda la superficie<br/>los datos se DESTRUYEN]
```


| Tipo | Acción | Recuperación de datos |
|------|--------|----------------------|
| **Rápido** | Borra solo la tabla de asignación (FAT) | ✅ Los datos siguen en disco |
| **Completo** | Escribe ceros en toda la superficie | ❌ Datos destruidos |

> [!warning] Advertencia forense
> El formato rápido **no elimina datos**. Un especialista puede recuperarlos con herramientas como `photorec`, `testdisk`, o análisis forense.

---

## Nombres de archivo y extensiones

### Límites históricos

| Sistema | Nombre | Extensión | Ejemplo |
|---------|--------|-----------|---------|
| FAT16 | 8 caracteres | 3 caracteres | `TESIS.DOC` |
| FAT32 / NTFS | 255 caracteres | 255 caracteres | `mi_tesis_doctoral_v2_final.docx` |

### Extensiones y formatos

| Extensión | Tipo | Formato |
|-----------|------|---------|
| `.txt` | Documento | Texto plano |
| `.docx` | Documento | Word (XML comprimido) |
| `.xlsx` | Hoja de cálculo | Excel (XML comprimido) |
| `.pptx` | Presentación | PowerPoint (XML comprimido) |
| `.html` / `.htm` | Web | HyperText Markup Language |
| `.js` | Web | JavaScript |
| `.php` | Web | PHP preprocesado |
| `.mp3` | Audio | MPEG-1 Audio Layer 3 |
| `.mp4` | Video | MPEG-4 Part 14 (contenedor) |
| `.jpg` | Imagen | JPEG comprimido |
| `.png` | Imagen | PNG sin pérdida |

> [!info] Nota técnica
> MP4 **no** es una evolución de MP3. MP4 es un **contenedor** que puede incluir audio, video, subtítulos y metadatos.

---

## Límite de longitud de ruta (260 caracteres)

Por defecto Windows limita la ruta a **260 caracteres** (p. ej. `C:\Carpeta\Subcarpeta\Archivo.txt`). Rigen dos reglas independientes:

- Cada componente (carpeta/archivo) ≤ **255** caracteres.
- Ruta total ≤ **32.767** caracteres (pero el límite de 260 aplica si no se activa la opción larga).

Para habilitar rutas largas:

```cmd
reg query HKLM\SYSTEM\CurrentControlSet\Control\FileSystem /v LongPathsEnabled
reg add  HKLM\SYSTEM\CurrentControlSet\Control\FileSystem /v LongPathsEnabled /t REG_DWORD /d 1 /f
```

Y usar el prefijo `\\?\` para copiar rutas muy largas sin recortar:

```cmd
robocopy "\\?\C:\LAB_LONGPATH" "C:\DESTINO_LARGO" /E /COPYALL /R:1 /W:1
```

> [!warning] Caracteres prohibidos
> En nombres y rutas nunca uses: `\ / : * ? " < > |`

---
