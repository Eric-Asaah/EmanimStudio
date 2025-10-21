import sys
import os
import subprocess
import json
import shutil
from pathlib import Path
import importlib.util

class EmanimStudioDoctor:
    def __init__(self):
        self.studio_root = Path(__file__).parent
        self.python_root = Path(sys.executable).parent
        self.system_report = {
            "status": "healthy",
            "issues": [],
            "recommendations": [],
            "environment": {},
            "structure": {},
            "dependencies": {},
            "gui_type": "web_based"  # NEW: Track GUI type
        }
    
    def run_comprehensive_check(self):
        """Run all diagnostic checks with error handling"""
        print("🔍 EmanimStudio Comprehensive Diagnostic System")
        print("=" * 60)
        
        try:
            self.check_system_architecture()
            self.check_python_environment()
            self.check_manim_installation()
            self.check_ffmpeg_integration()
            self.check_laTeX_system()
            self.check_gui_components()
            self.check_backend_integration()  # NEW: Check backend files
            self.check_animation_workflow()
            self.check_portability_integrity()
        except Exception as e:
            print(f"❌ Diagnostic error: {e}")
            self.system_report["issues"].append(f"Diagnostic system error: {e}")
        
        return self.generate_final_report()
    
    def check_system_architecture(self):
        """Check the complete folder structure and organization"""
        print("\n📁 SYSTEM ARCHITECTURE CHECK")
        print("-" * 40)
        
        expected_structure = {
            "Core": [
                "EmanimStudio.bat",
                "diagnostics.py", 
                "diagnose.bat",
                "fix_environment.bat"
            ],
            "Libraries": [
                "Lib/python312/",
                "Lib/site-packages/",
                "Lib/ffmpeg-8.0-essentials_build/"
            ],
            "Application": [
                "GUI/index.html",
                "GUI/animations_list.json",
                "GUI/styles.css",
                "GUI/script.js",
                "Scripts/",
                "Animations/",
                "Output/",
                "Miktex/"
            ]
        }
        
        self.system_report["structure"] = {}
        
        for category, items in expected_structure.items():
            self.system_report["structure"][category] = {}
            print(f"\n{category}:")
            
            for item in items:
                full_path = self.studio_root / item
                if full_path.exists():
                    status = "✅ PRESENT"
                    if full_path.is_file():
                        size = f"({full_path.stat().st_size} bytes)"
                    else:
                        size = f"({len(list(full_path.rglob('*')))} items)"
                else:
                    status = "❌ MISSING"
                    size = ""
                    self.system_report["issues"].append(f"Missing file/directory: {item}")
                    
                    # Add specific recommendations for critical files
                    if item == "diagnose.bat":
                        self.system_report["recommendations"].append("Create diagnose.bat diagnostic launcher")
                    elif item == "GUI/styles.css":
                        self.system_report["recommendations"].append("Create GUI/styles.css for GUI styling")
                    elif item == "GUI/script.js":
                        self.system_report["recommendations"].append("Create GUI/script.js for GUI functionality")
                    elif item == "fix_environment.bat":
                        self.system_report["recommendations"].append("Create fix_environment.bat for quick repairs")
                
                print(f"  {status} {item} {size}")
                self.system_report["structure"][category][item] = {
                    "exists": full_path.exists(),
                    "path": str(full_path),
                    "type": "file" if full_path.is_file() else "directory"
                }
    
    def check_python_environment(self):
        """Deep check of Python configuration"""
        print("\n🐍 PYTHON ENVIRONMENT CHECK")
        print("-" * 40)
        
        # Check Python executable
        python_exe = Path(sys.executable)
        print(f"Python Executable: {python_exe}")
        print(f"Python Version: {sys.version}")
        
        # Critical ._pth file check
        pth_file = self.python_root / "python312._pth"
        required_pth_content = [
            "python312.zip",
            ".",
            "..\\..\\Lib\\site-packages", 
            "import site"
        ]
        
        if pth_file.exists():
            with open(pth_file, 'r') as f:
                current_content = [line.strip() for line in f if line.strip() and not line.startswith('```')]
            
            # Filter out only the valid configuration lines
            valid_lines = []
            for line in current_content:
                if line in required_pth_content:
                    valid_lines.append(line)
            
            if valid_lines == required_pth_content:
                print("✅ python312._pth: CORRECTLY CONFIGURED")
            else:
                print("❌ python312._pth: MISCONFIGURED")
                print(f"   Expected: {required_pth_content}")
                print(f"   Found: {current_content}")
                self.system_report["issues"].append("Python ._pth file contains extra text/invalid content")
                self.system_report["recommendations"].append("Run fix_environment.bat to clean python312._pth file")
                
                # Auto-fix suggestion
                print("   💡 Run 'fix_environment.bat' to automatically fix this issue")
        else:
            print("❌ python312._pth: FILE MISSING")
            self.system_report["issues"].append("Python ._pth file missing")
            self.system_report["recommendations"].append("Create python312._pth file with portable configuration")
        
        # Check site-packages accessibility
        site_packages = self.studio_root / "Lib" / "site-packages"
        if site_packages.exists():
            package_count = len([p for p in site_packages.glob('*') if p.is_dir() and not p.name.endswith('.dist-info')])
            print(f"✅ Site-packages: ACCESSIBLE ({package_count} packages)")
        else:
            print("❌ Site-packages: INACCESSIBLE")
            self.system_report["issues"].append("Site-packages directory inaccessible")
    
    def check_manim_installation(self):
        """Comprehensive Manim installation check with better error handling"""
        print("\n🎬 MANIM INSTALLATION CHECK")
        print("-" * 40)
        
        try:
            import manim
            version = getattr(manim, '__version__', 'Unknown')
            print(f"✅ Manim Version: {version}")
            
            # Check critical Manim components with proper import paths
            manim_components = [
                'manim',  # Base package
                'manim.scene',  # Scene module
                'manim.animation',  # Animation module
                'manim.camera',  # Camera module
                'manim.mobject',  # Mobject module
            ]
            
            for component in manim_components:
                try:
                    __import__(component)
                    print(f"   ✅ {component}")
                except ImportError as e:
                    print(f"   ❌ {component}: {e}")
                    self.system_report["issues"].append(f"Manim component missing: {component}")
            
            # Test basic Manim functionality
            try:
                from manim import Circle, Scene
                print("   ✅ Basic Manim imports: WORKING")
            except ImportError as e:
                print(f"   ❌ Basic Manim imports: FAILED - {e}")
                self.system_report["issues"].append(f"Basic Manim imports failing: {e}")
                    
        except ImportError as e:
            print(f"❌ MANIM IMPORT FAILED: {e}")
            self.system_report["issues"].append("Manim not importable")
            self.system_report["recommendations"].append("Reinstall Manim in portable site-packages")
    
    def check_ffmpeg_integration(self):
        """Check FFmpeg installation and integration"""
        print("\n🎥 FFMPEG INTEGRATION CHECK")
        print("-" * 40)
        
        ffmpeg_paths = [
            self.studio_root / "Lib" / "ffmpeg-8.0-essentials_build" / "bin" / "ffmpeg.exe",
            self.studio_root / "Lib" / "ffmpeg-8.0-essentials_build" / "bin" / "ffprobe.exe"
        ]
        
        for ffmpeg_exe in ffmpeg_paths:
            if ffmpeg_exe.exists():
                print(f"✅ {ffmpeg_exe.name}: FOUND")
            else:
                print(f"❌ {ffmpeg_exe.name}: MISSING")
                self.system_report["issues"].append(f"FFmpeg component missing: {ffmpeg_exe.name}")
        
        # Test FFmpeg functionality
        try:
            result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                version_line = result.stdout.split('\n')[0]
                print(f"✅ FFmpeg Runtime: WORKING ({version_line})")
            else:
                print("❌ FFmpeg Runtime: EXECUTION FAILED")
                self.system_report["issues"].append("FFmpeg execution failed")
        except Exception as e:
            print(f"❌ FFmpeg Runtime: {e}")
            self.system_report["issues"].append(f"FFmpeg runtime error: {e}")
    
    def check_laTeX_system(self):
        """Check MikTeX installation and LaTeX capabilities"""
        print("\n📝 LaTeX SYSTEM CHECK")
        print("-" * 40)
        
        miktex_path = self.studio_root / "Miktex"
        if miktex_path.exists():
            file_count = len(list(miktex_path.rglob('*.*')))
            print(f"✅ MikTeX: INSTALLED ({file_count} files)")
        else:
            print("❌ MikTeX: NOT INSTALLED")
            self.system_report["issues"].append("MikTeX LaTeX system missing")
            self.system_report["recommendations"].append("Install portable MikTeX for LaTeX rendering")
    
    def check_gui_components(self):
        """Check web GUI components"""
        print("\n🌐 GUI COMPONENTS CHECK")
        print("-" * 40)
        
        gui_path = self.studio_root / "GUI"
        if not gui_path.exists():
            print("❌ GUI folder: MISSING")
            self.system_report["issues"].append("GUI folder missing")
            return
            
        critical_gui_files = [
            "index.html",  # Main interface
            "animations_list.json",  # Animation database
            "styles.css",  # Styling
            "script.js"   # Functionality
        ]
        
        for gui_file in critical_gui_files:
            file_path = gui_path / gui_file
            if file_path.exists():
                size = file_path.stat().st_size
                print(f"✅ {gui_file}: PRESENT ({size} bytes)")
                
                # Analyze index.html to understand GUI type
                if gui_file == "index.html":
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'render.php' in content:
                            self.system_report["gui_type"] = "web_based_php"
                            print("   🔍 GUI Type: Web-based (PHP backend)")
                        elif 'fetch' in content and '.json' in content:
                            self.system_report["gui_type"] = "web_based_javascript"
                            print("   🔍 GUI Type: Web-based (JavaScript backend)")
            else:
                print(f"❌ {gui_file}: MISSING")
                self.system_report["issues"].append(f"GUI file missing: {gui_file}")
                if gui_file == "styles.css":
                    self.system_report["recommendations"].append("Create GUI/styles.css for GUI styling")
                elif gui_file == "script.js":
                    self.system_report["recommendations"].append("Create GUI/script.js for GUI functionality")
    
    def check_backend_integration(self):
        """Check backend integration files for the web GUI"""
        print("\n🔧 BACKEND INTEGRATION CHECK")
        print("-" * 40)
        
        gui_type = self.system_report.get("gui_type", "unknown")
        
        if gui_type == "web_based_php":
            # Check for PHP backend files
            php_files = [
                "GUI/render.php",
                "GUI/play.php", 
                "GUI/status.json"
            ]
            
            for php_file in php_files:
                file_path = self.studio_root / php_file
                if file_path.exists():
                    print(f"✅ {php_file}: PRESENT")
                else:
                    print(f"❌ {php_file}: MISSING")
                    self.system_report["issues"].append(f"PHP backend file missing: {php_file}")
            
            if not any("php" in issue for issue in self.system_report["issues"]):
                print("✅ PHP Backend: All files present")
            else:
                self.system_report["recommendations"].append("Create PHP backend files or switch to Python backend")
        
        else:
            # Check for Python backend integration
            backend_files = [
                "Scripts/start_gui.py",
                "Scripts/render_handler.py",
                "Scripts/video_player.py"
            ]
            
            for backend_file in backend_files:
                file_path = self.studio_root / backend_file
                if file_path.exists():
                    print(f"✅ {backend_file}: PRESENT")
                else:
                    print(f"❌ {backend_file}: MISSING")
                    self.system_report["issues"].append(f"Backend integration file missing: {backend_file}")
            
            if not any("backend" in issue for issue in self.system_report["issues"]):
                print("✅ Backend Integration: All files present")
            else:
                self.system_report["recommendations"].append("Create Python backend integration scripts")
    
    def check_animation_workflow(self):
        """Check animation creation and rendering workflow"""
        print("\n🎞️ ANIMATION WORKFLOW CHECK")
        print("-" * 40)
        
        animations_dir = self.studio_root / "Animations"
        output_dir = self.studio_root / "Output"
        
        # Check directories
        for directory, purpose in [(animations_dir, "source"), (output_dir, "output")]:
            if directory.exists():
                file_count = len(list(directory.glob("*")))
                print(f"✅ {purpose.title()} Directory: READY ({file_count} files)")
            else:
                print(f"❌ {purpose.title()} Directory: MISSING")
                self.system_report["issues"].append(f"{purpose.title()} directory missing")
        
        # Check for Python animation files
        py_files = list(animations_dir.glob("*.py"))
        if py_files:
            print(f"✅ Animation Files: {len(py_files)} found")
            for py_file in py_files[:3]:  # Show first 3
                print(f"   📄 {py_file.name}")
                
                # Check if animation files have proper Manim structure
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'class' in content and 'Scene' in content and 'def construct' in content:
                            print(f"      ✅ Valid Manim scene structure")
                        else:
                            print(f"      ⚠️  May not be a valid Manim scene")
                except:
                    print(f"      ❓ Could not read file content")
        else:
            print("⚠️  Animation Files: No .py files found in Animations/ directory")
            self.system_report["recommendations"].append("Add Manim animation .py files to Animations folder")
    
    def check_portability_integrity(self):
        """Verify the portable nature of the installation"""
        print("\n💼 PORTABILITY INTEGRITY CHECK")
        print("-" * 40)
        
        # Check for absolute paths that might break portability
        portable_checks = [
            ("No system Python dependency", sys.prefix == str(self.python_root)),
            ("Self-contained FFmpeg", (self.studio_root / "Lib" / "ffmpeg-8.0-essentials_build").exists()),
            ("Self-contained LaTeX", (self.studio_root / "Miktex").exists()),
        ]
        
        for check_name, check_result in portable_checks:
            if check_result:
                print(f"✅ {check_name}")
            else:
                print(f"❌ {check_name}")
                self.system_report["issues"].append(f"Portability issue: {check_name}")
    
    def generate_final_report(self):
        """Generate comprehensive diagnostic report"""
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE DIAGNOSTIC REPORT")
        print("=" * 60)
        
        # Overall status
        if not self.system_report["issues"]:
            self.system_report["status"] = "HEALTHY"
            print("🎉 SYSTEM STATUS: FULLY OPERATIONAL")
            print("All components are properly configured and ready for animation creation!")
        else:
            self.system_report["status"] = "NEEDS_ATTENTION"
            print(f"⚠️  SYSTEM STATUS: {len(self.system_report['issues'])} ISSUES DETECTED")
            
            print("\n🚨 IDENTIFIED ISSUES:")
            for i, issue in enumerate(self.system_report["issues"], 1):
                print(f"   {i}. {issue}")
            
            print("\n💡 RECOMMENDED ACTIONS:")
            for i, recommendation in enumerate(self.system_report["recommendations"], 1):
                print(f"   {i}. {recommendation}")
        
        # GUI-specific recommendations
        gui_type = self.system_report.get("gui_type", "unknown")
        if gui_type == "web_based_php":
            print("\n🌐 GUI TYPE: Web-based with PHP Backend")
            print("   💡 Your GUI expects PHP server functionality")
            print("   💡 Consider switching to Python backend for portability")
        
        # Generate JSON report for AI analysis
        report_file = self.studio_root / "system_diagnostic_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.system_report, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Detailed report saved to: {report_file}")
        print("\n💡 You can share this JSON report with AI assistants for further troubleshooting!")
        
        return self.system_report

def main():
    """Main diagnostic execution with error handling"""
    try:
        doctor = EmanimStudioDoctor()
        report = doctor.run_comprehensive_check()
        
        # Exit with appropriate code
        return 0 if report["status"] == "HEALTHY" else 1
    except Exception as e:
        print(f"💥 CRITICAL DIAGNOSTIC FAILURE: {e}")
        return 2

if __name__ == "__main__":
    sys.exit(main())