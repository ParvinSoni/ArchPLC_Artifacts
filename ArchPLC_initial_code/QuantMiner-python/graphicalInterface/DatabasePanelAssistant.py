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

from apriori_solver import *
from graphicalInterface.DatabasePanel import DatabasePanel

PANNEAU_AUCUN = 0
PANNEAU_DEFAUT = 1
PANNEAU_PRE_CHARGEMENT_BD = 2
PANNEAU_PRE_EXTRACION = 3
PANNEAU_CONFIG_TECHNIQUE = 4
PANNEAU_RESULTATS = 6
PANNEAU_TECH_GENERIQUE = 7

class DatabasePanelAssistant(DatabasePanel):
    # Defines the zone in which the wizard-specific controls should be located:
    # * Creates new form PanelBase
    def __init__(self, contexteResolution):
        self.m_contexteResolution = None
        self.__m_iPanneauPrecedent = PANNEAU_AUCUN
        self.__m_iPanneauSuivant = PANNEAU_AUCUN
        self.__m_iNumeroEtape = 0
        self.__m_sIntituleEtape = None
        self.__m_sFichierAide = None
        self.__m_indicateurEtape = None
        self.m_zoneControles = None
        self.__jButtonPrecedent = None
        self.__jButtonSuivant = None

        self.m_contexteResolution = contexteResolution
        self.__m_iPanneauPrecedent = PANNEAU_AUCUN
        self.__m_iPanneauSuivant = PANNEAU_AUCUN

        self.m_zoneControles = None


        
    def DefinirEtape(self, iNumeroEtape, sIntituleEtape, sFichierAide):
        self.__m_iNumeroEtape = iNumeroEtape #the order of that step e.g. first step, second step
        self.__m_sIntituleEtape = sIntituleEtape #title of step
        self.__m_sFichierAide = sFichierAide #file aid



    def DefinirPanneauPrecedent(self, iPanneau):
        self.__m_iPanneauPrecedent = iPanneau


    #Define the next panel 
    def DefinirPanneauSuivant(self, iPanneau):
        self.__m_iPanneauSuivant = iPanneau

    def __jButtonSuivantActionPerformed(self, evt):

        # We carry out the necessary specific treatments:
        # preprocess before going to next step
        if not self.TraitementsSpecifiquesAvantSuivant():
            return

        # Go to subsequent panel :
        if self.m_contexteResolution is not None:
            self.m_contexteResolution.m_fenetreProprietaire.ActiverPanneau(self.__m_iPanneauSuivant)

    def __jButtonPrecedentActionPerformed(self, evt):

        if not self.TraitementsSpecifiquesAvantPrecedent():
            return

        # We go back to the previous panel:
        if self.m_contexteResolution is not None:
            self.m_contexteResolution.m_fenetreProprietaire.ActiverPanneau(self.__m_iPanneauPrecedent)


    # Method to override in the daughter class to perform some processing before moving on to the next panel:
    def TraitementsSpecifiquesAvantSuivant(self):
        return self.SychroniserDonneesInternesSelonAffichage()



    # Method to override in the daughter class to perform some processing before returning to the previous panel:
    def TraitementsSpecifiquesAvantPrecedent(self):
        return self.SychroniserDonneesInternesSelonAffichage()
