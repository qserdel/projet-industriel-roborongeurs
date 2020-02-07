import sys
from PyQt5 import QtWidgets, uic

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
        self.menuRecapitulatifPattern = MenuRecapitulatifPattern(self)
        self.menuConfirmationSuppressionSerie = MenuConfirmationSuppressionSerie(self)
        self.menuConfirmationModificationPattern = MenuConfirmationModificationPattern(self)
        self.menuChoixSouris = MenuChoixSouris(self)
        self.menuConfirmationSuppressionSouris = MenuConfirmationSuppressionSouris(self)
        self.menuEssaiE1 = MenuEssaiE1(self)
        self.menuEssaiE2 = MenuEssaiE2(self)
        self.retourMenu

    #Fonction de retour au menu de base, commune à (presque) tous les menus
    def retourMenu(self):
        print('Retour au menu de base')
        self.selector.setCurrentIndex(0)

#Le menu de base
class MenuBase():
    def __init__(self,interface):
        #boutons du menu
        self.buttonAccesCreationPattern = interface.findChild(QtWidgets.QPushButton, 'accesCreationPattern')
        self.buttonAccesCreationPattern.clicked.connect(self.accesCreationPattern)
        self.buttonAccesResultats = interface.findChild(QtWidgets.QPushButton, 'accesResultats')
        self.buttonAccesResultats.clicked.connect(self.accesResultats)
        self.buttonAccesSelectionPattern = interface.findChild(QtWidgets.QPushButton, 'accesSelectionPattern')
        self.buttonAccesSelectionPattern.clicked.connect(self.accesSelectionPattern)

    def accesCreationPattern(self):
        print('Accès au menu de création de pattern')
        interface.selector.setCurrentIndex(1)
    def accesSelectionPattern(self):
        print('Accès au menu de séléction de pattern')
        interface.selector.setCurrentIndex(2)
    def accesResultats(self):
        print('Accès au menu des résultats')
        interface.selector.setCurrentIndex(3)

#Le menu de création de pattern
class MenuCreationPattern():
    def __init__(self,interface):
        #boutons du menu
        self.buttonRetourMenu = interface.findChild(QtWidgets.QPushButton, 'retourMenuCreationPattern')
        self.buttonRetourMenu.clicked.connect(interface.retourMenu)
        #entrées utilisateur
        self.cadreNom = interface.findChild(QtWidgets.QPlainTextEdit,'cadreNomPattern')
        self.cadreNombreSouris = interface.findChild(QtWidgets.QSpinBox,'cadreNombreSouris')
        self.cadreNombreJours = interface.findChild(QtWidgets.QSpinBox,'cadreNombreJours')
        self.cadreNombreEssais = interface.findChild(QtWidgets.QSpinBox,'cadreNombreEssais')
        self.cadreTempsMax = interface.findChild(QtWidgets.QTimeEdit,'cadreTempsMax')
        self.checkModeEntrainement = interface.findChild(QtWidgets.QCheckBox,'checkModeEntrainement')

#Le menu de sélection de pattern existant
class MenuSelectionPattern():
    def __init__(self,interface):
        #boutons du menu
        self.buttonRetourMenu = interface.findChild(QtWidgets.QPushButton, 'retourMenuSelectionPattern')
        self.buttonRetourMenu.clicked.connect(interface.retourMenu)
        #liste des patterns existants
        self.listePatterns = interface.findChild(QtWidgets.QListWidget,'listePatterns')

#Le menu d'affichage, d'export et de supression des résultats
class MenuResultats():
    def __init__(self,interface):
        #boutons du menu
        self.buttonRetourMenu = interface.findChild(QtWidgets.QPushButton, 'retourMenuResultats')
        self.buttonRetourMenu.clicked.connect(interface.retourMenu)
        self.buttonSupprimerSerie = interface.findChild(QtWidgets.QPushButton, 'supprimerSerie')
        self.buttonSupprimerSerie.clicked.connect(self.accesSuppressionSerie)
        #liste des séries de résultats
        self.listeSeries = interface.findChild(QtWidgets.QListWidget,'listeSeries')
        #infos de la série de résultats
        self.infoSerie = interface.findChild(QtWidgets.QTableView,'infoSerie')

    def accesSuppressionSerie(self):
        print('Accès au menu de supression d\'une série')
        interface.selector.setCurrentIndex(6)


