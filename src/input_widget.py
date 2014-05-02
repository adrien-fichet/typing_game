#-*-coding:utf-8-*-

from PyQt5 import QtWidgets, QtGui, QtCore


class InputWidget(QtWidgets.QLineEdit):

    def __init__(self, parent=None):
        super(InputWidget, self).__init__(parent)
        self.parent = parent
        self.setReadOnly(True)
        self.setMinimumWidth(500)
        self.setFont(QtGui.QFont('Monospace', 14))
        self.setAlignment(QtCore.Qt.AlignHCenter)
        self.setStyleSheet(
            '''
            QLineEdit {
                background-color : black;
                color : lime;
                border : 0px
            }
            '''
        )
        self.returnPressed.connect(self.validate_input)

    def validate_input(self):
        if not self.isReadOnly():
            self.parent.validate_input(self.text())
            self.setText('')