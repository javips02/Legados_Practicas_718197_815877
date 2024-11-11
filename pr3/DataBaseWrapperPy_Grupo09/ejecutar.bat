@echo off
setlocal

:: Configuración
set PYTHON_VERSION=3.11.0
set PYTHON_INSTALLER=python-%PYTHON_VERSION%-amd64.exe
set PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/%PYTHON_INSTALLER%

:: Descargar Python si no está instalado
echo Comprobando si python esta instalado ...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python no está instalado. Descargando Python %PYTHON_VERSION%...
    curl -o %PYTHON_INSTALLER% %PYTHON_URL%
    
    echo Instalando Python %PYTHON_VERSION%...
    start /wait %PYTHON_INSTALLER% /quiet PrependPath=1 Include_test=0

    :: Verificar si Python se instaló correctamente
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo Error al instalar Python. Abortando.
        pause
        exit /b 1
    )
)

set REQ_PATH=.\practica3
:: Ruta donde se creará el entorno virtual
set VENV_PATH=.\env
:: Ruta al pip del entorno virtual
set PIP="%VENV_PATH%\Scripts\pip.exe"

:: Crear el entorno virtual
echo Creando entorno virtual en %VENV_PATH% ...
python -m venv "%VENV_PATH%"

:: Activar el entorno virtual
call "%VENV_PATH%\Scripts\activate.bat"

:: Instalar las dependencias de tu aplicación 
echo Instalando dependencias ...
%PIP% install -r "requirements.txt"  > nul 2>&1

:: Ejecutar la aplicación Flask y esperar a que termine 
cd app
echo Lanzando aplicación ...
python app.py
pause
endlocal
