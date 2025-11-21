# Proyecto: Extensión de Materiales en SAP

## ✅ Descripción

Este proyecto automatiza la extensión de materiales en SAP utilizando:

**SAP GUI Scripting (VBS)** para interactuar con SAP.

**Python (pandas, numpy)** para generar un archivo TXT desde una plantilla Excel y datos temporales.

El objetivo es reducir la intervención manual y garantizar un flujo controlado y repetible.

## ✅ Flujo de Trabajo

1. LeerExcel_CopiarPortapapeles.vbs

   - Abre la plantilla Excel y copia datos al portapapeles.

2. script_tmp.vbs

   - Consulta SAP y genera tmp.xlsx en data/tmp/.

3. Python (txt_writer.py)

   - Combina datos de la plantilla y tmp.xlsx.

   - Aplica reglas de formateo y normalización.

   - Genera archivo TXT delimitado por tabuladores.

4. cargue_sap.vbs

   - Carga el archivo TXT en SAP.

5. kill_excel.py

   - Cierra instancias de Excel.

6. cleanup.py

   - Elimina archivos temporales.

7. logs

   - Copia resultados y logs a carpeta con timestamp.

✅ Diagrama del Flujo

graph TD
A[Plantilla Excel] -->|Leer datos| B[VBS: LeerExcel_CopiarPortapapeles]
B --> C[VBS: script_tmp]
C -->|Genera tmp.xlsx| D[Python: txt_writer]
D -->|Genera archivo TXT| E[VBS: cargue_sap]
E --> F[Python: kill_excel]
F --> G[Python: cleanup]
G --> H[logs con timestamp]

✅ Estructura del Proyecto

ExtensionMateriales/
├─ ExtensionMateriales.exe
├─ config/
│ └─ config.json
├─ data/
│ └─ templates/
│ └─ Plantilla Extension Materiales.xlsx
├─ scripts/
│ ├─ LeerExcel_CopiarPortapapeles.vbs
│ ├─ script_tmp.vbs
│ ├─ cargue_sap.vbs
├─ logs/ (generado automáticamente)

✅ Instrucciones de Ejecución

Opción 1: Ejecutable (.exe)

    Coloque la plantilla actualizada en:

    data/templates/Plantilla Extension Materiales.xlsx

    Ejecute el programa:

    Doble clic en ExtensionMateriales.exe.

El flujo:

Copia datos al portapapeles (VBS).

    Genera tmp.xlsx desde SAP (VBS).

    Crea archivo TXT para cargue (Python).

    Ejecuta cargue en SAP (VBS).

    Cierra Excel y limpia temporales.

Resultados:

Se guardan en logs/YYYYMMDD_HHMMSS/.

Incluye: archivo_cargue.txt, app.log, log_materiales_no_encontrados.csv.

Opción 2: Proyecto con Python

Activar entorno virtual:

call venv\Scripts\activate

Ejecutar flujo:

python -m src.app.main

Desactivar entorno:

call venv\Scripts\deactivate.bat

✅ Requisitos

SAP GUI Scripting habilitado.

Python 3.10+ (si se usa modo desarrollo).

Librerías: pandas, numpy, openpyxl, pyinstaller.

✅ Notas Importantes

No mueva ni renombre carpetas (config/, data/, scripts/).

Si falta la plantilla, el programa mostrará un error indicando la ruta esperada.

Para cambiar la plantilla, solo reemplácela en data/templates/.
