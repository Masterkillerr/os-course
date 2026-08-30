# ⌨️ Línea de comandos, PowerShell y automatización

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

---

## Programador de tareas (Task Scheduler)

Automatiza la ejecución de programas a hora, evento o condición. Se abre desde Herramientas administrativas.

### Asistente visual (Crear tarea)
1. **General** — nombre, descripción, nivel de seguridad (cuenta que ejecuta la tarea, privilegio).
2. **Desencadenadores** — *cuándo*: Una vez, Diaria, Semanal, Mensual, al iniciar sesión, al bloquear, etc.
3. **Acciones** — *qué* ejecutar: Iniciar un programa, enviar un correo, mostrar un mensaje. Ruta + argumentos.
4. **Condiciones** — *si* se ejecuta: solo si el equipo está inactivo, con corriente alterna, con red local.
5. **Configuración** — permisos, reglas de ejecución, eliminación automática.

```mermaid
graph TD
    G[General: nombre + cuenta] --> D[Desencadenadores: cuándo]
    D --> A[Acciones: qué ejecutar]
    A --> C[Condiciones: si se ejecuta]
    C --> CF[Configuración: permisos y reglas]
```

### Desde consola (schtasks)
```cmd
:: Crear tarea diaria a las 15:30
schtasks /create /tn Backup /tr "backup.bat" /sc daily /st 15:30

:: Consultar
schtasks /query /tn "Backup"

:: Eliminar
schtasks /delete /tn "Backup"
```

> [!warning] Auditoría
> Habilita el **historial** de tareas programadas: es clave para auditorías y para saber por qué algo corrió (o no).

---

## Consejos de productividad

- **Redirecciones:** `>` (sobrescribe) y `>>` (agrega). `systeminfo > info.txt`
- **Pipes `|`:** `dir *.exe /b | findstr "notepad"`
- **Combinar:** `dir /s /b > lista.txt` (todo el árbol a un archivo)
- **Ayuda:** `help` o `comando /?` en CMD; `Get-Help` en PowerShell.
- **Concatenar archivos:** `copy a.txt + b.txt c.txt`

---

## 📝 Autoevaluación

```flipcard
**Pregunta 1 — ¿Qué es CMD realmente?**
¿El símbolo del sistema es el sistema operativo DOS?
---
No. CMD es una aplicación de línea de comandos de Windows; recuerda a MS-DOS pero no es DOS ni parte del núcleo.
```

```flipcard
**Pregunta 2 — ¿Qué diferencia a PowerShell de CMD?**
¿Por qué PowerShell es más potente para automatizar?
---
PowerShell usa cmdlets (Verbo-Sustantivo) y trabaja con objetos .NET en la pipeline, no solo texto; permite scripts, remoto y tareas en segundo plano.
```

```flipcard
**Pregunta 3 — ¿Para qué sirve schtasks?**
¿Cómo programo una copia de seguridad diaria?
---
Con `schtasks /create /tn Backup /tr "backup.bat" /sc daily /st 15:30`, o con el asistente del Programador de tareas (General → Desencadenadores → Acciones).
```

---

## ⚠️ Errores comunes

> [!warning] Error 1: Creer que CMD es MS-DOS
> CMD es una consola de Windows, no el sistema operativo DOS.

> [!warning] Error 2: Usar `>` cuando se quería `>>`
> `>` sobrescribe el archivo; `>>` agrega. `systeminfo > info.txt` reemplaza; `>>` acumula.

> [!warning] Error 3: Pensar que PowerShell es solo "CMD con otro nombre"
> PowerShell procesa objetos y tiene cientos de cmdlets; un alias como `dir` en realidad es `Get-ChildItem`.

---

## Referencias

> [!info] Recursos externos
> - [Microsoft — Símbolo del sistema (referencia)](https://learn.microsoft.com/es-es/windows-server/administration/windows-commands/cmd)
> - [Microsoft — Documentación de PowerShell](https://docs.microsoft.com/es-es/powershell/)
> - [Microsoft — Schtasks](https://learn.microsoft.com/es-es/windows-server/administration/windows-commands/schtasks)
