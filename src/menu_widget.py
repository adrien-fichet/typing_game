#-*-coding:utf-8-*-

from PyQt5 import QtWidgets, QtCore
from src.help_label import HelpLabel
from src.life_widget import LifeWidget


class MenuWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(MenuWidget, self).__init__(parent)
        self.parent = parent
        self.game_started = False
        self.setFixedSize(190, 500)

        help_label = HelpLabel(self, 'Escape: Quit\nF5:     Start / Pause')

        self.start_or_pause_button = QtWidgets.QPushButton('Start')
        self.start_or_pause_button.setMinimumHeight(30)
        self.start_or_pause_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.start_or_pause_button.clicked.connect(self.start_or_pause_game)

        self.life_widget = LifeWidget(self, 30, self.parent.nb_of_lives)
        life_widget_layout = QtWidgets.QHBoxLayout()
        life_widget_layout.addStretch(1)
        life_widget_layout.addWidget(self.life_widget)
        life_widget_layout.addStretch(1)

        self.state_label = QtWidgets.QLabel('Not Running')
        self.state_label.setAlignment(QtCore.Qt.AlignHCenter)

        self.level_label = QtWidgets.QLabel('Level 1')
        self.level_label.setAlignment(QtCore.Qt.AlignHCenter)

        self.score_label = QtWidgets.QLabel('Score : 0')
        self.score_label.setAlignment(QtCore.Qt.AlignHCenter)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(help_label)
        vbox.addWidget(self.start_or_pause_button)
        vbox.addSpacing(50)
        vbox.addLayout(life_widget_layout)
        vbox.addWidget(self.state_label)
        vbox.addSpacing(20)
        vbox.addWidget(self.level_label)
        vbox.addWidget(self.score_label)
        vbox.addStretch(1)
        self.setLayout(vbox)

    def start_or_pause_game(self):
        self.parent.typing_board.start_or_pause_game()
