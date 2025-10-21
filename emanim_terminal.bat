@echo off
setlocal enabledelayedexpansion
title EmanimStudio - Terminal Mode

:: Get the directory where this BAT file is located
set "STUDIO_ROOT=%~dp0"
set "STUDIO_ROOT=%STUDIO_ROOT:~0,-1%"

:: Set up paths
set "PYTHON_HOME=%STUDIO_ROOT%\Lib\python312"
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
if not exist "%ANIMATIONS_DIR%\Emanim" mkdir "%ANIMATIONS_DIR%\Emanim"
if not exist "%ANIMATIONS_DIR%\Miscellaneous" mkdir "%ANIMATIONS_DIR%\Miscellaneous"

:: Initialize variables
set "LAST_RENDERED="
set "QUALITY=-ql"
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
echo            EMANIM STUDIO - TERMINAL MODE
echo        Portable Animation Renderer
echo    ============================================
echo.
echo    [1] Browse Categories
echo    [2] Quick Re-render Last Animation
echo    [3] View Output Videos
echo    [4] Batch Render Category
echo    [5] Quality Settings
echo    [6] Clean Output Folder
echo    [7] System Info
echo    [8] Switch to GUI Mode
echo    [9] Exit
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
if "!CHOICE!"=="8" goto SWITCH_TO_GUI
if "!CHOICE!"=="9" exit /b

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
echo    [Q] Quit
echo.
set /p "CAT_CHOICE=Enter your choice: "

if /i "!CAT_CHOICE!"=="B" goto MAIN_MENU
if /i "!CAT_CHOICE!"=="Q" exit /b

if "!CAT_CHOICE!"=="1" set "CATEGORY=Math" && set "CATEGORY_NAME=Math Animations"
if "!CAT_CHOICE!"=="2" set "CATEGORY=Physics" && set "CATEGORY_NAME=Physics Animations"
if "!CAT_CHOICE!"=="3" set "CATEGORY=Emaphy" && set "CATEGORY_NAME=Emaphy Animations"
if "!CAT_CHOICE!"=="4" set "CATEGORY=Miscellaneous" && set "CATEGORY_NAME=Miscellaneous Animations"

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
    echo    Folder: !CATEGORY_DIR!
    echo.
    echo    Add .py animation files to this folder
    echo.
    echo    Press any key to continue...
    pause >nul
    goto BROWSE_CATEGORIES
)

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
    set "TITLE=%%~nF"
    set "DESCRIPTION=No description available"
    
    :: Read metadata from file (first 5 lines only)
    set "LINE_NUM=0"
    for /f "usebackq tokens=1,* delims=:" %%A in ("%%F") do (
        set /a "LINE_NUM+=1"
        if !LINE_NUM! LEQ 5 (
            if "%%A"=="# TITLE" set "TITLE=%%B"
            if "%%A"=="# DESCRIPTION" set "DESCRIPTION=%%B"
        )
    )
    
    echo    [!INDEX!] !TITLE!
    echo        File: !FILENAME!
    echo        Desc: !DESCRIPTION!
    echo.
    set "ANIM_!INDEX!=%%F"
    set "ANIM_TITLE_!INDEX!=!TITLE!"
    set /a INDEX+=1
)

if "!BATCH_MODE!"=="1" (
    echo    [B] Back to Batch Setup
) else (
    echo    [B] Back to Categories
)
echo    [M] Main Menu
echo    [Q] Quit
echo.
set /p "ANIM_CHOICE=Select animation: "

if /i "!ANIM_CHOICE!"=="B" (
    if "!BATCH_MODE!"=="1" (
        goto BATCH_RENDER_LOOP
    ) else (
        goto BROWSE_CATEGORIES
    )
)
if /i "!ANIM_CHOICE!"=="M" goto MAIN_MENU
if /i "!ANIM_CHOICE!"=="Q" exit /b

