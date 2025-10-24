@echo off
setlocal enabledelayedexpansion
title EmanimStudio - Terminal Mode
color 0B

:: ==========================================
:: EMANIM STUDIO - TERMINAL INTERFACE
:: Polished and optimized version
:: ==========================================

:: Get the directory where this BAT file is located
set "STUDIO_ROOT=%~dp0"
set "STUDIO_ROOT=%STUDIO_ROOT:~0,-1%"

:: Set up paths for portable Python, FFmpeg, and packages
set "PYTHON_HOME=%STUDIO_ROOT%\Lib\python312"
set "PYTHONPATH=%STUDIO_ROOT%\Lib\site-packages"
set "PATH=%PYTHON_HOME%;%STUDIO_ROOT%\Scripts;%STUDIO_ROOT%\Lib\ffmpeg-8.0-essentials_build\bin;%PATH%"

:: Set MiKTeX path if it exists
if exist "%STUDIO_ROOT%\MiKTeX" (
    set "PATH=%STUDIO_ROOT%\MiKTeX\miktex\bin\x64;%PATH%"
)

:: Set folders
set "ANIMATIONS_DIR=%STUDIO_ROOT%\Animations"
set "OUTPUT_DIR=%STUDIO_ROOT%\Output"

:: Create folders if they don't exist
if not exist "%ANIMATIONS_DIR%" mkdir "%ANIMATIONS_DIR%"
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

:: Create category folders
if not exist "%ANIMATIONS_DIR%\Math" mkdir "%ANIMATIONS_DIR%\Math"
if not exist "%ANIMATIONS_DIR%\Physics" mkdir "%ANIMATIONS_DIR%\Physics"
if not exist "%ANIMATIONS_DIR%\Emaphy" mkdir "%ANIMATIONS_DIR%\Emaphy"
if not exist "%ANIMATIONS_DIR%\Miscellaneous" mkdir "%ANIMATIONS_DIR%\Miscellaneous"

:: Initialize variables
set "LAST_RENDERED="
set "LAST_RENDERED_FILE="
set "QUALITY=-ql"
set "QUALITY_NAME=Low (Fast)"
set "BATCH_MODE=0"

:: Check if called from GUI with parameters
if "%~1"=="render" (
    set "CATEGORY=%~2"
    set "FILENAME=%~3"
    set "CATEGORY_DIR=%ANIMATIONS_DIR%\!CATEGORY!"
    set "SELECTED=!CATEGORY_DIR!\!FILENAME!"
    
    echo Rendering !CATEGORY!/!FILENAME!...
    "%PYTHON_HOME%\python.exe" -m manim "!SELECTED!" !QUALITY! --media_dir "%OUTPUT_DIR%"
    
    if errorlevel 1 (
        echo RENDERING FAILED!
        exit /b 1
    ) else (
        echo RENDERING COMPLETE!
        exit /b 0
    )
)

:: Main Menu
:MAIN_MENU
cls
echo.
echo    ============================================
echo          EMANIM STUDIO - TERMINAL MODE
echo        Portable Animation Renderer
echo    ============================================
echo.
echo    [1] Browse Categories
echo    [2] Quick Re-render Last Animation
echo    [3] View Output Videos
echo    [4] Batch Render Category
echo    [5] Quality Settings [Current: !QUALITY_NAME!]
echo    [6] Clean Output Folder
echo    [7] System Info
echo    [8] Return to Main Launcher
echo    [9] Exit EmanimStudio
echo.
if defined LAST_RENDERED (
    echo    Last rendered: !LAST_RENDERED!
    echo.
)
set /p "CHOICE=Enter your choice [1-9]: "

if "!CHOICE!"=="1" goto BROWSE_CATEGORIES
if "!CHOICE!"=="2" goto QUICK_RERENDER
if "!CHOICE!"=="3" goto VIEW_VIDEOS
if "!CHOICE!"=="4" goto BATCH_RENDER
if "!CHOICE!"=="5" goto QUALITY_SETTINGS
if "!CHOICE!"=="6" goto CLEAN_OUTPUT
if "!CHOICE!"=="7" goto SYSTEM_INFO
if "!CHOICE!"=="8" exit /b 0
if "!CHOICE!"=="9" exit /b 1

