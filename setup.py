import sys
from cx_Freeze import setup, Executable

# Get the App class for the version and name.
from src.app import App

# GUI applications require a different
# base on Windows (the default is for a console application).
base = None

if sys.platform == "win32":
    base = "Win32GUI"

build_exe_options = {
    "packages": [
        "pygame",
    ],
    "excludes": [
        "tkinter",
        "pygame.examples",
    ],
    "include_files": [
        # directories
        'assets',

        # files
        'maze.txt',
    ],
    "build_exe":
        f'build\\{App.SLUG_NAME}-v{App.VERSION}+exe.{sys.platform}'
}

setup(
    name=App.NAME,
    version=App.VERSION,
    description="A game made with pygame and ❤.",
    options={"build_exe": build_exe_options},
    executables=[
        Executable("main.py", base=base, targetName=App.SLUG_NAME)
    ],
)