if !ANIM_CHOICE! GEQ 1 if !ANIM_CHOICE! LEQ !ANIM_COUNT! (
    set "SELECTED=!ANIM_%ANIM_CHOICE%!"
    set "SELECTED_TITLE=!ANIM_TITLE_%ANIM_CHOICE%!"
    
    if "!BATCH_MODE!"=="1" (
        set "BATCH_LIST=!BATCH_LIST! "!SELECTED!""
        goto BATCH_RENDER_LOOP
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
echo    File: %%~nxSELECTED%%
echo    Quality: !QUALITY!
echo.
echo    [RENDERING IN PROGRESS...]
echo.

"%PYTHON_HOME%\python.exe" -m manim "!SELECTED!" !QUALITY! --media_dir "%OUTPUT_DIR%"

if errorlevel 1 (
    echo    [RENDERING FAILED!]
    echo.
    echo    Check animation file for errors
    echo.
    set "LAST_RENDERED=!SELECTED_TITLE! (Failed)"
) else (
    echo    [RENDERING COMPLETE!]
    echo.
    set "LAST_RENDERED=!SELECTED_TITLE!"
    
    :: NEW: Better video file detection that handles complex paths
    echo    Searching for rendered video...
    
    :: Method 1: Look for the most recently created MP4 file
    set "VIDEO_FILE="
    for /f "delims=" %%V in ('dir "%OUTPUT_DIR%\*.mp4" /s /b /od 2^>nul') do set "VIDEO_FILE=%%V"
    
    if defined VIDEO_FILE (
        echo    Video found: !VIDEO_FILE!
        echo    Playing video automatically...
        start "" "!VIDEO_FILE!"
        echo    Video player launched...
        echo.
    ) else (
        echo    Warning: Could not find rendered video file
        echo    Check folder manually: %OUTPUT_DIR%
        echo.
    )
)

echo.
echo    Press any key to continue...
pause >nul
goto ANIMATION_MENU

:: Quick Re-render Last Animation
:QUICK_RERENDER
if not defined LAST_RENDERED (
    echo.
    echo    No previous animation found!
    echo.
    pause >nul
    goto MAIN_MENU
)
echo.
echo    Re-rendering: !LAST_RENDERED!
echo.
goto RENDER_ANIMATION

:: View Output Videos
:VIEW_VIDEOS
cls
echo.
echo    ============================================
echo               OUTPUT VIDEOS
echo    ============================================
echo.
set "VIDEO_COUNT=0"
echo    Searching for video files...
echo.

:: Use better search that handles complex paths
for /f "delims=" %%V in ('dir "%OUTPUT_DIR%\*.mp4" /s /b 2^>nul') do (
    set /a VIDEO_COUNT+=1
    echo    [!VIDEO_COUNT!] %%~nxV
    echo        Full Path: %%V
    echo.
    set "VIDEO_!VIDEO_COUNT!=%%V"
)

if !VIDEO_COUNT! EQU 0 (
    echo    No MP4 files found in output folder or subfolders
    echo    Check: %OUTPUT_DIR%
) else (
    echo    Total videos found: !VIDEO_COUNT!
    echo.
    echo    [P] Play specific video
    echo    [O] Open output folder
    echo    [B] Back to Main Menu
    echo.
    set /p "VID_OPTION=Select option: "
    
    if /i "!VID_OPTION!"=="P" (
        set /p "VID_NUM=Enter video number [1-!VIDEO_COUNT!]: "
        if !VID_NUM! GEQ 1 if !VID_NUM! LEQ !VIDEO_COUNT! (
            echo Playing: !VIDEO_%VID_NUM%!
            start "" "!VIDEO_%VID_NUM%!"
            timeout /t 3 >nul
        )
    )
    if /i "!VID_OPTION!"=="O" (
        start "" "%OUTPUT_DIR%"
        echo    Opening output folder...
        timeout /t 2 >nul
    )
)

if /i not "!VID_OPTION!"=="B" (
    echo.
    echo    Press any key to continue...
    pause >nul
    goto VIEW_VIDEOS
)
goto MAIN_MENU

:: Batch Render Category
:BATCH_RENDER
set "BATCH_MODE=1"
set "BATCH_LIST="
cls
echo.
echo    ============================================
echo               BATCH RENDER MODE
echo    ============================================
echo.
echo    Select a category to batch render:
echo.
goto BROWSE_CATEGORIES

:BATCH_RENDER_LOOP
if defined BATCH_LIST (
    echo    Added: !SELECTED_TITLE!
    echo.
    set /p "CONTINUE=Add another animation? [Y/n]: "
    if /i not "!CONTINUE!"=="n" goto ANIMATION_MENU
)

:: Process batch render
set "BATCH_MODE=0"
cls
echo.
echo    ============================================
echo               BATCH RENDERING
echo    ============================================
echo.
echo    Rendering !BATCH_LIST: =! animations...
echo.

set "SUCCESS_COUNT=0"
set "FAIL_COUNT=0"
for %%A in (!BATCH_LIST!) do (
    echo    Rendering: %%~nxA
    "%PYTHON_HOME%\python.exe" -m manim "%%A" !QUALITY! --media_dir "%OUTPUT_DIR%"
    if errorlevel 1 (
        echo    FAILED: %%~nxA
        set /a FAIL_COUNT+=1
    ) else (
        echo    SUCCESS: %%~nxA
        set /a SUCCESS_COUNT+=1
    )
    echo.
)

echo    ============================================
echo    BATCH COMPLETE!
echo    Successful: !SUCCESS_COUNT!
echo    Failed: !FAIL_COUNT!
echo    ============================================
echo.
echo    Press any key to continue...
pause >nul
goto MAIN_MENU

:: Quality Settings
:QUALITY_SETTINGS
cls
echo.
echo    ============================================
echo               QUALITY SETTINGS
echo    ============================================
echo.
echo    Current: !QUALITY!
echo.
echo    [1] Low Quality (-ql) - Fastest
echo    [2] Medium Quality (-qm) - Balanced
echo    [3] High Quality (-qh) - Best
echo    [4] Preview Quality (-p) - Interactive
echo.
echo    [B] Back
echo.
set /p "QUAL_CHOICE=Select quality: "
if /i "!QUAL_CHOICE!"=="B" goto MAIN_MENU
if "!QUAL_CHOICE!"=="1" set "QUALITY=-ql"
if "!QUAL_CHOICE!"=="2" set "QUALITY=-qm"
if "!QUAL_CHOICE!"=="3" set "QUALITY=-qh"
if "!QUAL_CHOICE!"=="4" set "QUALITY=-p"
echo.
echo    Quality set to: !QUALITY!
timeout /t 2 >nul
goto QUALITY_SETTINGS

:: Clean Output Folder
:CLEAN_OUTPUT
cls
echo.
echo    ============================================
echo               CLEAN OUTPUT FOLDER
echo    ============================================
echo.
echo    WARNING: This will delete ALL files in:
echo    %OUTPUT_DIR%
echo.
set /p "CONFIRM=Are you sure? [y/N]: "

if /i "!CONFIRM!"=="y" (
    rmdir /s /q "%OUTPUT_DIR%" 2>nul
    mkdir "%OUTPUT_DIR%"
    echo.
    echo    Output folder cleaned successfully!
) else (
    echo.
    echo    Operation cancelled.
)

echo.
echo    Press any key to continue...
pause >nul
goto MAIN_MENU

:: System Info
:SYSTEM_INFO
cls
echo.
echo    ============================================
echo               SYSTEM INFORMATION
echo    ============================================
echo.
echo    Studio Root: %STUDIO_ROOT%
echo    Python: %PYTHON_HOME%
echo    Animations: %ANIMATIONS_DIR%
echo    Output: %OUTPUT_DIR%
echo.
echo    --------------------------------------------
echo.
set "TOTAL_ANIM=0"
for /r "%ANIMATIONS_DIR%" %%F in (*.py) do set /a TOTAL_ANIM+=1
echo    Total Animations: !TOTAL_ANIM!

set "TOTAL_VIDEOS=0"
for /f "delims=" %%V in ('dir "%OUTPUT_DIR%\*.mp4" /s /b 2^>nul') do set /a TOTAL_VIDEOS+=1
echo    Rendered Videos: !TOTAL_VIDEOS!
echo    Current Quality: !QUALITY!
echo.
echo    --------------------------------------------
echo.
pause >nul
goto MAIN_MENU

:: Switch to GUI Mode
:SWITCH_TO_GUI
if exist "%STUDIO_ROOT%\emanim_gui.py" (
    echo Launching GUI mode...
    "%PYTHON_HOME%\python.exe" "%STUDIO_ROOT%\emanim_gui.py"
) else (
    echo GUI not available. Using terminal mode.
    pause
    goto MAIN_MENU
)