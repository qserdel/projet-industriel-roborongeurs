from PyQt5 import QtWidgets, uic
import sys

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('test2.ui', self)

        self.button = self.findChild(QtWidgets.QPushButton, 'b1') # Find the button
        self.button.clicked.connect(self.printButtonPressed) # Remember to pass the definition

        self.show()

    def printButtonPressed(self):
        # This is executed when the button is pressed
        print('printButtonPressed')


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
