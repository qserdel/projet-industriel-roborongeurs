import sys
from PyQt5 import QtWidgets, uic
from gestionStockage import *
#variables globales pour faciliter la navigation entre les menus
Base = 0
CreationPattern = 1
SelectionPattern = 2
Resultats = 3
ConfirmationSuppressionSerie = 4
ConfirmationModificationPattern = 5
ChoixSouris = 6
ConfirmationSupressionSouris = 7
ExperienceEssai = 8
ConfirmationArreterExperience = 9
PlacementPots = 10
FinExperience = 11

#La classe globale qui gère la création et la navigation pour tous les menus
class Interface(QtWidgets.QMainWindow):
    def __init__(self):
        super(Interface, self).__init__()
        #charge touts les patterns stockés en json
        self.dictPatterns=loadAllPatterns()
        #charge le fichier .ui de l'interface
        uic.loadUi('interface.ui', self)
        #créé le selecteur de menu
        self.selector = self.findChild(QtWidgets.QStackedWidget, 'stackedWidget')
        #créé tous les menus de l'interface
        self.menuBase = MenuBase(self)
        self.menuCreationPattern = MenuCreationPattern(self)
        self.menuSelectionPattern = MenuSelectionPattern(self)
        self.menuResultats = MenuResultats(self)
        self.menuConfirmationSuppressionSerie = MenuConfirmationSuppressionSerie(self)
        self.menuConfirmationModificationPattern = MenuConfirmationModificationPattern(self)
        self.menuChoixSouris = MenuChoixSouris(self)
        self.menuConfirmationSuppressionSouris = MenuConfirmationSuppressionSouris(self)
        self.menuEssai = MenuEssai(self)
        self.menuConfirmationArreterExperience = MenuConfirmationArreterExperience(self)
        self.menuPlacementPots = MenuPlacementPots(self)
        self.menuFinExperience=menuFinExperience(self)
        #affiche le menu de base
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
        self.interface=interface
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
        interface.menuCreationPattern.clearAll()
    def accesSelectionPattern(self):
        print('Accès au menu de séléction de pattern')
        interface.selector.setCurrentIndex(SelectionPattern)
        interface.menuSelectionPattern.afficherListePattern(interface)
    def accesResultats(self):
        print('Accès au menu des résultats')
        interface.menuResultats.afficherListeSeries(interface)
        interface.selector.setCurrentIndex(Resultats)

#Le menu de création de pattern
class MenuCreationPattern():
    def __init__(self,interface):
        self.interface=interface
        #boutons du menu
        self.buttonRetourMenu = interface.findChild(QtWidgets.QPushButton, 'retourMenuCreationPattern')
        self.buttonRetourMenu.clicked.connect(interface.retourMenu)
        self.buttonValiderCreationPattern = interface.findChild(QtWidgets.QPushButton, 'validerCreationPattern')
        self.buttonValiderCreationPattern.clicked.connect(self.creerPattern)
        self.buttonPlacementPots = interface.findChild(QtWidgets.QPushButton, 'placementDesPots')
        self.buttonPlacementPots.clicked.connect(self.accesPlacementPots)
        #entrées utilisateur
        self.cadreNom = interface.findChild(QtWidgets.QPlainTextEdit,'cadreNomPattern')
        self.cadreNombreSouris = interface.findChild(QtWidgets.QSpinBox,'cadreNombreSouris')
        self.cadreNombreJours = interface.findChild(QtWidgets.QSpinBox,'cadreNombreJours')
        self.cadreNombreEssais = interface.findChild(QtWidgets.QSpinBox,'cadreNombreEssais')
        self.cadreTempsMax = interface.findChild(QtWidgets.QTimeEdit,'cadreTempsMax')
        self.checkModeEntrainement = interface.findChild(QtWidgets.QCheckBox,'checkModeEntrainement')
        #activer ou desactiver les boutons en fonctions des valeurs contenues dans les cadres d'entrées
        self.cadreNom.textChanged.connect(self.activerBoutonValidationCreation)
        self.cadreNombreSouris.valueChanged.connect(self.activerBoutonValidationCreation)
        self.cadreNombreJours.valueChanged.connect(self.activerBoutonValidationCreation)
        self.cadreNombreEssais.valueChanged.connect(self.activerBoutonPlacementPots)
        self.cadreTempsMax.timeChanged.connect(self.activerBoutonValidationCreation)

    def creerPattern(self):
        #méthode partiellement fonctionnelle à teminer
        nom=self.cadreNom.toPlainText()
        nbSouris=self.cadreNombreSouris.value()
        nbJours=self.cadreNombreJours.value()
        nbJours=self.cadreNombreJours.value()
        #nbEssais=self.cadreNombreEssais.value #à mettre quand j'aurais géré la création auto de tableau
        nbEssais=2
        tempsMax=self.cadreTempsMax.time().toString("mm:ss") #l'affichage en mm:ss
        entrainement=self.checkModeEntrainement.isChecked()
        #ajouter la gestion du tableau de placement
        if(entrainement):
            placementPots=[[0],[0]]
        else:
            placementPots=[[0,1],[0,1]]
        pattern=Pattern(nom,nbSouris,nbJours,nbEssais,entrainement,tempsMax)
        pattern.placementPots(interface.menuPlacementPots.dictEssais)
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
        self.buttonValiderCreationPattern.setEnabled(False)
        self.buttonPlacementPots.setEnabled(False)
        interface.menuPlacementPots.dictEssais=None

    def activerBoutonPlacementPots(self):
        if(self.cadreNombreEssais.value()!=0):
            self.buttonPlacementPots.setEnabled(True)
        else:
            self.buttonPlacementPots.setEnabled(False)
        self.activerBoutonValidationCreation()

    def activerBoutonValidationCreation(self):
        if(not self.cadreNom.toPlainText()=='' and not self.cadreNombreSouris.value()==0 and not self.cadreNombreJours.value()==0 and not self.cadreNombreEssais.value()==0 and not self.cadreTempsMax.time().toString("mm:ss")=='00:00' and not interface.menuPlacementPots.dictEssais==None):
            self.buttonValiderCreationPattern.setEnabled(True)
        else:
            self.buttonValiderCreationPattern.setEnabled(False)

    def accesPlacementPots(self):
        print("accès au menu de placement des pots")
        interface.menuPlacementPots.creationListeEssai()
        interface.selector.setCurrentIndex(PlacementPots)

