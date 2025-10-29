import sys
import os
import json
import shutil
import glob
import psutil
import platform
from pathlib import Path
from datetime import datetime
import importlib.util

class EmanimStudioDiagnostic:
    def __init__(self, studio_root=None):
        if studio_root:
            self.studio_root = Path(studio_root)
        else:
            current_file = Path(__file__)
            self.studio_root = current_file.parent.parent if current_file.parent.name == "Diagnostics" else current_file.parent

        self.diagnostics_root = self.studio_root / "Diagnostics"
        self.logs_dir = self.diagnostics_root / "repair_logs"
        self.backups_dir = self.diagnostics_root / "backups"
        
        self.logs_dir.mkdir(exist_ok=True)
        self.backups_dir.mkdir(exist_ok=True)
        
        self.system_report = {
            "status": "healthy",
            "issues": [],
            "recommendations": [],
            "health_score": 100,
            "timestamp": datetime.now().isoformat()
        }

    def log_event(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file = self.logs_dir / f"diagnostics_{datetime.now().strftime('%Y%m%d')}.log"
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] {message}\n")
            print(f"📝 {message}")
        except Exception as e:
            print(f"📝 {message} [Log write failed: {e}]")

    def run_full_diagnostic(self):
        self.log_event("Starting full diagnostic")
        
        self.system_report = {
            "status": "healthy",
            "issues": [],
            "recommendations": [],
            "health_score": 100,
            "timestamp": datetime.now().isoformat(),
            "mode": "full_diagnostic"
        }
        
        # Only check what actually matters
        self._check_python_environment()
        self._check_dependencies()
        self._check_ffmpeg()
        self._check_miktex()
        self._check_core_files()
        
        self.system_report["health_score"] = self._calculate_health_score()
        return self.system_report

    def run_structure_report(self):
        self.log_event("Generating structure report")
        
        report = {
            "system_resources": self._get_system_resources(),
            "content_stats": self._get_content_statistics(),
            "dependencies": self._get_dependency_status(),
            "folder_structure": self._get_folder_structure(),
            "timestamp": datetime.now().isoformat()
        }
        
        return report

    def run_auto_repair(self):
        self.log_event("Starting auto-repair")
        
        repairs = []
        temp_files = self._clean_temp_files()
        if temp_files:
            repairs.append(f"Cleaned {temp_files} temporary files")
        
        return {
            "repairs_performed": repairs,
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        }

    def _check_python_environment(self):
        # FIXED: Correct Python path with capital P
        python_exe = self.studio_root / "Lib" / "Python312" / "python.exe"
        if not python_exe.exists():
            self.system_report["issues"].append("Python executable not found")
            return False
        
        # Only check absolutely essential files
        essential_files = ["Lib/Python312/python.exe"]
        
        for file_path in essential_files:
            if not (self.studio_root / file_path).exists():
                self.system_report["issues"].append(f"Missing essential: {file_path}")
                return False
        
        return True

    def _check_dependencies(self):
        dependencies = {
            "manim": "manim",
            "numpy": "numpy", 
            "pillow": "PIL",
            "PyQt5": "PyQt5",
            "scipy": "scipy"
        }
        
        missing_deps = []
        
        for dep_name, import_name in dependencies.items():
            try:
                if import_name == "PIL":
                    import PIL
                else:
                    importlib.import_module(import_name)
            except ImportError:
                missing_deps.append(dep_name)
        
        if missing_deps:
            self.system_report["recommendations"].append(f"Optional dependencies missing: {', '.join(missing_deps)}")
        return True

    def _check_ffmpeg(self):
        # FIXED: Correct FFmpeg path
        ffmpeg_folder = self.studio_root / "Lib" / "FFmpeg"
        if ffmpeg_folder.exists():
            self.system_report["recommendations"].append("FFmpeg folder found")
            return True
        else:
            self.system_report["recommendations"].append("FFmpeg folder not found (optional)")
            return False

    def _check_miktex(self):
        # FIXED: Correct MiKTeX path
        miktex_folder = self.studio_root / "Lib" / "Miktex"
        if miktex_folder.exists():
            self.system_report["recommendations"].append("MikTeX folder found")
            return True
        else:
            self.system_report["recommendations"].append("MikTeX folder not found (optional)")
            return False

    def _check_core_files(self):
        # FIXED: Check actual core files
        core_files = ["main.py", "emanim_terminal.bat", "Diagnose.bat"]
        
        for file_path in core_files:
            if not (self.studio_root / file_path).exists():
                self.system_report["issues"].append(f"Missing core file: {file_path}")
                return False
        
        return True

    def _get_system_resources(self):
        try:
            disk = psutil.disk_usage(str(self.studio_root))
            memory = psutil.virtual_memory()
            
            return {
                "disk_free_gb": round(disk.free / (1024**3), 2),
                "disk_total_gb": round(disk.total / (1024**3), 2),
                "memory_available_gb": round(memory.available / (1024**3), 2),
                "memory_total_gb": round(memory.total / (1024**3), 2)
            }
        except:
            return {}

    def _get_content_statistics(self):
        # FIXED: Correct animation patterns
        animation_patterns = ["Animations/**/*.py"]
        total_animations = 0
        categories = {}
        
        for pattern in animation_patterns:
            for file in glob.glob(str(self.studio_root / pattern), recursive=True):
                total_animations += 1
                category = Path(file).parent.name
                categories[category] = categories.get(category, 0) + 1
        
        return {
            "total_animations": total_animations,
            "categories": categories
        }

    def _get_dependency_status(self):
        dependencies = {
            "manim": "manim",
            "numpy": "numpy", 
            "pillow": "PIL",
            "PyQt5": "PyQt5",
            "scipy": "scipy"
        }
        
        status = {}
        
        for dep_name, import_name in dependencies.items():
            try:
                if import_name == "PIL":
                    import PIL
                    status[dep_name] = True
                else:
                    importlib.import_module(import_name)
                    status[dep_name] = True
            except ImportError:
                status[dep_name] = False
        
        return status

    def _get_folder_structure(self):
        folders = {}
        # FIXED: Correct folder names
        main_folders = ["Animations", "Lib", "Output", "Diagnostics", "Assets"]
        
        for folder in main_folders:
            folder_path = self.studio_root / folder
            if folder_path.exists():
                try:
                    size = sum(f.stat().st_size for f in folder_path.rglob('*') if f.is_file())
                    folders[folder] = round(size / (1024*1024), 1)
                except:
                    folders[folder] = 0
        
        return folders

    def _calculate_health_score(self):
        base_score = 100
        critical_issues = [issue for issue in self.system_report["issues"] 
                          if "core file" in issue.lower() or "python executable" in issue.lower()]
        
        base_score -= len(critical_issues) * 30
        return max(0, min(100, base_score))

    def _clean_temp_files(self):
        cleaned_count = 0
        temp_patterns = ["*.tmp", "*.temp", "*.log", "*.bak"]
        
        for pattern in temp_patterns:
            for file in self.studio_root.glob(pattern):
                try:
                    file.unlink()
                    cleaned_count += 1
                except:
                    pass
        
        return cleaned_count

