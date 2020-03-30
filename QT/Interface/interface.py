import sys
from PyQt5 import QtWidgets, uic
from gestionStockage import *
from chronoThread import chronoThread

#sur PC

#TODO régler les bugs de placement des pots (position initiale des sliders)

#Sur raspberry

#TODO +++ implémenter la détection USB
#TODO ++ lancer directement au boot
#TODO ++ affichage plein écran automatique
#TODO créer raccourci bureau
#TODO gérer la mise en forme sur la tablette

#variables globales pour faciliter la navigation entre les menus
Base = 0
CreationPattern = 1
SelectionPattern = 2
Resultats = 3
ConfirmationSuppressionSerie = 4
ChoixSouris = 5
ConfirmationSupressionSouris = 6
ExperienceEssai = 7
ConfirmationArreterExperience = 8
PlacementPots = 9
FinExperience = 10
CopiePattern = 11

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
        self.menuChoixSouris = MenuChoixSouris(self)
        self.menuConfirmationSuppressionSouris = MenuConfirmationSuppressionSouris(self)
        self.menuEssai = MenuEssai(self)
        self.menuConfirmationArreterExperience = MenuConfirmationArreterExperience(self)
        self.menuPlacementPots = MenuPlacementPots(self)
        self.menuFinExperience=menuFinExperience(self)
        self.menuCopie=menuCopie(self)
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
        self.buttonCopierPattern = interface.findChild(QtWidgets.QPushButton, 'copierPattern')
        self.buttonCopierPattern.clicked.connect(self.accesCopiePattern)
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
        #remplis toutes les valeurs du pattern avec le contenu des cadres du menu
        nom=self.cadreNom.toPlainText()
        nbSouris=self.cadreNombreSouris.value()
        nbJours=self.cadreNombreJours.value()
        nbEssais=self.cadreNombreEssais.value()
        tempsMax=self.cadreTempsMax.time().toString("mm:ss") #l'affichage en mm:ss
        entrainement=self.checkModeEntrainement.isChecked()
        pattern=Pattern(nom,nbSouris,nbJours,nbEssais,entrainement,tempsMax)
        pattern.placementPots(interface.menuPlacementPots.dictEssais)
        savePattern(pattern)
        print("nouveau pattern créé:")
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

    def accesCopiePattern(self):
        print("acces au menu de création par copie de pattern")
        interface.menuCopie.afficherListePattern()
        interface.selector.setCurrentIndex(CopiePattern)

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
        print("Création du fichier csv dans ./Resultats/csv")

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
        #chrono
        self.affichageChrono=interface.findChild(QtWidgets.QLabel, 'temps')
        self.chronoRunning=False

    #mise à jour de l'affichage du menu
    def updateAffichage(self):
        self.nomPattern.setText(interface.patternActuel.nom)
        self.nomSouris.setText(interface.sourisActuelle.nom)
        self.affichageChrono.setText("00:00")
        #si le thread chrono tourne encore, on l'arrête
        if(self.chronoRunning):
            self.buttonStartStop.setChecked(False)
            self.startStopChrono()
        for nomEssai in sorted(interface.sourisActuelle.dictEssais):
            essai=interface.sourisActuelle.dictEssais[nomEssai]
            if(essai.issue==-1):
                Interface.essaiActuel=essai
                self.nomEssai.setText(nomEssai)
                break
        #gestion de la fin de la liste des essais de la souris
        if(not essai.issue==-1):
            interface.selector.setCurrentIndex(FinExperience)
        else:
            self.placementPot1.setText(str(essai.placementPot1))
            #on ne peut pas cliquer sur les boutons tant que le chrono n'a pas été lancé
            self.buttonReussite.setEnabled(False)
            self.buttonEchec.setEnabled(False)
            self.buttonTempsEcoule.setEnabled(False)
            #s'il s'agit d'un essai E1, on n'affiche pas le placement du pot 2
            if(essai.isE2):
                self.labelPot2.setEnabled(True)
                self.placementPot2.setEnabled(True)
                self.placementPot2.setText(str(essai.placementPot2))
            else:
                self.labelPot2.setEnabled(False)
                self.placementPot2.setEnabled(False)
                self.placementPot2.setText('X')

    #fonction appelée lorsque l'on appuie sur le bouton "Start/stop"
    def startStopChrono(self):
        if(self.buttonStartStop.isChecked()):
            print("start")
            #thread paralllèle du chrono
            self.chronoThread=chronoThread(interface)
            self.chronoRunning=True
            self.chronoThread.start()
            self.buttonReussite.setEnabled(True)
            if(interface.essaiActuel.isE2):
                self.buttonEchec.setEnabled(True)
        else:
            print("stop")
            self.chronoRunning=False
            self.chronoThread.join()

    def tempsEcoule(self):
        print("Temps écoulé, retour à l'essai E1 précédent")
        interface.essaiActuel.issue=0
        #la souris doit recommencer à l'essai E1 précédent, on créé une copie de cet essai
        nomNouvelEssaiE1=list(self.nomEssai.text())
        nomNouvelEssaiE1[4]='1'
        nomNouvelEssaiE1="".join(nomNouvelEssaiE1[0:5])
        print(nomNouvelEssaiE1)
        i=1
        #on s'assure de créer un essai qui n'existe pas dans la liste
        nomNouvelEssaiE1courant=nomNouvelEssaiE1+"("+str(i)+")"
        while(nomNouvelEssaiE1courant in interface.sourisActuelle.dictEssais):
            i+=1
            nomNouvelEssaiE1courant=nomNouvelEssaiE1+"("+str(i)+")"
        nomNouvelEssaiE1=nomNouvelEssaiE1courant
        interface.sourisActuelle.dictEssais[nomNouvelEssaiE1]=EssaiE1(interface.essaiActuel.placementPot1)
        #si l'essai raté est de type E2, on créé aussi une copie de l'essai E2
        if(interface.essaiActuel.isE2):
            nomNouvelEssaiE2=list(self.nomEssai.text())
            nomNouvelEssaiE2[4]='2'
            nomNouvelEssaiE2="".join(nomNouvelEssaiE2[0:5])
            print(nomNouvelEssaiE2)
            i=1
            #on s'assure de créer un essai qui n'existe pas dans la liste
            nomNouvelEssaiE2courant=nomNouvelEssaiE2+"("+str(i)+")"
            while(nomNouvelEssaiE2courant in interface.sourisActuelle.dictEssais):
                i+=1
                nomNouvelEssaiE2courant=nomNouvelEssaiE2+"("+str(i)+")"
            nomNouvelEssaiE2=nomNouvelEssaiE2courant
            interface.sourisActuelle.dictEssais[nomNouvelEssaiE2]=EssaiE2(interface.essaiActuel.placementPot1,interface.essaiActuel.placementPot1)
        interface.essaiActuel.temps=self.affichageChrono.text()
        savePattern(interface.patternActuel)
        self.updateAffichage()

    def reussite(self):
        print("Réussite, accès à l'essai suivant")
        interface.essaiActuel.issue=1
        interface.essaiActuel.temps=self.affichageChrono.text()
        savePattern(interface.patternActuel)
        self.updateAffichage()

    def echec(self):
        print("Echec, accès à l'essai précédent")
        interface.essaiActuel.issue=2
        interface.essaiActuel.temps=self.affichageChrono.text()
        savePattern(interface.patternActuel)
        self.updateAffichage()

    def arretExperience(self):
        print("accès au menu de validation de l'arrêt de l'expérience")
        if(self.chronoRunning):
            self.startStopChrono()
        interface.selector.setCurrentIndex(ConfirmationArreterExperience)


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
        self.buttonEssaiSuivant=interface.findChild(QtWidgets.QPushButton, 'essaiSuivant')
        self.buttonEssaiSuivant.clicked.connect(self.essaiSuivant)
        #le selecteur d'essai
        self.selecteurEssai=interface.findChild(QtWidgets.QComboBox,'selecteurEssai')

        #les cadres de placement des pots
        self.placementPot1=interface.findChild(QtWidgets.QDoubleSpinBox,'boxPlacementPot1')
        self.placementPot2=interface.findChild(QtWidgets.QDoubleSpinBox,'boxPlacementPot2')
        #les sliders giga-stylés d'aide au placement
        self.sliderPot1=interface.findChild(QtWidgets.QSlider,'sliderPlacementPot1')
        self.sliderPot1.valueChanged.connect(self.updateSlider1)
        self.sliderPot2=interface.findChild(QtWidgets.QSlider,'sliderPlacementPot2')
        self.sliderPot2.valueChanged.connect(self.updateSlider2)


    def retourPlacementPots(self):
        print("retour au menu de création de pattern")
        interface.selector.setCurrentIndex(CreationPattern)
        self.selecteurEssai.currentIndexChanged.disconnect()
        interface.menuCreationPattern.activerBoutonValidationCreation()

    def creationListeEssai(self):
        self.selecteurEssai.clear()
        self.dictEssais=dict()
        if(interface.menuCreationPattern.checkModeEntrainement.isChecked()):
            self.placementPot2.setEnabled(False)
            self.sliderPot2.setEnabled(False)
        for i in range(0,interface.menuCreationPattern.cadreNombreEssais.value()):
            nomEssai="T"+str(i).zfill(2)
            self.selecteurEssai.addItem(nomEssai)
            self.dictEssais[nomEssai+"E1"]=EssaiE1(0)
            if(not interface.menuCreationPattern.checkModeEntrainement.isChecked()):
                self.dictEssais[nomEssai+"E2"]=EssaiE2(0,0)
        self.selecteurEssai.currentIndexChanged.connect(self.selectionEssai)
        self.selectionEssai()

    def selectionEssai(self):
        if('T00E1' in self.dictEssais):
            self.placementPot1.setValue(self.dictEssais[self.selecteurEssai.currentText()+"E1"].placementPot1)
            if(not interface.menuCreationPattern.checkModeEntrainement.isChecked()):
                print(self.dictEssais[self.selecteurEssai.currentText()+"E2"].placementPot2)
                self.placementPot2.setValue(self.dictEssais[self.selecteurEssai.currentText()+"E2"].placementPot2)
        #blocage du bouton "essai suivant" si on est au dernier essai de la liste
        if(self.selecteurEssai.currentIndex() ==self.selecteurEssai.count()-1):
            self.buttonEssaiSuivant.setEnabled(False)
        else:
            self.buttonEssaiSuivant.setEnabled(True)
        self.updatePlacement1()
        self.updatePlacement2()
        self.updateSlider1()
        self.updateSlider2()

    def updatePlacement1(self):
        valeur=self.placementPot1.value()
        self.sliderPot1.setValue(valeur*2)
        self.dictEssais[self.selecteurEssai.currentText()+"E1"].placementPot1=self.placementPot1.value()
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
        self.sliderPot2.setValue(valeur*2)
        self.dictEssais[self.selecteurEssai.currentText()+"E2"].placementPot2=self.placementPot2.value()

    def updateSlider2(self):
        valeur=self.sliderPot2.value()/2
        if(valeur==0.5):
            valeur=1
        if(valeur==-0.5):
            valeur=-1
        self.placementPot2.setValue(valeur)
        self.updatePlacement2()

    def essaiSuivant(self):
        self.updateSlider1()
        self.updateSlider2()
        self.selecteurEssai.setCurrentIndex(self.selecteurEssai.currentIndex() +1)


