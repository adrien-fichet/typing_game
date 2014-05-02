#-*-coding:utf-8-*-

from PyQt5 import QtWidgets, QtGui


class HelpLabel(QtWidgets.QLabel):

    def __init__(self, parent=None, help_text=None):
        super(HelpLabel, self).__init__(parent)
        self.parent = parent
        self.help_text = help_text
        self.setFont(QtGui.QFont('Monospace', 9))
        self.setMinimumHeight(len(self.help_text.split('\n')) * 15 + 10)

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setPen(QtGui.QColor(0, 0, 0))
        qp.setBrush(QtGui.QColor(200, 200, 200))
        qp.drawRect(0, 0, self.width() - 1, self.height() - 1)

        for i in range(len(self.help_text.split('\n'))):
            qp.drawText(10, 17 + 15 * i, self.help_text.split('\n')[i])

        qp.end()
