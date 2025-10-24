@echo off
:: Minimize this window immediately
powershell -WindowStyle Hidden -Command "start-process cmd -ArgumentList '/c,\"\"%~f0\"\" inner' -WindowStyle Hidden"

if "%~1"=="inner" (
    chcp 65001 >nul
    "Lib\python312\pythonw.exe" "main.py"
)
exit