#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys

from PyQt4 import QtCore, QtGui

class LifeWidget(QtGui.QWidget):
    """ Un widget représentant une barre de vie """

    def __init__(self, parent = None, cote = 50, nb_carres_total = 5):
        super(LifeWidget, self).__init__(parent)

        # Côté d'un carré de vie
        self.cote = cote

        # Nombre de carrés de vie
        self.nb_carres_total = nb_carres_total
        self.nb_carres_restants = self.nb_carres_total

        # Initialisation de l'interface graphique
        self.init_UI()
        
    def init_UI(self):
        """ Définition de l'interface graphique """
        self.setFixedSize(self.cote, self.nb_carres_total * self.cote)

    def paintEvent(self, event):
        """ Redéfinition pour personnaliser l'apparence """
        qp = QtGui.QPainter()
        qp.begin(self)
        self.draw_widget(qp)
        qp.end()

    def draw_widget(self, qp):
        """ Dessinage du widget """
        qp.setPen(QtCore.Qt.NoPen)

        for i in range(0, self.nb_carres_total * self.cote, self.cote):

            # Changement de la couleur en fonction du nombre de carrés restants
            if (float(i) / self.cote) < self.nb_carres_restants:
                qp.setBrush(QtGui.QColor(0, 255, 0))
            else:
                qp.setBrush(QtGui.QColor(255, 0, 0))

            # On dessine les carrés en commencant par le plus en bas
            qp.drawRect(0, self.nb_carres_total * self.cote - (i + self.cote),
                        self.cote - 1, self.cote - 1)

    def keyPressEvent(self, event):
        """ Redéfinition pour gérer les touches """
        # On ajoute ou retire un carré lors de l'appui sur les flèches
        # haut / bas
        if event.key() == QtCore.Qt.Key_Up:
            self.ajouter_un_carre()
        elif event.key() == QtCore.Qt.Key_Down:
            self.enlever_un_carre()

        # On ferme le widget lors de l'appui sur Echap
        elif event.key() == QtCore.Qt.Key_Escape:
            self.close()

    def enlever_un_carre(self):
        """ Perte d'un carré de vie """
        if self.nb_carres_restants > 0:
            self.nb_carres_restants = self.nb_carres_restants - 1
            self.repaint()

        # print(self.nb_carres_restants)

    def ajouter_un_carre(self):
        """ Ajout d'un carré de vie """
        if self.nb_carres_restants < self.nb_carres_total:
            self.nb_carres_restants = self.nb_carres_restants + 1
            self.repaint()

        # print(self.nb_carres_restants)

def main():
    app = QtGui.QApplication(sys.argv)
    window = LifeWidget()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
