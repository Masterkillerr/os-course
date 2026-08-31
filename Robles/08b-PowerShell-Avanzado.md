---
title: "⌨️ PowerShell Avanzado y Programador de Tareas"
sidebar_title: "⌨️ PowerShell Avanzado"
order: 72
unit: null
clase: 2
tema: "PowerShell avanzado, DOS legacy, Task Scheduler y productividad"
profesor: "Fabián Robles"
tags: [powershell, cmdlets, schtasks, dos-legacy, clase-2, sistemas-operativos]
prerequisitos: ["Línea de comandos básica"]
tiempo_clase: null
---

# ⌨️ PowerShell Avanzado y Programador de Tareas

> [!info] Módulo
> **Unidad 3 — Herramientas**
> **Tema:** PowerShell avanzado, comandos DOS legacy, Task Scheduler y productividad
> **Ver también:** [[08-Linea-de-Comandos|⌨️ Línea de comandos]]

---

## SFC, DISM y CHKDSK — diagnóstico y reparación (Taller No. 1)

Tres herramientas de mantenimiento, con un **orden de ejecución que importa**:

1. **`sfc /scannow`** (System File Checker) — repara archivos de sistema individuales dañados o
   modificados. Se puede correr desde CMD o PowerShell.
2. Si `sfc` falla con un error como *"La protección de recursos de Windows encontró archivos
   corruptos pero no pudo reparar algunos de ellos"* → **`DISM`** (Deployment Image Servicing and
   Management), que repara el **almacén de componentes** (la imagen base) del que `sfc` depende
   para reparar:
   ```cmd
   DISM /Online /Cleanup-Image /CheckHealth
   DISM /Online /Cleanup-Image /ScanHealth
   DISM /Online /Cleanup-Image /RestoreHealth
   ```
3. **`chkdsk C: /F /R`** (CHKDSK) — verifica y repara el **disco** en sí: marca sectores dañados y
   recupera datos. Se ejecuta al final porque opera a un nivel más bajo (el medio físico), no los
   archivos del SO.

> [!important] Por qué ese orden
> `sfc` depende de que la imagen de Windows (que `DISM` repara) esté sana; si el propio disco tiene
> sectores dañados (lo que `chkdsk` detecta), ni `sfc` ni `DISM` pueden garantizar una reparación
> confiable. Por eso: primero intenta `sfc` (rápido, específico) → si falla, sube de nivel a `DISM`
> (imagen del SO) → `chkdsk` ataca el disco físico, el nivel más bajo.

### Switches adicionales de `sfc`

| Switch | Efecto |
|---|---|
| `/scannow` | Analiza y repara todos los archivos de sistema protegidos. |
| `/verifyonly` | Solo escanea (no repara). |
| `/scanfile <archivo>` | Analiza y repara un archivo específico. |
| `/verifyfile <archivo>` | Solo verifica un archivo específico (no repara). |
| `/offwindir <dir>` | Ubicación del directorio de Windows para reparación sin conexión. |
| `/offbootdir <dir>` | Ubicación del directorio de arranque para reparación sin conexión. |
| `/offlogfile=<ruta>` | Dónde guardar el archivo de registro de la operación. |

---

## Comandos DOS heredados (legado, referencia rápida)

> [!note] Cultura general
> Documento fuente: *"3 clase Comandos SIMBOLO, POWER SHELL y SOFTWARE.pdf"*. Ayuda para cualquiera:
> `HELP <comando>` (nuevos Windows) o `<comando> /?` (método tradicional). La mayoría son reliquias de
> MS-DOS que ya no se usan a diario, pero aparecen en exámenes de cultura general de la materia.

| Comando | Qué hace |
|---|---|
| `ASSOC` | Muestra/modifica asociaciones de extensión de archivo con programas |
| `ATTRIB` | Muestra/modifica atributos de archivos |
| `AT` | Programa ejecución de comandos a una hora/fecha (requiere el servicio de programación) |
| `ANSI.SYS` | Carga el código ANSI vía `Device=` en `Config.sys` |
| `APPEND` | Indica en qué directorios buscar archivos de datos (complementa `PATH`) |
| `ASSIGN` | Redirige un disco a otro (eliminado desde DOS 6) |
| `BACKUP` / `RESTORE` | Copia de seguridad de archivos y su restauración (eliminado desde DOS 6) |
| `BASIC` | Invoca el lenguaje BASIC de IBM en DOS IBM |
| `.BAT` | Extensión de archivos de procedimientos (ej. `AUTOEXEC.BAT`, se ejecuta al arrancar) |
| `BREAK` | Activa/desactiva interrupción con Ctrl+Pausa |
| `BUFFERS` | En `config.sys`, define capacidad del búfer de disco |
| `CALL` | Llama a otro `.bat` como subprograma desde un `.bat` |
| `CD` / `CHDIR` | Cambia de directorio |
| `CHCP` | Selecciona la tabla de códigos de caracteres |

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

