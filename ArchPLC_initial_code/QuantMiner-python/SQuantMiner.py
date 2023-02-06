#                                             
# *Copyright 2007, 2011 CCLS Columbia University (USA), LIFO University of Orl��ans (France), BRGM (France)
# *
# *Authors: Cyril Nortet, Xiangrong Kong, Ansaf Salleb-Aouissi, Christel Vrain, Daniel Cassard
# *
# *This file is part of QuantMiner.
# *
# *QuantMiner is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.
# *
# *QuantMiner is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# *
# *You should have received a copy of the GNU General Public License along with QuantMiner.  If not, see <http://www.gnu.org/licenses/>.
# 
#
# * Realized by:
# * Students: Cyril Nortet and Xiangrong Kong
# * Advisors: Ansaf Salleb-Aouissi (CCLS, Columbia University)
# * 		     Christel Vrain (LIFO, University of Orleans)
# *           Daniel Cassard (BRGM, France)
# 
import sys
from os.path import exists
import os

cwd = os.getcwd()
sys.path.append(cwd)
# sys.path.append('C:\\Users\\aalsahee\\python_physical_model\\Saudi\\trace\\Traces\\qtm\\src\\')

import time
from apriori_solver.onefile import *
from geneticAlgorithm import *
from graphicalInterface.PanelPreLoadDB import PanelPreLoadDB
from graphicalInterface.PanelPreExtraction import PanelPreExtraction
from graphicalInterface.PanelTechnConfig import PanelTechnConfig
from graphicalInterface.PanelResults import PanelResults
from graphicalInterface.PanelGenetic import PanelGenetic
from tools import *
from database.onefile import DatabaseAdmin
from database.onefile import CsvFileParser
from graphicalInterface.TreeTable.AttributsBDModel import AttributsBDModel

# miningAlgorithm = ResolutionContext.TECHNIQUE_APRIORI_QUAL
miningAlgorithm = ResolutionContext.TECHNIQUE_ALGO_GENETIQUE


actuator_f = "input/actuator.txt"
actuator_file = open(actuator_f, "r")
actuator = actuator_file.readlines()[0].strip()
actuator_file.close()

print("Actuator: " + actuator)

PANNEAU_AUCUN = 0
PANNEAU_DEFAUT = 1
PANNEAU_PRE_CHARGEMENT_BD = 2
PANNEAU_PRE_EXTRACION = 3
PANNEAU_CONFIG_TECHNIQUE = 4
PANNEAU_RESULTATS = 6
PANNEAU_TECH_GENERIQUE = 7

CONSIDER = {}
ColumnType = {}

start_time = time.time()


