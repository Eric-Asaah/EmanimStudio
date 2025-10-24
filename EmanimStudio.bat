@ECHO OFF
@echo off
chcp 65001 >nul
title EmanimStudio - Launch Portal
mode con: cols=100 lines=35

:: =============================================
:: EMANIMSTUDIO ENVIRONMENT CONFIGURATION
:: =============================================
set "STUDIO_ROOT=%~dp0"
set "PYTHON_HOME=%STUDIO_ROOT%Lib\python312"
set "PYTHONPATH=%STUDIO_ROOT%Lib\site-packages"
set "PATH=%PYTHON_HOME%;%STUDIO_ROOT%Lib\ffmpeg-8.0-essentials_build\bin;%PATH%"

:MAIN_LAUNCHER
cls
color 09
echo.
echo       ███████╗███╗   ███╗ █████╗ ███╗   ██╗██╗███╗   ███╗
echo       ██╔════╝████╗ ████║██╔══██╗████╗  ██║██║████╗ ████║
echo       █████╗  ██╔████╔██║███████║██╔██╗ ██║██║██╔████╔██║
echo       ██╔══╝  ██║╚██╔╝██║██╔══██║██║╚██╗██║██║██║╚██╔╝██║
echo       ███████╗██║ ╚═╝ ██║██║  ██║██║ ╚████║██║██║ ╚═╝ ██║
echo       ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚═╝     ╚═╝
color 0C
echo                              ███████╗████████╗██╗   ██╗██████╗ ██╗ ██████╗ 
echo                              ██╔════╝╚══██╔══╝██║   ██║██╔══██╗██║██╔═══██╗
echo                              ███████╗   ██║   ██║   ██║██║  ██║██║██║   ██║
echo                              ╚════██║   ██║   ██║   ██║██║  ██║██║██║   ██║
echo                              ███████║   ██║   ╚██████╔╝██████╔╝██║╚██████╔╝
echo                              ╚══════╝   ╚═╝    ╚═════╝ ╚═════╝ ╚═╝ ╚═════╝ 
color 0A
echo.
echo                    ========================================================
echo                                MATHEMATICAL ANIMATION STUDIO
echo                    ========================================================
echo.
echo                             EMANIMSTUDIO IS A PRODUCT OF EMAPHY
echo                          A comprehensive learning platform by Eric Asaah
echo.
color 09
echo                               [1] 🚀 LAUNCH TERMINAL INTERFACE
echo                               [2] 🎨 PREVIEW GRAPHICAL INTERFACE
echo                               [3] 🔧 SYSTEM DIAGNOSTICS
echo                               [4] 💾 BACKUP MANAGER
echo                               [5] 🛠️  AUTO-REPAIR
echo                               [6] ℹ️  SYSTEM INFORMATION
echo                               [7] 📖 VIEW README
echo                               [8] 🚪 EXIT
echo.
set /p "CHOICE=                              Select an option [1-8]: "

if "%CHOICE%"=="1" goto LAUNCH_TERMINAL
if "%CHOICE%"=="2" goto PREVIEW_GUI
if "%CHOICE%"=="3" goto RUN_DIAGNOSTICS
if "%CHOICE%"=="4" goto BACKUP_MANAGER
if "%CHOICE%"=="5" goto AUTO_REPAIR
if "%CHOICE%"=="6" goto SYSTEM_INFO
if "%CHOICE%"=="7" goto VIEW_README
if "%CHOICE%"=="8" goto EXIT

:VIEW_README
cls
if exist "README.txt" (
    type "README.txt"
    echo.
    echo Press any key to return to main menu...
    pause >nul
) else (
    echo README file not found!
    echo Please ensure README.txt is in the same folder as EmanimStudio.exe
    echo.
    pause
)
goto MAIN_LAUNCHER

:LAUNCH_TERMINAL
cls
color 09
echo.
echo       ========================================================
echo                    LAUNCHING TERMINAL INTERFACE
echo       ========================================================
echo.

REM Change to script directory first
cd /d "%~dp0"

