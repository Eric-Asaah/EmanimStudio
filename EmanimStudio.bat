@echo off
chcp 65001 >nul
title EmanimStudio - Portable Animation Studio

:MAIN_MENU
cls
echo.
echo ==========================================
echo      🎬 WELCOME TO EMANIM STUDIO!
echo ==========================================
echo.
echo 👋 Hello there! Don't worry about this terminal window.
echo    It's just text commands: you're in complete control!
echo.
echo 💡 Think of this as a friendly menu system.
echo    We'll guide you through every step. 😊
echo.
echo 🚀 What would you like to do?
echo.
echo 1. 🎥 Create and Render Animation
echo 2. 🔧 Run System Diagnostics
echo 3. 📁 Open Animations Folder
echo 4. 🎥 Open Output Videos Folder
echo 5. 📺 Play Latest Video
echo 6. 🛠️ Fix Python Environment
echo 7. 🎨 Try Graphical Interface (Coming soon)
echo 8. ❓ Help and Instructions
echo 9. ❌ Exit
echo.
set /p CHOICE="Please enter your choice [1-9]: "

if "%CHOICE%"=="1" goto CREATE_ANIMATION
if "%CHOICE%"=="2" goto DIAGNOSTICS
if "%CHOICE%"=="3" goto OPEN_ANIMATIONS
if "%CHOICE%"=="4" goto OPEN_OUTPUT
if "%CHOICE%"=="5" goto PLAY_VIDEO
if "%CHOICE%"=="6" goto FIX_ENVIRONMENT
if "%CHOICE%"=="7" goto GUI_INTERFACE
if "%CHOICE%"=="8" goto HELP
if "%CHOICE%"=="9" goto EXIT

echo.
echo ❌ Invalid choice! Please enter 1-9.
echo.
pause
goto MAIN_MENU

:CREATE_ANIMATION
cls
echo.
echo ==========================================
echo         🎥 CREATE ANIMATION
echo ==========================================
echo.
echo 📝 Let's create an animation step by step!
echo.
echo 🔍 First, let me check what animation categories you have...
echo.
python -c "import sys; sys.path.append('Scripts'); from core.backend import get_backend; backend = get_backend(); categories = backend.get_categories(); print(f'Found {len(categories)} categories:'); [print(f'   {i+1}. {cat['display_name']} ({cat['animation_count']} animations)') for i, cat in enumerate(categories)]"
echo.
set /p CAT_CHOICE="Choose a category [1-4]: "

if "%CAT_CHOICE%"=="1" set CATEGORY=Math
if "%CAT_CHOICE%"=="2" set CATEGORY=Physics
if "%CAT_CHOICE%"=="3" set CATEGORY=Emanim
if "%CAT_CHOICE%"=="4" set CATEGORY=Miscellaneous

echo.
echo 📂 Checking animations in %CATEGORY%...
python -c "import sys; sys.path.append('Scripts'); from core.backend import get_backend; backend = get_backend(); anims = backend.get_animations('%CATEGORY%'); print(f'Found {len(anims)} animations:'); [print(f'   {i+1}. {anim['title']}') for i, anim in enumerate(anims)]"
echo.
set /p ANIM_CHOICE="Choose animation [number] or 'b' to go back: "

if /i "%ANIM_CHOICE%"=="b" goto MAIN_MENU

echo.
echo 🎬 Rendering animation...
python -c "import sys; sys.path.append('Scripts'); from core.backend import get_backend; backend = get_backend(); anims = backend.get_animations('%CATEGORY%'); import os; os.system(''); result = backend.render_animation('%CATEGORY%', anims[int('%ANIM_CHOICE%')-1]['filename']); print(result['message'])"
echo.
pause
goto MAIN_MENU

:DIAGNOSTICS
cls
echo.
echo ==========================================
echo         🔧 SYSTEM DIAGNOSTICS
echo ==========================================
echo.
echo 🔍 Checking your system health...
echo 💡 This will make sure everything is working properly.
echo.
python -c "import sys; sys.path.append('Scripts'); from core.backend import get_backend; backend = get_backend(); result = backend.run_diagnostics(); print('Diagnostics complete!')"
echo.
echo 📊 Diagnostics complete! Your system should be ready.
echo.
pause
goto MAIN_MENU

:OPEN_ANIMATIONS
echo.
echo 📁 Opening Animations folder...
python -c "import sys; sys.path.append('Scripts'); from core.backend import get_backend; backend = get_backend(); result = backend.open_animations_folder(); print(result['message'])"
echo.
pause
goto MAIN_MENU

:OPEN_OUTPUT
echo.
echo 🎥 Opening Output Videos folder...
python -c "import sys; sys.path.append('Scripts'); from core.backend import get_backend; backend = get_backend(); result = backend.open_output_folder(); print(result['message'])"
echo.
pause
goto MAIN_MENU

:PLAY_VIDEO
echo.
echo 📺 Playing latest video...
python -c "import sys; sys.path.append('Scripts'); from core.backend import get_backend; backend = get_backend(); result = backend.play_latest_video(); print(result['message'])"
echo.
pause
goto MAIN_MENU

:FIX_ENVIRONMENT
echo.
echo 🛠️ Fixing Python environment...
python -c "import sys; sys.path.append('Scripts'); from core.backend import get_backend; backend = get_backend(); result = backend.fix_environment(); print(result['message'])"
echo.
pause
goto MAIN_MENU

:GUI_INTERFACE
echo.
echo 🎨 Launching Graphical Interface...
python -c "import sys; sys.path.append('Scripts'); from core.backend import get_backend; backend = get_backend(); result = backend.launch_gui_placeholder(); print(result['message'])"
echo.
pause
goto MAIN_MENU

:HELP
cls
echo.
echo ==========================================
echo         ❓ HELP & INSTRUCTIONS
echo ==========================================
echo.
echo 🎯 HOW TO USE EMANIM STUDIO:
echo.
echo 1. Add your animation .py files to the Animations folder
echo 2. Use the categories: Math, Physics, Emanim, Miscellaneous
echo 3. Run diagnostics first to check everything works
echo 4. Your rendered videos will appear in Output folder
echo.
echo 💡 TIPS:
echo - Don't panic about the terminal - it's just text!
echo - Everything is self-contained in this folder
echo - No internet required after download
echo - Can run from USB drives
echo.
echo 🆘 TROUBLESHOOTING:
echo - Run Diagnostics if something doesn't work
echo - Use Fix Environment for Python issues
echo - Check Animations folder for your files
echo.
echo 🎨 GRAPHICAL INTERFACE:
echo - Currently in development
echo - Use 'Try Graphical Interface' for a preview
echo - Terminal is fully functional in the meantime
echo.
pause
goto MAIN_MENU

:EXIT
echo.
echo 👋 Thank you for using EmanimStudio!
echo 🎬 Happy animating!
echo.
timeout /t 2 >nul
exit