#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
import random

from PyQt4 import QtCore, QtGui
from src.life_widget import LifeWidget
from src.words import get_word_list

class HelpLabel(QtGui.QLabel):
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

class MenuWidget(QtGui.QWidget):
    """ Menu du jeu avec le score, la vie, etc. """

    def __init__(self, parent = None):
        super(MenuWidget, self).__init__(parent)
        self.parent = parent
        self.game_started = False
        self.init_UI()

    def init_UI(self):
        """ Définition de l'interface graphique """
        self.setFixedSize(190, 500)

        # Label d'aide expliquant les touches
        aide = "Escape: Quit\nF5:     Start / Pause"    
        help_label = HelpLabel(self, aide)

        # Bouton pour démarrer ou mettre en pause le jeu
        self.start_or_pause_button = QtGui.QPushButton("Start")
        self.start_or_pause_button.setMinimumHeight(30)
        self.start_or_pause_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.connect(self.start_or_pause_button, QtCore.SIGNAL("clicked()"),
                     self.start_or_pause_game)

        # Barre de vie
        self.life_bar = LifeWidget(self, 30, self.parent.nb_of_lives)
        life_bar_layout = QtGui.QHBoxLayout()
        life_bar_layout.addStretch(1)
        life_bar_layout.addWidget(self.life_bar)
        life_bar_layout.addStretch(1)

        # Label indiquant l'état du jeu
        self.state_label = QtGui.QLabel("Not Running")
        self.state_label.setAlignment(QtCore.Qt.AlignHCenter)

        # Label indiquant le niveau actuel
        self.level_label = QtGui.QLabel("Niveau 1")
        self.level_label.setAlignment(QtCore.Qt.AlignHCenter)

        # Label indiquant le score
        self.score_label = QtGui.QLabel("Score : 0")
        self.score_label.setAlignment(QtCore.Qt.AlignHCenter)

        # Layout
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(help_label)
        vbox.addWidget(self.start_or_pause_button)
        vbox.addSpacing(50)
        vbox.addLayout(life_bar_layout)
        vbox.addWidget(self.state_label)
        vbox.addSpacing(20)
        vbox.addWidget(self.level_label)
        vbox.addWidget(self.score_label)
        vbox.addStretch(1)
        self.setLayout(vbox)

    def start_or_pause_game(self):
        """ Envoi du signal de démarrage ou de mise en pause au parent"""
        self.parent.typing_board.start_or_pause_game()

class WordWidget(QtGui.QLabel):
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
    
class InputWidget(QtGui.QLineEdit):
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
        self.connect(self, QtCore.SIGNAL("returnPressed()"),
                     self.validate_input)

    def validate_input(self):
        """ Envoi du mot saisi au widget parent pour validation """
        if not self.isReadOnly():
            self.parent.validate_input(self.text())
            self.setText("")

