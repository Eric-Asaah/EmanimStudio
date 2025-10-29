#!/usr/bin/env python3
"""
Emanim Studio - Master Launcher
Installer Version - Animations in installation directory
ROBUST VERSION - Works after Inno Setup
"""

import os
import subprocess
import sys
import shutil
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QMessageBox, QGridLayout, QDialog, QTextBrowser,
    QSizePolicy, QSpacerItem, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtGui import QFont, QPainter, QColor


class PathManager:
    def __init__(self):
        self.setup_paths()
    
    def setup_paths(self):
        """INSTALLER VERSION - Animations stay in installation directory"""
        # Base directory - where EXE or script lives
        if getattr(sys, 'frozen', False):
            self.exe_dir = Path(sys.executable).parent
        else:
            self.exe_dir = Path(__file__).parent
        
        # ANIMATIONS STAY IN INSTALLATION FOLDER (Read-only)
        self.animations_dir = self.exe_dir / "Animations"
        
        # Only user output goes to Desktop
        desktop_dir = Path.home() / "Desktop"
        self.output_dir = desktop_dir / "EmanimStudio Videos"
        
        # Critical paths
        self.python_home = self.exe_dir / "Lib" / "Python312"
        self.batch_file = self.exe_dir / "emanim_terminal.bat"
        
        # Create output directory only (animations are pre-bundled)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Set environment
        os.environ["STUDIO_ROOT"] = str(self.exe_dir)
        os.environ["PYTHON_HOME"] = str(self.python_home)
        os.environ["OUTPUT_DIR"] = str(self.output_dir)
        os.environ["ANIMATIONS_DIR"] = str(self.animations_dir)
    
    def get_batch_command(self):
        """Get command to launch terminal"""
        return [str(self.batch_file)]
    
    def get_python_executable(self):
        """Get Python executable path with fallback"""
        candidate = self.python_home / "python.exe"
        if sys.platform.startswith("win") and candidate.exists():
            return str(candidate)
        else:
            return shutil.which("python") or sys.executable


class AnimatedSymbol(QLabel):
    def __init__(self, symbol, parent=None):
        super().__init__(symbol, parent)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                font-size: 24px;
                color: rgba(100, 255, 218, 0.8);
                background: transparent;
                border: none;
            }
        """)

        # Create floating animation
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(3000 + (hash(symbol) % 2000))
        self.animation.setLoopCount(-1)

    def start_animation(self, start_pos, end_pos):
        self.animation.setStartValue(start_pos)
        self.animation.setEndValue(end_pos)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.start()


class SysInfoDialog(QDialog):
    def __init__(self, html_content: str, parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setModal(True)

        # Size and placement relative to parent
        parent_rect = parent.geometry() if parent else QRect(100, 100, 900, 600)
        w = min(1000, int(parent_rect.width() * 0.9))
        h = min(720, int(parent_rect.height() * 0.8))
        self.resize(w, h)
        if parent:
            pr = parent.geometry()
            self.move(pr.x() + (pr.width() - w) // 2, pr.y() + (pr.height() - h) // 2)

        # Shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(12, 36, 60, 160))

        # Main container
        self.card = QWidget(self)
        self.card.setObjectName("sys_card")
        self.card.setGraphicsEffect(shadow)
        self.card.setGeometry(20, 20, w - 40, h - 40)

        card_style = """
            QWidget#sys_card {
                background: rgba(10, 25, 47, 0.95);
                border: 1px solid rgba(100, 255, 218, 0.14);
                border-radius: 12px;
            }
        """
        self.card.setStyleSheet(card_style)

        main_layout = QVBoxLayout(self.card)
        main_layout.setContentsMargins(18, 12, 18, 12)
        main_layout.setSpacing(12)

        # Top bar
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(0, 0, 0, 0)
        top_bar.setSpacing(6)

        title = QLabel("ℹ️ EmanimStudio")
        title.setStyleSheet("font-size:18px; color: #64ffda; font-weight:bold;")
        title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        top_bar.addWidget(title)

        top_bar.addItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Back button
        back_btn = QPushButton("Back")
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setFixedHeight(30)
        back_btn.setFixedWidth(90)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(100,255,218,0.95);
                color: #0a192f;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0a192f;
                color: #64ffda;
                border: 2px solid #64ffda;
            }
        """)
        back_btn.clicked.connect(self.accept)
        top_bar.addWidget(back_btn)

        main_layout.addLayout(top_bar)

        # Content area
        content = QTextBrowser()
        content.setHtml(html_content)
        content.setOpenExternalLinks(True)
        content.setReadOnly(True)
        content.setStyleSheet("""
            QTextBrowser {
                background: transparent;
                border: none;
                color: #ccd6f6;
                font-family: "Courier New", monospace;
                font-size: 12px;
            }
            a { color: #64ffda; }
        """)
        main_layout.addWidget(content, 1)

        # Bottom caption
        caption = QLabel("Professional mathematical animation studio")
        caption.setStyleSheet("font-size:11px; color: #8892b0;")
        caption.setAlignment(Qt.AlignRight)
        main_layout.addWidget(caption)

        # Fade-in animation
        self._fade = QPropertyAnimation(self, b"windowOpacity")
        self._fade.setDuration(260)
        self._fade.setStartValue(0.0)
        self._fade.setEndValue(1.0)
        self._fade.setEasingCurve(QEasingCurve.InOutQuad)
        self.setWindowOpacity(0.0)
        self._fade.start()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.accept()
        else:
            super().keyPressEvent(event)


