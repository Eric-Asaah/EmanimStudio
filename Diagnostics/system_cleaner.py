import os
import glob
import shutil
from pathlib import Path
from datetime import datetime

def clean_system():
    """Clean unnecessary files from root and diagnostics folders"""
    current_file = Path(__file__)
    studio_root = current_file.parent.parent if current_file.parent.name == "Diagnostics" else current_file.parent
    diagnostics_root = studio_root / "Diagnostics"
    
    print("🧹 Cleaning unnecessary files...")
    cleaned_files = 0
    cleaned_size = 0
    
    # Patterns to clean
    clean_patterns = [
        "*.tmp", "*.temp", "*.log", "*.bak", 
        "*.old", "*.cache", "*.pyc", "__pycache__",
        "Thumbs.db", ".DS_Store"
    ]
    
    # Clean root directory
    print("📁 Cleaning root directory...")
    for pattern in clean_patterns:
        for file_path in studio_root.rglob(pattern):
            try:
                if file_path.is_dir():
                    size = sum(f.stat().st_size for f in file_path.rglob('*') if f.is_file())
                    shutil.rmtree(file_path)
                    cleaned_files += 1
                    cleaned_size += size
                    print(f"   🗑️  Removed directory: {file_path.relative_to(studio_root)}")
                else:
                    size = file_path.stat().st_size
                    file_path.unlink()
                    cleaned_files += 1
                    cleaned_size += size
                    print(f"   🗑️  Removed file: {file_path.relative_to(studio_root)}")
            except Exception as e:
                print(f"   ⚠️  Could not remove {file_path}: {e}")
    
    # Clean old diagnostic reports (keep last 5)
    print("📊 Cleaning old diagnostic reports...")
    reports_dir = diagnostics_root / "repair_logs"
    if reports_dir.exists():
        # FIXED: Use correct report file patterns
        report_files = list(reports_dir.glob("auto_repair_report_*.json"))
        report_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        # Keep only 5 most recent reports
        for old_report in report_files[5:]:
            try:
                size = old_report.stat().st_size
                old_report.unlink()
                cleaned_files += 1
                cleaned_size += size
                print(f"   🗑️  Removed old report: {old_report.name}")
            except Exception as e:
                print(f"   ⚠️  Could not remove {old_report}: {e}")
    
    # Clean old log files (keep last 3)
    print("📝 Cleaning old log files...")
    if reports_dir.exists():
        # FIXED: Use correct log file patterns
        log_files = list(reports_dir.glob("auto_repair_*.log"))
        log_files.extend(reports_dir.glob("diagnostics_*.log"))
        log_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        # Keep only 3 most recent logs
        for old_log in log_files[3:]:
            try:
                size = old_log.stat().st_size
                old_log.unlink()
                cleaned_files += 1
                cleaned_size += size
                print(f"   🗑️  Removed old log: {old_log.name}")
            except Exception as e:
                print(f"   ⚠️  Could not remove {old_log}: {e}")
    
    # Clean backup directory (keep last 3 enhanced backups)
    print("💾 Cleaning old backups...")
    backups_dir = diagnostics_root / "backups"
    if backups_dir.exists():
        # FIXED: Use correct backup patterns
        enhanced_backups = list(backups_dir.glob("enhanced_python_*"))
        enhanced_backups.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        # Keep only 3 most recent enhanced backups
        for old_backup in enhanced_backups[3:]:
            try:
                if old_backup.is_dir():
                    size = sum(f.stat().st_size for f in old_backup.rglob('*') if f.is_file())
                    shutil.rmtree(old_backup)
                    cleaned_files += 1
                    cleaned_size += size
                    print(f"   🗑️  Removed old backup: {old_backup.name}")
                else:
                    size = old_backup.stat().st_size
                    old_backup.unlink()
                    cleaned_files += 1
                    cleaned_size += size
                    print(f"   🗑️  Removed old backup: {old_backup.name}")
            except Exception as e:
                print(f"   ⚠️  Could not remove {old_backup}: {e}")
    
    # FIXED: Clean temporary output files (but keep the Output folder structure)
    print("🎬 Cleaning temporary output files...")
    output_dir = studio_root / "Output"
    if output_dir.exists():
        # Clean temporary files but keep folder structure
        temp_output_patterns = ["*.tmp", "*.temp", "*.log", "*.bak"]
        for pattern in temp_output_patterns:
            for file_path in output_dir.rglob(pattern):
                try:
                    size = file_path.stat().st_size
                    file_path.unlink()
                    cleaned_files += 1
                    cleaned_size += size
                    print(f"   🗑️  Removed temp output: {file_path.relative_to(studio_root)}")
                except Exception as e:
                    print(f"   ⚠️  Could not remove {file_path}: {e}")
    
    print(f"\n✅ Cleanup completed!")
    print(f"📊 Removed {cleaned_files} files/directories")
    print(f"💾 Freed {cleaned_size / (1024*1024):.1f} MB of space")

if __name__ == "__main__":
    clean_system()