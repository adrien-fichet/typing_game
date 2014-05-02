#-*-coding:utf-8-*-

from PyQt5 import QtWidgets, QtCore
from src.help_label import HelpLabel
from src.life_widget import LifeWidget


class MenuWidget(QtWidgets.QWidget):
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
        self.start_or_pause_button = QtWidgets.QPushButton("Start")
        self.start_or_pause_button.setMinimumHeight(30)
        self.start_or_pause_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.start_or_pause_button.clicked.connect(self.start_or_pause_game)

        # Barre de vie
        self.life_bar = LifeWidget(self, 30, self.parent.nb_of_lives)
        life_bar_layout = QtWidgets.QHBoxLayout()
        life_bar_layout.addStretch(1)
        life_bar_layout.addWidget(self.life_bar)
        life_bar_layout.addStretch(1)

        # Label indiquant l'état du jeu
        self.state_label = QtWidgets.QLabel("Not Running")
        self.state_label.setAlignment(QtCore.Qt.AlignHCenter)

        # Label indiquant le niveau actuel
        self.level_label = QtWidgets.QLabel("Niveau 1")
        self.level_label.setAlignment(QtCore.Qt.AlignHCenter)

        # Label indiquant le score
        self.score_label = QtWidgets.QLabel("Score : 0")
        self.score_label.setAlignment(QtCore.Qt.AlignHCenter)

        # Layout
        vbox = QtWidgets.QVBoxLayout()
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
