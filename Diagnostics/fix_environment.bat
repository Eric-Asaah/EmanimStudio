@echo off
chcp 65001 >nul
title EmanimStudio Environment Fixer

echo Fixing python312._pth file...
echo.

set "PYTHONHOME=%~dp0Lib\python312"
set "PATH=%~dp0Lib\python312;%PATH%"

echo Creating clean python312._pth file...
(
echo python312.zip
echo .
echo ..\..\Lib\site-packages
echo import site
) > "%~dp0Lib\python312\python312._pth"

echo ✅ python312._pth has been fixed!
echo.
echo Now run diagnose.bat to check the system again.
pause