# Release v1.0.0 — 2025-12-17

- **Resumen:** Versión inicial estable que consolida utilidades para lectura y procesamiento de materiales desde Excel, generación de logs y scripts de integración con SAP.
- **Destacado:** Mejora en la robustez del procesamiento y en la trazabilidad de errores.

## Nuevas funcionalidades
- **Lectura Excel:** Soporte mejorado para distintos formatos de entradas, en [src/app/io/excel_reader.py](src/app/io/excel_reader.py).
- **Salida TXT y logs:** Escritura estandarizada de salidas y logs en [src/app/io/txt_writer.py](src/app/io/txt_writer.py) y carpeta `data/`.
- **Tareas automatizadas:** Nuevas tareas de limpieza y gestión de procesos en [src/app/tasks](src/app/tasks).
- **Scripts de integración:** Añadido/actualizado el script VBScript para copiar portapapeles desde Excel: [scripts/LeerExcel_CopiarPortapapeles.vbs](scripts/LeerExcel_CopiarPortapapeles.vbs).

## Correcciones
- **Manejo de errores:** Mejoras en excepciones y mensajes más claros en [src/app/utils/exceptions.py](src/app/utils/exceptions.py).
- **Estabilidad:** Evita bloqueos al cerrar Excel mediante la tarea `kill_excel` en [src/app/tasks/kill_excel.py](src/app/tasks/kill_excel.py).
- **Formatos de salida:** Corrección en formato de archivos de carga y logs para compatibilidad con SAP.

## Cambios y notas de migración
- **Dependencias:** Verificar e instalar paquetes en [requirements.txt](requirements.txt) antes de actualizar.
- **Configuración:** Revisar [config/config.json](config/config.json) para rutas y parámetros; puede requerir ajustes si se migra desde una versión previa.
- **Compatibilidad:** No se esperan breaking changes con flujos existentes, pero se recomienda probar en entorno de staging.

## Archivos relevantes
- **Entrada principal:** [src/app/main.py](src/app/main.py)
- **Documentación:** [README.md](README.md)
- **Dependencias:** [requirements.txt](requirements.txt)
- **Scripts útiles:** [scripts/LeerExcel_CopiarPortapapeles.vbs](scripts/LeerExcel_CopiarPortapapeles.vbs)

## Cómo probar / actualizar
- Instalar dependencias:

  - Revisar y ejecutar:

```bash
pip install -r requirements.txt
```

- Ejecutar pipeline principal desde [src/app/main.py](src/app/main.py) o usar `run_pipeline.bat` en Windows.
- Revisar logs generados en `logs/` para verificar operaciones y errores.

## Contacto / Soporte
- Reportar errores y solicitudes en el repositorio o contactar al equipo responsable del proyecto.
