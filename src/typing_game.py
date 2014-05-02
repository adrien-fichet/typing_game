# -*- coding: utf-8 -*-

import sys
import ctypes

from PyQt5 import QtCore, QtWidgets, QtGui
from src.menu.menu_widget import MenuWidget
from src.typing_board import TypingBoard
from src.input_widget import InputWidget


class TypingGame(QtWidgets.QWidget):
    nb_of_lives = 5

    def __init__(self, parent=None):
        super(TypingGame, self).__init__(parent)
        self.setWindowTitle('Typing Game')
        self.setWindowIcon(QtGui.QIcon('data/icon.png'))
        self.setFixedSize(700, 550)
        self.typing_board = TypingBoard(self)
        self.typing_board.move(10, 10)
        self.input_widget = InputWidget(self)
        self.input_widget.move(10, 520)
        self.menu_widget = MenuWidget(self)
        self.menu_widget.move(510, 10)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

        elif event.key() == QtCore.Qt.Key_F5:
            self.typing_board.start_or_pause_game()

    def validate_input(self, w):
        words = [i.text for i in self.typing_board.displayed_word_widgets]

        if w in words:
            word_widget = self.typing_board.find_word_widget(w)
            self.typing_board.displayed_word_widgets.remove(word_widget)
            word_widget.move_to_initial_position()
            self.typing_board.score += 1
            self.menu_widget.score_label.setText('Score : {}'.format(self.typing_board.score))

    def lose_one_life(self):
        if self.nb_of_lives > 1:
            self.nb_of_lives -= 1
            self.menu_widget.life_widget.remove_one_life()
        else:
            self.menu_widget.life_widget.remove_one_life()
            self.show_end_game()

    def show_end_game(self):
        self.nb_of_lives = 5
        self.typing_board.stop_game()


def main():
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('sniksnp.typing_game')
    app = QtWidgets.QApplication(sys.argv)
    window = TypingGame()
    window.show()
    sys.exit(app.exec_())
