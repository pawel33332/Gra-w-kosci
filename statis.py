import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QListWidget, QFileDialog, QMessageBox, QLineEdit, QLabel, QTableWidgetItem, QPushButton, QDateEdit
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QImage, QPixmap, QFont
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QSize

import detailed_statistics
import menu
import json
import ranking_list

class Statis(QMainWindow):
    def __init__(self,widget):
       super(Statis, self).__init__()
       loadUi("menu.ui", self)
       self.widget=widget
       self.setgraphicselement()
       self.show_statistics()
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
        self.image_label, self.text_label = self.createWidgets("graphics/dice_1.png", "Ilość zwycięstw\n gracza 1/gracza 2:")
        layout.addWidget(self.image_label, 3, 3)
        layout.addWidget(self.text_label, 3, 4)
        layout.setAlignment(self.image_label, Qt.AlignRight)

        self.image_label2, self.text_label2 = self.createWidgets("graphics/dice_2.png",
                                                               "Ilość zwycięstw/przegranych\n z graczem CPU:")
        layout.addWidget(self.image_label2, 4, 3)
        layout.addWidget(self.text_label2, 4, 4)
        layout.setAlignment(self.image_label2, Qt.AlignRight)

        self.image_label3, self.text_label3 = self.createWidgets("graphics/dice_3.png",
                                                                 "Najwyższy zdobyty wynik\n przez gracza 1/gracza 2:")
        layout.addWidget(self.image_label3, 5, 3)
        layout.addWidget(self.text_label3, 5, 4)
        layout.setAlignment(self.image_label3, Qt.AlignRight)

        self.image_label4, self.text_label4 = self.createWidgets("graphics/dice_4.png",
                                                                 "Najwyższy zdobyty wynik przeciwko\n graczowi CPU/przez gracza CPU:")
        layout.addWidget(self.image_label4, 6, 3)
        layout.addWidget(self.text_label4, 6, 4)
        layout.setAlignment(self.image_label4, Qt.AlignRight)

        self.text_label5 = QLabel(self)
        self.text_label6 = QLabel(self)
        self.text_label7 = QLabel(self)

        self.text_label5.setStyleSheet(
            "QLabel { color: rgb(255, 255, 255);font-size: 34px; font-weight: bold; }"
            "QLabel:hover { color: rgb(255, 0, 0); }"
        )
        self.text_label5.setAlignment(Qt.AlignCenter)
        self.text_label5.setText("Resetuj statystyki")
        self.text_label5.mousePressEvent = self.reset
        layout.addWidget(self.text_label5, 7, 3)


        self.text_label6.setStyleSheet(
            "QLabel { color: rgb(255, 255, 255);font-size: 34px; font-weight: bold; }"
            "QLabel:hover { color: rgb(255, 0, 0); }"
        )
        self.text_label6.setAlignment(Qt.AlignCenter)
        self.text_label6.setText("Szczegółowe statystyki")
        self.text_label6.mousePressEvent = self.detailed_statistics
        layout.addWidget(self.text_label6, 7, 4)

        self.text_label7.setStyleSheet(
            "QLabel { color: rgb(255, 255, 255);font-size: 34px; font-weight: bold; }"
            "QLabel:hover { color: rgb(255, 0, 0); }"
        )
        self.text_label7.setAlignment(Qt.AlignCenter)
        self.text_label7.setText("Lista rankingowa")
        self.text_label7.mousePressEvent = self.ranking_list
        layout.addWidget(self.text_label7, 7, 5)

        image_label6 = QLabel(self)
        image6 = QImage("graphics/button_undo.png")
        scaled_image6 = image6.scaled(image6.width() // 6, image6.height() // 6)
        scaled_pixmap6 = QPixmap.fromImage(scaled_image6)
        image_label6.setPixmap(scaled_pixmap6)
        image_label6.setGeometry(20, 20, scaled_pixmap6.width(), scaled_pixmap6.height())
        image_label6.mousePressEvent = self.undo

    def update_background(self):
        pixmap = QPixmap("background_image.png")
        scaled_pixmap = pixmap.scaled(QSize(self.width(), self.height()))
        self.background_label.setPixmap(scaled_pixmap)

    def createWidgets(self, image_path, text):
        image_label = QLabel()
        image = QImage(image_path)
        scaled_image = image.scaled(image.width() // 8, image.height() // 8)
        scaled_pixmap = QPixmap.fromImage(scaled_image)
        image_label.setPixmap(scaled_pixmap)

        text_label = QLabel(text)
        text_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #fff;")
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setCursor(Qt.PointingHandCursor)

        return image_label, text_label

    def show_statistics(self):
        with open("JSON/statistics.json", "r") as file:
            loaded_statistics = json.load(file)
        player1_number_win = loaded_statistics["player_win"].get("player1", 0)
        player2_number_win = loaded_statistics["player_win"].get("player2", 0)
        best_score_player1 = loaded_statistics["player_score"].get("player1", 0)
        best_score_player2 = loaded_statistics["player_score"].get("player2", 0)
        player1_number_win_with_computer=loaded_statistics["player_win_with_computer"].get("player1", 0)
        computer_number_win = loaded_statistics["player_win_with_computer"].get("playerCPU", 0)
        best_score_with_computer=loaded_statistics["player_with_computer_score"].get("player1", 0)
        best_score_computer=loaded_statistics["player_with_computer_score"].get("playerCPU", 0)

        self.text_label.setText(self.text_label.text()+" "+str(player1_number_win)+" : "+str(player2_number_win))
        self.text_label2.setText(self.text_label2.text() + " " +str(player1_number_win_with_computer) + " : " + str(computer_number_win))
        self.text_label3.setText(self.text_label3.text() + " " + str(best_score_player1) + " : " + str(best_score_player2))
        self.text_label4.setText(self.text_label4.text() + " " + str(best_score_with_computer)  + " : " + str(best_score_computer))

    def reset(self,event):
        confirmation = QMessageBox.question(self, 'Potwierdzenie resetowania', 'Czy na pewno chcesz usunąć statystyki?',
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            with open('JSON/statistics.json', 'r') as json_file:
                data = json.load(json_file)

            data["player_win"]["player1"] = 0
            data["player_win"]["player2"] = 0
            data["player_score"]["player1"] = 0
            data["player_score"]["player2"] = 0
            data["player_win_with_computer"]["player1"]=0
            data["player_win_with_computer"]["playerCPU"] = 0
            data["player_with_computer_score"]["player1"] = 0
            data["player_with_computer_score"]["playerCPU"] = 0

            json_data = json.dumps(data, indent=4)
            statistics_points = {"statistics_points": []}

            with open('JSON/statistics.json', 'w') as json_file:
                json_file.write(json_data)
            with open('JSON/statistics_points.json', 'w') as json_file:
                json.dump(statistics_points, json_file)
            QMessageBox.information(self, 'Informacja', 'Statystyki zostały zresetowane.')
            #self.show_statistics()
    def undo(self,event):
        widget=self.widget
        class_menu = menu.Menu(widget)
        widget.addWidget(class_menu)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    def detailed_statistics(self,event):
        widget = self.widget
        class_detailed = detailed_statistics.Detailed_statistics(widget)
        widget.addWidget(class_detailed)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    def ranking_list(self,event):
        widget = self.widget
        class_ranking = ranking_list.Ranking_list(widget)
        widget.addWidget(class_ranking)
        widget.setCurrentIndex(widget.currentIndex() + 1)