echo.
echo    Invalid choice! Press any key to continue...
pause >nul
goto MAIN_MENU

:: Browse Categories
:BROWSE_CATEGORIES
cls
echo.
echo    ============================================
echo               SELECT CATEGORY
echo    ============================================
echo.
echo    [1] Math Animations
echo    [2] Physics Animations
echo    [3] Emaphy Animations
echo    [4] Miscellaneous Animations
echo.
echo    [B] Back to Main Menu
echo    [Q] Exit EmanimStudio
echo.
set /p "CAT_CHOICE=Enter your choice: "

if /i "!CAT_CHOICE!"=="B" goto MAIN_MENU
if /i "!CAT_CHOICE!"=="Q" exit /b 1

set "CATEGORY="
set "CATEGORY_NAME="

if "!CAT_CHOICE!"=="1" (
    set "CATEGORY=Math"
    set "CATEGORY_NAME=Math Animations"
)
if "!CAT_CHOICE!"=="2" (
    set "CATEGORY=Physics"
    set "CATEGORY_NAME=Physics Animations"
)
if "!CAT_CHOICE!"=="3" (
    set "CATEGORY=Emaphy"
    set "CATEGORY_NAME=Emaphy Animations"
)
if "!CAT_CHOICE!"=="4" (
    set "CATEGORY=Miscellaneous"
    set "CATEGORY_NAME=Miscellaneous Animations"
)

if not defined CATEGORY (
    echo.
    echo    Invalid choice! Press any key to continue...
    pause >nul
    goto BROWSE_CATEGORIES
)

set "CATEGORY_DIR=%ANIMATIONS_DIR%\!CATEGORY!"
set "ANIM_COUNT=0"
for %%F in ("!CATEGORY_DIR!\*.py") do set /a ANIM_COUNT+=1

if !ANIM_COUNT! EQU 0 (
    cls
    echo.
    echo    ============================================
    echo              NO ANIMATIONS FOUND
    echo    ============================================
    echo.
    echo    Category: !CATEGORY_NAME!
    echo    Folder: !CATEGORY_DIR!
    echo.
    echo    Add .py animation files to this folder
    echo    Each file should contain a Scene class
    echo.
    echo    Press any key to continue...
    pause >nul
    goto BROWSE_CATEGORIES
)

goto ANIMATION_MENU

:: Animation Selection
:ANIMATION_MENU
cls
echo.
echo    ============================================
echo               !CATEGORY_NAME!
echo    ============================================
echo.
echo    Available Animations:
echo.

set "INDEX=1"
for %%F in ("!CATEGORY_DIR!\*.py") do (
    set "FILENAME=%%~nxF"
    set "BASENAME=%%~nF"
    set "TITLE=!BASENAME!"
    set "DESCRIPTION=No description"
    
    :: Read metadata from file (first 10 lines only for speed)
    set "LINE_NUM=0"
    for /f "usebackq tokens=1,* delims=:" %%A in ("%%F") do (
        set /a "LINE_NUM+=1"
        if !LINE_NUM! LEQ 10 (
            set "LINE=%%A"
            set "VALUE=%%B"
            if "!LINE!"=="# TITLE" set "TITLE=!VALUE:~1!"
            if "!LINE!"=="# DESCRIPTION" set "DESCRIPTION=!VALUE:~1!"
        )
    )
    
    echo    [!INDEX!] !TITLE!
    echo        !DESCRIPTION!
    echo.
    set "ANIM_!INDEX!=%%F"
    set "ANIM_TITLE_!INDEX!=!TITLE!"
    set "ANIM_BASE_!INDEX!=!BASENAME!"
    set /a INDEX+=1
)

set /a "ANIM_COUNT=!INDEX!-1"

