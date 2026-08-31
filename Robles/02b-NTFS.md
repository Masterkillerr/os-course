---
next: 02c-ReFS-y-atributos
parent: 02-Sistemas-de-Archivos
prev: 02a-FAT
title: "💾 NTFS — New Technology File System"
sidebar_title: "💾 NTFS — New Technology File System"
order: 62
unit: "Unidad 2 — Almacenamiento y Arranque"
clase: 2
tema: "New Technology File System"
profesor: "Fabián Robles"
tags: [sistemas-archivos, fat, ntfs, refs, cluster, clase-2, sistemas-operativos]
prerequisitos: ["Conceptos de almacenamiento", "Qué es un byte/bit"]
tiempo_clase: "18:18 - 46:33"
---

# 💾 NTFS — New Technology File System

> [!info] Módulo
> **Clase 2** — Sistemas de Archivos (FAT, NTFS, ReFS, exFAT)
> **Tema:** 💾 NTFS — New Technology File System
> **Ver también:** [[02-Sistemas-de-Archivos|💾 Sistemas de Archivos]]

> [!tip] Prerrequisitos
> - Conceptos básicos de sistemas operativos
> - [[02-Sistemas-de-Archivos|💾 Sistemas de Archivos]] — visión general

---

> [!info] Anterior
> [[02-Sistemas-de-Archivos|💾 Sistemas de Archivos]] — visión general

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

