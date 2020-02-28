#TODO afficher les patterns dans les Resultats
#TODO resize l'affichage dans selection pattern
#TODO supression de patterns/resultats
#TODO créer le txt avec le bouton export
#TODO gestion du placement des pots
#TODO temps init à 05:00

import os
import time
import json

class Souris():

    def __init__(self,nom):
        self.nom = nom
        self.dictEssais = dict()
    def ajouterEssai(self,cle,essais):
        self.dictEssais[cle]=essais

    def affichage(self):
        affichage="\n  nom: "+self.nom
        affichage+="\n  dictEssais: {"
        for cle in self.dictEssais:
            affichage += "\n    "+cle+": "+self.dictEssais[cle].affichage()
        affichage += "\n  }"
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
    issue=0
    isE2=False;

    def __init__(self,placementPot1):
        self.placementPot1=placementPot1

    def start(self):
        print("rien")

    def stop(self):
        print("rien")

    def affichage(self):
        affichage="\n      placementPot1: "+str(self.placementPot1)
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
        if(self.issue==0): return "pas commencé"
        if(self.issue==1): return "   réussi   "
        if(self.issue==2): return "temps écoulé"

class EssaiE2():
    temps="00:00"
    placementPot1=0
    placementPot2=0
    issue=0
    isE2=True;

    def __init__(self,placementPot1,placementPot2):
        self.placementPot1=placementPot1
        self.placementPot2=placementPot2

    def start(self):
        print("rien")

    def stop(self):
        print("rien")

    def affichage(self):
        affichage="\n      placementPot1: "+str(self.placementPot1)
        affichage+="\n      placementPot2: "+str(self.placementPot2)
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
            if(self.issue==0): return "pas commencé"
            if(self.issue==1): return "   réussi   "
            if(self.issue==2): return "temps écoulé"
            if(self.issue==3): return "   échoué   "

class Pattern():

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
        self.dictSouris=dict()
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
        patternDict = {
        "nom":self.nom,
        "nbSouris":self.nbSouris,
        "nbJours":self.nbJours,
        "nbEssais":self.nbEssais,
        "entrainement":self.entrainement,
        "tempsMax":time.strftime("%M:%S",self.tempsMax),
        "dateDebut":self.dateDebut,
        "placementPots":self.placementPots,
        "sourisDict":sourisDict
        }
        return patternDict

#fonction de sauvegarde de pattern avec la bibliothèque pickle
def savePattern(pattern):
    patternDict=pattern.toJson()
    path="Resultats/json/"+pattern.nom+".json"
    with open(path,'w') as fichierPattern:
        #patternPickler=pickle.Pickler(fichierPattern)
        json.dump(patternDict,fichierPattern)
    #fichierPattern.close()

#fonction de chargement de pattern
def loadPattern(nomFichier):
    path="Resultats/json/"+nomFichier
    with open(path,'r') as fichierPattern:
        patternDict = json.load(fichierPattern)
    nom=patternDict["nom"]
    nbSouris=patternDict["nbSouris"]
    nbJours=patternDict["nbJours"]
    nbEssais=patternDict["nbEssais"]
    entrainement=patternDict["entrainement"]
    tempsMax=patternDict["tempsMax"]
    dateDebut=patternDict["dateDebut"]
    placementPots=patternDict["placementPots"]
    dictSouris=dict()
    for nomSouris in patternDict["sourisDict"]:
        souris=patternDict["sourisDict"][nomSouris]
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
    pattern = Pattern(nom,0,nbJours,nbEssais,entrainement,tempsMax,placementPots)
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
    print(listeFichiersPatterns)
    for nomPattern in listeFichiersPatterns:
        print(nomPattern)
        dictPatterns[nomPattern]=loadPattern(nomPattern)
    return dictPatterns

def transcriptionTxt(pattern):
    path="Resultats/txt/"+pattern.nom+".txt"
    fichierTxt=open(path,'w')
    texte="Pattern: "+pattern.nom
    texte+="\n________________________________________"
    texte+="\nnombre de souris: "+str(pattern.nbSouris)
    texte+="\nnombre de jours: "+str(pattern.nbJours)
    texte+="\nnombre d'essais par experience: "+str(pattern.nbJours)
    if(pattern.entrainement):
        texte+="\nmode: entrainement"
    if(not(pattern.entrainement)):
        texte+="\nmode: expérimentation"
    texte+="\ntemps maximum: "+time.strftime("%M:%S",pattern.tempsMax)
    texte+="\ndate de début: "+pattern.dateDebut
    texte+="\n________________________________________"
    for nomSouris in pattern.dictSouris:
        texte+="\n souris "+nomSouris+" :\n"
        for nomEssai in pattern.dictSouris[nomSouris].dictEssais:
            essai = pattern.dictSouris[nomSouris].dictEssais[nomEssai]
            texte+="\n    | essai "+nomEssai+"| "
            texte+="issue: "+essai.issueToString()+"| "
            texte+="temps: "+essai.temps+"| "
            texte+="pot1: "+str(essai.placementPot1)+"| "
            if(essai.isE2):
                texte+="pot2: "+str(essai.placementPot2)+"| "
            texte+="\n    ___________________________________________________"
        texte+="\n"
    fichierTxt.write(texte)
    fichierTxt.close()

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

testCreationPattern()
testCreationPattern2()
