#-*-coding:utf-8-*-

import random

from PyQt5 import QtWidgets, QtGui


class WordWidget(QtWidgets.QLabel):
    """ Un widget représentant un mot à taper """

    def __init__(self, parent = None, texte = None):
        super(WordWidget, self).__init__(parent)
        self.parent = parent
        self.texte = texte
        self.nb_of_letters = float(len(self.texte))
        self.init_UI()

    def init_UI(self):
        """ Définition de l'interface graphique """
        self.setStyleSheet(
            """
            QLabel {
            color : lime
            }
            """)

        if self.texte:
            self.setText(self.texte)

        self.setFont(QtGui.QFont("Monospace", 14))
        self.move_to_initial_position()

    def move_down(self, interval):
        """ Déplacement du texte vers le bas """
        if self.y() >= self.parent.height():
            self.parent.displayed_word_widgets.remove(self)
            self.move_to_initial_position()

            # Décrémentation du nombre de vies
            self.parent.parent.lose_one_life()

        else:
            # On déplace le mot plus ou moins vite en fonction du nombre
            # de lettres qui le composent
            self.move(self.x(), self.y() + (interval / self.nb_of_letters * 0.5))

    def move_to_initial_position(self):
        """ Déplacement du widget vers sa position d'origine """
        self.move(random.randint(0, 400), -40)