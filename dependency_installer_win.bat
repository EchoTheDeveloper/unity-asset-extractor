@echo off
echo Installing Python dependencies...
pip install -r requirements.txt

REM Check if installation was successful
if errorlevel 1 (
    echo Failed to install dependencies.
    pause
    exit /b 1
) else (
    echo Dependencies installed successfully.
    pause
)
