@echo off
chcp 65001 >nul
title EmanimStudio - Environment Repair
color 0E

echo.
echo ==========================================
echo    EMANIM STUDIO AUTO-REPAIR SYSTEM
echo ==========================================
echo.

set STUDIO_ROOT=%~dp0

:: Set up Python environment
set PYTHONHOME=%STUDIO_ROOT%Lib\python312
set PYTHONPATH=%STUDIO_ROOT%Lib\site-packages
set PATH=%STUDIO_ROOT%Lib\python312;%STUDIO_ROOT%Lib\ffmpeg-8.0-essentials_build\bin;%PATH%

:: NEW: Enhanced repair with backup and recovery options
echo [1/4] Creating backup before repair...
python "%STUDIO_ROOT%Diagnostics\backup_manager.py" --create full --comment "Pre-repair backup" >nul 2>&1

echo [2/4] Running comprehensive repair...
python "%STUDIO_ROOT%Diagnostics\auto_repair.py"

if errorlevel 1 (
    echo.
    echo ❌ Standard repair failed. Attempting emergency recovery...
    python "%STUDIO_ROOT%Diagnostics\emergency_recovery.py" --repair-python
)

echo [3/4] Verifying repair...
python "%STUDIO_ROOT%Diagnostics\system_check.py" >nul 2>&1

if errorlevel 1 (
    echo.
    echo ⚠️  Some issues may remain. Check detailed diagnostics.
) else (
    echo.
    echo ✅ Repair completed successfully!
)

echo.
pause