#Le menu de sélection de pattern existant
class MenuSelectionPattern():
    def __init__(self,interface):
        self.interface=interface
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
        interface.menuChoixSouris.affichageNomListe()
        print('Accès au menu de choix d\'une souris')
        interface.selector.setCurrentIndex(ChoixSouris)

    def accesSuppressionPattern(self):
        print('Acces au menu de supression de pattern/série')
        interface.selector.setCurrentIndex(ConfirmationSuppressionSerie)
        interface.menuConfirmationSuppressionSerie.nomSerie.setText(interface.patternActuel.nom)

    def afficherListePattern(self,interface):
        self.listePatterns.clear()
        for nomPattern in interface.dictPatterns:
            self.listePatterns.addItem(interface.dictPatterns[nomPattern].nom)

    def afficherInfoPattern(self):
        texte=self.listePatterns.currentText()
        if(texte!=''):
            interface.patternActuel=interface.dictPatterns[texte+".json"]
            self.infoPattern.setText(interface.patternActuel.affichage())


#Le menu d'affichage, d'export et de supression des résultats
class MenuResultats():
    def __init__(self,interface):
        self.interface=interface
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
        self.infoSerie = interface.findChild(QtWidgets.QLabel,'infoSerie')
        #affichage de la liste des patterns enregistrés et des infos du pattern selectionné
        self.afficherListeSeries(interface)
        self.listeSeries.currentIndexChanged.connect(self.afficherInfoSerie)

    def accesSuppressionSerie(self):
        print('Accès au menu de supression d\'une série/pattern')
        interface.selector.setCurrentIndex(ConfirmationSuppressionSerie)
        interface.menuConfirmationSuppressionSerie.nomSerie.setText(interface.patternActuel.nom)

    def export(self):
        transcriptionCsv(interface.patternActuel)
        print("l'export USB n'est pas encore implémenté")
        #TODO implémenter la détection USB (et ça va être long...)

    def afficherListeSeries(self,interface):
        self.listeSeries.clear()
        for nomPattern in interface.dictPatterns:
            self.listeSeries.addItem(interface.dictPatterns[nomPattern].nom)

    def afficherInfoSerie(self):
        texte=self.listeSeries.currentText()
        if(texte!=''):
            interface.patternActuel=interface.dictPatterns[texte+".json"]
            self.infoSerie.setText(interface.patternActuel.affichage())


