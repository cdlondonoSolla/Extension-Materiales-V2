@echo off
REM Activar el entorno virtual y ejecutar el pipeline
echo Activando entorno virtual...
call venv\Scripts\activate

echo Ejecutando flujo principal...
python -m src.app.main


call venv\Scripts\deactivate.bat
echo Entorno virtual desactivado.
echo Proceso finalizado. Código de salida: %ERRORLEVEL%
exit