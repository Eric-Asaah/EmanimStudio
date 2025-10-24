# Scripts\video_player.py
import os
import subprocess
import time
from pathlib import Path
import glob


class VideoPlayer:
    """
    Robust video player that NEVER plays old cached videos
    Always finds and plays the most recently created video
    """

    def __init__(self, project_root=None):
        self.project_root = project_root or Path(__file__).parent.parent
        self.output_dir = self.project_root / "Output"

    def play_latest_video(self, scene_name=None):
        """
        Find and play the MOST RECENT video file
        Completely ignores Manim's cache and always finds fresh renders
        """
        print("🎬 Searching for latest video...")

        # Method 1: Look in Output directory first (new system)
        latest_video = self._find_newest_file(self.output_dir, "*.mp4")

        # Method 2: Look in Manim's video directory (backup)
        if not latest_video:
            manim_videos = self.project_root / "media" / "videos"
            latest_video = self._find_newest_file(manim_videos, "*.mp4")

        # Method 3: Search entire project for any MP4
        if not latest_video:
            latest_video = self._find_newest_file(self.project_root, "*.mp4")

        if latest_video:
            print(f"✅ Found: {latest_video.name}")
            print(f"📍 Path: {latest_video}")
            print(f"🕒 Modified: {time.ctime(latest_video.stat().st_mtime)}")

            # Play the video
            return self._play_video(latest_video)
        else:
            print("❌ No video files found!")
            return False

    def play_specific_video(self, video_path):
        """Play a specific video file"""
        video_file = Path(video_path)

        if video_file.exists():
            print(f"🎬 Playing: {video_file.name}")
            return self._play_video(video_file)
        else:
            print(f"❌ Video not found: {video_path}")
            return False

    def _find_newest_file(self, directory, pattern):
        """Find the newest file matching pattern in directory"""
        if not directory.exists():
            return None

        # Get all matching files with their modification times
        files = []
        for file_path in directory.rglob(pattern):
            if file_path.is_file():
                files.append((file_path.stat().st_mtime, file_path))

        if files:
            # Sort by modification time (newest first)
            files.sort(reverse=True)
            return files[0][1]  # Return newest file

        return None

    def _play_video(self, video_path):
        """Actually play the video file"""
        try:
            # Method 1: Use os.startfile (most reliable on Windows)
            os.startfile(video_path)
            print(f"▶️  Playing: {video_path.name}")
            return True

        except Exception as e:
            print(f"❌ Could not play video: {e}")
            return False

    def clear_video_cache(self):
        """Clear ALL video cache to ensure fresh renders"""
        cache_dirs = [
            self.project_root / "Output" / "cache",
            self.project_root / "media",
            self.project_root / "Output" / "videos"  # Manim's output
        ]

        print("🧹 Clearing video cache...")
        for cache_dir in cache_dirs:
            if cache_dir.exists():
                try:
                    # Remove all MP4 files in cache
                    for mp4_file in cache_dir.rglob("*.mp4"):
                        try:
                            mp4_file.unlink()
                            print(f"   Deleted: {mp4_file}")
                        except:
                            pass

                    # Remove the cache directory itself
                    import shutil
                    shutil.rmtree(cache_dir)
                    print(f"   Removed: {cache_dir}")
                except Exception as e:
                    print(f"   ⚠️  Could not clear {cache_dir}: {e}")

    def list_all_videos(self):
        """List all video files in project for debugging"""
        print("\n📁 All video files in project:")

        video_files = []
        for mp4_file in self.project_root.rglob("*.mp4"):
            video_files.append((
                mp4_file.stat().st_mtime,
                mp4_file
            ))

        # Sort by modification time (newest first)
        video_files.sort(reverse=True)

        for mtime, video_file in video_files[:10]:  # Show 10 newest
            print(f"   🕒 {time.ctime(mtime)} - {video_file}")

        return [vf[1] for vf in video_files]


# Simple function for your batch files
def play_latest_video():
    """One-line function to always play the newest video"""
    player = VideoPlayer()
    player.clear_video_cache()  # Always clear cache first
    return player.play_latest_video()


def play_fresh_render(scene_file, scene_class):
    """
    Render and immediately play FRESH video (no cache)
    """
    player = VideoPlayer()

    # Clear cache first
    player.clear_video_cache()

    # Render with NO CACHE
    print(f"🎬 Fresh render: {scene_class}")
    cmd = [
        "manim", "-ql", "--disable_caching",
        str(scene_file), scene_class
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True,
                                cwd=player.project_root, timeout=120)

        if result.returncode == 0:
            print("✅ Render completed")
            # Play the newest video
            return player.play_latest_video()
        else:
            print(f"❌ Render failed: {result.stderr}")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False
