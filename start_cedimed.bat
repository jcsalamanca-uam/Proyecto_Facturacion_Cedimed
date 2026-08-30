@echo off
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    py -3.11 -m venv .venv
)

call .venv\Scripts\activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py migrate

start "" http://127.0.0.1:8000/
python manage.py runserver 127.0.0.1:8000
