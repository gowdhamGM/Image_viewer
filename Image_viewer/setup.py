import sys
from cx_Freeze import setup, Executable
import os

PYTHON_INSTALLATION = "%s/" % os.path.split(sys.executable)[0]
os.environ['TCL_LIBRARY'] = "%stcl/tcl8.6" % PYTHON_INSTALLATION
os.environ['TK_LIBRARY'] = "%stcl/tk8.6" % PYTHON_INSTALLATION
# Dependencies are automatically detected, but it might need fine tuning.
#build_exe_options = {"packages": ["os", "sys", "pygame", "ezpygame"], "excludes": ["tkinter"]} no
#build_exe_options = {"packages": ["os", "sys", "pygame", "ezpygame", "tkinter"]} still no

build_exe_options = {"includes": ["os", "sys", "pygame", "ezpygame", "random"], "include_files":["%sDLLs/tcl86t.dll" % PYTHON_INSTALLATION, "%sDLLs/tk86t.dll" % PYTHON_INSTALLATION], "optimize":2} # aw yis
# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "gestdera",
        version = "00001",
        description = "Gesture drawing app",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base=base)])