> [!info] Captura del profesor: arranque y entorno del Programador de tareas
> El PDF *"4 programador de tareas.pdf"* abre con el diálogo **Ejecutar** mostrando
> `taskschd.msc` como comando de arranque. Luego muestra la consola **Programador
> de tareas** de tres columnas: izquierda = árbol "Programador de tareas (local)"
> → "Biblioteca del Programador de tareas"; centro = "Resumen del Programador de
> tareas" con estado de tareas ejecutadas en últimas 24h (ejemplo real: 0 total,
> 0 en ejecución, 0 sin errores, 0 detenido, 0 con errores); derecha = panel
> **Acciones** (Conectarse a otro equipo, Crear tarea básica, Crear tarea,
> Importar tarea, Mostrar todas las tareas en ejecución, Deshabilitar el
> historial de todas las tareas, Configuración de cuenta de servicio AT).
> La Biblioteca lista tareas reales del sistema (`MicrosoftEdgeUpdateTaskMachineCore`,
> `GoogleUpdateTaskMachineCore`, `OneDrive Reporting`, `OneDrive Backup`, etc.) con
> columnas Estado/Desencadenadores/Hora próxima ejecución/Hora última ejecución/
> Resultados.

> [!info] Captura del profesor: pestaña por pestaña — ventana "Crear tarea"
> Ejemplo real usado en el PDF: una tarea llamada **EJEMPLO** para reproducir un
> video a ciertas horas.
> - **General**: campos Nombre (`EJEMPLO`), Ubicación (`\`), Autor
>   (`DIRTIC\SISTEMAS`), Descripción (`TAREAS EJEMPLO PARA EJECUTAR UN VIDEO A
>   CIERTAS HORAS DEL DÍA`); radios "Ejecutar solo cuando el usuario haya
>   iniciado sesión" / "Ejecutar tanto si el usuario inició sesión como si no";
>   checkbox "Ejecutar con los privilegios más altos"; dropdown "Configurar
>   para: Windows Vista™, Windows Server™ 2008".
> - **Desencadenadores**: lista vacía + botones Nuevo/Editar/Eliminar. La
>   ventana "Nuevo desencadenador" muestra dropdown "Iniciar la tarea" con
>   opciones **Según una programación, Al iniciar la sesión, Al iniciar el
>   sistema, Al estar inactivo, Al producirse un evento, Al crear o modificar
>   tarea, Al conectarse a una sesión de usuario, Al desconectarse de una
>   sesión de usuario, Al bloquearse/desbloquearse la estación de trabajo**.
>   Con "Según una programación" elegido: radios Una vez/Diariamente/
>   **Semanalmente**/Mensualmente — el ejemplo semanal muestra Inicio
>   `21/02/2024 9:00:00 a.m.`, "Repetir cada: 1 semanas en:" con los 7 días de
>   la semana marcados. Sección "Configuración avanzada": Retraso máx.
>   (retraso aleatorio), Repetir cada 1 hora durante 1 día, Detener tarea si
>   se ejecuta más de 3 días, Expiración, checkbox Habilitado.
> - **Acciones**: dropdown "Acción" con **Iniciar un programa / Enviar un
>   correo electrónico (desusado) / Mostrar un mensaje (desusado)**. Ejemplo
>   real de "Programa o script": `"D:\Instalación NVMe.mp4"` (campos
>   Agregar argumentos / Iniciar en, ambos opcionales).
> - **Condiciones**: sección "Inactivo" (iniciar solo si el equipo está
>   inactivo X minutos, detener si deja de estar inactivo, reiniciar si se
>   reanuda inactividad); sección "Energía" (iniciar solo con corriente
>   alterna ✓, detener si empieza a usar batería ✓, activar el equipo para
>   ejecutar esta tarea ✓); sección "Red" (iniciar solo si hay conexión de
>   red disponible, dropdown "Cualquier conexión").
> - **Configuración**: checkboxes Permitir que la tarea se ejecute a
>   petición ✓, Ejecutar tarea lo antes posible si no hubo inicio programado,
>   Si la tarea no se ejecuta reiniciarla cada 1 minuto (máx. 3 veces),
>   Detener la tarea si se ejecuta más de 3 días, Detener tarea en ejecución
>   si no finaliza cuando se solicite, Eliminar tareas no reprogramadas
>   después de 30 días; dropdown "Aplicar la siguiente regla si la tarea ya
>   está en ejecución": **Ejecutar una instancia nueva en paralelo**.
>
> Tras Aceptar, la tarea EJEMPLO aparece en la Biblioteca con su próxima
> ejecución calculada ("A las 9:00 a. m. cada Domingo, Martes, Miércoles...").
> El PDF cierra recordando `schtasks /query /tn "NombreDeLaTarea"` y
> `schtasks /delete /tn "NombreDeLaTarea"` para gestionar la tarea por consola.

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
