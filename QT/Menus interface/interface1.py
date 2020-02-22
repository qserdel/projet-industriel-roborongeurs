import sys
from PyQt5 import QtWidgets, uic
from gestionStockage import *
#variables globales pour faciliter la navigation entre les menus
Base = 0
CreationPattern = 1
SelectionPattern = 2
Resultats = 3
RecapitulatifPattern = 4
ConfirmationSuppressionSerie = 5
ConfirmationModificationPattern = 6
ChoixSouris = 7
ConfirmationSupressionSouris = 8
EssaiE1 = 9
EssaiE2 = 10
ConfirmationArreterExperience = 11
PlacementPots = 12

#La classe globale qui gère la création et la navigation pour tous les menus
class Interface(QtWidgets.QMainWindow):
    def __init__(self):
        super(Interface, self).__init__()
        self.dictPatterns=loadAllPatterns()
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
        self.menuConfirmationArreterExperience = MenuConfirmationArreterExperience(self)
        #tous les patterns déjà créés
        self.retourMenu()

    #Fonction de retour au menu de base, commune à (presque) tous les menus
    def retourMenu(self):
        print('Retour au menu de base')
        self.selector.setCurrentIndex(Base)

    #mets à jour tous les patterns
    def updatePatterns(self):
        self.dictPatterns=loadAllPatterns()

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
        interface.menuCreationPattern.clearAll()
        print('Accès au menu de création de pattern')
        interface.selector.setCurrentIndex(CreationPattern)
    def accesSelectionPattern(self):
        print('Accès au menu de séléction de pattern')
        interface.selector.setCurrentIndex(SelectionPattern)
        interface.menuSelectionPattern.afficherListePattern(interface)
    def accesResultats(self):
        print('Accès au menu des résultats')
        interface.selector.setCurrentIndex(Resultats)

#Le menu de création de pattern
class MenuCreationPattern():
    def __init__(self,interface):
        #boutons du menu
        self.buttonRetourMenu = interface.findChild(QtWidgets.QPushButton, 'retourMenuCreationPattern')
        self.buttonRetourMenu.clicked.connect(interface.retourMenu)
        self.buttonValiderCreationPattern = interface.findChild(QtWidgets.QPushButton, 'validerCreationPattern')
        self.buttonValiderCreationPattern.clicked.connect(self.creerPattern)
        #entrées utilisateur
        self.cadreNom = interface.findChild(QtWidgets.QPlainTextEdit,'cadreNomPattern')
        self.cadreNombreSouris = interface.findChild(QtWidgets.QSpinBox,'cadreNombreSouris')
        self.cadreNombreJours = interface.findChild(QtWidgets.QSpinBox,'cadreNombreJours')
        self.cadreNombreEssais = interface.findChild(QtWidgets.QSpinBox,'cadreNombreEssais')
        self.cadreTempsMax = interface.findChild(QtWidgets.QTimeEdit,'cadreTempsMax')
        self.checkModeEntrainement = interface.findChild(QtWidgets.QCheckBox,'checkModeEntrainement')

    def creerPattern(self):
        #méthode partiellement fonctionnelle à teminer
        nom=self.cadreNom.toPlainText()
        nbSouris=self.cadreNombreSouris.value()
        nbJours=self.cadreNombreJours.value()
        nbJours=self.cadreNombreJours.value()
        #nbEssais=self.cadreNombreEssais.value #à mettre quand j'aurais géré la création auto de tableau
        nbEssais=2
        tempsMax=self.cadreTempsMax.time().toString("hh:mm") #l'affichage donne hh:mm mais on s'en sert comme mm:ss
        entrainement=self.checkModeEntrainement.isChecked()
        #ajouter la gestion du tableau de placement
        if(entrainement):
            placementPots=[[0],[0]]
        else:
            placementPots=[[0,1],[0,1]]
        pattern=Pattern(nom,nbSouris,nbJours,nbEssais,entrainement,tempsMax,placementPots)
        savePattern(pattern)
        print(pattern.affichage())
        interface.updatePatterns()
        interface.retourMenu()

    #vide toutes les cases de ce menu
    def clearAll(self):
        self.cadreNom.clear()
        self.cadreNombreSouris.setValue(0)
        self.cadreNombreJours.setValue(0)
        self.cadreNombreEssais.setValue(0)
        self.cadreTempsMax.clear()
        self.checkModeEntrainement.setChecked(False)