class TypingBoard(QtGui.QWidget):
    """ Zone de défilement des mots """

    def __init__(self, parent = None):
        super(TypingBoard, self).__init__(parent)
        self.parent = parent
        
        self.word_widgets = self.retrieve_words()
        self.displayed_word_widgets = []
        self.displayed_word_widgets.append(
            self.word_widgets[random.randint(0, len(self.word_widgets) - 1)])
        
        self.timer = QtCore.QBasicTimer()
        self.game_started = False
        self.timer_interval = 200
        self.minimum_new_word_interval = 1500
        self.maximum_new_word_interval = 2500
        self.time = 0
        self.total_time = 0
        self.word_widget_interval = 50
        self.current_level = 1
        self.is_stopped = True
        self.score = 0

        self.init_UI()

    def init_UI(self):
        """ Définition de l'interface graphique """
        self.setFixedSize(500, 500)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 0))
        self.setPalette(p)

    def start_or_pause_game(self):
        """ Démarrage ou mise en pause du jeu """
        if self.game_started:
            self.timer.stop()
            self.parent.input_widget.setReadOnly(True)
            self.parent.menu_widget.start_or_pause_button.setText("Start")
            self.parent.menu_widget.state_label.setText("Paused")
        else:
            self.timer.start(self.timer_interval, self)
            self.parent.input_widget.setReadOnly(False)
            self.parent.menu_widget.start_or_pause_button.setText("Pause")
            self.parent.menu_widget.state_label.setText("Running")

            if self.is_stopped:
                # Remise à 1 du niveau
                self.current_level = 1
                self.parent.menu_widget.level_label.setText("Niveau {n}".format(
                    n = self.current_level))

                # Remise à 0 du score
                self.score = 0
                self.parent.menu_widget.score_label.setText("Score : {s}".format(
                    s = self.score))
                self.is_stopped = False

        self.game_started = not self.game_started

    def stop_game(self):
        """ Fin du jeu, replacement de tous les widgets """
        for i in self.displayed_word_widgets:
            i.move_to_initial_position()

        self.displayed_word_widgets = []
        self.timer.stop()
        self.parent.input_widget.setReadOnly(True)
        self.parent.input_widget.setText("")
        self.parent.menu_widget.start_or_pause_button.setText("Start")
        self.parent.menu_widget.state_label.setText("Finished")
        self.game_started = False
        self.is_stopped = True

        for i in range(self.parent.nb_of_lives):
            self.parent.menu_widget.life_bar.ajouter_un_carre()

    def retrieve_words(self):
        """ Récupération des mots du fichier "mots.txt" """
        # f = open("data/mots.txt", "r")
        # word_list = f.read().split("\n")
        word_list = get_word_list()
        word_list = [i.decode("utf-8") for i in word_list]
        random.shuffle(word_list)
        return [WordWidget(self, i) for i in word_list if i != ""]

    def timerEvent(self, event):
        """ Redéfinition pour actualiser le jeu en fonction du timer """
        # Mise à jour des timers
        self.time += self.timer_interval
        self.total_time += self.timer_interval

        # Augmentation de la vitesse (intervalle entre chaque
        # actualisation) toutes les 30 secondes
        if self.total_time >= 30E3:
            self.word_widget_interval += 5
            self.current_level += 1
            self.parent.menu_widget.level_label.setText(
                "Niveau {n}".format(n = self.current_level))
            self.total_time = 0
            self.minimum_new_word_interval -= 100
            self.maximum_new_word_interval -= 100

        # Ajout aléatoire d'un mot
        if self.time >= random.randint(self.minimum_new_word_interval,
                                       self.maximum_new_word_interval):
            self.time = 0
            r = random.randint(0, len(self.word_widgets) - 1)

            # Si le mot n'est pas déjà en train de descendre, on l'ajoute
            if not self.word_widgets[r] in self.displayed_word_widgets:
                # print("Ajout de {m}".format(m = self.word_widgets[r].texte))
                self.displayed_word_widgets.append(self.word_widgets[r])

        # Déplacement des mots vers le bas
        for i in self.displayed_word_widgets:
            i.move_down(self.word_widget_interval)

    def find_word_widget(self, w):
        """ Retourne le WordWidget dont le texte est w """
        for i in self.displayed_word_widgets:
            if QtCore.QString(i.texte) == w:
                return i

class TypingGame(QtGui.QWidget):
    """ Un jeu faisant appel à la rapidité de saisie au clavier """

    def __init__(self, parent = None):
        super(TypingGame, self).__init__(parent)

        self.nb_of_lives = 5
        self.init_UI()

    def init_UI(self):
        """ Définition de l'interface graphique """
        self.setWindowTitle("Typing Game")
        self.setWindowIcon(QtGui.QIcon("data/snake.png"))
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
        words = [QtCore.QString(i.texte)
                 for i in self.typing_board.displayed_word_widgets]

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
    app = QtGui.QApplication(sys.argv)
    window = TypingGame()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
