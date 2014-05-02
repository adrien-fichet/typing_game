# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets, QtGui


class LifeWidget(QtWidgets.QWidget):

    def __init__(self, parent=None, width=50, nb_lives=5):
        super(LifeWidget, self).__init__(parent)
        self.width = width
        self.nb_lives = nb_lives
        self.nb_lives_remaining = self.nb_lives
        self.setFixedSize(self.width, self.nb_lives * self.width)

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setPen(QtCore.Qt.NoPen)

        for i in range(0, self.nb_lives * self.width, self.width):

            if (float(i) / self.width) < self.nb_lives_remaining:
                qp.setBrush(QtGui.QColor(0, 255, 0))
            else:
                qp.setBrush(QtGui.QColor(255, 0, 0))

            qp.drawRect(0, self.nb_lives * self.width - (i + self.width), self.width - 1, self.width - 1)

        qp.end()

    def remove_one_life(self):
        if self.nb_lives_remaining > 0:
            self.nb_lives_remaining -= 1
            self.repaint()

    def reset(self):
        self.nb_lives_remaining = self.nb_lives
        self.repaint()