#Le menu de sélection de pattern existant
class MenuSelectionPattern():
    def __init__(self,interface):
        #boutons du menu
        self.buttonRetourMenu = interface.findChild(QtWidgets.QPushButton, 'retourMenuSelectionPattern')
        self.buttonRetourMenu.clicked.connect(interface.retourMenu)
        self.buttonSelectionnerPattern = interface.findChild(QtWidgets.QPushButton, 'selectionnerPattern')
        self.buttonSelectionnerPattern.clicked.connect(self.selectionnerPattern)
        self.buttonSupprimerPattern = interface.findChild(QtWidgets.QPushButton, 'supprimerPattern')
        self.buttonSupprimerPattern.clicked.connect(self.accesSuppressionPattern)
        #liste des patterns existants
        self.listePatterns = interface.findChild(QtWidgets.QComboBox,'listePattern')
        #infos du pattern sélectionné
        self.infoPattern = interface.findChild(QtWidgets.QLabel, 'infoPattern')
        #affichage de la liste des patterns enregistrés et des infos du pattern selectionné
        self.afficherListePattern(interface)
        self.listePatterns.currentIndexChanged.connect(self.afficherInfoPattern)


    def selectionnerPattern(self):
        nomPattern=self.listePatterns.currentText()
        print('Accès au menu de choix d\'une souris')
        interface.selector.setCurrentIndex(ChoixSouris)

    def accesSuppressionPattern(self):
        print('Acces au menu de supression de pattern/série')
        interface.selector.setCurrentIndex(ConfirmationSuppressionSerie)

    def afficherListePattern(self,interface):
        self.listePatterns.clear()
        for nomPattern in interface.dictPatterns:
            self.listePatterns.addItem(interface.dictPatterns[nomPattern].nom)

    def afficherInfoPattern(self):
        pattern=interface.dictPatterns[self.listePatterns.currentText()+".json"]
        self.infoPattern.setText(pattern.affichage())


#Le menu d'affichage, d'export et de supression des résultats
class MenuResultats():
    def __init__(self,interface):
        #boutons du menu
        self.buttonRetourMenu = interface.findChild(QtWidgets.QPushButton, 'retourMenuResultats')
        self.buttonRetourMenu.clicked.connect(interface.retourMenu)
        self.buttonSupprimerSerie = interface.findChild(QtWidgets.QPushButton, 'supprimerSerie')
        self.buttonSupprimerSerie.clicked.connect(self.accesSuppressionSerie)
        self.buttonExportUSB = interface.findChild(QtWidgets.QPushButton, 'exportUSB')
        self.buttonExportUSB.clicked.connect(self.export)
        #liste des séries de résultats
        self.listeSeries = interface.findChild(QtWidgets.QComboBox,'listeSeries')
        #infos de la série de résultats
        self.infoSerie = interface.findChild(QtWidgets.QTableView,'infoSerie')

    def accesSuppressionSerie(self):
        print('Accès au menu de supression d\'une série/pattern')
        interface.selector.setCurrentIndex(ConfirmationSuppressionSerie)
    def export(self):
        print("l'export n'est pas encore implémenté")
        #à remplir (et ça va être long...)


