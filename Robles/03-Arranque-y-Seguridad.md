---
next: 01-TPM
prev: 04-Estructuras-de-Datos
title: "🛡️ Arranque y Seguridad"
sidebar_title: "🛡️ Arranque y Seguridad"
order: 80
unit: null
clase: 2
tema: "Arranque y Seguridad (POST, UEFI, Secure Boot, Core Isolation)"
profesor: "Fabián Robles"
tags: [arranque, secure-boot, core-isolation, uefi, bios, clase-2, sistemas-operativos]
prerequisitos: ["TPM", "Sistemas de archivos", "Conceptos de firmware"]
tiempo_clase: "58:49 - 01:47:01"
---

# 🛡️ Arranque y Seguridad

> [!info] Módulo
> **Unidad 2 — Almacenamiento y Arranque**
> **Tema:** Arranque y Seguridad (POST, UEFI, Secure Boot, Core Isolation)
> **Ver también:** [[01-TPM|🔐 TPM]], [[02-Sistemas-de-Archivos|💾 Sistemas de archivos]]

> [!tip] Prerrequisitos
> - TPM (funciones y propósito)
> - Sistemas de archivos (FAT, NTFS)
> - Conceptos de firmware (ROM, BIOS, UEFI)

---

## 📋 Tabla de contenidos

