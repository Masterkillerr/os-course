---
title: "🧠 Fundamentos del SO — Procesos, Memoria y Kernel"
sidebar_title: "🧠 Procesos y Kernel"
order: 21
unit: null
clase: 2
tema: "Procesos, memoria, E/S, sincronización, virtualización y tipos de kernel"
profesor: "Fabián Robles"
tags: [procesos, memoria, sincronización, virtualización, kernel, sistemas-operativos]
prerequisitos: ["Conceptos básicos de sistemas operativos"]
tiempo_clase: null
---

# 🧠 Fundamentos del Sistema Operativo — Procesos, Memoria y Kernel

> [!info] Módulo
> **Clase 2** — Procesos, Memoria y Kernel
> **Tema:** Procesos, memoria, E/S, sincronización, virtualización y tipos de kernel
> **Ver también:** [[09-Fundamentos-del-SO|🧠 Fundamentos del SO]]
>
> [!info] Objetivo
> Conceptos centrales que el SO gestiona en tiempo de ejecución: procesos, memoria, E/S, concurrencia y virtualización, más los tipos de kernel. Base para entender cualquier SO moderno.

> [!tip] Prerrequisitos
> - Conceptos básicos de sistemas operativos
> - [[09-Fundamentos-del-SO|🧠 Fundamentos del SO]] — arquitectura y modos de ejecución

---

## Procesos y Threads

| Concepto | Definición |
|---|---|
| **Proceso** | Programa en ejecución con espacio de memoria aislado y recursos propios asignados por el SO. |
| **Thread (hilo)** | Unidad de ejecución *dentro* de un proceso; los threads comparten memoria y recursos entre sí. |
| **Multiprogramación / multitarea** | Capacidad del SO de mantener varios procesos en memoria y ejecutarlos concurrentemente. |

```mermaid
graph TD
    P1[Proceso A<br/>espacio aislado] --> T1[Thread 1]
    P1 --> T2[Thread 2]
    P2[Proceso B<br/>espacio aislado] --> T3[Thread 1]
    CPU[CPU] -->|planificador| P1
    CPU -->|planificador| P2
```

> [!warning] Multitarea cooperativa vs preventiva
> **Cooperativa:** cada proceso conserva la CPU hasta que la cede (una falla congela el equipo). **Preventiva:** el reloj del sistema interrumpe periódicamente y el SO elige el siguiente proceso (tiempo compartido).

### Colas de planificación

```mermaid
graph TD
    JQ[Cola de trabajos] -->|admisión| RQ[Cola de listos]
    RQ -->|planificador| CPU[CPU]
    CPU -->|E/S| IOW[Cola de espera de E/S]
    IOW -->|E/S lista| RQ
    CPU -->|fin de quantum| RQ
    CPU -->|termina| EXIT([Salida])
```

El SO mueve los procesos entre la **cola de trabajos**, la **cola de listos** (esperando CPU), la **cola de espera de E/S** y la salida según su estado.

### Herramientas de inspección de procesos

> [!info] Del laboratorio (Clase 3)
> El profesor inspecciona el escritorio con **Windows R** (Ejecutar), **Task Manager** y **explorer.exe**.

#### Windows R (Ejecutar)
`Windows R` abre el cuadro **Ejecutar**. Allí puedes lanzar aplicaciones, utilidades oFolderPath:
- `explorer.exe` — el **explorador de archivos**.
- `tarea` / `taskmgr` — el **Administrador de tareas**.
- `msconfig`, `regedit`, `tpm.msc`, `cmd`, `powershell` — utilidades.

#### `explorer.exe`: dos caras
`explorer.exe` es *una sola* aplicación que cumple **dos roles**:
1. **Explorador de archivos** (navegador de carpetas).
2. **Shell del escritorio** (la barra de tareas y el fondo).

> [!warning] Finalizar el explorador cierra el escritorio
> Si "finalizas" `explorer.exe` en el Administrador de tareas, desaparece el escritorio; si lo
> "reinicias" (no finalizas) vuelve. El **modo ventana** de Task Manager está montado sobre él.

