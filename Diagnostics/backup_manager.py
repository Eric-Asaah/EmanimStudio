#!/usr/bin/env python3
"""
EmanimStudio Backup Manager
Comprehensive backup and restore system for project preservation
"""
import sys
import os
import shutil
import zipfile
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


class BackupManager:
    def __init__(self, studio_root=None):
        # Auto-detect paths
        current_file = Path(__file__)
        if current_file.parent.name == "Diagnostics":
            self.studio_root = current_file.parent.parent
            self.diagnostics_root = current_file.parent
        else:
            self.studio_root = current_file.parent
            self.diagnostics_root = self.studio_root / "Diagnostics"

        self.backups_dir = self.diagnostics_root / "backups"
        self.backups_dir.mkdir(exist_ok=True)

        # Backup configurations
        self.backup_profiles = {
            "full": {
                "description": "Complete system backup",
                "include": [
                    "Scripts/",
                    "Animations/",
                    "Output/",
                    "Diagnostics/",
                    "EmanimStudio.bat",
                    "diagnose.bat",
                    "fix_environment.bat"
                ],
                "exclude": [
                    "Output/*.mp4",  # Exclude large video files
                    "Diagnostics/backups/",  # Don't backup backups
                    "Diagnostics/repair_logs/",  # Exclude logs
                    "*.tmp",
                    "*.log"
                ]
            },
            "config_only": {
                "description": "Configuration and scripts only",
                "include": [
                    "Scripts/",
                    "Diagnostics/",
                    "EmanimStudio.bat",
                    "diagnose.bat",
                    "fix_environment.bat"
                ],
                "exclude": [
                    "Animations/",
                    "Output/",
                    "Diagnostics/backups/",
                    "Diagnostics/repair_logs/"
                ]
            },
            "animations_only": {
                "description": "Animation files only",
                "include": [
                    "Animations/"
                ],
                "exclude": [
                    "*.mp4",
                    "*.log"
                ]
            }
        }

    def create_backup(self, profile_name="full", comment=""):
        """Create a backup with specified profile"""
        if profile_name not in self.backup_profiles:
            print(f"❌ Unknown backup profile: {profile_name}")
            return None

        profile = self.backup_profiles[profile_name]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{profile_name}_{timestamp}"
        backup_path = self.backups_dir / backup_name
        backup_path.mkdir(exist_ok=True)

        print(f"💾 Creating {profile_name} backup: {backup_name}")
        print(f"   Description: {profile['description']}")

        # Create metadata
        metadata = {
            "name": backup_name,
            "profile": profile_name,
            "description": profile['description'],
            "timestamp": datetime.now().isoformat(),
            "comment": comment,
            "studio_root": str(self.studio_root),
            "files": []
        }

        files_backed_up = 0
        total_size = 0

        # Process included files/directories
        for include_pattern in profile["include"]:
            include_path = self.studio_root / include_pattern

            if include_path.is_file():
                # Single file
                if self._should_include_file(include_path, profile["exclude"]):
                    dest_path = backup_path / include_pattern
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(include_path, dest_path)

                    file_size = include_path.stat().st_size
                    metadata["files"].append({
                        "path": str(include_pattern),
                        "size": file_size,
                        "type": "file"
                    })
                    files_backed_up += 1
                    total_size += file_size

            elif include_path.is_dir():
                # Directory - copy recursively
                for file_path in include_path.rglob('*'):
                    if file_path.is_file() and self._should_include_file(file_path, profile["exclude"]):
                        # Calculate relative path for backup structure
                        rel_path = file_path.relative_to(self.studio_root)
                        dest_path = backup_path / rel_path
                        dest_path.parent.mkdir(parents=True, exist_ok=True)

                        shutil.copy2(file_path, dest_path)

                        file_size = file_path.stat().st_size
                        metadata["files"].append({
                            "path": str(rel_path),
                            "size": file_size,
                            "type": "file"
                        })
                        files_backed_up += 1
                        total_size += file_size

        # Save metadata
        metadata["total_files"] = files_backed_up
        metadata["total_size"] = total_size

        metadata_file = backup_path / "backup_metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        # Create zip archive for portability
        zip_path = self.backups_dir / f"{backup_name}.zip"
        self._create_zip_archive(backup_path, zip_path)

        # Clean up temporary directory
        shutil.rmtree(backup_path)

        print(
            f"✅ Backup completed: {files_backed_up} files, {self._format_size(total_size)}")
        print(f"📦 Archive: {zip_path.name}")

        return {
            "backup_path": zip_path,
            "metadata": metadata
        }

    def _should_include_file(self, file_path: Path, exclude_patterns: List[str]) -> bool:
        """Check if a file should be included based on exclude patterns"""
        rel_path = file_path.relative_to(self.studio_root)

        for pattern in exclude_patterns:
            if pattern.endswith('/'):
                # Directory pattern
                if str(rel_path).startswith(pattern[:-1]):
                    return False
            elif '*' in pattern:
                # Wildcard pattern
                import fnmatch
                if fnmatch.fnmatch(str(rel_path), pattern):
                    return False
            else:
                # Exact match
                if str(rel_path) == pattern:
                    return False

        return True

    def _create_zip_archive(self, source_dir: Path, zip_path: Path):
        """Create zip archive from directory"""
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in source_dir.rglob('*'):
                if file_path.is_file():
                    rel_path = file_path.relative_to(source_dir)
                    zipf.write(file_path, rel_path)

    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"

    def list_backups(self):
        """List all available backups"""
        backups = []

        for backup_file in self.backups_dir.glob("*.zip"):
            # Try to read metadata
            metadata = self.get_backup_metadata(backup_file)
            if metadata:
                backups.append(metadata)
            else:
                # Basic info for backups without metadata
                backups.append({
                    "name": backup_file.stem,
                    "file": backup_file.name,
                    "size": backup_file.stat().st_size,
                    "timestamp": datetime.fromtimestamp(backup_file.stat().st_mtime).isoformat(),
                    "has_metadata": False
                })

        return sorted(backups, key=lambda x: x.get('timestamp', ''), reverse=True)

    def get_backup_metadata(self, backup_path: Path) -> Optional[Dict]:
        """Extract metadata from backup file"""
        try:
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                if 'backup_metadata.json' in zipf.namelist():
                    with zipf.open('backup_metadata.json') as f:
                        metadata = json.load(f)
                        metadata['file'] = backup_path.name
                        metadata['size'] = backup_path.stat().st_size
                        return metadata
        except:
            pass
        return None

    def restore_backup(self, backup_name: str, target_dir: Path = None, overwrite=False):
        """Restore a backup to specified directory"""
        if target_dir is None:
            target_dir = self.studio_root

        backup_path = self.backups_dir / backup_name
        if not backup_path.exists():
            print(f"❌ Backup not found: {backup_name}")
            return False

        # Read metadata first
        metadata = self.get_backup_metadata(backup_path)
        if not metadata:
            print("❌ Backup metadata missing or corrupted")
            return False

        print(f"🔄 Restoring backup: {metadata.get('name', backup_name)}")
        print(f"   Profile: {metadata.get('profile', 'unknown')}")
        print(f"   Target: {target_dir}")
        print(f"   Files: {metadata.get('total_files', 0)}")

        if not overwrite:
            response = input(
                "❓ This will overwrite existing files. Continue? (y/N): ")
            if response.lower() != 'y':
                print("Restore cancelled.")
                return False

        try:
            # Extract backup
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                # First, extract everything to temp location
                temp_dir = self.backups_dir / "temp_restore"
                if temp_dir.exists():
                    shutil.rmtree(temp_dir)
                temp_dir.mkdir()

                zipf.extractall(temp_dir)

                # Now copy files to target, preserving structure
                restored_files = 0
                for item in temp_dir.rglob('*'):
                    if item.is_file() and item.name != 'backup_metadata.json':
                        rel_path = item.relative_to(temp_dir)
                        target_path = target_dir / rel_path

                        # Ensure target directory exists
                        target_path.parent.mkdir(parents=True, exist_ok=True)

                        shutil.copy2(item, target_path)
                        restored_files += 1

                # Clean up temp directory
                shutil.rmtree(temp_dir)

            print(f"✅ Restore completed: {restored_files} files restored")
            return True

        except Exception as e:
            print(f"❌ Restore failed: {e}")
            return False

    def delete_backup(self, backup_name: str):
        """Delete a backup file"""
        backup_path = self.backups_dir / backup_name
        if backup_path.exists():
            backup_path.unlink()
            print(f"✅ Deleted backup: {backup_name}")
            return True
        else:
            print(f"❌ Backup not found: {backup_name}")
            return False

    def cleanup_old_backups(self, keep_count=10):
        """Keep only the most recent backups"""
        backups = self.list_backups()

        if len(backups) <= keep_count:
            print(f"ℹ️  Only {len(backups)} backups exist, keeping all")
            return

        backups_to_delete = backups[keep_count:]

        for backup in backups_to_delete:
            backup_file = self.backups_dir / backup['file']
            if backup_file.exists():
                backup_file.unlink()
                print(f"🗑️  Deleted old backup: {backup['file']}")

        print(f"✅ Cleanup completed: kept {keep_count} most recent backups")


