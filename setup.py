import sys
from cx_Freeze import setup, Executable

includefiles = ['data/words.txt', 'im/icon.ico']
buildOptions = dict(packages=[], excludes=[], include_files=includefiles, icon='im/icon.ico')
base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable('run.py', base=base, targetName='typing_game.exe')
]

setup(
    name='typing_game',
    version='1.0',
    description='',
    options=dict(build_exe=buildOptions),
    executables=executables
)