#### Task Manager — tres grandes categorías
Task Manager clasifica los procesos en:

| Categoría | Qué muestra |
|-----------|-------------|
| **Aplicaciones** | Programas con ventana (p. ej. Word, Edge). |
| **Procesos en segundo plano** | Servicios y apps sin ventana (98 en el ejemplo). |
| **Procesos de Windows** | Núcleo y componentes críticos del SO (116 en el ejemplo). |

> [!note] Finalizar vs reiniciar
> *Finalizar* un proceso mata la tarea; *reiniciar* cierra y vuelve a abrir (p. ej. el Explorador).

#### Task Manager — el resto de las pestañas (Taller No. 1)

Más allá de Procesos, el Administrador de tareas tiene varias pestañas con valor práctico y de
diagnóstico:

| Pestaña | Qué muestra |
|---|---|
| **Rendimiento** | Gráficas de CPU, Memoria, Memoria auxiliar (HDD/SSD), Ethernet/Wi-Fi y GPU en tiempo real. |
| **Historial de aplicaciones** | Consumo de recursos por aplicación desde una fecha definida — útil, por ejemplo, para saber cuánto tiempo usa un empleado cada app. |
| **Aplicaciones de inicio** (arranque) | Qué programas cargan al iniciar Windows y si están Habilitados/Deshabilitados; permite ver propiedades y abrir la ubicación del archivo. |
| **Usuarios** | Qué usuarios tienen sesión activa, qué procesos ejecuta cada uno y cuántos recursos consume; permite desconectar un usuario. |
| **Detalles** | Todos los procesos con: PID, estado, usuario que lo ejecuta, RAM consumida, arquitectura y una descripción corta. |
| **Servicios** | Listado completo de los servicios del sistema operativo. |

> [!info] Memoria reservada para hardware
> Parte de la RAM se bloquea para el hardware — forma parte de la **VRAM** (memoria compartida
> con la GPU), archivos temporales y caché. Para ver cuánta VRAM usa el controlador de pantalla:
> `Ejecutar → dxdiag.exe`. También se puede ajustar desde BIOS/UEFI o `msconfig` (cantidad máxima
> de memoria).

#### RESMON (Monitor de recursos) y PERFMON (Monitor de rendimiento)

`resmon.exe` da una vista más detallada que Task Manager, en particular de la pestaña **Memoria**:

| Métrica RAM (RESMON) | Significado |
|---|---|
| **En uso** | Consumida por el SO a nivel de kernel/shell y gestión de procesos-hardware. |
| **Modificada** | Datos cambiados desde que se cargaron del disco pero aún no guardados (ej. portapapeles). |
| **En espera** | Datos leídos recientemente del disco que se mantienen en RAM por si se vuelven a pedir (buffer de caché); **no cuenta como "en uso"**, pero mejora el rendimiento — se puede liberar para dejar más RAM libre. |
| **Libre** | RAM sin utilizar. |

`perfmon.exe` (Monitor de rendimiento) es una herramienta adicional y más completa; `perfmon /report`
genera un informe con secciones: Resultados del diagnóstico, Configuración de software/hardware,
CPU, Red, Disco, Memoria y Estadísticas.

> [!tip] Liberar la memoria en espera vía PowerShell
> Termina los 20 procesos que más memoria consumen (⚠️ úsalo con cuidado, cierra procesos activos):
> ```powershell
> Get-Process | Sort-Object -Property WorkingSet64 -Descending | Select-Object -First 20 |
>   ForEach-Object { Start-Process -FilePath 'taskkill.exe' -ArgumentList '/F', '-PID', $_.Id }
> ```
> `taskkill.exe /F /PID <id>` fuerza (`/F`) la terminación de un proceso por su PID.

#### Herramientas de optimización y benchmark

- **Windows PC Manager** (Microsoft) — optimizador oficial: limpieza, salud del sistema,
  aceleración de arranque, todo configurable desde una sola app.
