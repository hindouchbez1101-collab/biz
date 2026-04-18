@echo off
title Clinique Cerine Alaa-Med — Serveur Local
color 0A

echo.
echo  ╔══════════════════════════════════════╗
echo  ║   Clinique Cerine Alaa-Med           ║
echo  ║   Serveur réseau local               ║
echo  ╚══════════════════════════════════════╝
echo.

cd /d "%~dp0"

REM Activer l'environnement virtuel si existant
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Appliquer les migrations
echo [1/3] Application des migrations...
python manage.py migrate --run-syncdb
echo.

REM Collecter les fichiers statiques
echo [2/3] Preparation des fichiers statiques...
python manage.py collectstatic --noinput
echo.

REM Trouver l'IP locale du PC
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    set LOCAL_IP=%%a
    goto :found
)
:found
set LOCAL_IP=%LOCAL_IP: =%

echo [3/3] Demarrage du serveur...
echo.
echo  ┌──────────────────────────────────────────┐
echo  │  Accès depuis CE PC :                    │
echo  │  http://localhost:8000                   │
echo  │                                          │
echo  │  Accès depuis les AUTRES appareils       │
echo  │  sur le même réseau WiFi/câble :         │
echo  │  http://%LOCAL_IP%:8000          │
echo  │                                          │
echo  │  Appuyez sur CTRL+C pour arrêter         │
echo  └──────────────────────────────────────────┘
echo.

python manage.py runserver 0.0.0.0:8000

pause