class EmanimMasterLauncher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.pm = PathManager()
        self.setup_environment()
        self.init_ui()
        self.animated_symbols = []

    def setup_environment(self):
        """Setup environment variables using PathManager"""
        self.studio_root = str(self.pm.exe_dir)
        self.script_dir = str(self.pm.exe_dir)
        self.animations_dir = str(self.pm.animations_dir)
        self.output_dir = str(self.pm.output_dir)
        self.python_home = str(self.pm.python_home)

        self.pythonpath = os.path.join(self.python_home, "Lib", "site-packages")
        self.ffmpeg_bin = os.path.join(self.script_dir, "Lib", "FFmpeg", "bin")
        self.miktex_bin = os.path.join(self.script_dir, "Lib", "Miktex", "texmfs", "install", "miktex", "bin", "x64")

        os.environ["PYTHONPATH"] = self.pythonpath

        # Safe PATH building
        current_path = os.environ.get("PATH", "")
        parts = [current_path]
        
        if os.path.exists(self.python_home):
            parts.insert(0, self.python_home)
        if os.path.exists(self.ffmpeg_bin):
            parts.insert(0, self.ffmpeg_bin)
        if os.path.exists(self.miktex_bin):
            parts.insert(0, self.miktex_bin)
        
        os.environ["PATH"] = os.pathsep.join(parts)

    def init_ui(self):
        """Initialize the UI - NORMAL WINDOW BEHAVIOR"""
        self.setWindowTitle("EmanimStudio - Mathematical Animation Studio")
        
        # NORMAL WINDOW WITH ALL CONTROLS
        self.setWindowFlags(Qt.Window | 
                           Qt.WindowMinimizeButtonHint |
                           Qt.WindowMaximizeButtonHint |
                           Qt.WindowCloseButtonHint)
        
        # Set size constraints for good UX
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)
        
        # Show as normal resizable window
        self.showNormal()

        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0a192f, stop:0.3 #112240, stop:0.6 #1d3b5c, stop:1 #2d547a);
            }
            QLabel {
                color: white;
                background: transparent;
            }
            QPushButton {
                background-color: rgba(100, 255, 218, 0.9);
                color: #0a192f;
                font-size: 16px;
                font-weight: bold;
                border: 2px solid #64ffda;
                border-radius: 12px;
                padding: 20px;
                min-width: 220px;
                min-height: 70px;
            }
            QPushButton:hover {
                background-color: #0a192f;
                color: #64ffda;
                border: 2px solid #64ffda;
            }
            QPushButton:pressed {
                background-color: #112240;
                color: #64ffda;
            }
        """)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(25)
        main_layout.setContentsMargins(60, 40, 60, 40)

        # Header Section
        header_layout = QVBoxLayout()
        header_layout.setSpacing(15)

        emanim_title = QLabel("EMANIM")
        emanim_title.setAlignment(Qt.AlignCenter)
        emanim_title.setStyleSheet("""
            font-size: 82px;
            font-weight: bold;
            color: #64ffda;
            letter-spacing: 10px;
            margin: 25px;
            background: transparent;
        """)
        header_layout.addWidget(emanim_title)

        studio_title = QLabel("STUDIO")
        studio_title.setAlignment(Qt.AlignCenter)
        studio_title.setStyleSheet("""
            font-size: 64px;
            font-weight: bold;
            color: #ff6b6b;
            letter-spacing: 15px;
            margin-bottom: 15px;
            background: transparent;
        """)
        header_layout.addWidget(studio_title)

        math_symbols = QLabel("∫ ∑ π ∞ ∇ Δ ∮ ∏ √ ∂ ± × ÷")
        math_symbols.setAlignment(Qt.AlignCenter)
        math_symbols.setStyleSheet("""
            font-size: 28px;
            color: rgba(168, 178, 209, 0.7);
            letter-spacing: 12px;
            margin: 20px;
            opacity: 0.8;
            background: transparent;
        """)
        header_layout.addWidget(math_symbols)

        tagline = QLabel("PROFESSIONAL MATHEMATICAL ANIMATION STUDIO")
        tagline.setAlignment(Qt.AlignCenter)
        tagline.setStyleSheet("""
            font-size: 22px;
            color: #f8f9fa;
            letter-spacing: 4px;
            margin-bottom: 10px;
            background: transparent;
        """)
        header_layout.addWidget(tagline)

        brand = QLabel("EMANIMSTUDIO IS A PRODUCT OF EMAPHY")
        brand.setAlignment(Qt.AlignCenter)
        brand.setStyleSheet("""
            font-size: 16px;
            color: #ccd6f6;
            margin-bottom: 8px;
            background: transparent;
        """)
        header_layout.addWidget(brand)

        creator = QLabel("A comprehensive learning platform by Eric Asaah")
        creator.setAlignment(Qt.AlignCenter)
        creator.setStyleSheet("""
            font-size: 14px;
            color: #8892b0;
            font-style: italic;
            margin-bottom: 40px;
            background: transparent;
        """)
        header_layout.addWidget(creator)

        main_layout.addLayout(header_layout)

        # Button Grid
        button_layout = QGridLayout()
        button_layout.setSpacing(25)
        button_layout.setContentsMargins(120, 30, 120, 30)

        buttons = [
            ("🚀 LAUNCH TERMINAL", "Complete animation control terminal", self.launch_terminal),
            ("ℹ️ SYSTEM INFO", "View installation details and content", self.launch_sysinfo),
            ("📖 DOCUMENTATION", "Read instructions and guides", self.launch_readme),
            ("🚪 EXIT", "Close EmanimStudio", self.exit_app)
        ]

        for i, (text, tooltip, callback) in enumerate(buttons):
            btn = QPushButton(text)
            btn.setToolTip(tooltip)
            btn.clicked.connect(callback)
            row = i // 2
            col = i % 2
            button_layout.addWidget(btn, row, col)

        main_layout.addLayout(button_layout)
        main_layout.addStretch()

        # Footer
        footer_layout = QHBoxLayout()
        footer_left = QLabel("EmanimStudio v2.0 • Professional Animation Engine")
        footer_left.setStyleSheet("font-size: 11px; color: #8892b0; background: transparent;")

        footer_right = QLabel("Emaphy Platform • Created by Eric Asaah")
        footer_right.setAlignment(Qt.AlignRight)
        footer_right.setStyleSheet("font-size: 11px; color: #8892b0; background: transparent;")

        footer_layout.addWidget(footer_left)
        footer_layout.addStretch()
        footer_layout.addWidget(footer_right)

        main_layout.addLayout(footer_layout)

        # Start floating symbols
        QTimer.singleShot(100, self.start_floating_symbols)

    def start_floating_symbols(self):
        symbols = ["∫", "∑", "π", "∞", "∇", "Δ", "∮", "∏", "√", "∂", "±", "×", "÷", "="]

        for symbol in symbols[:8]:
            animated_symbol = AnimatedSymbol(symbol, self)
            self.animated_symbols.append(animated_symbol)

            x = 100 + (hash(symbol) % max(1, (self.width() - 200)))
            y = 150 + (hash(symbol) % 250)

            end_x = x + (hash(symbol) % 100 - 50)
            end_y = y + (hash(symbol) % 80 - 40)

            animated_symbol.move(x, y)
            animated_symbol.show()
            animated_symbol.start_animation(animated_symbol.pos(),
                                            animated_symbol.pos() + type(animated_symbol.pos())(end_x - x, end_y - y))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()

    def launch_terminal(self):
        """ROBUST terminal launch - TERMINAL in FULLSCREEN, GUI as normal window"""
        if not self.pm.batch_file.exists():
            QMessageBox.critical(self, "File Not Found", 
                               f"Terminal batch file not found!\n\nLooking for: {self.pm.batch_file}")
            return

        try:
            # Remember GUI window state
            self.was_maximized = self.isMaximized()
            
            # Hide GUI
            self.hide()
            
            # LAUNCH TERMINAL IN FULLSCREEN - SIMPLE & RELIABLE APPROACH
            if sys.platform == 'win32':
                # Windows: Use start with /max for fullscreen terminal
                process = subprocess.Popen([
                    'cmd.exe', '/c',
                    'start', '/max', 'EmanimStudio Terminal',  # /max = fullscreen
                    str(self.pm.batch_file)
                ], 
                cwd=str(self.pm.exe_dir),
                shell=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)
            else:
                # Other platforms
                process = subprocess.Popen([
                    str(self.pm.batch_file)
                ], 
                cwd=str(self.pm.exe_dir),
                shell=True)
            
            # Wait for terminal to complete
            process.wait()
            
            # Restore GUI with previous state (NORMAL WINDOW)
            self.show()
            if self.was_maximized:
                self.showMaximized()  # GUI returns maximized if it was before
            else:
                self.showNormal()     # GUI returns as normal window
                
            self.raise_()
            self.activateWindow()
            
        except Exception as e:
            # Always restore GUI on error
            self.show()
            QMessageBox.critical(self, "Launch Error", 
                               f"Failed to launch terminal:\n{str(e)}")

    def launch_sysinfo(self):
        try:
            python_exe = self.pm.get_python_executable()
            cmd = [
                python_exe, "-c",
                "import sys, os, platform; from pathlib import Path; "
                "print('=== EMANIM STUDIO SYSTEM INFO ==='); print(); "
                "print(f'Python: {sys.version.split()[0]}'); "
                "print(f'Platform: {platform.system()} {platform.release()}'); print(); "
                "print('FOLDERS:'); cwd = Path('.').resolve(); "
                "print(f'   Location: {cwd}'); "
                f"print(f'   Animations: {{\"OK\" if Path(\"{self.animations_dir}\").exists() else \"MISSING\"}}'); "
                f"print(f'   Output: {{\"OK\" if Path(\"{self.output_dir}\").exists() else \"MISSING\"}}'); print(); "
                "print('TOOLS:'); "
                "try: import manim; print(f'   Manim: {manim.__version__}'); "
                "except: print('   Manim: NOT FOUND'); "
                "try: import numpy; print(f'   NumPy: {numpy.__version__}'); "
                "except: print('   NumPy: NOT FOUND'); print(); "
                f"print('CONTENT:'); anim_dir = Path('{self.animations_dir}'); "
                "if anim_dir.exists(): "
                "    cats = [d.name for d in anim_dir.iterdir() if d.is_dir()]; "
                "    total = sum(len(list(c.glob('*.py'))) for c in cats); "
                "    print(f'   Categories: {len(cats)}'); print(f'   Files: {total}'); "
                "else: print('   No animations folder found');"
            ]

            process = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', 
                                   cwd=str(self.pm.exe_dir), timeout=10)

            if process.returncode != 0:
                self.show_basic_sysinfo()
                return

            sysinfo_text = process.stdout.strip()
            info_html = f"""
            <h2 style="color: #64ffda;">ℹ️ EmanimStudio System Information</h2>
            <div style="font-family: 'Courier New', monospace; font-size: 12px; background: #112240; color: #ccd6f6; padding: 14px; border-radius: 8px; border: 1px solid #1e3a52; line-height: 1.45;">
            <pre>{sysinfo_text}</pre>
            </div>
            <p style="font-size: 12px; margin-top: 12px; color: #8892b0;">
            Professional mathematical animation studio
            </p>
            """

            dlg = SysInfoDialog(info_html, parent=self)
            dlg.exec_()

        except Exception:
            self.show_basic_sysinfo()

    def show_basic_sysinfo(self):
        animation_status = "READY" if self.pm.animations_dir.exists() else "MISSING"
        animation_count = 0
        if self.pm.animations_dir.exists():
            for category in ["Math", "Physics", "Emaphy", "Miscellaneous"]:
                category_dir = self.pm.animations_dir / category
                if category_dir.exists():
                    animation_count += len(list(category_dir.glob("*.py")))

        info_html = f"""
        <h2 style="color: #64ffda;">ℹ️ EmanimStudio System Information</h2>
        <div style="font-family: Arial, sans-serif; font-size: 13px; background: #112240; color: #ccd6f6; padding: 14px; border-radius: 8px; border: 1px solid #1e3a52;">
        <p><b>Mode:</b> PROFESSIONAL INSTALLATION</p>
        <p><b>Location:</b> {self.studio_root}</p>
        <p><b>Animations:</b> {animation_status} ({animation_count} animations)</p>
        <p><b>Output:</b> {self.output_dir}</p>
        <p><b>Status:</b> Ready to render animations</p>
        <p><b>Features:</b> Mathematical animations, Video rendering, LaTeX support</p>
        </div>
        <p style="font-size: 12px; margin-top: 12px; color: #8892b0;">
        Create amazing mathematical visualizations with EmanimStudio!
        </p>
        """
        dlg = SysInfoDialog(info_html, parent=self)
        dlg.exec_()

    def launch_readme(self):
        doc_html = """
        <h1 style="color:#64ffda; margin-bottom:6px;">EMANIM STUDIO - PROFESSIONAL MATHEMATICAL ANIMATION STUDIO</h1>

        <h3 style="color:#ccd6f6; margin-top:8px;">QUICK START</h3>
        <div style="background:#0f2436; padding:10px; border-radius:6px;">
        <ul>
          <li>Launch <b>EmanimStudio</b> from Start Menu or Desktop</li>
          <li>Choose <b>LAUNCH TERMINAL</b> for animation control</li>
          <li>Browse pre-built mathematical animations</li>
          <li>Render professional videos instantly</li>
        </ul>
        </div>

        <h3 style="color:#ccd6f6; margin-top:8px;">FOLDER STRUCTURE</h3>
        <div style="background:#0f2436; padding:10px; border-radius:6px;">
        <ul>
          <li><b>Program Files/EmanimStudio/</b> - Application files and animations</li>
          <li><b>Desktop/EmanimStudio Videos/</b> - Rendered videos</li>
        </ul>
        </div>

        <h3 style="color:#ccd6f6; margin-top:8px;">GETTING STARTED</h3>
        <div style="background:#0f2436; padding:10px; border-radius:6px;">
        <ol>
          <li>Launch EmanimStudio</li>
          <li>Select LAUNCH TERMINAL</li>
          <li>Choose animation category</li>
          <li>Select animation template</li>
          <li>Set quality (480p to 4K)</li>
          <li>Render and enjoy!</li>
        </ol>
        </div>

        <h3 style="color:#ccd6f6; margin-top:8px;">VIDEO LOCATION</h3>
        <div style="background:#0f2436; padding:10px; border-radius:6px;">
        <p>Your rendered videos are automatically saved to:</p>
        <p><b>Desktop/EmanimStudio Videos/</b></p>
        <p>This folder is created automatically and easy to find!</p>
        </div>

        <h3 style="color:#ccd6f6; margin-top:8px;">ANIMATIONS</h3>
        <div style="background:#0f2436; padding:10px; border-radius:6px;">
        <p>EmanimStudio comes with pre-built animations:</p>
        <ul>
          <li><b>Math:</b> Calculus, Geometry, Algebra</li>
          <li><b>Physics:</b> Mechanics, Waves, Optics</li>
          <li><b>Emaphy:</b> Educational content</li>
          <li><b>Miscellaneous:</b> Various visualizations</li>
        </ul>
        </div>

        <h3 style="color:#ccd6f6; margin-top:8px;">META</h3>
        <div style="background:#0f2436; padding:10px; border-radius:6px;">
        <p><b>CREATED BY:</b> Eric Asaah<br>
        <b>WEBSITE:</b> <a href="https://github.com/ericasaah">https://github.com/ericasaah</a><br>
        <b>VERSION:</b> 2.0</p>
        </div>
        """

        dlg = SysInfoDialog(doc_html, parent=self)
        dlg.exec_()

    def exit_app(self):
        reply = QMessageBox.question(self, "Exit EmanimStudio",
                                     "<h3>🚪 Exit EmanimStudio?</h3><p>Are you sure you want to close the application?</p>",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.quit()


def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Arial", 11))
    app.setApplicationName("EmanimStudio")
    app.setOrganizationName("Emaphy")
    app.setApplicationVersion("2.0")
    launcher = EmanimMasterLauncher()
    launcher.showNormal()  # Normal window behavior
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()