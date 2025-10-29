@echo off
chcp 65001 >nul
title EmanimStudio Diagnostic System

:MAIN_MENU
cls
echo.
echo ==========================================
echo    EMANIM STUDIO DIAGNOSTIC SYSTEM
echo ==========================================
echo.

set STUDIO_ROOT=%~dp0
set PYTHONHOME=%STUDIO_ROOT%Lib\python312
set PATH=%STUDIO_ROOT%Lib\python312;%PATH%

echo Available modes:
echo   1. Full Diagnostic (health check + structure + repair)
echo   2. Structure Report Only
echo   3. Auto-Repair Only  
echo   4. System Cleanup
echo   5. Exit Diagnostic System
echo.
set /p "CHOICE=Select mode (1-5): "

if "%CHOICE%"=="" (
    echo.
    echo ❌ No selection made. Please try again.
    timeout /t 2 /nobreak >nul
    goto MAIN_MENU
)

if "%CHOICE%"=="1" (
    goto RUN_FULL
) else if "%CHOICE%"=="2" (
    goto RUN_STRUCTURE
) else if "%CHOICE%"=="3" (
    goto RUN_REPAIR
) else if "%CHOICE%"=="4" (
    goto RUN_CLEAN
) else if "%CHOICE%"=="5" (
    goto EXIT
) else (
    echo.
    echo ❌ Invalid choice '%CHOICE%'. Please try again.
    timeout /t 2 /nobreak >nul
    goto MAIN_MENU
)

:RUN_FULL
echo.
echo 🔍 RUNNING FULL DIAGNOSTIC...
python "%STUDIO_ROOT%Diagnostics\diagnostic_system.py" full
goto RETURN_TO_MENU

:RUN_STRUCTURE
echo.
echo 📊 GENERATING STRUCTURE REPORT...
python "%STUDIO_ROOT%Diagnostics\diagnostic_system.py" structure
goto RETURN_TO_MENU

:RUN_REPAIR
echo.
echo 🔧 RUNNING AUTO-REPAIR...
python "%STUDIO_ROOT%Diagnostics\diagnostic_system.py" repair
goto RETURN_TO_MENU

:RUN_CLEAN
echo.
echo 🧹 CLEANING SYSTEM...
python "%STUDIO_ROOT%Diagnostics\system_cleaner.py"
goto RETURN_TO_MENU

:RETURN_TO_MENU
echo.
if errorlevel 1 (
    echo ❌ Operation completed with issues.
) else (
    echo ✅ Operation completed successfully!
)

echo.
echo Press any key to return to main menu...
pause >nul
goto MAIN_MENU

:EXIT
echo.
echo 👋 Exiting EmanimStudio Diagnostic System...
timeout /t 1 /nobreak >nul
exit /b 0