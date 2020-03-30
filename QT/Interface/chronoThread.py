import sys
from threading import Thread
import time
from PyQt5 import QtWidgets, uic
from gestionStockage import *

#classe qui gère la création d'un second thread pour executer le chrono en parallèle du reste de l'interface
class chronoThread(Thread):

    def __init__(self,interface):
        Thread.__init__(self)
        self.interface=interface

    def run(self):
        start=time.time()
        while(self.interface.menuEssai.chronoRunning):
            actualTime=time.localtime(time.time()-start)
            self.interface.menuEssai.affichageChrono.setText(time.strftime("%M:%S",actualTime))
            #si le temps dépasse le temps max, on active le bouton "Temps écoulé"
            if(actualTime[5]+actualTime[4]*60>=self.interface.patternActuel.tempsMax[5]+self.interface.patternActuel.tempsMax[4]*60):
                self.interface.menuEssai.buttonTempsEcoule.setEnabled(True)
            time.sleep(1)
