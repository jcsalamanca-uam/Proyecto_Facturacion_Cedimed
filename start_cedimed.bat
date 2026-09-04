@ecYa eho off
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    py -3 -m venv .venv
    if errorlevel 1 (
        echo No se pudo crear el entorno virtual. Instala Python 3.11 o superior.
        pause
        exit /b 1
    )
)

call .venv\Scripts\activate

python -m pip install --upgrade pip
if errorlevel 1 pause & exit /b 1
python -m pip install -r requirements.txt
if errorlevel 1 pause & exit /b 1
python manage.py migrate
if errorlevel 1 pause & exit /b 1

start "" http://127.0.0.1:8000/
python manage.py runserver 127.0.0.1:8000
