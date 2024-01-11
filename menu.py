from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.uic import loadUi

import game_1_player
import game_2_players
import rules
import settings
import statis
class Menu(QMainWindow):
    def __init__(self,widget):
        super(Menu, self).__init__()
        loadUi("menu.ui", self)
        self.setgraphicselement()
        self.widget=widget
        self.time_limit=300
        self.volume=100
    def setgraphicselement(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QGridLayout(central_widget)

        background_label = QLabel()
        pixmap = QPixmap("graphics/background.png")
        scaled_pixmap = pixmap.scaled(1366, 768)
        background_label.setPixmap(scaled_pixmap)
        layout.addWidget(background_label, 0, 0, 9, 9)
        background_label.setScaledContents(True)
        self.update_background()
        image_label1, text_label1 = self.createWidgets("graphics/dice_1.png", "Gra z komputerem")
        layout.addWidget(image_label1, 3, 3)
        layout.addWidget(text_label1, 3, 4)

        image_label2, text_label2 = self.createWidgets("graphics/dice_2.png", "Gra w 2 osoby")
        layout.addWidget(image_label2, 4, 3)
        layout.addWidget(text_label2, 4, 4)

        image_label3, text_label3 = self.createWidgets("graphics/dice_3.png", "Zasady gry")
        layout.addWidget(image_label3, 5, 3)
        layout.addWidget(text_label3, 5, 4)

        image_label4, text_label4 = self.createWidgets("graphics/dice_4.png", "Statystyki")
        layout.addWidget(image_label4, 6, 3)
        layout.addWidget(text_label4, 6, 4)

        image_label5, text_label5 = self.createWidgets("graphics/dice_5.png", "Ustawienia")
        layout.addWidget(image_label5, 7, 3)
        layout.addWidget(text_label5, 7, 4)
        data=[text_label1,text_label2,text_label3,text_label4,text_label5]
        for i in data:
            i.setStyleSheet(
                "QLabel { font-size:38px;font-weight: bold;color: rgb(255, 255, 255); }"
                "QLabel:hover { color: rgb(255, 0, 0); }"
            )

        text_label1.mousePressEvent = self.one_player
        text_label2.mousePressEvent = self.two_player
        text_label3.mousePressEvent = self.rules
        text_label4.mousePressEvent = self.statistics
        text_label5.mousePressEvent = self.settings



    def update_background(self):
        pixmap = QPixmap("background_image.png")
        scaled_pixmap = pixmap.scaled(QSize(self.width(), self.height()))
        self.background_label.setPixmap(scaled_pixmap)

    def createWidgets(self, image_path, text):
        image_label = QLabel()
        image = QImage(image_path)
        scaled_image = image.scaled(image.width() // 8, image.height() // 8)
        scaled_pixmap = QPixmap.fromImage(scaled_image)
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setPixmap(scaled_pixmap)

        text_label = QLabel(text)
        text_label.setStyleSheet("font-size: 38px; font-weight: bold; color: #fff;")
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setCursor(Qt.PointingHandCursor)

        return image_label, text_label
    def one_player(self,event):
        class_1_player = game_1_player.Game1Player(self.widget)
        self.widget.addWidget(class_1_player)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
    def two_player(self,event):
        class_2_player = game_2_players.Game2Players(self.widget)
        self.widget.addWidget(class_2_player)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
    def rules(self, event):
        class_rules = rules.Rules(self.widget)
        self.widget.addWidget(class_rules)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
    def statistics(self,event):
        class_statistics = statis.Statis(self.widget)
        self.widget.addWidget(class_statistics)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
    def settings(self,event):
        class_settings = settings.Settings(self.widget)
        self.widget.addWidget(class_settings)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

