\
@echo off
cd /d %~dp0

REM ---- Important: avoid running from protected folders like Downloads if Windows blocks venv.
REM Recommended: move folder to C:\CliniqueApp\ then run this file.

python -m venv .venv
call .venv\Scripts\activate.bat

python -m pip install --upgrade pip
pip install -r requirements.txt

set DJANGO_DEBUG=1
set DB_ENGINE=sqlite

python manage.py makemigrations clinic
python manage.py migrate
python manage.py init_demo

python manage.py runserver 0.0.0.0:8080
pause
