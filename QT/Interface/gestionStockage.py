#TODO plein ecran

import os
import time
import json
import csv

class Souris():

    def __init__(self,nom):
        self.nom = nom
        self.dictEssais = dict()
    def ajouterEssai(self,cle,essais):
        self.dictEssais[cle]=essais

    def affichage(self):
        affichage="\n  souris "+self.nom+": "
        for cle in self.dictEssais:
            affichage += "\n    "+cle+":"+self.dictEssais[cle].affichage()
        return affichage

    def toJson(self):
        essaiDict=dict()
        for nomEssai in self.dictEssais:
            essaiDict[nomEssai]=self.dictEssais[nomEssai].toJson()
        sourisJson= {
        "nom":self.nom,
        "essaiDict":essaiDict
        }
        return sourisJson

class EssaiE1():
    temps="00:00"
    placementPot1=0
    issue=-1
    isE2=False;

    def __init__(self,placementPot1):
        self.placementPot1=placementPot1

    def start(self):
        #TODO gérer ça
        print("rien")

    def stop(self):
        #TODO gérer ça
        print("rien")

    def affichage(self):
        affichage=" ["+str(self.placementPot1)+"]        "+self.issueToString()
        return affichage

    def toJson(self):
        essaiE1Json={
        "isE2":False,
        "placementPot1":self.placementPot1,
        "temps":self.temps,
        "issue":self.issue
        }
        return essaiE1Json

    def issueToString(self):
        if(self.issue==-1): return "pas commencé"
        if(self.issue==0): return "temps écoulé"
        if(self.issue==1): return "   réussi   "

class EssaiE2():
    temps="00:00"
    placementPot1=0
    placementPot2=0
    issue=-1
    isE2=True;

    def __init__(self,placementPot1,placementPot2):
        self.placementPot1=placementPot1
        self.placementPot2=placementPot2

    def start(self):
        print("rien")

    def stop(self):
        print("rien")

    def affichage(self):
        affichage=" ["+str(self.placementPot1)+" "+str(self.placementPot2)+"] "+self.issueToString()
        return affichage

    def toJson(self):
        essaiE2Json={
        "isE2":True,
        "placementPot1":self.placementPot1,
        "placementPot2":self.placementPot2,
        "temps":self.temps,
        "issue":self.issue
        }
        return essaiE2Json

    def issueToString(self):
            if(self.issue==-1): return "pas commencé"
            if(self.issue==0): return "temps écoulé"
            if(self.issue==1): return "   réussi   "
            if(self.issue==2): return "   échoué   "

class Pattern():

    def __init__(self,nom,nbSouris,nbJours,nbEssais,entrainement,tempsMax):
        #tous les attributs "basiques" du pattern
        self.nom = nom
        self.nbSouris=nbSouris
        self.nbJours=nbJours
        self.nbEssais=nbEssais
        self.entrainement=entrainement
        #tempsMax sous la forme "MM:SS" passé en struct_time
        self.tempsMax=time.strptime(tempsMax,"%M:%S")
        #date actuelle
        date = time.localtime()
        #passée au format dd/mm/yyyy
        self.dateDebut=time.strftime("%d/%m/%Y", date)
        #création d'un dictionnaire [si:Souris] à partir de nbSouris
        self.dictSouris=dict()
        for i in range(0,nbSouris):
            self.ajouterSouris("s"+str(i))
            #pour chaque souris: création d'un dictionnaire [TjEk:essai] à partir de nbEssais, entrainement et le tableau placementsPots
            #for j in range(0,nbEssais):
            #    self.dictSouris["s"+str(i)].ajouterEssai("T"+str(j)+"E1",EssaiE1(placementPots[j][0]))
            #    if(not(entrainement)):
            #        self.dictSouris["s"+str(i)].ajouterEssai("T"+str(j)+"E2",EssaiE2(placementPots[j][0],placementPots[j][1]))

    def ajouterSouris(self,nom):
        self.dictSouris[nom]=Souris(nom)

    def placementPots(self,dictEssais):
        for i in range(0,self.nbSouris):
            #pour chaque souris: création d'un dictionnaire [TjEk:essai] à partir de nbEssais, entrainement et le tableau placementsPots
            self.dictSouris["s"+str(i)].dictEssais=dictEssais

    def supprimerSouris(self,nom):
        del self.dictSouris[nom]

    def startEssai(essai):
        essai.start()

    def affichage(self):
        affichage="nom: "+self.nom
        affichage+="\nnbSouris: "+str(self.nbSouris)
        affichage+="    nbJours: "+str(self.nbJours)
        affichage+="    nbEssais: "+str(self.nbEssais)
        affichage+="\nentrainement: "+str(self.entrainement)
        affichage+="\ntempsMax: "+ time.strftime("%M:%S",self.tempsMax)
        affichage+="\ndateDebut:"+self.dateDebut
        #affichage+="\ndictSouris: {"
        #for cle in self.dictSouris:
        #    affichage += "\n"+cle+": "+self.dictSouris[cle].affichage()
        #affichage += "\n}"
        return affichage

    def toJson(self):
        sourisDict=dict()
        for nomSouris in self.dictSouris:
            sourisDict[nomSouris]=self.dictSouris[nomSouris].toJson()
        patternJson = {
        "nom":self.nom,
        "nbSouris":self.nbSouris,
        "nbJours":self.nbJours,
        "nbEssais":self.nbEssais,
        "entrainement":self.entrainement,
        "tempsMax":time.strftime("%M:%S",self.tempsMax),
        "dateDebut":self.dateDebut,
        "sourisDict":sourisDict
        }
        return patternJson

