#-*-coding:utf-8-*-

from PyQt5 import QtWidgets, QtGui


class HelpLabel(QtWidgets.QLabel):
    """ Label contenant un texte d'aide """

    def __init__(self, parent = None, aide = None):
        super(HelpLabel, self).__init__(parent)
        self.parent = parent
        self.aide = aide
        self.init_UI()

    def init_UI(self):
        """ Définition de l'interface graphique """
        self.setFont(QtGui.QFont("Monospace", 9))
        self.setMinimumHeight(len(self.aide.split("\n")) * 15 + 10)

    def paintEvent(self, event):
        """ Redéfinition pour personnaliser l'apparence """
        qp = QtGui.QPainter()
        qp.begin(self)
        self.draw_widget(qp)
        qp.end()

    def draw_widget(self, qp):
        """ Dessinage du widget """
        qp.setPen(QtGui.QColor(0, 0, 0))
        qp.setBrush(QtGui.QColor(200, 200, 200))
        qp.drawRect(0, 0, self.width() - 1, self.height() - 1)

        for i in range(len(self.aide.split("\n"))):
            qp.drawText(10, 17 + 15 * i, self.aide.split("\n")[i])