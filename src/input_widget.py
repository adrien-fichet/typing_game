#-*-coding:utf-8-*-

from PyQt5 import QtWidgets, QtGui, QtCore


class InputWidget(QtWidgets.QLineEdit):
    """ Un widget pour saisir les mots """

    def __init__(self, parent = None):
        super(InputWidget, self).__init__(parent)
        self.parent = parent
        self.setReadOnly(True)
        self.init_UI()

    def init_UI(self):
        """ Définition de l'interface graphique """
        self.setMinimumWidth(500)
        self.setFont(QtGui.QFont("Monospace", 14))
        self.setAlignment(QtCore.Qt.AlignHCenter)

        self.setStyleSheet(
            """
            QLineEdit {
            background-color : black;
            color : lime;
            border : 0px}
            """)

        # Connection du signal émis lors de l'appui sur Entrée
        self.returnPressed.connect(self.validate_input)

    def validate_input(self):
        """ Envoi du mot saisi au widget parent pour validation """
        if not self.isReadOnly():
            self.parent.validate_input(self.text())
            self.setText("")