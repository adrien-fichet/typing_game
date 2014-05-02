#-*-coding:utf-8-*-

import random

from PyQt5 import QtWidgets, QtCore, QtGui
from src.word_widget import WordWidget


class TypingBoard(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(TypingBoard, self).__init__(parent)
        self.parent = parent

        self.word_widgets = self.get_words()
        self.displayed_word_widgets = []
        self.displayed_word_widgets.append(self.word_widgets[random.randint(0, len(self.word_widgets) - 1)])

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

        self.setFixedSize(500, 500)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 0))
        self.setPalette(p)

    def start_or_pause_game(self):
        if self.game_started:
            self.timer.stop()
            self.parent.input_widget.setReadOnly(True)
            self.parent.menu_widget.start_or_pause_button.setText('Start')
            self.parent.menu_widget.state_label.setText('Paused')
        else:
            self.timer.start(self.timer_interval, self)
            self.parent.input_widget.setReadOnly(False)
            self.parent.menu_widget.start_or_pause_button.setText('Pause')
            self.parent.menu_widget.state_label.setText('Running')

            if self.is_stopped:
                self.current_level = 1
                self.parent.menu_widget.level_label.setText('Level {}'.format(self.current_level))
                self.score = 0
                self.parent.menu_widget.score_label.setText('Score : {}'.format(self.score))
                self.is_stopped = False

        self.game_started = not self.game_started

    def stop_game(self):
        for i in self.displayed_word_widgets:
            i.move_to_initial_position()

        self.displayed_word_widgets = []
        self.timer.stop()
        self.parent.input_widget.setReadOnly(True)
        self.parent.input_widget.setText('')
        self.parent.menu_widget.start_or_pause_button.setText('Start')
        self.parent.menu_widget.state_label.setText('Finished')
        self.game_started = False
        self.is_stopped = True
        self.parent.menu_widget.life_widget.reset()

    def get_words(self):
        f = open('data/words.txt', 'r')
        word_list = f.read().split('\n')
        random.shuffle(word_list)
        return [WordWidget(self, i) for i in word_list if i != '']

    def timerEvent(self, event):
        self.time += self.timer_interval
        self.total_time += self.timer_interval

        if self.total_time >= 30E3:
            self.word_widget_interval += 5
            self.current_level += 1
            self.parent.menu_widget.level_label.setText('Level {}'.format(self.current_level))
            self.total_time = 0
            self.minimum_new_word_interval -= 100
            self.maximum_new_word_interval -= 100

        if self.time >= random.randint(self.minimum_new_word_interval, self.maximum_new_word_interval):
            self.time = 0
            r = random.randint(0, len(self.word_widgets) - 1)

            if not self.word_widgets[r] in self.displayed_word_widgets:
                self.displayed_word_widgets.append(self.word_widgets[r])

        for i in self.displayed_word_widgets:
            i.move_down(self.word_widget_interval)

    def find_word_widget(self, w):
        for i in self.displayed_word_widgets:
            if i.text == w:
                return i