#Le menu recapitulatif des parametres d'un pattern existant
class MenuRecapitulatifPattern():
    def __init__(self,interface):
        #boutons du menu
        self.buttonRetourMenu = interface.findChild(QtWidgets.QPushButton, 'retourMenuRecapitulatifPattern')
        self.buttonRetourMenu.clicked.connect(interface.retourMenu)
        self.buttonSelectionnerPattern = interface.findChild(QtWidgets.QPushButton, 'modifierPattern')
        self.buttonSelectionnerPattern.clicked.connect(self.accesChoixSouris)
        self.buttonModifierPattern = interface.findChild(QtWidgets.QPushButton, 'retourMenuResultats')
        self.buttonModifierPattern.clicked.connect(self.accesValidationModificationPattern)

    def accesValidationModificationPattern(self):
        print('Accès au menu de validation de modification d\'un pattern')
        interface.selector.setCurrentIndex(7)

    def accesChoixSouris(self):
        print('Accès au menu de choix d\'une souris dans un pattern')
        interface.selector.setCurrentIndex(6)

#Le menu de confirmation de supression d'un pattern existant
class MenuConfirmationSuppressionSerie():
    def __init__(self,interface):
        self.buttonSupprimer = interface.findChild(QtWidgets.QPushButton, 'validerSuppressionSerie')
        self.buttonSupprimer.clicked.connect(self.supprimer)
        self.buttonAnnuler = interface.findChild(QtWidgets.QPushButton, 'annulerSuppressionSerie')
        self.buttonAnnuler.clicked.connect(self.annuler)

    def supprimer(self):
        print('supression d\'une série')
        interface.selector.setCurrentIndex(3)

    def annuler(self):
        print('retour au menu des résultats')
        interface.selector.setCurrentIndex(3)

#Le menu de confirmation des modifications sur un pattern existant
class MenuConfirmationModificationPattern():
    def __init__(self,interface):
        self.buttonSupprimer = interface.findChild(QtWidgets.QPushButton, 'validerModificationPattern')
        self.buttonSupprimer.clicked.connect(self.modifier)
        self.buttonAnnuler = interface.findChild(QtWidgets.QPushButton, 'annulerModificationPattern')
        self.buttonAnnuler.clicked.connect(self.annuler)

    def modifier(self):
        print('modification d\'un pattern')
        interface.selector.setCurrentIndex(1)

    def annuler(self):
        print('retour au menu de sélection pattern')
        interface.selector.setCurrentIndex(2)

#Le menu du choix de la souris à exploiter
class MenuChoixSouris():
    def __init__(self,interface):
        self.buttonRetourMenu = interface.findChild(QtWidgets.QPushButton, 'retourMenuChoixSouris')
        self.buttonRetourMenu.clicked.connect(interface.retourMenu)
        self.buttonChoisirSouris = interface.findChild(QtWidgets.QPushButton, 'supprimerSouris')
        self.buttonChoisirSouris.clicked.connect(self.accesSuppressionSouris)
        self.buttonSupprimerSouris = interface.findChild(QtWidgets.QPushButton, 'choisirSouris')
        self.buttonSupprimerSouris.clicked.connect(self.accesEssaiE1)

    def accesEssaiE1(self):
        print('lancement de l\'expérience')
        interface.selector.setCurrentIndex(10)

    def accesSuppressionSouris(self):
        print('acces au menu de supression d\'une souris')
        interface.selector.setCurrentIndex(9)

#Le menu de confirmation de supression d'une souris dans un pattern
class MenuConfirmationSuppressionSouris():
    def __init__(self,interface):
        print("hey")

#Le menu de suivi de l'experience, phase à 1 pot
class MenuEssaiE1():
    def __init__(self,interface):
        print("hey")

#Le menu de suivi de l'experience, phase à 2 pots
class MenuEssaiE2():
    def __init__(self,interface):
        print("hey")


app = QtWidgets.QApplication(sys.argv)
interface = Interface()
interface.show()
app.exec_()