if "!BATCH_MODE!"=="1" (
    echo    [B] Back to Batch Setup
) else (
    echo    [B] Back to Categories
)
echo    [M] Main Menu
echo    [Q] Exit
echo.
set /p "ANIM_CHOICE=Select animation [1-!ANIM_COUNT!]: "

if /i "!ANIM_CHOICE!"=="B" (
    if "!BATCH_MODE!"=="1" (
        set "BATCH_MODE=0"
        goto BATCH_RENDER
    ) else (
        goto BROWSE_CATEGORIES
    )
)
if /i "!ANIM_CHOICE!"=="M" goto MAIN_MENU
if /i "!ANIM_CHOICE!"=="Q" exit /b 1

:: Validate numeric input
set "VALID=0"
if !ANIM_CHOICE! GEQ 1 if !ANIM_CHOICE! LEQ !ANIM_COUNT! set "VALID=1"

if !VALID! EQU 1 (
    set "SELECTED=!ANIM_%ANIM_CHOICE%!"
    set "SELECTED_TITLE=!ANIM_TITLE_%ANIM_CHOICE%!"
    set "SELECTED_BASE=!ANIM_BASE_%ANIM_CHOICE%!"
    
    if "!BATCH_MODE!"=="1" (
        set "BATCH_LIST=!BATCH_LIST! "!SELECTED!""
        echo    Added: !SELECTED_TITLE!
        timeout /t 1 /nobreak >nul
        goto ANIMATION_MENU
    )
    goto RENDER_ANIMATION
)

echo.
echo    Invalid choice! Press any key to continue...
pause >nul
goto ANIMATION_MENU

:: Render Animation
:RENDER_ANIMATION
cls
echo.
echo    ============================================
echo               RENDERING ANIMATION
echo    ============================================
echo.
echo    Category: !CATEGORY_NAME!
echo    Animation: !SELECTED_TITLE!
echo    File: !SELECTED!
echo    Quality: !QUALITY_NAME!
echo.
echo    Detecting scene classes...
echo.

:: Detect scene name using Python
"%PYTHON_HOME%\python.exe" -c "import ast; content = open(r'!SELECTED!', encoding='utf-8').read(); tree = ast.parse(content); scenes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef) and any(hasattr(b, 'id') and b.id == 'Scene' for b in node.bases)]; scene = scenes[0] if scenes else '!SELECTED_BASE!'; print(f'Using scene: {scene}'); open(r'%TEMP%\scene_name.txt', 'w').write(scene)" 2>nul

if exist "%TEMP%\scene_name.txt" (
    set /p SCENE_NAME=<"%TEMP%\scene_name.txt"
    del "%TEMP%\scene_name.txt" 2>nul
) else (
    set "SCENE_NAME=!SELECTED_BASE!"
    echo    Warning: Could not detect scene, using filename
)

echo    Scene class: !SCENE_NAME!
echo.
echo    ----------------------------------------
echo    Starting render process...
echo    ----------------------------------------
echo.

:: Render the animation
"%PYTHON_HOME%\python.exe" -m manim "!SELECTED!" "!SCENE_NAME!" !QUALITY! --media_dir "%OUTPUT_DIR%"

if errorlevel 1 (
    echo.
    echo    ========================================
    echo              RENDERING FAILED
    echo    ========================================
    echo.
    echo    Possible issues:
    echo    - Syntax error in Python code
    echo    - Scene class not found
    echo    - Missing dependencies
    echo    - Invalid Manim syntax
    echo.
    echo    Scene attempted: !SCENE_NAME!
    echo    File: !SELECTED!
    echo.
    set "LAST_RENDERED=!SELECTED_TITLE! (Failed)"
    pause
    goto ANIMATION_MENU
)

:: Success!
echo.
echo    ============================================
echo            RENDERING COMPLETE!
echo    ============================================
echo.

set "LAST_RENDERED=!SELECTED_TITLE!"
set "LAST_RENDERED_FILE=!SELECTED!"

