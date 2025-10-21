"""
Simple video player for EmanimStudio
Handles video playback operations with portable paths
"""
import os
import subprocess
from pathlib import Path

class VideoPlayer:
    def __init__(self, root_dir=None):
        # Auto-detect root directory if not provided
        if root_dir is None:
            self.root_dir = self.find_studio_root()
        else:
            self.root_dir = Path(root_dir)
        
        print(f"🎥 Video Player initialized at: {self.root_dir}")
    
    def find_studio_root(self):
        """Automatically find the EmanimStudio root directory"""
        # Method 1: Check if running from Scripts folder
        current_file = Path(__file__).resolve()
        if current_file.parent.name == "Scripts":
            return current_file.parent.parent
        
        # Method 2: Check if running from root
        if (current_file.parent / "EmanimStudio.bat").exists():
            return current_file.parent
        
        # Method 3: Current directory
        return Path.cwd()
    
    def play_video(self, video_path):
        """Play a video file using system default player"""
        try:
            # Handle both relative and absolute paths
            if Path(video_path).is_absolute():
                full_path = Path(video_path)
            else:
                full_path = self.root_dir / video_path
            
            if not full_path.exists():
                return {
                    "status": "error", 
                    "message": f"Video file not found: {video_path}",
                    "searched_path": str(full_path)
                }
            
            print(f"🎥 Playing video: {full_path.name}")
            
            # Use system default player
            if os.name == 'nt':  # Windows
                os.startfile(str(full_path))
                return {
                    "status": "success", 
                    "message": f"Playing {full_path.name}",
                    "video_path": str(full_path)
                }
            else:
                return {
                    "status": "error", 
                    "message": "Video playback only supported on Windows",
                    "suggestion": "Manually open the video file from Output folder"
                }
            
        except Exception as e:
            return {
                "status": "error", 
                "message": f"Failed to play video: {str(e)}",
                "exception_type": type(e).__name__
            }
    
    def find_latest_video(self):
        """Find the most recently created video file in Output folder"""
        output_dir = self.root_dir / "Output"
        
        if not output_dir.exists():
            return None
        
        try:
            # Find all MP4 files and get the most recent one
            video_files = list(output_dir.glob("**/*.mp4"))
            if not video_files:
                return None
            
            # Sort by modification time, most recent first
            latest_video = max(video_files, key=lambda f: f.stat().st_mtime)
            return latest_video
            
        except Exception as e:
            print(f"❌ Error finding latest video: {e}")
            return None
    
    def play_latest_video(self):
        """Play the most recently created video"""
        latest_video = self.find_latest_video()
        
        if latest_video:
            # Convert to relative path for playback
            relative_path = latest_video.relative_to(self.root_dir)
            return self.play_video(str(relative_path))
        else:
            return {
                "status": "error", 
                "message": "No video files found in Output folder",
                "suggestion": "Render an animation first"
            }
    
    def list_videos(self):
        """List all available video files"""
        output_dir = self.root_dir / "Output"
        videos = []
        
        if output_dir.exists():
            for video_file in output_dir.glob("**/*.mp4"):
                if video_file.is_file():
                    stat = video_file.stat()
                    videos.append({
                        "filename": video_file.name,
                        "path": str(video_file.relative_to(self.root_dir)),
                        "size": stat.st_size,
                        "modified": stat.st_mtime,
                        "full_path": str(video_file)
                    })
        
        # Sort by modification time, newest first
        videos.sort(key=lambda x: x["modified"], reverse=True)
        return videos

# Test function
def test_video_player():
    """Test the video player system"""
    player = VideoPlayer()
    print("✅ Video Player Ready")
    print(f"📁 Root: {player.root_dir}")
    
    # List available videos
    videos = player.list_videos()
    print(f"🎥 Found {len(videos)} video files:")
    
    for video in videos[:3]:  # Show first 3
        print(f"   - {video['filename']} ({video['size']} bytes)")
    
    if videos:
        print("🎯 Latest video ready to play!")
    else:
        print("💡 No videos found. Render an animation first!")

if __name__ == "__main__":
    test_video_player()