- **Cinebench** — benchmark de estrés de CPU/GPU; útil para observar en vivo cómo suben CPU,
  memoria y GPU en Rendimiento/RESMON bajo carga máxima, y comparar el resultado (puntaje) entre
  equipos.

#### Administrador de tareas del navegador y Service Workers

> [!info] Del Taller No. 1
> La mayoría de navegadores tienen **su propio administrador de tareas**, independiente del de
> Windows, con distinta información: Chrome (`⋮` → Más herramientas → Administrador de tareas)
> muestra CPU, memoria, red y proceso por pestaña; **Firefox es más limitado** (solo CPU y RAM).
> Cada pestaña/extensión de Chrome corre como su propio proceso — se puede ver a qué pestaña
> corresponde cada entrada.

Un **Service Worker** es un script que el navegador ejecuta **en segundo plano**, independiente
de la pestaña que lo registró, para dar capacidades que una página normal no tiene:

- **Gestión de caché** — guarda HTML/CSS/JS/imágenes localmente para cargar más rápido (o
  funcionar offline) en visitas futuras.
- **Notificaciones push** — el sitio puede notificar al usuario aunque no esté abierto.
- **Background sync** — sincroniza datos con el servidor aunque el usuario no esté usando el sitio.
- **Actualizaciones automáticas** — mantiene la app web al día en segundo plano.
- **Trabajo offline** — sirve recursos cacheados con red lenta o sin conexión.

> [!tip] Por qué importa para un ingeniero de sistemas
> Un Service Worker es, en esencia, un **proceso en segundo plano gestionado por el navegador**,
> igual en concepto a un servicio de Windows: consume recursos, corre sin interacción directa del
> usuario, y aparece en el administrador de tareas del navegador — no en el de Windows.

---

## Gestión de memoria

- **RAM:** acceso rápido pero capacidad física limitada.
- **Memoria virtual:** extiende la capacidad usando el disco mediante **paginación**.
- **Paginación:** divide la memoria en páginas que se mueven entre RAM y disco según demanda, permitiendo usar más memoria de la físicamente disponible.
- **Protección:** garantiza el aislamiento entre los espacios de direcciones de distintos procesos.

```mermaid
graph LR
    P[Proceso] -->|páginas| RAM[(RAM: páginas activas)]
    P -->|páginas en disco| DISK[(Disco: paginación)]
    RAM -.->|swap bajo demanda| DISK
```

---

## Entrada/Salida (E/S)

- **Periféricos:** discos, red, impresoras, etc.
- **Controladores de dispositivo:** interfaz de software entre el SO y el hardware específico.
- **Interrupciones:** señal asíncrona que notifica al procesador un evento de E/S.
- **DMA (Direct Memory Access):** transferencia de datos a memoria **sin intervención continua de la CPU**.

```mermaid
graph TD
    CPU[CPU] -->|ordena| CTRL[Controlador de dispositivo]
    CTRL --> DEV[Dispositivo periférico]
    DEV -->|interrupción| CPU
    DEV -->|DMA directo| MEM[(Memoria)]
```

---

## Sincronización y concurrencia

- **Condición de carrera:** acceso simultáneo a un recurso compartido genera inconsistencias.
- **Mutex:** exclusión mutua (un solo hilo a la vez en la sección crítica).
- **Semáforos / monitores:** coordinan el acceso exclusivo a secciones críticas.
- **Deadlock (interbloqueo):** procesos se bloquean mutuamente esperando recursos que el otro retiene.

```mermaid
graph TD
    P1[Proceso 1<br/>tiene Recurso A] -->|espera Recurso B| P2[Proceso 2<br/>tiene Recurso B]
    P2 -->|espera Recurso A| P1
    style P1 fill:#ff6b6b
    style P2 fill:#ff6b6b
```

> [!warning] Deadlock
> P1 tiene A y espera B; P2 tiene B y espera A → ninguno avanza. Evítalo con orden de adquisición de recursos o *timeout*.

---

## Virtualización