#menu ouvert lorsqu'une souris a fini sa série d'essais
class menuFinExperience():
    def __init__(self,interface):
        self.buttonRetour=interface.findChild(QtWidgets.QPushButton, 'retourChoixSourisFin')
        self.buttonRetour.clicked.connect(self.retourChoixSouris)

    def retourChoixSouris(self):
        interface.menuChoixSouris.affichageInfoSouris()
        interface.selector.setCurrentIndex(ChoixSouris)

#menu permettant de créer un nouveau pattern à partir des paramètres d'un pattern existant
class menuCopie():
    def __init__(self,interface):
        #boutons du menus
        self.buttonCopierPattern=interface.findChild(QtWidgets.QPushButton, 'validerCopiePattern')
        self.buttonCopierPattern.clicked.connect(self.copierPattern)
        self.buttonRetour=interface.findChild(QtWidgets.QPushButton, 'retourCopie')
        self.buttonRetour.clicked.connect(interface.retourMenu)
        #affichage et entrée utilisateur du menu
        self.listePatterns=interface.findChild(QtWidgets.QComboBox, 'listePatternsCopie')
        self.listePatterns.currentIndexChanged.connect(self.afficherInfoPattern)
        self.nomPattern=interface.findChild(QtWidgets.QPlainTextEdit, 'nomPatternCopie')
        self.infoPattern=interface.findChild(QtWidgets.QLabel, 'infoPatternCopie')

    def afficherListePattern(self):
        self.listePatterns.clear()
        for nomPattern in interface.dictPatterns:
            self.listePatterns.addItem(interface.dictPatterns[nomPattern].nom)

    def afficherInfoPattern(self):
        texte=self.listePatterns.currentText()
        if(texte!=''):
            interface.patternActuel=interface.dictPatterns[texte+".json"]
            affichage=interface.patternActuel.affichage()+"\nessais:"
            for nomEssai in interface.patternActuel.dictSouris[list(interface.patternActuel.dictSouris.keys())[0]].dictEssais:
                essai=interface.patternActuel.dictSouris[list(interface.patternActuel.dictSouris.keys())[0]].dictEssais[nomEssai]
                affichage+="\n\t"+nomEssai+"\t"
                if(essai.isE2):
                    affichage+="["+str(essai.placementPot1)+" "+str(essai.placementPot2)+"]"
                else:
                    affichage+="["+str(essai.placementPot1)+"]"
            self.infoPattern.setText(affichage)
            i=1
            while((texte+"("+str(i)+").json") in interface.dictPatterns):
                i+=1
            self.nomPattern.setPlainText(self.listePatterns.currentText()+"("+str(i)+")")

    def copierPattern(self):
        nom=self.nomPattern.toPlainText()
        nbSouris=interface.patternActuel.nbSouris
        nbJours=interface.patternActuel.nbJours
        nbEssais=interface.patternActuel.nbEssais
        entrainement=interface.patternActuel.entrainement
        tempsMax=time.strftime("%M:%S",interface.patternActuel.tempsMax)
        patternCopie=Pattern(nom,nbSouris,nbJours,nbEssais,entrainement,tempsMax)
        patternCopie.placementPots(interface.patternActuel.dictSouris[list(interface.patternActuel.dictSouris.keys())[0]].dictEssais)
        savePattern(patternCopie)
        interface.dictPatterns=loadAllPatterns()
        print("pattern copié et enregistré")
        interface.retourMenu()



app = QtWidgets.QApplication(sys.argv)
interface = Interface()
interface.show()
app.exec_()
