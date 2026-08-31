---
next: 05-Historia-Windows
parent: 08-Linea-de-Comandos
prev: 08a-CMD
title: "⌨️ PowerShell — cmdlets y ejemplos"
sidebar_title: "⌨️ PowerShell — cmdlets y ejemplos"
order: 102
unit: "Unidad 3 — Herramientas"
clase: 2
tema: "cmdlets y ejemplos"
profesor: "Fabián Robles"
tags: [cmd, powershell, automatización, linea-comandos, sistemas-operativos]
prerequisitos: ["Conceptos básicos de Windows"]
tiempo_clase: null
---

# ⌨️ PowerShell — cmdlets y ejemplos

> [!info] Módulo
> **Clase 2** — Línea de comandos, PowerShell y automatización
> **Tema:** ⌨️ PowerShell — cmdlets y ejemplos
> **Ver también:** [[08-Linea-de-Comandos|⌨️ Línea de Comandos (CMD y PowerShell)]]

> [!tip] Prerrequisitos
> - Conceptos básicos de sistemas operativos
> - [[08-Linea-de-Comandos|⌨️ Línea de Comandos (CMD y PowerShell)]] — visión general

---

> [!info] Anterior
> [[08-Linea-de-Comandos|⌨️ Línea de Comandos (CMD y PowerShell)]] — visión general

PowerShell usa **cmdlets** con formato `Verbo-Sustantivo` y trabaja con **objetos** (no solo texto), lo que permite encadenarlos en una *pipeline*.

```mermaid
graph LR
    A[Get-ChildItem] -->|objetos| B[Where-Object]
    B -->|filtrados| C[Sort-Object]
    C -->|ordenados| D[Export-Csv]
```

### CMD ↔ PowerShell (alias comunes)
| CMD | PowerShell (cmdlet) | Alias PS |
|---|---|---|
| `dir` | `Get-ChildItem` | `gci`, `ls` |
| `cd` | `Set-Location` | `sl` |
| `type` | `Get-Content` | `gc`, `cat` |
| `copy` | `Copy-Item` | `cpi`, `cp` |
| `del` | `Remove-Item` | `ri`, `rm` |
| `move` | `Move-Item` | `mi`, `mv` |
| `cls` | `Clear-Host` | `clear` |
| `tasklist` | `Get-Process` | `gps` |
| `ipconfig` | `Get-NetIPAddress` | — |
| `help` | `Get-Help` | `gh` |

### Ejemplos útiles
```powershell
# Listar procesos
Get-Process

# Solo lo que inicia con M
Get-ChildItem M*

# Info de BIOS
Get-WmiObject -Class Win32_BIOS

# Primeras 50 líneas a otro archivo
Get-Content "nuevo.txt" -TotalCount 50 | Set-Content "jaja.txt"

# Servicios a HTML
Get-Service | ConvertTo-Html -Property Name,Status > Servicios.htm

# Ver todos los alias
Get-Alias
```

> [!tip] Ayuda integrada
> `Get-Help <cmdlet>` (o `help`) abre la documentación, incluso conectándose a la web. `Get-Alias` lista todos los alias disponibles.

### Actualizar PowerShell con `winget`

```cmd
winget install --id Microsoft.Powershell.Preview --source winget
```

