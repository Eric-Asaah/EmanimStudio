#!/usr/bin/env python3
"""
EmanimStudio Auto-Repair System v2.1
Enhanced with backup system integration and improved repair options
"""

import os
import sys
import shutil
from pathlib import Path
import json
from datetime import datetime
import subprocess


class EmanimAutoRepair:
    def __init__(self):
        # Get studio root (parent of Diagnostics folder)
        self.diagnostics_dir = Path(__file__).parent
        self.studio_root = self.diagnostics_dir.parent
        self.issues_fixed = []
        self.issues_found = []
        self.backups_dir = self.diagnostics_dir / "backups"

    def log(self, message, level="INFO"):
        """Print colored log messages"""
        colors = {
            "INFO": "\033[94m",     # Blue
            "SUCCESS": "\033[92m",   # Green
            "WARNING": "\033[93m",   # Yellow
            "ERROR": "\033[91m",     # Red
            "RESET": "\033[0m"
        }
        color = colors.get(level, colors["RESET"])
        print(f"{color}[{level}]{colors['RESET']} {message}")

    def check_enhanced_backups(self):
        """Check enhanced backup system status"""
        self.log("Checking enhanced backup system...", "INFO")

        enhanced_backups = list(self.backups_dir.glob("enhanced_python_*"))

        if not enhanced_backups:
            self.issues_found.append("No enhanced backups available")
            self.log("⚠ No enhanced backups found", "WARNING")
            self.log("  Create one using: backup_manager.bat", "INFO")
            return False
        else:
            latest_backup = max(
                enhanced_backups, key=lambda x: x.stat().st_mtime)
            self.log(
                f"✓ Enhanced backups available: {len(enhanced_backups)}", "SUCCESS")
            self.log(f"  Latest: {latest_backup.name}", "INFO")
            return True

    def check_python_pth(self):
        """Check and fix python312._pth file - ENHANCED VERSION"""
        self.log("Checking python312._pth configuration...", "INFO")

        pth_file = self.studio_root / "Lib" / "python312" / "python312._pth"

        if not pth_file.exists():
            self.issues_found.append("python312._pth file missing")
            self.create_python_pth(pth_file)
        else:
            # Verify content - ENHANCED: Include DLLs path
            content = pth_file.read_text()
            required_lines = [
                "python312.zip",
                ".",
                "DLLs",
                r"..\..\Lib\site-packages",
                "import site"
            ]

            missing_lines = [
                line for line in required_lines if line not in content]

            if missing_lines:
                self.issues_found.append(
                    f"python312._pth incomplete (missing: {', '.join(missing_lines)})")
                self.create_python_pth(pth_file)
            else:
                self.log("python312._pth is correctly configured", "SUCCESS")

    def create_python_pth(self, pth_file):
        """Create or fix python312._pth file - ENHANCED VERSION"""
        content = """python312.zip
.
DLLs
..\..\Lib\site-packages
..\..\Scripts
import site
"""
        try:
            pth_file.parent.mkdir(parents=True, exist_ok=True)
            pth_file.write_text(content)
            self.issues_fixed.append("Created/fixed python312._pth file")
            self.log(f"✓ Created python312._pth at {pth_file}", "SUCCESS")
        except Exception as e:
            self.log(f"✗ Failed to create python312._pth: {e}", "ERROR")

    def check_folder_structure(self):
        """Verify all required folders exist - ENHANCED VERSION"""
        self.log("Checking folder structure...", "INFO")

        required_folders = [
            "Animations/Math",
            "Animations/Physics",
            "Animations/Emaphy",
            "Animations/Miscellaneous",
            "Output",
            "Scripts",
            "Lib/python312",
            "Lib/site-packages",
            "Lib/ffmpeg-8.0-essentials_build",
            "Diagnostics/backups",
            "Diagnostics/repair_logs"
        ]

        for folder in required_folders:
            folder_path = self.studio_root / folder
            if not folder_path.exists():
                self.issues_found.append(f"Missing folder: {folder}")
                try:
                    folder_path.mkdir(parents=True, exist_ok=True)
                    self.issues_fixed.append(f"Created folder: {folder}")
                    self.log(f"✓ Created {folder}", "SUCCESS")
                except Exception as e:
                    self.log(f"✗ Failed to create {folder}: {e}", "ERROR")
            else:
                self.log(f"✓ {folder} exists", "INFO")

    def check_tkinter_functionality(self):
        """Check if tkinter is working - NEW CHECK"""
        self.log("Checking tkinter functionality...", "INFO")

        python_exe = self.studio_root / "Lib" / "python312" / "python.exe"
        if not python_exe.exists():
            self.issues_found.append("Python executable not found")
            self.log("✗ Python executable missing", "ERROR")
            return False

        try:
            result = subprocess.run([
                str(python_exe),
                "-c", "import tkinter; print('Tkinter OK')"
            ], capture_output=True, text=True, timeout=10)

            if result.returncode == 0:
                self.log("✓ Tkinter is working", "SUCCESS")
                return True
            else:
                self.issues_found.append("Tkinter import failed")
                self.log("✗ Tkinter not working", "ERROR")
                self.log("  Try restoring from enhanced backup", "INFO")
                return False

        except Exception as e:
            self.issues_found.append(f"Tkinter check failed: {e}")
            self.log(f"✗ Tkinter check error: {e}", "ERROR")
            return False

    def check_terminal_launcher(self):
        """Check if emanim_terminal.bat exists"""
        self.log("Checking terminal launcher...", "INFO")

        terminal_bat = self.studio_root / "emanim_terminal.bat"
        if not terminal_bat.exists():
            self.issues_found.append("emanim_terminal.bat missing")
            self.log("✗ emanim_terminal.bat not found", "WARNING")
            self.log("  Please create this file from the provided template", "INFO")
        else:
            self.log("✓ emanim_terminal.bat exists", "SUCCESS")

    def check_dependencies(self):
        """Check if critical Python packages are installed"""
        self.log("Checking Python dependencies...", "INFO")

        try:
            import manim
            self.log(f"✓ Manim {manim.__version__} installed", "SUCCESS")
        except ImportError:
            self.issues_found.append("Manim not found in site-packages")
            self.log("✗ Manim not installed", "ERROR")
            self.log("  Install with: pip install manim", "INFO")

        # Check other critical packages
        packages = ['numpy', 'pillow', 'pycairo', 'manimpango']
        for package in packages:
            try:
                __import__(package)
                self.log(f"✓ {package} installed", "SUCCESS")
            except ImportError:
                self.log(f"⚠ {package} not found (may be optional)", "WARNING")

    def check_ffmpeg(self):
        """Verify FFmpeg is accessible"""
        self.log("Checking FFmpeg...", "INFO")

        ffmpeg_path = self.studio_root / "Lib" / \
            "ffmpeg-8.0-essentials_build" / "bin" / "ffmpeg.exe"

        if ffmpeg_path.exists():
            self.log(f"✓ FFmpeg found at {ffmpeg_path}", "SUCCESS")
        else:
            self.issues_found.append("FFmpeg executable not found")
            self.log("✗ FFmpeg not found", "ERROR")

    def optimize_environment(self):
        """Create helper scripts for environment setup"""
        self.log("Creating environment helpers...", "INFO")

        # Create a quick test script
        test_script = self.studio_root / "test_manim.bat"
        test_content = """@echo off
echo Testing Manim Installation...
echo.
Lib\\python312\\python.exe -c "import manim; print(f'Manim {manim.__version__} - OK')"
if errorlevel 1 (
    echo [ERROR] Manim test failed!
) else (
    echo [SUCCESS] Manim is working!
)
echo.
pause
"""
        try:
            test_script.write_text(test_content)
            self.issues_fixed.append("Created test_manim.bat helper")
            self.log("✓ Created test_manim.bat", "SUCCESS")
        except Exception as e:
            self.log(f"✗ Failed to create test script: {e}", "ERROR")

    def create_enhanced_backup(self):
        """Create an enhanced backup if none exist"""
        self.log("Checking if enhanced backup creation is needed...", "INFO")

        enhanced_backups = list(self.backups_dir.glob("enhanced_python_*"))
        if not enhanced_backups:
            self.log(
                "No enhanced backups found - suggesting creation...", "WARNING")
            self.log("  Run: create_enhanced_backup.bat", "INFO")

            # Check if the backup script exists
            backup_script = self.studio_root / "create_enhanced_backup.bat"
            if backup_script.exists():
                self.log("✓ Enhanced backup script available", "SUCCESS")
            else:
                self.issues_found.append("Enhanced backup tools not available")
                self.log("✗ Enhanced backup tools missing", "ERROR")
        else:
            self.log(
                f"✓ Enhanced backups available: {len(enhanced_backups)}", "SUCCESS")

    def repair_tkinter_emergency(self):
        """Emergency tkinter repair using enhanced backups"""
        self.log("Checking tkinter emergency repair options...", "INFO")

        # Check if tkinter is broken
        python_exe = self.studio_root / "Lib" / "python312" / "python.exe"
        if not python_exe.exists():
            return False

        try:
            result = subprocess.run([
                str(python_exe),
                "-c", "import tkinter"
            ], capture_output=True, text=True, timeout=10)

            if result.returncode != 0:
                self.issues_found.append("Tkinter is broken")
                self.log("✗ Tkinter requires emergency repair", "ERROR")

                # Check if we have enhanced backups for recovery
                enhanced_backups = list(
                    self.backups_dir.glob("enhanced_python_*"))
                if enhanced_backups:
                    latest_backup = max(
                        enhanced_backups, key=lambda x: x.stat().st_mtime)
                    self.log(
                        f"✓ Recovery available from: {latest_backup.name}", "SUCCESS")
                    self.log("  Run: restore_latest.bat", "INFO")
                    return True
                else:
                    self.log("✗ No recovery backups available", "ERROR")
                    return False
            else:
                self.log("✓ Tkinter is functional", "SUCCESS")
                return True

        except Exception as e:
            self.log(f"✗ Tkinter check failed: {e}", "ERROR")
            return False

    def check_python_dlls(self):
        """Check if Python DLLs are properly configured"""
        self.log("Checking Python DLL configuration...", "INFO")

        python_dir = self.studio_root / "Lib" / "python312"
        dlls_dir = python_dir / "DLLs"

        critical_dlls = [
            "_tkinter.pyd",
            "tcl86t.dll",
            "tk86t.dll"
        ]

        missing_dlls = []
        for dll in critical_dlls:
            dll_path = dlls_dir / dll
            if not dll_path.exists():
                # Also check root directory
                root_dll_path = python_dir / dll
                if not root_dll_path.exists():
                    missing_dlls.append(dll)

        if missing_dlls:
            self.issues_found.append(
                f"Missing critical DLLs: {', '.join(missing_dlls)}")
            self.log(f"✗ Missing DLLs: {missing_dlls}", "ERROR")
            self.log("  These are required for tkinter functionality", "INFO")
            return False
        else:
            self.log("✓ All critical DLLs present", "SUCCESS")
            return True

    def generate_report(self):
        """Generate repair report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "studio_root": str(self.studio_root),
            "issues_found": self.issues_found,
            "issues_fixed": self.issues_fixed,
            "status": "HEALTHY" if not self.issues_found else "NEEDS_ATTENTION"
        }

        report_file = self.diagnostics_dir / "repair_log.json"
        try:
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)
            self.log(f"✓ Report saved to {report_file}", "SUCCESS")
        except Exception as e:
            self.log(f"✗ Failed to save report: {e}", "ERROR")

        return report

    def run_full_repair(self):
        """Run all repair checks"""
        print("\n" + "="*60)
        print("  EMANIM STUDIO AUTO-REPAIR SYSTEM v2.1")
        print("="*60 + "\n")

        self.check_python_pth()
        print()

        self.check_folder_structure()
        print()

        self.check_python_dlls()
        print()

        self.check_tkinter_functionality()
        print()

        self.check_terminal_launcher()
        print()

        self.check_dependencies()
        print()

        self.check_ffmpeg()
        print()

        self.check_enhanced_backups()
        print()

        self.repair_tkinter_emergency()
        print()

        self.create_enhanced_backup()
        print()

        self.optimize_environment()
        print()

        report = self.generate_report()

        print("\n" + "="*60)
        print("  REPAIR SUMMARY")
        print("="*60)
        print(f"\nIssues Found: {len(self.issues_found)}")
        for issue in self.issues_found:
            print(f"  ⚠ {issue}")

        print(f"\nIssues Fixed: {len(self.issues_fixed)}")
        for fix in self.issues_fixed:
            print(f"  ✓ {fix}")

        print(f"\nOverall Status: {report['status']}")

        # Provide actionable recommendations
        if self.issues_found:
            print(f"\n💡 RECOMMENDED ACTIONS:")
            if any("tkinter" in issue.lower() for issue in self.issues_found):
                print("  • Run: restore_latest.bat - Fix tkinter with enhanced backup")
            if any("backup" in issue.lower() for issue in self.issues_found):
                print("  • Run: create_enhanced_backup.bat - Create recovery point")
            if any("python312._pth" in issue for issue in self.issues_found):
                print("  • Python path configuration was automatically fixed")
            if any("folder" in issue.lower() for issue in self.issues_found):
                print("  • Missing folders were automatically created")

        print("\n" + "="*60 + "\n")

        return report


def main():
    """Command-line interface for auto-repair"""
    import argparse

    parser = argparse.ArgumentParser(
        description='EmanimStudio Auto-Repair System')
    parser.add_argument('--quick', action='store_true',
                        help='Run quick repairs only')
    parser.add_argument('--fix-tkinter', action='store_true',
                        help='Focus on tkinter repair')
    parser.add_argument('--create-backup', action='store_true',
                        help='Create enhanced backup')

    args = parser.parse_args()

    repair = EmanimAutoRepair()

    if args.quick:
        print("🚀 Running Quick Auto-Repair...")
        repair.check_python_pth()
        repair.check_folder_structure()
        repair.check_tkinter_functionality()
    elif args.fix_tkinter:
        print("🔧 Focusing on Tkinter Repair...")
        repair.check_python_dlls()
        repair.check_tkinter_functionality()
        repair.repair_tkinter_emergency()
    elif args.create_backup:
        repair.create_enhanced_backup()
    else:
        report = repair.run_full_repair()

    # Return appropriate exit code
    if repair.issues_found:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
