import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QListWidget, QFileDialog, QMessageBox, QLineEdit, QLabel, QTableWidgetItem, QPushButton, QDateEdit
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QImage, QPixmap, QFont
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QSize
import menu
import json
import base64

class Settings(QMainWindow):
    def __init__(self,widget):
       super(Settings, self).__init__()
       loadUi("menu.ui", self)
       self.setgraphicselement()
       self.widget=widget
       self.selected_time=180
    def setgraphicselement(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QGridLayout(central_widget)

        background_label = QLabel()
        pixmap = QPixmap("graphics/background.png")
        scaled_pixmap = pixmap.scaled(1280, 720)
        background_label.setPixmap(scaled_pixmap)
        layout.addWidget(background_label, 0, 0, 9, 9)
        background_label.setScaledContents(True)
        self.update_background()

        image_label1, text_label1 = self.createWidgets("graphics/dice_1.png", "Ustaw limit czasu\n dla zawodników gry w kości")
        layout.addWidget(image_label1, 3, 3)
        layout.addWidget(text_label1, 3, 4)

        image_label2, text_label2 = self.createWidgets("graphics/dice_2.png", "Ustaw poziom trudności\n gracza komputerowego")
        layout.addWidget(image_label2, 5, 3)
        layout.addWidget(text_label2, 5, 4)

        image_label3, text_label3 = self.createWidgets("graphics/dice_3.png", "Ustaw poziom głośności\n gry")
        layout.addWidget(image_label3, 7, 3)
        layout.addWidget(text_label3, 7, 4)

        data = [text_label1, text_label2, text_label3]
        for i in data:
            i.setStyleSheet(
                "QLabel { font-size:28px;font-weight: bold;color: rgb(255, 255, 255); }"
                "QLabel:hover { color: rgb(255, 0, 0); }"
            )


        image_label6 = QLabel(self)
        image6 = QImage("graphics/button_undo.png")
        scaled_image6 = image6.scaled(image6.width() // 6, image6.height() // 6)
        scaled_pixmap6 = QPixmap.fromImage(scaled_image6)
        image_label6.setPixmap(scaled_pixmap6)
        image_label6.setGeometry(20, 20, scaled_pixmap6.width(), scaled_pixmap6.height())
        image_label6.mousePressEvent = self.undo

        self.difficulty_combobox = QComboBox(self.centralwidget)
        self.difficulty_combobox.setStyleSheet("background-color: white;color:black;font-size:24px")
        self.difficulty_combobox.view().setStyleSheet("background-color: white; color:black;")
        self.difficulty_combobox.setEditable(True)
        self.difficulty_combobox.lineEdit().setAlignment(Qt.AlignCenter)
        self.difficulty_combobox.addItems(["Latwy", "Trudny"])
        self.difficulty_combobox.currentIndexChanged.connect(self.difficulty_changed)
        self.difficulty_combobox.setMaximumHeight(40)
        layout.addWidget(self.difficulty_combobox, 6, 4, 1, 1)

        self.time_limit_combobox = QComboBox(self.centralwidget)
        self.time_limit_combobox.setStyleSheet("background-color: white;color:black;font-size:24px")
        self.time_limit_combobox.view().setStyleSheet("background-color: white; color:black;")
        self.time_limit_combobox.setEditable(True)
        self.time_limit_combobox.lineEdit().setAlignment(Qt.AlignCenter)
        self.time_limit_combobox.addItems(["120 sekund", "180 sekund", "240 sekund", "300 sekund","360 sekund","420 sekund","480 sekund","540 sekund","600 sekund"])
        self.time_limit_combobox.currentIndexChanged.connect(self.on_time_limit_changed)
        self.time_limit_combobox.setMaximumHeight(40)
        layout.addWidget(self.time_limit_combobox, 4, 4, 1,1)

        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setMinimum(0)
        self.volumeSlider.setMaximum(100)
        self.volumeSlider.setSingleStep(1)
        self.volumeSlider.valueChanged.connect(self.set_volume)
        self.volumeSlider.setMaximumWidth(360)
        layout.setAlignment(self.volumeSlider, Qt.AlignHCenter)
        layout.addWidget(self.volumeSlider, 7, 4, 2, 2)


        with open("JSON/settings.json", "r") as file:
            loaded_settings = json.load(file)
        time_ = loaded_settings.get("time_limit", 180)
        volume_ = loaded_settings.get("sound_volume", 100)
        difficulty_ = loaded_settings.get("difficulty", "easy")
        if difficulty_ == "easy":
            difficulty_nr = 0
        else:
            difficulty_nr = 1
        time_nr = (time_ / 60) - 2
        volume_nr = volume_ / 100
        self.time_limit_combobox.setCurrentIndex(int(time_nr))
        self.volumeSlider.setSliderPosition(int(volume_nr * 100))
        self.difficulty_combobox.setCurrentIndex(int(difficulty_nr))
    def update_background(self):
        pixmap = QPixmap("background_image.png")  # Twoja grafika tła
        scaled_pixmap = pixmap.scaled(QSize(self.width(), self.height()))
        self.background_label.setPixmap(scaled_pixmap)
    def createWidgets(self, image_path, text):
        image_label = QLabel()
        image = QImage(image_path)
        scaled_image = image.scaled(image.width() // 8, image.height() // 8)
        scaled_pixmap = QPixmap.fromImage(scaled_image)
        image_label.setPixmap(scaled_pixmap)

        text_label = QLabel(text)
        text_label.setStyleSheet("font-size: 38px; font-weight: bold; color: #fff;")
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setCursor(Qt.PointingHandCursor)

        return image_label, text_label
    def set_volume(self, value):
            volume = value
            with open("JSON/settings.json", "r") as file:
                loaded_settings = json.load(file)
            time_ = loaded_settings.get("time_limit", 180)
            difficulty_ = loaded_settings.get("difficulty", "easy")
            settings = {
                "time_limit": time_,
                "sound_volume": volume,
                "difficulty": difficulty_
            }
            with open("JSON/settings.json", "w") as file:
                json.dump(settings, file, indent=4)


    def on_time_limit_changed(self, index):
        a=["120 sekund","180 sekund","240 sekund","300 sekund","360 sekund","420 sekund","480 sekund","540 sekund","600 sekund"]
        self.selected_time = self.time_limit_combobox.currentText()
        print("Wybrano:", self.selected_time)
        b=a.index(self.selected_time)
        b=b+2
        self.selected_time=b*60
        with open("JSON/settings.json", "r") as file:
            loaded_settings = json.load(file)
        volume_ = loaded_settings.get("sound_volume", 1)
        difficulty_ = loaded_settings.get("difficulty", "easy")
        settings = {
            "time_limit": self.selected_time,
            "sound_volume": volume_,
            "difficulty": difficulty_
        }
        with open("JSON/settings.json", "w") as file:
            json.dump(settings, file,indent=4)

    def difficulty_changed(self, index):
        self.selected_difficulty = self.difficulty_combobox.currentText()
        if self.selected_difficulty == "Latwy":
            self.selected_difficulty = "easy"
        elif self.selected_difficulty == "Trudny":
            self.selected_difficulty = "hard"
        with open("JSON/settings.json", "r") as file:
            loaded_settings = json.load(file)
        volume_ = loaded_settings.get("sound_volume", 1)
        time_ = loaded_settings.get("time_limit", 180)
        settings = {
            "time_limit": time_,
            "sound_volume": volume_,
            "difficulty": self.selected_difficulty
        }
        with open("JSON/settings.json", "w") as file:
            json.dump(settings, file,indent=4)
    def return_selected_time(self):
        with open("JSON/settings.json", "r") as file:
            loaded_settings = json.load(file)
        time_limit = loaded_settings.get("time_limit", 180)
        return time_limit
    def return_selected_difficulty(self):
        with open("JSON/settings.json", "r") as file:
            loaded_settings = json.load(file)
        difficulty = loaded_settings.get("difficulty", "hard")
        return difficulty
    def undo(self,event):
        widget=self.widget
        class_menu = menu.Menu(widget)
        widget.addWidget(class_menu)
        widget.setCurrentIndex(widget.currentIndex() + 1)