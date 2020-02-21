#TODO créer des classes souris, pattern, essaiE1, essai E2
#TODO choisir le type de stockage des objets (JSON ou pickle)
#TODO afficher le nom des fichiers stockés dans l'interface

import json
import os
import time
import pickle

class Souris():

    def __init__(self,nom):
        self.nom = nom
        self.dictEssais = dict()
    def ajouterEssai(self,cle,essais):
        self.dictEssais[cle]=essais

    def affichage(self):
        affichage="\nnom: "+self.nom
        affichage+="\ndictEssais: {"
        for cle in self.dictEssais:
            affichage += "\n"+cle+": "+self.dictEssais[cle].affichage()
        affichage += "\n}"
        return affichage

class EssaiE1():
    temps="00:00"
    placementPot1=0
    issue=0

    def __init__(self,placementPot1):
        self.placementPot1=placementPot1

    def start(self):
        print("rien")

    def affichage(self):
        affichage="\nplacementPot1: "+str(self.placementPot1)
        return affichage

class EssaiE2():
    temps="00:00"
    placementPot1=0
    placementPot2=0
    issue=0

    def __init__(self,placementPot1,placementPot2):
        self.placementPot1=placementPot1
        self.placementPot2=placementPot2

    def start(self):
        print("rien")

    def affichage(self):
        affichage="\nplacementPot1: "+str(self.placementPot1)
        affichage+="\nplacementPot2: "+str(self.placementPot2)
        return affichage

class Pattern():
    dictSouris=dict()

    def __init__(self,nom,nbSouris,nbJours,nbEssais,entrainement,tempsMax,placementPots):
        #tous les attributs "basiques" du pattern
        self.nom = nom
        self.nbSouris=nbSouris
        self.nbJours=nbJours
        self.nbEssais=nbEssais
        self.entrainement=entrainement
        self.placementPots=placementPots
        #tempsMax sous la forme "MM:SS" passé en struct_time
        self.tempsMax=time.strptime(tempsMax,"%M:%S")
        #date actuelle
        date = time.localtime()
        #passée au format dd/mm/yyyy
        self.dateDebut=time.strftime("%d/%m/%Y", date)
        #création d'un dictionnaire [si:Souris] à partir de nbSouris
        for i in range(0,nbSouris):
            self.ajouterSouris("s"+str(i))
            #pour chaque souris: création d'un dictionnaire [TjEk:essai] à partir de nbEssais, entrainement et le tableau placementsPots
            for j in range(0,nbEssais):
                self.dictSouris["s"+str(i)].ajouterEssai("T"+str(j)+"E1",EssaiE1(placementPots[j][0]))
                if(not(entrainement)):
                    self.dictSouris["s"+str(i)].ajouterEssai("T"+str(j)+"E2",EssaiE2(placementPots[j][0],placementPots[j][1]))
    def ajouterSouris(self,nom):
        self.dictSouris[nom]=Souris(nom)
    def supprimerSouris(self,nom):
        del self.dictSouris[nom]

    def affichage(self):
        affichage="\nnom: "+self.nom
        affichage+="\nnbSouris: "+str(self.nbSouris)
        affichage+="\nnbJours: "+str(self.nbJours)
        affichage+="\nnbEssais: "+str(self.nbEssais)
        affichage+="\nentrainement: "+str(self.entrainement)
        affichage+="\ntempsMax: "+ time.strftime("%M:%S",self.tempsMax)
        affichage+="\ndateDebut:"+self.dateDebut
        affichage+="\ndictSouris: {"
        for cle in self.dictSouris:
            affichage += "\n"+cle+": "+self.dictSouris[cle].affichage()
        affichage += "\n}"
        return affichage

def savePattern(pattern):
    patternDict = {
    "nom":pattern.nom,
    "nbSouris":pattern.nbSouris,
    "nbJours":pattern.nbJours,
    "nbEssais":pattern.nbEssais,
    "entrainement":pattern.entrainement,
    "tempsMax":time.strftime("%M:%S",pattern.tempsMax),
    "dateDebut":pattern.dateDebut,
    "placementPots":pattern.placementPots,
    "dictSouris":pattern.dictSouris
    }
    path="Resultats/JSON/"+pattern.nom
    fichierPattern=open(path,'wb')
    patternPickler=pickle.Pickler(fichierPattern)
    patternPickler.dump(patternDict)
    fichierPattern.close()

def loadPattern(nomFichier):
    path="Resultats/JSON/"+nomFichier
    fichierPattern=open(path,'rb')
    patternDepickler=pickle.Unpickler(fichierPattern)
    patternDict=patternDepickler.load()
    fichierPattern.close()
    nom=patternDict["nom"]
    nbSouris=patternDict["nbSouris"]
    nbJours=patternDict["nbJours"]
    nbEssais=patternDict["nbEssais"]
    entrainement=patternDict["entrainement"]
    tempsMax=patternDict["tempsMax"]
    dateDebut=patternDict["dateDebut"]
    placementPots=patternDict["placementPots"]
    dictSouris=patternDict["dictSouris"]
    pattern = Pattern(nom,nbSouris,nbJours,nbEssais,entrainement,tempsMax,placementPots)
    return pattern

def testRead():
    #ouvrir le fichier
    # with open(machin) as template pour assurer la fermeture
    template = open("JSON/template.json","r")
    #lire le contenu du fichier
    contenu_template = template.read()
    print(contenu_template)
    #fermer le fichier
    template.close()
def testWrite():
    #créer/ouvrir le fichier
    testWrite = open("JSON/testWrite.json","w")
    #ecrire dans le fichier
    testWrite.write("heyheyhey ça marche super")
    #fermer le fichier
    testWrite.close()
def testPickle():
    souris=Souris("Jerry")
    fichierSouris=open('JSON/fichierSouris','wb')
    sourisPickle=pickle.Pickler(fichierSouris)
    sourisPickle.dump(souris.nom)
def testCreationPattern():
    nom="patternTest"
    nbSouris=2
    nbJours=10
    nbEssais=3
    entrainement=False
    tempsMax="05:00"
    placementPots=[[0,3.5],[0,2],[0,1]]
    pattern = Pattern(nom,nbSouris,nbJours,nbEssais,entrainement,tempsMax,placementPots)
    savePattern(pattern)
    print(pattern.affichage())
def testCreationPattern2():
    pattern=loadPattern("patternTest")
    print(pattern.affichage())
#changer le path
#os.chdir("Resultats")
testCreationPattern2()
#testPickle()
#testRead()
#testWrite()
