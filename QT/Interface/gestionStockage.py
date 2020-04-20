import os
import time
import json
import csv
from glob import glob
from subprocess import check_output, CalledProcessError

#BasePath = "/home/pi/Desktop/Roborongeurs_commun/QT/Interface/" #chemin complet vers le programme sur Raspberry, commenter cette ligne sur PC
BasePath=""
class Souris():

    def __init__(self,nom):
        self.nom = nom
        self.dictEssais = dict()

    def ajouterEssai(self,cle,essais):
        self.dictEssais[cle]=essais

    def affichage(self):
        affichage="\n  souris "+self.nom+" : "
        for cle in sorted(self.dictEssais):
            affichage += "\n    "+cle+" :"+self.dictEssais[cle].affichage()
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

    def affichage(self):
        affichage="\t["+str(self.placementPot1)+"]\t"+self.issueToString()
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
        if(self.issue==1): return "réussi"

class EssaiE2():
    temps="00:00"
    placementPot1=0
    placementPot2=0
    issue=-1
    isE2=True;

    def __init__(self,placementPot1,placementPot2):
        self.placementPot1=placementPot1
        self.placementPot2=placementPot2

    def affichage(self):
        affichage="\t["+str(self.placementPot1)+"|"+str(self.placementPot2)+"]\t"+self.issueToString()
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
            if(self.issue==1): return "réussi"
            if(self.issue==2): return "échoué"

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
        #date actuelle passée au format dd/mm/yyyy
        self.dateDebut=time.strftime("%d/%m/%Y", time.localtime())
        #création d'un dictionnaire [si:Souris] à partir de nbSouris
        self.dictSouris=dict()
        for i in range(0,nbSouris):
            self.ajouterSouris("s"+str(i))

    def ajouterSouris(self,nom):
        self.dictSouris[nom]=Souris(nom)

    def placementPots(self,dictEssais):
        for i in range(0,self.nbSouris):
            #pour chaque souris: création d'un dictionnaire [TjEk:essai] à partir de nbEssais, entrainement et le tableau placementsPots
            self.dictSouris["s"+str(i)].dictEssais=dictEssais
            for nomEssai in self.dictSouris["s"+str(i)].dictEssais:
                self.dictSouris["s"+str(i)].dictEssais[nomEssai].temps="00:00"
                self.dictSouris["s"+str(i)].dictEssais[nomEssai].issue=-1


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

#fonction de sauvegarde de pattern avec la bibliothèque json
def savePattern(pattern):
    patternJson=pattern.toJson()
    path=BasePath+"Resultats/json/"+pattern.nom+".json"
    with open(path,'w') as fichierPattern:
        json.dump(patternJson,fichierPattern)

#fonction de chargement de pattern
def loadPattern(nomFichier):
    path=BasePath+"Resultats/json/"+nomFichier
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
    path=BasePath+"Resultats/json"
    dictPatterns=dict()
    listeFichiersPatterns=os.listdir(path)
    for nomPattern in listeFichiersPatterns:
        dictPatterns[nomPattern]=loadPattern(nomPattern)
    return dictPatterns

#Création des fichiers csv pour l'export de résultats
def transcriptionCsv(pattern,USBpath):
    path=USBpath+"/"+pattern.nom+"_infos.csv"
    path="Resultats/csv/"+pattern.nom+"_infos.csv"
    with open(path, mode='w') as fichierCsv:
        CsvWriter = csv.writer(fichierCsv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        CsvWriter.writerow(['Pattern','Jours','Temps max','nb Souris','nb Essais'])
        CsvWriter.writerow([pattern.nom,pattern.nbJours,time.strftime("%M:%S",pattern.tempsMax),pattern.nbSouris,pattern.nbEssais])
    path=USBpath+"/"+pattern.nom+"_resultats.csv"
    path="Resultats/csv/"+pattern.nom+"_resultats.csv"
    with open(path, mode='w') as fichierCsv:
        CsvWriter = csv.writer(fichierCsv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        CsvWriter.writerow(['Souris','Essai','Pot1','Pot2','Distance(cm)','Issue','Temps(s)'])
        for nomSouris in pattern.dictSouris:
            souris=pattern.dictSouris[nomSouris]
            for nomEssai in sorted(souris.dictEssais):
                essai=souris.dictEssais[nomEssai]
                #temps en secondes
                temps=int(essai.temps[0]+essai.temps[1])*60+int(essai.temps[3]+essai.temps[4])
                if(essai.isE2):
                    #distance entre les pots en cm
                    distance=abs(essai.placementPot1-essai.placementPot2)*15
                    CsvWriter.writerow([nomSouris,nomEssai,essai.placementPot1,essai.placementPot2,distance,essai.issue,temps])
                else:
                    CsvWriter.writerow([nomSouris,nomEssai,essai.placementPot1,"#N/A","#N/A",essai.issue,temps])

#Foctions de détection de cle USB trouvées sur StackOverflow
def get_usb_devices():
    sdb_devices = map(os.path.realpath, glob('/sys/block/sd*'))
    usb_devices = (dev for dev in sdb_devices
    if 'usb' in dev.split('/')[5])
    return dict((os.path.basename(dev), dev) for dev in usb_devices)

def get_mount_points(devices=None):
    devices = devices or get_usb_devices()  # if devices are None: get_usb_devices
    output = check_output(['mount']).splitlines()
    output = [tmp.decode('UTF-8') for tmp in output]

    def is_usb(path):
        return any(dev in path for dev in devices)
    usb_info = (line for line in output if is_usb(line.split()[0]))
    fullInfo = []
    for info in usb_info:
        print(info)
        mountURI = info.split()[0]
        usbURI = info.split()[2]
        print(info.split().__sizeof__())
        for x in range(3, info.split().__sizeof__()):
            if info.split()[x].__eq__("type"):
                for m in range(3, x):
                    usbURI += " "+info.split()[m]
                break
        fullInfo.append([mountURI, usbURI])
    return fullInfo
