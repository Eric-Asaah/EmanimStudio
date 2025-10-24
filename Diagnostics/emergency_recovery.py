#!/usr/bin/env python3
"""
EmanimStudio Emergency Recovery System v2.1
Enhanced with backup system integration and improved recovery options
"""
import sys
import os
import shutil
import zipfile
import subprocess
from pathlib import Path
from datetime import datetime


class EmergencyRecovery:
    def __init__(self):
        # Auto-detect paths
        current_file = Path(__file__)
        if current_file.parent.name == "Diagnostics":
            self.studio_root = current_file.parent.parent
            self.diagnostics_root = current_file.parent
        else:
            self.studio_root = current_file.parent
            self.diagnostics_root = self.studio_root / "Diagnostics"

        self.backups_dir = self.diagnostics_root / "backups"
        self.recovery_logs = self.diagnostics_root / "repair_logs" / "recovery"
        self.recovery_logs.mkdir(parents=True, exist_ok=True)

    def log_recovery(self, action: str, status: str = "INFO"):
        """Log recovery actions"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{status}] {action}\n"

        log_file = self.recovery_logs / \
            f"recovery_{datetime.now().strftime('%Y%m%d')}.log"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)

        print(f"🚨 {action}")

    def restore_from_enhanced_backup(self):
        """Restore from enhanced backup - PRIMARY RECOVERY METHOD"""
        self.log_recovery("ATTEMPTING ENHANCED BACKUP RESTORATION", "CRITICAL")

        # Find enhanced backups
        enhanced_backups = list(self.backups_dir.glob("enhanced_python_*"))
        if not enhanced_backups:
            self.log_recovery("No enhanced backups found", "ERROR")
            print("❌ No enhanced backups available for recovery")
            print("💡 Create an enhanced backup first using backup tools")
            return False

        # Get latest backup
        latest_backup = max(enhanced_backups, key=lambda x: x.stat().st_mtime)
        self.log_recovery(f"Found enhanced backup: {latest_backup.name}")

        print("🔄 Enhanced Backup Recovery")
        print("=" * 50)
        print(f"Backup: {latest_backup.name}")
        print(
            f"Created: {datetime.fromtimestamp(latest_backup.stat().st_mtime)}")
        print()
        print("This will:")
        print("• Backup current Python installation")
        print("• Restore working Python from enhanced backup")
        print("• Preserve your animations and outputs")
        print()

        response = input("Proceed with recovery? (y/N): ")
        if response.lower() != 'y':
            print("Recovery cancelled.")
            return False

        try:
            # Run the restore script from the backup
            restore_script = latest_backup / "restore_python.bat"
            if restore_script.exists():
                self.log_recovery(
                    f"Executing restore script: {restore_script}")

                # Run the batch file
                result = subprocess.run(
                    [str(restore_script)],
                    cwd=str(latest_backup),
                    capture_output=True,
                    text=True,
                    timeout=300  # 5 minute timeout
                )

                if result.returncode == 0:
                    self.log_recovery(
                        "Enhanced backup restoration completed successfully", "SUCCESS")
                    print("✅ Enhanced backup restoration completed!")
                    print("💡 Run 'diagnose.bat' to verify system health.")
                    return True
                else:
                    self.log_recovery(
                        f"Restore script failed with exit code {result.returncode}", "ERROR")
                    print(f"❌ Restore failed. Error: {result.stderr}")
                    return False
            else:
                self.log_recovery(
                    "Restore script not found in backup", "ERROR")
                print("❌ Restore script missing from backup")
                return False

        except subprocess.TimeoutExpired:
            self.log_recovery("Restore script timed out", "ERROR")
            print("❌ Restore timed out - system may be in unstable state")
            return False
        except Exception as e:
            self.log_recovery(f"Restore failed: {e}", "ERROR")
            print(f"❌ Restore failed: {e}")
            return False

    def nuclear_reset(self):
        """Complete system reset - use as last resort"""
        self.log_recovery("INITIATING NUCLEAR SYSTEM RESET", "CRITICAL")

        print("⚠️ " * 20)
        print("🚨 NUCLEAR SYSTEM RESET")
        print("⚠️ " * 20)
        print()
        print("THIS WILL:")
        print("• Delete ALL system files except your animations and outputs")
        print("• Restore from the most recent enhanced backup")
        print("• Recreate core system files")
        print("• Preserve your Animations/ and Output/ folders")
        print()
        print("THIS IS A DESTRUCTIVE OPERATION!")
        print()

        response = input("Type 'NUCLEAR RESET' to confirm: ")
        if response != "NUCLEAR RESET":
            print("Reset cancelled.")
            return False

        # Try enhanced backup first
        if self.restore_from_enhanced_backup():
            return True

        # Fallback to original nuclear reset
        return self._legacy_nuclear_reset()

    def _legacy_nuclear_reset(self):
        """Legacy nuclear reset when no enhanced backups exist"""
        self.log_recovery("Falling back to legacy nuclear reset", "WARNING")

        # Create emergency backup first
        self._create_emergency_backup()

        try:
            # Step 1: Preserve user data
            preserved_folders = ["Animations", "Output"]
            temp_preserve = self.studio_root / "TEMP_PRESERVE"
            temp_preserve.mkdir(exist_ok=True)

            for folder in preserved_folders:
                source = self.studio_root / folder
                if source.exists():
                    dest = temp_preserve / folder
                    shutil.copytree(source, dest, dirs_exist_ok=True)
                    self.log_recovery(f"Preserved {folder}")

            # Step 2: Remove all system files
            system_files_to_remove = [
                "Scripts",
                "Diagnostics",
                "EmanimStudio.bat",
                "diagnose.bat",
                "fix_environment.bat",
                "system_diagnostic_report.json",
                "python312._pth"
            ]

            for item in system_files_to_remove:
                path = self.studio_root / item
                if path.exists():
                    if path.is_file():
                        path.unlink()
                    else:
                        shutil.rmtree(path)
                    self.log_recovery(f"Removed {item}")

            # Step 3: Restore from latest backup (enhanced or zip)
            enhanced_backups = list(self.backups_dir.glob("enhanced_python_*"))
            zip_backups = list(self.backups_dir.glob("*.zip"))

            if enhanced_backups:
                latest_backup = max(
                    enhanced_backups, key=lambda x: x.stat().st_mtime)
                self.log_recovery(
                    f"Restoring from enhanced backup: {latest_backup.name}")
                restore_script = latest_backup / "restore_python.bat"
                if restore_script.exists():
                    subprocess.run([str(restore_script)],
                                   cwd=str(latest_backup))
            elif zip_backups:
                latest_backup = max(
                    zip_backups, key=lambda x: x.stat().st_mtime)
                self.log_recovery(
                    f"Restoring from zip backup: {latest_backup.name}")
                # Extract zip backup
                with zipfile.ZipFile(latest_backup, 'r') as zip_ref:
                    zip_ref.extractall(self.studio_root)
            else:
                self.log_recovery(
                    "No backups found - recreating basic structure", "WARNING")
                self._recreate_basic_structure()

            # Step 4: Restore preserved data
            for folder in preserved_folders:
                source = temp_preserve / folder
                if source.exists():
                    dest = self.studio_root / folder
                    shutil.copytree(source, dest, dirs_exist_ok=True)
                    self.log_recovery(f"Restored {folder}")

            # Clean up
            shutil.rmtree(temp_preserve)

            self.log_recovery(
                "NUCLEAR RESET COMPLETED SUCCESSFULLY", "SUCCESS")
            print("🎉 System has been completely reset and restored!")
            print("💡 Run 'diagnose.bat' to verify system health.")

            return True

        except Exception as e:
            self.log_recovery(f"NUCLEAR RESET FAILED: {e}", "CRITICAL")
            print("❌ Reset failed! System may be in unstable state.")
            print("💡 Check recovery logs and consider manual restoration.")
            return False

    def _create_emergency_backup(self):
        """Create emergency backup before destructive operations"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            emergency_dir = self.backups_dir / f"emergency_backup_{timestamp}"
            emergency_dir.mkdir(exist_ok=True)

            # Backup critical files
            critical_items = [
                "EmanimStudio.bat",
                "diagnose.bat",
                "fix_environment.bat",
                "Scripts",
                "Diagnostics"
            ]

            for item in critical_items:
                source = self.studio_root / item
                if source.exists():
                    if source.is_file():
                        shutil.copy2(source, emergency_dir / item)
                    else:
                        shutil.copytree(source, emergency_dir / item)

            self.log_recovery(
                f"Emergency backup created: {emergency_dir.name}")
            return True

        except Exception as e:
            self.log_recovery(f"Emergency backup failed: {e}", "WARNING")
            return False

    def _recreate_basic_structure(self):
        """Recreate basic system structure when no backup exists"""
        self.log_recovery("Recreating basic system structure")

        # Create essential directories
        essential_dirs = [
            "Scripts",
            "Diagnostics",
            "Animations/Math",
            "Animations/Physics",
            "Animations/Emanim",
            "Animations/Miscellaneous",
            "Output"
        ]

        for directory in essential_dirs:
            path = self.studio_root / directory
            path.mkdir(parents=True, exist_ok=True)

        # Create basic batch files
        self._create_basic_launcher()
        self._create_basic_diagnostics()

        self.log_recovery("Basic system structure recreated")

    def _create_basic_launcher(self):
        """Create basic EmanimStudio.bat"""
        bat_content = """@echo off
chcp 65001 >nul
title EmanimStudio - Recovery Mode
color 0C

echo.
echo ========================================
echo    EMANIMSTUDIO - RECOVERY MODE
echo ========================================
echo.
echo System is in recovery mode.
echo Please run diagnostics and repair tools.
echo.
pause
"""
        bat_file = self.studio_root / "EmanimStudio.bat"
        bat_file.write_text(bat_content)

    def _create_basic_diagnostics(self):
        """Create basic diagnostics script"""
        diag_content = '''import sys
print("EmanimStudio - Recovery Diagnostics")
print("System is in recovery mode.")
print("Please use emergency recovery tools.")
'''
        diag_file = self.studio_root / "Diagnostics" / "recovery_diagnostics.py"
        diag_file.write_text(diag_content)

    def repair_python_environment(self):
        """Emergency Python environment repair"""
        self.log_recovery("Performing emergency Python environment repair")

        python_dir = self.studio_root / "Lib" / "python312"
        if not python_dir.exists():
            self.log_recovery(
                "Python directory missing - cannot repair", "ERROR")
            return False

        # Repair ._pth file
        pth_file = python_dir / "python312._pth"
        pth_content = """python312.zip
.
DLLs
..\\..\\Lib\\site-packages
import site
"""
        pth_file.write_text(pth_content)
        self.log_recovery("Python ._pth file repaired")

        # Verify Python functionality
        try:
            result = subprocess.run([
                str(python_dir / "python.exe"),
                "-c", "import tkinter; print('Python + Tkinter OK')"
            ], capture_output=True, timeout=10)

            if result.returncode == 0:
                self.log_recovery("Python environment verified")
                return True
            else:
                self.log_recovery("Python environment still broken", "ERROR")
                return False

        except Exception as e:
            self.log_recovery(f"Python verification failed: {e}", "ERROR")
            return False

    def recover_from_github(self):
        """Attempt to recover by downloading from GitHub"""
        self.log_recovery("Attempting GitHub recovery")

        print("🌐 GitHub Recovery")
        print("This will attempt to download the latest version from GitHub.")
        print("Your local changes will be lost!")
        print()

        response = input("Continue? (y/N): ")
        if response.lower() != 'y':
            return False

        try:
            # Check if git is available
            result = subprocess.run(["git", "--version"], capture_output=True)
            if result.returncode != 0:
                self.log_recovery(
                    "Git not available - cannot use GitHub recovery", "ERROR")
                return False

            # Create backup first
            self._create_emergency_backup()

            # Reset to GitHub version
            os.chdir(self.studio_root)
            subprocess.run(["git", "fetch", "origin"], check=True)
            subprocess.run(["git", "reset", "--hard",
                           "origin/main"], check=True)
            subprocess.run(["git", "clean", "-fd"], check=True)

            self.log_recovery(
                "GitHub recovery completed successfully", "SUCCESS")
            print("✅ Successfully recovered from GitHub!")
            return True

        except Exception as e:
            self.log_recovery(f"GitHub recovery failed: {e}", "ERROR")
            return False

    def system_health_emergency(self):
        """Comprehensive emergency health check"""
        self.log_recovery("Running emergency health assessment")

        critical_components = [
            ("Python Installation", self.studio_root / "Lib" / "python312"),
            ("Manim Library", self.studio_root / "Lib" / "site-packages" / "manim"),
            ("FFmpeg", self.studio_root / "Lib" / "ffmpeg-8.0-essentials_build"),
            ("Main Launcher", self.studio_root / "EmanimStudio.bat"),
            ("Scripts Directory", self.studio_root / "Scripts"),
            ("Animations Directory", self.studio_root / "Animations"),
            ("Enhanced Backups", self.backups_dir)
        ]

        broken_components = []
        enhanced_backups = list(self.backups_dir.glob("enhanced_python_*"))

        for name, path in critical_components:
            if name == "Enhanced Backups":
                if enhanced_backups:
                    print(f"✅ {name} - {len(enhanced_backups)} available")
                else:
                    print(f"❌ {name} - NONE AVAILABLE")
                    broken_components.append(name)
            elif path.exists():
                print(f"✅ {name}")
            else:
                print(f"❌ {name} - MISSING")
                broken_components.append(name)

        if broken_components:
            print(f"\n🚨 {len(broken_components)} CRITICAL ISSUES FOUND")
            print("Recommended actions:")

            if "Python Installation" in broken_components:
                print("  • Use 'Enhanced Backup Restore' to fix Python")
            if "Enhanced Backups" in broken_components:
                print("  • Create enhanced backup immediately")
            if "Main Launcher" in broken_components or "Scripts Directory" in broken_components:
                print("  • Use 'Nuclear Reset' to restore system files")

            return False
        else:
            print("\n✅ All critical components present")
            print("💡 System can be recovered using enhanced backups")
            return True


