#!/usr/bin/env python3
"""
EmanimStudio Dependency Test - CORRECT PATHS
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path


def log_message(message):
    """Print message to console and log file"""
    print(f"[TEST] {message}")
    with open("dependency_test.log", "a", encoding="utf-8") as f:
        f.write(f"{message}\n")


def test_python_environment():
    """Test if Python environment is self-contained"""
    log_message("=== TESTING PYTHON ENVIRONMENT ===")

    python_exe = Path("Lib/python312/python.exe")
    if python_exe.exists():
        log_message(f"✓ Python executable found: {python_exe}")
    else:
        log_message(f"✗ Python executable missing: {python_exe}")
        return False

    try:
        result = subprocess.run([
            str(python_exe),
            "-c",
            "import sys; print('Python path:', sys.prefix); import manim; print('Manim version:', manim.__version__)"
        ], capture_output=True, text=True, timeout=30, cwd=os.getcwd())

        if result.returncode == 0:
            log_message("✓ Python imports work")
            for line in result.stdout.split('\n'):
                if 'Python path' in line or 'Manim version' in line:
                    log_message(f"  {line.strip()}")
        else:
            log_message(f"✗ Python imports failed: {result.stderr}")
            return False

    except Exception as e:
        log_message(f"✗ Python test error: {e}")
        return False

    return True


def test_ffmpeg():
    """Test if FFmpeg works - CORRECT PATH"""
    log_message("=== TESTING FFMPEG ===")

    # CORRECT PATH: Lib\FFmpeg\bin\ffmpeg.exe
    ffmpeg_exe = Path("Lib/FFmpeg/bin/ffmpeg.exe")

    if not ffmpeg_exe.exists():
        log_message(f"✗ FFmpeg executable not found at: {ffmpeg_exe}")
        # Show what's actually in Lib/FFmpeg
        ffmpeg_dir = Path("Lib/FFmpeg")
        if ffmpeg_dir.exists():
            log_message("Contents of Lib/FFmpeg:")
            for item in ffmpeg_dir.rglob("*"):
                if item.is_file():
                    log_message(f"  - {item.relative_to(ffmpeg_dir)}")
        return False

    log_message(f"✓ FFmpeg found: {ffmpeg_exe}")

    try:
        result = subprocess.run([
            str(ffmpeg_exe),
            "-version"
        ], capture_output=True, text=True, timeout=10, cwd=os.getcwd())

        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if 'ffmpeg version' in line:
                    log_message(f"✓ FFmpeg version: {line.split()[2]}")
                    break
            return True
        else:
            log_message(f"✗ FFmpeg test failed: {result.stderr}")
            return False

    except Exception as e:
        log_message(f"✗ FFmpeg test error: {e}")
        return False


def test_miktex():
    """Test if MiKTeX works - CORRECT PATH"""
    log_message("=== TESTING MIKTEX ===")

    # CORRECT PATH: Lib\Miktex\texmfs\install\miktex\bin\x64\pdflatex.exe
    pdflatex_exe = Path(
        "Lib/Miktex/texmfs/install/miktex/bin/x64/pdflatex.exe")

    if not pdflatex_exe.exists():
        log_message(f"✗ pdflatex executable not found at: {pdflatex_exe}")
        return False

    log_message(f"✓ pdflatex found: {pdflatex_exe}")

    try:
        result = subprocess.run([
            str(pdflatex_exe),
            "--version"
        ], capture_output=True, text=True, timeout=10, cwd=os.getcwd())

        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if 'MiKTeX' in line:
                    log_message(f"✓ MiKTeX version: {line.strip()}")
                    break
            return True
        else:
            log_message(f"✗ MiKTeX test failed: {result.stderr}")
            return False

    except Exception as e:
        log_message(f"✗ MiKTeX test error: {e}")
        return False


def test_animation_rendering():
    """Test if we can actually render an animation"""
    log_message("=== TESTING ANIMATION RENDERING ===")

    animation_file = Path("Animations/Math/1. 2SetVennDiagram.py")
    if not animation_file.exists():
        log_message("✗ Test animation file not found")
        return False

    python_exe = Path("Lib/python312/python.exe")

    try:
        # Create Test_Output directory
        Path("Test_Output").mkdir(exist_ok=True)

        result = subprocess.run([
            str(python_exe),
            "-m", "manim",
            "render",
            str(animation_file),
            "VennDiagramAB",
            "-ql",  # low quality for speed
            "--media_dir", "Test_Output"
        ], capture_output=True, text=True, timeout=120, cwd=os.getcwd())

        if result.returncode == 0:
            log_message("✓ Animation rendering successful!")

            # Check if video was created
            video_path = Path(
                "Test_Output/videos/1. 2SetVennDiagram/480p15/VennDiagramAB.mp4")
            if video_path.exists():
                size_mb = video_path.stat().st_size / (1024 * 1024)
                log_message(f"✓ Video created: {size_mb:.2f} MB")
                return True
            else:
                log_message("✗ Video file not created but command succeeded")
                # Check what was actually created
                if Path("Test_Output").exists():
                    log_message("Contents of Test_Output:")
                    for item in Path("Test_Output").rglob("*"):
                        log_message(f"  - {item}")
                return False
        else:
            log_message(f"✗ Rendering failed: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        log_message("✗ Rendering timed out (2 minutes)")
        return False
    except Exception as e:
        log_message(f"✗ Rendering error: {e}")
        return False


def main():
    """Run all dependency tests"""
    log_message("Starting EmanimStudio Dependency Test - CORRECT PATHS")
    log_message(f"Working directory: {os.getcwd()}")

    # Clear previous log
    if os.path.exists("dependency_test.log"):
        os.remove("dependency_test.log")

    tests = [
        test_python_environment,
        test_ffmpeg,
        test_miktex,
        test_animation_rendering
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        log_message("")  # Empty line between tests

    # Final results
    log_message("=== TEST RESULTS ===")
    log_message(f"Passed: {passed}/{total}")

    if passed == total:
        log_message("🎉 SUCCESS: EmanimStudio is fully self-contained!")
        return 0
    else:
        log_message("❌ FAILED: Some dependencies are missing or broken")
        return 1


if __name__ == "__main__":
    sys.exit(main())
