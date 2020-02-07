import sys
from PyQt5 import QtWidgets, uic

class Interface(QtWidgets.QMainWindow):
    def __init__(self):
        super(Interface, self).__init__()
        uic.loadUi('test6Main.ui', self)
        self.selector = self.findChild(QtWidgets.QStackedWidget, 'stackedWidget')

        self.button1 = self.findChild(QtWidgets.QPushButton, 'pushButton1')
        self.button1.clicked.connect(self.pushButton1Pressed)
        self.button2 = self.findChild(QtWidgets.QPushButton, 'pushButton2')
        self.button2.clicked.connect(self.pushButton2Pressed)

    def pushButton1Pressed(self):
        print('pushButton1Pressed')
        self.selector.setCurrentIndex(1)
    def pushButton2Pressed(self):
        print('pushButton2Pressed')
        self.selector.setCurrentIndex(0)

app = QtWidgets.QApplication(sys.argv)
interface = Interface()
interface.show()
app.exec_()
