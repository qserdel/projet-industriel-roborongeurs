from PyQt5 import QtWidgets, uic
import sys

class Ui1(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui1, self).__init__()
        uic.loadUi('test3.ui', self)

        self.button = self.findChild(QtWidgets.QPushButton, 'Menu2') # Find the button
        self.button.clicked.connect(self.printButtonPressed) # Remember to pass the definition



    def printButtonPressed(self):
        Menu2.show()
        self.hide()
        print('printButtonPressed')

class Ui2(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui2, self).__init__()
        uic.loadUi('test5.ui', self)

        self.button = self.findChild(QtWidgets.QPushButton, 'Menu1') # Find the button
        self.button.clicked.connect(self.printButtonPressed) # Remember to pass the definition



    def printButtonPressed(self):
        Menu1.show()
        self.hide()
        print('printButtonPressed')


app = QtWidgets.QApplication(sys.argv)
Menu1 = Ui1()
Menu2 = Ui2()
Menu1.show()
app.exec_()
