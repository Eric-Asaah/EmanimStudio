#!/usr/bin/env python3
"""
EmanimStudio Structure Report - Comprehensive System Analysis
Enhanced with backup system integration and detailed diagnostics
"""

import os
import sys
from pathlib import Path
from datetime import datetime


class StructureReporter:
    def __init__(self, studio_root=None):
        # Auto-detect root path
        if studio_root is None:
            current_file = Path(__file__)
            if current_file.parent.name == "Diagnostics":
                self.studio_root = current_file.parent.parent
            else:
                self.studio_root = current_file.parent
        else:
            self.studio_root = Path(studio_root)

        self.backups_dir = self.studio_root / "Diagnostics" / "backups"

    def print_header(self, title):
        """Print formatted section header"""
        print(f"\n{title}")
        print("=" * 60)

    def get_folder_size(self, path):
        """Calculate folder size in MB"""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if os.path.exists(fp):
                        total_size += os.path.getsize(fp)
            return round(total_size / (1024 * 1024), 2)  # Convert to MB
        except:
            return 0

    def count_files_by_type(self, path, extension):
        """Count files with specific extension"""
        try:
            return len(list(Path(path).rglob(f"*{extension}")))
        except:
            return 0

    def analyze_root_structure(self):
        """Analyze root directory structure"""
        self.print_header("📁 ROOT DIRECTORY STRUCTURE")

        root_items = []
        for item in self.studio_root.iterdir():
            if item.name.startswith('.'):
                continue

            item_info = {
                'name': item.name,
                'is_dir': item.is_dir(),
                'size_mb': self.get_folder_size(item) if item.is_dir() else 0,
                'file_count': len(list(item.rglob('*'))) if item.is_dir() else 1
            }
            root_items.append(item_info)

        # Sort: directories first, then files
        root_items.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))

        for item in root_items:
            if item['is_dir']:
                icon = "📁"
                size_info = f"({item['file_count']} items, {item['size_mb']}MB)"
            else:
                icon = "📄"
                size_info = f"({item['size_mb']}MB)" if item['size_mb'] > 0 else ""

            print(f"  {icon} {item['name']} {size_info}")

    def analyze_python_environment(self):
        """Detailed Python environment analysis"""
        self.print_header("🐍 PYTHON ENVIRONMENT")

        python_dir = self.studio_root / "Lib" / "python312"

        if not python_dir.exists():
            print("  ❌ Python directory not found!")
            return

        # Python executable check
        python_exe = python_dir / "python.exe"
        print(
            f"  {'✅' if python_exe.exists() else '❌'} Python executable: {python_exe.name}")

        # Critical directories
        critical_dirs = [
            ("DLLs", python_dir / "DLLs"),
            ("tcl", python_dir / "tcl"),
            ("Lib", python_dir / "Lib"),
            ("Scripts", python_dir / "Scripts")
        ]

        for name, path in critical_dirs:
            if path.exists():
                file_count = len(list(path.rglob('*')))
                size_mb = self.get_folder_size(path)
                print(f"  ✅ {name}: {file_count} files, {size_mb}MB")
            else:
                print(f"  ❌ {name}: MISSING")

        # Critical files check
        critical_files = [
            ("python312._pth", python_dir / "python312._pth"),
            ("_tkinter.pyd", python_dir / "DLLs" / "_tkinter.pyd"),
            ("tcl86t.dll", python_dir / "DLLs" / "tcl86t.dll"),
            ("tk86t.dll", python_dir / "DLLs" / "tk86t.dll")
        ]

        for name, path in critical_files:
            if path.exists():
                size_kb = round(path.stat().st_size / 1024, 1)
                print(f"  ✅ {name}: {size_kb}KB")
            else:
                print(f"  ❌ {name}: MISSING")

    def analyze_animations(self):
        """Analyze animations structure"""
        self.print_header("🎬 ANIMATIONS STRUCTURE")

        animations_dir = self.studio_root / "Animations"

        if not animations_dir.exists():
            print("  ❌ Animations directory not found!")
            return

        categories = {}
        total_animations = 0

        for category in animations_dir.iterdir():
            if category.is_dir():
                py_files = list(category.glob("*.py"))
                categories[category.name] = len(py_files)
                total_animations += len(py_files)

        if categories:
            for category, count in sorted(categories.items()):
                print(f"  📁 {category}: {count} animations")
            print(f"  📊 Total animations: {total_animations}")
        else:
            print("  ℹ️  No animation categories found")

    def analyze_output(self):
        """Analyze output directory"""
        self.print_header("🎥 OUTPUT & RENDERED CONTENT")

        output_dir = self.studio_root / "Output"

        if not output_dir.exists():
            print("  ❌ Output directory not found!")
            return

        # Count video files
        video_files = list(output_dir.rglob("*.mp4"))
        total_size_mb = sum(
            f.stat().st_size for f in video_files) / (1024 * 1024)

        print(f"  🎥 Rendered videos: {len(video_files)}")
        print(f"  💾 Total video size: {round(total_size_mb, 2)}MB")

        # Show recent videos (last 5)
        if video_files:
            recent_videos = sorted(
                video_files, key=lambda x: x.stat().st_mtime, reverse=True)[:5]
            print("  📅 Recent videos:")
            for video in recent_videos:
                size_mb = round(video.stat().st_size / (1024 * 1024), 1)
                mod_time = datetime.fromtimestamp(
                    video.stat().st_mtime).strftime("%m/%d %H:%M")
                print(f"    • {video.name} ({size_mb}MB) - {mod_time}")

    def analyze_diagnostics(self):
        """Analyze diagnostics system"""
        self.print_header("🔧 DIAGNOSTICS SYSTEM")

        diagnostics_dir = self.studio_root / "Diagnostics"

        if not diagnostics_dir.exists():
            print("  ❌ Diagnostics directory not found!")
            return

        # Diagnostic scripts
        scripts = [
            "health_monitor.py",
            "auto_repair.py",
            "emergency_recovery.py",
            "structure_report.py",
            "backup_manager.py"
        ]

        available_scripts = []
        for script in scripts:
            if (diagnostics_dir / script).exists():
                available_scripts.append(script)

        print(
            f"  📝 Diagnostic scripts: {len(available_scripts)}/{len(scripts)} available")
        for script in available_scripts:
            print(f"    ✅ {script}")

        # Backup system analysis
        self.analyze_backup_system()

    def analyze_backup_system(self):
        """Enhanced backup system analysis"""
        self.print_header("💾 ENHANCED BACKUP SYSTEM")

        if not self.backups_dir.exists():
            print("  ❌ Backups directory not found!")
            return

        # Count backup types
        enhanced_backups = list(self.backups_dir.glob("enhanced_python_*"))
        emergency_backups = list(self.backups_dir.glob("emergency_backup_*"))
        diagnostic_backups = list(self.backups_dir.glob("diagnostic_*"))

        print(f"  🔄 Enhanced backups: {len(enhanced_backups)}")
        print(f"  🚨 Emergency backups: {len(emergency_backups)}")
        print(f"  📊 Diagnostic backups: {len(diagnostic_backups)}")

        # Show latest enhanced backup
        if enhanced_backups:
            latest_backup = max(
                enhanced_backups, key=lambda x: x.stat().st_mtime)
            backup_size = self.get_folder_size(latest_backup)
            file_count = len(list(latest_backup.rglob('*')))
            mod_time = datetime.fromtimestamp(
                latest_backup.stat().st_mtime).strftime("%Y-%m-%d %H:%M")

            print(f"  📅 Latest enhanced backup:")
            print(f"    • {latest_backup.name}")
            print(f"    • {file_count} files, {backup_size}MB")
            print(f"    • Created: {mod_time}")

            # Check if restore script exists
            restore_script = latest_backup / "restore_python.bat"
            if restore_script.exists():
                print(f"    • ✅ Restore script: Available")
            else:
                print(f"    • ❌ Restore script: Missing")
        else:
            print("  ⚠️  No enhanced backups available")
            print("  💡 Run: create_enhanced_backup.bat")

    def analyze_dependencies(self):
        """Analyze installed dependencies"""
        self.print_header("📦 DEPENDENCIES & PACKAGES")

        site_packages = self.studio_root / "Lib" / "site-packages"

        if not site_packages.exists():
            print("  ❌ Site-packages directory not found!")
            return

        # Key packages to check
        key_packages = {
            'manim': 'Animation engine',
            'numpy': 'Numerical computing',
            'PIL': 'Image processing (Pillow)',
            'cairo': 'Vector graphics (PyCairo)',
            'manimpango': 'Text rendering',
            'scipy': 'Scientific computing',
            'matplotlib': 'Plotting library'
        }

        installed_count = 0
        for package, description in key_packages.items():
            package_path = site_packages / package
            if package_path.exists() or any(site_packages.glob(f"{package}*")):
                print(f"  ✅ {package}: {description}")
                installed_count += 1
            else:
                print(f"  ❌ {package}: MISSING - {description}")

        print(
            f"  📊 Installed: {installed_count}/{len(key_packages)} key packages")

        # Total package count
        all_packages = [p for p in site_packages.iterdir(
        ) if p.is_dir() and not p.name.endswith('.dist-info')]
        print(f"  📁 Total packages: {len(all_packages)}")

    def analyze_ffmpeg(self):
        """Analyze FFmpeg installation"""
        self.print_header("🎥 FFMPEG & MEDIA TOOLS")

        ffmpeg_dir = self.studio_root / "Lib" / "ffmpeg-8.0-essentials_build"

        if not ffmpeg_dir.exists():
            print("  ❌ FFmpeg directory not found!")
            return

        # Check critical executables
        executables = [
            ("ffmpeg.exe", "Video processing"),
            ("ffprobe.exe", "Media analysis"),
            ("ffplay.exe", "Media playback")
        ]

        available_tools = 0
        for exe, purpose in executables:
            exe_path = ffmpeg_dir / "bin" / exe
            if exe_path.exists():
                print(f"  ✅ {exe}: {purpose}")
                available_tools += 1
            else:
                print(f"  ❌ {exe}: MISSING - {purpose}")

        print(f"  📊 Available tools: {available_tools}/{len(executables)}")

        # FFmpeg directory size
        ffmpeg_size = self.get_folder_size(ffmpeg_dir)
        print(f"  💾 FFmpeg installation: {ffmpeg_size}MB")

    def generate_summary(self):
        """Generate overall system summary"""
        self.print_header("📊 SYSTEM SUMMARY")

        # Calculate totals
        total_dirs = len(
            [d for d in self.studio_root.rglob('*') if d.is_dir()])
        total_files = len(
            [f for f in self.studio_root.rglob('*') if f.is_file()])
        total_size = self.get_folder_size(self.studio_root)

        print(f"  📁 Total directories: {total_dirs}")
        print(f"  📄 Total files: {total_files}")
        print(f"  💾 Total size: {total_size}MB")
        print(
            f"  🗓️  Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # System health assessment
        critical_components = [
            ("Python Installation", self.studio_root /
             "Lib" / "python312" / "python.exe"),
            ("Animations", self.studio_root / "Animations"),
            ("Diagnostics", self.studio_root / "Diagnostics"),
            ("Enhanced Backups", self.backups_dir)
        ]

        healthy_components = sum(
            1 for name, path in critical_components if path.exists())

        print(
            f"  🏥 System health: {healthy_components}/{len(critical_components)} critical components")

        if healthy_components == len(critical_components):
            print("  ✅ System structure: HEALTHY")
        else:
            print("  ⚠️  System structure: NEEDS ATTENTION")

    def run_comprehensive_report(self):
        """Run full structure analysis"""
        print("\n" + "=" * 70)
        print("           EMANIM STUDIO - COMPREHENSIVE STRUCTURE REPORT")
        print("=" * 70)

        print(f"Studio Root: {self.studio_root}")
        print(f"Report Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        self.analyze_root_structure()
        self.analyze_python_environment()
        self.analyze_animations()
        self.analyze_output()
        self.analyze_dependencies()
        self.analyze_ffmpeg()
        self.analyze_diagnostics()
        self.generate_summary()

        print("\n" + "=" * 70)
        print("Report completed successfully! 🎉")
        print("=" * 70)

    def run_quick_report(self):
        """Run quick structure overview"""
        print("\n🚀 EMANIM STUDIO - QUICK STRUCTURE OVERVIEW")
        print("=" * 50)

        root_items = []
        for item in self.studio_root.iterdir():
            if item.name.startswith('.'):
                continue
            root_items.append(item)

        # Sort and display
        root_items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))

        print("📁 FOLDERS:")
        for item in root_items:
            if item.is_dir():
                item_count = len(list(item.rglob('*')))
                print(f"  📁 {item.name}/ ({item_count} items)")

        print("\n📄 FILES:")
        for item in root_items:
            if item.is_file():
                size_kb = round(item.stat().st_size / 1024, 1)
                print(f"  📄 {item.name} ({size_kb}KB)")

        # Quick stats
        total_dirs = len(
            [d for d in self.studio_root.rglob('*') if d.is_dir()])
        total_files = len(
            [f for f in self.studio_root.rglob('*') if f.is_file()])

        print(f"\n📊 Totals: {total_dirs} directories, {total_files} files")

        # Check enhanced backups
        enhanced_backups = list(self.backups_dir.glob(
            "enhanced_python_*")) if self.backups_dir.exists() else []
        print(f"💾 Enhanced backups: {len(enhanced_backups)} available")


def main():
    """Command-line interface"""
    import argparse

    parser = argparse.ArgumentParser(
        description='EmanimStudio Structure Report')
    parser.add_argument('--quick', action='store_true',
                        help='Run quick overview')
    parser.add_argument('--backups', action='store_true',
                        help='Show backup details only')
    parser.add_argument('--python', action='store_true',
                        help='Show Python details only')

    args = parser.parse_args()

    reporter = StructureReporter()

    if args.quick:
        reporter.run_quick_report()
    elif args.backups:
        reporter.analyze_backup_system()
    elif args.python:
        reporter.analyze_python_environment()
    else:
        reporter.run_comprehensive_report()


if __name__ == "__main__":
    main()
