### Description
A word typing game. The goal is to type the words as they fall down before they reach the bottom
of the game window. The falling speed increases over time, and each word falls down more or less rapidly
depending on its length (shorter words fall down quicker).

Coded in Python3 with PyQt5.

### Screenshot
<p align="center">
  <img src="https://raw.githubusercontent.com/sniksnp/typing_game/master/im/screenshot.jpg" alt="" />
</p>

### How to run the application (dev)
- Install [Python 3.3.5](https://www.python.org/downloads/release/python-335)
- Install [PyQt5 5.2.1](http://www.riverbankcomputing.com/software/pyqt/download5)
- ```python run.py```

### How to build a Windows installer with cx_Freeze and Inno Setup
- Install [cx_Freeze](http://cx-freeze.sourceforge.net)
- ```python setup.py build```: this creates a ```build/exe.win32-3.3``` directory
- Install [Inno Setup](http://www.jrsoftware.org/isinfo.php)
- Launch the Inno Setup Compiler
- Create a new script file using the Script Wizard
  - Application main executable file = build/exe.win32-3.3/typing_game.exe
  - Other application files = build/exe.win32-3.3/*
  - Custom compiler output folder = typing_game/dist
  - Compiler output base file name = typing_game-setup
  - Custom setup icon file = im/icon.ico
- Compile the generated script: this creates ```dist/typing_game-setup.exe``` which can be used to install the
application on Windows

### Widgets hierarchy
The main widget, ```TypingGame```, is composed of a ```TypingBoard```, a ```MenuWidget``` and an
```InputWidget```. Each word of the ```TypingBoard``` is represented by a ```WordWidget```.