| Paradigma | Característica |
|---|---|
| **Máquinas virtuales** | Varios SO completos sobre un hardware con aislamiento total. |
| **Contenedores** | Aislamiento ligero de aplicaciones que comparten el kernel del SO anfitrión. |
| **Hipervisores** | Software que gestiona y asigna recursos físicos entre las VMs (Type 1/Type 2). |

```mermaid
graph TD
    H[Hardware] --> HV[Hipervisor]
    HV --> VM1[VM: Windows]
    HV --> VM2[VM: Linux]
    H2[Hardware] --> DOC[Docker / contenedor]
    DOC --> C1[Contenedor A]
    DOC --> C2[Contenedor B]
```

---

## Tipos de kernel

| Tipo | Descripción | Ejemplos |
|---|---|---|
| **Monolítico** | Drivers y extensiones en el espacio central, acceso total al hardware; alto rendimiento. | Linux, DOS, Unix |
| **Micronúcleo** | Servicios en entornos aislados; más estable y fácil de depurar. | QNX, Symbian, Genode |
| **Híbrido** | Combina mono + micro: partes críticas en kernel, servicios en usuario. | Windows, macOS modernos |
| **Nanonúcleo** | Mínimo código en kernel (memoria + IPC). | GNU Hurd |
| **Exonúcleo** | Solo recursos básicos (CPU, memoria física); el resto en bibliotecas de usuario. | Exokernel (MIT) |

```mermaid
graph LR
    M[Monolítico<br/>todo en kernel] -->|menos código en kernel| MI[Micronúcleo<br/>servicios aislados]
    H[Híbrido<br/>equilibrio] --> MI
```

> [!info] Qué se saca del kernel en un micronúcleo
> En el modelo monolítico, el **manejador de interrupciones**, el **planificador de procesos** y el **gestor de memoria** viven en modo kernel. En un **micronúcleo** se mueven al **modo usuario**, porque es el usuario quien los define y administra.

> [!note] ¿En qué lenguaje está escrito Windows?
> Es un híbrido de **C, C++, C# / Visual C++**; el **núcleo es C**. (Para contraste: Java desciende de C++.)

> [!info] Captura del profesor: Monolítico vs MicroKernel, con logos reales (naps.com.mx)
> Dos diagramas lado a lado, cada uno con 3 filas horizontales (de arriba abajo):
>
> **Monolítico** (logos **MS-DOS, Linux (pingüino), Unix, Android** junto al
> título):
> - Fila amarilla **"Procesos (modo usuario)"**: `Compilador` · `Aplicación` · `Navegador`
> - Fila roja **"Núcleo (modo privilegiado)"**, 2 sub-filas: `Comunicación entre
>   procesos` · `Controlador de video` · `Subsistema de red` — y debajo:
>   `Sistema de archivos` · `Planificador de procesos` · `Manejo de
>   interrupciones` · `Memoria virtual`
> - Fila gris **"Hardware"**: `Disco duro` · `Procesador` · `Tarjeta de video`
>   · `Memoria` · `Tarjeta de red`
> - Texto bajo el título: *"La modificación de cualquier componente de un
>   núcleo monolítico implica que sea necesario compilar el núcleo por
>   completo."*
>
> **MicroKernel** (logos **Genode, QNX, Symbian**):
> - Fila amarilla **"Procesos (modo usuario)"**: `Compilador` · `Aplicación` ·
>   `Navegador` (idéntica a la de Monolítico)
> - Fila naranja **"Software de sistema"** (capa que NO existe en el
>   monolítico): `Sistema de archivos` · `Controlador de video` ·
>   `Comunicación entre procesos` · `Subsistema de red`
> - Fila roja **"Núcleo (modo privilegiado)"**, mucho más pequeña: solo
>   `Manejo de interrupciones` · `Planificador de procesos` · `Memoria virtual`
> - Fila gris **"Hardware"**: `Disco duro` · `Tarjeta de video` · `Procesador`
>   · `Memoria` · `Tarjeta de red` (mismos 5 componentes, orden distinto)
>
> **La diferencia clave visual**: en Monolítico, "Sistema de archivos",
> "Controlador de video", "Comunicación entre procesos" y "Subsistema de red"
> están DENTRO de la fila roja (núcleo); en MicroKernel esos mismos 4
> elementos se sacan a su propia fila naranja de "Software de sistema",
> fuera del núcleo — dejando el núcleo con solo 3 elementos.