:: ============================================
:: EXPLICIT VIDEO DETECTION - KNOWS EXACT LOCATION
:: ============================================
echo    Locating rendered video...
set "VIDEO_FILE="

:: Set quality folder based on current quality setting
set "QUALITY_FOLDER=480p15"
if "!QUALITY!"=="-qm" set "QUALITY_FOLDER=720p30"
if "!QUALITY!"=="-qh" set "QUALITY_FOLDER=1080p60" 
if "!QUALITY!"=="-qk" set "QUALITY_FOLDER=1440p60"

:: EXPLICIT PATH: Check the exact expected location
set "EXPECTED_VIDEO=%OUTPUT_DIR%\videos\!SELECTED_BASE!\!QUALITY_FOLDER!\!SCENE_NAME!.mp4"

if exist "!EXPECTED_VIDEO!" (
    set "VIDEO_FILE=!EXPECTED_VIDEO!"
    goto :video_found
)

:: Fallback: Quick search in case of slight path variation
for /f "delims=" %%V in ('dir "%OUTPUT_DIR%\videos\!SELECTED_BASE!" /s /b /a-d /o-d 2^>nul') do (
    set "VIDEO_FILE=%%V"
    goto :video_found
)

:video_found

if defined VIDEO_FILE (
    echo    Found: !VIDEO_FILE!
    echo.
    echo    [1] Play video now
    echo    [2] Open output folder  
    echo    [3] Render another animation
    echo    [4] Return to main menu
    echo.
    set /p "AFTER_CHOICE=What would you like to do? [1-4]: "
    
    if "!AFTER_CHOICE!"=="1" (
        echo    Opening video player...
        start "" "!VIDEO_FILE!"
        timeout /t 2 /nobreak >nul
        goto ANIMATION_MENU
    )
    if "!AFTER_CHOICE!"=="2" (
        echo    Opening output folder...
        start "" "%OUTPUT_DIR%\videos"
        timeout /t 2 /nobreak >nul
        goto ANIMATION_MENU
    )
    if "!AFTER_CHOICE!"=="3" goto ANIMATION_MENU
    if "!AFTER_CHOICE!"=="4" goto MAIN_MENU
    
    goto ANIMATION_MENU
) else (
    echo    Warning: Could not locate rendered video
    echo    Expected: !EXPECTED_VIDEO!
    echo    Check manually: %OUTPUT_DIR%\videos
    echo.
    pause
    goto ANIMATION_MENU
)

:: Quick Re-render
:QUICK_RERENDER
if not defined LAST_RENDERED_FILE (
    cls
    echo.
    echo    ============================================
    echo              NO PREVIOUS ANIMATION
    echo    ============================================
    echo.
    echo    You haven't rendered anything yet!
    echo    Please browse categories first.
    echo.
    pause
    goto MAIN_MENU
)

cls
echo.
echo    ============================================
echo              QUICK RE-RENDER
echo    ============================================
echo.
echo    Re-rendering: !LAST_RENDERED!
echo    Quality: !QUALITY_NAME!
echo.
echo    Press any key to start...
pause >nul

set "SELECTED=!LAST_RENDERED_FILE!"
set "SELECTED_TITLE=!LAST_RENDERED!"
for %%F in ("!SELECTED!") do set "SELECTED_BASE=%%~nF"
goto RENDER_ANIMATION

:: View Output Videos
:VIEW_VIDEOS
cls
echo.
echo    ============================================
echo              OUTPUT VIDEOS
echo    ============================================
echo.
echo    Opening output folder...
echo    Location: %OUTPUT_DIR%\videos
echo.

if exist "%OUTPUT_DIR%\videos" (
    start "" "%OUTPUT_DIR%\videos"
) else (
    echo    No videos folder found yet.
    echo    Render an animation first!
)

echo.
echo    Press any key to return to menu...
pause >nul
goto MAIN_MENU

