# SIMPLE ASCII-ONLY DEBUG SCRIPT
print("=== EMANIMSTUDIO DEBUG INFORMATION ===")

import sys
import os
from pathlib import Path
import traceback

print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")
print()

print("=== CURRENT DIRECTORY STRUCTURE ===")
current_dir = Path.cwd()
print(f"Working directory: {current_dir}")

print("\nRoot folder contents:")
try:
    for item in current_dir.iterdir():
        print(f"  [DIR] {item.name}" if item.is_dir() else f"  [FILE] {item.name}")
except Exception as e:
    print(f"  ERROR listing directory: {e}")

print("\n=== CHECKING EMANIMSTUDIO FILES ===")
important_files = [
    "EmanimStudio.bat",
    "Scripts/core/backend.py", 
    "Scripts/AutoRepair.py",
    "Scripts/RenderHandler.py",
    "Scripts/VideoPlayer.py",
    "Animations/",
    "Lib/python312/python.exe"
]

for file_path in important_files:
    full_path = current_dir / file_path
    if full_path.exists():
        print(f"  FOUND: {file_path}")
    else:
        print(f"  MISSING: {file_path}")

print("\n=== PYTHON PATH ===")
print("Python is looking in these folders:")
for i, path in enumerate(sys.path[:10]):  # First 10 only
    print(f"  {i+1:2d}. {path}")

print("\n=== ATTEMPTING BACKEND IMPORT ===")
try:
    print("Trying to import backend...")
    scripts_path = current_dir / "Scripts"
    if scripts_path.exists():
        sys.path.insert(0, str(scripts_path))
        print(f"Added to path: {scripts_path}")
        
        from core.backend import get_backend
        print("SUCCESS! Backend imported")
        
        backend = get_backend()
        print("SUCCESS! Backend initialized")
        
        # Test basic functions
        categories = backend.get_categories()
        print(f"Found {len(categories)} categories")
        
    else:
        print("ERROR: Scripts folder not found")
        
except Exception as e:
    print(f"FAILED: {e}")
    print("\nERROR DETAILS:")
    print(traceback.format_exc())
    
    # Manual check
    print("\n=== MANUAL FILE CHECK ===")
    backend_path = current_dir / "Scripts" / "core" / "backend.py"
    print(f"Backend file exists: {backend_path.exists()}")
    
    if backend_path.exists():
        print("Backend file found at:", backend_path)

print("\n=== SUGGESTIONS ===")
print("1. Check Scripts/core/backend.py exists")
print("2. Verify folder structure is correct")
print("3. Make sure all required files are present")

print("\n=== DEBUG COMPLETE ===")
input("Press Enter to close...")