class QuantMiner(object):

    # def __init__(self):
    #     pass

    def printRules(self):
        if not self.m_contexteResolution.m_listeRegles is None:
            print(self.m_contexteResolution.m_listeRegles)
            print("$$$$$$$$")

    def __init__(self):
        self.m_panneauCourant = None
        self.m_iPanneauCourant = 0
        self.m_contexteResolution = None
        self.__aProposMenuItem = None
        self.__chargeProfilMenuItem = None
        self.__fermeMenuItem = None
        self.__jMenuItemInfosRegles = None
        self.__jMenuItemParametrage = None
        self.__jMenuOutils = None
        self.__jMenuProfils = None
        self.__menuAide = None
        self.__menuFichier = None
        self.__menuPrincipal = None
        self.__ouvrirAideMenuItem = None
        self.__ouvrirMenuItem = None
        self.__panneauPrincipal = None
        self.__quitteMenuItem = None
        self.__sauveProfilMenuItem = None
        self.o_config_file1_name = None
        self.o_config_file1 = None
    
        dimensionEcran = None
        iconeFenetre = None
    
        self.m_contexteResolution = None
        self.m_iPanneauCourant = PANNEAU_AUCUN

       #*Open File menu item clicked 
    def load_csv_file(self, path):
        sFichierChoisi = path #absolute path of the file
        gestionnaireBD = None

        description = []
        description.append("File DBase 4")
        description.append("File csv")
        extention = []
        extention.append("dbf")
        extention.append("csv")

        # sFichierChoisi = ToolsInterface.DialogOuvertureFichier(self, ENV.CHEMIN_DERNIERE_BASE_OUVERTE, description, extention)

        if sFichierChoisi is not None:
            
            index = sFichierChoisi.rfind('.')
            if index < 0:
                return
            extension = sFichierChoisi[index + 1:len(sFichierChoisi)].lower()

            # BD manager
            gestionnaireBD = DatabaseAdmin(sFichierChoisi, extension)
            # sys.exit()
            print("QuantMiner " + gestionnaireBD.m_sNomBaseDeDonnees)

            # IsDataBaseValid
            if gestionnaireBD.EstBaseDeDonneesValide():
                # ENV.CHEMIN_DERNIERE_BASE_OUVERTE = sFichierChoisi

                # m_current_panel
                if self.m_panneauCourant is not None:
                    if not self.m_panneauCourant.AnnulerPanneau(): # CancelPanel
                        return

                self.m_contexteResolution = ResolutionContext(self)
                self.m_contexteResolution.m_gestionnaireBD = gestionnaireBD
                # #In step 1, at the beginning, all columns are selected, and we also get to know column type due to AnalyserTypesChampsBD()
                # TakeAllColumns
                self.m_contexteResolution.m_gestionnaireBD.PrendreEnCompteToutesLesColonnes()
            else:
                print(None, "An error occured while loading the database. QuantMiner supports only table in DBF or CSV format. Use Excel for example to generate such tables.", "Error", JOptionPane.ERROR_MESSAGE) #GEN-LAST:event_ouvrirMenuItemActionPerformed

    def create_config1_file(self):
        global actuator, miningAlgorithm
        global CONSIDER, ColumnType

        print("Creating the config file: " + self.o_config_file1_name)
        self.o_config_file1 = open(self.o_config_file1_name, "w")

        # Get the number of columns that are selected in the first step
        number_of_columns = self.m_contexteResolution.m_gestionnaireBD.ObtenirNombreColonnesPrisesEnCompte() 
        print("Number of columns: " + str(number_of_columns))

        for i in range(0, number_of_columns):
            colonne = self.m_contexteResolution.m_gestionnaireBD.ObtenirColonneBDPriseEnCompte(i)
            sNomColonne = colonne.m_sNomColonne
            # print("\nColumn name: " + sNomColonne)
            CONSIDER[sNomColonne] = False
            ColumnType[sNomColonne] = "C"
            line = sNomColonne + ","
            screen_line = str(i+1) + "- Column " + str(sNomColonne) + ": "
            
            iTypePosition = qt.m_contexteResolution.ObtenirTypePrisEnCompteAttribut(sNomColonne)
            if colonne.m_iTypeValeurs == DatabaseAdmin.TYPE_VALEURS_COLONNE_REEL:
                if not miningAlgorithm == ResolutionContext.TECHNIQUE_APRIORI_QUAL:
                    line += "N,"
                    screen_line += "numerical, "
                    ColumnType[sNomColonne] = "N"
                else:
                    line += "C,"
                    screen_line += "categorical, "
                    ColumnType[sNomColonne] = "C"
            if colonne.m_iTypeValeurs == DatabaseAdmin.TYPE_VALEURS_COLONNE_ITEM:
                line += "C,"
                screen_line += "categorical, "

            if self.m_contexteResolution.m_gestionnaireBD.m_colonnesPrisesEnCompte[i].m_bPrendreEnCompte:
                line += "T"
                screen_line += "considered"
                CONSIDER[sNomColonne] = True
            else:
                line += "F"
                screen_line += "non-considered"
            
            print(screen_line)
            if i == number_of_columns-1:
                self.o_config_file1.write(line)
            else:
                self.o_config_file1.write(line + "\n")

        # print("Re-run the program. If you would like to change the presented configuration, then update the configuration file: " + self.o_config_file1_name + " before proceeding")
        # sys.exit()
        self.o_config_file1.close()

    def load_config1_file(self):
        global actuator, miningAlgorithm
        global CONSIDER, ColumnType

        print("\nLoading the config file: " + self.o_config_file1_name + "\n")
        self.o_config_file1 = open(self.o_config_file1_name)
        lines = self.o_config_file1.readlines()

        # Get the number of columns that are selected in the first step
        number_of_columns = self.m_contexteResolution.m_gestionnaireBD.ObtenirNombreColonnesPrisesEnCompte()
        # print(lines)

        for i in range(0, number_of_columns):
            # print(lines[i])
            print(lines)

            line = lines[i].split(",")
            sNomColonne = line[0]
            screen_line = str(i+1) + "- Column " + str(sNomColonne) + ": "
            CONSIDER[sNomColonne] = False
            ColumnType[sNomColonne] = "C"

            if line[1].upper().strip() == "N":
                if not miningAlgorithm == ResolutionContext.TECHNIQUE_APRIORI_QUAL:
                    ColumnType[sNomColonne] = "N"
                    screen_line += "numerical, "
                    self.m_contexteResolution.m_gestionnaireBD.m_colonnesPrisesEnCompte[i].m_iTypeColonne = DatabaseAdmin.TYPE_VALEURS_COLONNE_REEL
                else:
                    ColumnType[sNomColonne] = "C"
                    screen_line += "categorical, "
                    self.m_contexteResolution.m_gestionnaireBD.m_colonnesPrisesEnCompte[i].m_iTypeColonne = DatabaseAdmin.TYPE_VALEURS_COLONNE_ITEM
            if line[1].upper().strip() == "C":
                screen_line += "categorical, "
                self.m_contexteResolution.m_gestionnaireBD.m_colonnesPrisesEnCompte[i].m_iTypeColonne = DatabaseAdmin.TYPE_VALEURS_COLONNE_ITEM
            
            if line[2].upper().strip() == "T":
                CONSIDER[sNomColonne] = True
                screen_line += "considered"
                self.m_contexteResolution.m_gestionnaireBD.m_colonnesPrisesEnCompte[i].m_bPrendreEnCompte = True
            if line[2].upper().strip() == "F":
                screen_line += "non-considered"
                self.m_contexteResolution.m_gestionnaireBD.m_colonnesPrisesEnCompte[i].m_bPrendreEnCompte = False

            print(screen_line)

        print("\nThe configuration file: " + self.o_config_file1_name + " is loaded.")
        self.o_config_file1.close()

    def check_config1_file(self):
        global actuator

        input_file = self.m_contexteResolution.m_gestionnaireBD.m_sNomBaseDeDonnees
        dot_offset = len(input_file)

        if "." in input_file:
            dot_offset = input_file.find(".")
        self.o_config_file1_name = "output/config1-" + input_file[:dot_offset] + ".cfg"

        file_exists = exists(self.o_config_file1_name)
        if not file_exists:
            self.create_config1_file()
        else:
            self.load_config1_file()

    def create_config2_file(self):
        global actuator

        print("Creating the config file: " + self.o_config_file2_name)
        self.o_config_file2 = open(self.o_config_file2_name, "w")

        # Get the number of columns that are selected in the first step
        number_of_columns = self.m_contexteResolution.m_gestionnaireBD.ObtenirNombreColonnesPrisesEnCompte() 
        print("Number of columns: " + str(number_of_columns))

        for i in range(0, number_of_columns):
            colonne = self.m_contexteResolution.m_gestionnaireBD.ObtenirColonneBDPriseEnCompte(i)
            sNomColonne = colonne.m_sNomColonne

            line = sNomColonne + ","
            screen_line = str(i+1) + "- Column " + str(sNomColonne) + ": "
            
            colonneDonnees = self.m_contexteResolution.m_gestionnaireBD.ObtenirColonneBDPriseEnCompte(i)
            if colonneDonnees is not None:
                sNomColonne = str(colonneDonnees.m_sNomColonne)
                if colonneDonnees.m_iTypeValeurs == DatabaseAdmin.TYPE_VALEURS_COLONNE_REEL:
                    # line += "N,"
                    sDescriptionElement = "[" + str(colonneDonnees.ObtenirBorneMin()) + ";" + str(colonneDonnees.ObtenirBorneMax()) + "]"
                    sDescriptionElement += "," + str(colonneDonnees.m_iNombreLignes-colonneDonnees.m_iNombreValeursReellesCorrectes) + " missing values."
                    screen_line += sDescriptionElement + ", "
                    line += sDescriptionElement # + ","

                    noeudCourant = [sNomColonne, AttributsBDModel.ELEMENT_MODEL_ATTRIBUT_QUANT, sDescriptionElement, self.m_contexteResolution.ObtenirInfosPostionnementRegles(), (colonneDonnees.m_iNombreValeursReellesCorrectes<=0)]
                    print(noeudCourant)
                elif colonneDonnees.m_iTypeValeurs == DatabaseAdmin.TYPE_VALEURS_COLONNE_ITEM:
                    sDescriptionElement = str(colonneDonnees.ObtenirNombreValeursDifferentes()) + " distinct values"
                    
                    line += sDescriptionElement # + ","
                    noeudCourant = [sNomColonne, AttributsBDModel.ELEMENT_MODEL_ATTRIBUT_QUAL, sDescriptionElement, self.m_contexteResolution.ObtenirInfosPostionnementRegles(), False]
                    print(noeudCourant)
                    
            print(screen_line)

            # if not line.endswith(","):
            #     line += ","
            if actuator in line:
                line += ",R,T"
            else:
                line += ",L,F"

            if i == number_of_columns-1:
                self.o_config_file2.write(line)
            else:
                self.o_config_file2.write(line + "\n")

        self.o_config_file2.close()

        # print("Re-run the program. If you would like to change the presented configuration, then update the configuration file: " + self.o_config_file2_name + " before proceeding")
        # sys.exit()

    def load_config2_file(self):
        global actuator
        global CONSIDER, ColumnType

        print("\nLoading the config file: " + self.o_config_file2_name + "\n")
        self.o_config_file2 = open(self.o_config_file2_name)
        lines = self.o_config_file2.readlines()
        
        #Load data
        # self.m_contexteResolution.m_gestionnaireBD.ChargerDonneesPrisesEnCompte()
        # self.m_contexteResolution.GenererStructuresDonneesSelonBDPriseEnCompte()

        # Get the number of columns that are selected in the first step
        number_of_columns = self.m_contexteResolution.m_gestionnaireBD.ObtenirNombreColonnesPrisesEnCompte()
        

        for i in range(0, number_of_columns):
            line = lines[i].split(",")

            colonne = self.m_contexteResolution.m_gestionnaireBD.ObtenirColonneBDPriseEnCompte(i)
            sNomColonne = colonne.m_sNomColonne
            isCategorical = colonne.m_iTypeValeurs == DatabaseAdmin.TYPE_VALEURS_COLONNE_ITEM
            isNumerical = colonne.m_iTypeValeurs == DatabaseAdmin.TYPE_VALEURS_COLONNE_REEL
            isConsider = self.m_contexteResolution.m_gestionnaireBD.m_colonnesPrisesEnCompte[i].m_bPrendreEnCompte

            if not sNomColonne == line[0]:
                print("ERROR: Configuration file 2 does not match!")
                sys.exit()

            side = "L"
            necessarilyPresent = "F"

            if isCategorical:
                side = line[2].strip()
                necessarilyPresent = line[3].strip()
            else:
                side = line[3].strip()
                necessarilyPresent = line[4].strip()

            if side == "I":
                side = ResolutionContext.PRISE_EN_COMPTE_INDEFINI
            elif side == "N":
                side = ResolutionContext.PRISE_EN_COMPTE_ITEM_NULLE_PART
            elif side == "L":
                side = ResolutionContext.PRISE_EN_COMPTE_ITEM_GAUCHE
            elif side == "R":
                side = ResolutionContext.PRISE_EN_COMPTE_ITEM_DROITE
            elif side == "B":
                side = ResolutionContext.PRISE_EN_COMPTE_ITEM_2_COTES

            if necessarilyPresent == "T":
                necessarilyPresent = True
            elif necessarilyPresent == "F":
                necessarilyPresent = False

            print("necessarilyPresent: " + str(necessarilyPresent))

            screen_line = str(i+1) + "- Column " + str(sNomColonne) + ": " + line[1]
            if len(line) > 3:
                screen_line += ", " + line[2]

            print("------------------------------")

            if isConsider and isCategorical:
                print("colonne.m_iTypeValeurs: " + str(colonne.m_iTypeValeurs))

                tListeItems = colonne.ConstituerTableauValeurs() # only works for qualtitaves   
                
                tItems = colonne.ConstituerTableauValeurs()
                if tItems is not None:
                    iIndiceItem = 0
                    while iIndiceItem < len(tItems):
                        self.m_contexteResolution.DefinirTypePrisEnCompteItem(sNomColonne, tListeItems[iIndiceItem], side)
                        iIndiceItem += 1

                tItems = colonne.ConstituerTableauValeurs()
                if tItems is not None:
                    iIndiceItem = 0
                    while iIndiceItem < len(tItems):
                        iTypePriseEnCompte = self.m_contexteResolution.ObtenirTypePrisEnCompteItem(sNomColonne, tItems[iIndiceItem])
                        print("- Quant side: " + getTypePosition(iTypePriseEnCompte))
                        iIndiceItem += 1

                tItems = colonne.ConstituerTableauValeurs()
                if tItems is not None:
                    iIndiceItem = 0
                    while iIndiceItem < len(tItems):
                        sNomColonne = str(colonne.m_sNomColonne)
                        iTypePriseEnCompte = self.m_contexteResolution.ObtenirTypePrisEnCompteItem(sNomColonne, tItems[iIndiceItem])
                        # if iTypePriseEnCompte != ResolutionContext.PRISE_EN_COMPTE_ITEM_NULLE_PART:
                        self.m_contexteResolution.DefinirPresenceObligatoireItem(sNomColonne, tItems[iIndiceItem], necessarilyPresent)
                        bPresenceObligatoire = self.m_contexteResolution.ObtenirPresenceObligatoireItem(sNomColonne, tItems[iIndiceItem])
                        print(bPresenceObligatoire)
                        iIndiceItem += 1

            if isConsider and isNumerical:
                self.m_contexteResolution.DefinirTypePrisEnCompteAttribut(sNomColonne, side)

                iTypePriseEnCompte = self.m_contexteResolution.ObtenirTypePrisEnCompteAttribut(sNomColonne)
                print("Quant side: " + getTypePosition(iTypePriseEnCompte))

        print("\nThe configuration file: " + self.o_config_file2_name + " is loaded.")
        self.o_config_file2.close()

    def check_config2_file(self):
        global actuator

        input_file = self.m_contexteResolution.m_gestionnaireBD.m_sNomBaseDeDonnees
        dot_offset = len(input_file)

        if "." in input_file:
            dot_offset = input_file.find(".")
        self.o_config_file2_name = "output/config2-" + input_file[:dot_offset] + ".cfg"

        file_exists = exists(self.o_config_file2_name)
        if not file_exists:
            self.create_config2_file()
        else:
            self.load_config2_file()

    @staticmethod
    def main(args):
        
        print("This is QuantMiner!")

    def DefaultPanel(self):
        output = "Welcome!"
        # print(output)
        return output

    #    *
    #     * Activate a specific panel
    #     * @param iPanneau panel ID
    #     
    def ActiverPanneau(self, iPanneau):
        if iPanneau == PANNEAU_DEFAUT:
            self.m_panneauCourant = (self.DefaultPanel()) #Default panel

        elif iPanneau == PANNEAU_PRE_CHARGEMENT_BD: #step1
            self.m_panneauCourant = (PanelPreLoadDB(self.m_contexteResolution))

        elif iPanneau == PANNEAU_PRE_EXTRACION: #step2
            self.m_panneauCourant = (PanelPreExtraction(self.m_contexteResolution))

        elif iPanneau == PANNEAU_CONFIG_TECHNIQUE: #step 3 parameter configuration
            self.m_panneauCourant = (PanelTechnConfig(self.m_contexteResolution))

        elif iPanneau == PANNEAU_RESULTATS: #step 5
            if self.m_contexteResolution is None:
                print("m_contexteResolution is null")
            elif self.m_contexteResolution.m_listeRegles is None:
                print("m_contexteResolution.m_listeRegles is null")
            self.m_panneauCourant = (PanelResults(self.m_contexteResolution))


        elif iPanneau == PANNEAU_TECH_GENERIQUE: #step 4
            self.m_panneauCourant = (PanelGenetic(self.m_contexteResolution))

        else:
            iPanneau = PANNEAU_AUCUN
            self.m_panneauCourant = None

        self.m_iPanneauCourant = iPanneau



