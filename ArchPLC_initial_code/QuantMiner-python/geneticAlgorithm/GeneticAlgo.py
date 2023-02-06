import random
import math

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

from apriori_solver.onefile import *
from database import *
# from solver.EvaluationBaseAlgorithm import EvaluationBaseAlgorithm

class GeneticAlgo(EvaluationBaseAlgorithm):

    # Data structures for the optimization of calculations:
    def __CalculerTableIndicesTirages(self):
        iTable = 0
        iTirage = 0
        iPlageRoulette = None
        iPlageRestante = 0
        iIndiceReglePotentielle = 0

        self.__m_tIndicesAleatoiresCroisements = [0 for _ in range(16384)]

        iPlageRoulette = math.trunc((self.m_iNombreReglesPotentielles * (self.m_iNombreReglesPotentielles+1)) / float(2))
        for iTable in range(0, 16384):
            iTirage = int((random.random() * float(iPlageRoulette)))

            # We determine the index of the individual corresponding to the result of the random shot on the beach
            iPlageRestante = iPlageRoulette - self.m_iNombreReglesPotentielles
            iIndiceReglePotentielle = self.m_iNombreReglesPotentielles - 1
            while iTirage<iPlageRestante:
                iPlageRestante -= iIndiceReglePotentielle
                iIndiceReglePotentielle -= 1

            self.__m_tIndicesAleatoiresCroisements[iTable] = iIndiceReglePotentielle

        self.__m_compteurIndicesAleatoiresCroisements = 0


    #    *Genetics Algorithm
    #     * @param iNombreIndividus number of individuals
    #     * @param gestionBD GestionnaireBaseDeDonnees obj
    #     
    def __init__(self, iNombreIndividus, gestionBD):
        self.__m_fTauxCroisement = 0.0
        self.__m_fTauxMutation = 0.0
        self.__m_tIndicesAleatoiresCroisements = None
        self.__m_compteurIndicesAleatoiresCroisements = 0

        super().__init__(iNombreIndividus, gestionBD)

        self.__m_fTauxCroisement = 0.0
        self.__m_fTauxMutation = 0.0

        self.__CalculerTableIndicesTirages()



    #    *Set Genetic parameters
    #     * @param fTauxCroisement Crossover rate
    #     * @param fTauxMutation Mutation rate
    #     
    def SpecifierParametresGenetiques(self, fTauxCroisement, fTauxMutation):
        self.__m_fTauxCroisement = fTauxCroisement
        self.__m_fTauxMutation = fTauxMutation


    #*Do evolution
    def Evoluer(self):
        iIndiceReglePotentielle = 0
        iIndiceReglePotentiellePere = 0
        iIndiceReglePotentielleMere = 0
        iNombreReglesPotentiellesRemplacees = 0
        iPlageRoulette = 0
        reglePotentielleEvolue = None

        #The number of potential rules to be replaced
        iNombreReglesPotentiellesRemplacees = int((float(self.m_iNombreReglesPotentielles) * self.__m_fTauxCroisement))
        self.m_iNombreReglesPotentiellesAEvaluer = 0

        iIndiceReglePotentielle = 0
        while iIndiceReglePotentielle < iNombreReglesPotentiellesRemplacees:

            reglePotentielleEvolue = self.m_tReglesPotentielles[iIndiceReglePotentielle]

            iIndiceReglePotentiellePere = self.__m_tIndicesAleatoiresCroisements[int(((self.__m_compteurIndicesAleatoiresCroisements)&0x3FFF))]
            self.__m_compteurIndicesAleatoiresCroisements += 1
            iIndiceReglePotentielleMere = self.__m_tIndicesAleatoiresCroisements[int(((self.__m_compteurIndicesAleatoiresCroisements)&0x3FFF))]
            self.__m_compteurIndicesAleatoiresCroisements += 1
            # Ancienne technique de choix des parents :
            #iIndiceIndividuPere = iNombreIndividusRemplaces + (int)( (m_tRandomFloat[(int)((m_compteurRandomFloat++)&0xFFFF)]) * ((float)(m_iNombreIndividus-iNombreIndividusRemplaces)) )
            #iIndiceIndividuMere = iNombreIndividusRemplaces + (int)( (m_tRandomFloat[(int)((m_compteurRandomFloat++)&0xFFFF)]) * ((float)(m_iNombreIndividus-iNombreIndividusRemplaces)) )

            #Do crossover
            self.EffectuerCroisement(reglePotentielleEvolue, self.m_tReglesPotentielles[iIndiceReglePotentiellePere], self.m_tReglesPotentielles[iIndiceReglePotentielleMere])

            if EvaluationBaseAlgorithm.m_tRandomFloat[int(((EvaluationBaseAlgorithm.m_compteurRandomFloat)&0xFFFF))] <= self.__m_fTauxMutation:
                EvaluationBaseAlgorithm.m_compteurRandomFloat += 1
                self.EffectuerMutation(reglePotentielleEvolue)
            else:
                EvaluationBaseAlgorithm.m_compteurRandomFloat += 1

            self.m_tReglesPotentiellesAEvaluer[self.m_iNombreReglesPotentiellesAEvaluer] = reglePotentielleEvolue
            self.m_iNombreReglesPotentiellesAEvaluer += 1
            iIndiceReglePotentielle += 1

        #The rest potential rules that haven't been replaced by crossover
        iIndiceReglePotentielle = iNombreReglesPotentiellesRemplacees
        while iIndiceReglePotentielle < self.m_iNombreReglesPotentielles:

            if EvaluationBaseAlgorithm.m_tRandomFloat[int(((EvaluationBaseAlgorithm.m_compteurRandomFloat)&0xFFFF))] <= self.__m_fTauxMutation:
                EvaluationBaseAlgorithm.m_compteurRandomFloat += 1
                reglePotentielleEvolue = self.m_tReglesPotentielles[iIndiceReglePotentielle]
                self.EffectuerMutation(reglePotentielleEvolue)
                self.m_tReglesPotentiellesAEvaluer[self.m_iNombreReglesPotentiellesAEvaluer] = reglePotentielleEvolue
                self.m_iNombreReglesPotentiellesAEvaluer += 1
            else:
                EvaluationBaseAlgorithm.m_compteurRandomFloat += 1
            iIndiceReglePotentielle += 1

        super().EvaluerReglesPotentielles()


    #    * Perform Mutation
    #     * @param reglePotentielle Potential rules
    #     
    def EffectuerMutation(self, reglePotentielle):
        iIndiceDimension = 0
        iIndiceDisjonction = 0
        iNombreValeursDomaine = 0
        iIndiceValeurDomaineMin = None
        iIndiceValeurDomaineMax = 0
        iIndiceIntervalle = 0
        colonneDonnees = None

        iIndiceDimension = 0
        while iIndiceDimension<self.m_iDimension:

            if (self.m_bPrendreEnCompteQuantitatifsGauche and (iIndiceDimension<self.m_iNombreItemsQuantCond)) or (self.m_bPrendreEnCompteQuantitatifsDroite and (iIndiceDimension>=self.m_iNombreItemsQuantCond)):

                if iIndiceDimension<self.m_iNombreItemsQuantCond:
                    colonneDonnees = self.m_tItemsQuantCond[iIndiceDimension].m_colonneDonnees
                    iIndiceIntervalle = iIndiceDimension * self.m_schemaRegleOptimale.m_iNombreDisjonctionsGauche + self.m_iDisjonctionGaucheCourante
                    iIndiceDisjonction = self.m_iDisjonctionGaucheCourante
                else:
                    colonneDonnees = self.m_tItemsQuantObj[iIndiceDimension-self.m_iNombreItemsQuantCond].m_colonneDonnees
                    iIndiceIntervalle = self.m_iDebutIntervallesDroite + ((iIndiceDimension-self.m_iNombreItemsQuantCond)*self.m_schemaRegleOptimale.m_iNombreDisjonctionsDroite) + self.m_iDisjonctionDroiteCourante
                    iIndiceDisjonction = self.m_iDisjonctionDroiteCourante

                iNombreValeursDomaine = colonneDonnees.m_iNombreValeursReellesCorrectes

                if EvaluationBaseAlgorithm.m_tRandomFloat[int(((EvaluationBaseAlgorithm.m_compteurRandomFloat)&0xFFFF))] > 0.5:
                    EvaluationBaseAlgorithm.m_compteurRandomFloat += 1

                    iIndiceValeurDomaineMin = reglePotentielle.m_tIndiceMin[iIndiceIntervalle]
                    iIndiceValeurDomaineMax = reglePotentielle.m_tIndiceMax[iIndiceIntervalle]
                    iIndiceValeurDomaineMin += int(((EvaluationBaseAlgorithm.m_tRandomFloat[int(((EvaluationBaseAlgorithm.m_compteurRandomFloat)&0xFFFF))] - 0.4) * (float(iNombreValeursDomaine)) * 0.05))
                    EvaluationBaseAlgorithm.m_compteurRandomFloat += 1
                    iIndiceValeurDomaineMax += int(((EvaluationBaseAlgorithm.m_tRandomFloat[int(((EvaluationBaseAlgorithm.m_compteurRandomFloat)&0xFFFF))] - 0.6) * (float(iNombreValeursDomaine)) * 0.05))
                    EvaluationBaseAlgorithm.m_compteurRandomFloat += 1

                    self.VerifierEtAffecterBornesReglePotentielle(reglePotentielle, iIndiceDimension, iIndiceDisjonction, iIndiceValeurDomaineMin, iIndiceValeurDomaineMax)
                else:
                    EvaluationBaseAlgorithm.m_compteurRandomFloat += 1


            iIndiceDimension += 1


    #    *Create a new rule potentialRuleChild, child of the crossover of a father rule and a mother rule.
    #     * @param reglePotentielleFille potentialRuleChild
    #     * @param reglePotentiellePere potentialRuleFather
    #     * @param reglePotentielleMere potentialRuleMother
    #     
    def EffectuerCroisement(self, reglePotentielleFille, reglePotentiellePere, reglePotentielleMere):
        iIndiceDimension = 0
        iIndiceIntervalle = 0
        iIndiceDisjonction = 0
        iResultatRoulette = 0

        iIndiceDimension = 0
        while iIndiceDimension<self.m_iDimension:

            if (self.m_bPrendreEnCompteQuantitatifsGauche and (iIndiceDimension<self.m_iNombreItemsQuantCond)) or (self.m_bPrendreEnCompteQuantitatifsDroite and (iIndiceDimension>=self.m_iNombreItemsQuantCond)):

                if iIndiceDimension<self.m_iNombreItemsQuantCond:
                    iIndiceIntervalle = (iIndiceDimension*self.m_schemaRegleOptimale.m_iNombreDisjonctionsGauche) + self.m_iDisjonctionGaucheCourante
                    iIndiceDisjonction = self.m_iDisjonctionGaucheCourante
                else:
                    iIndiceIntervalle = self.m_iDebutIntervallesDroite + ((iIndiceDimension-self.m_iNombreItemsQuantCond)*self.m_schemaRegleOptimale.m_iNombreDisjonctionsDroite) + self.m_iDisjonctionDroiteCourante
                    iIndiceDisjonction = self.m_iDisjonctionDroiteCourante
                    
                iResultatRoulette = int((8.0 * EvaluationBaseAlgorithm.m_tRandomFloat[int(((EvaluationBaseAlgorithm.m_compteurRandomFloat)&0xFFFF))]))
                EvaluationBaseAlgorithm.m_compteurRandomFloat += 1

                if iResultatRoulette == 0:
                    self.VerifierEtAffecterBornesReglePotentielle(reglePotentielleFille, iIndiceDimension, iIndiceDisjonction, reglePotentiellePere.m_tIndiceMin[iIndiceIntervalle], reglePotentiellePere.m_tIndiceMax[iIndiceIntervalle])
                elif iResultatRoulette == 1:
                    self.VerifierEtAffecterBornesReglePotentielle(reglePotentielleFille, iIndiceDimension, iIndiceDisjonction, reglePotentielleMere.m_tIndiceMin[iIndiceIntervalle], reglePotentielleMere.m_tIndiceMax[iIndiceIntervalle])
                elif iResultatRoulette <= 4:
                    self.VerifierEtAffecterBornesReglePotentielle(reglePotentielleFille, iIndiceDimension, iIndiceDisjonction, reglePotentiellePere.m_tIndiceMin[iIndiceIntervalle], reglePotentielleMere.m_tIndiceMax[iIndiceIntervalle])
                else:
                    self.VerifierEtAffecterBornesReglePotentielle(reglePotentielleFille, iIndiceDimension, iIndiceDisjonction, reglePotentielleMere.m_tIndiceMin[iIndiceIntervalle], reglePotentiellePere.m_tIndiceMax[iIndiceIntervalle])
            iIndiceDimension += 1