:: Batch Render
:BATCH_RENDER
cls
echo.
echo    ============================================
echo              BATCH RENDERING
echo    ============================================
echo.
echo    This feature allows you to render multiple
echo    animations from one category automatically.
echo.
echo    [1] Start batch render
echo    [B] Back to main menu
echo.
set /p "BATCH_CHOICE=Enter your choice: "

if /i "!BATCH_CHOICE!"=="B" goto MAIN_MENU
if "!BATCH_CHOICE!"=="1" (
    set "BATCH_MODE=1"
    set "BATCH_LIST="
    goto BROWSE_CATEGORIES
)
goto BATCH_RENDER

:: Quality Settings
:QUALITY_SETTINGS
cls
echo.
echo    ============================================
echo              QUALITY SETTINGS
echo    ============================================
echo.
echo    Current: !QUALITY_NAME!
echo.
echo    [1] Low Quality (Fast) - 480p, 15fps
echo    [2] Medium Quality - 720p, 30fps
echo    [3] High Quality (Slow) - 1080p, 60fps
echo    [4] Production Quality (Very Slow) - 4K
echo.
echo    [B] Back to main menu
echo.
set /p "QUAL_CHOICE=Select quality: "

if /i "!QUAL_CHOICE!"=="B" goto MAIN_MENU

if "!QUAL_CHOICE!"=="1" (
    set "QUALITY=-ql"
    set "QUALITY_NAME=Low (Fast)"
)
if "!QUAL_CHOICE!"=="2" (
    set "QUALITY=-qm"
    set "QUALITY_NAME=Medium"
)
if "!QUAL_CHOICE!"=="3" (
    set "QUALITY=-qh"
    set "QUALITY_NAME=High"
)
if "!QUAL_CHOICE!"=="4" (
    set "QUALITY=-qk"
    set "QUALITY_NAME=Production (4K)"
)

echo.
echo    Quality set to: !QUALITY_NAME!
timeout /t 2 /nobreak >nul
goto MAIN_MENU

:: Clean Output Folder
:CLEAN_OUTPUT
cls
echo.
echo    ============================================
echo              CLEAN OUTPUT FOLDER
echo    ============================================
echo.
echo    WARNING: This will delete ALL rendered videos
echo    and temporary files from the output folder.
echo.
echo    Are you sure? [Y/N]
echo.
set /p "CLEAN_CONFIRM=Confirm deletion: "

if /i "!CLEAN_CONFIRM!"=="Y" (
    echo.
    echo    Cleaning output folder...
    if exist "%OUTPUT_DIR%\videos" rd /s /q "%OUTPUT_DIR%\videos"
    if exist "%OUTPUT_DIR%\images" rd /s /q "%OUTPUT_DIR%\images"
    if exist "%OUTPUT_DIR%\texts" rd /s /q "%OUTPUT_DIR%\texts"
    echo    Output folder cleaned!
) else (
    echo    Cancelled.
)

echo.
pause
goto MAIN_MENU

:: System Info
:SYSTEM_INFO
cls
echo.
echo    ============================================
echo              SYSTEM INFORMATION
echo    ============================================
echo.

"%PYTHON_HOME%\python.exe" -c "import sys, os; from pathlib import Path; print(f'Python: {sys.version.split()[0]}'); print(f'Studio: {os.getcwd()}'); print(); print('FOLDERS:'); [print(f'   {f}: OK' if Path(f).exists() else f'   {f}: MISSING') for f in ['Animations', 'Output', 'Lib', 'Scripts']]; print(); print('TOOLS:'); exec('try:\n    import manim\n    print(f\"   Manim: {manim.__version__}\")\nexcept:\n    print(\"   Manim: NOT FOUND\")'); print(); exec('from pathlib import Path; anim_dir = Path(\"Animations\"); cats = [d for d in anim_dir.iterdir() if d.is_dir()]; total = sum(len(list(c.glob(\"*.py\"))) for c in cats); print(f\"ANIMATIONS:\"); print(f\"   Categories: {len(cats)}\"); print(f\"   Total files: {total}\")')"

echo.
echo    Press any key to return to menu...
pause >nul
goto MAIN_MENU