Alternativa: descargar el instalador de la última versión directamente desde la
[documentación oficial de instalación](https://learn.microsoft.com/es-es/powershell/scripting/install/installing-powershell-on-windows).

### Tabla completa de alias PowerShell → cmdlet

> [!info] Del documento fuente
> Captura de `Get-Alias` en una instalación estándar de Windows PowerShell (referencia completa).

| Alias | Cmdlet | | Alias | Cmdlet |
|---|---|---|---|---|
| `%` | `ForEach-Object` | | `gsv` | `Get-Service` |
| `?` | `Where-Object` | | `gtz` | `Get-TimeZone` |
| `ac` | `Add-Content` | | `gu` | `Get-Unique` |
| `asnp` | `Add-PSSnapin` | | `gv` | `Get-Variable` |
| `cat` | `Get-Content` | | `gwmi` | `Get-WmiObject` |
| `cd` | `Set-Location` | | `h` / `history` | `Get-History` |
| `chdir` | `Set-Location` | | `icm` | `Invoke-Command` |
| `clc` | `Clear-Content` | | `iex` | `Invoke-Expression` |
| `clear` | `Clear-Host` | | `ihy` | `Invoke-History` |
| `cli` | `Clear-Item` | | `ii` | `Invoke-Item` |
| `cls` | `Clear-Host` | | `ipal` | `Import-Alias` |
| `clv` | `Clear-Variable` | | `ipcsv` | `Import-Csv` |
| `compare` | `Compare-Object` | | `ipmo` | `Import-Module` |
| `copy` / `cp` / `cpi` | `Copy-Item` | | `irm` | `Invoke-RestMethod` |
| `curl` / `iwr` / `wget` | `Invoke-WebRequest` | | `ise` | `powershell_ise.exe` |
| `del` / `erase` / `rd` / `ri` / `rm` / `rmdir` | `Remove-Item` | | `kill` | `Stop-Process` |
| `diff` | `Compare-Object` | | `ls` / `dir` / `gci` | `Get-ChildItem` |
| `echo` / `write` | `Write-Output` | | `man` | `help` |
| `epal` | `Export-Alias` | | `md` / `mkdir` | (función) |
| `epcsv` | `Export-Csv` | | `measure` | `Measure-Object` |
| `fc` | `Format-Custom` | | `mi` / `move` / `mv` | `Move-Item` |
| `fl` | `Format-List` | | `mount` | `New-PSDrive` |
| `foreach` | `ForEach-Object` | | `ni` | `New-Item` |
| `ft` | `Format-Table` | | `nv` | `New-Variable` |
| `fw` | `Format-Wide` | | `ogv` | `Out-GridView` |
| `gal` | `Get-Alias` | | `popd` / `pushd` | `Pop-/Push-Location` |
| `gc` / `type` | `Get-Content` | | `ps` / `gps` | `Get-Process` |
| `gcb` | `Get-Clipboard` | | `pwd` / `gl` | `Get-Location` |
| `gcm` | `Get-Command` | | `r` | `Invoke-History` |
| `gi` | `Get-Item` | | `rni` / `ren` | `Rename-Item` |
| `gin` | `Get-ComputerInfo` | | `sajb` | `Start-Job` |
| `gjb` | `Get-Job` | | `sal` | `Set-Alias` |
| `gm` | `Get-Member` | | `saps` / `start` | `Start-Process` |
| `gmo` | `Get-Module` | | `sasv` | `Start-Service` |
| `gp` / `gpv` | `Get-ItemProperty(Value)` | | `sc` | `Set-Content` |
| `group` | `Group-Object` | | `select` | `Select-Object` |
| `set` / `sv` | `Set-Variable` | | `shcm` | `Show-Command` |
| `si` | `Set-Item` | | `sl` | `Set-Location` |
| `sleep` | `Start-Sleep` | | `sls` | `Select-String` |
| `sort` | `Sort-Object` | | `sp` | `Set-ItemProperty` |
| `spjb` / `spps` / `spsv` | `Stop-Job/Process/Service` | | `tee` | `Tee-Object` |
| `where` | `Where-Object` | | `wjb` | `Wait-Job` |

### Herramientas y comandos adicionales de PowerShell

- **Historial persistente:** PowerShell recuerda 4096 comandos en texto plano, por usuario, en
  `%userprofile%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt`.
  Consultar su configuración: `Get-PSReadlineOption | select HistoryNoDuplicates, MaximumHistoryCount, HistorySearchCursorMovesToEnd, HistorySearchCaseSensitive, HistorySavePath, HistorySaveStyle`.
- **Extraer el serial de Windows:**
  ```powershell
  (Get-WmiObject -query 'select * from SoftwareLicensingService').OA3xOriginalProductKey
  ```
  o desde CMD: `wmic path softwarelicensingservice get OA3xOriginalProductKey`.
- **Información del equipo:** `systeminfo.exe` (CMD) o `Get-ComputerInfo` (PowerShell).
- **PowerShell ISE** (`powershell_ise.exe`): editor gráfico para escribir y guardar scripts `.ps1` con varios comandos.
- **Diagnóstico de RAM:** `MdSched.exe` (Diagnóstico de memoria de Windows, desde Windows 7). Ofrece
  reiniciar y testear de inmediato, o testear en el próximo reinicio; el resultado se muestra tras reiniciar.

> [!info] Imágenes de referencia (documento fuente)
> El PDF de origen incluye capturas de: la tabla de alias de `Get-Alias`, la ruta del historial en el
> explorador de archivos, la ventana de **Diagnóstico de memoria de Windows** con sus dos opciones, y el
> resultado del test de RAM sin errores.

---

