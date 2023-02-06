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
import sys
sys.path.append('C:\\Users\\Administrator\\Desktop\\qtm\\src\\')

from database import *
from apriori_solver import *
from graphicalInterface.TableEvolvedCells import *
from graphicalInterface.DatabasePanelAssistant import DatabasePanelAssistant
# from solver import *
from tools import *
# from database.DatabaseAdmin import DatabaseAdmin
from database.onefile import DatabaseAdmin
import pandas as pd


# Prise en compte des informations entr�es :
# t = {'Attributes': ["C1", "C2", "C3"], 'Type': ["Numerical", "Categorical", "Categorical"], 'Consider': [True, True, True]}
# tableModel = pd.DataFrame(data=t) 
tableModel = []

class PanelPreLoadDB(DatabasePanelAssistant):
    def __init__(self, contexteResolution):
        self.m_gestionnaireBD = None
        self.m_modeleColonnesInitiales = None

        super().__init__(contexteResolution)

        sInfosBase = None
        # A TableColumn represents all the attributes of a column in a JTable, 
        # such as width, resizibility, minimum and maximum width
        colonneTableau = None

        self.m_gestionnaireBD = self.m_contexteResolution.m_gestionnaireBD

        if self.m_gestionnaireBD is None:
            print("m_gestionnaireBD is None!")
            return

        self.m_gestionnaireBD.LibererDonneesEnMemoire() #release data column

        sInfosBase = "Database " + self.m_gestionnaireBD.ObtenirNomBaseDeDonnees()
        sInfosBase += ",   " + str(self.m_gestionnaireBD.ObtenirNombreLignes()) + " records."
        print(sInfosBase)

        self.__InitialiserContenuPanneau() #initialize the content of the panel of first step
        # print("$$$$$$$$$$$$$")
        # super().DefinirEtape(1, "Attributes selection from the database", ENV.REPERTOIRE_AIDE+"pre_loading.htm") #define step
        # super().DefinirPanneauPrecedent(MainWindow.PANNEAU_AUCUN) #since this is the first step's panel, no previous panel exist
        # super().DefinirPanneauSuivant(MainWindow.PANNEAU_PRE_EXTRACION) #next panel is the second step panel
        # super().initBaseComponents()

        self.TraitementsSpecifiquesAvantSuivant()
        


    class DefaultTableModelAnonymousInnerClass():
        def __init__(self, outerInstance):
            self.__outerInstance = outerInstance
            self.names = ["Attributes", "Type", "Consider"]
            self.types = ["str", "str", "bool"]
            self.canEdit = [False, True, True]

        def getColumnName(self, columnIndex):
            return self.names[columnIndex]

        def getColumnClass(self, columnIndex):
            return self.types[columnIndex]

        def isCellEditable(self, rowIndex, columnIndex):
            return self.canEdit [columnIndex]

    #    *
    #     * Initialize panel contents
    #     
    def __InitialiserContenuPanneau(self):
        global tableModel

        # tableModel = None
        iNombreLignes = 0
        iIndiceLigne = 0
        iNombreColonnes = 0
        iIndiceColonne = 0
        sNomColonne = None

        iNombreColonnes = self.m_gestionnaireBD.ObtenirNombreColonnesBDInitiale() #get the initial number of columns

        if iNombreColonnes == 0:
            return

        # # start to delete all existed lines one by one:
        # iNombreLignes = len(tableModel.index) # lines count
        # # print(iNombreLignes)
        # for iIndiceLigne in range(0, iNombreColonnes):
        #     print("iIndiceLigne: " + str(iIndiceLigne))
        #     tableModel.drop(iIndiceLigne)

        # tableModel = self.m_gestionnaireBD.csvParser.m_data[0]

        # Filling of the table with the list of column names available in total in the DB:
        iIndiceColonne = 0
        while iIndiceColonne < iNombreColonnes:
            ligneDonnees = [None for _ in range(3)]
            sNomColonne = self.m_gestionnaireBD.ObtenirNomColonneBDInitiale(iIndiceColonne) #Set column name

            #Attribute name
            ligneDonnees[0] = str(sNomColonne)

            #Attribute type
            if self.m_gestionnaireBD.ObtenirTypeColonne(sNomColonne) == DatabaseAdmin.TYPE_VALEURS_COLONNE_REEL: #Set column type
                ligneDonnees[1] = "Numerical" #column type is numerical
            else:
                ligneDonnees[1] = "Categorical" #column type is categorical

            #Consider
            #consider this column or not, during initialization, it is true, we set all as selected
            #due to the call of PrendreEnCompteToutesLesColonnes() in FenetrePrincipale
            ligneDonnees[2] = bool(self.m_gestionnaireBD.EstPriseEnCompteColonne(sNomColonne))

            # tableModel.loc[len(tableModel)] = ligneDonnees
            # tableModel.addRow(ligneDonnees)
            tableModel.append(ligneDonnees)
            iIndiceColonne += 1


    # Overriding the parent method to update the data structures
    # according to what has been entered in the control fields:
    def SychroniserDonneesInternesSelonAffichage(self):
        global tableModel

        # tableModel = None
        lignesTableauVector = None
        elementsLigneVector = None
        lignesTableauEnum = []
        elementsLigneEnum = None
        sNomColonneDonnees = None
        sTypeDonnees = None
        priseEnCompteColonne = None
        iTypeColonneDonnees = 0
        bPrendreEnCompte = False

        #Returns the Vector of Vectors that contains the table's data values.
        # for index, row in tableModel.iterrows():
        #     lignesTableauEnum.append((row['Attributes'], row['Type'], row['Consider']))
        for row in tableModel:
            lignesTableauEnum.append((row[0], row[1], row[2]))
        
        # Line enumeration:
        for line in lignesTableauEnum:
            #Returns an enumeration of the components of this vector
            for elementsLigneVector in line:
                # Interpretation of each of the elements of the current line:
                try:
                    sNomColonneDonnees = str(elementsLigneVector[0])
                    sTypeDonnees = str(elementsLigneVector[1])
                    priseEnCompteColonne = bool(elementsLigneVector[2])
    
                    bPrendreEnCompte = False
                    iTypeColonneDonnees = DatabaseAdmin.TYPE_VALEURS_COLONNE_ERREUR
                    
                    if sTypeDonnees == "Categorical":
                        iTypeColonneDonnees = DatabaseAdmin.TYPE_VALEURS_COLONNE_ITEM
                    elif sTypeDonnees == "Numerical":
                        iTypeColonneDonnees = DatabaseAdmin.TYPE_VALEURS_COLONNE_REEL
    
                    bPrendreEnCompte = bool(priseEnCompteColonne) and (iTypeColonneDonnees != DatabaseAdmin.TYPE_VALEURS_COLONNE_ERREUR)
    
                    # We tell the database manager if we take the attribute into account when
                    # of the rule extraction, and if this is the case we specify its type:
                    self.m_gestionnaireBD.DefinirPriseEnCompteColonne(sNomColonneDonnees, iTypeColonneDonnees, bPrendreEnCompte)
                except Exception as e:
                    pass

        return True


    #    *The process before going to next step. Here will read data
    #     
    def TraitementsSpecifiquesAvantSuivant(self):
        #if data sync failed
        if not self.SychroniserDonneesInternesSelonAffichage():
            return False

        #if the number checked in step 1 is zero
        if self.m_gestionnaireBD.ObtenirNombreColonnesPrisesEnCompte() == 0:
            # Afficher message erreur !!!
            return False
        
        #Load data
        self.m_gestionnaireBD.ChargerDonneesPrisesEnCompte()
        # GenerateDataStructuresAccording toBDPriseInAccount
        self.m_contexteResolution.GenererStructuresDonneesSelonBDPriseEnCompte()
        # print("#######")
        return True


