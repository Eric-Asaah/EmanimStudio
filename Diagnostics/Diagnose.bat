@echo off
chcp 65001 >nul
title EmanimStudio Diagnostic Suite

echo.
echo ==========================================
echo     EMANIM STUDIO DIAGNOSTIC LAUNCHER
echo ==========================================
echo.

REM Set up portable Python environment
set "PYTHONHOME=%~dp0Lib\python312"
set "PATH=%~dp0Lib\python312;%~dp0Lib\ffmpeg-8.0-essentials_build\bin;%PATH%"

REM Run the comprehensive diagnostic system
"%~dp0Lib\python312\python.exe" "%~dp0diagnostics.py"

echo.
echo Diagnostic complete. Check the report above.
echo.
pause