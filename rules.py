from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import  Qt, QSize
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.uic import loadUi
import menu

class Rules(QMainWindow):
    def __init__(self,widget):
       super(Rules, self).__init__()
       loadUi("menu.ui", self)
       self.setgraphicselement()
       self.widget=widget
    def setgraphicselement(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QGridLayout(central_widget)

        background_label = QLabel()
        pixmap = QPixmap("graphics/background.png")
        scaled_pixmap = pixmap.scaled(1366, 768)
        background_label.setPixmap(scaled_pixmap)
        layout.addWidget(background_label, 0, 0, 9, 7)
        background_label.setScaledContents(True)
        self.update_background()

        rules_textedit = QTextEdit()
        rules_textedit.setReadOnly(True)
        #rules_textedit.setAlignment(Qt.AlignCenter)
        rules_textedit.setAlignment(Qt.AlignJustify)
        rules_textedit.setStyleSheet(
            "QTextEdit { background-color: #ff9; border: 8px solid #808080; border-radius: 8px; border-color:#500000 }"
        )
        rules_textedit.setLineWrapMode(QTextEdit.WidgetWidth)
        rules_textedit.setFontPointSize(13)
        rules_textedit.setText(
                "1. W każdej z 13 kolejek każdy z graczy ma do dyspozycji trzy rzuty kostkami."
                " Pierwszy z nich odbywa się zawsze wszystkimi pięcioma kostkami, a w drugim"
                " oraz trzecim, które nie są obowiązkowe, wybrane kostki mogą zostać zatrzymane."
                " Rzut odbywa się wtedy tylko kośćmi nieoznaczonymi."
                
                "\n\n2. Po wykonaniu rzutów układ oczek uzyskany na kostkach musi zostać zapisany"
                " przez gracza w tabeli punktacji do jednej z 13 kategorii. Raz wybrana kategoria"
                " nie może być później ponownie wybrana."

                "\n\n3. Kategorie z górnej części tabeli: Wybierając jedną z nich, komputer wpisuje w pozycji"
                " odpowiadającej tej kategorii sumę oczek z kostek wskazujących wybraną liczbę. Jeśli w górnych"
                " kategoriach tabeli uzyska się razem 63 pkt. lub więcej, to dodatkowo otrzymuje się"
                " premię w wysokości 35 pkt."
                "\n\n4. Kategorie dolnej części tabeli: trzy jednakowe, cztery jednakowe - suma oczek z wszystkich"
                " kostek; full - trzy jednakowe liczby oczek  oraz dwie inne jednakowe; mały strit - jeśli występują"
                " cztery kolejne liczby oczek;  duży strit - liczby oczek  z wszystkich kostek są  kolejnymi"
                " liczbami;generał - pięć jednakowych kostek; szansa - suma oczek z wszystkich kostek."
                "\n\n5. Drugi, trzeci i każdy kolejny wyrzucony generał może zostać użyty jako dżoker, jeśli kategoria"
                " generał i kategoria z górnej części tabeli odpowiadająca danemu generałowi są już wykorzystane."
                " Dżokera zapisuje się w dolnych kategoriach tabeli punktacji, otrzymując stosowną liczbę punktów"
                " (tzn. 25 pkt. za fula, 30 pkt za małego strita, 40 pkt. za dużego lub sumę oczek za pozostałe),"
                " chyba że wszystkie dolne kategorie są już wykorzystane, wtedy trzeba go zapisać do jednej z górnych."
                " Poza możliwością użycia jako dżokerów za kolejnych wyrzuconych generałów otrzymuje się 100 pkt. premii,"
                " ale pod warunkiem, że pierwszy został zapisany do kategorii generał."
                "\n\n6. Koniec gry następuje po zakończeniu wszystkich 13 kolejek, kiedy wszystkie kategorie tabeli"
                " punktacji są wypełnione. Wygrywa gracz, który zdobył najwięcej punktów (suma z górnej"
                " i dolnej części tabeli)."
                "\n\n7. Każdy gracz ma określony limit czasu, na zaznaczenie 13 kategorii w swojej karcie wyników."
                " Przekroczenie tego limitu skutkuje automatycznym zwycięstwem przeciwnika."

        )
        layout.addWidget(rules_textedit,3,2,5,3)


        image_label6 = QLabel(self)
        image6 = QImage("graphics/button_undo.png")
        scaled_image6 = image6.scaled(image6.width() // 6, image6.height() // 6)
        scaled_pixmap6 = QPixmap.fromImage(scaled_image6)
        image_label6.setPixmap(scaled_pixmap6)
        image_label6.setGeometry(20, 20, scaled_pixmap6.width(), scaled_pixmap6.height())
        image_label6.mousePressEvent = self.undo
    def update_background(self):
        pixmap = QPixmap("background_image.png")  # Twoja grafika tła
        scaled_pixmap = pixmap.scaled(QSize(self.width(), self.height()))
        self.background_label.setPixmap(scaled_pixmap)
    def undo(self,event):
        widget=self.widget
        class_menu = menu.Menu(widget)
        widget.addWidget(class_menu)
        widget.setCurrentIndex(widget.currentIndex() + 1)



