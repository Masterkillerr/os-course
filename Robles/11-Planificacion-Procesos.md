---
next: 10-Android-Dalvik
prev: 09b-Procesos-Memoria-Kernel
title: "📅 Planificación de Procesos — Ejercicios Gantt"
sidebar_title: "📅 Planificación (Gantt)"
order: 40
unit: null
clase: 2
tema: "Ejercicios de planificación: monoprogramado, multiprogramación, quantum, multiproceso"
profesor: "Fabián Robles"
tags: [planificacion, gantt, monoprogramacion, multiprogramacion, quantum, multiproceso, sistemas-operativos]
prerequisitos: ["Fundamentos del SO", "Mono vs Multi (proceso, tarea, usuario)"]
tiempo_clase: null
---

# 📅 Planificación de Procesos — Ejercicios Gantt

> [!info] Módulo
> **Clase 2** — Ejercicios de Planificación de CPU
> **Tema:** Ejercicios prácticos de planificación de CPU, con diagramas tipo Gantt de 32 unidades de tiempo
> **Ver también:** [[09-Fundamentos-del-SO|🧠 Fundamentos del SO]]

> [!warning] Formato de examen probable
> El profesor usa exactamente este formato de tabla en sus diapositivas — Jobs/I-O
> por proceso, una fila por proceso, 32 columnas de tiempo, colores por estado —
> y una de las diapositivas (Multiprocesamiento) queda **sin resolver**, como
> plantilla en blanco. Es razonable esperar que un examen pida completar una
> tabla igual a esta a mano. La sección final de esta nota explica el método
> paso a paso para resolverla.

---

## 📋 Tabla de contenidos

