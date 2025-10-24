#!/usr/bin/env python3
"""
Emanim Studio - Simple Launcher
Uses absolute path to find EmanimStudio.bat
"""

import os
import subprocess
import tkinter as tk
from tkinter import messagebox


def launch_emanim_studio():
    """Launch the main EmanimStudio.bat using absolute path"""
    # Get the current script directory to find the project folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_folder = script_dir  # Use current directory where main.py is located
    bat_file = os.path.join(project_folder, "EmanimStudio.bat")

    if os.path.exists(bat_file):
        try:
            # Launch EmanimStudio.bat in a new command window
            subprocess.Popen(f'start cmd /k "{bat_file}"', shell=True)
            print("🚀 Launching Emanim Studio...")
            # Close the launcher after starting
            root.after(1000, root.destroy)
        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to launch Emanim Studio:\n{e}")
    else:
        messagebox.showerror(
            "Error", f"EmanimStudio.bat not found!\nLooking for: {bat_file}")


# Create the main window
root = tk.Tk()
root.title("Emanim Studio")
root.geometry("400x300")
root.eval('tk::PlaceWindow . center')  # Center window

# CLASSIC BLUE BACKGROUND
root.configure(bg='#0078D7')  # Windows classic blue

# Main header
header = tk.Label(root, text="🎬 Emanim Studio",
                  font=("Arial", 24, "bold"),
                  fg="white", bg='#0078D7')
header.pack(pady=30)

# Version info
version = tk.Label(root, text="Ready to animate!",
                   font=("Arial", 12),
                   fg="white", bg='#0078D7')
version.pack(pady=5)

# Big Start button (white with blue text to match classic theme)
start_button = tk.Button(root,
                         text="🚀 START HERE",
                         command=launch_emanim_studio,
                         font=("Arial", 18, "bold"),
                         bg="white",
                         fg="#0078D7",  # Changed to blue to match theme
                         width=20,
                         height=3,
                         cursor="hand2",
                         relief="raised",
                         bd=3)
start_button.pack(pady=40)

# Footer
footer = tk.Label(root, text="Click START to begin animating with Manim",
                  font=("Arial", 10),
                  fg="white", bg='#0078D7')
footer.pack(side=tk.BOTTOM, pady=10)

# Start the GUI
root.mainloop()