- [[#Secuencia-de-arranque]]
- [[#ROM-BIOS-vs-UEFI]]
- [[#Secure-Boot-—-La-guardería-del-sistema]]
- [[#Aislamiento-de-núcleo-(Core-Isolation)]]
- [[#BitLocker]]
- [[#EFS-—-cifrado-por-archivo-(Encrypting-File-System)]]
- [[#Registro-de-Windows-(regedit)]]
- [[#Contraseñas-cifradas-vs-encriptadas]]
- [[#Malware-clásico-Virus-de-sector-de-arranque]]
- [[#Ataques-DMA-(Direct-Memory-Access)]]
- [[#Ciclo-de-vida-completo-de-una-sesión]]

---

## Secuencia de arranque

```mermaid
graph TD
    A[🔌 Presionar encendido] --> B[📋 POST<br>Power-On Self-Test]
    B --> C[🧠 ROM / BIOS / UEFI<br>Inicializa hardware]
    C --> D[🔒 Secure Boot<br>Verifica firma digital]
    D --> E[🔐 TPM<br>Valida integridad]
    E --> F[📦 Bootloader<br>Carga kernel]
    F --> G[🪟 Kernel<br>Núcleo del SO]
    G --> H[🔧 Servicios / Drivers]
    H --> I[🖥️ Escritorio / GUI]
    
    style E fill:#ff6b6b
    style I fill:#4ecdc4
```

> [!warning] Regla de oro
> Todo se carga en la **RAM** (área de trabajo del procesador). Si la RAM se llena, el sistema se vuelve lento.

> [!info] Captura del profesor: arquitectura y flujo de arranque de Microsoft Pluton
> Fuente: `2 TPM introducción y seguridd del dispositivo.pdf`, diapositiva
> "Flujo de Carga del FIRMWARE". Dos diagramas:
>
> **Diagrama de arquitectura** (dos bloques apilados con doble flecha entre
> ellos):
> - **Bloque de software** (arriba): caja "Sistema operativo Windows"
>   contiene dos sub-cajas lado a lado: `Controladores de Plutón` y
>   `Firmware de Plutón`. Nota al lado: *"Durante el inicio de Windows, se
>   utiliza en su lugar la última versión del firmware de Plutón, si está
>   disponible."*
> - **Bloque de hardware y firmware** (abajo): caja "CPU (sistema en chip)"
>   contiene: `Procesador de seguridad Plutón`, un icono de `CPU Núcleos`, y
>   (resaltado en naranja) `Firmware de Microsoft Plutón`. Nota al lado:
>   *"En el arranque del sistema, el firmware de Microsoft Plutón se carga
>   desde el almacenamiento Flash."*
>
> **Flujo de arranque** (secuencia lineal con una decisión):
> ```
> [Encender] (ícono de power)
>       ↓
> Hardware de Plutón e Inicialización de ROM
>       ↓
> Cargar Firmware de Plutón del almacenamiento flash SPI
>       ↓
> UEFI: Arranque en CPU
>       ↓
> Entrega de UEFI a Boot Manager y winload (cargador del SO)
>       ↓
> ¿Versión actualizada de firmware de Plutón disponible en Windows? (decisión)
>       ├─ Sí → Cargar Firmware Plutón de Windows ──┐
>       └─ No → Usar el firmware de Plutón de flash SPI ─┤
>                                                          ↓
>                                                   Iniciar en Windows
> ```

> [!warning] Para memorizar — orden exacto del flujo Pluton
> El orden es: **Hardware Plutón + ROM → Firmware desde SPI flash → UEFI en
> CPU → Boot Manager/winload → decisión de versión de firmware → Windows**.
> El punto que más se confunde: la decisión ocurre **después** de que UEFI
> entrega el control a winload, no antes — es decir, el sistema ya está
> arrancando Windows cuando decide qué firmware de Plutón usar.

---

## ROM BIOS vs UEFI

```mermaid
graph TD
    subgraph BIOS["BIOS (legacy)"]
        B1[Arranque en modo 16 bits] --> B2[Solo MBR] --> B3[Lento, sin seguridad de arranque]
    end
    subgraph UEFI["UEFI (moderno)"]
        U1[Modo 32/64 bits] --> U2[Soporta GPT + Secure Boot] --> U3[Rápido, interfaz gráfica]
    end
```

| Característica | BIOS | UEFI |
|----------------|------|------|
| Dirección de arranque | `0x7C00` (fija) | Variable (GUID) |
| Particiones | MBR (4 primarias) | GPT (ilimitadas) |
| Tamaño máximo disco | 2 TB | 9.4 ZB |
| Interfaz | Texto | Gráfica + mouse |
| Secure Boot | ❌ No | ✅ Sí |
| Velocidad | Lenta | Rápida |

### MBR vs GPT

```mermaid
graph TD
    subgraph MBR["MBR (legacy)"]
        M1[512 bytes totales] --> M2[4 particiones primarias máx]
        M2 --> M3[Límite 2.2 TB]
    end
    subgraph GPT["GPT (UEFI)"]
        G1[Tabla de particiones redundante] --> G2[Particiones casi ilimitadas]
        G2 --> G3[Soporta discos > 2 TB y sectores 4K]
    end
```

| Característica | MBR | GPT |
|----------------|-----|-----|
| Sector 0 | MBR | GPT Header |
| Tabla | Sectores 1-33 | Sectores 1-33 |
| Particiones | 4 primarias | 128+ |
| Tamaño máximo | 2 TB | 9.4 ZB |

> [!info] Nota
> El TPM debe habilitarse desde ROM BIOS/UEFI antes de instalar el sistema operativo. Si está deshabilitado en firmware, Windows no podrá usarlo.

---

## Secure Boot — La guardería del sistema

> [!example] Analogía del profesor
> **❌ Sin Secure Boot** (años 90): El papá deja al niño en la puerta del colegio y se va. Cualquiera podría llevárselo.
>
> **✅ Con Secure Boot** (hoy): El papá entrega el niño personalmente a la profesora, quien lo acompaña al salón.

```mermaid
graph TD
    A[UEFI] --> B{¿Bootloader<br>tiene firma válida?}
    B -->|NO| C[❌ BLOQUEAR ARRANQUE]
    B -->|SÍ| D[✅ PERMITIR ARRANQUE]
    D --> E[Kernel cargado]
    
    style C fill:#ff6b6b
    style D fill:#4ecdc4
```

> [!warning] Limitación
> Secure Boot protege **solo el arranque**. Una vez en el sistema operativo, el malware puede ejecutarse igual.

---

## Aislamiento de núcleo (Core Isolation)

### Niveles de privilegio (Anillos de protección)

```mermaid
graph TD
    R3[Aplicaciones de usuario<br/>Ring 3] --> R2[Controladores<br/>Ring 2 / 1]
    R2 --> R0[Núcleo del SO / Kernel<br/>Ring 0 — máximo privilegio]
    R0 --> HW[Hardware]
    style R0 fill:#ff6b6b
    style R3 fill:#4ecdc4
```
> El kernel corre en **Ring 0** (acceso total al hardware); las apps en **Ring 3** (sin acceso directo). Una app pide al SO (syscall) para tocar hardware.

### Tipos de hipervisor (virtualización)

```mermaid
graph TD
    subgraph T1["Type 1 — Bare metal"]
        H1[Hipervisor] --> HW1[Hardware]
        H1 --> VM1[VM: Windows]
        H1 --> VM2[VM: Linux]
    end
    subgraph T2["Type 2 — Hosted"]
        SO[SO anfitrión] --> H2[Hipervisor]
        H2 --> VM3[VM: Linux]
        SO --> HW2[Hardware]
    end
```

```mermaid
graph TD
    subgraph RAM["RAM (Área de trabajo)"]
        A[Zona protegida] --> B[Kernel / Núcleo]
        C[Aplicaciones] --> D[Antivirus]
    end
    
    E[Virtualization-Based Security] --> A
    F[Memory Integrity] --> A
    G[Bloqueo de controladores] --> A
    
    style A fill:#ff6b6b
    style C fill:#95a5a6
```

> [!info] ¿Por qué es necesario?
> - El kernel se ejecuta con privilegios máximos.
> - Si un malware infecta el kernel, tiene control total del equipo.
> - Core Isolation usa **VBS (Virtualization-Based Security)** para crear una región especial en RAM donde el kernel está protegido de modificaciones.

### Funciones activadas

| Función | Protege contra |
|---------|----------------|
| **Integridad de memoria** | Modificación del kernel en RAM |
| **Protección de excepción** | Corrupción de memoria (buffer overflows) |
| **Bloqueo de controladores** | Drivers maliciosos o vulnerables |

> [!warning] Conflicto común
> En el aula, el profesor mencionó conflictos con VirtualBox cuando estas funciones están activas — el hipervisor necesita acceso directo a memoria.

---