#Le menu recapitulatif des parametres d'un pattern existant
class MenuRecapitulatifPattern():
    def __init__(self,interface):
        #boutons du menu
        self.buttonRetourMenu = interface.findChild(QtWidgets.QPushButton, 'retourMenuRecapitulatifPattern')
        self.buttonRetourMenu.clicked.connect(interface.retourMenu)
        self.buttonContinuerExperience = interface.findChild(QtWidgets.QPushButton, 'continuerExperience')
        self.buttonContinuerExperience.clicked.connect(self.accesChoixSouris)
        self.buttonModifierPattern = interface.findChild(QtWidgets.QPushButton, 'modifierPattern')
        self.buttonModifierPattern.clicked.connect(self.accesValidationModificationPattern)
        #informations concernant le pattern
        self.nom = interface.findChild(QtWidgets.QLabel, 'nomRecapitulatif')
        self.nbSouris = interface.findChild(QtWidgets.QLabel, 'nbSourisRecapitulatif')
        self.nbJours = interface.findChild(QtWidgets.QLabel, 'nbJoursRecapitulatif')
        self.nbEssais = interface.findChild(QtWidgets.QLabel, 'nbEssaisRecapitulatif')
        self.TempsMax = interface.findChild(QtWidgets.QLabel, 'tempsMaxRecapitulatif')
        self.modeEntrainement = interface.findChild(QtWidgets.QLabel, 'modeEntrainementRecapitulatif')

    def accesValidationModificationPattern(self):
        print('Accès au menu de validation de modification d\'un pattern')
        interface.selector.setCurrentIndex(ConfirmationModificationPattern)

    def accesChoixSouris(self):
        print('Accès au menu de choix d\'une souris dans un pattern')
        interface.selector.setCurrentIndex(ChoixSouris)

#Le menu de confirmation de supression d'un pattern existant
class MenuConfirmationSuppressionSerie():
    def __init__(self,interface):
        self.buttonSupprimer = interface.findChild(QtWidgets.QPushButton, 'validerSuppressionSerie')
        self.buttonSupprimer.clicked.connect(self.supprimerSerie)
        self.buttonAnnuler = interface.findChild(QtWidgets.QPushButton, 'annulerSuppressionSerie')
        self.buttonAnnuler.clicked.connect(self.annulerSuppressionSerie)
        #informations sur la série à supprimer
        self.nomSerie = interface.findChild(QtWidgets.QLabel, 'nomSerieASupprimer')

    def supprimerSerie(self):
        print('suppression d\'une série pas encore implémentée')
        self.annulerSuppressionSerie()

    def annulerSuppressionSerie(self):
        print('retour au menu des résultats')
        interface.selector.setCurrentIndex(Base)

#Le menu de confirmation des modifications sur un pattern existant
class MenuConfirmationModificationPattern():
    def __init__(self,interface):
        self.buttonSupprimer = interface.findChild(QtWidgets.QPushButton, 'validerModificationPattern')
        self.buttonSupprimer.clicked.connect(self.modifier)
        self.buttonAnnuler = interface.findChild(QtWidgets.QPushButton, 'annulerModificationPattern')
        self.buttonAnnuler.clicked.connect(self.annuler)

    def modifier(self):
        print('modification d\'un pattern')
        interface.selector.setCurrentIndex(CreationPattern)

    def annuler(self):
        print('retour au menu de sélection pattern')
        interface.selector.setCurrentIndex(SelectionPattern)

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
        interface.selector.setCurrentIndex(EssaiE1)

    def accesSuppressionSouris(self):
        print('acces au menu de confirmation de supression d\'une souris')
        interface.selector.setCurrentIndex(ConfirmationSupressionSouris)

#Le menu de confirmation de supression d'une souris dans un pattern
class MenuConfirmationSuppressionSouris():
    def __init__(self,interface):
        self.buttonValiderSupressionSouris = interface.findChild(QtWidgets.QPushButton, 'validerSupressionSouris')
        self.buttonValiderSupressionSouris.clicked.connect(self.supprimerSouris)
        self.buttonAnnulerSupressionSouris = interface.findChild(QtWidgets.QPushButton, 'annulerSupressionSouris')
        self.buttonAnnulerSupressionSouris.clicked.connect(self.retourChoixSouris)

    def supprimerSouris(self):
        print("supression de souris pas encore implémentée")
        self.retourChoixSouris()

    def retourChoixSouris(self):
        print("retour au menu de sélection de souris")
        interface.selector.setCurrentIndex(ChoixSouris)

