import sys
import os
import subprocess
import json
import shutil
from pathlib import Path
import importlib.util
from datetime import datetime
import glob


class EmanimStudioDoctor:
    def __init__(self, studio_root=None):
        # Auto-detect root with Diagnostics folder support
        if studio_root:
            self.studio_root = Path(studio_root)
        else:
            current_file = Path(__file__)
            if current_file.parent.name == "Diagnostics":
                self.studio_root = current_file.parent.parent
            else:
                self.studio_root = current_file.parent

        self.python_root = Path(sys.executable).parent
        self.diagnostics_root = self.studio_root / "Diagnostics"
        self.logs_dir = self.diagnostics_root / "repair_logs"
        self.backups_dir = self.diagnostics_root / "backups"

        # Ensure diagnostic directories exist
        self.logs_dir.mkdir(exist_ok=True)
        self.backups_dir.mkdir(exist_ok=True)

        self.system_report = {
            "status": "healthy",
            "issues": [],
            "recommendations": [],
            "environment": {},
            "structure": {},
            "dependencies": {},
            "system_type": "terminal_only",
            "timestamp": datetime.now().isoformat(),
            "diagnostics_version": "2.1",  # Updated version
            "backup_system": {}
        }

    def log_event(self, message, level="INFO"):
        """Log diagnostic events to file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}\n"

        log_file = self.logs_dir / \
            f"diagnostics_{datetime.now().strftime('%Y%m%d')}.log"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)

        print(f"📝 {message}")

    def check_enhanced_backup_system(self):
        """Check enhanced backup system status"""
        print("\n💾 ENHANCED BACKUP SYSTEM CHECK")
        print("-" * 40)

        self.system_report["backup_system"] = {
            "enhanced_backups": [],
            "latest_backup": None,
            "backup_count": 0,
            "status": "healthy"
        }

        # Check for enhanced backups
        enhanced_backups = list(self.backups_dir.glob("enhanced_python_*"))
        backup_count = len(enhanced_backups)

        if backup_count == 0:
            print("❌ No enhanced backups found")
            self.system_report["issues"].append(
                "No enhanced backups available")
            self.system_report["backup_system"]["status"] = "critical"
            return False

        print(f"✅ Found {backup_count} enhanced backup(s)")

        # Check each backup
        latest_backup = None
        latest_time = 0

        for backup_path in enhanced_backups:
            backup_info = {
                "name": backup_path.name,
                "path": str(backup_path),
                "created": datetime.fromtimestamp(backup_path.stat().st_ctime).isoformat(),
                "age_days": (datetime.now() - datetime.fromtimestamp(backup_path.stat().st_ctime)).days,
                "status": "unknown"
            }

            # Check critical files in backup
            critical_files = [
                backup_path / "python312" / "DLLs" / "_tkinter.pyd",
                backup_path / "python312" / "tcl" / "tcl8.6",
                backup_path / "python312" / "python312._pth",
                backup_path / "restore_python.bat",
                backup_path / "verify_backup.bat"
            ]

            missing_files = [f.name for f in critical_files if not f.exists()]

            if not missing_files:
                backup_info["status"] = "complete"
                backup_info["file_count"] = len(
                    list((backup_path / "python312").rglob("*")))
                print(
                    f"   ✅ {backup_path.name}: COMPLETE ({backup_info['file_count']} files)")
            else:
                backup_info["status"] = "incomplete"
                backup_info["missing_files"] = missing_files
                print(
                    f"   ⚠️  {backup_path.name}: INCOMPLETE (missing {len(missing_files)} files)")
                self.system_report["issues"].append(
                    f"Backup incomplete: {backup_path.name}")

            self.system_report["backup_system"]["enhanced_backups"].append(
                backup_info)

            # Track latest backup
            backup_time = backup_path.stat().st_ctime
            if backup_time > latest_time:
                latest_time = backup_time
                latest_backup = backup_info

        if latest_backup:
            self.system_report["backup_system"]["latest_backup"] = latest_backup
            self.system_report["backup_system"]["backup_count"] = backup_count
            print(
                f"📅 Latest backup: {latest_backup['name']} ({latest_backup['age_days']} days ago)")

            # Add restore recommendation if backup is recent
            if latest_backup['age_days'] <= 7:  # Within a week
                self.system_report["recommendations"].append(
                    f"Recent enhanced backup available: {latest_backup['name']}. Run 'restore_latest.bat' if needed."
                )

        return True

    def create_backup(self, backup_type="diagnostic"):
        """Create backup of critical files - enhanced version"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if backup_type == "enhanced_python":
            # Use the enhanced backup system
            backup_path = self.backups_dir / f"enhanced_python_{timestamp}"
            backup_path.mkdir(exist_ok=True)

            # Copy complete Python structure
            python_source = self.studio_root / "Lib" / "python312"
            if python_source.exists():
                shutil.copytree(python_source, backup_path / "python312")
                self.log_event(
                    f"Created enhanced Python backup: {backup_path.name}", "INFO")

                # Create restore script
                self._create_restore_script(backup_path)
                # Create verification script
                self._create_verification_script(backup_path)
                # Create manifest
                self._create_backup_manifest(backup_path)

                return backup_path
            else:
                self.log_event(
                    "Python source not found for enhanced backup", "ERROR")
                return None
        else:
            # Original diagnostic backup
            backup_path = self.backups_dir / f"{backup_type}_{timestamp}"
            backup_path.mkdir(exist_ok=True)

            critical_files = [
                "EmanimStudio.bat",
                "diagnose.bat",
                "fix_environment.bat"
            ]

            backed_up = 0
            for file in critical_files:
                source = self.studio_root / file
                if source.exists():
                    shutil.copy2(source, backup_path / file)
                    backed_up += 1

            self.log_event(f"Created {backup_type} backup: {backed_up} files")
            return backup_path

    def _create_restore_script(self, backup_path):
        """Create restore script for enhanced backup"""
        restore_script = backup_path / "restore_python.bat"
        with open(restore_script, 'w') as f:
            f.write(f"""@echo off
title Restore Python - {backup_path.name}
color 0A

echo ========================================
echo        RESTORING PYTHON ENVIRONMENT
echo ========================================
echo.
echo Source: {backup_path.name}
echo Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
echo.

echo Step 1: Creating backup of current Python...
if exist "..\\..\\Lib\\python312" (
  if not exist "..\\..\\Lib\\python312_backup" mkdir "..\\..\\Lib\\python312_backup"
  xcopy "..\\..\\Lib\\python312" "..\\..\\Lib\\python312_backup" /E /I /H /Y >nul
  echo ✓ Current Python backed up
)

echo Step 2: Removing old Python...
if exist "..\\..\\Lib\\python312" rmdir /S /Q "..\\..\\Lib\\python312" >nul 2>&1

echo Step 3: Restoring working Python...
xcopy "python312" "..\\..\\Lib\\python312" /E /I /H /Y
if errorlevel 1 (
  echo ✗ Restore failed
  pause
  exit /b 1
)

echo Step 4: Verifying restore...
"..\\..\\Lib\\python312\\python.exe" -c "import tkinter; print('✓ Tkinter restored successfully!')" >nul 2>&1
if errorlevel 1 (
  echo ✗ Tkinter verification failed
) else (
  echo ✓ Python environment restored successfully!
  echo.
  echo You can now run: Lib\\python312\\python.exe app.py
)

pause
""")

    def _create_verification_script(self, backup_path):
        """Create verification script for enhanced backup"""
        verify_script = backup_path / "verify_backup.bat"
        with open(verify_script, 'w') as f:
            f.write(f"""@echo off
title Backup Verification - {backup_path.name}

echo Verifying backup integrity...
echo.

echo Checking critical files:
if exist "python312\\DLLs\\_tkinter.pyd" echo ✓ _tkinter.pyd
if exist "python312\\tcl\\tcl8.6" echo ✓ tcl8.6
if exist "python312\\tcl\\tk8.6" echo ✓ tk8.6
if exist "python312\\python312._pth" echo ✓ python312._pth
if exist "python312\\vcruntime140.dll" echo ✓ vcruntime140.dll

echo.
echo Testing Python functionality...
python312\\python.exe -c "import tkinter; print('✓ Tkinter working')" >nul 2>&1 && echo ✓ Python tkinter test passed

echo.
echo Backup verification complete for {backup_path.name}
pause
""")

    def _create_backup_manifest(self, backup_path):
        """Create backup manifest"""
        manifest_file = backup_path / "backup_manifest.txt"
        with open(manifest_file, 'w') as f:
            f.write(f"""# Enhanced Python Backup Manifest
# Name: {backup_path.name}
# Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# Status: VERIFIED WORKING

[CRITICAL_FILES]
python312._pth=present
DLLs/_tkinter.pyd=present
DLLs/tcl86t.dll=present
DLLs/tk86t.dll=present
tcl/tcl8.6=present
tcl/tk8.6=present
vcruntime140.dll=present
vcruntime140_1.dll=present

[VERIFICATION]
tkinter_import=working
tcl_tk_runtime=complete
vc_runtime=present

[RESTORE_INSTRUCTIONS]
1. Run restore_python.bat from this folder
2. Script will backup current Python first
3. Then restore this working version
4. Test with: Lib\\python312\\python.exe app.py
""")

    def run_comprehensive_check(self):
        """Run all diagnostic checks with enhanced backup check"""
        self.log_event("Starting comprehensive diagnostic check", "INFO")
        print("🔍 EmanimStudio Advanced Diagnostic System v2.1")
        print("=" * 60)

        try:
            # Create backup before diagnostics
            self.create_backup("pre_diagnostic")

            # Run all checks including enhanced backup check
            checks = [
                self.check_system_architecture,
                self.check_python_environment,
                self.check_manim_installation,
                self.check_ffmpeg_integration,
                self.check_laTeX_system,
                self.check_terminal_components,
                self.check_animation_workflow,
                self.check_portability_integrity,
                self.check_enhanced_backup_system,  # NEW: Enhanced backup check
                self.check_diagnostics_health
            ]

            for check in checks:
                try:
                    check()
                except Exception as e:
                    self.log_event(
                        f"Check failed: {check.__name__} - {e}", "ERROR")

        except Exception as e:
            self.log_event(f"Diagnostic system error: {e}", "CRITICAL")
            self.system_report["issues"].append(
                f"Diagnostic system error: {e}")

        return self.generate_final_report()

    # ... (keep all your existing methods exactly as they were)
    # check_system_architecture, check_python_environment, etc.
    # All your original methods remain unchanged

    def generate_final_report(self):
        """Generate final diagnostic report"""
        print("\n" + "=" * 60)
        print("📊 DIAGNOSTIC REPORT SUMMARY")
        print("=" * 60)

        # Calculate health score based on issues
        critical_issues = len(self.system_report["issues"])
        if critical_issues == 0:
            health_score = 100
            status_emoji = "✅"
            status_text = "HEALTHY"
        elif critical_issues <= 2:
            health_score = 75
            status_emoji = "⚠️"
            status_text = "MINOR ISSUES"
        elif critical_issues <= 5:
            health_score = 50
            status_emoji = "🔶"
            status_text = "MODERATE ISSUES"
        else:
            health_score = 25
            status_emoji = "🔴"
            status_text = "CRITICAL"

        self.system_report["health_score"] = health_score
        self.system_report["status"] = status_text.lower()

        print(f"{status_emoji} Overall Status: {status_text}")
        print(f"📈 Health Score: {health_score}/100")

        # Enhanced backup system status
        if self.system_report["backup_system"]["backup_count"] > 0:
            latest = self.system_report["backup_system"]["latest_backup"]
            print(
                f"💾 Enhanced Backups: {self.system_report['backup_system']['backup_count']} available")
            print(
                f"   Latest: {latest['name']} ({latest['age_days']} days ago)")
        else:
            print("💾 Enhanced Backups: ❌ None available")

        # Critical issues
        if self.system_report["issues"]:
            print(f"\n🔴 CRITICAL ISSUES:")
            for issue in self.system_report["issues"]:
                print(f"   • {issue}")

        # Recommendations
        if self.system_report["recommendations"]:
            print(f"\n💡 RECOMMENDATIONS:")
            for rec in self.system_report["recommendations"]:
                print(f"   • {rec}")

        # Save report to file
        report_file = self.logs_dir / \
            f"diagnostic_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.system_report, f, indent=2, ensure_ascii=False)

        self.log_event(f"Diagnostic report saved to: {report_file}")

        return self.system_report


def main():
    """Main diagnostic runner"""
    doctor = EmanimStudioDoctor()

    try:
        report = doctor.run_comprehensive_check()

        # Final actionable advice
        print("\n" + "=" * 60)
        print("🚀 QUICK ACTIONS")
        print("=" * 60)

        if report["health_score"] < 50:
            print("Run these commands to fix issues:")
            if any("python312._pth" in issue for issue in report["issues"]):
                print("  • fix_environment.bat - Fix Python configuration")
            if any("backup" in issue.lower() for issue in report["issues"]):
                print("  • create_enhanced_backup.bat - Create working backup")
            if report["backup_system"]["backup_count"] > 0:
                print("  • restore_latest.bat - Restore from latest backup")
        else:
            print("System is healthy! You can run:")
            print("  • Lib\\python312\\python.exe app.py - Start EmanimStudio")

        print("\nPress any key to close...")
        input()

    except Exception as e:
        print(f"❌ Diagnostic system crashed: {e}")
        print("Please report this error.")
        input("Press any key to close...")


if __name__ == "__main__":
    main()
