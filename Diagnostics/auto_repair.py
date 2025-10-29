#!/usr/bin/env python3
"""
EmanimStudio Auto-Repair System v2.2 (PyQt5 Version)
Updated with correct folder names from your actual structure
FIXED: All absolute paths removed, using relative paths only
"""

import os
import sys
import shutil
from pathlib import Path
import json
import argparse
from datetime import datetime
import subprocess
import platform

def find_studio_root():
    """Detect the main EmanimStudio root directory."""
    current_file = Path(__file__).resolve()
    if current_file.parent.name == "Diagnostics":
        return current_file.parent.parent
    else:
        return current_file.parent

class EmanimAutoRepair:
    def __init__(self):
        self.studio_root = find_studio_root()
        self.diagnostics_dir = self.studio_root / "Diagnostics"
        self.issues_fixed = []
        self.issues_found = []
        self.backups_dir = self.diagnostics_dir / "backups"
        self.logs_dir = self.diagnostics_dir / "repair_logs"
        
        # CORRECTED PATHS - using your actual folder names
        self.python_exe_path = self.studio_root / "Lib" / "Python312" / ("python.exe" if platform.system() == "Windows" else "python")
        self.python_dir = self.python_exe_path.parent
        
        # CORRECTED: Your FFmpeg folder is "FFmpeg" not "ffmpeg-8.0-essentials_build"
        self.ffmpeg_exe_path = self.studio_root / "Lib" / "FFmpeg" / "bin" / "ffmpeg.exe"
        
        # CORRECTED: Your MiKTeX folder is "Miktex" (lowercase 't')
        self.miktex_bin = self.studio_root / "Lib" / "Miktex" / "texmfs" / "install" / "miktex" / "bin" / "x64"

        # Ensure necessary diagnostic folders exist
        self.logs_dir.mkdir(exist_ok=True)
        self.backups_dir.mkdir(exist_ok=True)

    def log(self, message, level="INFO"):
        """Print colored log messages and save to file"""
        print(f"[{level}] {message}")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        log_file = self.logs_dir / f"auto_repair_{datetime.now().strftime('%Y%m%d')}.log"
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"[ERROR] Failed to write to log file {log_file}: {e}")

    def check_python_pth(self):
        """Check and fix python312._pth file"""
        self.log("Checking python312._pth configuration...", "INFO")
        pth_fixed = False
        pth_file = self.python_dir / "python312._pth"

        if not self.python_dir.exists():
             self.log(f"✗ Python directory not found ({self.python_dir}), cannot check .pth file.", "ERROR")
             self.issues_found.append("Python directory missing")
             return False

        if not pth_file.exists():
            self.issues_found.append(f"{pth_file.name} file missing")
            self.log(f"✗ {pth_file.name} missing.", "WARNING")
            pth_fixed = self.create_python_pth(pth_file)
        else:
            try:
                content = pth_file.read_text(encoding='utf-8')
                # Required lines for embeddable python finding site-packages and scripts
                required_lines_map = {
                    "python312.zip": False,
                    ".": False,
                    # CORRECTED: site-packages is inside python312/Lib/
                    str(Path("Lib") / "site-packages").replace('\\','/'): False,
                    "import site": False
                }

                lines_in_file = [line.strip().replace('\\','/') for line in content.splitlines() if line.strip() and not line.strip().startswith('#')]

                missing_lines_keys = []
                for req_line in required_lines_map.keys():
                     req_line_norm = req_line.replace('\\','/')
                     if req_line_norm not in lines_in_file:
                          missing_lines_keys.append(req_line)
                     else:
                          required_lines_map[req_line] = True

                if missing_lines_keys:
                    self.issues_found.append(
                        f"{pth_file.name} incomplete (missing: {', '.join(missing_lines_keys)})")
                    self.log(f"✗ {pth_file.name} incomplete. Missing: {missing_lines_keys}", "WARNING")
                    pth_fixed = self.create_python_pth(pth_file)
                else:
                    self.log(f"✓ {pth_file.name} is correctly configured", "SUCCESS")
                    return True

            except Exception as e:
                self.log(f"✗ Error reading or parsing {pth_file.name}: {e}", "ERROR")
                self.issues_found.append(f"Error accessing {pth_file.name}")
                pth_fixed = self.create_python_pth(pth_file)

        return pth_fixed

    def create_python_pth(self, pth_file):
        """Create or fix python312._pth file"""
        self.log(f"Attempting to create/fix {pth_file.name}...", "INFO")
        # CORRECTED: site-packages path is inside python312/Lib/
        content = """python312.zip
.
Lib/site-packages
import site
"""
        try:
            pth_file.parent.mkdir(parents=True, exist_ok=True)
            pth_file.write_text(content, encoding='utf-8')
            if f"{pth_file.name} file missing" in self.issues_found or \
               any(f"{pth_file.name} incomplete" in issue for issue in self.issues_found):
                self.issues_fixed.append(f"Created/fixed {pth_file.name} file")
            self.log(f"✓ Successfully wrote {pth_file.name}", "SUCCESS")
            return True
        except Exception as e:
            self.log(f"✗ Failed to create/write {pth_file.name}: {e}", "ERROR")
            if f"Failed to fix {pth_file.name}" not in self.issues_found:
                 self.issues_found.append(f"Failed to fix {pth_file.name}")
            return False

    def check_folder_structure(self):
        """Verify essential folders exist with CORRECT names"""
        self.log("Checking folder structure...", "INFO")
        all_folders_ok = True

        # CORRECTED: Using your actual folder names
        required_folders_relative = [
            Path("Animations") / "Math", 
            Path("Animations") / "Physics",
            Path("Animations") / "Emaphy", 
            Path("Animations") / "Miscellaneous",
            Path("Output"),
            Path("Lib") / "Python312",  # FIXED: Capital P in Python312
            Path("Lib") / "FFmpeg",  # CORRECTED: "FFmpeg" not "ffmpeg-8.0-essentials_build"
            Path("Lib") / "Miktex",  # CORRECTED: "Miktex" not "MiKTeX"
            Path("Diagnostics") / "backups", 
            Path("Diagnostics") / "repair_logs"
        ]

        for folder_rel in required_folders_relative:
            folder_path = self.studio_root / folder_rel
            check_msg = f"Checking: {folder_rel}... "
            if not folder_path.exists():
                all_folders_ok = False
                issue_msg = f"Missing folder: {folder_rel}"
                if issue_msg not in self.issues_found: 
                    self.issues_found.append(issue_msg)
                try:
                    os.makedirs(folder_path, exist_ok=True)
                    fix_msg = f"Created folder: {folder_rel}"
                    if fix_msg not in self.issues_fixed: 
                        self.issues_fixed.append(fix_msg)
                    self.log(f"✓ {check_msg} MISSING -> CREATED", "SUCCESS")
                except Exception as e:
                    self.log(f"✗ {check_msg} FAILED TO CREATE: {e}", "ERROR")
            else:
                self.log(f"✓ {folder_rel} exists", "INFO")

        if all_folders_ok and not any("Missing folder" in issue for issue in self.issues_found):
             self.log("✓ Essential folder structure is OK.", "SUCCESS")

        return all_folders_ok

    def check_terminal_launcher(self):
        """Check if EmanimStudio.bat exists"""
        self.log("Checking terminal launcher (emanim_terminal.bat)...", "INFO")
        # FIXED: Looking for emanim_terminal.bat (your actual terminal file)
        terminal_bat = self.studio_root / "emanim_terminal.bat"
        if not terminal_bat.exists():
            issue_msg = "emanim_terminal.bat missing"
            if issue_msg not in self.issues_found: 
                self.issues_found.append(issue_msg)
            self.log("✗ emanim_terminal.bat not found in root directory", "WARNING")
            self.log("  The main terminal interface cannot be launched without this file.", "INFO")
            return False
        else:
            self.log("✓ emanim_terminal.bat exists", "SUCCESS")
            return True

    def check_main_launcher(self):
        """Check if main.py exists"""
        self.log("Checking main GUI launcher (main.py)...", "INFO")
        # CORRECTED: Looking for main.py (your GUI file)
        launcher_py = self.studio_root / "main.py"
        if not launcher_py.exists():
            issue_msg = "main.py missing"
            if issue_msg not in self.issues_found: 
                self.issues_found.append(issue_msg)
            self.log("✗ main.py not found in root directory", "ERROR")
            self.log("  The main GUI cannot be launched without this file.", "INFO")
            return False
        else:
            self.log("✓ main.py exists", "SUCCESS")
            return True

    def check_dependencies(self):
        """Check if critical Python packages are installed"""
        self.log("Checking Python dependencies (PyQt5, Manim, NumPy, etc.)...", "INFO")
        all_deps_ok = True

        if not self.python_exe_path.exists():
            issue_msg = "Python executable not found for dependency check"
            if issue_msg not in self.issues_found: 
                self.issues_found.append(issue_msg)
            self.log("✗ Python executable missing, cannot check dependencies", "ERROR")
            return False

        packages_to_check = {
            "PyQt5": True,
            "manim": True,
            "numpy": True,
            "Pillow": True,
            "pycairo": False,
            "manimpango": False,
        }
        missing_critical = []
        missing_optional = []

        sub_env = os.environ.copy()
        # CORRECTED: site-packages is inside Python312
        sub_env["PYTHONPATH"] = str(self.python_dir / "Lib" / "site-packages") + os.pathsep + sub_env.get("PYTHONPATH", "")

        for pkg_name, is_critical in packages_to_check.items():
             import_name = "PIL" if pkg_name == "Pillow" else pkg_name
             check_cmd = f"import {import_name}; print('{pkg_name} OK')"
             try:
                 result = subprocess.run(
                     [str(self.python_exe_path), "-c", check_cmd],
                     capture_output=True, text=True, check=True, timeout=10,
                     cwd=self.python_dir, env=sub_env
                 )
                 self.log(f"✓ Dependency Check: {pkg_name} installed", "SUCCESS")
             except subprocess.CalledProcessError as e:
                 all_deps_ok = False
                 issue_msg = f"Dependency missing: {pkg_name}"
                 log_msg = f"✗ Dependency Check: {pkg_name} NOT FOUND"
                 if is_critical:
                     if issue_msg not in self.issues_found: 
                         self.issues_found.append(issue_msg)
                     self.log(log_msg, "ERROR")
                     missing_critical.append(pkg_name)
                 else:
                     self.log(log_msg + " (Optional)", "WARNING")
                     missing_optional.append(pkg_name)
             except subprocess.TimeoutExpired:
                  self.log(f"✗ Dependency Check Timeout: {pkg_name}", "ERROR")
                  issue_msg = f"Timeout checking dependency: {pkg_name}"
                  if issue_msg not in self.issues_found: 
                      self.issues_found.append(issue_msg)
                  all_deps_ok = False
             except Exception as e:
                 self.log(f"✗ Dependency Check Error ({pkg_name}): {e}", "ERROR")
                 issue_msg = f"Error checking dependency {pkg_name}"
                 if issue_msg not in self.issues_found: 
                     self.issues_found.append(issue_msg)
                 all_deps_ok = False

        if missing_critical:
            self.log("  Recommendation: Install missing critical dependencies", "INFO")
        if missing_optional:
             self.log("  Note: Missing optional dependencies might affect certain Manim features.", "INFO")

        return all_deps_ok

    def check_ffmpeg(self):
        """Verify FFmpeg executable exists and is runnable"""
        self.log("Checking FFmpeg executable...", "INFO")
        # CORRECTED: Using your actual FFmpeg path
        ffmpeg_ok = False

        if not self.ffmpeg_exe_path.parent.exists():
             log_msg = f"✗ FFmpeg bin directory not found: {self.ffmpeg_exe_path.parent}"
             issue_msg = "FFmpeg directory missing"
             self.log(log_msg, "ERROR")
             if issue_msg not in self.issues_found: 
                 self.issues_found.append(issue_msg)
        elif not self.ffmpeg_exe_path.exists():
            log_msg = f"✗ ffmpeg.exe not found at {self.ffmpeg_exe_path}"
            issue_msg = "ffmpeg.exe executable not found"
            self.log(log_msg, "ERROR")
            if issue_msg not in self.issues_found: 
                self.issues_found.append(issue_msg)
        else:
            self.log(f"✓ ffmpeg.exe found at {self.ffmpeg_exe_path}", "INFO")
            try:
                result = subprocess.run(
                    [str(self.ffmpeg_exe_path), "-version"],
                    capture_output=True, text=True, timeout=5, check=True,
                    creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
                )
                if "ffmpeg version" in result.stdout.lower():
                     self.log("✓ FFmpeg execution test successful", "SUCCESS")
                     ffmpeg_ok = True
                else:
                     self.log("⚠ FFmpeg ran but output unexpected (might still work)", "WARNING")
                     ffmpeg_ok = True
            except subprocess.TimeoutExpired:
                 log_msg = "✗ FFmpeg execution timed out"
                 issue_msg = "FFmpeg timed out"
                 self.log(log_msg, "ERROR")
                 if issue_msg not in self.issues_found: 
                     self.issues_found.append(issue_msg)
            except Exception as e:
                log_msg = f"✗ FFmpeg execution test failed: {e}"
                issue_msg = f"FFmpeg execution error: {e}"
                self.log(log_msg, "ERROR")
                if issue_msg not in self.issues_found: 
                    self.issues_found.append(issue_msg)

        if not ffmpeg_ok:
             self.log("  Recommendation: Ensure FFmpeg is correctly extracted in Lib/FFmpeg", "INFO")

        return ffmpeg_ok

    def check_miktex(self):
        """Verify MiKTeX exists"""
        self.log("Checking MiKTeX installation...", "INFO")
        # CORRECTED: Using your actual MiKTeX path
        miktex_ok = False

        if not self.miktex_bin.exists():
            log_msg = f"✗ MiKTeX bin directory not found: {self.miktex_bin}"
            issue_msg = "MiKTeX directory missing"
            self.log(log_msg, "WARNING")
            if issue_msg not in self.issues_found: 
                self.issues_found.append(issue_msg)
        else:
            miktex_exe = self.miktex_bin / "miktex.exe"
            if miktex_exe.exists():
                self.log("✓ MiKTeX found", "SUCCESS")
                miktex_ok = True
            else:
                self.log("⚠ MiKTeX directory exists but miktex.exe not found", "WARNING")
                miktex_ok = True  # Still consider it OK for now

        return miktex_ok

    def optimize_environment(self):
        """Create helper batch scripts for common tasks"""
        self.log("Creating/updating helper scripts...", "INFO")
        helpers_created = False
        fix_applied = False

        # CORRECTED: Using your actual Python path
        python_rel_path = Path("Lib") / "Python312" / "python.exe"  # FIXED: Capital P
        
        # test_manim.bat
        test_manim_script = self.studio_root / "test_manim.bat"
        test_manim_content = f"""@echo off
echo Testing Manim Installation...
echo Running from: %~dp0
echo Python Executable: %~dp0{python_rel_path}
echo.
if not exist "%~dp0{python_rel_path}" (
    echo [ERROR] Python not found at expected location!
    pause
    exit /b 1
)
"%~dp0{python_rel_path}" -c "import manim; print(f'Manim {{manim.__version__}} - OK')"
if errorlevel 1 (
    echo [ERROR] Manim import failed! Check Python path and installation in site-packages.
) else (
    echo [SUCCESS] Manim seems to be working!
)
echo.
pause
"""
        try:
            needs_update = not test_manim_script.exists() or test_manim_script.read_text(encoding='utf-8') != test_manim_content
            if needs_update:
                test_manim_script.write_text(test_manim_content, encoding='utf-8')
                self.log("✓ Created/updated test_manim.bat", "SUCCESS")
                if "Created/updated helper batch scripts" not in self.issues_fixed:
                     self.issues_fixed.append("Created/updated helper batch scripts")
                helpers_created = True
                fix_applied = True
        except Exception as e:
            self.log(f"✗ Failed to create/update test_manim.bat: {e}", "ERROR")
            if "Failed helper script: test_manim.bat" not in self.issues_found:
                self.issues_found.append("Failed helper script: test_manim.bat")

        return fix_applied

    def generate_report(self):
        """Generate and save the final repair report - FIXED VERSION"""
        self.log("Generating final repair report...", "INFO")
        # Determine health based ONLY on remaining unfixed issues
        unfixed_issues = [issue for issue in self.issues_found
                          if not any(fix in issue or issue in fix for fix in self.issues_fixed)]
        unfixed_count = len(unfixed_issues)

        # FIXED: Calculate proper health score
        total_issues = len(self.issues_found)
        if total_issues == 0:
            health_score = 100
            health_status = "HEALTHY"
        else:
            fixed_count = len(self.issues_fixed)
            health_score = int((fixed_count / total_issues) * 100)
            
            # Adjust based on remaining issues
            if unfixed_count > 0:
                health_score = max(20, health_score - (unfixed_count * 10))
            
            # Set status based on score
            if health_score >= 80:
                health_status = "HEALTHY"
            elif health_score >= 50:
                health_status = "NEEDS_ATTENTION" 
            else:
                health_status = "PROBLEMS_DETECTED"

        report = {
            "timestamp": datetime.now().isoformat(),
            "studio_root": str(self.studio_root),
            "issues_found_count": len(self.issues_found),
            "issues_fixed_count": len(self.issues_fixed),
            "issues_found_details": self.issues_found,
            "issues_fixed_details": self.issues_fixed,
            "health_score": health_score,
            "final_status": "REPAIRS_ATTEMPTED" if self.issues_fixed else "CHECK_COMPLETE",
            "overall_health": health_status,
            "unfixed_issues_count": unfixed_count,
            "unfixed_issues_details": unfixed_issues
        }

        report_filename = f"auto_repair_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_file_path = self.logs_dir / report_filename
        try:
            self.logs_dir.mkdir(parents=True, exist_ok=True)
            with open(report_file_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=4)
            self.log(f"✓ Detailed report saved to: Diagnostics\\repair_logs\\{report_filename}", "SUCCESS")
        except Exception as e:
            self.log(f"✗ Failed to save detailed report to {report_file_path}: {e}", "ERROR")

        return report

    def run_full_repair(self):
        """Run all relevant repair checks and fixes"""
        print("\n" + "="*60)
        print("    EMANIM STUDIO AUTO-REPAIR SYSTEM v2.2 (Updated Paths)")
        print("="*60 + "\n")
        self.log("Starting full auto-repair process...", "INFO")

        # CORRECTED: Added MiKTeX check
        repair_steps = [
            self.check_folder_structure,
            self.check_python_pth,
            self.check_terminal_launcher,
            self.check_main_launcher,
            self.check_dependencies,
            self.check_ffmpeg,
            self.check_miktex,  # NEW: Check MiKTeX
            self.optimize_environment,
        ]

        for step_func in repair_steps:
            try:
                self.log(f"--- Running Step: {step_func.__name__} ---", "INFO")
                step_func()
                print("-" * 40)
            except Exception as e:
                 self.log(f"ERROR during step {step_func.__name__}: {e}", "CRITICAL")
                 if f"Repair step {step_func.__name__} crashed: {e}" not in self.issues_found:
                      self.issues_found.append(f"Repair step {step_func.__name__} crashed: {e}")
                 print(f"❌ CRITICAL ERROR during {step_func.__name__}. See logs.")
                 print("-" * 40)

        report = self.generate_report()

        print("\n" + "="*60)
        print("    REPAIR SUMMARY")
        print("="*60)

        found_count = report["issues_found_count"]
        fixed_count = report["issues_fixed_count"]
        unfixed_count = report["unfixed_issues_count"]
        final_health = report["overall_health"]

        if found_count > 0:
            print(f"\n{found_count} potential issue(s) detected during the scan.")
        if fixed_count > 0:
            print(f"{fixed_count} issue(s) were automatically fixed/addressed:")
            for fix in report["issues_fixed_details"][:5]:
                print(f"  ✓ {fix}")
            if fixed_count > 5: 
                print(f"  ... and {fixed_count - 5} more.")

        if unfixed_count > 0:
             print(f"\n{unfixed_count} issue(s) remain and require attention:")
             for issue in report["unfixed_issues_details"][:5]:
                  print(f"  ⚠ {issue}")
             if unfixed_count > 5: 
                 print(f"  ... and {unfixed_count - 5} more (see report file).")

        print(f"\nOverall Status: {final_health}")

        if final_health != "HEALTHY":
            print(f"\n💡 RECOMMENDED ACTIONS:")
            suggestions = set()
            unfixed_list = report["unfixed_issues_details"]

            if any("dependency missing" in issue.lower() for issue in unfixed_list):
                 suggestions.add("Install missing Python dependencies using pip.")
            if any("FFmpeg" in issue for issue in unfixed_list):
                 suggestions.add("Ensure FFmpeg is correctly extracted in Lib/FFmpeg folder.")
            if any("MiKTeX" in issue for issue in unfixed_list):
                 suggestions.add("Ensure MiKTeX is correctly extracted in Lib/Miktex folder.")
            if any("emanim_terminal.bat missing" in issue for issue in unfixed_list):
                 suggestions.add("Restore emanim_terminal.bat from a backup or template.")
            if any("main.py missing" in issue for issue in unfixed_list):
                 suggestions.add("Restore main.py. The GUI cannot start without it.")
            if any("Python executable missing" in issue for issue in unfixed_list):
                 suggestions.add("CRITICAL: Python runtime is missing. Re-extract the portable Python folder.")

            if suggestions:
                 for i, suggestion in enumerate(sorted(list(suggestions))):
                      print(f"  {i+1}. {suggestion}")
            else:
                 print("  Review the issues listed above and the detailed JSON report file.")

        print("\n" + "="*60 + "\n")
        return report

def main():
    """Command-line interface for auto-repair"""
    parser = argparse.ArgumentParser(
        description='EmanimStudio Auto-Repair System v2.2 (Updated Paths) - Checks and fixes common configuration issues.')
    parser.add_argument('--full', action='store_true',
                        help='Run the full comprehensive repair process (default action).')

    args = parser.parse_args()

    try:
        repair = EmanimAutoRepair()
    except Exception as e:
         print(f"[CRITICAL] Failed to initialize AutoRepair system: {e}")
         print("\nPress Enter to exit...")
         input()
         sys.exit(2)

    final_report = None
    exit_code = 0

    try:
        final_report = repair.run_full_repair()

        if final_report and final_report.get("overall_health") != "HEALTHY":
            exit_code = 1

    except Exception as e:
         repair.log(f"Auto-repair main function crashed: {e}", "CRITICAL")
         print(f"\n❌ CRITICAL ERROR during repair process: {e}")
         exit_code = 2

    print("\nRepair process finished. Press Enter to exit...")
    input()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()