"""
Self-healing component that can fix common issues automatically
Integrated with main diagnostic system
"""
import json
import os
from pathlib import Path

class EmanimStudioRepair:
    def __init__(self, studio_root=None):
        # Auto-detect root directory if not provided
        if studio_root is None:
            # Try to auto-detect the EmanimStudio root
            self.studio_root = self.find_studio_root()
        else:
            self.studio_root = Path(studio_root)
    
    def find_studio_root(self):
        """Automatically find the EmanimStudio root directory"""
        # Method 1: Check if running from Scripts folder
        current_file = Path(__file__).resolve()
        if current_file.parent.name == "Scripts":
            return current_file.parent.parent
        
        # Method 2: Check if running from root
        if (current_file.parent / "EmanimStudio.bat").exists():
            return current_file.parent
        
        # Method 3: Current directory
        return Path.cwd()
    
    def fix_python_pth(self):
        """Fix the Python ._pth file for portable operation"""
        pth_file = self.studio_root / "Lib" / "python312" / "python312._pth"
        correct_content = """python312.zip
.
..\\..\\Lib\\site-packages
import site
"""
        try:
            # Create directory if it doesn't exist
            pth_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(pth_file, 'w') as f:
                f.write(correct_content)
            print(f"✅ Fixed Python ._pth file: {pth_file}")
            return True
        except Exception as e:
            print(f"❌ Failed to fix Python ._pth file: {e}")
            return False
    
    def create_missing_dirs(self):
        """Create any missing critical directories"""
        critical_dirs = [
            "Animations",
            "Animations/Math",
            "Animations/Physics", 
            "Animations/Emaphy",
            "Animations/Miscellaneous",
            "Output",
            "GUI",
            "Scripts",
            "Diagnostics"
        ]
        
        created_count = 0
        for dir_name in critical_dirs:
            dir_path = self.studio_root / dir_name
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                if not any(dir_path.iterdir()):  # If empty, count as created
                    created_count += 1
            except Exception as e:
                print(f"❌ Failed to create directory {dir_name}: {e}")
        
        print(f"✅ Created/verified {created_count} critical directories")
        return created_count > 0
    
    def fix_environment_paths(self):
        """Fix environment variables for portable operation"""
        try:
            # Add portable Python to PATH (for current process)
            python_dir = self.studio_root / "Lib" / "python312"
            ffmpeg_dir = self.studio_root / "Lib" / "ffmpeg-8.0-essentials_build" / "bin"
            
            current_path = os.environ.get('PATH', '')
            
            # Add our portable directories to the front of PATH
            new_paths = [
                str(python_dir),
                str(ffmpeg_dir),
                *current_path.split(os.pathsep)
            ]
            
            # Remove duplicates while preserving order
            seen = set()
            unique_paths = []
            for path in new_paths:
                if path not in seen:
                    seen.add(path)
                    unique_paths.append(path)
            
            os.environ['PATH'] = os.pathsep.join(unique_paths)
            os.environ['PYTHONHOME'] = str(python_dir)
            
            print("✅ Fixed environment paths for portable operation")
            return True
            
        except Exception as e:
            print(f"❌ Failed to fix environment paths: {e}")
            return False
    
    def check_python_installation(self):
        """Check if portable Python is working"""
        try:
            python_exe = self.studio_root / "Lib" / "python312" / "python.exe"
            if python_exe.exists():
                print(f"✅ Portable Python found: {python_exe}")
                return True
            else:
                print(f"❌ Portable Python not found: {python_exe}")
                return False
        except Exception as e:
            print(f"❌ Error checking Python installation: {e}")
            return False
    
    def run_complete_repair(self):
        """Run all repair operations"""
        print("🛠️ Starting EmanimStudio Auto-Repair...")
        print(f"📁 Studio root: {self.studio_root}")
        print()
        
        results = {
            'python_pth': self.fix_python_pth(),
            'directories': self.create_missing_dirs(),
            'environment': self.fix_environment_paths(),
            'python_check': self.check_python_installation()
        }
        
        print()
        success_count = sum(results.values())
        total_count = len(results)
        
        if success_count == total_count:
            print("🎉 All repairs completed successfully!")
        else:
            print(f"⚠️ {success_count}/{total_count} repairs completed successfully")
        
        return results

# Test function
def test_auto_repair():
    """Test the auto-repair system"""
    repair = EmanimStudioRepair()
    repair.run_complete_repair()

if __name__ == "__main__":
    test_auto_repair()