#Le menu de confirmation de supression d'un pattern existant
class MenuConfirmationSuppressionSerie():
    def __init__(self,interface):
        self.interface=interface
        #boutons du menu
        self.buttonSupprimer = interface.findChild(QtWidgets.QPushButton, 'validerSuppressionSerie')
        self.buttonSupprimer.clicked.connect(self.supprimerSerie)
        self.buttonAnnuler = interface.findChild(QtWidgets.QPushButton, 'annulerSuppressionSerie')
        self.buttonAnnuler.clicked.connect(self.annulerSuppressionSerie)
        #informations sur la série à supprimer
        self.nomSerie = interface.findChild(QtWidgets.QLabel, 'nomSerieASupprimer')

    def supprimerSerie(self):
        path="Resultats/json/"+interface.patternActuel.nom+".json"
        print('suppression du pattern/série: '+path)
        os.remove(path)
        interface.dictPatterns=loadAllPatterns()
        self.annulerSuppressionSerie()

    def annulerSuppressionSerie(self):
        print('retour au menu des résultats')
        interface.selector.setCurrentIndex(Base)

#Le menu de confirmation des modifications sur un pattern existant
class MenuConfirmationModificationPattern():
    def __init__(self,interface):
        self.interface=interface
        #boutons du menu
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
        self.interface=interface
        #boutons du menu
        self.buttonRetourMenu = interface.findChild(QtWidgets.QPushButton, 'retourMenuChoixSouris')
        self.buttonRetourMenu.clicked.connect(interface.retourMenu)
        self.buttonChoisirSouris = interface.findChild(QtWidgets.QPushButton, 'supprimerSouris')
        self.buttonChoisirSouris.clicked.connect(self.accesSuppressionSouris)
        self.buttonSupprimerSouris = interface.findChild(QtWidgets.QPushButton, 'choisirSouris')
        self.buttonSupprimerSouris.clicked.connect(self.accesEssai)
        #nom du pattern courant
        self.nomPattern = interface.findChild(QtWidgets.QLabel, 'nomPatternChoixSouris')
        #affichage de la lsite des souris du pattern
        self.listeSouris = interface.findChild(QtWidgets.QComboBox, 'comboBoxChoixSouris')
        #affichage des infos de la souris selectionnée
        self.infoSouris = interface.findChild(QtWidgets.QLabel, 'infoSouris')
        self.listeSouris.currentIndexChanged.connect(self.affichageInfoSouris)
#ici
    def accesEssai(self):
        print('lancement de l\'expérience')
        interface.selector.setCurrentIndex(ExperienceEssai)
        interface.menuEssai.updateAffichage()

    def accesSuppressionSouris(self):
        print('acces au menu de confirmation de supression d\'une souris')
        interface.selector.setCurrentIndex(ConfirmationSupressionSouris)

    def affichageNomListe(self):
        self.nomPattern.setText(interface.patternActuel.nom)
        self.listeSouris.clear()
        for souris in interface.patternActuel.dictSouris:
            self.listeSouris.addItem(souris)

    def affichageInfoSouris(self):
        texte=self.listeSouris.currentText()
        if(texte!=''):
            interface.sourisActuelle=interface.patternActuel.dictSouris[texte]
            self.infoSouris.setText(interface.sourisActuelle.affichage())

#Le menu de confirmation de supression d'une souris dans un pattern
class MenuConfirmationSuppressionSouris():
    def __init__(self,interface):
        self.interface=interface
        #boutons du menu
        self.buttonValiderSupressionSouris = interface.findChild(QtWidgets.QPushButton, 'validerSupressionSouris')
        self.buttonValiderSupressionSouris.clicked.connect(self.supprimerSouris)
        self.buttonAnnulerSupressionSouris = interface.findChild(QtWidgets.QPushButton, 'annulerSupressionSouris')
        self.buttonAnnulerSupressionSouris.clicked.connect(self.retourChoixSouris)

    def supprimerSouris(self):
        interface.patternActuel.dictSouris.pop(interface.sourisActuelle.nom,None)
        self.retourChoixSouris()

    def retourChoixSouris(self):
        print("retour au menu de sélection de souris")
        interface.selector.setCurrentIndex(ChoixSouris)
        interface.menuChoixSouris.affichageNomListe()

