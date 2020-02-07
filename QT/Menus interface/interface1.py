import sys
from PyQt5 import QtWidgets, uic
print("initialisation")
#La classe globale qui gère la création et la navigation pour tous les menus
class Interface(QtWidgets.QMainWindow):
    def __init__(self):
        super(Interface, self).__init__()
        uic.loadUi('mainwindow.ui', self)
        self.selector = self.findChild(QtWidgets.QStackedWidget, 'stackedWidget')
        self.menuBase = MenuBase(self)
        self.menuCreationPattern = MenuCreationPattern(self)
        self.menuSelectionPattern = MenuSelectionPattern(self)
        self.menuResultats = MenuResultats(self)
        self.RetourMenu

        #Fonction de retour au menu de base, commune à tous les menus
    def RetourMenu(self):
        print('Retour au menu de base')
        self.selector.setCurrentIndex(0)

#Le menu de base
class MenuBase():
    def __init__(self,interface):
        self.buttonAccesCreationPattern = interface.findChild(QtWidgets.QPushButton, 'accesCreationPattern')
        self.buttonAccesCreationPattern.clicked.connect(self.AccesCreationPattern)
        self.buttonAccesResultats = interface.findChild(QtWidgets.QPushButton, 'accesResultats')
        self.buttonAccesResultats.clicked.connect(self.AccesResultats)
        self.buttonAccesSelectionPattern = interface.findChild(QtWidgets.QPushButton, 'accesSelectionPattern')
        self.buttonAccesSelectionPattern.clicked.connect(self.AccesSelectionPattern)

    def AccesCreationPattern(self):
        print('Accès au menu de création de pattern')
        interface.selector.setCurrentIndex(1)
    def AccesSelectionPattern(self):
        print('Accès au menu de séléction de pattern')
        interface.selector.setCurrentIndex(2)
    def AccesResultats(self):
        print('Accès au menu des résultats')
        interface.selector.setCurrentIndex(3)

#Le menu de création de pattern
class MenuCreationPattern():
    def __init__(self,interface):
        self.buttonRetourMenu = interface.findChild(QtWidgets.QPushButton, 'retourMenuCreationPattern')
        self.buttonRetourMenu.clicked.connect(interface.RetourMenu)

#Le menu de sélection de pattern existant
class MenuSelectionPattern():
    def __init__(self,interface):
        self.buttonRetourMenu = interface.findChild(QtWidgets.QPushButton, 'retourMenuSelectionPattern')
        self.buttonRetourMenu.clicked.connect(interface.RetourMenu)

#Le menu d'affichage, d'export et de supression des résultats
class MenuResultats():
    def __init__(self,interface):
        self.buttonRetourMenu = interface.findChild(QtWidgets.QPushButton, 'retourMenuResultats')
        self.buttonRetourMenu.clicked.connect(interface.RetourMenu)



app = QtWidgets.QApplication(sys.argv)
interface = Interface()
interface.show()
app.exec_()