- [[#El formato de la tabla]]
- [[#Monoprogramado-Monotarea]]
- [[#Multiprogramación-Multitarea]]
- [[#Multiprogramación-con-otro-color-(ejemplo-2)]]
- [[#Multiprogramación-con-Quantum]]
- [[#Multiproceso-(1-core,-4-hilos)]]
- [[#Multiprocesamiento-—-plantilla-en-blanco]]
- [[#Método-para-resolver-cualquier-ejercicio-de-este-tipo]]

---

## El formato de la tabla

Todos los ejercicios comparten la misma estructura:

- Columna **Jobs**: número de "trabajos" (unidades de CPU) que pide el proceso.
- Columna **I/O**: número de operaciones de entrada/salida que hace el proceso.
- Una fila por **Proceso** (A, B, C, D…).
- Una fila **TOTAL** que suma Jobs y I/O de todos los procesos.
- Una cuadrícula de **32 columnas** ("Execution A-B-C-D/IO"), numeradas 1-32,
  representando unidades de tiempo discretas.
- Celdas coloreadas: **verde** = CPU ejecutando Jobs de ese proceso, **amarillo**
  = ese proceso haciendo I/O, **naranja** (solo en el ejercicio con Quantum) =
  tiempo perdido en cambio de contexto.
- Debajo: **T.E.** (Tiempo Efectivo, %) y **T.O.** (Tiempo Ocioso, %), con la
  fórmula literal del profesor: *"Tiempo de trabajo 'Verdes - Jobs' / Tiempo
  total (real) 'Todo Execute'/'Todo Jobs+I/O' de ejecución"*.

---

## Monoprogramado-Monotarea

> [!info] Captura del profesor: ejercicio resuelto (versión 1, sin T.E./T.O.)
> Tabla con 4 procesos, cada uno ejecuta **secuencialmente** (uno termina del
> todo antes de que empiece el siguiente) — sin solaparse nunca en el tiempo:
>
> | Proceso | Jobs | I/O | Detalle |
> |---|---|---|---|
> | A | 5 | 3 | 5 jobs-3 I/O |
> | B | 7 | 1 | 7 jobs-1 I/O |
> | C | 5 | 3 | 6 jobs-3 I/O *(texto de la diapositiva, aunque Jobs dice 5)* |
> | D | 5 | 3 | 5 jobs-3 I/O |
> | **TOTAL** | **22** | **10** | |
>
> Bloques de ejecución en la cuadrícula: A ocupa 1-8, B ocupa 9-16, C ocupa
> 17-24, D ocupa 25-32 — cada bloque intercala verde (jobs) y amarillo (I/O)
> según su propio patrón, pero nunca se solapa con el bloque de otro proceso.
> Preguntas planteadas (sin resolver en esta diapositiva): *"¿Cuánto es el
> tiempo efectivo del procesador?" · "¿Qué tipo de procesador sería el
> reflejado a partir de este gráfico?" · "¿Actualmente se tiene en los
> sistemas operativos modernos algo que funcione de esta manera?"*

> [!info] Captura del profesor: mismo ejercicio, versión 2 (CON T.E./T.O. resueltos)
> Repite la tabla (D ahora es **4 jobs-4 I/O**, total **21/11**) y añade el
> cálculo:
> - **T.E. = 65,6%** → `21/32 = 0,65625`
> - **T.O. = 34,4%** → `65,6%` *(texto literal de la diapositiva — nótese que
>   el profesor escribe el mismo 65,6% en la celda de T.O., aparenta ser un
>   error de copiado/pegado en la plantilla original; el T.O. real debería
>   ser 100% − 65,6% = 34,4%, que es el número a la izquierda)*
>
> Debajo, una **"Uniprogramming problem"** variante: Process B cambia a
> **6 jobs-0 I/O** (antes 7 jobs-1 I/O) y su bloque de ejecución (columnas
> 9-16) se resalta completo en **rojo** con un marco rojo alrededor de todo
> el resto de la tabla — total baja a **20/10**, T.E. = **62,5%** (`20/32`),
> T.O. = **37,5%**.

---

## Multiprogramación-Multitarea

> [!info] Captura del profesor: multiprogramación, ejemplo 1
> Misma tabla de 4 procesos (A: 5-3, B: 7-1, C: 6-3, D: 5-3, total 23/10),
> pero ahora **los bloques de ejecución SÍ se solapan/intercalan** en el
> tiempo — a diferencia de monoprogramado. Dos variantes en la misma
> diapositiva:
> - Arriba: **T.E. = 100,0%**, `21/23 = 1`, T.O. = 0,0%
> - Abajo (B cambia a 7 jobs-1 I/O): **T.E. = 91,0%**, `21/23 = 1`, T.O. = 0,0%
>
> *(Nota: los dos T.O. de 0,0% con T.E. distinto de 100% son inconsistentes en
> la diapositiva original — probablemente una celda sin actualizar en la
> plantilla del profesor; no asumas que T.O. = 0% es la regla general.)*

## Multiprogramación con otro color (ejemplo 2)

> [!info] Captura del profesor: "EJERCICIOS DE MULTI — otro color"
> Mismo formato pero con paleta magenta/azul en vez de verde/amarillo (para
> distinguirlo visualmente del ejercicio anterior). Tabla: A: 5 Jobs-7 I/O,
> B: 7 Jobs-6 I/O, C: 6 Jobs-6 I/O *(fila dice "4 jobs-4 I/O" en la columna
> Jobs/IO pero el detalle dice "6 jobs-6 I/O")*, D: 4 Jobs-8 I/O — total
> **19/21**. **T.E. = 83%** (`19/22 = 0,8636364`), **T.O. = 13,6%** (con
> "86,4%" repetido a la derecha, mismo patrón de inconsistencia de celda que
> el ejercicio anterior). Segunda tabla idéntica en la misma diapositiva con
> D cambiado a "3 Jobs - 4 I/O", mismos totales y resultado.

---

## Multiprogramación con Quantum

> [!info] Captura del profesor: multiprogramación con Quantum de 2 unidades
> Nota del profesor en la diapositiva: *"ALGO MÁS REAL A LO QUE TENEMOS EN LA
> ACTUALIDAD EN EL USO DE LA CPU — SE DEFINE COMO EL TIEMPO DE USO DEL
> PROCESADOR EN UN QUANTUM DE TIEMPO, para nuestros ejercicios de 2 Unidades.
> Los cuadros de color NARANJA son el tiempo que se gasta en el cambio de
> contexto de la CPU."*
>
> Introduce un **tercer color, naranja**, intercalado entre bloques verdes:
> cada vez que el planificador cambia de proceso (cada 2 unidades = 1
> quantum), se "pierde" una celda naranja de cambio de contexto.
>
> - Ejemplo 1 (3 procesos A/B/C): total **12 Jobs / 2 I/O**. **T.E. = 66,7%**
>   (`12/18 = 0,6666667`), **T.O. = 33,3%** (`66,7%` repetido, mismo patrón
>   de celda).
> - Ejemplo 2 (4 procesos A/B/C/D): total **14 Jobs / 4 I/O**. **T.E. = 63,6%**
>   (`14/22 = 0,6363636`), **T.O. = 36,4%** (`63,6%` repetido).
>
> **Efecto del quantum**: el T.E. baja respecto a multiprogramación sin
> quantum (100%/91% arriba vs 66,7%/63,6% aquí) porque cada cambio de
> contexto naranja cuenta como tiempo NO efectivo (no es Job ni I/O útil).

---

## Multiproceso (1 core, 4 hilos)

> [!info] Captura del profesor: "Para comprender mejor... los Hilos con un buen planificador siempre respetan el hilo al proceso asociado"
> Escenario: **1 CORE, 4 HILOS** — cada uno de los 4 procesos (A/B/C/D, con
> sus mismos Jobs/I-O: 5-3, 7-1, 6-3, 5-3, total 23/10) se asigna a su propio
> **THREAD** (Thread 1 = Process A, Thread 2 = Process B, Thread 3 = Process
> C, Thread 4 = Process D), coloreado igual que su proceso (verde/celeste/
> azul/rojo).
>
> La tabla tiene columnas **CPU 1 a CPU 8** (los "ciclos de CPU" del core,
> no 8 cores físicos) más un **CLOCK**, y filas separadas por **I/O CANAL 1-4**
> (uno por proceso, en amarillo) debajo de los 4 threads.
>
> Ejecución real mostrada, columna por columna (CPU 1-9; CPU 10-15 vacías):
>
> | CPU | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
> |---|---|---|---|---|---|---|---|---|---|
> | Thread 1 (A, verde) | A1 | A2 | | | | *(naranja)* | A3 | A4 | A5 |
> | Thread 2 (B, celeste) | | B1 | B2 | | *(naranja)* | B3 | B4 | B5 | B6 |
> | Thread 3 (C, azul) | | | C1 | | | | C2 | C3 | C4 |
> | Thread 4 (D, rojo) | | | D1 | | | | D2 | D3 | |
>
> (B7 y C5/C6 caen fuera de esta tabla de 9 columnas, más a la derecha en la
> diapositiva — el patrón se mantiene: cada thread retoma justo donde
> quedó, con una celda naranja de cambio de contexto cada vez que el core
> pasa de un thread a otro.)
>
> - **I/O CANAL 1** (para A): `A1 A2 A3` — **I/O CANAL 2** (para B): `B1` —
>   **I/O CANAL 3** (para C): `C1 C2 C3` — **I/O CANAL 4** (para D): `D1 D2 D3`
> - Nótese que los 4 canales de I/O corren **en columnas distintas entre sí**
>   (canal 1 usa CPU 3-5, canal 3 usa CPU 3-5 también pero es un canal físico
>   distinto — los canales de I/O SÍ pueden solaparse entre sí, a diferencia
>   del CPU que es un único recurso compartido).
>
> Pie de diapositiva: *"El cuadro naranja significa el cambio de contexto"*.
>
> **Idea clave del ejercicio**: aunque hay 4 hilos "corriendo", solo hay
> **1 core físico** — la tabla de 8 "CPU" columnas son ciclos de tiempo del
> mismo core, no 8 procesadores. Cada hilo mantiene su afinidad a su proceso
> (Thread 1 siempre ejecuta bloques de A, nunca de B/C/D).

---

## Multiprocesamiento — plantilla en blanco

> [!warning] Posible formato de examen — esta diapositiva NO está resuelta
> El profesor deja esta tabla **completamente vacía** (sin ninguna celda
> coloreada, sin T.E./T.O. calculados) — es la plantilla más probable para
> una pregunta de examen tipo "complete el diagrama":
>
> | Proceso | Jobs | I/O | Detalle |
> |---|---|---|---|
> | A | 5 | 3 | 5 Jobs - 3 I/O |
> | B | 6 | 4 | 6 Jobs - 4 I/O |
> | C | 3 | 3 | 3 Jobs - 3 I/O |
> | D | 9 | 2 | 9 Jobs - 2 I/O |
> | **TOTAL** | **23** | **12** | |
>
> Cuadrícula vacía de 32 columnas, título **"Multiprogramming"** sobre la
> cuadrícula, filas T.E./T.O. presentes pero sin valores. A diferencia de los
> ejercicios anteriores (donde los procesos comparten 1 CPU secuencial o con
> quantum), el título "EJERCICIOS DE MULTIPROCESAMIENTO" sugiere que este es
> el caso de **múltiples CPUs físicos** — pero la tabla en sí no indica
> cuántos CPUs hay, así que probablemente esa restricción se da oralmente en
> clase o en el enunciado del examen. **Ver la sección siguiente para el
> método de resolución.**

---

## Método para resolver cualquier ejercicio de este tipo

Reconstruido a partir de los patrones en los ejercicios ya resueltos arriba:

1. **Anota Jobs + I/O de cada proceso** en la tabla lateral, y su color
   asignado (verde=A por convención, luego celeste/azul/rojo o similar).
2. **Decide el modelo de ejecución** que pide el enunciado:
   - *Monoprogramado*: un proceso corre COMPLETO (todos sus Jobs y su I/O
     intercalados) antes de que empiece el siguiente. Bloques nunca se
     solapan en el tiempo.
   - *Multiprogramación*: cuando un proceso entra en I/O (amarillo), la CPU
     **no se queda ociosa** — otro proceso listo toma el turno. Los bloques
     de distintos procesos se intercalan en las mismas columnas de tiempo.
   - *Multiprogramación con Quantum*: como multiprogramación, pero el
     planificador solo deja correr cada proceso **2 unidades seguidas**
     (el quantum) antes de forzar un cambio — y cada cambio de proceso cuesta
     **1 celda naranja** de cambio de contexto, que no cuenta como tiempo útil.
   - *Multiproceso (1 core, N hilos)*: cada proceso vive en su propio "carril"
     (thread), pero solo hay 1 CPU física — los threads se turnan igual que
     en quantum, con naranja en cada cambio, y cada I/O va a su propio
     "I/O CANAL" en paralelo (los canales de I/O SÍ pueden trabajar
     simultáneamente entre sí, a diferencia de la CPU).
3. **Rellena la cuadrícula** columna por columna (1→32), coloreando cada
   celda: verde = Job de ese proceso ejecutando en CPU, amarillo = ese
   proceso esperando/haciendo I/O, naranja = cambio de contexto (solo en
   Quantum/Multiproceso).
4. **Cuenta las celdas verdes totales** (= suma de Jobs de todos los
   procesos, dato ya en la fila TOTAL) y el **ancho real usado** de la
   cuadrícula (última columna con contenido).
5. Calcula:
   - **T.E. (Tiempo Efectivo) = Total Jobs (verdes) / Ancho real usado**
   - **T.O. (Tiempo Ocioso) = 1 − T.E.** (como porcentaje)
6. **Verifica la afinidad**: en los ejercicios con hilos/quantum, un proceso
   que empezó a ejecutar en un carril/hilo debe **volver al mismo carril**
   tras su I/O — nunca "salta" a otro proceso.

> [!tip] Atajo para estimar rápido sin dibujar toda la cuadrícula
> Si el modelo es multiprogramación **sin** quantum ni cambios de contexto
> (el caso más simple), el ancho real usado tiende a ser muy cercano al
> total de Jobs (T.E. cerca de 100%) porque casi no hay tiempo perdido — la
> CPU casi nunca está ociosa. En cambio, con Quantum o Multiproceso, cada
> cambio de contexto resta puntos de T.E.: más procesos y quantum más corto
> → más cambios de contexto → T.E. más bajo.

---

## Referencias

> [!info] Recursos externos
> - Documento fuente: *"1 Introducción General.pdf"* (roblestecnologia.com), páginas de ejercicios "EJERCICIOS DE MONOPROGRAMADO/MULTI/MULTIPROCESO"
> - [[09-Fundamentos-del-SO|🧠 Fundamentos del SO]] — conceptos de Mono vs Multi que estos ejercicios aplican
