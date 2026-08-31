---
next: 05-Historia-Windows
prev: 01-TPM
title: "⌨️ Línea de Comandos (CMD y PowerShell)"
sidebar_title: "⌨️ Línea de comandos"
order: 100
unit: "Unidad 3 — Herramientas"
clase: 2
tema: "Línea de comandos, PowerShell y automatización"
profesor: "Fabián Robles"
tags: [cmd, powershell, automatización, linea-comandos, sistemas-operativos]
prerequisitos: ["Conceptos básicos de Windows"]
tiempo_clase: null
---

# ⌨️ Línea de Comandos (CMD y PowerShell)

> [!info] Módulo
> **Unidad 3 — Herramientas**
> **Tema:** CMD, PowerShell, cmdlets, Programador de tareas, schtasks
> **Ver también:** [[09-Fundamentos-del-SO|🧠 Fundamentos del SO]]

> [!info] Objetivo
> Conocer las dos consolas de Windows (CMD y PowerShell), sus comandos esenciales, y cómo automatizar tareas con el Programador de tareas. Equivalentes a la terminal de Linux o macOS.

---

## 📋 Tabla de contenidos

- [[#Windows PowerShell vs Símbolo del sistema]]
- [[#CMD — Comandos esenciales]]
- [[#PowerShell — cmdlets y ejemplos]]
- [[#Programador de tareas (Task Scheduler)]]
- [[#Consejos de productividad]]
- [[#📝 Autoevaluación]]
- [[#⚠️ Errores comunes]]

---

## Windows PowerShell vs Símbolo del sistema

Windows ofrece **dos consolas**. Visualmente parecidas, pero muy distintas en la práctica:

| | Símbolo del sistema (CMD) | Windows PowerShell |
|---|---|---|
| Origen | Recuerda a MS-DOS, pero **no es DOS** ni parte del SO | Shell y lenguaje de scripts sobre **.NET** (C#) |
| Modelo | Comandos sueltos (programas `.exe`) | **Cmdlets** (`Verbo-Sustantivo`), objetos en la pipeline |
| Automatización | Lotes `.bat` limitados | Scripts `.ps1` potentes, remoto, tareas en segundo plano |
| Apertura | `cmd` o Win+R | Win + X → PowerShell, o `powershell` |

> [!warning] CMD no es MS-DOS
> El símbolo del sistema es una aplicación de línea de comandos de Windows; no es el sistema operativo DOS ni forma parte del núcleo.

```mermaid
graph LR
    U[Usuario] --> CMD[Símbolo del sistema<br/>texto plano]
    U --> PS[PowerShell<br/>objetos .NET]
    CMD --> EXE[Programas .exe]
    PS --> NET[.NET Framework / C#]
    PS --> PIPE[Pipeline de objetos]
```

---

## CMD — Comandos esenciales

### 1️⃣ Navegación de directorios y archivos
| Comando | Descripción | Ejemplo |
|---|---|---|
| `cd` / `chdir` | Cambiar directorio | `cd C:\Users\IngeAmigo\Documentos` |
| `cd ..` | Subir un nivel | `cd ..` |
| `cd \` | Ir a la raíz | `cd \` |
| `dir` | Listar archivos y carpetas | `dir /w` (en ancho) |
| `tree` | Estructura de carpetas en árbol | `tree /F` (incluye archivos) |
| `pushd` / `popd` | Guardar y recuperar directorio | `pushd D:\Proyectos` |

### 2️⃣ Manejo de archivos y carpetas
| Comando | Descripción | Ejemplo |
|---|---|---|
| `mkdir` / `md` | Crear carpeta | `mkdir Proyecto1` |
| `rmdir` / `rd` | Eliminar carpeta vacía | `rmdir CarpetaVieja` |
| `del` / `erase` | Eliminar archivos | `del archivo.txt` |
| `copy` | Copiar archivos | `copy archivo.txt D:\Backup` |
| `xcopy` | Copiar carpetas y subcarpetas | `xcopy C:\Proyectos D:\Backup /E /I` |
| `robocopy` | Copia robusta (reanudable) | `robocopy C:\Proyectos D:\Backup /MIR /Z` |
| `move` | Mover archivos o carpetas | `move archivo.txt D:\Documentos` |
| `ren` / `rename` | Cambiar nombre | `rename archivo.txt nuevo.txt` |
| `attrib` | Atributos (solo lectura, oculto, sistema) | `attrib +h archivo.txt` |

### 3️⃣ Visualización y edición
| Comando | Descripción | Ejemplo |
|---|---|---|
| `type` | Mostrar contenido de texto | `type notas.txt` |
| `more` | Texto paginado | `type notas.txt \| more` |
| `echo` | Mostrar texto | `echo Hola mundo` |
| `find` | Buscar texto en archivos | `find "error" log.txt` |
| `findstr` | Patrones avanzados (regex) | `findstr /i "error warning" log.txt` |
| `fc` | Comparar archivos | `fc a.txt b.txt` |

### 4️⃣ Red y conectividad
| Comando | Descripción | Ejemplo |
|---|---|---|
| `ping` | Probar conectividad | `ping google.com` |
| `ipconfig` | Configuración de red | `ipconfig /all` |
| `tracert` | Rastrear ruta a un host | `tracert google.com` |
| `netstat` | Conexiones activas | `netstat -an` |
| `nslookup` | Consultar DNS | `nslookup ejemplo.com` |
| `arp` | Tabla ARP | `arp -a` |
| `net` | Usuarios, shares, grupos | `net user` / `net share` |
| `pathping` | Mezcla ping + tracert | `pathping google.com` |

### 5️⃣ Procesos y tareas
| Comando | Descripción | Ejemplo |
|---|---|---|
| `tasklist` | Listar procesos | `tasklist` |
| `taskkill` | Finalizar procesos | `taskkill /IM notepad.exe /F` |
| `start` | Abrir programas/ventanas | `start notepad.exe` |
| `shutdown` | Apagar o reiniciar | `shutdown /s /t 60` |
| `schtasks` | Programar tareas | `schtasks /create /tn Backup /tr "backup.bat" /sc daily /st 15:30` |

### 6️⃣ Información del sistema
| Comando | Descripción | Ejemplo |
|---|---|---|
| `systeminfo` | Info detallada del sistema | `systeminfo` |
| `wmic` | Administración de Windows | `wmic cpu get name,NumberOfCores` |
| `driverquery` | Controladores instalados | `driverquery /v /fo list` |
| `chkdsk` | Revisar y reparar discos | `chkdsk C: /F /R` |
| `sfc` | Archivos de sistema | `sfc /scannow` |
| `dism` | Reparar la imagen de Windows | `DISM /Online /Cleanup-Image /RestoreHealth` |
| `diskpart` | Discos y particiones | `diskpart` → `list disk` |
| `powercfg` | Energía/batería | `powercfg /batteryreport` |
| `fsutil` | Sistema de archivos avanzado | `fsutil volume diskfree C:` |

### 7️⃣ Avanzados y utilidades
| Comando | Descripción | Ejemplo |
|---|---|---|
| `reg` | Registro de Windows | `reg query HKLM\SYSTEM\CurrentControlSet\Services` |
| `assoc` | Asociar extensión a tipo | `assoc .txt=txtfile` |
| `ftype` | Programa asociado al tipo | `ftype txtfile="notepad.exe %1"` |
| `compact` | Comprimir archivos NTFS | `compact /c archivo.txt` |
| `mklink` | Enlaces simbólicos | `mklink /D Link CarpetaDestino` |
| `whoami` | Usuario actual | `whoami` |
| `hostname` | Nombre del equipo | `hostname` |

---

## PowerShell — cmdlets y ejemplos

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
