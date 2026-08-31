---
title: "🛡️ Seguridad Avanzada (BitLocker, EFS, Malware)"
sidebar_title: "🛡️ Seguridad Avanzada"
order: 52
unit: null
clase: 2
tema: "BitLocker, EFS, registro, malware, DMA y VirtualBox"
profesor: "Fabián Robles"
tags: [bitlocker, efs, malware, dma, regedit, virtualbox, clase-2]
prerequisitos: ["Arranque y Seguridad", "TPM", "Sistemas de archivos"]
tiempo_clase: null
---

# 🛡️ Seguridad Avanzada (BitLocker, EFS, Malware)

> [!info] Módulo
> **Unidad 2 — Almacenamiento y Arranque**
> **Tema:** BitLocker, EFS, registro, malware, DMA y VirtualBox
> **Ver también:** [[03-Arranque-y-Seguridad|🛡️ Arranque y seguridad]], [[01-TPM|🔐 TPM]]

---

## BitLocker

```mermaid
graph TD
    A[TPM genera clave maestra] --> B[Guarda clave en chip TPM]
    A --> C[Cifra disco con AES-256]
    C --> D{¿Cambia hardware<br>crítico?}
    D -->|NO| E[Arranque normal]
    D -->|SÍ| F[TPM detecta cambio]
    F --> G[Pide clave de recuperación]
    G --> H[Cuenta Microsoft]
    G --> I[Clave local / USB]
    
    style A fill:#ff6b6b
    style C fill:#4ecdc4
    style F fill:#ffd93d
```

### ¿Dónde se usa contraseña?

| Unidad | Contraseña directa | Clave de recuperación |
|--------|-------------------|----------------------|
| **Sistema (C:)** | ❌ No | ✅ Sí (cuenta Microsoft / TPM) |
| **Datos fijos (D:, E:)** | ✅ Sí | ✅ Sí |
| **USB extraíble** | ✅ Sí | ✅ Sí |

> [!info] ¿Por qué no contraseña en C:?
> Es un problema de huevo y gallina: necesitas acceder al sistema para escribir la contraseña... pero el sistema está en el disco cifrado. Por eso se usa el TPM.

---

## EFS — cifrado por archivo (Encrypting File System)

> [!info] Del laboratorio (Clase 3)
> **EFS** cifra **archivos o carpetas individuales** (no el volumen entero como BitLocker).

| | BitLocker | EFS |
|---|---|---|
| Alcance | Volumen/disco completo | Archivo o carpeta |
| Llave | TPM (VMK/FMK) | **Local**, asociada a tu cuenta |
| Portabilidad | El disco se descifra con el TPM | El archivo lleva su cifrado; en otro equipo: *"no tiene permisos"* |
| Robustez | Alta (hardware + TPM) | Menor — *"tendencia a morir"* |

Para activarlo: `Propiedades` del archivo → `Avanzadas` → **Cifrar contenido para proteger los datos**. El cifrado queda ligado a tu usuario de Windows: si llevas el archivo a la PC de otro, no podrás abrirlo.

> [!warning] EFS ≠ BitLocker
> EFS protege archivos sueltos con una llave local; BitLocker protege todo el volumen usando el TPM. No son intercambiables.

---

## Registro de Windows (`regedit`)

El **Registro** es el *"árbol genealógico de Windows"*: base central de configuración del SO.

> [!tip] Lo que se puede hacer desde el Registro
> - Establecer **políticas de seguridad** (p. ej. que el navegador pida clave al abrir).
> - **Apagar la telemetría**.
> - **Bloquear puertos USB**.
> - Ampliar el **límite de longitud de ruta** de archivos (ver [[02-Sistemas-de-Archivos|💾 Sistemas de archivos]]).

```mermaid
graph TD
    HKCR[HKEY_CLASSES_ROOT] --> HIVES[Hives del registro]
    HKCU[HKEY_CURRENT_USER] --> HIVES
    HKLM[HKEY_LOCAL_MACHINE] --> HIVES
    HU[HKEY_USERS] --> HIVES
    HCV[HKEY_CURRENT_CONFIG] --> HIVES
```

