"""
Unified Backend System for EmanimStudio
Provides single API for both terminal and GUI interfaces
"""
import os
import sys
from pathlib import Path

# Add current directory to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from AutoRepair import EmanimStudioRepair
    from RenderHandler import RenderHandler
    from VideoPlayer import VideoPlayer
    # Note: We'll handle emanim_gui import separately since it might not exist yet
except ImportError as e:
    print(f"⚠️ Import warning: {e}")

class EmanimBackend:
    """Main backend API for EmanimStudio"""
    
    def __init__(self, root_dir=None):
        self.root_dir = self._find_studio_root() if root_dir is None else Path(root_dir)
        self.repair = EmanimStudioRepair(self.root_dir)
        self.renderer = RenderHandler(self.root_dir)
        self.video_player = VideoPlayer(self.root_dir)
        
        print(f"🎯 EmanimBackend initialized at: {self.root_dir}")
    
    def _find_studio_root(self):
        """Automatically find the EmanimStudio root directory"""
        current_file = Path(__file__).resolve()
        if current_file.parent.name == "core" and current_file.parent.parent.name == "Scripts":
            return current_file.parent.parent.parent
        return Path.cwd()
    
    # System Management
    def run_diagnostics(self):
        """Run complete system diagnostics and repair"""
        return self.repair.run_complete_repair()
    
    def fix_environment(self):
        """Fix Python environment and paths"""
        return self.repair.fix_environment_paths()
    
    # Animation Management
    def get_categories(self):
        """Get available animation categories"""
        return self.renderer.get_animation_categories()
    
    def get_animations(self, category):
        """Get animations in a specific category"""
        return self.renderer.get_animations_in_category(category)
    
    def render_animation(self, category, filename, quality="medium"):
        """Render an animation"""
        return self.renderer.render_animation(category, filename, quality)
    
    # Video Management
    def play_video(self, video_path):
        """Play a video file"""
        return self.video_player.play_video(video_path)
    
    def play_latest_video(self):
        """Play the most recent video"""
        return self.video_player.play_latest_video()
    
    def list_videos(self):
        """List all available videos"""
        return self.video_player.list_videos()
    
    # GUI Interface
    def launch_gui(self):
        """Launch the GUI (emanim_gui)"""
        try:
            # Try to import emanim_gui dynamically
            gui_path = self.root_dir / "Scripts" / "emanim_gui.py"
            if gui_path.exists():
                # Add Scripts to Python path
                scripts_dir = self.root_dir / "Scripts"
                if str(scripts_dir) not in sys.path:
                    sys.path.insert(0, str(scripts_dir))
                
                # Import and run the GUI
                from emanim_gui import EmanimStudioGUI
                gui = EmanimStudioGUI()
                gui.run()
                return {"status": "success", "message": "GUI launched successfully"}
            else:
                return {
                    "status": "error", 
                    "message": "GUI not available yet",
                    "suggestion": "The graphical interface is still in development"
                }
        except Exception as e:
            return {
                "status": "error", 
                "message": f"Failed to launch GUI: {e}",
                "suggestion": "Use the terminal interface for now"
            }
    
    def launch_gui_placeholder(self):
        """Launch a simple GUI placeholder"""
        try:
            import tkinter as tk
            from tkinter import messagebox
            
            root = tk.Tk()
            root.title("EmanimStudio - Coming Soon!")
            root.geometry("400x300")
            root.configure(bg='#2b2b2b')
            
            # Simple placeholder message
            msg_frame = tk.Frame(root, bg='#2b2b2b')
            msg_frame.pack(expand=True, fill='both', padx=40, pady=40)
            
            tk.Label(msg_frame, text="🎬", font=("Arial", 32), 
                    bg='#2b2b2b', fg='white').pack(pady=10)
            
            tk.Label(msg_frame, text="Graphical Interface", 
                    font=("Arial", 18, "bold"), 
                    bg='#2b2b2b', fg='white').pack(pady=5)
            
            tk.Label(msg_frame, text="Coming Soon!", 
                    font=("Arial", 14), 
                    bg='#2b2b2b', fg='#ffa500').pack(pady=5)
            
            tk.Label(msg_frame, text="For now, please use the\nterminal interface", 
                    font=("Arial", 10), 
                    bg='#2b2b2b', fg='#cccccc').pack(pady=20)
            
            def switch_to_terminal():
                root.destroy()
                self._launch_terminal()
            
            tk.Button(msg_frame, text="Switch to Terminal", 
                     command=switch_to_terminal,
                     bg='#0078d4', fg='white',
                     font=("Arial", 10)).pack(pady=10)
            
            root.mainloop()
            return {"status": "success", "message": "GUI placeholder closed"}
            
        except Exception as e:
            return {"status": "error", "message": f"GUI placeholder failed: {e}"}
    
    def _launch_terminal(self):
        """Launch the terminal interface"""
        try:
            terminal_launcher = self.root_dir / "EmanimStudio.bat"
            if terminal_launcher.exists():
                os.system(f'cmd /c "{terminal_launcher}"')
        except Exception as e:
            print(f"❌ Could not launch terminal: {e}")
    
    # Utility Methods
    def open_animations_folder(self):
        """Open the animations folder in file explorer"""
        animations_dir = self.root_dir / "Animations"
        try:
            if animations_dir.exists():
                os.startfile(str(animations_dir))
                return {"status": "success", "message": "Animations folder opened"}
            else:
                return {"status": "error", "message": "Animations folder not found"}
        except Exception as e:
            return {"status": "error", "message": f"Could not open folder: {e}"}
    
    def open_output_folder(self):
        """Open the output videos folder"""
        output_dir = self.root_dir / "Output"
        try:
            if output_dir.exists():
                os.startfile(str(output_dir))
                return {"status": "success", "message": "Output folder opened"}
            else:
                return {"status": "error", "message": "Output folder not found"}
        except Exception as e:
            return {"status": "error", "message": f"Could not open folder: {e}"}

# Global instance for easy access
_backend_instance = None

def get_backend():
    """Get or create the global backend instance"""
    global _backend_instance
    if _backend_instance is None:
        _backend_instance = EmanimBackend()
    return _backend_instance

# Test function
def test_backend():
    """Test the unified backend system"""
    backend = get_backend()
    print("🎯 Testing EmanimStudio Backend...")
    
    # Test categories
    categories = backend.get_categories()
    print(f"📂 Found {len(categories)} categories:")
    for category in categories:
        print(f"   - {category['display_name']} ({category['animation_count']} animations)")
    
    # Test videos
    videos = backend.list_videos()
    print(f"🎥 Found {len(videos)} video files")
    
    print("✅ Backend system ready!")

if __name__ == "__main__":
    test_backend()