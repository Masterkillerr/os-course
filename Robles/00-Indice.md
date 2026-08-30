---
title: "🗂️ Índice — Curso de Sistemas Operativos"
clase: 2
tema: "TPM, File Systems, Boot y Seguridad"
profesor: "Fabián Robles"
tags: [indice, clase-2, sistemas-operativos]
---

# 🗂️ Índice — Curso de Sistemas Operativos

> [!info] Curso de Sistemas Operativos
> **Materia:** Sistemas Operativos  
> **Módulos:** Introducción (Clase 1) + TPM, File Systems, Boot, Estructuras, Historia, Mercado, Línea de comandos y Fundamentos del SO (Clase 2)  
> **Profesor:** Fabián Robles

---

## 📚 Notas de clase

| # | Módulo | Enlace | Temas |
|---|--------|--------|-------|
| 0 | [[🗂️ Índice\|00-Indice]] | `00-Indice.md` | Mapa del curso |
| 1 | [[📘 Introducción-a-los-SO\|07-Introduccion-SO]] | `07-Introduccion-SO.md` | Definición de SO, clasificación, compilaciones/Insider, SysInternals, estadísticas |
| 2 | [[🔐 TPM\|01-TPM]] | `01-TPM.md` | Funciones, implementaciones, estándares TCG, BitLocker |
| 3 | [[💾 Sistemas-de-Archivos\|02-Sistemas-de-Archivos]] | `02-Sistemas-de-Archivos.md` | FAT, NTFS, ReFS, exFAT, clusters, atributos |
| 4 | [[🛡️ Arranque-y-Seguridad\|03-Arranque-y-Seguridad]] | `03-Arranque-y-Seguridad.md` | POST, UEFI, Secure Boot, Core Isolation, DMA |
| 5 | [[📊 Estructuras-de-Datos\|04-Estructuras-de-Datos]] | `04-Estructuras-de-Datos.md` | Arrays vs Listas, aplicación en sistemas de archivos |
| 6 | [[🪟 Historia-Windows\|05-Historia-Windows]] | `05-Historia-Windows.md` | Línea de tiempo Windows desktop y server |
| 7 | [[📊 Mercado-OS\|06-Mercado-OS]] | `06-Mercado-OS.md` | Cuota de mercado, tendencias laborales, geopolítica |
| 8 | [[⌨️ Línea-de-Comandos\|08-Linea-de-Comandos]] | `08-Linea-de-Comandos.md` | CMD, PowerShell, cmdlets, Programador de tareas, schtasks |
| 9 | [[🧠 Fundamentos-del-SO\|09-Fundamentos-del-SO]] | `09-Fundamentos-del-SO.md` | Procesos/threads, memoria virtual, E/S, sincronización, virtualización, tipos de kernel |

---

## 🔗 Enlaces rápidos entre notas

```
📘 Introducción ──► [[07-Introduccion-SO\|📘 Introducción a los S.O.]]

TPM ────────┐
            ├──► [[02-Sistemas-de-Archivos\|💾 Sistemas de archivos]]
            │
            └──► [[03-Arranque-y-Seguridad\|🛡️ Arranque y seguridad]]

Sistemas de Archivos ──► [[04-Estructuras-de-Datos\|📊 Estructuras de datos]]

Historia Windows ──────► [[06-Mercado-OS\|📊 Mercado de OS]]
```

---

## 🌐 Recursos externos

| Recurso | URL | Descripción |
|---------|-----|-------------|
| [Trusted Computing Group](https://trustedcomputinggroup.org/) | https://trustedcomputinggroup.org/ | Estándares TPM |
| [Microsoft — BitLocker](https://learn.microsoft.com/en-us/windows/security/information-protection/bitlocker/bitlocker-overview) | Microsoft Learn | Cifrado de disco |
| [Microsoft — Secure Boot](https://learn.microsoft.com/en-us/windows-hardware/drivers/install/secure-boot) | Microsoft Learn | Arranque seguro |
| [Microsoft — File Systems](https://learn.microsoft.com/en-us/windows/storage/file-systems/) | Microsoft Learn | Sistemas de archivos |
| [StatCounter — OS Market Share](https://gs.statcounter.com/os-version) | StatCounter | Cuota de mercado |
| [TCG TPM 2.0 Spec](https://trustedcomputinggroup.org/work-groups/trusted-platform-module/) | TCG | Especificación técnica |
| [Stack Overflow Survey](https://survey.stackoverflow.co/) | Stack Overflow | Encuesta desarrolladores |
| [IEEE Spectrum](https://spectrum.ieee.org/top-programming-languages) | IEEE | Ranking lenguajes |

---

## 📝 Nota del transcript

> Las notas se generaron a partir de la transcripción de **Clase 2 TPM** y del PDF de presentación
> **"Clase Sistema Operativo Intro"** (profesor Fabián Robles).  
> Se eliminaron digresiones vulgares, anécdotas personales y comentarios fuera de tema.  
> Se preservó y estructuró el contenido educativo: definiciones, ejemplos, analogías y referencias.

---

## 📖 Glosario

| Término | Definición |
|---------|-----------|
| **TPM** | Trusted Platform Module — chip criptográfico para seguridad |
| **PCR** | Platform Configuration Register — registro de mediciones de arranque |
| **Secure Boot** | Verificación de firma digital del bootloader |
| **Core Isolation** | Aislamiento del kernel en RAM usando virtualización |
| **BitLocker** | Cifrado de disco completo de Microsoft |
| **FAT** | File Allocation Table — sistema de archivos básico |
| **NTFS** | New Technology File System — sistema de archivos moderno |
| **ReFS** | Resilient File System — sistema de archivos auto-reparable |
| **Cluster** | Unidad de asignación de espacio en disco |
| **Fragmentación interna** | Espacio desperdiciado dentro de un cluster |
| **Fragmentación externa** | Espacio desperdiciado entre clusters |
| **MBR** | Master Boot Record — esquema de particiones antiguo |
| **GPT** | GUID Partition Table — esquema de particiones moderno |
| **DMA** | Direct Memory Access — acceso directo a memoria |
| **UEFI** | Unified Extensible Firmware Interface — firmware moderno |
| **POST** | Power-On Self-Test — autoprueba de encendido |
