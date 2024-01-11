import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QGuiApplication

import menu
class Main(QMainWindow):
    def __init__(self):
        super(Main,self).__init__()
if __name__ == "__main__":
    app=QApplication(sys.argv)
    app.setApplicationName('Kości')

    font = app.font()
    font.setPointSize(18)
    app.setFont(font)

    palette = app.palette()
    palette.setColor(palette.WindowText, QColor(160,160,160))
    app.setPalette(palette)
    widget = QtWidgets.QStackedWidget()

    mainwindow = menu.Menu(widget)
    mainwindow.showFullScreen()
    widget.addWidget(mainwindow)
    screen = QGuiApplication.primaryScreen()
    screen_size = screen.size()
    widget.resize(screen_size*0.90)
    widget.setMinimumSize(1440,900)
    widget.setMaximumSize(2560,1440)

    widget.show()
    app.exec_()


