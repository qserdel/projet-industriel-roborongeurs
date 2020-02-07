from PyQt5 import QtWidgets, uic
import sys

class Ui1(QtWidgets.QWidget):
    widget1=None
    widget2=None
    def __init__(self):
        super(Ui1, self).__init__()
        uic.loadUi('test6Widget1.ui', self)
        self.button = self.findChild(QtWidgets.QPushButton, 'Button1') # Find the button
        self.button.clicked.connect(self.Button1Pressed)

    def Button1Pressed(self):
        uic.loadUi('test6Widget2.ui', self.widget2)
        print('Button1Pressed')
        self.button = self.findChild(QtWidgets.QPushButton, 'Button2') # Find the button
        self.button.clicked.connect(self.Button2Pressed)

    def Button2Pressed(self):
        uic.loadUi('test6Widget1.ui', self.widget1)
        self.button = self.findChild(QtWidgets.QPushButton, 'Button1') # Find the button
        self.button.clicked.connect(self.Button1Pressed)
        print('Button2Pressed')

app = QtWidgets.QApplication(sys.argv)
mainwindow = Ui1()
mainwindow.show()
app.exec_()
