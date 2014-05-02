# Description
A word typing game. The goal is to type the words as they fall down before they reach the bottom
of the game window. The falling speed increases over time. Each word falls down more or less rapidly
depending on its length (shorter words fall down quicker).

Coded in Python3 with PyQt5.

# How to run the application
Install [Python 3.3.5](https://www.python.org/downloads/release/python-335)
Install [PyQt5 5.2.1](http://www.riverbankcomputing.com/software/pyqt/download5)

```
python run.py
```

# Widgets hierarchy
The main widget, ```TypingGame```, is composed of a ```TypingBoard```, a ```MenuWidget``` and an
```InputWidget```. Each word of the ```TypingBoard``` is represented by a ```WordWidget```.
