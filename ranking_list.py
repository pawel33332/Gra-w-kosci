import json
import re
from PyQt5 import QtGui
import statis
import mysql.connector
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QImage, QPixmap, QColor
from PyQt5.QtWidgets import QMainWindow, QLabel, QComboBox, QLineEdit, QPushButton, QVBoxLayout, QTableWidgetItem, \
    QTableWidget, QMessageBox, QWidget, QGridLayout
from PyQt5.uic import loadUi
from datetime import datetime, date
import winreg
#from mysql.connector.locales.eng import client_error
#mysql.connector.plugins.mysql_native_password'

class Ranking_list(QMainWindow):
    def __init__(self,widget):
        super(Ranking_list, self).__init__()
        loadUi("menu.ui", self)
        self.widget = widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QGridLayout(central_widget)
        self.avg_count_points=-1
        self.setgraphicselement()
        self.conn=0
        try:
            self.conn = mysql.connector.connect(
                host='',
                user='',
                password='',
                database=''
            )
            if self.conn.is_connected():
                print("Polaczono")
                self.cursor = self.conn.cursor()
                self.calculate_points()
                current_date = date.today()
                year = str(current_date.year)
                self.show_results(self.count_combobox.currentIndex(), year)
        except mysql.connector.Error as e:
            QMessageBox.information(None, 'Bląd', 'Brak połaczenia z bazą')

    def setgraphicselement(self):
        background_label = QLabel()
        pixmap = QPixmap("graphics/background_game.png")
        scaled_pixmap = pixmap.scaled(1366, 768)
        background_label.setPixmap(scaled_pixmap)
        self.layout.addWidget(background_label, 0, 0, 9, 5)
        background_label.setScaledContents(True)
        self.update_background()

        self.text_label1 = QLabel(self)
        self.text_label1.setStyleSheet(
            "QLabel { color: rgb(255, 255, 255);font-size: 52px; font-weight: bold; }"
        )
        self.text_label1.setAlignment(Qt.AlignCenter)
        self.text_label1.setText("Lista rankingowa")
        self.text_label1.setAlignment(Qt.AlignCenter)
        self.text_label1.setToolTip("Do miesięcznej listy rankingowej zalicza się średnia z 20\nnajlepszych zdobytych wyników w danym miesiącu")
        self.layout.addWidget(self.text_label1, 0, 0, 1, 5)

        self.text_label = QLabel(self)
        self.text_label.setStyleSheet(
            "QLabel { color: rgb(255, 255, 255);font-size: 34px; font-weight: bold; }"
        )
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setText("Wyślij swój obecny rekord miesięczny: ")
        self.layout.addWidget(self.text_label, 1,0,1,5)

        self.mail = QLineEdit(self)
        self.mail.setPlaceholderText("email")
        self.layout.addWidget(self.mail, 2, 1,1,1)
        self.layout.setAlignment(self.mail, Qt.AlignCenter)

        self.nick = QLineEdit(self)
        self.nick.setPlaceholderText("nick")
        self.layout.addWidget(self.nick, 2, 2,1,1)
        self.layout.setAlignment(self.nick, Qt.AlignCenter)

        self.send_button = QPushButton('Wyślij', self)
        self.layout.addWidget(self.send_button, 2, 3,1,1)
        self.send_button.clicked.connect(self.send_record)

        self.text_label2 = QLabel(self)
        self.text_label2.setGeometry(480, 210, 700, 40)
        self.text_label2.setStyleSheet(
            "QLabel { color: rgb(255, 255, 255);font-size: 34px; font-weight: bold; }"
        )
        self.text_label2.setAlignment(Qt.AlignCenter)
        self.text_label2.setText("Wybierz miesiąc dla listy rankingowej")
        self.layout.addWidget(self.text_label2, 3,0,1,5)

        self.count_combobox = QComboBox(self)
        self.count_combobox.setGeometry(1180, 210, 300, 40)
        self.count_combobox.setStyleSheet("background-color: white;color:black;font-size:24px")
        self.count_combobox.view().setStyleSheet("background-color: white; color:black;")
        self.count_combobox.setEditable(True)
        self.count_combobox.lineEdit().setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.count_combobox, 3, 4,1,1)
        self.layout.setAlignment(self.count_combobox, Qt.AlignLeft)
        current_date = date.today()
        current_month = datetime.now().month - 1
        year = str(current_date.year)
        options = ["styczen "+year, "luty "+year,"marzec "+year,
        "kwiecien "+year, "maj "+year, "czerwiec "+year, "lipiec "+year,"sierpień "+year,
        "wrzesien "+year,"pazdziernik "+year,"listopad "+year,"grudzien "+year]
        self.count_combobox.addItems(options)
        self.count_combobox.lineEdit().setReadOnly(True)
        self.count_combobox.setCurrentIndex(current_month)
        #self.count_combobox.currentIndexChanged.connect(self.show_results)
        #self.count_combobox.currentIndexChanged.connect(lambda event: self.show_results(current_month,year))
        self.count_combobox.currentIndexChanged.connect(lambda index, combobox=self.count_combobox: self.show_results(index, year))

        self.table = QTableWidget(self)
        self.table.setRowCount(100)
        self.table.setColumnCount(3)
        self.table.verticalHeader().setVisible(False)
        self.layout.addWidget(self.table, 4, 1, 4, 3)

        for row in range(100):
            for col in range(3):
                item = QTableWidgetItem("")
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, item)
        # Ustawienie układu dla okna głównego
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, header.Stretch)
        header.setSectionResizeMode(1, header.Stretch)
        header.setSectionResizeMode(2, header.Stretch)
        header_labels = ['Numer miejsca','Nick','Śr. ilośc punktów']
        self.table.setHorizontalHeaderLabels(header_labels)
        self.table.setStyleSheet("background-color: #f0f0f0;")

        self.image_label2 = QLabel(self)
        self.image2 = QImage("graphics/button_undo.png")
        self.scaled_image2 = self.image2.scaled(self.image2.width() // 6, self.image2.height() // 6)
        self.scaled_pixmap2 = QPixmap.fromImage(self.scaled_image2)
        self.image_label2.setPixmap(self.scaled_pixmap2)
        self.image_label2.setGeometry(20, 20, self.scaled_pixmap2.width(), self.scaled_pixmap2.height())
        self.image_label2.mousePressEvent = self.undo
    def update_background(self):
        pixmap = QPixmap("background_game.png")  # Twoja grafika tła
        scaled_pixmap = pixmap.scaled(QSize(self.width(), self.height()))
        self.background_label.setPixmap(scaled_pixmap)

    def send_points(self,email,nick,month,year,machine_id,points):
        try:
            query = "SELECT id FROM Users Where email=%s"
            self.cursor.execute(query,(email,))
            result = self.cursor.fetchone()
            print(result)
            result2=None
            if result:
                print(result[0])
                query_machine_id="SELECT id FROM Users Where id=%s AND machine_id=%s"
                self.cursor.execute(query_machine_id, (result[0],machine_id))
                result2 = self.cursor.fetchone()
                if result2:
                    query_count = "SELECT point_count FROM Points Where user_id=%s AND month=%s AND year=%s"
                    self.cursor.execute(query_count, (result[0], month, year))
                    result3 = self.cursor.fetchone()
                    if result3:
                        query_update = "UPDATE Points SET point_count = %s WHERE user_id = %s " \
                                       "AND month = %s AND year = %s AND point_count < %s"
                        self.cursor.execute(query_update, (points, result[0], month, year,points))
                        self.conn.commit()
                        QMessageBox.information(None, 'Informacja', 'Pomyślnie wysłano wynik')
                    else:
                        query_add = "INSERT INTO Points(user_id,month,year,point_count) VALUES (%s, %s, %s, %s)"
                        self.cursor.execute(query_add, (result[0], month, year, points))
                        self.conn.commit()
                        QMessageBox.information(None, 'Informacja', 'Pomyślnie wysłano wynik')
                else:
                    QMessageBox.information(None, 'Bląd', 'Podane dane są przypisane do innego urządzenia.')
            else:
                machine = machine_id
                list_machine = [machine]
                print(list_machine)
                query_machine_id="SELECT id FROM Users Where machine_id=%s"
                self.cursor.execute(query_machine_id, list_machine)
                result4 = self.cursor.fetchone()
                if result4:
                    QMessageBox.information(None, 'Błąd', 'Nie można dodać użytkownika. Podane dane '
                                                                  'są przypisane do innego urządzenia.')
                else:
                    query_mail_nick="SELECT id FROM Users Where email=%s OR nickname=%s"
                    self.cursor.execute(query_mail_nick, (email,nick))
                    result5 = self.cursor.fetchone()
                    if result5:
                        QMessageBox.information(None, 'Błąd', 'Podany email lub nick już istnieje w bazie.')
                    else:
                        query_add="INSERT INTO Users (nickname, email,machine_id) VALUES (%s, %s, %s)"
                        machine=machine_id
                        list_machine=[machine]
                        self.cursor.execute(query_add, (nick,email,machine_id))
                        self.conn.commit()
                        self.send_points(email, nick, month, year,machine_id,self.avg_count_points)
                        #QMessageBox.information(None, 'Informacja', 'Pomyslnie utworzono konto i wysłano wynik')
        except mysql.connector.Error as err:
            print(f"Błąd MySQL: {err}")
    def calculate_points(self):
        # Aktualna data i czas
        with open("JSON/statistics_points.json", "r") as file:
            statistics_points = json.load(file)
        current_datetime = date.today()
        print(current_datetime.month)

        # Wybór tylko tych rekordów z obecnego miesiąca i roku
        current_month=[]
        if len(statistics_points)<2:
            QMessageBox.information(None, 'Brak wyników', 'Nie ma wystarczającej liczby wyników w tym miesiącu.'
                                                          ' Musisz zgromadzić co najmniej 20 wyników')
            return
        for record in statistics_points["statistics_points"]:
            if datetime.strptime(record["date"],'%Y-%m-%d').month ==\
            current_datetime.month and datetime.strptime(record["date"],'%Y-%m-%d').year == current_datetime.year:
                current_month.append(record['points'])
        if len(current_month) >= 20:
            sorted_records = sorted(current_month, reverse=True)
            top_20_records = sorted_records[:20]
            average_points = round((sum(top_20_records) / len(top_20_records)),2)
            self.avg_count_points=average_points
            self.text_label.setText("Wyślij swój obecny rekord miesięczny: "+str(average_points)+" pkt.")
        else:
            QMessageBox.information(None, 'Brak wyników', 'Nie ma wystarczającej liczby wyników w tym miesiącu.'
                                                          ' Musisz zgromadzić co najmniej 20 wyników')
            return
    def send_record(self):
        if self.conn==0:
            return
        email = self.mail.text()
        nick = self.nick.text()
        registry = winreg.HKEY_LOCAL_MACHINE
        address = 'SOFTWARE\\Microsoft\\Cryptography'
        keyargs = winreg.KEY_READ | winreg.KEY_WOW64_64KEY
        key = winreg.OpenKey(registry, address, 0, keyargs)
        value = winreg.QueryValueEx(key, 'MachineGuid')
        winreg.CloseKey(key)
        unique_id = value[0]
        email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
        if email_pattern.match(email):
            if len(nick) < 4:
                QMessageBox.warning(self, 'Walidacja Nicku', 'Nick musi zawierać co najmniej 4 litery.')
                return
            else:
                print(email)
                print(self.avg_count_points)
                if self.avg_count_points==-1:
                    QMessageBox.information(None, 'Brak wyników', 'Nie ma wystarczającej liczby wyników w tym miesiącu.'
                                                                  ' Musisz zgromadzić co najmniej 20 wyników')
                else:
                    current_datetime = date.today()
                    month=current_datetime.month
                    year=current_datetime.year
                    self.send_points(email,nick,month,year,unique_id,self.avg_count_points)
        else:
            QMessageBox.warning(self, 'Walidacja E-mail', 'Adres e-mail jest niepoprawny.')
            return
        print("send")
    def show_results(self,month,year):
        if self.conn==0:
            return
        self.table.clearContents()
        month=int(month)+1
        year=int(year)
        query_results = "SELECT u.nickname,p.point_count FROM Points AS p JOIN Users AS u ON p.user_id=u.id " \
                        "WHERE p.month=%s AND p.year=%s ORDER BY p.point_count DESC LIMIT 100"
        self.cursor.execute(query_results,(month,year))
        results_points = self.cursor.fetchall()
        if results_points:
            results_with_rank = []
            rank = 1
            prev_value = None
            for index, (name, value) in enumerate(results_points):
                if value != prev_value:
                    rank = index + 1
                results_with_rank.append((rank, name, value))
                prev_value = value

            for row_index, (number,name, value) in enumerate(results_with_rank):
                item_number = QTableWidgetItem(str(number))
                item_number.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_index, 0, item_number)

                item_name = QTableWidgetItem(name)
                item_name.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_index, 1, item_name)

                item_value = QTableWidgetItem(str(value))
                item_value.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_index, 2, item_value)

                if number==1:
                    item_number.setBackground(QtGui.QColor('gold'))
                    item_name.setBackground(QtGui.QColor('gold'))
                    item_value.setBackground(QtGui.QColor('gold'))
                elif number==2:
                    item_number.setBackground(QtGui.QColor('silver'))
                    item_name.setBackground(QtGui.QColor('silver'))
                    item_value.setBackground(QtGui.QColor('silver'))
                elif number==3:
                    item_number.setBackground(QtGui.QColor('brown'))
                    item_name.setBackground(QtGui.QColor('brown'))
                    item_value.setBackground(QtGui.QColor('brown'))
    def undo(self,event):
        widget=self.widget
        class_statistics = statis.Statis(widget)
        widget.addWidget(class_statistics)
        widget.setCurrentIndex(widget.currentIndex() + 1)