@echo off
REM ============================================================
REM Compila el proyecto en un .exe usando PyInstaller (Windows)
REM Nueva filosofía:
REM - NO empaqueta la plantilla Excel (usuario la actualiza)
REM - Incluye config.json y scripts VBS
REM ============================================================

setlocal
set PROJECT_ROOT=%~dp0
set APP_NAME=ExtensionMateriales
set ENTRYPOINT=src\app\main.py

echo [1/6] Activando entorno virtual...
call "%PROJECT_ROOT%venv\Scripts\activate"

echo [2/6] Limpiando compilaciones previas...
rmdir /S /Q "%PROJECT_ROOT%build" 2>nul
rmdir /S /Q "%PROJECT_ROOT%dist" 2>nul
del /Q "%PROJECT_ROOT%%APP_NAME%.spec" 2>nul

echo [3/6] Compilando con PyInstaller...
pyinstaller --clean --noconfirm ^
  --name "%APP_NAME%" ^
  --onefile ^
  --console ^
  --collect-submodules pandas ^
  --collect-submodules numpy ^
  --add-data "config;config" ^
  --add-data "scripts;scripts" ^
  "%ENTRYPOINT%"

IF %ERRORLEVEL% NEQ 0 (
  echo Error durante la compilación (%ERRORLEVEL%). Revisar mensajes arriba.
  goto :deactivate
)

echo [4/6] Copiando README y requirements opcionales...
IF EXIST "%PROJECT_ROOT%README.txt" copy "%PROJECT_ROOT%README.txt" "%PROJECT_ROOT%dist\" >nul
IF EXIST "%PROJECT_ROOT%requirements.txt" copy "%PROJECT_ROOT%requirements.txt" "%PROJECT_ROOT%dist\" >nul

echo [5/6] Ejecutable generado:
echo   %PROJECT_ROOT%dist\%APP_NAME%.exe

echo [6/6] Desactivando entorno virtual...
:deactivate
call "%PROJECT_ROOT%venv\Scripts\deactivate.bat" 2>nul

echo Listo. Presiona una tecla para abrir la carpeta dist...
pause
start "" "%PROJECT_ROOT%dist"
endlocal