import datetime
import json
from PyQt5.QtChart import QChart, QLineSeries, QChartView, QScatterSeries
from PyQt5.QtWidgets import QLabel, QComboBox, QVBoxLayout, QProgressBar, QGridLayout, QWidget
from PyQt5.QtGui import QPainter, QPen, QFont, QImage, QPixmap
from PyQt5.QtCore import Qt, QSize
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow
from numpy import mean

import statis


class Detailed_statistics(QMainWindow):
    def __init__(self,widget):
        super(Detailed_statistics, self).__init__()
        loadUi("menu.ui", self)
        self.widget = widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QGridLayout(central_widget)
        self.date = datetime.date.today()
        with open('JSON/statistics_points.json') as f:
            data = json.load(f)['statistics_points']
        number_of_documents = len(data)
        if number_of_documents>1:
            self.setgraphicselement()
            self.date = datetime.date.today()
            self.linear_chart()
            self.regression_chart_points()
            self.count_wins()
        else:
            self.text_label1 = QLabel(self)
            self.text_label1.setStyleSheet(
                "QLabel { color: rgb(255, 0, 0);font-size: 52px; font-weight: bold; }"
            )
            self.text_label1.setAlignment(Qt.AlignCenter)
            self.text_label1.setText("Musisz rozegrać co najmniej 2 pojedynki")
            self.layout.addWidget(self.text_label1, 0, 4)

            self.image_label2 = QLabel(self)
            self.image2 = QImage("graphics/button_undo.png")
            self.scaled_image2 = self.image2.scaled(self.image2.width() // 6, self.image2.height() // 6)
            self.scaled_pixmap2 = QPixmap.fromImage(self.scaled_image2)
            self.image_label2.setPixmap(self.scaled_pixmap2)
            self.image_label2.setGeometry(20, 20, self.scaled_pixmap2.width(), self.scaled_pixmap2.height())
            self.image_label2.mousePressEvent = self.undo

    def setgraphicselement(self):
        background_label = QLabel()
        pixmap = QPixmap("graphics/background_game.png")
        scaled_pixmap = pixmap.scaled(1366, 768)
        background_label.setPixmap(scaled_pixmap)
        self.layout.addWidget(background_label, 0, 0, 9, 7)
        background_label.setScaledContents(True)
        #self.update_background()

        self.text_label1 = QLabel(self)
        self.text_label1.setStyleSheet(
            "QLabel { color: rgb(255, 255, 255);font-size: 52px; font-weight: bold; }"
        )
        self.text_label1.setAlignment(Qt.AlignCenter)
        self.text_label1.setText("Szczegółowe statystyki")
        self.layout.addWidget(self.text_label1, 0, 0,1,7)
        self.layout.setAlignment(self.text_label1, Qt.AlignCenter)

        self.text_label2 = QLabel(self)
        self.text_label2.setStyleSheet(
            "QLabel { color: rgb(255, 255, 255);font-weight:bold; }"
        )
        #self.text_label2.setAlignment(Qt.AlignCenter)
        self.text_label2.setText("Wybierz ilość ostatnich pojedynków")
        self.layout.addWidget(self.text_label2, 1, 2,1,1)

        self.text_label3 = QLabel(self)
        self.text_label3.setStyleSheet(
            "QLabel { color: rgb(255, 255, 255);font-weight:bold; }"
        )
        self.text_label3.setAlignment(Qt.AlignCenter)
        self.text_label3.setText("Średnia ilość punktów: ")
        self.text_label3.setMaximumWidth(640)
        self.layout.addWidget(self.text_label3, 2, 4, 2, 1)
        self.layout.setAlignment(self.text_label3, Qt.AlignCenter)

        self.text_label3_2 = QLabel(self)
        self.text_label3_2.setStyleSheet(
            "QLabel { color: rgb(255, 255, 255);font-weight:bold;}"
        )
        self.text_label3_2.setAlignment(Qt.AlignCenter)
        self.text_label3_2.setText("Średnia ilosć w poprzednich pojedynkach: ")
        self.text_label3_2.setMaximumWidth(640)
        self.layout.addWidget(self.text_label3_2, 3, 4, 2, 1)
        self.layout.setAlignment(self.text_label3_2, Qt.AlignCenter)



        self.text_label5 = QLabel(self)
        self.text_label5.setStyleSheet(
            "QLabel { color: rgb(255, 255, 255);font-weight:bold;}"
        )
        self.text_label5.setAlignment(Qt.AlignCenter)
        self.text_label5.setText("% wygranych\n pojedynków z CPU")
        self.text_label5.setMaximumWidth(640)
        #self.text_label5.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.addWidget(self.text_label5, 5, 4, 3, 1)
        #self.layout.setAlignment(self.text_label5, Qt.AlignCenter)

        self.count_combobox = QComboBox(self)
        self.count_combobox.setStyleSheet("background-color: white;color:black;font-size:24px")
        self.count_combobox.view().setStyleSheet("background-color: white; color:black;")
        self.count_combobox.setEditable(True)
        self.count_combobox.lineEdit().setAlignment(Qt.AlignCenter)
        options = ["10", "20", "30", "40", "50", "75", "100"]
        self.count_combobox.addItems(options)
        self.count_combobox.lineEdit().setReadOnly(True)
        self.count_combobox.currentIndexChanged.connect(self.view_charts)
        self.layout.addWidget(self.count_combobox, 1, 3,1,1)
        self.layout.setAlignment(self.count_combobox, Qt.AlignRight)

        self.wykres_liniowy = QLabel(self)
        self.layout.addWidget(self.wykres_liniowy, 2, 0, 2, 4)

        self.regression_chart =  QLabel(self)
        self.layout.addWidget(self.regression_chart, 5, 0, 2, 4)

        self.wins_bar = QProgressBar(self)
        self.wins_bar.setTextVisible(False)
        self.wins_bar.setValue(50)
        self.wins_bar.setMaximumWidth(300)
        self.wins_bar.setMinimumWidth(300)
        self.layout.addWidget(self.wins_bar, 5, 4,2,1)
        self.layout.setAlignment(self.wins_bar, Qt.AlignCenter)

        self.image_label2 = QLabel(self)
        self.image2 = QImage("graphics/button_undo.png")
        self.scaled_image2 = self.image2.scaled(self.image2.width() // 6, self.image2.height() // 6)
        self.scaled_pixmap2 = QPixmap.fromImage(self.scaled_image2)
        self.image_label2.setPixmap(self.scaled_pixmap2)
        self.image_label2.setGeometry(20, 20, self.scaled_pixmap2.width(), self.scaled_pixmap2.height())
        self.image_label2.mousePressEvent = self.undo

    def view_charts(self):
        self.linear_chart()
        self.regression_chart_points()
        self.count_wins()
    def update_background(self):
        pixmap = QPixmap("background_game.png")  # Twoja grafika tła
        scaled_pixmap = pixmap.scaled(QSize(self.width(), self.height()))
        self.background_label.setPixmap(scaled_pixmap)
    def save_statistics_points(self,points,win):
        with open("JSON/statistics_points.json", "r") as file:
            statistics_points = json.load(file)
        if win==1:
            win=True
        else:
            win=False
        new_data = {
            "date": str(self.date),
            "points": points,
            "win": win
        }
        statistics_points["statistics_points"].append(new_data)
        with open('JSON/statistics_points.json', 'w') as f:
            json.dump(statistics_points, f, indent=4)
    def calculate_regression(self,x, y):
        n = len(x)
        sum_x = sum_y = sum_xy = sum_x_squared = 0

        for i in range(n):
            sum_x += x[i]
            sum_y += y[i]
            sum_xy += x[i] * y[i]
            sum_x_squared += x[i] * x[i]

        a = (n * sum_xy - sum_x * sum_y) / (n * sum_x_squared - sum_x * sum_x)
        b = (sum_y - a * sum_x) / n

        return a, b
    def linear_chart(self):
        self.wykres_liniowy.deleteLater()
        self.wykres_liniowy = QLabel(self)
        self.layout.addWidget(self.wykres_liniowy, 2, 0, 3, 3)
        self.wykres_liniowy.setMinimumHeight(200)
        label_layout2 = QVBoxLayout()

        with open('JSON/statistics_points.json') as f:
            data = json.load(f)['statistics_points']
        points = [(entry['points']) for entry in data]
        a=len(points)
        index = int(self.count_combobox.currentText())
        if a-index>0:
            b=(a-index)
        else:
            b=0
        chart = QChart()
        chart.setTitle('Wykres zdobywanych punktów w ostatnich rozgrywkach')
        series = QLineSeries()
        if b-index<=0:
            history_b=0
        else:
            history_b=(b-index)-1
        avg_points=int(mean(points[b:a]))
        self.text_label3.setToolTip("Średnia liczona jest z " + str(int(a - b)) + " ostatnich pojedynków")
        self.text_label3_2.setToolTip("Średnia liczona jest z "+str(int(a-b))+" poprzednich pojedynków")
        if b!=0:
            if b - index >= 0:
                avg_points_history = int(mean(points[history_b:b]))
                self.text_label3_2.setText("<br><br><span style='font-size:30px'>Średnia ilość w poprzednich pojedynkach:</span><span style='font-size:48px'><br> " + str(avg_points_history)+"</span>")
                self.text_label3_2.setTextFormat(Qt.RichText)
                roznica=(avg_points-avg_points_history)/avg_points_history*100
                if roznica>=0:
                    str_roznica="<span style='font-size:30px'>Wzrost średniej ilości punktów:</span><span style='font-size:48px'><br>"
                else:
                    str_roznica = "<span style='font-size:30px'>Spadek średniej ilości punktów:</span><span style='font-size:48px'><br>"
                str_roznica+=str(abs(round(roznica, 2)))
                #self.text_label3.setText("Średnia ilość punktów:\n " + str(avg_points)+"\n"+str_roznica+"%)")
                self.text_label3.setText(
                    "<span style='font-size:30px'>Średnia ilość punktów:</span><span style='font-size:48px'><br>" + str(avg_points) + "</span><br><span style='font-size:30px'>"+str_roznica+"%</span><br>")
                # Ustawienie formatowania HTML
                self.text_label3.setTextFormat(Qt.RichText)
            else:
                self.text_label3_2.setText("<span style='font-size:30px'>Średnia ilość w poprzednich pojedynkach:<br></span><span style='font-size:48px'> brak danych</span>")
                self.text_label3.setText(
                    "<span style='font-size:30px'>Średnia ilość punktów:</span><span style='font-size:48px'><br>" + str(avg_points) + "</span><br>")
                self.text_label3.setTextFormat(Qt.RichText)
        else:
            self.text_label3_2.setText("<span style='font-size:30px'>Średnia ilość w poprzednich pojedynkach:<br></span><span style='font-size:48px'> brak danych</span>")
            self.text_label3.setText(
                "Średnia ilość punktów:<span style='font-size:48px'><br>" + str(avg_points) + "</span>")
            self.text_label3.setTextFormat(Qt.RichText)
        print(avg_points)


        for i, point_value in enumerate(points[b:a]):
            series.append(i+1, point_value)
        chart.addSeries(series)
        chart.createDefaultAxes()
        axis_x = chart.axisX()
        axis_y = chart.axisY()
        axis_x.setLabelsFont(QFont("Arial", 12))
        axis_x.setLabelFormat("%d")
        axis_y.setLabelsFont(QFont("Arial", 12))

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        font = QFont("Arial", 12)
        chart_view.setFont(font)

        label_layout2.addWidget(chart_view)
        self.wykres_liniowy.setLayout(label_layout2)
        self.wykres_liniowy.show()

    def regression_chart_points(self):
        self.regression_chart.deleteLater()
        self.regression_chart = QLabel(self)
        self.regression_chart.setMinimumHeight(280)
        self.layout.addWidget(self.regression_chart, 5, 0, 3, 3)


        label_layout3 = QVBoxLayout()
        with open('JSON/statistics_points.json') as f:
            data = json.load(f)['statistics_points']

        # Przygotowanie danych do analizy
        points = [(entry['points']) for entry in data]
        x_values, y_values = zip(*[(i+1, entry['points']) for i, entry in enumerate(data)])
        a_ = len(points)
        index = int(self.count_combobox.currentText())
        if a_ - index > 0:
            b_ = (a_ - index)
        else:
            b_ = 0
        a,b=self.calculate_regression(x_values[b_:a_], y_values[b_:a_])
        regression_line = [a * x + b for x in x_values[b_:a_]]
        chart = QChart()
        chart.setTitle('Regresja liniowa zdobywanych punktów')
        series = QScatterSeries()
        for i, point_value in enumerate(points[b_:a_]):
            series.append(i+1, point_value)
        regression_series = QLineSeries()
        for i in range(len(points[b_:a_])):
            regression_series.append(x_values[i], regression_line[i])
        pen = QPen()
        if regression_line[-1] > regression_line[0]:
            pen = QPen(Qt.green)  # Linia idzie w górę - kolor zielony
        elif regression_line[-1] < regression_line[0]:
            pen = QPen(Qt.red)
        else:
            pen = QPen(Qt.white)
        pen.setWidth(4)
        #pen.setColor(Qt.red)
        if y_values[0] != 0:
            # Obliczanie spadku w procentach
            difference = regression_line[-1] - regression_line[0]
            percent_drop = (difference / regression_line[0]) * 100

        #self.text_label4.setText(text+str(abs(round(percent_drop,2)))+"%")
        regression_series.setPen(pen)
        chart.addSeries(series)
        chart.addSeries(regression_series)
        chart.createDefaultAxes()
        axis_x = chart.axisX()
        axis_y = chart.axisY()
        axis_x.setLabelsFont(QFont("Arial", 12))
        axis_x.setLabelFormat("%d")
        axis_y.setLabelsFont(QFont("Arial", 12))
        axis_y.setVisible(False)
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        label_layout3.addWidget(chart_view)
        self.regression_chart.setLayout(label_layout3)
        self.regression_chart.show()

    def count_wins(self):
        with open('JSON/statistics_points.json') as f:
            data = json.load(f)['statistics_points']
        wins = [(entry['win']) for entry in data]
        a_ = len(wins)
        index = int(self.count_combobox.currentText())
        if a_ - index > 0:
            b_ = (a_ - index) - 1
        else:
            b_ = 0
        sum_wins=sum(wins[b_:a_])
        division=50
        if a_-b_-1!=0:
            division=round((sum_wins/(a_-b_-1))*100,2)
        self.wins_bar.setValue(int(division))
        self.text_label5.setText("<span style='font-size:30px'>Procent wygranych pojedynków z CPU:<br></span><span style='font-size:48px'><br>"+str(division)+"%<br></span>")
        self.text_label5.setTextFormat(Qt.RichText)
        b_history = 0
        if b_ != 0:
            if b_-index>=0:
                b_history = b_-index
                sum_wins_history = sum(wins[b_history:b_])
                #percent_history = round((sum_wins / b_history) * 100, 2)
                roznica = abs(round(((sum_wins-sum_wins_history) / sum_wins_history * 100),2))
                text = self.text_label5.text()
                if roznica >= 0:
                    str_roznica = "<span style='font-size:30px'>Wzrost w porównaniu z poprz. okresem:<br><span style='font-size:48px'>"
                else:
                    str_roznica = "<span style='font-size:30px'>Spadek w porównaniu z poprz. okresem:<br><span style='font-size:48px'>"
                self.text_label5.setText(text + str_roznica+str(roznica)+"%</span>")
            else:
                text = self.text_label5.text()
                self.text_label5.setText(text + "<span style='font-size:30px'>Wzrost/Spadek:<br></span><span style='font-size:48px'>brak danych</span>")
        else:
            text = self.text_label5.text()
            self.text_label5.setText(
                text + "<span style='font-size:30px'>Wzrost/Spadek:<br></span><span style='font-size:48px'>brak danych</span>")
    def undo(self,event):
        widget=self.widget
        class_statistics = statis.Statis(widget)
        widget.addWidget(class_statistics)
        widget.setCurrentIndex(widget.currentIndex() + 1)