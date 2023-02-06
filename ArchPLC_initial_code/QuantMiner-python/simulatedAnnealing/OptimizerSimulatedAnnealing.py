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
import os

cwd = os.getcwd()
sys.path.append(cwd)
# sys.path.append('C:\\Users\\aalsahee\\python_physical_model\\Saudi\\trace\\Traces\\qtm\\src\\')

from apriori import *
from database import *
from graphicalInterface import *
from solver import *

from solver.RuleOptimizer import RuleOptimizer

class OptimizerSimulatedAnnealing(RuleOptimizer):



    # Tableaux r�pertoriant l'�volution de la qualit� d'une r�gle au fur et � mesure de son optimisation :

    # METTRE CETTE VARIABLE A VRAI POUR AFFICHER UN GRAPHE D'EVOLUTION DE LA QUALITE APRES L'OPTIMISATION D'UNE REGLE :
    m_bAfficherGrapheQualite = False



    def __init__(self):
        self.m_algoRecuitSimule = None
        self.m_parametresReglesQuantitatives = None
        self.m_parametresAlgo = None
        self.m_tQualiteMoyenne = None
        self.m_tQualiteMin = None
        self.m_tQualiteMax = None
        self.__m_iNombreEtapesCalculRegle = 0

        self.m_algoRecuitSimule = None




    def DefinirContexteResolution(self, contexteResolution):
        super().DefinirContexteResolution(contexteResolution)

        if self.m_contexteResolution is None:
            self.m_algoRecuitSimule = None
            return

        self.m_parametresReglesQuantitatives = self.m_contexteResolution.m_parametresReglesQuantitatives
        self.m_parametresAlgo = self.m_contexteResolution.m_parametresTechRecuitSimule
        self.m_algoRecuitSimule = SimulatedAnnealingAlgo(self.m_contexteResolution.m_gestionnaireBD, self.m_parametresAlgo.m_iNombreIterations, self.m_parametresAlgo.m_iNombreSolutionsParalleles)
        self.m_algoRecuitSimule.SpecifierParametresStatistiques(self.m_parametresReglesQuantitatives.m_fMinSupp, self.m_parametresReglesQuantitatives.m_fMinConf, self.m_parametresReglesQuantitatives.m_fMinSuppDisjonctions)

        if m_bAfficherGrapheQualite:
            self.__m_iNombreEtapesCalculRegle = self.m_parametresAlgo.m_iNombreIterations
            self.m_tQualiteMoyenne = [0 for _ in range(self.__m_iNombreEtapesCalculRegle)]
            self.m_tQualiteMin = [0 for _ in range(self.__m_iNombreEtapesCalculRegle)]
            self.m_tQualiteMax = [0 for _ in range(self.__m_iNombreEtapesCalculRegle)]



    #int i not used but needed in abstract class for OptimizerGeneticAlgorithm
    def OptimiseRegle(self, regle, i):
        iNombreItemsQuantitatifs = 0
        iIndiceEtape = 0
        bRegleEstSolide = False
        meilleureRegle = None

        if (m_algoRecuitSimule is None) or (regle is None):
            return False

        iNombreItemsQuantitatifs = regle.CompterItemsGaucheSelonType(Item.ITEM_TYPE_QUANTITATIF) + regle.CompterItemsDroiteSelonType(Item.ITEM_TYPE_QUANTITATIF)

        # Si la r�gle est uniquement qualitative, on ne cherche pas � l'optimiser :
        if iNombreItemsQuantitatifs <= 0:

            regle.EvaluerSiQualitative(self.m_contexteResolution)

            return ((regle.m_fSupport >= self.m_parametresReglesQuantitatives.m_fMinSupp) and (regle.m_fConfiance >= self.m_parametresReglesQuantitatives.m_fMinConf))



        # Calcul de la r�gle optimis�e, sur le sch�ma courant :

        # On indique � l'algorithme la forme de la r�gle qu'il doit optimiser :
        self.m_algoRecuitSimule.SpecifierSchemaRegle(regle)

        self.m_algoRecuitSimule.GenererReglesPotentiellesInitiales()

        condition = True
        while condition:
            self.m_algoRecuitSimule.InitialiserRecuitSimulePourNouvellePasse()

            iIndiceEtape = 0
            while iIndiceEtape<self.m_parametresAlgo.m_iNombreIterations:
                self.m_algoRecuitSimule.NouvelleEtape()

                if m_bAfficherGrapheQualite:
                    self.m_tQualiteMoyenne[iIndiceEtape] = self.m_algoRecuitSimule.CalculerQualiteMoyenne()
                    self.m_tQualiteMin[iIndiceEtape] = self.m_algoRecuitSimule.ObtenirPireQualiteCourante()
                    self.m_tQualiteMax[iIndiceEtape] = self.m_algoRecuitSimule.ObtenirMeilleureQualiteCourante()
                iIndiceEtape += 1

            condition = self.m_algoRecuitSimule.InitierNouvellePasse()

        #change to index 0 for first best rule (changes made in EvaluationBaseAlgorithm.java to display top n rules per association for genetic algorithm)
        meilleureRegle = self.m_algoRecuitSimule.ObtenirMeilleureRegle(0)

        if meilleureRegle is not None:
            bRegleEstSolide = ((meilleureRegle.m_fSupport >= self.m_parametresReglesQuantitatives.m_fMinSupp) and (meilleureRegle.m_fConfiance >= self.m_parametresReglesQuantitatives.m_fMinConf))
            if bRegleEstSolide:
                regle.CopierRegleAssociation(meilleureRegle)
        else:
            bRegleEstSolide = False


        if m_bAfficherGrapheQualite:
            fenetreDetailsRegle = None
            fenetreDetailsRegle = DialogGraphQuality(self.m_contexteResolution.m_fenetreProprietaire, True, self.m_contexteResolution)
            fenetreDetailsRegle.SpecifierQualitesMoyennes(self.m_tQualiteMoyenne)
            fenetreDetailsRegle.SpecifierQualitesMax(self.m_tQualiteMax)
            fenetreDetailsRegle.SpecifierQualitesMin(self.m_tQualiteMin)
            fenetreDetailsRegle.ConstruireGraphe()
            fenetreDetailsRegle.show()


        return bRegleEstSolide

