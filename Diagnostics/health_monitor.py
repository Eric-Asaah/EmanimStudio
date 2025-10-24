#!/usr/bin/env python3
"""
EmanimStudio Health Monitor - SUPER VERSION
Combines comprehensive health tracking with quick system validation and emergency fixes
"""

import json
import time
import sys
import os
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
import psutil
import threading


class SuperHealthMonitor:
    def __init__(self, studio_root=None):
        # Auto-detect root path like quick check
        if studio_root is None:
            current_file = Path(__file__)
            if current_file.parent.name == "Diagnostics":
                self.studio_root = current_file.parent.parent
            else:
                self.studio_root = current_file.parent
        else:
            self.studio_root = Path(studio_root)

        self.health_file = self.studio_root / "Diagnostics" / "health_history.json"
        self.metrics_file = self.studio_root / "Diagnostics" / "performance_metrics.json"
        self.health_history = self.load_health_history()
        self.check_results = []
        self.critical_failures = 0

    def load_health_history(self):
        """Load previous health records"""
        if self.health_file.exists():
            try:
                with open(self.health_file, 'r') as f:
                    return json.load(f)
            except:
                return {"checks": []}
        return {"checks": []}

    def save_health_history(self):
        """Save health history to file"""
        self.health_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.health_file, 'w') as f:
            json.dump(self.health_history, f, indent=2)

    # === COMPREHENSIVE HEALTH CHECKS ===

    def check_disk_space(self):
        """Check available disk space with detailed metrics"""
        try:
            usage = psutil.disk_usage(str(self.studio_root))
            return {
                "total_gb": round(usage.total / (1024**3), 2),
                "used_gb": round(usage.used / (1024**3), 2),
                "free_gb": round(usage.free / (1024**3), 2),
                "percent_used": usage.percent,
                "status": "healthy" if usage.percent < 90 else "warning"
            }
        except:
            return {"status": "unknown", "error": "Could not check disk space"}

    def check_memory_usage(self):
        """Check system memory with detailed metrics"""
        try:
            memory = psutil.virtual_memory()
            return {
                "total_gb": round(memory.total / (1024**3), 2),
                "available_gb": round(memory.available / (1024**3), 2),
                "percent_used": memory.percent,
                "status": "healthy" if memory.percent < 80 else "warning"
            }
        except:
            return {"status": "unknown", "error": "Could not check memory"}

    def count_animations(self):
        """Count animations by category"""
        animations_dir = self.studio_root / "Animations"
        categories = {}
        total = 0

        if animations_dir.exists():
            for category in animations_dir.iterdir():
                if category.is_dir():
                    count = len(list(category.glob("*.py")))
                    categories[category.name] = count
                    total += count

        return {
            "total": total,
            "by_category": categories
        }

    def count_rendered_videos(self):
        """Count rendered videos"""
        output_dir = self.studio_root / "Output"
        video_count = 0
        total_size_mb = 0

        if output_dir.exists():
            for video in output_dir.rglob("*.mp4"):
                video_count += 1
                total_size_mb += video.stat().st_size / (1024**2)

        return {
            "count": video_count,
            "total_size_mb": round(total_size_mb, 2)
        }

    def check_python_health(self):
        """Check Python installation health"""
        python_dir = self.studio_root / "Lib" / "python312"
        pth_file = python_dir / "python312._pth"

        issues = []

        if not python_dir.exists():
            issues.append("Python directory missing")
        if not pth_file.exists():
            issues.append("python312._pth missing")
        if not (python_dir / "python.exe").exists():
            issues.append("python.exe missing")

        return {
            "status": "healthy" if not issues else "error",
            "issues": issues
        }

    def check_dependencies_health(self):
        """Check if critical dependencies are available"""
        results = {}

        # Test packages with their actual import names
        packages_to_test = [
            ('manim', 'manim'),
            ('numpy', 'numpy'),
            ('pillow', 'PIL'),      # Pillow imports as PIL
            ('pycairo', 'cairo')    # PyCairo imports as cairo
        ]

        for display_name, import_name in packages_to_test:
            try:
                if import_name == 'PIL':
                    # Pillow needs specific submodule import
                    __import__('PIL.Image')
                else:
                    __import__(import_name)
                results[display_name] = "installed"
            except ImportError as e:
                results[display_name] = "missing"

        all_installed = all("installed" in v for v in results.values())

        return {
            "status": "healthy" if all_installed else "warning",
            "packages": results
        }

    # === QUICK SYSTEM CHECKS ===

    def quick_check(self, check_name, check_func):
        """Run a quick check and record results"""
        try:
            result = check_func()
            status = "✅ PASS" if result else "❌ FAIL"
            self.check_results.append(f"{status} {check_name}")
            if not result:
                self.critical_failures += 1
            return result
        except Exception as e:
            self.check_results.append(f"❌ ERROR {check_name}: {e}")
            self.critical_failures += 1
            return False

    def check_core_files(self):
        """Check core files for your EmanimStudio setup"""
        your_files = [
            "EmanimStudio.bat",          # Main launcher
            "emanim_terminal.bat",       # Terminal interface
            "Animations/",               # Animations
            "Output/",                   # Output
            "Lib/python312/python.exe",  # Python
            "Diagnostics/",              # Diagnostics
        ]

        missing = []
        for file_path in your_files:
            if not (self.studio_root / file_path).exists():
                missing.append(file_path)

        # Only fail if critical components missing
        critical = ["Lib/python312/python.exe", "Animations/"]
        has_critical = all((self.studio_root / f).exists() for f in critical)

        return has_critical

    def check_ffmpeg(self):
        """Quick FFmpeg availability check"""
        try:
            result = subprocess.run(
                ['ffmpeg', '-version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False

    def check_directory_permissions(self):
        """Check if we can write to necessary directories"""
        test_dirs = [
            self.studio_root / "Animations",
            self.studio_root / "Output",
            self.studio_root / "Diagnostics" / "repair_logs"
        ]

        for directory in test_dirs:
            directory.mkdir(exist_ok=True)
            test_file = directory / "write_test.tmp"
            try:
                test_file.write_text("test")
                test_file.unlink()
            except:
                return False
        return True

    def check_script_integrity(self):
        """Check if main scripts are not corrupted"""
        scripts_to_check = [
            "Scripts/terminal_interface.py",
            "Diagnostics/diagnostics.py"
        ]

        for script in scripts_to_check:
            script_path = self.studio_root / script
            if script_path.exists():
                # Basic check: file has content and is readable
                try:
                    content = script_path.read_text(encoding='utf-8')
                    if len(content) < 100:  # Arbitrary minimum size
                        return False
                    if "import" not in content and "def " not in content:
                        return False
                except:
                    return False
        return True

    def check_basic_system_resources(self):
        """Quick system resources check"""
        try:
            # Check disk space (Windows)
            if os.name == 'nt':
                import ctypes
                free_bytes = ctypes.c_ulonglong(0)
                ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                    ctypes.c_wchar_p(str(self.studio_root)),
                    None, None, ctypes.pointer(free_bytes)
                )
                free_gb = free_bytes.value / (1024**3)
                return free_gb > 1.0  # At least 1GB free
            else:
                # Linux/Mac
                statvfs = os.statvfs(str(self.studio_root))
                free_gb = (statvfs.f_bavail * statvfs.f_frsize) / (1024**3)
                return free_gb > 1.0
        except:
            return True  # If we can't check, assume it's OK

    # === COMBINED FEATURES ===

    def calculate_uptime_stats(self):
        """Calculate usage statistics from history"""
        if not self.health_history.get("checks"):
            return {"total_checks": 0, "avg_per_day": 0}

        checks = self.health_history["checks"]
        total_checks = len(checks)

        if total_checks < 2:
            return {"total_checks": total_checks, "avg_per_day": 0}

        first_check = datetime.fromisoformat(checks[0]["timestamp"])
        last_check = datetime.fromisoformat(checks[-1]["timestamp"])
        days = (last_check - first_check).days or 1

        return {
            "total_checks": total_checks,
            "avg_per_day": round(total_checks / days, 2),
            "first_check": first_check.strftime("%Y-%m-%d"),
            "last_check": last_check.strftime("%Y-%m-%d")
        }

    def generate_health_score(self):
        """Generate a simple health score (0-100)"""
        total_checks = len(self.check_results)
        passed_checks = sum(
            1 for result in self.check_results if "✅" in result)

        if total_checks == 0:
            return 0

        score = (passed_checks / total_checks) * 100
        return int(score)

    def emergency_fixes(self):
        """Apply quick emergency fixes for common issues"""
        print("\n🔧 Applying Emergency Fixes...")

        fixes_applied = 0

        # Ensure critical directories exist
        critical_dirs = [
            self.studio_root / "Animations",
            self.studio_root / "Output",
            self.studio_root / "Diagnostics" / "repair_logs",
            self.studio_root / "Diagnostics" / "backups"
        ]

        for directory in critical_dirs:
            directory.mkdir(parents=True, exist_ok=True)
            fixes_applied += 1

        # Fix Python ._pth file if missing
        pth_file = self.studio_root / "Lib" / "python312" / "python312._pth"
        if not pth_file.exists() and pth_file.parent.exists():
            pth_content = """python312.zip

..\\..\\Lib\\site-packages
import site
"""
            pth_file.write_text(pth_content)
            fixes_applied += 1

        print(f"✅ Applied {fixes_applied} emergency fixes")
        return fixes_applied

    def run_quick_check(self):
        """Run all quick checks and return summary"""
        print("⚡ EmanimStudio Quick System Check")
        print("=" * 40)

        checks = [
            ("Core Files", self.check_core_files),
            ("Python Imports", lambda: self.check_dependencies_health()
             ["status"] == "healthy"),
            ("FFmpeg", self.check_ffmpeg),
            ("File Permissions", self.check_directory_permissions),
            ("Script Integrity", self.check_script_integrity),
            ("System Resources", self.check_basic_system_resources),
        ]

        for check_name, check_func in checks:
            self.quick_check(check_name, check_func)

        # Display results
        print("\n".join(self.check_results))

        # Summary
        print(f"\n{'='*40}")
        if self.critical_failures == 0:
            print("🎉 QUICK CHECK: ALL SYSTEMS GO!")
            print("System is ready for animation creation.")
            return True
        else:
            print(f"⚠️  QUICK CHECK: {self.critical_failures} ISSUES FOUND")
            print("Run with --fix to apply emergency repairs.")
            return False

    def run_full_health_check(self):
        """Run comprehensive health check"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "disk": self.check_disk_space(),
            "memory": self.check_memory_usage(),
            "animations": self.count_animations(),
            "videos": self.count_rendered_videos(),
            "python": self.check_python_health(),
            "dependencies": self.check_dependencies_health(),
            "quick_checks": {
                "core_files": self.check_core_files(),
                "ffmpeg": self.check_ffmpeg(),
                "permissions": self.check_directory_permissions(),
                "script_integrity": self.check_script_integrity()
            },
            "uptime_stats": self.calculate_uptime_stats()
        }

        # Determine overall health
        critical_issues = []
        warnings = []

        if report["disk"]["status"] != "healthy":
            warnings.append("Low disk space")
        if report["memory"]["status"] != "healthy":
            warnings.append("High memory usage")
        if report["python"]["status"] != "healthy":
            critical_issues.extend(report["python"]["issues"])
        if report["dependencies"]["status"] != "healthy":
            warnings.append("Missing dependencies")

        # Add quick check issues
        if not report["quick_checks"]["core_files"]:
            critical_issues.append("Missing core files")
        if not report["quick_checks"]["ffmpeg"]:
            warnings.append("FFmpeg not available")
        if not report["quick_checks"]["permissions"]:
            critical_issues.append("Write permission issues")

        report["overall_status"] = (
            "critical" if critical_issues else
            "warning" if warnings else
            "healthy"
        )
        report["critical_issues"] = critical_issues
        report["warnings"] = warnings

        # Add to history
        self.health_history["checks"].append(report)

        # Keep only last 100 checks
        if len(self.health_history["checks"]) > 100:
            self.health_history["checks"] = self.health_history["checks"][-100:]

        self.save_health_history()

        return report

    def print_health_report(self, report):
        """Print formatted health report"""
        print("\n" + "="*70)
        print("  EMANIM STUDIO SUPER HEALTH REPORT")
        print("="*70 + "\n")

        # Overall Status
        status_emoji = {
            "healthy": "🟢",
            "warning": "🟡",
            "critical": "🔴"
        }
        emoji = status_emoji.get(report["overall_status"], "⚪")
        print(f"Overall Status: {emoji} {report['overall_status'].upper()}")

        # Health Score
        quick_score = self.generate_health_score()
        print(f"Health Score: {quick_score}/100")

        if report["critical_issues"]:
            print("\n🔴 CRITICAL ISSUES:")
            for issue in report["critical_issues"]:
                print(f"   • {issue}")

        if report["warnings"]:
            print("\n⚠️  WARNINGS:")
            for warning in report["warnings"]:
                print(f"   • {warning}")

        # System Resources
        print("\n📊 SYSTEM RESOURCES:")
        if "free_gb" in report['disk']:
            print(
                f"   💾 Disk: {report['disk']['free_gb']}GB free / {report['disk']['total_gb']}GB total ({report['disk']['percent_used']}% used)")
        else:
            print(f"   💾 Disk: {report['disk']['status']}")

        if "available_gb" in report['memory']:
            print(
                f"   🧠 Memory: {report['memory']['available_gb']}GB available / {report['memory']['total_gb']}GB total ({report['memory']['percent_used']}% used)")
        else:
            print(f"   🧠 Memory: {report['memory']['status']}")

        # Content Stats
        print("\n🎬 CONTENT STATISTICS:")
        print(f"   📁 Total Animations: {report['animations']['total']}")
        for category, count in report['animations']['by_category'].items():
            print(f"      • {category}: {count}")
        print(
            f"   🎥 Rendered Videos: {report['videos']['count']} ({report['videos']['total_size_mb']}MB)")

        # Dependencies
        print("\n📦 DEPENDENCIES:")
        for package, status in report['dependencies']['packages'].items():
            symbol = "✅" if status == "installed" else "❌"
            print(f"   {symbol} {package}: {status}")

        # Quick Checks
        print("\n⚡ QUICK CHECKS:")
        quick_checks = report['quick_checks']
        print(
            f"   {'✅' if quick_checks['core_files'] else '❌'} Core Files: {'Present' if quick_checks['core_files'] else 'Missing'}")
        print(
            f"   {'✅' if quick_checks['ffmpeg'] else '❌'} FFmpeg: {'Available' if quick_checks['ffmpeg'] else 'Not Found'}")
        print(
            f"   {'✅' if quick_checks['permissions'] else '❌'} Permissions: {'OK' if quick_checks['permissions'] else 'Issues'}")
        print(
            f"   {'✅' if quick_checks['script_integrity'] else '❌'} Script Integrity: {'OK' if quick_checks['script_integrity'] else 'Corrupted'}")

        # Usage Stats
        if report['uptime_stats']['total_checks'] > 0:
            print("\n📈 USAGE STATISTICS:")
            print(
                f"   📋 Total Health Checks: {report['uptime_stats']['total_checks']}")
            print(
                f"   📊 Average per Day: {report['uptime_stats']['avg_per_day']}")
            if 'first_check' in report['uptime_stats']:
                print(
                    f"   🗓️  First Check: {report['uptime_stats']['first_check']}")
                print(
                    f"   🗓️  Last Check: {report['uptime_stats']['last_check']}")

        print("\n" + "="*70 + "\n")

# Command-line interface


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='EmanimStudio Super Health Monitor')
    parser.add_argument('--quick', action='store_true',
                        help='Run quick system check only')
    parser.add_argument('--fix', action='store_true',
                        help='Apply emergency fixes')
    parser.add_argument('--score', action='store_true',
                        help='Show health score only')
    parser.add_argument('--history', action='store_true',
                        help='Show health check history')

    args = parser.parse_args()

    monitor = SuperHealthMonitor()

    if args.fix:
        monitor.emergency_fixes()

    if args.quick:
        success = monitor.run_quick_check()
    else:
        report = monitor.run_full_health_check()
        monitor.print_health_report(report)
        success = report["overall_status"] != "critical"

    if args.score:
        score = monitor.generate_health_score()
        print(f"\n🏥 System Health Score: {score}/100")

    if args.history:
        checks = monitor.health_history.get("checks", [])
        print(f"\n📊 Health Check History: {len(checks)} records")
        for i, check in enumerate(checks[-5:]):  # Show last 5
            status = check.get('overall_status', 'unknown')
            timestamp = check.get('timestamp', '')[:16]
            print(f"  {i+1}. {timestamp} - {status}")

    # Return appropriate exit code
    sys.exit(0 if success else 1)

# Utility functions for other modules


def is_system_healthy():
    """Ultra-fast system health check for other modules"""
    monitor = SuperHealthMonitor()
    return (
        monitor.check_core_files() and
        monitor.check_dependencies_health()["status"] == "healthy" and
        monitor.check_ffmpeg()
    )


def get_health_status():
    """Return detailed health status for GUI or other interfaces"""
    monitor = SuperHealthMonitor()
    report = monitor.run_full_health_check()

    return {
        'healthy': report["overall_status"] == "healthy",
        'score': monitor.generate_health_score(),
        'issues': len(report["critical_issues"]) + len(report["warnings"]),
        'status': report["overall_status"],
        'timestamp': datetime.now().isoformat()
    }


if __name__ == "__main__":
    main()