def getTypePosition(i):
    if i == 0:
        return "PRISE_EN_COMPTE_INDEFINI"
    if i == 1:
        return "PRISE_EN_COMPTE_ITEM_NULLE_PART"
    if i == 2:
        return "PRISE_EN_COMPTE_ITEM_GAUCHE"
    if i == 3:
        return "PRISE_EN_COMPTE_ITEM_DROITE"
    if i == 4:
        return "PRISE_EN_COMPTE_ITEM_2_COTES"

def execQTM(qt, path):
    global miningAlgorithm

    qt.load_csv_file(path)
    # print(qt.m_contexteResolution)
    # qt.ActiverPanneau(PANNEAU_DEFAUT)
    qt.ActiverPanneau(PANNEAU_PRE_CHARGEMENT_BD)
    gestionnaireBD = qt.m_contexteResolution.m_gestionnaireBD
    # print(qt.m_contexteResolution.__m_tableParametresItemsQualitatifs["Class"])

    qt.m_contexteResolution.m_iTechniqueResolution = miningAlgorithm
    
    qt.check_config1_file()
    qt.check_config2_file()
    
    qt.ActiverPanneau(PANNEAU_PRE_EXTRACION)
    
    # Standard Apriori
    # qt.m_contexteResolution.m_iTechniqueResolution = ResolutionContext.TECHNIQUE_APRIORI_QUAL
    # Genetic algorithm
    # qt.m_contexteResolution.m_iTechniqueResolution = ResolutionContext.TECHNIQUE_ALGO_GENETIQUE
    # Simulated annealing
    # qt.m_contexteResolution.m_iTechniqueResolution = ResolutionContext.TECHNIQUE_RECUIT_SIMULE
    # Load a set of precomputed rules
    # qt.m_contexteResolution.m_iTechniqueResolution = ResolutionContext.TECHNIQUE_CHARGEMENT

    
    
    qt.ActiverPanneau(PANNEAU_CONFIG_TECHNIQUE)
    
    qt.ActiverPanneau(PANNEAU_RESULTATS)
    
    qt.ActiverPanneau(PANNEAU_TECH_GENERIQUE)

    # PRISE_EN_COMPTE_INDEFINI = 0 #undefined
    # PRISE_EN_COMPTE_ITEM_NULLE_PART = 1 #no where
    # PRISE_EN_COMPTE_ITEM_GAUCHE = 2 #left side
    # PRISE_EN_COMPTE_ITEM_DROITE = 3 #right side
    # PRISE_EN_COMPTE_ITEM_2_COTES = 4 #two sides

qt = QuantMiner()
qt.main("bye")

# path = "D:\\DELL_LAPTOP_BYE\\aalsahee\\python_physical_model\\Saudi\\trace\\ARCHPLC_EVALUATIONS\\1-IX_Set_Park_Position\\input\\normal_all_removed_types_0.csv"
# execQTM(qt, path)

input_path = 'input'
files = os.listdir(input_path)
for f in files:
    if f.endswith(".txt"):
        continue

    path = cwd + "\\" + input_path + "\\" + f

    qt = QuantMiner()
    qt.main("bye")

    execQTM(qt, path)

    qt = QuantMiner()
    qt.main("bye")

    execQTM(qt, path)

    print("***********")

    # sys.exit()

print("--- %s seconds ---" % (time.time() - start_time))