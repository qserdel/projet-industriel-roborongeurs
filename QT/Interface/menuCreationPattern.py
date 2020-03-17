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
        tempsMax=self.cadreTempsMax.time().toString("hh:mm") #l'affichage donne hh:mm mais on s'en sert comme mm:ss
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
        if(not self.cadreNom.toPlainText()=='' and not self.cadreNombreSouris.value()==0 and not self.cadreNombreJours.value()==0 and not self.cadreNombreEssais.value()==0 and not self.cadreTempsMax.time().toString("hh:mm")=='00:00' and not interface.menuPlacementPots.dictEssais==None):
            self.buttonValiderCreationPattern.setEnabled(True)
        else:
            self.buttonValiderCreationPattern.setEnabled(False)

    def accesPlacementPots(self):
        print("accès au menu de placement des pots")
        interface.menuPlacementPots.creationListeEssai()
        interface.selector.setCurrentIndex(PlacementPots)