#Le menu de suivi de l'experience
class MenuEssai():
    def __init__(self,interface):
        self.interface=interface
        #boutons du menu
        self.buttonTempsEcoule = interface.findChild(QtWidgets.QPushButton, 'tempsEcoule')
        self.buttonTempsEcoule.clicked.connect(self.tempsEcoule)
        self.buttonReussite = interface.findChild(QtWidgets.QPushButton, 'reussite')
        self.buttonReussite.clicked.connect(self.reussite)
        self.buttonEchec = interface.findChild(QtWidgets.QPushButton, 'echec')
        self.buttonEchec.clicked.connect(self.echec)
        self.buttonArretExperience = interface.findChild(QtWidgets.QPushButton, 'arreterExperience')
        self.buttonArretExperience.clicked.connect(self.arretExperience)
        #nom du pattern actuel
        self.nomPattern= interface.findChild(QtWidgets.QLabel, 'nomPatternEssai')
        #nom de la souris actuelle
        self.nomSouris=interface.findChild(QtWidgets.QLabel, 'nomSourisEssai')
        #nom de l'essai en cours
        self.nomEssai=interface.findChild(QtWidgets.QLabel, 'nomEssai')
        #placement des pots
        self.placementPot1=interface.findChild(QtWidgets.QLabel, 'placementPot1')
        self.placementPot2=interface.findChild(QtWidgets.QLabel, 'placementPot2')
        #label du pot2
        self.labelPot2=interface.findChild(QtWidgets.QLabel, 'labelPot2')
        #buton de marche/arret du chrono
        self.buttonStartStop=interface.findChild(QtWidgets.QPushButton, 'startStopChrono')
        self.buttonStartStop.clicked.connect(self.startStopChrono)

    def tempsEcoule(self):
        print("chrono pas encore implémenté")
        interface.essaiActuel.issue=2
        savePattern(interface.patternActuel)
        interface.menuEssai.nomPattern.setText(interface.patternActuel.nom)
        interface.menuEssai.nomSouris.setText(interface.sourisActuelle.nom)
        self.updateAffichage()

    def reussite(self):
        print("accès à l'essai suivant")
        interface.essaiActuel.issue=1
        savePattern(interface.patternActuel)
        interface.menuEssai.nomPattern.setText(interface.patternActuel.nom)
        interface.menuEssai.nomSouris.setText(interface.sourisActuelle.nom)
        self.updateAffichage()

    def echec(self):
        print("retour à l'essai précédent")
        interface.essaiActuel.issue=2
        savePattern(interface.patternActuel)
        interface.menuEssai.nomPattern.setText(interface.patternActuel.nom)
        interface.menuEssai.nomSouris.setText(interface.sourisActuelle.nom)
        self.updateAffichage()

    def arretExperience(self):
        print("accès au menu de validation de l'arrêt de l'expérience")
        interface.selector.setCurrentIndex(ConfirmationArreterExperience)

    def updateAffichage(self):
        #self.time=
        self.nomPattern.setText(interface.patternActuel.nom)
        self.nomSouris.setText(interface.sourisActuelle.nom)
        for nomEssai in interface.sourisActuelle.dictEssais:
            essai=interface.sourisActuelle.dictEssais[nomEssai]
            if(essai.issue==-1):
                Interface.essaiActuel=essai
                self.nomEssai.setText(nomEssai)
                break
        if(not essai.issue==-1):
            interface.selector.setCurrentIndex(FinExperience)
        else:
            self.placementPot1.setText(str(essai.placementPot1))
            if(essai.isE2):
                self.labelPot2.setEnabled(True)
                self.placementPot2.setEnabled(True)
                self.placementPot2.setText(str(essai.placementPot2))
                self.buttonEchec.setEnabled(True)
            else:
                self.labelPot2.setEnabled(False)
                self.placementPot2.setEnabled(False)
                self.placementPot2.setText('X')
                self.buttonEchec.setEnabled(False)

    def startStopChrono(self):
        if(self.buttonStartStop.isChecked()):
            print("start")
        else:
            print("stop")

#Le menu de confirmation de supression d'une souris dans un pattern
class MenuConfirmationArreterExperience():
    def __init__(self,interface):
        self.interface=interface
        #boutons du menu
        self.buttonValiderArretExperience = interface.findChild(QtWidgets.QPushButton, 'validerArretExperience')
        self.buttonValiderArretExperience.clicked.connect(interface.retourMenu)
        self.buttonAnnulerArretExperience = interface.findChild(QtWidgets.QPushButton, 'annulerArretExperience')
        self.buttonAnnulerArretExperience.clicked.connect(self.retourExperience)

    def retourExperience(self):
        print("retour à l'expérience en cours")
        interface.selector.setCurrentIndex(ExperienceEssai)

