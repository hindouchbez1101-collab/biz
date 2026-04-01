\
@echo off
cd /d %~dp0

python -m venv .venv
call .venv\Scripts\activate.bat

python -m pip install --upgrade pip
pip install -r requirements.txt

REM Load .env into environment variables (simple parser)
for /f "usebackq tokens=1,* delims==" %%a in (`type .env`) do (
  if not "%%a"=="" set %%a=%%b
)

set DJANGO_DEBUG=0
set DB_ENGINE=postgres

python manage.py makemigrations clinic
python manage.py migrate
python manage.py init_demo

python manage.py runserver 0.0.0.0:8080
pause
