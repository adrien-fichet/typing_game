#-*-coding:utf-8-*-

import random

from PyQt5 import QtWidgets, QtGui


class WordWidget(QtWidgets.QLabel):

    def __init__(self, parent=None, text=None):
        super(WordWidget, self).__init__(parent)
        self.parent = parent
        self.text = text
        self.nb_of_letters = float(len(self.text))
        self.setStyleSheet(
            """
            QLabel {
                color : lime
            }
            """
        )

        if self.text:
            self.setText(self.text)

        self.setFont(QtGui.QFont("Monospace", 14))
        self.move_to_initial_position()

    def move_down(self, interval):
        if self.y() >= self.parent.height():
            self.parent.displayed_word_widgets.remove(self)
            self.move_to_initial_position()
            self.parent.parent.lose_one_life()
        else:
            self.move(self.x(), self.y() + (interval / self.nb_of_letters * 0.5))

    def move_to_initial_position(self):
        self.move(random.randint(0, 400), -40)