class MenuPlacementPots():
    def __init__(self,interface):
        self.interface=interface
        #boutons du menu
        self.buttonValiderPlacementPots=interface.findChild(QtWidgets.QPushButton,'validerPlacementPots')
        self.buttonValiderPlacementPots.clicked.connect(self.retourPlacementPots)
        #le selecteur d'essai
        self.selecteurEssai=interface.findChild(QtWidgets.QComboBox,'selecteurEssai')

        #les cadres de placement des pots
        self.placementPot1=interface.findChild(QtWidgets.QDoubleSpinBox,'boxPlacementPot1')
        self.placementPot1.valueChanged.connect(self.updatePlacement1)
        self.placementPot2=interface.findChild(QtWidgets.QDoubleSpinBox,'boxPlacementPot2')
        self.placementPot2.valueChanged.connect(self.updatePlacement2)
        #les sliders giga-stylés d'aide au placement
        self.sliderPot1=interface.findChild(QtWidgets.QSlider,'sliderPlacementPot1')
        self.sliderPot1.valueChanged.connect(self.updateSlider1)
        self.sliderPot2=interface.findChild(QtWidgets.QSlider,'sliderPlacementPot2')
        self.sliderPot2.valueChanged.connect(self.updateSlider2)


    def retourPlacementPots(self):
        print("retour au menu de création de pattern")
        interface.selector.setCurrentIndex(CreationPattern)
        interface.menuCreationPattern.activerBoutonValidationCreation()

    def creationListeEssai(self):
        self.selecteurEssai.clear()
        self.dictEssais=dict()
        print(interface.menuCreationPattern.checkModeEntrainement.isChecked())
        if(interface.menuCreationPattern.checkModeEntrainement.isChecked()):
            self.placementPot2.setEnabled(False)
            self.sliderPot2.setEnabled(False)
        for i in range(0,interface.menuCreationPattern.cadreNombreEssais.value()):
            nomEssai="T"+str(i)
            self.selecteurEssai.addItem(nomEssai)
            self.dictEssais[nomEssai+"E1"]=EssaiE1(self.placementPot1.value())
            if(not interface.menuCreationPattern.checkModeEntrainement.isChecked()):
                self.dictEssais[nomEssai+"E2"]=EssaiE2(self.placementPot1.value(),self.placementPot2.value())
        self.selecteurEssai.currentIndexChanged.connect(self.selectionEssai)

    def selectionEssai(self):
        if(not self.dictEssais['T0E1']==None):
            self.placementPot1.setValue(self.dictEssais[self.selecteurEssai.currentText()+"E1"].placementPot1)
            if(not interface.menuCreationPattern.checkModeEntrainement.isChecked()):
                self.placementPot2.setValue(self.dictEssais[self.selecteurEssai.currentText()+"E2"].placementPot2)

    def updatePlacement1(self):
        valeur=self.placementPot1.value()
        #TODO changer la valeur dans l'objet pattern
        if(valeur==0.5):
            valeur=1
        if(valeur==-0.5):
            valeur=-1
        self.sliderPot1.setValue(valeur*2)
        self.dictEssais[self.selecteurEssai.currentText()+"E1"]=EssaiE1(self.placementPot1.value())
        if(not interface.menuCreationPattern.checkModeEntrainement.isChecked()):
            self.dictEssais[self.selecteurEssai.currentText()+"E2"]=EssaiE2(self.placementPot1.value(),self.placementPot2.value())

    def updateSlider1(self):
        valeur=self.sliderPot1.value()/2
        if(valeur==0.5):
            valeur=1
        if(valeur==-0.5):
            valeur=-1
        self.placementPot1.setValue(valeur)
        self.updatePlacement1()

    def updatePlacement2(self):
        valeur=self.placementPot2.value()
        if(valeur==0.5):
            valeur=1
        if(valeur==-0.5):
            valeur=-1
        self.sliderPot2.setValue(valeur*2)
        self.dictEssais[self.selecteurEssai.currentText()+"E"+str(2)]=EssaiE2(self.placementPot1.value(),self.placementPot2.value())

    def updateSlider2(self):
        valeur=self.sliderPot2.value()/2
        if(valeur==0.5):
            valeur=1
        if(valeur==-0.5):
            valeur=-1
        self.placementPot2.setValue(valeur)
        self.updatePlacement2()

#menu ouvert lorsqu'une souris a fini sa série d'essais
class menuFinExperience():
    def __init__(self,interface):
        self.buttonRetour=interface.findChild(QtWidgets.QPushButton, 'retourChoixSourisFin')
        self.buttonRetour.clicked.connect(self.retourChoixSouris)

    def retourChoixSouris(self):
        interface.menuChoixSouris.affichageInfoSouris()
        interface.selector.setCurrentIndex(ChoixSouris)

app = QtWidgets.QApplication(sys.argv)
interface = Interface()
interface.show()
app.exec_()
