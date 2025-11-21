Proyecto: Extensión de Materiales en SAP

✅ Descripción

Este proyecto automatiza la extensión de materiales en SAP utilizando:

SAP GUI Scripting (VBS) para interactuar con SAP.

Python (pandas, numpy) para generar un archivo TXT desde una plantilla Excel y datos temporales.

El objetivo es reducir la intervención manual y garantizar un flujo controlado y repetible.

✅ Flujo de Trabajo

LeerExcel_CopiarPortapapeles.vbs

Abre la plantilla Excel y copia datos al portapapeles.

script_tmp.vbs

Consulta SAP y genera tmp.xlsx en data/tmp/.

Python (txt_writer.py)

Combina datos de la plantilla y tmp.xlsx.

Aplica reglas de formateo y normalización.

Genera archivo TXT delimitado por tabuladores.

cargue_sap.vbs

Carga el archivo TXT en SAP.

kill_excel.py

Cierra instancias de Excel.

cleanup.py

Elimina archivos temporales.

logs

Copia resultados y logs a carpeta con timestamp.

✅ Diagrama del Flujo

1 graph TD

2 A[Plantilla Excel] -->|Leer datos| B[VBS: LeerExcel_CopiarPortapapeles]

3 B --> C[VBS: script_tmp]

4 C -->|Genera tmp.xlsx| D[Python: txt_writer]

5 D -->|Genera archivo TXT| E[VBS: cargue_sap]

6 E --> F[Python: kill_excel]

7 F --> G[Python: cleanup]

8 G --> H[logs con timestamp]

9

✅ Estructura del Proyecto

1 ExtensionMateriales/

2 ├─ ExtensionMateriales.exe

3 ├─ config/

4 │ └─ config.json

5 ├─ data/

6 │ └─ templates/

7 │ └─ Plantilla Extension Materiales.xlsx

8 ├─ scripts/

9 │ ├─ LeerExcel_CopiarPortapapeles.vbs

10 │ ├─ script_tmp.vbs

11 │ ├─ cargue_sap.vbs

12 ├─ logs/ (generado automáticamente)

13

✅ Instrucciones de Ejecución

Opción 1: Ejecutable (.exe)

Coloque la plantilla actualizada en:

1 data/templates/Plantilla Extension Materiales.xlsx

2

Ejecute el programa:

Doble clic en ExtensionMateriales.exe.

O desde CMD:

1 ExtensionMateriales.exe

2

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

1 call venv\Scripts\activate

2

Ejecutar flujo:

1 python -m src.app.main

2

Desactivar entorno:

1 call venv\Scripts\deactivate.bat

2

✅ Requisitos

SAP GUI Scripting habilitado.

Python 3.10+ (si se usa modo desarrollo).

Librerías: pandas, numpy, openpyxl, pyinstaller.

✅ Notas Importantes

No mueva ni renombre carpetas (config/, data/, scripts/).

Si falta la plantilla, el programa mostrará un error indicando la ruta esperada.

Para cambiar la plantilla, solo reemplácela en data/templates/.
