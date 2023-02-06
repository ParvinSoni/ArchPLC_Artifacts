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

from solver.EvaluationBaseAlgorithm import EvaluationBaseAlgorithm

class SimulatedAnnealingAlgo(EvaluationBaseAlgorithm):




    def __init__(self, gestionBD, iNombreEtapes, iNombreReglesParalleles):
        self.__m_tReglesPotentiellesPrecedentes = None
        self.__m_fTemperature = 0.0
        self.__m_iNombreEtapes = 0

        super().__init__(iNombreReglesParalleles, gestionBD)

        self.__m_iNombreEtapes = iNombreEtapes



    def GenererReglesPotentiellesInitiales(self):
        super().GenererReglesPotentiellesInitiales()

        self.__m_tReglesPotentiellesPrecedentes = [None for _ in range(self.m_iNombreReglesPotentielles)]

        self.InitialiserRecuitSimulePourNouvellePasse()



    def InitialiserRecuitSimulePourNouvellePasse(self):
        iIndiceReglePotentielle = 0

        # M�morisation de la solution courante :
        iIndiceReglePotentielle = 0
        while iIndiceReglePotentielle<self.m_iNombreReglesPotentielles:
            self.__m_tReglesPotentiellesPrecedentes[iIndiceReglePotentielle] = ReglePotentielle(self, self.m_iDimension, self.m_iNombreTotalIntervalles)
            self.__m_tReglesPotentiellesPrecedentes[iIndiceReglePotentielle].Copier(self.m_tReglesPotentielles[iIndiceReglePotentielle])
            iIndiceReglePotentielle += 1

        self.__m_fTemperature = 1.0



    def NouvelleEtape(self):
        iIndiceDimension = 0
        iIndiceDisjonction = 0
        iNombreValeursDomaine = 0
        iIndiceValeurDomaineMin = None
        iIndiceValeurDomaineMax = 0
        iIndiceReglePotentielle = 0
        iNombreDisjonctions = 0
        iIndiceIntervalle = 0
        colonneDonnees = None
        reglePotentielle = None
        fAmplitude = 0.0

        iIndiceReglePotentielle = 0
        while iIndiceReglePotentielle<self.m_iNombreReglesPotentielles:

            self.m_tReglesPotentielles[iIndiceReglePotentielle].Copier(self.__m_tReglesPotentiellesPrecedentes[iIndiceReglePotentielle])
            reglePotentielle = self.m_tReglesPotentielles[iIndiceReglePotentielle]


            fQualiteMax = self.m_iNombreTransactions - self.m_fMinConf * float(reglePotentielle.m_iSupportCond)

            i = self.m_iNombreTransactions - int((self.m_fMinConf*float(self.m_iNombreTransactions)))

            #            if (reglePotentielle.m_iSupportRegle > (int)(m_fMinConf*(float)reglePotentielle.m_iSupportCond))
            #                fAmplitude = ((float)iNombreValeursDomaine) * 0.2 * (1.0 - ( ((float)Math.abs(reglePotentielle.m_iSupportRegle - (int)(m_fMinConf*(float)reglePotentielle.m_iSupportCond))) / ((float)i) ))
            #            else
            #                fAmplitude = ((float)iNombreValeursDomaine) * 0.2 + 0.8 * (1.0 - ((float)reglePotentielle.m_iSupportRegle) / ((float)m_iNombreTransactions) )
            #    


            # Si la confiance est �lev�e, on tente d'augmenter le support en augmentant la taille
            # des intervalles 




            if reglePotentielle.m_iSupportRegle > int((self.m_fMinSupp*float(iNombreValeursDomaine))):
                if reglePotentielle.m_iSupportRegle > int((self.m_fMinConf*float(reglePotentielle.m_iSupportCond))):
                    fAmplitude = 0.2 * (1.0 - ((float(abs(reglePotentielle.m_iSupportRegle - int((self.m_fMinConf*float(reglePotentielle.m_iSupportCond)))))) / (float(i))))
                else:
                    fAmplitude = 0.2 + 0.8 * (1.0 - (float(reglePotentielle.m_iSupportRegle)) / (float(self.m_iNombreTransactions)))
            else:
                fAmplitude = 0.2 + 0.8 * (1.0 - (float(reglePotentielle.m_iSupportRegle)) / (float(self.m_iNombreTransactions)))



            fAmplitude = self.__m_fTemperature


            iNombreDimensionsEffectives = 0
            #            
            #            if (m_bPrendreEnCompteQuantitatifsGauche && m_bPrendreEnCompteQuantitatifsDroite)
            #                iNombreDimensionsEffectives = m_iDimension
            #            else if (m_bPrendreEnCompteQuantitatifsGauche)
            #                iNombreDimensionsEffectives = m_iNombreItemsQuantCond;                
            #            else
            #                iNombreDimensionsEffectives = m_iNombreItemsQuantObj
            #            
            #            iIndiceDimension = (int)( m_tRandomFloat[(int)((m_compteurRandomFloat++)&0xFFFF)] * ((float)iNombreDimensionsEffectives) )
            #            
            #            if (m_bPrendreEnCompteQuantitatifsDroite && (!m_bPrendreEnCompteQuantitatifsGauche) )
            #                iIndiceDimension += m_iNombreItemsQuantCond
            #                

            iIndiceDimension = 0
            while iIndiceDimension<self.m_iDimension:

                if (self.m_bPrendreEnCompteQuantitatifsGauche and (iIndiceDimension<self.m_iNombreItemsQuantCond)) or (self.m_bPrendreEnCompteQuantitatifsDroite and (iIndiceDimension>=self.m_iNombreItemsQuantCond)):
                    if m_tRandomFloat[int(((m_compteurRandomFloat)&0xFFFF))] > 0.5:
                        m_compteurRandomFloat += 1

                        if iIndiceDimension<self.m_iNombreItemsQuantCond:
                            colonneDonnees = self.m_tItemsQuantCond[iIndiceDimension].m_colonneDonnees
                            iIndiceIntervalle = iIndiceDimension * self.m_schemaRegleOptimale.m_iNombreDisjonctionsGauche + self.m_iDisjonctionGaucheCourante
                            iIndiceDisjonction = self.m_iDisjonctionGaucheCourante
                        else:
                            colonneDonnees = self.m_tItemsQuantObj[iIndiceDimension-self.m_iNombreItemsQuantCond].m_colonneDonnees
                            iIndiceIntervalle = self.m_iDebutIntervallesDroite + ((iIndiceDimension-self.m_iNombreItemsQuantCond)*self.m_schemaRegleOptimale.m_iNombreDisjonctionsDroite) + self.m_iDisjonctionDroiteCourante
                            iIndiceDisjonction = self.m_iDisjonctionDroiteCourante

                        iNombreValeursDomaine = colonneDonnees.m_iNombreValeursReellesCorrectes

                        iIndiceValeurDomaineMin = reglePotentielle.m_tIndiceMin[iIndiceIntervalle]
                        iIndiceValeurDomaineMax = reglePotentielle.m_tIndiceMax[iIndiceIntervalle]
                        iIndiceValeurDomaineMin += int(((m_tRandomFloat[int(((m_compteurRandomFloat)&0xFFFF))] - 0.5) * fAmplitude*(float(iNombreValeursDomaine))))
                        m_compteurRandomFloat += 1
                        iIndiceValeurDomaineMax += int(((m_tRandomFloat[int(((m_compteurRandomFloat)&0xFFFF))] - 0.5) * fAmplitude*(float(iNombreValeursDomaine))))
                        m_compteurRandomFloat += 1

                        self.VerifierEtAffecterBornesReglePotentielle(reglePotentielle, iIndiceDimension, iIndiceDisjonction, iIndiceValeurDomaineMin, iIndiceValeurDomaineMax)

                    else:
                        m_compteurRandomFloat += 1

                iIndiceDimension += 1

            self.m_tReglesPotentiellesAEvaluer[self.m_iNombreReglesPotentiellesAEvaluer] = reglePotentielle
            self.m_iNombreReglesPotentiellesAEvaluer += 1

            iIndiceReglePotentielle += 1


        super().EvaluerReglesPotentielles()


        iIndiceReglePotentielle = 0
        while iIndiceReglePotentielle<self.m_iNombreReglesPotentielles:

            reglePotentielle = self.m_tReglesPotentielles[iIndiceReglePotentielle]
            if reglePotentielle.m_fQualite >= self.__m_tReglesPotentiellesPrecedentes[iIndiceReglePotentielle].m_fQualite:
                self.__m_tReglesPotentiellesPrecedentes[iIndiceReglePotentielle].Copier(reglePotentielle)

            if reglePotentielle.m_fQualite >= self.m_meilleureReglePotentielle[0].m_fQualite:
                self.m_meilleureReglePotentielle[0].Copier(reglePotentielle)

            iIndiceReglePotentielle += 1

        self.__m_fTemperature -= 1.0 / float(self.__m_iNombreEtapes)

