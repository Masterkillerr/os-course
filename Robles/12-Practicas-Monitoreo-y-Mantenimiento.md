---
sidebar_title: "🛠️ Prácticas — Monitoreo y Mantenimiento"
order: 103
unit: "Unidad 3 — Herramientas"
---

# Prácticas: Monitoreo y Mantenimiento del Sistema

## Práctica 1: Administrador de tareas (`taskmgr.exe`)

- **Procesos**: nombre, estado, cpu, memoria, disco, red + configuraciones. Administrador de tareas
  del navegador: cache, offline, notificaciones.
- **Rendimiento**: cpu, memoria, disco, wifi. `dxdiag.exe` para VRAM, `msconfig` sirve para limitar la RAM.
  - SSD: archivo de paginación → **sí** (encargado de paginar la memoria virtual con la RAM).
- **Historial de aplicaciones**: nombre, tiempo cpu, red, notificaciones.
- **Aplicaciones de arranque**: nombre, editor, estado, impacto.
- **Usuarios**: nombre, estado, cpu, memoria, disco, red.
- **Detalles**: nombre, pid, estado, usuario, cpu, plataforma 32/64, arquitectura.
- **Servicios**: nombre, pid, descripción, estado, grupo.

## Práctica 2: Monitores de recursos y rendimiento

- `resmon.exe` — Monitor de recursos.
- `perfmon.exe /report` — Informe de rendimiento.

## Práctica 3: Memoria (`taskmgr.exe` / `resmon.exe`)

- En uso
- Disponible
- Cache (en espera)
- Confirmada (con la memoria virtual)
- Bloque paginado (kernel disk)
- Bloque no paginado (kernel RAM)
- Velocidad, ranuras, factor de forma, reservada para hardware

## Práctica 4: Reparación de archivos e imagen del sistema

- **SFC** (System File Checker, archivos protegidos del sistema)
  - `/scannow`: analiza la integridad de todos los archivos.
- **DISM** (Deployment Image Servicing and Management, component store)
  - `/Online`: SO en ejecución.
  - `/Cleanup-Image`: limpieza y recuperación en la imagen.
  - `/CheckHealth`: revisión rápida de si la imagen está dañada (true/false).
  - `/ScanHealth`: qué parte del almacén de componentes está dañada.
  - `/RestoreHealth`: repara el almacén (`/Windows/WinSxS`).
- **CHKDSK** (Check Disk, archivos del disco)
  - `/F`: fix, reparar.
  - `/R`: recover, recupera lo que puede.

## Práctica 5: Microsoft PC Manager

- Home (PC Boost)
- Protection
- Storage
- Apps
- AI Tools
- Restore
- ClawBoard
- Settings (General)