> [!info] Captura del profesor: los 4 tipos de kernel en un solo diagrama (pchardwarepro.com)
> Cuadrícula 2×2, cada tipo con su propia caja "Kernel" (celeste) y flechas
> hacia/desde una caja "Software" (rosa):
> - **Micronúcleo** (arriba-izq): `Kernel` ↕ `Servers` ↔ `Software`, con
>   doble flecha punteada horizontal etiquetada **"IPC"** entre `Servers` y
>   `Software` — el kernel se comunica con Servers y con Software por
>   separado (flechas verticales), y Servers se comunica con Software vía IPC.
> - **Mononúcleo** (arriba-der): `Kernel` ↕ `Software` directo — sin caja
>   intermedia.
> - **Híbrido** (abajo-izq): una caja `Kernel` que **contiene** una sub-caja
>   `Servers` dentro de sí misma (Servers vive dentro del rectángulo del
>   Kernel), y de ahí baja a `Software`.
> - **Exonúcleo** (abajo-der): `Kernel` ↕ 3 cajas `Library` en paralelo
>   (`Library` · `Library` · `Library`) ↕ `Software` — las bibliotecas
>   median entre kernel y software.
>
> Pie de diapositiva: *"Leer documento COMPLEMENTO — TIPOS DE KERNEL"*.

> [!warning] Para memorizar — riesgo de examen (fill-in-the-blank)
> Si piden dibujar estos 4 de memoria, el detalle que más se confunde es
> **dónde vive la caja intermedia**:
> - Micronúcleo → intermediario = **Servers**, comunicado con Software por
>   **IPC** (flecha doble punteada).
> - Mononúcleo → **sin intermediario**, Kernel habla directo con Software.
> - Híbrido → Servers está **dentro** del Kernel (anidado), no al lado.
> - Exonúcleo → el intermediario son **Libraries** (plural, 3 cajas en
>   paralelo), no un único bloque.

---

## Mono vs Multi (proceso, tarea, usuario)

| Concepto | Mono… | Multi… |
|----------|--------|---------|
| **Monoproceso** | Un solo procesador físico atendiendo | **Multiproceso**: varios núcleos/workloads a la vez |
| **Monotarea** | Ejecuta una sola cosa; no avanza hasta terminar | **Multitarea**: el planificador alterna procesos (tiempo compartido) |
| **Monousuario** | Una sola sesión/persona | **Multiusuario**: varias sesiones abiertas a la vez |

> [!info] Windows es multiusuario
> Aunque en tu equipo eres tú, Windows soporta varias sesiones abiertas. Por eso al apagar a veces avisa: *"hay otro usuario con sesión abierta"*.

### Modos de ejecución: los 4 conceptos con ejemplos reales

> [!info] Captura del profesor: Monoprogramación / Monoprocesamiento / Multiprogramación / Multiprocesamiento
> Diagrama de 4 cajas verdes en cuadrícula 2×2, con flecha horizontal
> Monoprogramación→Monoprocesamiento y Multiprogramación→Multiprocesamiento:
>
> | Concepto | Definición literal de la diapositiva | Ejemplo |
> |---|---|---|
> | **Monoprogramación** | 1 programa en memoria, 1 CPU | MS-DOS |
> | **Monoprocesamiento** | 1 CPU ejecuta 1 o varios programas | Intel 8086 |
> | **Multiprogramación** | Varios programas en memoria, 1 CPU los intercambia | UNIX, Win95 |
> | **Multiprocesamiento** | Varios programas, múltiples CPUs | Intel i7, Servidores |
>
> Bajo "Monoprogramación" el profesor lista sus características: *un solo
> programa en memoria · no existe planificación compleja · no existe cambio
> de contexto · muy bajo aprovechamiento del procesador · gran tiempo ocioso
> de la CPU*.

