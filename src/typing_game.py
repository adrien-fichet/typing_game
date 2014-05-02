# -*- coding: utf-8 -*-

import sys
import ctypes

from PyQt5 import QtCore, QtWidgets, QtGui
from src.menu_widget import MenuWidget
from src.typing_board import TypingBoard
from src.input_widget import InputWidget


class TypingGame(QtWidgets.QWidget):
    """ Un jeu faisant appel à la rapidité de saisie au clavier """

    def __init__(self, parent = None):
        super(TypingGame, self).__init__(parent)

        self.nb_of_lives = 5
        self.init_UI()

    def init_UI(self):
        """ Définition de l'interface graphique """
        self.setWindowTitle("Typing Game")
        self.setWindowIcon(QtGui.QIcon("data/icon.png"))
        self.setFixedSize(700, 550)

        # Zone de défilement des mots
        self.typing_board = TypingBoard(self)
        self.typing_board.move(10, 10)

        # Zone de saisie de texte
        self.input_widget = InputWidget(self)
        self.input_widget.move(10, 520)

        # Menu
        self.menu_widget = MenuWidget(self)
        self.menu_widget.move(510, 10)

    def keyPressEvent(self, event):
        """ Redéfinition pour gérer les évènements clavier """
        # Fermeture du widget lors de l'appui sur Echap
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

        # Démarrage ou mise en pause du jeu lors de l'appui sur F5
        elif event.key() == QtCore.Qt.Key_F5:
            self.typing_board.start_or_pause_game()

    def validate_input(self, w):
        """ Validation du mot saisi par le joueur """
        words = [i.texte for i in self.typing_board.displayed_word_widgets]

        if w in words:
            word_widget = self.typing_board.find_word_widget(w)
            self.typing_board.displayed_word_widgets.remove(word_widget)
            word_widget.move_to_initial_position()
            self.typing_board.score += 1
            self.menu_widget.score_label.setText("Score : {s}".format(
                s = self.typing_board.score))

    def lose_one_life(self):
        """ On décrémente le nombre de vies s'il en reste au moins une """
        if self.nb_of_lives > 1:
            self.nb_of_lives -= 1
            self.menu_widget.life_bar.enlever_un_carre()
        else:
            self.menu_widget.life_bar.enlever_un_carre()
            self.show_end_game()

    def show_end_game(self):
        """ Affichage d'un message lorsque le joueur n'a plus de vies """
        self.nb_of_lives = 5
        self.typing_board.stop_game()


def main():
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('sniksnp.typing_game')
    app = QtWidgets.QApplication(sys.argv)
    window = TypingGame()
    window.show()
    sys.exit(app.exec_())