REM Check if terminal batch file exists
if not exist "emanim_terminal.bat" (
    echo                  ERROR: emanim_terminal.bat not found!
    echo                  Current directory: %CD%
    echo.
    echo                  Please ensure all EmanimStudio files are together.
    echo.
    echo                  Press any key to return...
    pause >nul
    goto MAIN_LAUNCHER
)

echo                  Starting the powerful terminal interface...
echo              This gives you complete control over animation creation!
echo.
echo                  Features:
echo                  • Browse tons of pre-built animations
echo                  • Real-time rendering
echo                  • Quality settings from 480p to 4K
echo                  • Batch rendering capabilities
echo.
timeout /t 2 /nobreak >nul

REM Launch the terminal interface
call "emanim_terminal.bat"

goto MAIN_LAUNCHER
:PREVIEW_GUI
cls
color 0B
echo.
echo        ███████╗███╗   ███╗ █████╗ ███╗   ██╗██╗███╗   ███╗
echo        ██╔════╝████╗ ████║██╔══██╗████╗  ██║██║████╗ ████║
echo        █████╗  ██╔████╔██║███████║██╔██╗ ██║██║██╔████╔██║
echo        ██╔══╝  ██║╚██╔╝██║██╔══██║██║╚██╗██║██║██║╚██╔╝██║
echo        ███████╗██║ ╚═╝ ██║██║  ██║██║ ╚████║██║██║ ╚═╝ ██║
echo        ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚═╝     ╚═╝


echo                        ███████╗████████╗██╗   ██╗██████╗ ██╗ ██████╗ 
echo                        ██╔════╝╚══██╔══╝██║   ██║██╔══██╗██║██╔═══██╗
echo                        ███████╗   ██║   ██║   ██║██║  ██║██║██║   ██║
echo                        ╚════██║   ██║   ██║   ██║██║  ██║██║██║   ██║
echo                        ███████║   ██║   ╚██████╔╝██████╔╝██║╚██████╔╝
echo                        ╚══════╝   ╚═╝    ╚═════╝ ╚═════╝ ╚═╝ ╚═════╝ 

echo.
echo                        ██████╗ ██╗   ██╗██╗
echo                        ██╔════╝ ██║   ██║██║
echo                        ██║  ███╗██║   ██║██║
echo                        ██║   ██║██║   ██║██║
echo                        ╚██████╔╝╚██████╔╝██║
echo                         ╚═════╝  ╚═════╝ ╚═╝

echo.
echo                    ========================================================
echo                           EMANIMSTUDIO GUI - COMING SOON!
echo                    ========================================================
echo.

echo             We're developing an enhanced visual interface to streamline
echo             your animation workflow with practical features:
echo.

echo             🖼️  DIRECT PREVIEW WINDOW
echo                View rendered animations immediately after completion
echo                Eliminates manual file browsing for quick review
echo.
echo             📂 ORGANIZED LIBRARY BROWSING
echo                Access tons of animations through categorized navigation
echo                Structured filtering by mathematical topics
echo.
echo             🎯 SIMPLIFIED RENDER WORKFLOW
echo                Visual progress indicators during animation processing
echo                Quality presets with clear resolution options
echo.
echo             🎨 OPTIMIZED INTERFACE DESIGN
echo                Clean layout with intuitive control placement
echo                Efficient navigation for mathematical content creation
echo.

echo.
echo             PLANNED ENHANCEMENTS:
echo             🎬 EXTENDED VIDEO COMPOSITING TOOLS
echo             📊 STREAMLINED ANIMATION WORKFLOWS  
echo             🔧 ADVANCED CONTENT CREATION FEATURES
echo.

echo             EmanimStudio - Product of Emaphy Platform
echo             Created by Eric Asaah
echo.

echo.
echo             Evolving mathematical animation creation...
echo.
set /p "RETURN=             Press [T] for Terminal or [B] to go back: "

if /i "%RETURN%"=="T" goto LAUNCH_TERMINAL
if /i "%RETURN%"=="B" goto MAIN_LAUNCHER
goto PREVIEW_GUI

:RUN_DIAGNOSTICS
cls
echo.
echo       ========================================================
echo                       RUNNING SYSTEM DIAGNOSTICS
echo       ========================================================
echo.
echo                  Checking system health and components...
echo                  This ensures everything is ready for animation creation!
echo.
timeout /t 2 /nobreak >nul

