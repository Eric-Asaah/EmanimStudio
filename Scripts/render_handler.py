"""
Simple render handler for EmanimStudio
Handles animation rendering operations with portable paths
"""
import subprocess
import os
import time
from pathlib import Path
import sys

class RenderHandler:
    def __init__(self, root_dir=None):
        # Auto-detect root directory if not provided
        if root_dir is None:
            self.root_dir = self.find_studio_root()
        else:
            self.root_dir = Path(root_dir)
        
        print(f"🎯 Render Handler initialized at: {self.root_dir}")
    
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
    
    def find_animation_file(self, category, filename):
        """Find animation file with flexible search"""
        # Try exact path first
        exact_path = self.root_dir / "Animations" / category / filename
        if exact_path.exists():
            return exact_path
        
        # Try case-insensitive search
        animations_dir = self.root_dir / "Animations" / category
        if animations_dir.exists():
            for file in animations_dir.glob("*.py"):
                if file.name.lower() == filename.lower():
                    return file
        
        # Try without category (backwards compatibility)
        root_animations = self.root_dir / "Animations" / filename
        if root_animations.exists():
            return root_animations
            
        return None
    
    def get_available_qualities(self):
        """Return available rendering quality options"""
        return {
            "low": "-ql",      # 480p, fastest
            "medium": "-qm",   # 720p, balanced  
            "high": "-qh",     # 1080p, slower
            "ultra": "-qk"     # 4K, slowest
        }
    
    def render_animation(self, category, filename, quality="medium"):
        """Render a Manim animation from specific category"""
        try:
            # Find the animation file
            animation_file = self.find_animation_file(category, filename)
            
            if not animation_file or not animation_file.exists():
                return {
                    "status": "error", 
                    "message": f"Animation file not found: {category}/{filename}",
                    "searched_path": str(self.root_dir / "Animations" / category / filename)
                }
            
            output_dir = self.root_dir / "Output"
            output_dir.mkdir(exist_ok=True)  # Ensure output directory exists
            
            # Get quality flag
            quality_flags = self.get_available_qualities()
            quality_flag = quality_flags.get(quality, "-qm")
            
            # Build command
            cmd = [
                sys.executable, "-m", "manim",
                quality_flag,
                str(animation_file),
                "-o", str(output_dir)
            ]
            
            print(f"🎬 Starting render: {category}/{filename}")
            print(f"📁 Input: {animation_file}")
            print(f"📁 Output: {output_dir}")
            print(f"⚡ Quality: {quality} ({quality_flag})")
            print(f"🔧 Command: {' '.join(cmd)}")
            
            start_time = time.time()
            
            # Run rendering
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                cwd=self.root_dir,
                timeout=600  # 10 minute timeout for longer animations
            )
            
            render_time = time.time() - start_time
            
            if result.returncode == 0:
                # Try to find the output video
                video_file = self.find_output_video(filename)
                
                success_message = f"✅ Successfully rendered {category}/{filename} in {render_time:.1f}s"
                if video_file:
                    success_message += f"\n🎥 Output: {video_file.name}"
                
                return {
                    "status": "success", 
                    "message": success_message,
                    "render_time": render_time,
                    "video_path": str(video_file) if video_file else None,
                    "quality": quality
                }
            else:
                error_details = result.stderr or result.stdout or "Unknown error"
                return {
                    "status": "error", 
                    "message": f"Render failed for {category}/{filename}",
                    "error_details": error_details[:500] + "..." if len(error_details) > 500 else error_details,
                    "return_code": result.returncode
                }
                
        except subprocess.TimeoutExpired:
            return {
                "status": "error", 
                "message": f"Render timeout (10 minutes) for {category}/{filename}",
                "suggestion": "Try lower quality setting or optimize animation"
            }
        except Exception as e:
            return {
                "status": "error", 
                "message": f"Render error: {str(e)}",
                "exception_type": type(e).__name__
            }
    
    def find_output_video(self, filename):
        """Find the output video file for a given animation"""
        output_dir = self.root_dir / "Output"
        base_name = Path(filename).stem
        
        if not output_dir.exists():
            return None
            
        # Look for MP4 files that match the animation name
        video_patterns = [
            f"**/*{base_name}*.mp4",      # Any video containing base name
            f"**/*{base_name}*/*.mp4",    # In subdirectories
            f"**/*.mp4"                   # Any MP4 (last resort)
        ]
        
        for pattern in video_patterns:
            for video_file in output_dir.glob(pattern):
                if video_file.is_file():
                    return video_file
        
        return None
    
    def get_animation_categories(self):
        """Get list of available animation categories"""
        animations_dir = self.root_dir / "Animations"
        categories = []
        
        if animations_dir.exists():
            for item in animations_dir.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    # Count Python files in this category
                    python_files = list(item.glob("*.py"))
                    categories.append({
                        "name": item.name,
                        "display_name": item.name.replace('_', ' ').title(),
                        "animation_count": len(python_files),
                        "path": str(item)
                    })
        
        return sorted(categories, key=lambda x: x["display_name"])
    
    def get_animations_in_category(self, category):
        """Get list of animations in a specific category"""
        category_dir = self.root_dir / "Animations" / category
        animations = []
        
        if category_dir.exists():
            for py_file in category_dir.glob("*.py"):
                if py_file.is_file():
                    animations.append({
                        "filename": py_file.name,
                        "title": py_file.stem.replace('_', ' ').title(),
                        "size": py_file.stat().st_size,
                        "modified": py_file.stat().st_mtime
                    })
        
        return sorted(animations, key=lambda x: x["title"])

# Test function
def test_render_handler():
    """Test the render handler system"""
    handler = RenderHandler()
    print("✅ Render Handler Ready")
    print(f"📁 Root: {handler.root_dir}")
    
    # Show available categories
    categories = handler.get_animation_categories()
    print(f"📂 Found {len(categories)} categories:")
    for category in categories:
        print(f"   - {category['display_name']} ({category['animation_count']} animations)")
    
    # Show available qualities
    qualities = handler.get_available_qualities()
    print(f"🎚️ Available qualities: {', '.join(qualities.keys())}")

if __name__ == "__main__":
    test_render_handler()