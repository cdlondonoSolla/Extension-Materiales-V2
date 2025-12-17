
@echo off
setlocal ENABLEEXTENSIONS

REM ============================================================
REM Compila el proyecto en un .exe usando PyInstaller (Windows)
REM Filosofía:
REM - NO empaqueta la plantilla Excel (usuario la actualiza)
REM - Incluye config.json y scripts VBS
REM ============================================================

REM Ubicar el script en su carpeta raíz
pushd "%~dp0"
set "PROJECT_ROOT=%CD%"
set "APP_NAME=ExtensionMateriales"
set "ENTRYPOINT=src\app\main.py"

echo [1/7] Activando entorno virtual...
IF EXIST "%PROJECT_ROOT%\venv\Scripts\activate.bat" (
    call "%PROJECT_ROOT%\venv\Scripts\activate.bat"
) ELSE (
    echo [ERROR] No se encontro %PROJECT_ROOT%\venv\Scripts\activate.bat
    echo Cree el entorno: python -m venv venv
    goto :end
)

echo [2/7] Limpiando compilaciones previas...
IF EXIST "%PROJECT_ROOT%\build" rmdir /S /Q "%PROJECT_ROOT%\build"
IF EXIST "%PROJECT_ROOT%\dist" rmdir /S /Q "%PROJECT_ROOT%\dist"
IF EXIST "%PROJECT_ROOT%\%APP_NAME%.spec" del /Q "%PROJECT_ROOT%\%APP_NAME%.spec" 2>nul

echo [3/7] Compilando con PyInstaller...
pyinstaller --clean --noconfirm ^
  --name "%APP_NAME%" ^
  --onefile ^
  --console ^
  --collect-submodules pandas ^
  --collect-submodules numpy ^
  --paths "%PROJECT_ROOT%\src" ^
  --add-data "config;config" ^
  --add-data "scripts;scripts" ^
  "%ENTRYPOINT%"

IF ERRORLEVEL 1 (
  echo [ERROR] Error durante la compilacion. Revisar mensajes arriba.
  goto :deactivate
)

echo [4/7] Verificando ejecutable...
IF NOT EXIST "%PROJECT_ROOT%\dist\%APP_NAME%.exe" (
  echo [ERROR] No se encontro el ejecutable en dist. Abortando.
  goto :deactivate
)

echo [5/7] Copiando README y requirements opcionales...
IF EXIST "%PROJECT_ROOT%\README.txt" (
  copy /Y "%PROJECT_ROOT%\README.txt" "%PROJECT_ROOT%\dist\" >nul
)
IF EXIST "%PROJECT_ROOT%\requirements.txt" (
  copy /Y "%PROJECT_ROOT%\requirements.txt" "%PROJECT_ROOT%\dist\" >nul
)

echo [6/7] Ejecutable generado:
echo   "%PROJECT_ROOT%\dist\%APP_NAME%.exe"

echo [7/7] Desactivando entorno virtual...
:deactivate
IF EXIST "%PROJECT_ROOT%\venv\Scripts\deactivate.bat" (
  call "%PROJECT_ROOT%\venv\Scripts\deactivate.bat" 2>nul
)

:end
echo Build completo. Presionaecho Build completo. Presiona una tecla para abrir la carpeta dist...
pause
start "" "%PROJECT_ROOT%\dist"
popd