if exist "Diagnostics\diagnostics.py" (
    python Diagnostics\diagnostics.py
) else (
    echo                  Diagnostics tool not found. Using basic check...
    echo.
    python --version
    echo.
    if exist "Lib\python312\python.exe" (
        echo                  ✓ Python: OK
    )
    if exist "Lib\site-packages\manim" (
        echo                  ✓ Manim: OK
    )
    if exist "Lib\ffmpeg-8.0-essentials_build" (
        echo                  ✓ FFmpeg: OK
    )
)

echo.
echo                  Press any key to return to main launcher...
pause >nul
goto MAIN_LAUNCHER

:BACKUP_MANAGER
cls
color 09
echo.
echo       ========================================================
echo                          BACKUP MANAGEMENT
echo       ========================================================
echo.
echo                  Managing your animation projects and system configuration...
echo.
timeout /t 2 /nobreak >nul

if exist "Diagnostics\backup_manager.py" (
    python Diagnostics\backup_manager.py --list
) else (
    echo                  Backup manager not found.
    echo.
    echo                  Your animations are stored in: %CD%\Animations
    echo                  Rendered videos are in: %CD%\Output
    echo.
    echo                  To backup, simply copy the entire EmanimStudio folder!
)

echo.
echo                  Press any key to return to main launcher...
pause >nul
goto MAIN_LAUNCHER

:AUTO_REPAIR
cls
color 09
echo.
echo       ========================================================
echo                          SYSTEM AUTO-REPAIR
echo       ========================================================
echo.
echo                  Scanning for issues and applying fixes...
echo                  Your system will be optimized for animation rendering!
echo.
timeout /t 2 /nobreak >nul

if exist "Diagnostics\auto_repair.py" (
    python Diagnostics\auto_repair.py
) else (
    echo                  Auto-repair tool not found. Running manual checks...
    echo.
    
    REM Check critical folders
    if not exist "Animations" (
        mkdir "Animations"
        echo                  ✓ Created Animations folder
    )
    if not exist "Output" (
        mkdir "Output"
        echo                  ✓ Created Output folder
    )
    if not exist "Animations\Math" mkdir "Animations\Math"
    if not exist "Animations\Physics" mkdir "Animations\Physics"
    if not exist "Animations\Emaphy" mkdir "Animations\Emaphy"
    if not exist "Animations\Miscellaneous" mkdir "Animations\Miscellaneous"
    
    echo                  ✓ Basic structure verified
)

echo.
echo                  Press any key to return to main launcher...
pause >nul
goto MAIN_LAUNCHER

:SYSTEM_INFO
cls
color 09
echo.
echo       ========================================================
echo                          SYSTEM INFORMATION
echo       ========================================================
echo.
echo                  EmanimStudio v2.0 - Professional Animation Suite
echo                  Owned by Emaphy - Created by Eric Asaah
echo.
echo                  Features:
echo                  • 65+ Pre-built Mathematical Animations
echo                  • Portable - No Installation Required
echo                  • Self-Healing Diagnostics System
echo                  • Professional Video Rendering Pipeline
echo.
echo                  Components:
echo                  • Manim Community Edition - Animation Engine
echo                  • FFmpeg - Video Processing
echo                  • MikTeX - Mathematical Typesetting
echo                  • Python 3.12 - Runtime Environment
echo.
echo                  Ready for: Mathematical Visualizations, Educational Content,
echo                  Scientific Presentations, and Creative Animations!
echo.
echo                  Installation Path: %CD%
echo.
echo.
echo                  Press any key to return to main launcher...
pause >nul
goto MAIN_LAUNCHER

:EXIT
cls
color 0C
echo.
echo       ========================================================
echo                         THANK YOU FOR USING
echo                           EMANIM STUDIO 1.0
echo       ========================================================
echo.
echo                  Create amazing mathematical animations!
color 0A
echo                  Brought to you by Emaphy - Eric Asaah
echo.
timeout /t 3 /nobreak >nul
exit