def main():
    """Command-line interface for backup manager"""
    import argparse

    parser = argparse.ArgumentParser(description='EmanimStudio Backup Manager')
    parser.add_argument('--create', choices=['full', 'config_only', 'animations_only'],
                        help='Create a new backup')
    parser.add_argument('--list', action='store_true',
                        help='List available backups')
    parser.add_argument('--restore', help='Restore a backup by name')
    parser.add_argument('--delete', help='Delete a backup by name')
    parser.add_argument('--cleanup', type=int,
                        help='Keep only N most recent backups')
    parser.add_argument('--comment', help='Comment for backup creation')

    args = parser.parse_args()

    manager = BackupManager()

    if args.create:
        manager.create_backup(args.create, args.comment or "")

    elif args.list:
        backups = manager.list_backups()
        print("\n📂 Available Backups:")
        print("=" * 60)
        for backup in backups:
            if backup.get('has_metadata', True):
                print(f"📦 {backup['file']}")
                print(f"   Profile: {backup.get('profile', 'unknown')}")
                print(f"   Date: {backup.get('timestamp', 'unknown')}")
                print(f"   Files: {backup.get('total_files', 0)}")
                print(
                    f"   Size: {manager._format_size(backup.get('size', 0))}")
                if backup.get('comment'):
                    print(f"   Comment: {backup['comment']}")
            else:
                print(f"📦 {backup['file']} (no metadata)")
            print()

    elif args.restore:
        manager.restore_backup(args.restore)

    elif args.delete:
        manager.delete_backup(args.delete)

    elif args.cleanup:
        manager.cleanup_old_backups(args.cleanup)

    else:
        # Default: list backups
        backups = manager.list_backups()
        if backups:
            print(f"Found {len(backups)} backups")
        else:
            print("No backups found. Use --create to make one.")


if __name__ == "__main__":
    main()
