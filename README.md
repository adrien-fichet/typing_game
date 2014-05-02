# Description
A word typing game. The goal is to type the words as they fall down before they reach the bottom
of the game window. The falling speed increases over time. Each word falls down more or less rapidly
depending on its length (shorter words fall down quicker).

Coded in Python with PyQt.

# How to run the application
```
python run.py
```

# Widgets hierarchy
The main widget (TypingGame) is composed of a scrolling zone (```TypingBoard```), a
menu (```MenuWidget```) and an input zone (```InputWidget```). Each word falling down
is a ```WordWidget```.