#Le menu de suivi de l'experience, phase à 1 pot
class MenuEssaiE1():
    def __init__(self,interface):
        self.buttonTempsEcoule = interface.findChild(QtWidgets.QPushButton, 'tempsEcouleE1')
        self.buttonTempsEcoule.clicked.connect(self.tempsEcoule)
        self.buttonReussite = interface.findChild(QtWidgets.QPushButton, 'reussiteE1')
        self.buttonReussite.clicked.connect(self.reussite)
        #bouton utile uniquement à la mise en page
        self.buttonEchec = interface.findChild(QtWidgets.QPushButton, 'echecE1')
        self.buttonArretExperience = interface.findChild(QtWidgets.QPushButton, 'arreterExperienceE1')
        self.buttonArretExperience.clicked.connect(self.arretExperience)

    def tempsEcoule(self):
        print("chrono pas encore implémenté")

    def reussite(self):
        print("accès à l'essai suivant")
        print("enregistrement des résultats et placement des pots pas encore implémenté")
        interface.selector.setCurrentIndex(EssaiE2)

    def arretExperience(self):
        print("accès au menu de validation de l'arrêt de l'expérience")
        interface.selector.setCurrentIndex(ConfirmationArreterExperience)

#Le menu de suivi de l'experience, phase à 2 pots
class MenuEssaiE2():
    def __init__(self,interface):
        self.buttonTempsEcoule = interface.findChild(QtWidgets.QPushButton, 'tempsEcouleE2')
        self.buttonTempsEcoule.clicked.connect(self.tempsEcoule)
        self.buttonReussite = interface.findChild(QtWidgets.QPushButton, 'reussiteE2')
        self.buttonReussite.clicked.connect(self.reussite)
        self.buttonEchec = interface.findChild(QtWidgets.QPushButton, 'echecE2')
        self.buttonEchec.clicked.connect(self.echec)
        self.buttonArretExperience = interface.findChild(QtWidgets.QPushButton, 'arreterExperienceE2')
        self.buttonArretExperience.clicked.connect(self.arretExperience)

    def tempsEcoule(self):
        print("chrono pas encore implémenté")

    def reussite(self):
        print("accès à l'essai suivant")
        print("enregistrement des résultats et placement des pots pas encore implémenté")
        interface.selector.setCurrentIndex(EssaiE1)

    def echec(self):
        print("retour à l'essai précédent")
        print("enregistrement des résultats et placement des pots pas encore implémenté")
        interface.selector.setCurrentIndex(EssaiE1)

    def arretExperience(self):
        print("accès au menu de validation de l'arrêt de l'expérience")
        interface.selector.setCurrentIndex(ConfirmationArreterExperience)

#Le menu de confirmation de supression d'une souris dans un pattern
class MenuConfirmationArreterExperience():
    def __init__(self,interface):
        self.buttonValiderArretExperience = interface.findChild(QtWidgets.QPushButton, 'validerArretExperience')
        self.buttonValiderArretExperience.clicked.connect(interface.retourMenu)
        self.buttonAnnulerArretExperience = interface.findChild(QtWidgets.QPushButton, 'annulerArretExperience')
        self.buttonAnnulerArretExperience.clicked.connect(self.retourExperience)

    def retourExperience(self):
        print("retour à l'expérience en cours")
        interface.selector.setCurrentIndex(EssaiE1)
        #ajouter un retour dynamique

app = QtWidgets.QApplication(sys.argv)
interface = Interface()
interface.show()
app.exec_()
