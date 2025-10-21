@echo off
chcp 65001 >nul
title EmanimStudio Debug Information

echo.
echo ==========================================
echo         🐛 EMANIMSTUDIO DEBUG INFO
echo ==========================================
echo.

echo 📅 TIMESTAMP: %date% %time%
echo.

echo 📁 CURRENT DIRECTORY:
echo   %CD%
echo.

echo 🐍 PYTHON INFORMATION:
python -c "
import sys
import os
from pathlib import Path

print('Python executable:', sys.executable)
print('Python version:', sys.version)
print('Python path:')
for i, path in enumerate(sys.path):
    print(f'  {i+1:2d}. {path}')
print()

print('Current working directory:', Path.cwd())
print('Script location:', Path(__file__).resolve() if '__file__' in globals() else 'Unknown')
print()

# Check if we can find EmanimStudio root
current_dir = Path.cwd()
print('Looking for EmanimStudio root...')
possible_roots = [
    current_dir,
    current_dir.parent if current_dir.name == 'Scripts' else None,
    current_dir.parent.parent if current_dir.parent.name == 'Scripts' else None
]

for root in possible_roots:
    if root and root.exists():
        batch_file = root / 'EmanimStudio.bat'
        scripts_dir = root / 'Scripts'
        if batch_file.exists() or scripts_dir.exists():
            print(f'✅ Possible root found: {root}')
            print(f'   EmanimStudio.bat exists: {batch_file.exists()}')
            print(f'   Scripts folder exists: {scripts_dir.exists()}')
            if scripts_dir.exists():
                core_backend = scripts_dir / 'core' / 'backend.py'
                print(f'   Backend exists: {core_backend.exists()}')
"

echo.
echo 📁 FOLDER STRUCTURE:
echo Root folder contents:
dir /B
echo.
if exist "Scripts" (
    echo Scripts folder contents:
    dir "Scripts" /B
    echo.
    if exist "Scripts\core" (
        echo Scripts\core folder contents:
        dir "Scripts\core" /B
    ) else (
        echo ❌ Scripts\core folder does not exist
    )
) else (
    echo ❌ Scripts folder does not exist
)

echo.
echo 🔧 ATTEMPTING BACKEND IMPORT:
python -c "
import sys
import os
from pathlib import Path
import traceback

print('Attempting to import backend...')

# Try different import methods
methods = [
    ('Direct import', 'import sys; sys.path.append(\"Scripts\"); from core.backend import get_backend'),
    ('Absolute path', 'import sys; sys.path.insert(0, \"Scripts\"); from core.backend import get_backend'),
    ('Current dir', 'import sys; sys.path.insert(0, \".\"); from Scripts.core.backend import get_backend'),
]

for method_name, import_code in methods:
    print(f'\nTrying: {method_name}')
    try:
        exec(import_code)
        print('✅ SUCCESS!')
        break
    except Exception as e:
        print(f'❌ FAILED: {e}')
        print(f'   Error details: {traceback.format_exc()}')
"

echo.
echo 📋 ENVIRONMENT VARIABLES:
echo PATH contains Python: %PATH% | findstr /i "python" >nul && echo ✅ Python in PATH || echo ❌ Python not in PATH
echo PATH contains Scripts: %PATH% | findstr /i "scripts" >nul && echo ✅ Scripts in PATH || echo ❌ Scripts not in PATH

echo.
echo 🎯 QUICK FIX ATTEMPT:
python -c "
import sys
from pathlib import Path

# Try to manually set up the path
current_dir = Path.cwd()
scripts_path = current_dir / 'Scripts'
core_path = scripts_path / 'core'

print('Current directory:', current_dir)
print('Scripts path exists:', scripts_path.exists())
print('Core path exists:', core_path.exists())

if core_path.exists():
    print('Adding to Python path...')
    sys.path.insert(0, str(scripts_path))
    print('New Python path:')
    for i, path in enumerate(sys.path[:5]):  # Show first 5
        print(f'  {i+1}. {path}')
    
    print('\nTrying import again...')
    try:
        from core.backend import get_backend
        print('✅ BACKEND IMPORT SUCCESSFUL!')
        backend = get_backend()
        print('✅ BACKEND INITIALIZATION SUCCESSFUL!')
    except Exception as e:
        print(f'❌ STILL FAILED: {e}')
        import traceback
        print('Full error:')
        print(traceback.format_exc())
else:
    print('❌ Core folder not found at expected location')
"

echo.
echo ==========================================
echo         🎯 DEBUG COMPLETE
echo ==========================================
echo.
echo 📊 Please share ALL the output above so I can fix the issues!
echo.
pause