> [!warning] Toca con cuidado
> Un valor mal puesto puede dejar el equipo inutilizable. Mejor practicar en una **máquina virtual**.

---

## Contraseñas: cifradas vs encriptadas

```mermaid
graph LR
    P[Contraseña] --> H["Hash (irreversible)<br/>se guarda solo el resumen"]
    P --> C["Cifrado reversible<br/>se descifra con la llave"]
    style H fill:#45b7d1
    style C fill:#ffd93d
```

> [!warning] Error común
> Si el sistema te muestra tu contraseña anterior, está almacenada de forma reversible → **no es seguro**.
>
> | Tipo | Descripción | Ejemplo |
> |------|-------------|---------|
> | **Cifrado reversible** | Se puede descifrar | ❌ Contraseñas en texto claro o reversible |
> | **Hash irreversible** | No se puede recuperar | ✅ NTLM, bcrypt, SHA-256 |

> El profesor corrigió a un estudiante en clase: las contraseñas deben ser **hasheadas**, no cifradas.

---

## Malware clásico: Virus de sector de arranque

```mermaid
graph TD
    A[Disquete infectado] --> B[BIOS lee sector de arranque]
    B --> C[Virus se carga PRIMERO]
    C --> D[Virus se esconde en RAM]
    D --> E[Sistema operativo se carga]
    E --> F[Virus activo → roba datos]
    
    G[Disquete limpio con antivirus] --> H[Arrancar desde disquete]
    H --> I[Antivirus escanea disco]
    I --> J[Eliminar virus del sector]
    
    style F fill:#ff6b6b
    style J fill:#4ecdc4
```

> [!info] Mitigación moderna
> Secure Boot + TPM detectan si el sector de arranque fue modificado y bloquean la ejecución. Ya no necesitamos disquetes.

---

## Ataques DMA (Direct Memory Access)

```mermaid
graph LR
    subgraph SinDMA["Sin DMA (lento)"]
        A1[Dispositivo] -->|petición| A2[Procesador]
        A2 --> A3[RAM]
    end
    
    subgraph ConDMA["Con DMA (peligroso)"]
        B1[Dispositivo<br>malicioso] --> B2[RAM<br>acceso directo]
    end
    
    style B2 fill:#ff6b6b
```

| Puerto | Riesgo |
|--------|--------|
| 🔴 FireWire (IEEE 1394) | Acceso directo a RAM |
| 🔴 Thunderbolt | Acceso directo a RAM |
| 🔴 PCI Express (sin IOMMU) | Acceso directo a RAM |

> [!warning] Peligro
> Un dispositivo malicioso puede **leer o escribir memoria RAM directamente**, bypasseando el sistema operativo.

---

## Ciclo de vida completo de una sesión

```mermaid
graph LR
    A[🔌 Presionar encendido] --> B[📋 POST]
    B --> C[🧠 ROM/BIOS/UEFI]
    C --> D[🔒 Secure Boot]
    D --> E[🔐 TPM]
    E --> F[📦 Bootloader]
    F --> G[🪟 Kernel]
    G --> H[🔧 Servicios]
    H --> I[🖥️ Escritorio]
    
    J[⚠️ HASTA AQUÍ LLEGA<br>LA SEGURIDAD] --> K[Antivirus]
    K --> L[Usuario]
    L --> M[Aplicaciones]
    
    style E fill:#ff6b6b
    style J fill:#ffd93d
```

> [!info] Importante
> La seguridad se garantiza hasta el paso 6 (kernel cargado). Después de eso, depende del usuario (antivirus, buenas prácticas, actualizaciones).

---

## Instalación en máquina virtual (VirtualBox + Windows 11)

Para practicar sin arriesgar el equipo real, instala Windows 11 dentro de **VirtualBox**. Como el anfitrión puede no tener TPM, Windows permite saltarse las comprobaciones durante el asistente de instalación.

```mermaid
graph TD
    H[Host: Windows / Linux / macOS] --> VB[VirtualBox]
    VB --> VM[Máquina virtual]
    VM --> G[Guest: Windows 11]
    G --> K[Kernel de Linux / Windows]
```

