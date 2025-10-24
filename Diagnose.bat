@echo off
chcp 65001 >nul
title EmanimStudio - Diagnostic Launcher v2.2
color 0E

echo.
echo ==========================================
echo    EMANIM STUDIO DIAGNOSTIC LAUNCHER v2.2
echo ==========================================
echo.
echo Enhanced with Auto-Repair ^& Backup Systems
echo.

set STUDIO_ROOT=%~dp0

:: Set up Python environment
set PYTHONHOME=%STUDIO_ROOT%Lib\python312
set PYTHONPATH=%STUDIO_ROOT%Lib\site-packages
set PATH=%STUDIO_ROOT%Lib\python312;%STUDIO_ROOT%Lib\ffmpeg-8.0-essentials_build\bin;%PATH%

:: FINAL VERSION: Preserves original functionality + enhanced tools
if "%~1"=="" (
    echo Available diagnostic modes:
    echo   1. Quick Check (fast)
    echo   2. Full Health Report (comprehensive)
    echo   3. Emergency Recovery
    echo   4. Backup Management
    echo   5. System Structure Report
    echo   6. Auto-Repair System
    echo   7. Enhanced Backup Tools  [NEW]
    echo.
    set /p CHOICE="Select mode (1-7): "
) else (
    set CHOICE=%~1
)

:: ORIGINAL FUNCTIONALITY - uses health_monitor.py and other original scripts
if "%CHOICE%"=="1" (
    echo Running Quick Check...
    python "%STUDIO_ROOT%Diagnostics\health_monitor.py" --quick
) else if "%CHOICE%"=="2" (
    echo Running Full Health Report...
    python "%STUDIO_ROOT%Diagnostics\health_monitor.py"
) else if "%CHOICE%"=="3" (
    echo Starting Emergency Recovery...
    python "%STUDIO_ROOT%Diagnostics\emergency_recovery.py" --health-check
) else if "%CHOICE%"=="4" (
    echo Starting Backup Management...
    python "%STUDIO_ROOT%Diagnostics\backup_manager.py" --list
) else if "%CHOICE%"=="5" (
    echo Generating System Structure Report...
    python "%STUDIO_ROOT%Diagnostics\structure_report.py"
) else if "%CHOICE%"=="6" (
    echo Starting Auto-Repair System...
    python "%STUDIO_ROOT%Diagnostics\auto_repair.py"
) else if "%CHOICE%"=="7" (
    echo Enhanced Backup Tools:
    echo   1. Create Enhanced Backup
    echo   2. Restore Latest Backup
    echo   3. Verify All Backups
    echo   4. Backup Status Report
    echo.
    set /p BACKUP_CHOICE="Select backup option (1-4): "
    
    if "%BACKUP_CHOICE%"=="1" (
        if exist "%STUDIO_ROOT%create_enhanced_backup.bat" (
            call "%STUDIO_ROOT%create_enhanced_backup.bat"
        ) else (
            echo ❌ Enhanced backup tool not found!
            echo Please ensure create_enhanced_backup.bat exists.
        )
    ) else if "%BACKUP_CHOICE%"=="2" (
        if exist "%STUDIO_ROOT%restore_latest.bat" (
            call "%STUDIO_ROOT%restore_latest.bat"
        ) else (
            echo ❌ Restore tool not found!
            echo Please ensure restore_latest.bat exists.
        )
    ) else if "%BACKUP_CHOICE%"=="3" (
        if exist "%STUDIO_ROOT%backup_manager.bat" (
            call "%STUDIO_ROOT%backup_manager.bat"
        ) else (
            echo ❌ Backup manager not found!
            echo Falling back to Python backup manager...
            python "%STUDIO_ROOT%Diagnostics\backup_manager.py" --list
        )
    ) else if "%BACKUP_CHOICE%"=="4" (
        echo Running Backup Status Report...
        python "%STUDIO_ROOT%Diagnostics\structure_report.py" --backups
    ) else (
        echo Invalid backup option
    )
) else (
    echo Running Default Health Check...
    python "%STUDIO_ROOT%Diagnostics\health_monitor.py"
)

if errorlevel 1 (
    echo.
    echo ❌ Diagnostics found issues. Check the report above.
    echo.
    echo 💡 Quick fixes available:
    echo   - Option 6: Auto-Repair System
    echo   - Option 7: Enhanced Backup Tools
    echo   - Option 3: Emergency Recovery
) else (
    echo.
    echo ✅ System is healthy!
)

echo.
pause