def main():
    """Command-line interface for emergency recovery"""
    import argparse

    parser = argparse.ArgumentParser(
        description='EmanimStudio Emergency Recovery v2.1')
    parser.add_argument('--enhanced-restore', action='store_true',
                        help='Restore from enhanced backup (RECOMMENDED)')
    parser.add_argument('--nuclear-reset', action='store_true',
                        help='COMPLETE system reset (last resort)')
    parser.add_argument('--repair-python', action='store_true',
                        help='Emergency Python environment repair')
    parser.add_argument('--github-recovery', action='store_true',
                        help='Recover from GitHub (requires git)')
    parser.add_argument('--health-check', action='store_true',
                        help='Emergency health assessment')

    args = parser.parse_args()

    recovery = EmergencyRecovery()

    if args.enhanced_restore:
        recovery.restore_from_enhanced_backup()
    elif args.nuclear_reset:
        recovery.nuclear_reset()
    elif args.repair_python:
        recovery.repair_python_environment()
    elif args.github_recovery:
        recovery.recover_from_github()
    elif args.health_check:
        recovery.system_health_emergency()
    else:
        print("🚨 EmanimStudio Emergency Recovery System v2.1")
        print("Enhanced with backup system integration")
        print()
        print("Available commands:")
        print("  --enhanced-restore - Restore from enhanced backup (RECOMMENDED)")
        print("  --health-check     - Emergency system assessment")
        print("  --repair-python    - Fix Python environment")
        print("  --github-recovery  - Restore from GitHub")
        print("  --nuclear-reset    - COMPLETE system reset (LAST RESORT)")
        print()
        print("💡 Use '--enhanced-restore' for fastest recovery")


if __name__ == "__main__":
    main()