### Saltar la verificación de TPM / RAM / Secure Boot
En el paso de verificación, `SHIFT+F10` abre la consola. En el Registro:
1. `HKEY_LOCAL_MACHINE\System\Setup` → nueva clave **LabConfig**.
2. Dentro, crea tres valores **DWORD de 32 bits** con valor `1`:
   - `BypassTPMCheck`
   - `BypassRAMCheck`
   - `BypassSecureBootCheck`
3. Vuelve al asistente y elige la versión de Windows.

### Saltar la cuenta Microsoft / conexión a Internet
En el paso de red: `SHIFT+F10` → `oobe\bypassnro` (reinicia y permite crear un usuario local sin internet).

> [!warning] Solo para laboratorio
> Estos *bypass* son para prácticas en VM. En equipo real, Windows 11 **requiere** TPM 2.0 y Secure Boot.

---

## 📝 Autoevaluación

<details>
<summary>📦 Abrir preguntas y respuestas</summary>

### Pregunta 1 — Secure Boot
¿Qué es Secure Boot y qué protege?

```mermaid
graph TD
    A[UEFI] --> B{¿Bootloader<br>tiene firma válida?}
    B -->|NO| C[❌ BLOQUEAR ARRANQUE]
    B -->|SÍ| D[✅ PERMITIR ARRANQUE]
    style C fill:#ff6b6b
    style D fill:#4ecdc4
```

> **Respuesta:** Secure Boot verifica la firma digital del bootloader. **Solo protege el arranque**, no el SO cargado.

---

### Pregunta 2 — BitLocker en C:
¿Por qué no se puede poner contraseña directa a la unidad C: en BitLocker?

```
PROBLEMA DEL HUEVO Y LA GALLINA
┌──────────────────────────────────┐
│ ❌ Necesitas acceder a C:       │
│ ❌ Pero C: está cifrada         │
│ ✅ TPM guarda la clave automáticamente │
└──────────────────────────────────┘
```

> **Respuesta:** Es problema de huevo/gallina: accedes al sistema cifrado para escribir la contraseña. Por eso se usa TPM.

---

### Pregunta 3 — Core Isolation
¿Qué es Core Isolation y por qué es necesaria?

| Sin Core Isolation | Con Core Isolation |
|-------------------|-------------------|
| Kernel en RAM expuesto | Kernel en región protegida |
| Malware puede modificarlo | Solo lectura para el resto |

> **Respuesta:** Aísla el kernel en RAM protegida usando virtualización. Protege contra modificaciones por malware.

</details>

---

## 🎯 Próximo paso

> [!info] Continuar con
> **[[04-Estructuras-de-Datos|📊 Estructuras de datos]]** — Ahora entenderás cómo las estructuras de datos (arrays, listas, árboles) son la base de todo lo que vimos en sistemas de archivos y arranque.

---

## ⚠️ Errores comunes

> [!warning] Error 1: Secure Boot = antivirus
> Secure Boot solo verifica el bootloader. No protege contra malware que se ejecuta después del arranque del sistema operativo.

> [!warning] Error 2: DMA es solo para redes
> DMA (Direct Memory Access) permite a dispositivos como FireWire, Thunderbolt o PCIe acceder a la RAM directamente, sin pasar por el procesador. Es un riesgo de seguridad físico.

> [!warning] Error 3: Arranque seguro = sistema limpio
> El arranque seguro garantiza que el bootloader es legítimo. Una vez en el SO, el usuario puede instalar malware igual.

> [!warning] Error 4: TPM = protección total
> TPM protege el arranque y datos en reposo. No protege contra phishing, ingeniería social, o malware en ejecución.

---

## Referencias

> [!info] Recursos externos
> - [Microsoft — Secure Boot](https://learn.microsoft.com/en-us/windows-hardware/drivers/install/secure-boot)
> - [Microsoft — Core Isolation](https://learn.microsoft.com/en-us/windows-hardware/design/device-experiences/windows-defender-application-control/core-isolation)
> - [Microsoft — BitLocker](https://learn.microsoft.com/en-us/windows/security/information-protection/bitlocker)
> - [TCG — TPM Specification](https://trustedcomputinggroup.org/work-groups/trusted-platform-module/)