def run_diagnostic_mode(mode):
    diagnostic = EmanimStudioDiagnostic()
    
    if mode == "full":
        print("🔍 RUNNING FULL DIAGNOSTIC")
        print("=" * 50)
        report = diagnostic.run_full_diagnostic()
        
        print(f"🏥 Health Score: {report['health_score']}/100")
        
        if report['issues']:
            print(f"🔴 Critical Issues: {len(report['issues'])}")
            for issue in report['issues']:
                print(f"   • {issue}")
        else:
            print("✅ No critical issues found")
            
        if report['recommendations']:
            print(f"💡 Recommendations: {len(report['recommendations'])}")
            for rec in report['recommendations']:
                print(f"   • {rec}")
            
    elif mode == "structure":
        print("📊 SYSTEM STRUCTURE REPORT")
        print("=" * 50)
        report = diagnostic.run_structure_report()
        
        resources = report.get('system_resources', {})
        content = report.get('content_stats', {})
        folders = report.get('folder_structure', {})
        deps = report.get('dependencies', {})
        
        print(f"\n💾 SYSTEM RESOURCES:")
        print(f"   Disk: {resources.get('disk_free_gb', 'N/A')}GB free / {resources.get('disk_total_gb', 'N/A')}GB total")
        print(f"   Memory: {resources.get('memory_available_gb', 'N/A')}GB available / {resources.get('memory_total_gb', 'N/A')}GB total")
        
        print(f"\n📁 FOLDER STRUCTURE:")
        for folder, size in folders.items():
            print(f"   {folder}: {size} MB")
        
        print(f"\n🎬 CONTENT STATISTICS:")
        print(f"   Total Animations: {content.get('total_animations', 0)}")
        for category, count in content.get('categories', {}).items():
            print(f"   • {category}: {count}")
        
        print(f"\n📦 DEPENDENCIES:")
        for dep, status in deps.items():
            status_icon = "✅" if status else "⚠️"
            print(f"   {status_icon} {dep}: {'installed' if status else 'optional'}")
            
    elif mode == "repair":
        print("🔧 RUNNING AUTO-REPAIR")
        print("=" * 50)
        report = diagnostic.run_auto_repair()
        
        repairs = report.get('repairs_performed', [])
        if repairs:
            print("✅ Repairs completed:")
            for repair in repairs:
                print(f"   • {repair}")
        else:
            print("✅ No repairs needed")
            
    elif mode == "clean":
        print("🧹 CLEANING SYSTEM")
        print("=" * 50)
        try:
            # FIXED: Import system_cleaner from current directory
            from system_cleaner import clean_system
            clean_system()
        except ImportError:
            print("⚠️  System cleaner not available")
        except Exception as e:
            print(f"❌ Clean failed: {e}")
        
    else:
        print("❌ Unknown mode. Running full diagnostic...")
        run_diagnostic_mode("full")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_diagnostic_mode(sys.argv[1])
    else:
        print("Usage: python diagnostic_system.py [full|structure|repair|clean]")