#fonction de sauvegarde de pattern avec la bibliothèque pickle
def savePattern(pattern):
    patternJson=pattern.toJson()
    path="Resultats/json/"+pattern.nom+".json"
    with open(path,'w') as fichierPattern:
        #patternPickler=pickle.Pickler(fichierPattern)
        json.dump(patternJson,fichierPattern)

#fonction de chargement de pattern
def loadPattern(nomFichier):
    path="Resultats/json/"+nomFichier
    with open(path,'r') as fichierPattern:
        #créé le dictionnaire patternJson avec json.load()
        patternJson = json.load(fichierPattern)
    nom=patternJson["nom"]
    nbSouris=patternJson["nbSouris"]
    nbJours=patternJson["nbJours"]
    nbEssais=patternJson["nbEssais"]
    entrainement=patternJson["entrainement"]
    tempsMax=patternJson["tempsMax"]
    dateDebut=patternJson["dateDebut"]
    dictSouris=dict()
    for nomSouris in patternJson["sourisDict"]:
        souris=patternJson["sourisDict"][nomSouris]
        dictEssais=dict()
        for nomEssai in souris["essaiDict"]:
            essai=souris["essaiDict"][nomEssai]
            if(essai["isE2"]):
                dictEssais[nomEssai]=EssaiE2(essai["placementPot1"],essai["placementPot2"])
                dictEssais[nomEssai].isE2=True
            else:
                dictEssais[nomEssai]=EssaiE1(essai["placementPot1"])
                dictEssais[nomEssai].isE2=False
            dictEssais[nomEssai].temps=essai["temps"]
            dictEssais[nomEssai].issue=essai["issue"]
        dictSouris[nomSouris]=Souris(nomSouris)
        dictSouris[nomSouris].dictEssais=dictEssais
    pattern = Pattern(nom,0,nbJours,nbEssais,entrainement,tempsMax)
    pattern.nbSouris=nbSouris
    pattern.dictSouris=dictSouris
    pattern.dateDebut=dateDebut
    return pattern

#chercher tous les fichiers présents dans le dossier Resultats/json
#et créé un dictionnaire de patterns correspondant
def loadAllPatterns():
    path="Resultats/json"
    dictPatterns=dict()
    listeFichiersPatterns=os.listdir(path)
    for nomPattern in listeFichiersPatterns:
        dictPatterns[nomPattern]=loadPattern(nomPattern)
    return dictPatterns

#Création des fichiers csv pour l'export de résultats
def transcriptionCsv(pattern):
    path="Resultats/csv/"+pattern.nom+".csv"
    with open(path, mode='w') as fichierCsv:
        CsvWriter = csv.writer(fichierCsv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        CsvWriter.writerow(['Pattern','Jours','Temps max','Souris','Essai','Distance','Issue','Temps'])
        CsvWriter.writerow([pattern.nom,pattern.nbJours,time.strftime("%M:%S",pattern.tempsMax)])
        for nomSouris in pattern.dictSouris:
            souris=pattern.dictSouris[nomSouris]
            CsvWriter.writerow([' ',' ',' ',nomSouris])
            for nomEssai in souris.dictEssais:
                essai=souris.dictEssais[nomEssai]
                if(essai.isE2):
                    distance=abs(essai.placementPot1-essai.placementPot2)
                    CsvWriter.writerow([' ',' ',' ',' ',nomEssai,distance,essai.issue,essai.temps])
                else:
                    CsvWriter.writerow([' ',' ',' ',' ',nomEssai,0,essai.issue,essai.temps])

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
    nom="patternTest1"
    nbSouris=2
    nbJours=5
    nbEssais=4
    entrainement=True
    tempsMax="03:00"
    placementPots=[[-3],[-4],[0],[2]]
    pattern = Pattern(nom,nbSouris,nbJours,nbEssais,entrainement,tempsMax,placementPots)
    savePattern(pattern)
    print(pattern.affichage())
    nom="patternTest2"
    nbSouris=4
    nbJours=15
    nbEssais=4
    entrainement=False
    tempsMax="05:30"
    placementPots=[[1,-3.5],[1,-2],[1,-1],[1,0]]
    pattern = Pattern(nom,nbSouris,nbJours,nbEssais,entrainement,tempsMax,placementPots)
    savePattern(pattern)
    print(pattern.affichage())

def testCreationPattern2():
    pattern=loadPattern("patternTest2.json")
    print(pattern.affichage())
    transcriptionTxt(pattern)
    dictTest=dict()
    dictTest=loadAllPatterns()
    for cle in dictTest:
        print(cle)
        print(dictTest[cle].affichage())

#testCreationPattern()
#testCreationPattern2()
