#-*-coding:utf-8-*-

import random

from PyQt5 import QtWidgets, QtCore, QtGui
from src.word_widget import WordWidget


class TypingBoard(QtWidgets.QWidget):
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
        f = open("data/words.txt", "r")
        word_list = f.read().split("\n")
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
            if i.texte == w:
                return i
