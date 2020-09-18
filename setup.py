import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["pygame"], "include_files": ['maze.txt', 'assets']}

# The version of the application
VERSION = "1.0"

# The filename of the compiled file
NAME = "macgyver-maze"

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None

if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="MacGyver Maze",
    version=VERSION,
    description="A game made with pygame and ❤.",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base, targetName="macgyver-maze")],
)