> [!info] Captura del profesor: la analogía del mesero/restaurante
> Misma cuadrícula 2×2, ahora con dibujos de mesero(s) y mesa(s):
> - **Monoprogramación**: 1 mesero, 1 mesa (1 solo cliente sentado).
> - **Monoprocesamiento**: 1 mesero (marcado "CPU"), pero ahora 2 mesas — el
>   mesero atiende ambas alternando (números 1 y 2 sobre las mesas).
> - **Multiprogramación**: varios meseros, 1 grupo de mesas juntas.
> - **Multiprocesamiento**: varios meseros, varios grupos de mesas separados.

> [!info] Captura del profesor: comparación 50% vs 100% de utilización (P1/P2)
> Dos líneas de tiempo apiladas, la de arriba **sin multiprogramación**: el
> Proceso P1 corre completo (Inicio → Inactivo/Espera ×3 → Fin) y **solo
> cuando P1 termina** arranca P2 ("En espera" ocupa todo el ancho de P1) —
> **Utilización: 50%**. La de abajo **con multiprogramación**: P1 y P2 se
> intercalan con flechas cruzadas verticales entre ambas líneas — cuando uno
> queda "Inactivo; Espera" el otro toma la CPU — **Utilización: 100%**.

---

## 📝 Autoevaluación

```flipcard
**Pregunta 1 — Proceso vs thread**
¿Cuál es la diferencia entre un proceso y un thread?
---
El proceso tiene espacio de memoria aislado y recursos propios; el thread es una unidad de ejecución dentro del proceso y comparte su memoria con los demás threads.
```

```flipcard
**Pregunta 2 — ¿Qué es la paginación?**
¿Para qué sirve la memoria virtual y la paginación?
---
Extienden la memoria disponible usando el disco: la memoria se divide en páginas que se mueven entre RAM y disco según demanda, permitiendo ejecutar procesos mayores que la RAM física.
```

```flipcard
**Pregunta 3 — ¿Qué es un deadlock?**
Dos procesos se bloquean esperando recursos que el otro retiene. ¿Cómo se llama?
---
Deadlock (interbloqueo). Se evita con orden de adquisición de recursos, timeouts o detección.
```

---

## ⚠️ Errores comunes

> [!warning] Error 1: Proceso = thread
> El proceso aísla memoria; el thread la comparte. No son lo mismo.

> [!warning] Error 2: Memoria virtual = RAM
> La memoria virtual usa disco (paginación); no es RAM física. Es más lenta pero más amplia.

> [!warning] Error 3: DMA usa la CPU
> El DMA transfiere datos a memoria sin intervención continua de la CPU; la CPU solo se entera vía interrupción al terminar.

> [!warning] Error 4: Cambiar el nombre de cuenta renombra la carpeta de usuario
> Al instalar Windows se crea la carpeta `C:\Users\<usuario>` con el nombre que diste. Si luego cambias el **nombre de cuenta** en Configuración, la **carpeta NO se renombra**. Renombrar la carpeta a mano rompe rutas y puede dejarte fuera de sesión. El nombre de cuenta, el de la carpeta y el del equipo en red son cosas distintas.

> [!warning] Error 5: EFS es tan seguro como BitLocker
> **EFS** cifra archivos/carpetas de forma individual con una llave **local** ligada a tu cuenta; es menos robusto que **BitLocker** (que cifra el volumen completo usando el TPM). Ver [[03-Arranque-y-Seguridad|🛡️ Arranque y seguridad]].

---

## Referencias

> [!info] Recursos externos
> - [TutorialsPoint — Operating System](https://www.tutorialspoint.com/operating_system/)
> - [Microsoft — Componentes de Windows](https://learn.microsoft.com/en-us/windows-hardware/drivers/kernel/overview-of-windows-components)
