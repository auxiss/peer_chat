@echo off
setlocal

REM Check if venv already exists
if not exist venv (
    echo Creating virtual environment 'venv'...
    python -m venv venv
) else (
    echo Virtual environment 'venv' already exists.
)

REM Activate the virtual environment
call venv\Scripts\activate

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install required packages
echo Installing required packages...
pip install ^
    blinker ^
    certifi ^
    charset-normalizer ^
    click ^
    Flask ^
    idna ^
    itsdangerous ^
    Jinja2 ^
    MarkupSafe ^
    pystun3 ^
    requests ^
    urllib3 ^
    Werkzeug

echo.
echo All packages installed successfully.
pause
