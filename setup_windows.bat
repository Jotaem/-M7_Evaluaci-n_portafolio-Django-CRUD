@echo off
REM Script de inicio rápido para el proyecto Django en Windows

echo ========================================
echo   Sistema de Gestión de Productos
echo   Django - Windows Setup
echo ========================================
echo.

REM Verificar si existe el entorno virtual
if not exist "venv" (
    echo [1/4] Creando entorno virtual...
    python -m venv venv
    if errorlevel 1 (
        echo Error al crear el entorno virtual.
        pause
        exit /b 1
    )
) else (
    echo [1/4] Entorno virtual ya existe
)

echo.
echo [2/4] Activando entorno virtual...
call venv\Scripts\activate.bat

echo.
echo [3/4] Instalando dependencias...
pip install -r requirements.txt -q

echo.
echo [4/4] Ejecutando migraciones...
python manage.py migrate

echo.
echo ========================================
echo   Servidor listo para iniciar!
echo ========================================
echo.
echo Siguiente paso: Ejecuta "python manage.py runserver"
echo URL: http://127.0.0.1:8000/
echo Admin: http://127.0.0.1:8000/admin/
echo.
pause
