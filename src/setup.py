import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["lxml", "termcolor", "requests", "json", "sys"], "excludes": ["tkinter"]}

setup(  name = "stackoverflow",
        version = "0.1",
        description = "A command line tool to search stack overflow for answers. Just type 'stackoverflow <your-query>'.",
        options = {"build_exe": build_exe_options},
        executables = [Executable("stackoverflow.py", base=None)])