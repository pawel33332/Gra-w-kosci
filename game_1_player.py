import math
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import  QFont
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from PyQt5.QtChart import QChart, QLineSeries, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QGridLayout
from PyQt5.uic import loadUi
import detailed_statistics
import menu
import settings
import sounds
import dice
import scorecard
import json
import numpy as np


class Game1Player(QMainWindow):
    def __init__(self,qd):
        super(Game1Player, self).__init__()
        loadUi("menu.ui", self)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QGridLayout(central_widget)
        self.qd = qd
        self.set_variables()
        self.wid = self.qd
    def set_variables(self):
        background_label = QLabel(self)
        pixmap = QPixmap("graphics/background_game.png")
        scaled_pixmap = pixmap.scaled(1366, 768)
        background_label.setPixmap(scaled_pixmap)
        self.layout.addWidget(background_label, 0, 0, 21, 11)
        background_label.setScaledContents(True)

        self.card = ["Karta punktowa", "Jedynki", "Dwójki", "Trójki", "Czwórki", "Piątki", "Szóstki", "Bonus",
                     "Suma górna", "Trzy jednakowe", "Cztery jednakowe", "Full (3x,2y)", "Mały strit (1-4,2-5,3-6)",
                     "Duży strit (1-5,2-6)", "Generał", "Szansa", "Suma", "Łączna suma"]
        a = 1
        self.player_nr = QLabel(self)
        self.player_nr.setText("Gracz 1")
        self.player_nr.setStyleSheet("color:white;font-weight:bold")
        self.player_nr.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.player_nr, a, 2)
        for i in self.card:
            label = self.createWidgets(str(i))
            self.layout.addWidget(label, a, 1)
            a += 1

        self.player=1 #kolej gracza 1 czy gracza 2
        self.d = settings.Settings(self)
        self.difficulty = self.d.return_selected_difficulty()
        self.selected_category="ones"
        self.selected_dice_computer = [0, 0, 0, 0, 0]
        self.score_player_one=[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0] # wartosci -1 gdyz sprawdzam
        # czy kategoria została już wybrana
        self.score_player_two = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0]
        self.tab_probabilities = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.selected_yahtzee_1=False
        self.selected_yahtzee_2 = False
        self.score_player_one_history=[0]
        self.score_player_two_history = [0]
        self.number_roll=0
        self.next_t = 1 # nastepna kolejka
        self.selected=False
        self.is_sel = [0,0,0,0,0]
        self.t = settings.Settings(self)
        self.time = self.t.return_selected_time()
        self.player_1_time = self.time
        self.player_2_time = self.time
        self.timer1 = QTimer(self)
        self.timer1.timeout.connect(self.update_timer)
        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.update_timer2)

        self.pause = QLabel(self)
        location_pause = QImage("graphics/pause.png")
        scaled_pau = location_pause.scaled(location_pause.width() // 1, location_pause.height() // 1)
        scaled_pause = QPixmap.fromImage(scaled_pau)
        self.pause.setPixmap(scaled_pause)
        self.layout.addWidget(self.pause, 1, 10, 1, 1)
        self.pause.mousePressEvent = self.pause_event

        self.play = QLabel(self)
        location_play = QImage("graphics/play.png")
        scaled_pl = location_play.scaled(location_play.width() // 1,
                                         location_play.height() // 1)
        scaled_play = QPixmap.fromImage(scaled_pl)
        self.play.setPixmap(scaled_play)
        self.layout.addWidget(self.play, 1, 10, 1, 1)
        self.play.hide()
        self.play.mousePressEvent = self.play_event

        self.result = QLabel(self)
        self.result.setAlignment(Qt.AlignCenter)
        self.result.setText("0 : 0")
        self.result.setStyleSheet("font-size:60px;color: rgb(255,255,255);")
        self.layout.addWidget(self.result, 1, 5, 1, 3)
        self.image_dice_1 = QLabel(self)
        self.image_dice_2 = QLabel(self)
        self.image_dice_3 = QLabel(self)
        self.image_dice_4 = QLabel(self)
        self.image_dice_5 = QLabel(self)

        self.category_ones = QLabel(self)
        self.category_twos = QLabel(self)
        self.category_threes = QLabel(self)
        self.category_fours = QLabel(self)
        self.category_fives = QLabel(self)
        self.category_sixes = QLabel(self)
        self.category_x3 = QLabel(self)
        self.category_x4 = QLabel(self)
        self.category_full = QLabel(self)
        self.category_small_s = QLabel(self)
        self.category_large_s = QLabel(self)
        self.category_yahtzee = QLabel(self)
        self.category_chance = QLabel(self)

        self.ones = 0  # zmienne przechowujace punkty dla danych kategorii
        self.twos = 0
        self.threes = 0
        self.fours = 0
        self.fives = 0
        self.sixes = 0
        self.bonus = 0
        self.sumag = 0  # suma gornej tabeli
        self.x3 = 0
        self.x4 = 0
        self.full = 0
        self.sstrit = 0
        self.lstrit = 0
        self.yahtzee = 0
        self.chance = 0
        self.sumad = 0  # suma dolnej tabeli
        self.totalsum = 0
        self.group_category = [self.ones, self.twos, self.threes, self.fours, self.fives, self.sixes, self.bonus,
                               self.sumag, self.x3, self.x4, self.full, self.sstrit, self.lstrit, self.yahtzee,
                               self.chance,self.sumad, self.totalsum]

        self.ones_ = QLabel("0", self)
        self.twos_ = QLabel("0", self)
        self.threes_ = QLabel("0", self)
        self.fours_ = QLabel("0", self)
        self.fives_ = QLabel("0", self)
        self.sixes_ = QLabel("0", self)
        self.bonus_ = QLabel("0", self)
        self.sumag_ = QLabel("0", self)
        self.x3_ = QLabel("0", self)
        self.x4_ = QLabel("0", self)
        self.full_ = QLabel("0", self)
        self.sstrit_ = QLabel("0", self)
        self.lstrit_ = QLabel("0", self)
        self.yahtzee_ = QLabel("0", self)
        self.chance_ = QLabel("0", self)
        self.sumad_ = QLabel("0", self)
        self.totalsum_ = QLabel("0", self)
        self.group_category_text = [self.ones_, self.twos_, self.threes_, self.fours_, self.fives_, self.sixes_,
                                    self.bonus_, self.sumag_, self.x3_, self.x4_, self.full_, self.sstrit_,
                                    self.lstrit_, self.yahtzee_,self.chance_, self.sumad_, self.totalsum_]
        self.image_robot = QLabel(self)
        location_image_robot = QImage("graphics/robot.png")
        scaled_robot = location_image_robot.scaled(location_image_robot.width() // 3, location_image_robot.height() // 3)
        scaled_pixmap8 = QPixmap.fromImage(scaled_robot)


        self.image_robot.setPixmap(scaled_pixmap8)
        self.image_robot.setAlignment(Qt.AlignCenter)
        #self.image_robot.setGeometry(1575, 375, scaled_pixmap8.width(), scaled_pixmap8.height())
        self.layout.addWidget(self.image_robot, 8, 9, 6, 2)
        self.image_robot.hide()
        self.robot_text = QLabel(self)
        self.layout.addWidget(self.robot_text, 6, 9, 3, 2)
        self.robot_text.setAlignment(Qt.AlignCenter)
        self.robot_text.setStyleSheet("font-size:36px;color: rgb(255,255,255);")
        self.robot_text.hide()

        self.button = QLabel(self)
        location_button = QImage("graphics/button_draw.png")
        scaled_button = location_button.scaled(location_button.width() // 1, location_button.height() // 1)
        scaled_pixmap7 = QPixmap.fromImage(scaled_button)
        self.button.setPixmap(scaled_pixmap7)
        self.button.setPixmap(scaled_pixmap7)
        self.button.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.button, 16, 6, 3, 1)

        self.button.mousePressEvent=self.roll_dice
        a = dice.Dice()
        self.dice = a.roll(self.is_sel, [1, 1, 1, 1, 1])
        self.set_dice_element()
        self.category()
        self.choose_category()

        self.label_time = QLabel(self)
        self.label_time.setGeometry(270, 70, 250, 70)
        self.label_time.setAlignment(Qt.AlignCenter)
        self.label_time.setText(str(self.time) + " s")
        self.label_time.setStyleSheet("font-size:36px;color: rgb(255,255,255);")
        self.label_time.setMinimumWidth(130)
        self.layout.addWidget(self.label_time, 1, 4, 1, 1)

        self.label_time2 = QLabel(self)
        self.label_time2.setGeometry(442, 70, 250, 70)
        self.label_time2.setAlignment(Qt.AlignCenter)
        self.label_time2.setText(str(self.time) + " s")
        self.label_time2.setStyleSheet("font-size:36px;color: rgb(255,255,255);")
        self.label_time2.setMinimumWidth(130)
        self.layout.addWidget(self.label_time2, 1, 8, 1, 1)

        self.timer1.start(1000)
        # Timer aktualizuje co 1 sekundę
        self.background_label = QLabel(self)
        self.image_play_again = QLabel(self)
        self.image2 = QImage("graphics/dice_1.png")
        self.scaled_image2 = self.image2.scaled(self.image2.width() // 10, self.image2.height() // 10)
        self.scaled_pixmap2 = QPixmap.fromImage(self.scaled_image2)

        self.text_play_again = QLabel(self)
        self.text_play_again.setText("Zagraj ponownie")
        self.text_play_again.setStyleSheet(
            "QLabel { color: rgb(255, 255, 255); }"
            "QLabel:hover { color: rgb(255, 0, 0); }"
        )
        self.text_play_again.hide()
        self.layout.addWidget(self.text_play_again, 19, 1, 1, 2)


        self.wykres_slupkowy = QLabel(self)
        self.wykres_liniowy = QLabel(self)
        self.sounds_ = sounds.Sounds()

        self.image_label2 = QLabel(self)
        self.image2 = QImage("graphics/button_undo.png")
        self.scaled_image2 = self.image2.scaled(self.image2.width() // 8, self.image2.height() // 8)
        self.scaled_pixmap2 = QPixmap.fromImage(self.scaled_image2)
        self.image_label2.setPixmap(self.scaled_pixmap2)
        self.layout.addWidget(self.image_label2, 1, 0, 1, 1)
        self.image_label2.mousePressEvent = self.undo

    def createWidgets(self, text):
        text_label = QLabel(text)
        text_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #fff;")
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setCursor(Qt.PointingHandCursor)

        return text_label
    def update_background(self):
        pixmap = QPixmap("background_game.png")
        scaled_pixmap = pixmap.scaled(QSize(self.width(), self.height()))
        self.background_label.setPixmap(scaled_pixmap)

    def category(self):
        if self.player==1:
            self.player_nr.setText("Gracz 1")
        elif self.player==2:
            self.player_nr.setText("CPU")
        x1=2
        self.ones_.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.ones_, 2, x1, 1, 1)

        self.twos_.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.twos_, 3, x1, 1, 1)

        self.threes_.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.threes_, 4, x1, 1, 1)

        self.fours_.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.fours_, 5, x1, 1, 1)

        self.fives_.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.fives_, 6, x1, 1, 1)

        self.sixes_.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.sixes_, 7, x1, 1, 1)

        self.bonus_.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.bonus_, 8, x1, 1, 1)

        self.sumag_.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.sumag_, 9, x1, 1, 1)

        self.x3_.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.x3_, 10, x1, 1, 1)

        self.x4_.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.x4_, 11, x1, 1, 1)

        self.full_.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.full_, 12, x1, 1, 1)

        self.sstrit_.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.sstrit_, 13, x1, 1, 1)

        self.lstrit_.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.lstrit_, 14, x1, 1, 1)

        self.yahtzee_.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.yahtzee_, 15, x1, 1, 1)

        self.chance_.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.chance_, 16, x1, 1, 1)

        self.sumad_.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.sumad_, 17, x1, 1, 1)

        self.totalsum_.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.totalsum_, 18, x1, 1, 1)


    def set_dice_element(self):
        #print(self.dice)
        location_dice_1 = QImage("graphics/dice_"+str(self.dice[0])+".png")
        location_dice_2 = QImage("graphics/dice_" + str(self.dice[1]) + ".png")
        location_dice_3 = QImage("graphics/dice_" + str(self.dice[2]) + ".png")
        location_dice_4 = QImage("graphics/dice_" + str(self.dice[3]) + ".png")
        location_dice_5 = QImage("graphics/dice_" + str(self.dice[4]) + ".png")

        scaled_image_dice_1 = location_dice_1.scaled(location_dice_1.width() // 8, location_dice_1.height() // 8)
        scaled_pixmap2 = QPixmap.fromImage(scaled_image_dice_1)
        self.image_dice_1.setPixmap(scaled_pixmap2)
        self.image_dice_1.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_dice_1, 4, 4, 3, 1)

        self.image_dice_1.mousePressEvent = lambda event: self.stop_dice(self.image_dice_1, 1)

        scaled_image_dice_2 = location_dice_2.scaled(location_dice_2.width() // 8, location_dice_2.height() // 8)
        scaled_pixmap3 = QPixmap.fromImage(scaled_image_dice_2)
        self.image_dice_2.setPixmap(scaled_pixmap3)
        self.image_dice_2.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_dice_2, 14, 4, 3, 1)
        self.image_dice_2.mousePressEvent = lambda event: self.stop_dice(self.image_dice_2, 2)

        scaled_image_dice_3 = location_dice_3.scaled(location_dice_3.width() // 8, location_dice_3.height() // 8)
        scaled_pixmap4 = QPixmap.fromImage(scaled_image_dice_3)
        self.image_dice_3.setPixmap(scaled_pixmap4)
        self.image_dice_3.setAlignment(Qt.AlignCenter)
        self.image_dice_3.setMinimumWidth(130)
        self.layout.addWidget(self.image_dice_3, 9, 6, 3, 1)
        self.image_dice_3.mousePressEvent = lambda event: self.stop_dice(self.image_dice_3, 3)

        scaled_image_dice_4 = location_dice_4.scaled(location_dice_4.width() // 8, location_dice_4.height() // 8)
        scaled_pixmap5 = QPixmap.fromImage(scaled_image_dice_4)
        self.image_dice_4.setPixmap(scaled_pixmap5)
        self.image_dice_4.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_dice_4, 4, 8, 3, 1)
        self.image_dice_4.mousePressEvent = lambda event: self.stop_dice(self.image_dice_4, 4)

        scaled_image_dice_5 = location_dice_5.scaled(location_dice_5.width() // 8, location_dice_5.height() // 8)
        scaled_pixmap6 = QPixmap.fromImage(scaled_image_dice_5)
        self.image_dice_5.setPixmap(scaled_pixmap6)
        self.image_dice_5.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_dice_5, 14, 8, 3, 1)
        self.image_dice_5.mousePressEvent = lambda event: self.stop_dice(self.image_dice_5, 5)

    def stop_dice(self, image, x):
        if self.is_sel[x - 1] == 1:
            self.is_sel[x - 1] = 0
            image.setStyleSheet("border: none;")
        else:
            self.is_sel[x - 1] = 1
            image.setStyleSheet("border: 4px solid red;")

    def roll_dice(self, event):
        self.number_roll += 1
        a = dice.Dice()
        self.dice = a.roll(self.is_sel, self.dice)
        self.sounds_.dice_rolling()
        self.set_dice_element()
        self.choose_category()
        if self.number_roll < 2:
            self.button.show()
        else:
            self.button.hide()
    def choose_category(self):
        a=scorecard.Scorecard(self.dice)
        self.ones = a.one
        self.twos = a.two
        self.threes = a.three
        self.fours = a.four
        self.fives = a.five
        self.sixes = a.six
        self.x3 = a.x3
        self.x4 = a.x4
        self.full = a.full
        self.sstrit = a.small_strit
        self.lstrit = a.large_strit
        self.yahtzee = a.yahtzee
        self.chance = a.chance

        self.ones_.setStyleSheet("QLabel:hover { color: rgb(255,255,255); } QLabel { background-color: green; }")
        self.twos_.setStyleSheet("QLabel:hover { color: rgb(255,255,255); } QLabel { background-color: green; }")
        self.threes_.setStyleSheet("QLabel:hover { color: rgb(255,255,255); } QLabel { background-color: green; }")
        self.fours_.setStyleSheet("QLabel:hover { color: rgb(255,255,255); } QLabel { background-color: green; }")
        self.fives_.setStyleSheet("QLabel:hover { color: rgb(255,255,255); } QLabel { background-color: green; }")
        self.sixes_.setStyleSheet("QLabel:hover { color: rgb(255,255,255); } QLabel { background-color: green; }")
        self.x3_.setStyleSheet("QLabel:hover { color: rgb(255,255,255); } QLabel { background-color: green; }")
        self.x4_.setStyleSheet("QLabel:hover { color: rgb(255,255,255); } QLabel { background-color: green; }")
        self.full_.setStyleSheet("QLabel:hover { color: rgb(255,255,255); } QLabel { background-color: green; }")
        self.sstrit_.setStyleSheet("QLabel:hover { color: rgb(255,255,255); } QLabel { background-color: green; }")
        self.lstrit_.setStyleSheet("QLabel:hover { color: rgb(255,255,255); } QLabel { background-color: green; }")
        self.yahtzee_.setStyleSheet("QLabel:hover { color: rgb(255,255,255); } QLabel { background-color: green; }")
        self.chance_.setStyleSheet("QLabel:hover { color: rgb(255,255,255); } QLabel { background-color: green; }")

        a = self.player
        if a == 1:
            a = self.score_player_one
        elif a == 2:
            a = self.score_player_two
        if self.yahtzee == 50:
            if a[13] >= 50:
                self.full = 25
                self.sstrit = 30
                self.lstrit = 40

        self.ones_.setText(str(self.ones))
        self.ones_.mousePressEvent = self._ones

        self.twos_.setText(str(self.twos))
        self.twos_.mousePressEvent = self._twos

        self.threes_.setText(str(self.threes))
        self.threes_.mousePressEvent = self._threes

        self.fours_.setText(str(self.fours))
        self.fours_.mousePressEvent = self._fours

        self.fives_.setText(str(self.fives))
        self.fives_.mousePressEvent = self._fives

        self.sixes_.setText(str(self.sixes))
        self.sixes_.mousePressEvent = self._sixes

        self.bonus_.setText("0")

        self.x3_.setText(str(self.x3))
        self.x3_.mousePressEvent = self._x3

        self.x4_.setText(str(self.x4))
        self.x4_.mousePressEvent = self._x4

        self.full_.setText(str(self.full))
        self.full_.mousePressEvent = self._full

        self.sstrit_.setText(str(self.sstrit))
        self.sstrit_.mousePressEvent = self._sstrit

        self.lstrit_.setText(str(self.lstrit))
        self.lstrit_.mousePressEvent = self._lstrit

        self.yahtzee_.setText(str(self.yahtzee))
        self.yahtzee_.mousePressEvent = self._yahtzee

        self.chance_.setText(str(self.chance))
        self.chance_.mousePressEvent = self._chance


        for i in range(0,17):
            if self.player==1:
                punkty=self.score_player_one
            elif self.player==2:
                punkty = self.score_player_two
            if punkty[i]!=-1:
                self.group_category_text[i].setText(str(punkty[i]))
                self.group_category_text[i].setStyleSheet("color: white;background-color:red;")
        self.bonus_.setStyleSheet("QLabel { color: rgb(255,255,255); } QLabel { background-color: black; }")
        self.sumag_.setStyleSheet("QLabel { color: rgb(255,255,255); } QLabel { background-color: black; }")
        self.sumad_.setStyleSheet("QLabel { color: rgb(255,255,255); } QLabel { background-color: black; }")
        self.totalsum_.setStyleSheet("QLabel { color: rgb(255,255,255); } QLabel { background-color: black; }")


    def next_turn(self):
        self.number_roll = 0
        self.is_sel = [0, 0, 0, 0, 0]
        self.button.show()
        self.image_dice_1.setStyleSheet("border: none;")
        self.image_dice_2.setStyleSheet("border: none;")
        self.image_dice_3.setStyleSheet("border: none;")
        self.image_dice_4.setStyleSheet("border: none;")
        self.image_dice_5.setStyleSheet("border: none;")
        a = dice.Dice()
        self.dice = a.roll(self.is_sel, [1, 1, 1, 1, 1])
        self.set_dice_element()
        if self.player==1:
            self.timer1.stop()
            self.player=2
            self.timer2.start(1000)
            for item in self.group_category_text:
                item.setEnabled(False)
        else:
            for item in self.group_category_text:
                item.setEnabled(True)
            self.image_robot.hide()
            self.robot_text.hide()
            self.timer2.stop()
            self.player=1
            self.timer1.start(1000)
        self.choose_category()
        self.category()
        if self.player==2:
            self.image_robot.show()
            self.robot_text.show()
            self.player_CPU(self.difficulty)
        self.next_t += 1
        if self.next_t == 27:
            self.button.hide()
            self.final_score()
            return

    def punctation(self):
        self.sounds_.click_button()
        if self.player==1:
            if self.yahtzee==50 and self.selected_yahtzee_1==True:
                if self.score_player_one[13]>=50:
                    self.score_player_one[13]+=100
            if sum(value for value in self.score_player_one[:6] if value != -1) > 62:
                self.score_player_one[6] = 35  # bonus za zdobycie przynajmniej 63 punktów
            sum_upper = sum(value for value in self.score_player_one[:7] if value != -1)
            sum_lower = sum(value for value in self.score_player_one[8:15] if value != -1)
            self.score_player_one[7] = sum_upper
            self.score_player_one[15] = sum_lower
            sum_total=self.score_player_one[7]+self.score_player_one[15]
            self.score_player_one[16]=sum_total
            self.score_player_one_history.append(sum_total)
        if self.player==2:
            if self.yahtzee == 50 and self.selected_yahtzee_2==True:
                if self.score_player_two[13] >= 50:
                    self.score_player_two[13] += 100
            if sum(value for value in self.score_player_two[:6] if value != -1) > 62:
                self.score_player_two[6] = 35
            sum_upper= sum(value for value in self.score_player_two[:7] if value != -1)
            sum_lower = sum(value for value in self.score_player_two[8:15] if value != -1)
            self.score_player_two[7] = sum_upper
            self.score_player_two[15] = sum_lower
            sum_total = self.score_player_two[7] + self.score_player_two[15]
            self.score_player_two[16] = sum_total
            self.score_player_two_history.append(sum_total)
        self.result.setText(str(self.score_player_one[16])+" : "+str(self.score_player_two[16]))

    def _ones(self,event):
        if self.player==1:
            if self.score_player_one[0]==-1:
                self.selected_category="ones"
                self.score_player_one[0]=self.ones
                self.punctation()
                self.next_turn()
        elif self.player==2:
            if self.score_player_two[0]==-1:
                self.score_player_two[0]=self.ones
                self.punctation()
                self.next_turn()
    def _twos(self,event):
        if self.player == 1:
            if self.score_player_one[1] == -1:
                self.selected_category = "twos"
                self.score_player_one[1] = self.twos
                self.punctation()
                self.next_turn()
        elif self.player == 2:
            if self.score_player_two[1] == -1:
                self.score_player_two[1] = self.twos
                self.punctation()
                self.next_turn()

    def _threes(self, event):
        if self.player == 1:
            if self.score_player_one[2] == -1:
                self.selected_category = "threes"
                self.score_player_one[2] = self.threes
                self.punctation()
                self.next_turn()
        elif self.player == 2:
            if self.score_player_two[2] == -1:
                self.score_player_two[2] = self.threes
                self.punctation()
                self.next_turn()

    def _fours(self, event):
        if self.player == 1:
            if self.score_player_one[3] == -1:
                self.selected_category = "fours"
                self.score_player_one[3] = self.fours
                self.punctation()
                self.next_turn()
        elif self.player == 2:
            if self.score_player_two[3] == -1:
                self.score_player_two[3] = self.fours
                self.punctation()
                self.next_turn()

    def _fives(self, event):
        if self.player == 1:
            if self.score_player_one[4] == -1:
                self.selected_category = "fives"
                self.score_player_one[4] = self.fives
                self.punctation()
                self.next_turn()
        elif self.player == 2:
            if self.score_player_two[4] == -1:
                self.score_player_two[4] = self.fives
                self.punctation()
                self.next_turn()


    def _sixes(self, event):
        if self.player == 1:
            if self.score_player_one[5] == -1:
                self.selected_category = "sixes"
                self.score_player_one[5] = self.sixes
                self.punctation()
                self.next_turn()
        elif self.player == 2:
            if self.score_player_two[5] == -1:
                self.score_player_two[5] = self.sixes
                self.punctation()
                self.next_turn()

    def _x3(self, event):
        if self.player == 1:
            if self.score_player_one[8] == -1:
                self.selected_category = "x3"
                self.score_player_one[8] = self.x3
                self.punctation()
                self.next_turn()
        elif self.player == 2:
            if self.score_player_two[8] == -1:
                self.score_player_two[8] = self.x3
                self.punctation()
                self.next_turn()

    def _x4(self, event):
        if self.player == 1:
            if self.score_player_one[9] == -1:
                self.selected_category = "x4"
                self.score_player_one[9] = self.x4
                self.punctation()
                self.next_turn()
        elif self.player == 2:
            if self.score_player_two[9] == -1:
                self.score_player_two[9] = self.x4
                self.punctation()
                self.next_turn()

    def _full(self, event):
        if self.player == 1:
            if self.score_player_one[10] == -1:
                self.selected_category = "full"
                self.score_player_one[10] = self.full
                self.punctation()
                self.next_turn()
        elif self.player == 2:
            if self.score_player_two[10] == -1:
                self.score_player_two[10] = self.full
                self.punctation()
                self.next_turn()


    def _sstrit(self, event):
        if self.player == 1:
            if self.score_player_one[11] == -1:
                self.selected_category = "sstrit"
                self.score_player_one[11] = self.sstrit
                self.punctation()
                self.next_turn()
        elif self.player == 2:
            if self.score_player_two[11] == -1:
                self.score_player_two[11] = self.sstrit
                self.punctation()
                self.next_turn()

    def _lstrit(self, event):
        if self.player == 1:
            if self.score_player_one[12] == -1:
                self.selected_category = "lstrit"
                self.score_player_one[12] = self.lstrit
                self.punctation()
                self.next_turn()
        elif self.player == 2:
            if self.score_player_two[12] == -1:
                self.score_player_two[12] = self.lstrit
                self.punctation()
                self.next_turn()

    def _yahtzee(self, event):
        if self.player == 1:
            if self.score_player_one[13] == -1:
                self.selected_category = "yahtzee"
                self.score_player_one[13] = self.yahtzee
                self.punctation()
                self.selected_yahtzee_1=True
                self.next_turn()
        elif self.player == 2:
            if self.score_player_two[13] == -1:
                self.score_player_two[13] = self.yahtzee
                self.punctation()
                self.selected_yahtzee_2 = True
                self.next_turn()

    def _chance(self, event):
        if self.player == 1:
            if self.score_player_one[14] == -1:
                self.selected_category = "szansa"
                self.score_player_one[14] = self.chance
                self.punctation()
                self.next_turn()
        elif self.player == 2:
            if self.score_player_two[14] == -1:
                self.score_player_two[14] = self.chance
                self.punctation()
                self.next_turn()

    def final_score(self):
        self.timer1.stop()
        self.timer2.stop()
        self.play.hide()
        self.pause.hide()
        self.sounds_.winner()

        if self.score_player_one[16]>self.score_player_two[16]:
            a="Zwycięstwo gracza 1 "+str(self.score_player_one[16])+" : "+str(self.score_player_two[16])
        elif self.score_player_one[16]<self.score_player_two[16]:
            a="Zwycięstwo gracza CPU "+str(self.score_player_one[16])+" : "+str(self.score_player_two[16])
        else:
            a="Zakonczono remisem "+str(self.score_player_one[16])+" : "+str(self.score_player_two[16])
        if self.player_1_time < 0:
            a="Gracz 1 przekroczył czas"
        if self.player_2_time < 0:
            a = "Gracz CPU przekroczył czas"
        self.save_statistics()

        self.result.setAlignment(Qt.AlignCenter)
        self.result.setText(a)
        self.result.setStyleSheet("font-size:60px;color: rgb(255,255,255);background-color:red;")
        self.layout.addWidget(self.result, 0, 0, 1, 11)

        chart = QChart()
        series = QBarSeries()

        set1 = QBarSet("Gracz 1")
        set2 = QBarSet("Gracz CPU")
        data1=[]
        data2=[]
        data1 = self.score_player_one[0:6]
        data1.extend(self.score_player_one[8:15])
        data2 = self.score_player_two[0:6]
        data2.extend(self.score_player_two[8:15])
        print(data1)
        print(data2)

        set1.append(data1)
        set2.append(data2)

        series.append(set1)
        series.append(set2)
        chart.setTitle("Wykres zdobytych punktów")
        chart.addSeries(series)
        chart.createDefaultAxes()
        categories = ["jedynki", "dwójki", "trójki", "czwórki", "piątki","szóstki","3x","4x","full","maly strit","duzy strit","general","szansa"]
        axisX = QBarCategoryAxis()
        axisX.append(categories)
        axisX.setLabelsFont(QFont("Arial", 12))


        axisY = QValueAxis()
        axisY.setLabelsFont(QFont("Arial", 10))
        axisY.setTickCount(11)  # Ilość etykiet na osi Y
        axisY.setLabelFormat("%i")  # Format etykiet na osi Y
        axisY.setRange(0, 50)  # Przedział na osi Y
        chart.axisY().setVisible(False)

        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)
        chart.axisX().setVisible(False)

        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)
        chart.axisX().setVisible(False)
        chart_view = QChartView(chart)
        chart.axisY().setLabelsFont(QFont("Arial", 10))

        self.wykres_slupkowy = chart_view
        self.wykres_slupkowy.setMaximumHeight(390)
        self.layout.addWidget(self.wykres_slupkowy, 1, 1, 9, 9)

        data1 = self.score_player_one_history
        data2 = self.score_player_two_history


        chart2 = QChart()
        chart2.setTitle("Wykres punktowy runda po rundzie")

        series1 = QLineSeries()
        series2 = QLineSeries()


        for i, (x, y) in enumerate(zip(data1, data2)):
            series1.append(i, x)
            series2.append(i, y)

        series1.setName("Gracz 1")
        series2.setName("Gracz CPU")

        chart2.addSeries(series1)
        chart2.addSeries(series2)


        axis_x = QValueAxis()
        axis_x.setRange(0, len(data1) - 1)
        axis_x.setTickCount(len(data1))
        axis_x.setLabelFormat("%d")
        axis_x.setLabelsVisible(True)


        axis_y =QValueAxis()
        axis_y.setLabelsVisible(True)

        if data2[-1] > data1[-1]:
            axis_y.setMax(data2[-1])

        chart2.addAxis(axis_x, Qt.AlignBottom)
        chart2.legend().setVisible(True)
        chart2.legend().setAlignment(Qt.AlignBottom)


        chart2.setAxisY(axis_y, series1)
        chart2.setAxisY(axis_y, series2)
        chart2.axisY().setLabelsFont(QFont("Arial", 10))
        chart2.axisX().setLabelsFont(QFont("Arial", 12))

        chart2.legend().setVisible(True)
        chart2.legend().setAlignment(Qt.AlignBottom)

        chart_view_line = QChartView(chart2)
        self.wykres_liniowy = chart_view_line
        self.layout.addWidget(self.wykres_liniowy, 9, 1, 10, 9)

        self.wykres_liniowy.show()
        self.wykres_slupkowy.show()
        self.text_play_again.show()
        self.text_play_again.mousePressEvent = self.play_again


    def update_timer(self):
        self.player_1_time -= 1
        self.label_time.setText(str(self.player_1_time) + "s")
        if self.player_1_time < 0:
            self.timer1.stop()
            for i in range(0,16):
                if self.score_player_two[i] == -1:
                    self.score_player_two[i] = 0
            self.final_score()

    def update_timer2(self):
        self.player_2_time -= 1
        self.label_time2.setText(str(self.player_2_time)+"s")
        if self.player_2_time < 0:
            self.timer2.stop()
            for i in range(0,16):
                if self.score_player_one[i] == -1:
                    self.score_player_one[i] = 0
            self.final_score()


    def save_statistics(self):
        with open("JSON/statistics.json", "r") as file:
            loaded_statistics = json.load(file)
        player1_number_win_with_computer = loaded_statistics["player_win_with_computer"].get("player1", 0)
        computer_number_win = loaded_statistics["player_win_with_computer"].get("playerCPU", 0)
        best_score_with_computer = loaded_statistics["player_with_computer_score"].get("player1", 0)
        best_score_computer = loaded_statistics["player_with_computer_score"].get("playerCPU", 0)
        win = False
        if self.player_1_time >= 0:
            if self.score_player_one[16]>self.score_player_two[16]:
                player1_number_win_with_computer+=1
                win=True
            if self.score_player_one[16]>best_score_with_computer:
                best_score_with_computer = self.score_player_one[16]
            statistics_win = {
                    "player1": player1_number_win_with_computer,
                    "playerCPU": computer_number_win
            }
            statistics_score = {
                    "player1": best_score_with_computer,
                    "playerCPU": best_score_computer
            }
            loaded_statistics["player_win_with_computer"].update(statistics_win)
            loaded_statistics["player_with_computer_score"].update(statistics_score)
            with open("JSON/statistics.json", "w") as f:
                json.dump(loaded_statistics, f, indent=4)
            detailed_stat = detailed_statistics.Detailed_statistics(None)
            if win==True:
                detailed_stat.save_statistics_points(self.score_player_one[16],1)
            else:
                detailed_stat.save_statistics_points(self.score_player_one[16], 0)

        if self.player_2_time >= 0:
            with open("JSON/statistics.json", "r") as file:
                loaded_statistics = json.load(file)
            if self.score_player_two[16] > self.score_player_one[16]:
                 computer_number_win += 1
            if self.score_player_two[16] > best_score_computer:
                best_score_computer = self.score_player_two[16]
            statistics_win = {
                    "player1": player1_number_win_with_computer,
                    "playerCPU": computer_number_win
            }
            statistics_score = {
                    "player1": best_score_with_computer,
                    "playerCPU": best_score_computer
            }
            loaded_statistics["player_win_with_computer"].update(statistics_win)
            loaded_statistics["player_with_computer_score"].update(statistics_score)
            with open("JSON/statistics.json", "w") as f:
                json.dump(loaded_statistics, f, indent=4)

    def play_again(self, event):
        self.background_label.deleteLater()
        self.wykres_liniowy.deleteLater()
        self.wykres_slupkowy.deleteLater()
        self.image_play_again.deleteLater()
        self.text_play_again.deleteLater()
        self.result.deleteLater()
        self.is_sel = [0, 0, 0, 0, 0]
        self.player = 1  # kolej gracza 1 czy gracza 2
        self.score_player_one = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,0]  # wartosci -1 gdyz sprawdzam
        # czy kategoria została już wybrana
        self.score_player_two = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0]
        self.tab_probabilities = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.selected_yahtzee_1 = False
        self.selected_yahtzee_2 = False
        self.score_player_one_history = [0]
        self.score_player_two_history = [0]
        self.number_roll = 0
        self.button.show()
        self.next_t = 1
        self.t = settings.Settings(self)
        self.result = QLabel()
        self.result.setAlignment(Qt.AlignCenter)
        self.result.setText("0 : 0")
        self.result.setStyleSheet("font-size:60px;color: rgb(255,255,255);")
        self.layout.addWidget(self.result, 1, 5, 1, 3)

        self.time = self.t.return_selected_time()
        self.player_1_time = self.time
        self.player_2_time = self.time
        self.label_time.setText(str(self.time)+"s")
        self.label_time2.setText(str(self.time)+"s")
        self.background_label = QLabel(self)
        self.wykres_slupkowy = QLabel(self)
        self.wykres_liniowy = QLabel(self)
        self.image_play_again = QLabel(self)

        self.text_play_again = QLabel(self)
        self.text_play_again.setText("Zagraj ponownie")
        self.text_play_again.setStyleSheet(
        "QLabel { color: rgb(255, 255, 255); }"
        "QLabel:hover { color: rgb(255, 0, 0); }"
        )
        self.layout.addWidget(self.text_play_again, 19, 1, 1, 2)
        self.text_play_again.hide()
        self.pause.show()
        self.button.show()
        self.player=1
        self.set_dice_element()
        self.punctation()
        self.category()
        self.choose_category()
        self.timer1.start()
    def player_CPU(self,difficulty):
        self.dice_element = [self.image_dice_1, self.image_dice_2, self.image_dice_3, self.image_dice_4,self.image_dice_5]
        if difficulty=="easy":
            QtCore.QTimer.singleShot(1000, lambda: self.build_categories(self.selected_category))
            QtWidgets.QApplication.processEvents()
            QtCore.QTimer.singleShot(2000, lambda: self.build_categories(self.selected_category))
            self.selected_dice_computer=[0,0,0,0,0]
            QtCore.QTimer.singleShot(4000, lambda: self.select_category_computer())
        elif difficulty=="hard":
            self.select_category_computer_hard()
            QtCore.QTimer.singleShot(1000, lambda: self.build_categories(self.selected_category))
            QtCore.QTimer.singleShot(1500, lambda: self.select_category_computer_hard())
            QtWidgets.QApplication.processEvents()
            QtCore.QTimer.singleShot(2000, lambda: self.build_categories(self.selected_category))
            self.selected_dice_computer = [0, 0, 0, 0, 0]
            QtCore.QTimer.singleShot(3000, lambda: self.select_category_computer_hard())
            QtCore.QTimer.singleShot(4000, lambda: self.select_category_computer())

    def select_category_computer_hard(self):
        tab_hierarchy = [11, 10, 9, 8, 7, 5, 4, 6, 3, 2, 1, 0, 12]
        hierarchy_categories = ["yahtzee", "lstrit", "sstrit", "full", "x4",
        "sixes", "fives", "x3", "fours", "threes", "twos", "ones", "chance"]
        hierachy_polish= ["general", "duzy strit", "maly strit", "full", "x4",
        "szostki", "piatki", "x3", "czworki", "trojki", "dwojki", "jedynki", "szansa"]
        self.tab_probabilities = np.array(self.calculate_probabilities())
        tab_active_categories = self.score_player_two[0:6]
        tab_active_categories.extend(self.score_player_two[8:15])
        for i in range(0, 13):
            if tab_active_categories[i] != -1:
                self.tab_probabilities[i] = -1
        max_indices = np.where(self.tab_probabilities == np.max(self.tab_probabilities))[0]
        indices_hierarchy = np.where(np.isin(tab_hierarchy, max_indices))
        min_indices_hierarchy = np.min(indices_hierarchy)
        #print(self.tab_probabilities)
        self.selected_category = hierarchy_categories[min_indices_hierarchy]
        self.text_selected_category=hierachy_polish[min_indices_hierarchy]
        self.robot_text.setText(self.text_selected_category)
    def select_category_computer(self):
        if self.difficulty=="easy":
            a="_"+self.selected_category
            func = getattr(self, a, None)
            print(func)
            func("none")
        elif self.difficulty=="hard":
            a = ["threes", "fours", "fives", "sixes"]
            if np.max(self.tab_probabilities)<100:
                if self.tab_probabilities[12]!=-1:
                    self.selected_category="chance"
                elif self.tab_probabilities[0]!=-1:
                    self.selected_category = "ones"
                elif self.tab_probabilities[1]!=-1:
                    self.selected_category = "twos"
                elif self.tab_probabilities[11]!=-1:
                    self.selected_category = "yahtzee"
                else:
                    selected_fragment = self.tab_probabilities[2:12]
                    print("S:",selected_fragment)
                    max_value = np.max(selected_fragment)
                    if max_value!=-1:
                        first_max_index = np.where(selected_fragment == max_value)[0][0]
                        self.selected_category = a[first_max_index]
            #self.robot_text.setText(self.selected_category)
            a = "_" + self.selected_category
            func = getattr(self, a, None)
            #print(func)
            func("none")

    def build_categories(self,selected_category):
        a = ["ones", "twos", "threes", "fours", "fives", "sixes"]
        for j in range(0, 5):
            if self.selected_dice_computer[j] == 1:
                self.selected_dice_computer[j] = 0
                self.stop_dice(self.dice_element[j], j + 1)
        self.dice_element=[self.image_dice_1,self.image_dice_2,self.image_dice_3,self.image_dice_4,self.image_dice_5]
        if selected_category=="ones":
            search=1
        elif selected_category=="twos":
            search = 2
        elif selected_category=="threes":
            search = 3
        elif selected_category=="fours":
            search = 4
        elif selected_category=="fives":
            search = 5
        elif selected_category=="sixes":
            search = 6
        if self.selected_category in a:
            for j in range(0,5):
                if self.dice[j]==search and self.selected_dice_computer[j]==0:
                    self.selected_dice_computer[j]=1
                    self.stop_dice(self.dice_element[j],j+1)
        a1 = self.dice.count(1)
        a2 = self.dice.count(2)
        a3 = self.dice.count(3)
        a4 = self.dice.count(4)
        a5 = self.dice.count(5)
        a6 = self.dice.count(6)
        all = [a1, a2, a3, a4, a5, a6]
        a_max = max(all)
        index_max = max(i for i, v in enumerate(all) if v == a_max)
        index_max += 1
        if self.selected_category == "x3" or self.selected_category == "x4" or self.selected_category == "yahtzee":
            for j in range(0, 5):
                if self.dice[j] == index_max and self.selected_dice_computer[j] == 0:
                    self.selected_dice_computer[j] = 1
                    self.stop_dice(self.dice_element[j], j + 1)
        if self.selected_category == "full":
            index_stop = [0, 0]
            index_stop_one = 0
            z = 0
            for j in range(0, 6):
                if all[j] == 1:
                    index_stop_one = j + 1
                if all[j] == 3 or all[j] == 2:
                    index_stop[z] = j + 1
                    z += 1
            if index_stop[1] == 0:
                index_stop[1] = index_stop_one
            for j in range(0, 5):
                if (self.dice[j] == index_stop[0] or self.dice[j] == index_stop[1]) and self.selected_dice_computer[j] == 0:
                    self.selected_dice_computer[j] = 1
                    self.stop_dice(self.dice_element[j], j + 1)
        if self.selected_category == "sstrit":
            tab = []
            section_start = 0
            section_stop = 0
            dice = np.array(self.dice)
            unique_values_1_to_4 = np.unique(dice[(dice >= 1) & (dice <= 4)])
            # Liczba unikalnych wartości od 2 do 6
            unique_values_2_to_5 = np.unique(dice[(dice >= 2) & (dice <= 5)])
            unique_values_3_to_6 = np.unique(dice[(dice >= 3) & (dice <= 6)])
            max_unique_values = max(len(unique_values_1_to_4), len(unique_values_2_to_5), len(unique_values_3_to_6))
            if len(unique_values_1_to_4) == max_unique_values:
                section_start = 1
                section_stop = 4
            elif len(unique_values_2_to_5) == max_unique_values:
                section_start = 2
                section_stop = 5
            else:
                section_start = 3
                section_stop = 6
            if self.tab_probabilities[9]==100: # jezeli wykonany jest maly strit, spróbuj zrobić duzego strita
                unique_values_1_to_5 = np.unique(dice[(dice >= 1) & (dice <= 5)])
                unique_values_2_to_6 = np.unique(dice[(dice >= 2) & (dice <= 6)])
                if len(unique_values_1_to_5) >= len(unique_values_2_to_6):
                    section_start = 1
                    section_stop = 5
                else:
                    section_start = 2
                    section_stop = 6
            for j in range(0, 5):
                if self.dice[j] >= section_start and self.dice[j] <= section_stop and self.selected_dice_computer[j] == 0:
                    tab.append(self.dice[j])
                    if tab.count(self.dice[j]) <= 1:
                        self.selected_dice_computer[j] = 1
                        self.stop_dice(self.dice_element[j], j + 1)
            tab = []
        if self.selected_category == "lstrit":
            tab = []
            section_start = 0
            section_stop = 0
            dice = np.array(self.dice)
            unique_values_1_to_5 = np.unique(dice[(dice >= 1) & (dice <= 5)])
            # Liczba unikalnych wartości od 2 do 6
            unique_values_2_to_6 = np.unique(dice[(dice >= 2) & (dice <= 6)])
            if len(unique_values_1_to_5) >= len(unique_values_2_to_6):
                section_start = 1
                section_stop = 5
            else:
                section_start = 2
                section_stop = 6
            for j in range(0, 5):
                if self.dice[j] >= section_start and self.dice[j] <= section_stop and self.selected_dice_computer[j] == 0:
                    tab.append(self.dice[j])
                    if tab.count(self.dice[j]) <= 1:
                        self.selected_dice_computer[j] = 1
                        self.stop_dice(self.dice_element[j], j + 1)
            tab = []
        if self.selected_category == "chance":
            for j in range(0, 5):
                if self.dice[j] == 6 or self.dice[j] == 5 and self.selected_dice_computer[j] == 0:
                    self.selected_dice_computer[j] = 1
                    self.stop_dice(self.dice_element[j], j + 1)
        self.roll_dice("none")

    def scheme_Bernoulli(self,n,k,p,q):
        P=(math.factorial(n) / (math.factorial(k) * math.factorial(n - k))) * (p ** k) * (q ** (n-k))
        P_round=round(P,2)
        return P_round*100
    def calculate_probabilities(self):
        probabilities=np.array([0,0,0,0,0,0,0,0,0,0,0,0,0])
        p=1/6
        q=5/6
        dice = np.array(self.dice)
        contains_1 = np.any(dice == 1)
        contains_2 = np.any(dice == 2)
        contains_3 = np.any(dice == 3)
        contains_4 = np.any(dice == 4)
        contains_5 = np.any(dice == 5)
        contains_6 = np.any(dice == 6)
        if contains_1:
            count_1 = np.count_nonzero(dice == 1)
            n = 5 - count_1
            k = 3 - count_1
            if k <= 0:
                probabilities[0] = 100
            else:
                probabilities[0] = self.scheme_Bernoulli(n, k, p, q)
        if contains_2:
            count_2 = np.count_nonzero(dice == 2)
            n = 5 - count_2
            k = 3 - count_2
            if k <= 0:
                probabilities[1] = 100
            else:
                probabilities[1] = self.scheme_Bernoulli(n, k,  p, q)
        if contains_3:
            count_3 = np.count_nonzero(dice == 3)
            n = 5 - count_3
            k = 3 - count_3
            if k <= 0:
                probabilities[2] = 100
            else:
                probabilities[2] = self.scheme_Bernoulli(n, k,  p, q)
        if contains_4:
            count_4 = np.count_nonzero(dice == 4)
            n = 5 - count_4
            k = 3 - count_4
            if k <= 0:
                probabilities[3] = 100
            else:
                probabilities[3] = self.scheme_Bernoulli(n, k,  p, q)
        if contains_5:
            count_5 = np.count_nonzero(dice == 5)
            n = 5 - count_5
            k = 3 - count_5
            if k <= 0:
                probabilities[4] = 100
            else:
                probabilities[4] = self.scheme_Bernoulli(n, k,  p, q)
        if contains_6:
            count_6 = np.count_nonzero(dice == 6)
            n = 5 - count_6
            k = 3 - count_6
            if k <= 0:
                probabilities[5] = 100
            else:
                probabilities[5] = self.scheme_Bernoulli(n, k,  p, q)

        unique_elements, counts = np.unique(dice, return_counts=True)
        max_counts = np.max(counts) #najwieksza ilosc powtorzen
        most_common_elements = max(unique_elements[counts == max_counts]) #wybor najwyzszej sumy oczek
        sorted_counts = np.sort(counts)[::-1]
        # Wybierz drugą największą wartość liczby wystąpień
        if len(sorted_counts) > 1:
            second_largest_count = sorted_counts[1]
        else:
            second_largest_count = 0
        #print("maxcounts:",max_counts)
        #print("most_common:", most_common_elements)
        n = 5 - max_counts ## dla 3x
        k = 3 - max_counts
        if k<=0:
            probabilities[6] = 100
        else:
            probabilities[6] = self.scheme_Bernoulli(n, k,  p, q)

        n = 5 - max_counts  ## dla 4x
        k = 4 - max_counts
        if k <= 0:
            probabilities[7] = 100
        else:
            probabilities[7] = self.scheme_Bernoulli(n, k,  p, q)
        #dla full
        if max_counts==3 and second_largest_count==2:
            probabilities[8] = 100
        elif max_counts==5:
            n=2
            k=2
            probabilities[8] = self.scheme_Bernoulli(n, k, p, q)
        elif max_counts==4:
            n = 1
            k = 1
            probabilities[8] = self.scheme_Bernoulli(n, k, p, q)
        elif max_counts==3 and second_largest_count==1:
            n = 1
            k = 1
            probabilities[8] = self.scheme_Bernoulli(n, k, p, q)
        elif max_counts==2 and second_largest_count==2:
            n = 1
            k = 1
            p = 2/6
            q = 4/6
            probabilities[8] = self.scheme_Bernoulli(n, k, p, q)
        elif max_counts==2 and second_largest_count==1:
            n = 2
            k = 2
            probabilities[8] = self.scheme_Bernoulli(n, k, p, q)
        elif max_counts==1:
            n = 3
            k = 3
            probabilities[8] = self.scheme_Bernoulli(n, k, p, q)
        p=1/6
        q=5/6
        # dla maly strit
        # Liczba unikalnych wartości od 1 do 4
        unique_values_1_to_4 = np.unique(dice[(dice >= 1) & (dice <= 4)])
        # Liczba unikalnych wartości od 2 do 5
        unique_values_2_to_5 = np.unique(dice[(dice >= 2) & (dice <= 5)])
        # Liczba unikalnych wartości od 3 do 6
        unique_values_3_to_6 = np.unique(dice[(dice >= 3) & (dice <= 6)])
        max_unique = max(len(unique_values_1_to_4), len(unique_values_2_to_5),len(unique_values_3_to_6))
        n = 5 - max_unique
        k = 4 - max_unique
        if k <= 0:
            probabilities[9] = 100
        elif all(elem in unique_values_1_to_4 for elem in [1, 2, 3]):
            p = 1 / 6
            q = 5 / 6
            probabilities[9] = self.scheme_Bernoulli(n, k, p, q)
        elif all(elem in unique_values_2_to_5 for elem in [2, 3, 4]):
            p = 2 / 6
            q = 4 / 6
            probabilities[9] = self.scheme_Bernoulli(n, k, p, q)
        elif all(elem in unique_values_3_to_6 for elem in [3, 4, 5]):
            p = 2 / 6
            q = 4 / 6
            probabilities[9] = self.scheme_Bernoulli(n, k, p, q)
        elif all(elem in unique_values_3_to_6 for elem in [4, 5, 6]):
            p = 1 / 6
            q = 5 / 6
            probabilities[9] = self.scheme_Bernoulli(n, k, p, q)
        else:
            probabilities[9] = self.scheme_Bernoulli(n, k, p, q)

        p = 1 / 6
        q = 5 / 6
        # dla duzy strit
        # Liczba unikalnych wartości od 1 do 5
        unique_values_1_to_5 =np.unique(dice[(dice >= 1) & (dice <= 5)])
        # Liczba unikalnych wartości od 2 do 6
        unique_values_2_to_6 = np.unique(dice[(dice >= 2) & (dice <= 6)])
        max_unique=max(len(unique_values_1_to_5),len(unique_values_2_to_6))
        n = 5 - max_unique  #duzystrit
        k = 5 - max_unique
        if all(elem in unique_values_1_to_5 for elem in [2,3,4,5]):
            p=2/6
            q=4/6
        if k <= 0:
            probabilities[10] = 100
        else:
            probabilities[10] = self.scheme_Bernoulli(n, k, p, q)
        p = 1 / 6
        q = 5 / 6

        n = 5 - max_counts  ## dla yahtzee
        k = 5 - max_counts
        if k <= 0:
            probabilities[11] = 100
            if self.tab_probabilities[11]==-1: #gdy juz wykorzystano raz generała
                probabilities[10] = 100
                probabilities[9] = 100
                probabilities[8] = 100
        else:
            probabilities[11] = self.scheme_Bernoulli(n, k,  p, q)
        return probabilities

    def pause_event(self,event):
        self.sounds_.click_button()
        if self.player==1:
            self.timer1.stop()
        else:
            self.timer2.stop()
        self.pause.hide()
        self.play.show()

    def play_event(self,event):
        self.sounds_.click_button()
        if self.player==1:
            self.timer1.start()
        else:
            self.timer2.start()
        self.play.hide()
        self.pause.show()


    def undo(self,event):
        self.timer1.stop()
        self.timer2.stop()
        self.timer2.deleteLater()
        self.timer2 = None
        self.timer1.deleteLater()
        self.timer1 = None
        a = menu.Menu(self.wid)
        self.wid.addWidget(a)
        self.wid.setCurrentIndex(self.wid.currentIndex() + 1)
