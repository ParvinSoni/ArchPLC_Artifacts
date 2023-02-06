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
# from apriori import *
# from apriori.onefile import StandardParameters
from database.onefile import *
from graphicalInterface.Centroid import Centroid
import sys


# Minimal support
DEFAUT_MINSUPP = 0.01 # 0.10
# Minimal confidence
DEFAUT_MINCONF = 1.00 # 0.60

class EvaluationBaseAlgorithm(object):


    class RefItemQualitatif(object):


        def __init__(self, outerInstance, colonneDonnees, iIndiceValeurAttribut, sChaineIdentifiant):
            self.m_colonneDonnees = None
            self.m_iIndiceValeurAttribut = 0
            self.m_sChaineIdentifiantItem = None

            self.__outerInstance = outerInstance

            self.m_colonneDonnees = colonneDonnees
            self.m_iIndiceValeurAttribut = iIndiceValeurAttribut
            self.m_sChaineIdentifiantItem = sChaineIdentifiant


    class RefItemQuantitatif(object):


        def __init__(self, outerInstance, colonneDonnees):
            self.m_colonneDonnees = None

            self.__outerInstance = outerInstance

            self.m_colonneDonnees = colonneDonnees



    #    *potential rules
    #     
    class ReglePotentielle:



        def __init__(self, outerInstance, iDimension, iNombreTotalIntervalles):
            self.m_iDimension = 0
            self.m_tIntervalleMin = None
            self.m_tIntervalleMax = None
            self.m_tIndiceMin = None
            self.m_tIndiceMax = None
            self.m_fQualite = 0.0
            self.m_iSupportRegle = 0
            self.m_iSupportCond = 0
            self.m_iNombreTotalIntervalles = 0

            self.__outerInstance = outerInstance

            iIndiceDimension = 0

            self.m_iDimension = iDimension
            self.m_iNombreTotalIntervalles = iNombreTotalIntervalles

            self.m_tIntervalleMin = []
            for i in range(0, self.m_iNombreTotalIntervalles):
                self.m_tIntervalleMin.append(0)

            self.m_tIntervalleMax = []
            for i in range(0, self.m_iNombreTotalIntervalles):
                self.m_tIntervalleMax.append(0)

            self.m_tIndiceMin = []
            for i in range(0, self.m_iNombreTotalIntervalles):
                self.m_tIndiceMin.append(0)

            self.m_tIndiceMax = []
            for i in range(0, self.m_iNombreTotalIntervalles):
                self.m_tIndiceMax.append(0)

            self.m_fQualite = 0.0
            self.m_iSupportRegle = 0
            self.m_iSupportCond = 0

        def compareTo(self, o):
            if self.m_fQualite < o.m_fQualite:
                return -1
            elif self.m_fQualite == o.m_fQualite:
                return 0
            else:
                return 1

        def __lt__(self, o):
            if self.m_fQualite < o.m_fQualite:
                return -1
            elif self.m_fQualite == o.m_fQualite:
                return 0
            else:
                return 1



        def Copier(self, reglePotentielle):
            iIndiceIntervalle = 0

            if reglePotentielle is None:
                return

            if not self.m_iDimension == reglePotentielle.m_iDimension:
                return


            iIndiceIntervalle = 0
            while iIndiceIntervalle<self.m_iNombreTotalIntervalles:
                self.m_tIntervalleMin[iIndiceIntervalle] = reglePotentielle.m_tIntervalleMin[iIndiceIntervalle]
                self.m_tIntervalleMax[iIndiceIntervalle] = reglePotentielle.m_tIntervalleMax[iIndiceIntervalle]
                self.m_tIndiceMin[iIndiceIntervalle] = reglePotentielle.m_tIndiceMin[iIndiceIntervalle]
                self.m_tIndiceMax[iIndiceIntervalle] = reglePotentielle.m_tIndiceMax[iIndiceIntervalle]
                iIndiceIntervalle += 1

            self.m_fQualite = reglePotentielle.m_fQualite
            self.m_iSupportRegle = reglePotentielle.m_iSupportRegle
            self.m_iSupportCond = reglePotentielle.m_iSupportCond

    # Representation of the diagram of the rule to be optimized:
    # Constituents of the rule:
    # Number of items of each type:

    # Data structures for the optimization of calculations:

    m_tRandomFloat = None # Real table between 0.0 and 1.0, drawn randomly
    m_compteurRandomFloat = 0




    @staticmethod
    def InitialiserValeursAleatoires():
        iIndiceValeur = 0

        if EvaluationBaseAlgorithm.m_tRandomFloat is not None:
            return

        EvaluationBaseAlgorithm.m_tRandomFloat = []
        for iIndiceValeur in range(0, 65536):
            EvaluationBaseAlgorithm.m_tRandomFloat.append(float(random.random()))

        EvaluationBaseAlgorithm.m_compteurRandomFloat = 0



    def __init__(self, iNombreReglesPotentielles, gestionBD):
        self.m_tItemsQualCond = None
        self.m_tItemsQuantCond = None
        self.m_tItemsQualObj = None
        self.m_tItemsQuantObj = None
        self.m_iNombreItemsQualCond = 0
        self.m_iNombreItemsQuantCond = 0
        self.m_iNombreItemsQualObj = 0
        self.m_iNombreItemsQuantObj = 0
        self.m_iDimension = 0
        self.m_iNombreTotalItems = 0
        self.m_iNombreReglesPotentielles = 0
        self.m_tReglesPotentielles = None
        self.m_meilleureReglePotentielle = None
        self.m_derniereReglePotentielleValide = None
        self.m_gestionBD = None
        self.m_fMinSupp = 0.0
        self.m_fMinConf = 0.0
        self.m_fMinSuppRegle = 0.0
        self.m_fMinSuppDisjonction = 0.0
        self.m_iNombreTransactions = 0
        self.m_iDebutIntervallesDroite = 0
        self.m_iNombreTotalIntervalles = 0
        self.m_iDisjonctionGaucheCourante = 0
        self.m_iDisjonctionDroiteCourante = 0
        self.m_iNombreDisjonctionsGaucheValides = 0
        self.m_iNombreDisjonctionsDroiteValides = 0
        self.m_bPrendreEnCompteQuantitatifsGauche = False
        self.m_bPrendreEnCompteQuantitatifsDroite = False
        self.m_iSupportCumuleCond = 0
        self.m_iSupportCumuleRegle = 0
        self.m_schemaRegleOptimale = None
        self.m_tLignesAPrendreEnCompte = None
        self.m_tPrendreEnCompteLigneDroite = None
        self.m_tLignesCouvertesGauche = None
        self.m_tLignesCouvertesDroite = None
        self.m_iNombreLignesAPrendreEnCompte = 0
        self.m_tReglesPotentiellesAEvaluer = None
        self.m_iNombreReglesPotentiellesAEvaluer = 0


        self.m_iNombreReglesPotentielles = iNombreReglesPotentielles
        self.m_gestionBD = gestionBD

        self.m_fMinSupp = 0.0
        self.m_fMinConf = 0.0
        self.m_iNombreTransactions = self.m_gestionBD.ObtenirNombreLignes()

        self.m_iNombreItemsQualCond = 0
        self.m_iNombreItemsQuantCond = 0
        self.m_iNombreItemsQualObj = 0
        self.m_iNombreItemsQuantObj = 0

        self.m_iDimension = 0
        self.m_iNombreTotalItems = 0
        self.m_schemaRegleOptimale = None

        self.m_tReglesPotentielles = []
        for i in range(0, self.m_iNombreReglesPotentielles):
            self.m_tReglesPotentielles.append(None)

        self.m_derniereReglePotentielleValide = None

        self.m_iNombreTotalIntervalles = 0
        self.m_iDebutIntervallesDroite = 0
        self.m_iNombreDisjonctionsGaucheValides = 0
        self.m_iNombreDisjonctionsDroiteValides = 0
        self.m_bPrendreEnCompteQuantitatifsGauche = False
        self.m_bPrendreEnCompteQuantitatifsDroite = False
        self.m_iSupportCumuleCond = 0
        self.m_iSupportCumuleRegle = 0

        EvaluationBaseAlgorithm.InitialiserValeursAleatoires()

        self.m_tLignesAPrendreEnCompte = []
        for i in range(0, self.m_iNombreTransactions):
            self.m_tLignesAPrendreEnCompte.append(0)
        self.m_tPrendreEnCompteLigneDroite = []
        for i in range(0, self.m_iNombreTransactions):
            self.m_tPrendreEnCompteLigneDroite.append(False)
        self.m_tLignesCouvertesGauche = []
        for i in range(0, self.m_iNombreTransactions):
            self.m_tLignesCouvertesGauche.append(False)
        self.m_tLignesCouvertesDroite = []
        for i in range(0, self.m_iNombreTransactions):
            self.m_tLignesCouvertesDroite.append(False)
        self.m_iNombreLignesAPrendreEnCompte = 0
        self.m_tReglesPotentiellesAEvaluer = []
        for i in range(0, self.m_iNombreReglesPotentielles):
            self.m_tReglesPotentiellesAEvaluer.append(None)

        self.m_iNombreReglesPotentiellesAEvaluer = 0

    #    *
    #     * Set statistic parameters
    #     * @param fMinSuppRegle Minimun support of a rule
    #     * @param fMinConf Minimun confidence of a rule
    #     * @param fMinSuppDisjonction minimun support disjunction
    #     
    def SpecifierParametresStatistiques(self, fMinSuppRegle, fMinConf, fMinSuppDisjonction):
        self.m_fMinSuppRegle = fMinSuppRegle
        self.m_fMinSuppDisjonction = fMinSuppDisjonction
        self.m_fMinSupp = self.m_fMinSuppRegle
        self.m_fMinConf = fMinConf



    def VerifierEtAffecterBornesReglePotentielle(self, reglePotentielle, iIndiceDimension, iIndiceDisjonction, iIndice1, iIndice2):
        colonneDonnees = None
        iIndiceTemp = 0
        iIndiceMax = 0
        iIndiceIntervalle = 0

        if iIndiceDimension < self.m_iNombreItemsQuantCond:
            colonneDonnees = self.m_tItemsQuantCond[iIndiceDimension].m_colonneDonnees
            iIndiceIntervalle = (self.m_schemaRegleOptimale.m_iNombreDisjonctionsGauche*iIndiceDimension) + iIndiceDisjonction
        else:
            colonneDonnees = self.m_tItemsQuantObj[iIndiceDimension-self.m_iNombreItemsQuantCond].m_colonneDonnees
            iIndiceIntervalle = self.m_iDebutIntervallesDroite + ((iIndiceDimension-self.m_iNombreItemsQuantCond)*self.m_schemaRegleOptimale.m_iNombreDisjonctionsDroite) + iIndiceDisjonction

        iIndiceMax = colonneDonnees.m_iNombreValeursReellesCorrectes - 1

        # We ensure the correct order of the terminals:
        if iIndice1 > iIndice2:
            iIndiceTemp = iIndice1
            iIndice1 = iIndice2
            iIndice2 = iIndiceTemp

        # We check that the indices do not go outside the authorized limits, otherwise we are forced to:
        if iIndice1 < 0:
            iIndice1 = 0
        if iIndice2 < 0:
            iIndice2 = 0
        if iIndice1 > iIndiceMax:
            iIndice1 = iIndiceMax
        if iIndice2 > iIndiceMax:
            iIndice2 = iIndiceMax

        # Assignment of the terminals in the rule:
        reglePotentielle.m_tIndiceMin[iIndiceIntervalle] = iIndice1
        reglePotentielle.m_tIndiceMax[iIndiceIntervalle] = iIndice2
        reglePotentielle.m_tIntervalleMin[iIndiceIntervalle] = colonneDonnees.m_tValeursReellesTriees[iIndice1]
        reglePotentielle.m_tIntervalleMax[iIndiceIntervalle] = colonneDonnees.m_tValeursReellesTriees[iIndice2]




    #    *
    #     * Give an initial value to a potential rule
    #     * @param reglePotentielle
    #     * @param iIndiceReglePotentielle
    #     
    def InitialiserReglePotentielle(self, reglePotentielle, iIndiceReglePotentielle):
        iAmplitudeIntervalle = 0
        iIndiceDimension = 0
        iIndiceDisjonction = 0
        iNombreValeursDomaine = 0
        iNombreDisjonctions = 0
        iIndiceValeurDomaineMin = None
        iIndiceValeurDomaineMax = 0
        colonneDonnees = None

        # During the additional passes, we keep the intervals already processed for the best rule:
        # During the additional passes, the intervals already treated are kept as best as possible:
        if ((not self.m_bPrendreEnCompteQuantitatifsGauche)) or ((not self.m_bPrendreEnCompteQuantitatifsDroite)):
            reglePotentielle.Copier(self.m_meilleureReglePotentielle[0])


        iIndiceDimension = 0
        while iIndiceDimension<self.m_iDimension:

            if (self.m_bPrendreEnCompteQuantitatifsGauche and (iIndiceDimension<self.m_iNombreItemsQuantCond)) or (self.m_bPrendreEnCompteQuantitatifsDroite and (iIndiceDimension>=self.m_iNombreItemsQuantCond)):


                if iIndiceDimension<self.m_iNombreItemsQuantCond:
                    colonneDonnees = self.m_tItemsQuantCond[iIndiceDimension].m_colonneDonnees
                    iIndiceDisjonction = self.m_iDisjonctionGaucheCourante
                else:
                    colonneDonnees = self.m_tItemsQuantObj[iIndiceDimension-self.m_iNombreItemsQuantCond].m_colonneDonnees
                    iIndiceDisjonction = self.m_iDisjonctionDroiteCourante


                iNombreValeursDomaine = colonneDonnees.m_iNombreValeursReellesCorrectes

                # Old method of totally random generation of intervals:
                #iIndexMinDomainValue = (int) (((float) java.lang.Math.random ()) * ((float) iNumberValuesDomain))
                #iIndexMaxDomainValue = (int) (((float) java.lang.Math.random ()) * ((float) iNumberValuesDomain))

                # Another old method that only generated maximum intervals, which is not good for diversity:
                #iIndexMinDomainValue = 0
                #iIndexMaxDomainValue = iNumberDomainValues-1

                # New method:
                # The amplitude of the starting interval is all the larger as the index of the
                # potential rule in the "rule population" is high, in order to increase the
                # variety. However, a start interval cannot contain fewer values
                # than specified with minimal support.
                iAmplitudeIntervalle = iNombreValeursDomaine
                if iIndiceReglePotentielle>0:
                    iAmplitudeIntervalle -= math.trunc((iIndiceReglePotentielle * (iNombreValeursDomaine - (int((self.m_fMinSupp*float(iNombreValeursDomaine)))))) / float((self.m_iNombreReglesPotentielles-1)))

                iIndiceValeurDomaineMin = int(((float(random.random())) * (float((iNombreValeursDomaine-iAmplitudeIntervalle)))))
                iIndiceValeurDomaineMax = iIndiceValeurDomaineMin + iAmplitudeIntervalle - 1

                self.VerifierEtAffecterBornesReglePotentielle(reglePotentielle, iIndiceDimension, iIndiceDisjonction, iIndiceValeurDomaineMin, iIndiceValeurDomaineMax)

            iIndiceDimension += 1


    #these are the rules we will evolve
    def GenererReglesPotentiellesInitiales(self):

        iIndiceReglePotentielle = 0
        reglePotentielle = None


        iIndiceReglePotentielle = 0
        while iIndiceReglePotentielle<self.m_iNombreReglesPotentielles:

            # Generating a rule without initialization: the daughter class will take care of
            # assign it initial values
            reglePotentielle = EvaluationBaseAlgorithm.ReglePotentielle(self, self.m_iDimension, self.m_iNombreTotalIntervalles)

            self.InitialiserReglePotentielle(reglePotentielle, iIndiceReglePotentielle)

            self.m_tReglesPotentielles[iIndiceReglePotentielle] = reglePotentielle
            self.m_tReglesPotentiellesAEvaluer[iIndiceReglePotentielle] = reglePotentielle
            iIndiceReglePotentielle += 1

        #creation the best top m_meilleureReglePotentielle.length rules
        #I'm unsure about this logic.
        #and also about ther support and confidence that show up for the top n rules.
        i = 0
        while i < len(self.m_meilleureReglePotentielle):
            # Creation of the potential rule representing the one that has had the best quality found so far:
            # creation of the potential rule with the best quality so far
            self.m_meilleureReglePotentielle[i] = EvaluationBaseAlgorithm.ReglePotentielle(self, self.m_iDimension, self.m_iNombreTotalIntervalles)

            # Creation of a potential rule intended to memorize the best rule found so far
            # during the multiple passes to obtain disjunctive rules:
            self.m_derniereReglePotentielleValide = EvaluationBaseAlgorithm.ReglePotentielle(self, self.m_iDimension, self.m_iNombreTotalIntervalles)

            self.m_iNombreReglesPotentiellesAEvaluer = self.m_iNombreReglesPotentielles
            self.EvaluerReglesPotentielles()

            # We force the memorization of the best initial rule:
            #we keep the best initial rule
            # m_meilleureReglePotentielle[i].Copier(m_tReglesPotentielles[m_iNombreReglesPotentielles-1])
            self.m_meilleureReglePotentielle[i].Copier(self.m_tReglesPotentielles[self.m_iNombreReglesPotentielles - 1 - i])
            i += 1

    def SpecifierSchemaRegle(self, regle):
        item = None
        itemQual = None
        itemQuant = None
        iIndiceItem = 0
        iNombreItemsGauche = 0
        iNombreItemsDroite = 0
        iIndiceAjoutQual = 0
        iIndiceAjoutQuant = 0
        iIndiceLigneDonnees = 0
        bItemsCouverts = True
        iValeurQualCourante = 0
        iIndiceDimension = 0


        # We start by storing in a more direct way (static arrays) the various
        # rule constituents:
        self.m_iNombreItemsQualCond = regle.CompterItemsGaucheSelonType(Item.ITEM_TYPE_QUALITATIF)
        self.m_iNombreItemsQuantCond = regle.CompterItemsGaucheSelonType(Item.ITEM_TYPE_QUANTITATIF)
        self.m_iNombreItemsQualObj = regle.CompterItemsDroiteSelonType(Item.ITEM_TYPE_QUALITATIF)
        self.m_iNombreItemsQuantObj = regle.CompterItemsDroiteSelonType(Item.ITEM_TYPE_QUANTITATIF)

        iNombreItemsGauche = self.m_iNombreItemsQualCond + self.m_iNombreItemsQuantCond
        iNombreItemsDroite = self.m_iNombreItemsQualObj + self.m_iNombreItemsQuantObj

        if self.m_iNombreItemsQualCond > 0:
            self.m_tItemsQualCond = []
            for i in range(0, self.m_iNombreItemsQualCond):
                self.m_tItemsQualCond.append(None)
        else:
            self.m_tItemsQualCond = None

        if self.m_iNombreItemsQuantCond > 0:
            self.m_tItemsQuantCond = []
            for i in range(0, self.m_iNombreItemsQuantCond):
                self.m_tItemsQuantCond.append(None)
        else:
            self.m_tItemsQuantCond = None

        if self.m_iNombreItemsQualObj > 0:
            self.m_tItemsQualObj = []
            for i in range(0, self.m_iNombreItemsQualObj):
                self.m_tItemsQualObj.append(None)
        else:
            self.m_tItemsQualObj = None

        if self.m_iNombreItemsQuantObj > 0:
            self.m_tItemsQuantObj = []
            for i in range(0, self.m_iNombreItemsQuantObj):
                self.m_tItemsQuantObj.append(None)
        else:
            self.m_tItemsQuantObj = None


        # Memorization of qualitative items:
        iIndiceAjoutQual = 0
        iIndiceAjoutQuant = 0
        iIndiceItem = 0
        while iIndiceItem<iNombreItemsGauche:
            item = regle.ObtenirItemGauche(iIndiceItem)
            if item is not None:
                if item.m_iTypeItem == Item.ITEM_TYPE_QUALITATIF:
                    itemQual = item
                    self.m_tItemsQualCond[iIndiceAjoutQual] = EvaluationBaseAlgorithm.RefItemQualitatif(self, itemQual.m_attributQual.m_colonneDonnees, itemQual.m_iIndiceValeur, itemQual.ObtenirNomCompletItem())
                    iIndiceAjoutQual += 1
                elif item.m_iTypeItem == Item.ITEM_TYPE_QUANTITATIF:
                    itemQuant = item
                    self.m_tItemsQuantCond[iIndiceAjoutQuant] = EvaluationBaseAlgorithm.RefItemQuantitatif(self, itemQuant.m_attributQuant.m_colonneDonnees)
                    iIndiceAjoutQuant += 1
            iIndiceItem += 1


       # Memorization of quantitative items:
        iIndiceAjoutQual = 0
        iIndiceAjoutQuant = 0
        iIndiceItem = 0
        while iIndiceItem<iNombreItemsDroite:
            item = regle.ObtenirItemDroite(iIndiceItem)
            if item is not None:
                if item.m_iTypeItem == Item.ITEM_TYPE_QUALITATIF:
                    itemQual = item
                    self.m_tItemsQualObj[iIndiceAjoutQual] = EvaluationBaseAlgorithm.RefItemQualitatif(self, itemQual.m_attributQual.m_colonneDonnees, itemQual.m_iIndiceValeur, itemQual.ObtenirNomCompletItem())
                    iIndiceAjoutQual += 1
                elif item.m_iTypeItem == Item.ITEM_TYPE_QUANTITATIF:
                    itemQuant = item
                    self.m_tItemsQuantObj[iIndiceAjoutQuant] = EvaluationBaseAlgorithm.RefItemQuantitatif(self, itemQuant.m_attributQuant.m_colonneDonnees)
                    iIndiceAjoutQuant += 1
            iIndiceItem += 1


        # Memorization of the rule diagram:
        self.m_schemaRegleOptimale = AssociationRule(regle)

        #print("m_schemaRegleOptimale.m_iNombreAssociationRules: " + m_schemaRegleOptimale.m_iNombreAssociationRules); 
        self.m_meilleureReglePotentielle = []
        for i in range(0, self.m_schemaRegleOptimale.m_iNombreAssociationRules):
            self.m_meilleureReglePotentielle.append(None)

        # Memorization of information on the diagram of the rule:
        self.m_iDimension = self.m_iNombreItemsQuantCond + self.m_iNombreItemsQuantObj
        self.m_iNombreTotalItems = self.m_iDimension + self.m_iNombreItemsQualCond + self.m_iNombreItemsQualObj
        self.m_iDebutIntervallesDroite = self.m_schemaRegleOptimale.m_iNombreDisjonctionsGauche * self.m_iNombreItemsQuantCond
        self.m_iNombreTotalIntervalles = self.m_schemaRegleOptimale.m_iNombreDisjonctionsGauche*self.m_iNombreItemsQuantCond + self.m_schemaRegleOptimale.m_iNombreDisjonctionsDroite*self.m_iNombreItemsQuantObj
        self.m_iDisjonctionGaucheCourante = 0
        self.m_iDisjonctionDroiteCourante = 0
        self.m_iNombreDisjonctionsGaucheValides = 1
        self.m_iNombreDisjonctionsDroiteValides = 1
        self.m_bPrendreEnCompteQuantitatifsGauche = True
        self.m_bPrendreEnCompteQuantitatifsDroite = True
        self.m_iSupportCumuleCond = 0
        self.m_iSupportCumuleRegle = 0


        # To optimize the calculations of the evaluation of a rule, we create a table which
        # list only the lines that cover the qualitative items of the rule
        # (the other lines will not necessarily be covered by the rule, or even by its left part):
        self.m_iNombreLignesAPrendreEnCompte = 0
        iIndiceLigneDonnees = 0
        while iIndiceLigneDonnees<self.m_iNombreTransactions:

            # Detection of lines covered by qualitative values in the LEFT part of the rule:
            bItemsCouverts = True
            iIndiceItem=0
            while bItemsCouverts and (iIndiceItem<self.m_iNombreItemsQualCond):
                iValeurQualCourante = self.m_tItemsQualCond[iIndiceItem].m_colonneDonnees.m_tIDQualitatif[iIndiceLigneDonnees]
                bItemsCouverts = bItemsCouverts and (iValeurQualCourante == self.m_tItemsQualCond[iIndiceItem].m_iIndiceValeurAttribut)
                iIndiceItem += 1

            # And check that they do not contain missing values for the quantitative items on the left:
            if bItemsCouverts:
                iIndiceItem=0
                while bItemsCouverts and (iIndiceItem<self.m_iNombreItemsQuantCond):
                    bItemsCouverts = not (self.m_tItemsQuantCond[iIndiceItem].m_colonneDonnees.m_tValeurReelle[iIndiceLigneDonnees] == DatabaseAdmin.VALEUR_MANQUANTE_FLOAT)
                    iIndiceItem += 1


            if bItemsCouverts:
                self.m_tLignesAPrendreEnCompte[self.m_iNombreLignesAPrendreEnCompte] = iIndiceLigneDonnees
                self.m_iNombreLignesAPrendreEnCompte += 1


            # Test of the qualitative values in the RIGHT part of the rule:     
            bItemsCouverts = True
            iIndiceItem=0
            while bItemsCouverts and (iIndiceItem<self.m_iNombreItemsQualObj):
                iValeurQualCourante = self.m_tItemsQualObj[iIndiceItem].m_colonneDonnees.m_tIDQualitatif[iIndiceLigneDonnees]
                bItemsCouverts = bItemsCouverts and (iValeurQualCourante == self.m_tItemsQualObj[iIndiceItem].m_iIndiceValeurAttribut)
                iIndiceItem += 1

            # And check that the row does not contain missing values for the quantitative items on the right:
            if bItemsCouverts:
                iIndiceItem=0
                while bItemsCouverts and (iIndiceItem<self.m_iNombreItemsQuantObj):
                    bItemsCouverts = not (self.m_tItemsQuantObj[iIndiceItem].m_colonneDonnees.m_tValeurReelle[iIndiceLigneDonnees] == DatabaseAdmin.VALEUR_MANQUANTE_FLOAT)
                    iIndiceItem += 1


            self.m_tPrendreEnCompteLigneDroite[iIndiceLigneDonnees] = bItemsCouverts

            self.m_tLignesCouvertesGauche[iIndiceLigneDonnees] = False
            self.m_tLignesCouvertesDroite[iIndiceLigneDonnees] = False
            iIndiceLigneDonnees += 1





    # Take into account a new disjunction and restart the algorithm:
    # Take into account a new disjunction and relaunch the algorithm:
    def InitierNouvellePasse(self):
        bProchainePassePrivilegieDroite = False
        tNouvellesLignesAPrendreEnCompte = None
        iNombreNouvellesLignesAPrendreEnCompte = 0
        iIndiceLigneDonnees = 0
        iIndiceLigne = 0
        bItemCondCouvertReglePotentielle = False
        bItemObjCouvertReglePotentielle = False
        bItemRegleCouvertReglePotentielle = False
        bPremierePasse = False
        iIndiceDimension = 0
        iIndiceIntervalle = 0
        fValeurReelle = 0.0
        iIndiceReglePotentielle = 0
        bNouvelleRegleEstSolide = False
        iAncienSupportCumuleRegle = 0
        iAncienSupportCumuleCond = 0



        # If no disjunction should appear in the rule, we can stop the algorithm:
        if (self.m_schemaRegleOptimale.m_iNombreDisjonctionsGauche == 1) and (self.m_schemaRegleOptimale.m_iNombreDisjonctionsDroite == 1):
            self.m_iSupportCumuleCond = self.m_meilleureReglePotentielle[0].m_iSupportCond
            self.m_iSupportCumuleRegle = self.m_meilleureReglePotentielle[0].m_iSupportRegle

            return False


        bPremierePasse = self.m_bPrendreEnCompteQuantitatifsGauche and self.m_bPrendreEnCompteQuantitatifsDroite



        # We check that the new pass produced a good quality rule, otherwise we do not take it into account:
        # We check that the new pass has produced a rule of good quality, otherwise we do not take it into account:
        #
        # Question - just use first rule out of the top n? I think it's ok becuase the first rule and the other (n-1) are all pretty similar, so if we check the
        # quality of the first rule of them, I think this is a pretty good determination of the quality of the rest of the rules.
        bNouvelleRegleEstSolide = (((float(self.m_meilleureReglePotentielle[0].m_iSupportRegle)) >= self.m_fMinSupp*(float(self.m_iNombreTransactions))) and ((float(self.m_meilleureReglePotentielle[0].m_iSupportRegle)) >= self.m_fMinConf*(float(self.m_meilleureReglePotentielle[0].m_iSupportCond))))

        if bNouvelleRegleEstSolide:


            # We memorize the characteristics of the last valid rule (cumulative), in case it is necessary to restore it:
            iAncienSupportCumuleRegle = self.m_iSupportCumuleRegle
            iAncienSupportCumuleCond = self.m_iSupportCumuleCond


            # We delete from the table all the examples covered by the rule:
            for i in range(0, self.m_iNombreTransactions):
                self.tNouvellesLignesAPrendreEnCompte.append(None)
            iNombreNouvellesLignesAPrendreEnCompte = 0


            # 'm_tLignesAPrendreEnCompte' contains all the lines covered by the qualitative items
            # left of the rule, does not contain a quantitative attribute whose corresponding line
            # has a missing value, and finally we successively remove all the lines
            # covered by the rule whose disjunctions are built incrementally.

            # 'm_tLinesCouvertesLauche' indicates for each line if it is covered
            # by one of the left disjunctions hitherto constructed for the rule

            # 'm_tTakeRightLine Account' indicates for each line if it is covered
            # by the set of qualitative items on the right side of the rule, and also if
            # it does not contain a missing value for any of the quantitative attributes on the right side.

            iIndiceLigne = 0
            while iIndiceLigne<self.m_iNombreLignesAPrendreEnCompte:

                iIndiceLigneDonnees = self.m_tLignesAPrendreEnCompte[iIndiceLigne] # Indice r�el de la lignes dans la BD

                bItemCondCouvertReglePotentielle = self.m_tLignesCouvertesGauche[iIndiceLigneDonnees]
                bItemObjCouvertReglePotentielle = self.m_tLignesCouvertesDroite[iIndiceLigneDonnees]

                # Test the quantitative values in the left part of the rule:
                #UNSURE ABOUT HARDCODING [0] HERE....
                if self.m_bPrendreEnCompteQuantitatifsGauche:

                    bItemCondCouvertReglePotentielle = True
                    iIndiceDimension=0
                    iIndiceIntervalle = self.m_iDisjonctionGaucheCourante
                    while bItemCondCouvertReglePotentielle and (iIndiceDimension<self.m_iNombreItemsQuantCond):
                        fValeurReelle = self.m_tItemsQuantCond[iIndiceDimension].m_colonneDonnees.m_tValeurReelle[iIndiceLigneDonnees]
                        bItemCondCouvertReglePotentielle = (fValeurReelle >= self.m_meilleureReglePotentielle[0].m_tIntervalleMin[iIndiceIntervalle]) and (fValeurReelle <= self.m_meilleureReglePotentielle[0].m_tIntervalleMax[iIndiceIntervalle])
                        iIndiceDimension += 1
                        iIndiceIntervalle += self.m_schemaRegleOptimale.m_iNombreDisjonctionsGauche

                    # Update of the support taking into account the addition of the new interval,
                    # and being careful not to count any overlapping zones:
                    if bItemCondCouvertReglePotentielle and ((not self.m_tLignesCouvertesGauche[iIndiceLigneDonnees])):
                        self.m_iSupportCumuleCond += 1

                    self.m_tLignesCouvertesGauche[iIndiceLigneDonnees] = self.m_tLignesCouvertesGauche[iIndiceLigneDonnees] or bItemCondCouvertReglePotentielle


                # Test of the quantitative values in the right part of the rule
                if self.m_bPrendreEnCompteQuantitatifsDroite:

                    # First we check the coverage, even if the condition is not checked
                    # (in order to correctly update the array 'm_tRightCoveredLines'):
                    bItemObjCouvertReglePotentielle = self.m_tPrendreEnCompteLigneDroite[iIndiceLigneDonnees]
                    iIndiceDimension = self.m_iNombreItemsQuantCond
                    iIndiceIntervalle = self.m_iDebutIntervallesDroite + self.m_iDisjonctionDroiteCourante
                    while bItemObjCouvertReglePotentielle and (iIndiceDimension<self.m_iDimension):
                        fValeurReelle = self.m_tItemsQuantObj[iIndiceDimension-self.m_iNombreItemsQuantCond].m_colonneDonnees.m_tValeurReelle[iIndiceLigneDonnees]
                        bItemObjCouvertReglePotentielle = (fValeurReelle >= self.m_meilleureReglePotentielle[0].m_tIntervalleMin[iIndiceIntervalle]) and (fValeurReelle <= self.m_meilleureReglePotentielle[0].m_tIntervalleMax[iIndiceIntervalle])
                        iIndiceDimension += 1
                        iIndiceIntervalle += self.m_schemaRegleOptimale.m_iNombreDisjonctionsDroite

                    self.m_tLignesCouvertesDroite[iIndiceLigneDonnees] = self.m_tLignesCouvertesDroite[iIndiceLigneDonnees] or bItemObjCouvertReglePotentielle


                # The rule is only covered if the left and right parts are covered:
                bItemRegleCouvertReglePotentielle = bItemCondCouvertReglePotentielle and bItemObjCouvertReglePotentielle

                if bItemRegleCouvertReglePotentielle:
                    self.m_iSupportCumuleRegle += 1


                # We only keep the lines not covered by the rule:
                if ((not bItemCondCouvertReglePotentielle)) or ((not bItemRegleCouvertReglePotentielle)):
                    tNouvellesLignesAPrendreEnCompte[iNombreNouvellesLignesAPrendreEnCompte] = iIndiceLigneDonnees
                    iNombreNouvellesLignesAPrendreEnCompte += 1

                iIndiceLigne += 1



            # We now check that the rule cumulating the disjunctions is also valid:
            bNouvelleRegleEstSolide = (((float(self.m_iSupportCumuleRegle)) >= self.m_fMinSuppRegle*(float(self.m_iNombreTransactions))) and ((float(self.m_iSupportCumuleRegle)) >= self.m_fMinConf*(float(self.m_iSupportCumuleCond))))


            if bNouvelleRegleEstSolide:

                # We replace the old row index by the new one, �pur�:
                self.m_tLignesAPrendreEnCompte = tNouvellesLignesAPrendreEnCompte
                self.m_iNombreLignesAPrendreEnCompte = iNombreNouvellesLignesAPrendreEnCompte

                # We take into account the new disjunction:
                if (self.m_bPrendreEnCompteQuantitatifsGauche) and ((not self.m_bPrendreEnCompteQuantitatifsDroite)):
                    self.m_iNombreDisjonctionsGaucheValides += 1

                if (self.m_bPrendreEnCompteQuantitatifsDroite) and ((not self.m_bPrendreEnCompteQuantitatifsGauche)):
                    self.m_iNombreDisjonctionsDroiteValides += 1

                # We memorize the best rule found so far:
                self.m_derniereReglePotentielleValide.Copier(self.m_meilleureReglePotentielle[0])

            # Otherwise we ignore the new rule and restore the previous state:
            else:
                self.m_iSupportCumuleRegle = iAncienSupportCumuleRegle
                self.m_iSupportCumuleCond = iAncienSupportCumuleCond




        if not bNouvelleRegleEstSolide:

            # If the last rule generated did not improve the initial rule, we stop the search
            # new disjunctions on the side where we just performed the previous pass:
            if self.m_bPrendreEnCompteQuantitatifsGauche:
                self.m_iDisjonctionGaucheCourante = self.m_schemaRegleOptimale.m_iNombreDisjonctionsGauche

            if self.m_bPrendreEnCompteQuantitatifsDroite:
                self.m_iDisjonctionDroiteCourante = self.m_schemaRegleOptimale.m_iNombreDisjonctionsDroite


            # We restore the last valid rule (if it exists):
            if not bPremierePasse:
                self.m_meilleureReglePotentielle[0].Copier(self.m_derniereReglePotentielleValide)
            else:
                # Update needed if the first rule found was not valid:
                self.m_iSupportCumuleCond = self.m_meilleureReglePotentielle[0].m_iSupportCond
                self.m_iSupportCumuleRegle = self.m_meilleureReglePotentielle[0].m_iSupportRegle




        bProchainePassePrivilegieDroite = self.m_bPrendreEnCompteQuantitatifsGauche


        if bProchainePassePrivilegieDroite:

            if self.m_iDisjonctionDroiteCourante+1 < self.m_schemaRegleOptimale.m_iNombreDisjonctionsDroite:
                self.m_iDisjonctionDroiteCourante += 1
                self.m_bPrendreEnCompteQuantitatifsGauche = False
                self.m_bPrendreEnCompteQuantitatifsDroite = True
            elif self.m_iDisjonctionGaucheCourante+1 < self.m_schemaRegleOptimale.m_iNombreDisjonctionsGauche:
                self.m_iDisjonctionGaucheCourante += 1
                self.m_bPrendreEnCompteQuantitatifsGauche = True
                self.m_bPrendreEnCompteQuantitatifsDroite = False
            else:
                self.m_bPrendreEnCompteQuantitatifsGauche = self.m_bPrendreEnCompteQuantitatifsDroite = False

        else:

            if self.m_iDisjonctionGaucheCourante+1 < self.m_schemaRegleOptimale.m_iNombreDisjonctionsGauche:
                self.m_iDisjonctionGaucheCourante += 1
                self.m_bPrendreEnCompteQuantitatifsGauche = True
                self.m_bPrendreEnCompteQuantitatifsDroite = False
            elif self.m_iDisjonctionDroiteCourante+1 < self.m_schemaRegleOptimale.m_iNombreDisjonctionsDroite:
                self.m_iDisjonctionDroiteCourante += 1
                self.m_bPrendreEnCompteQuantitatifsGauche = False
                self.m_bPrendreEnCompteQuantitatifsDroite = True
            else:
                self.m_bPrendreEnCompteQuantitatifsGauche = self.m_bPrendreEnCompteQuantitatifsDroite = False



        # We generate a new set of potential rules for the next pass:
        if self.m_bPrendreEnCompteQuantitatifsGauche or self.m_bPrendreEnCompteQuantitatifsDroite:

            # For the following passes, a lower support is used to allow additional rules to be incorporated into the main rule:
            self.m_fMinSupp = self.m_fMinSuppDisjonction

            iIndiceReglePotentielle = 0
            while iIndiceReglePotentielle<self.m_iNombreReglesPotentielles:
                self.InitialiserReglePotentielle(self.m_tReglesPotentielles[iIndiceReglePotentielle], iIndiceReglePotentielle)
                self.m_tReglesPotentiellesAEvaluer[iIndiceReglePotentielle] = self.m_tReglesPotentielles[iIndiceReglePotentielle]
                iIndiceReglePotentielle += 1

            self.m_iNombreReglesPotentiellesAEvaluer = self.m_iNombreReglesPotentielles
            self.EvaluerReglesPotentielles()

            self.m_meilleureReglePotentielle[0].Copier(self.m_tReglesPotentielles[self.m_iNombreReglesPotentielles-1])

            return True

        return False




    #    *
    #     * Evaluation of the set of potential rules in one scan of the dataset
    #     
    def EvaluerReglesPotentielles(self):
        reglePotentielle = None
        colonneDonnees = None
        iIndiceLigneDonnees = 0
        iIndiceLigne = 0
        iIndiceDimension = 0
        iIndiceDisjonction = 0
        iIndiceItem = 0
        iIndiceReglePotentielle = 0
        iValeurQualCourante = 0 # Qualitative value read for an attribute on a line of the database
        fValeurQuantCourante = 0 # Numerical value read for an attribute on a line of the DB
        bItemCondCouvertReglePotentielle = False
        bItemRegleCouvertReglePotentielle = False
        tValeursReelles = None # Array containing the values of quantitative attributes for a row
        iNombreDisjonctions = 0
        iIndiceIntervalle = 0
        bPremierePasse = False
        bTestPreliminaire = False


        bPremierePasse = (self.m_bPrendreEnCompteQuantitatifsGauche and self.m_bPrendreEnCompteQuantitatifsDroite)

        # The preliminary test makes it possible to avoid going through most of the calculation
        # in the case where the 1st quantitative item is not verified:
        bTestPreliminaire = self.m_bPrendreEnCompteQuantitatifsGauche and (self.m_iNombreItemsQuantCond > 0)


        # We reset the support measures for each of the potential rules:
        iIndiceReglePotentielle = 0
        while iIndiceReglePotentielle<self.m_iNombreReglesPotentiellesAEvaluer:
            reglePotentielle = self.m_tReglesPotentiellesAEvaluer[iIndiceReglePotentielle]
            reglePotentielle.m_iSupportCond = 0
            reglePotentielle.m_iSupportRegle = 0
            iIndiceReglePotentielle += 1

        tValeursReelles = []
        for i in range(0, self.m_iDimension):
            tValeursReelles.append(None)


        # We start by evaluating the coverage of the qualitative items, these being
        # common to all potential rules. For this, on the one hand we only cross the lines
        # covered by the left qualitative items of the rule. In addition, we have already
        # precalculated the right coverage when passing the rule scheme to the algorithm.
        iIndiceLigne = 0
        while iIndiceLigne < self.m_iNombreLignesAPrendreEnCompte:

            # The table 'm_tLignesAPRendreEnCompte' contains all the lines covered
            # by the QUALITATIVE left part of the rule,
            # but has been deprived of the lines covered by the entire rule (qualitative and quantitative items).

            iIndiceLigneDonnees = self.m_tLignesAPrendreEnCompte[iIndiceLigne] # Indice r�el de la lignes dans la BD


            # We list the numeric values for each column of the row:
            iIndiceDimension = 0
            while iIndiceDimension<self.m_iNombreItemsQuantCond:
                tValeursReelles[iIndiceDimension] = self.m_tItemsQuantCond[iIndiceDimension].m_colonneDonnees.m_tValeurReelle[iIndiceLigneDonnees]
                iIndiceDimension += 1

            if self.m_tPrendreEnCompteLigneDroite[iIndiceLigneDonnees]:
                iIndiceDimension = self.m_iNombreItemsQuantCond
                while iIndiceDimension<self.m_iDimension:
                    tValeursReelles[iIndiceDimension] = self.m_tItemsQuantObj[iIndiceDimension-self.m_iNombreItemsQuantCond].m_colonneDonnees.m_tValeurReelle[iIndiceLigneDonnees]
                    iIndiceDimension += 1


            # We then evaluate the coverage of the quantitative intervals for each of the potential rules:
            iIndiceReglePotentielle = 0
            while iIndiceReglePotentielle<self.m_iNombreReglesPotentiellesAEvaluer:

                reglePotentielle = self.m_tReglesPotentiellesAEvaluer[iIndiceReglePotentielle]

                bItemCondCouvertReglePotentielle = True
                if bTestPreliminaire:
                    bItemCondCouvertReglePotentielle = (tValeursReelles[0] >= reglePotentielle.m_tIntervalleMin[self.m_iDisjonctionGaucheCourante]) and (tValeursReelles[0] <= reglePotentielle.m_tIntervalleMax[self.m_iDisjonctionGaucheCourante])

                if bItemCondCouvertReglePotentielle:


                    # Test the quantitative values in the left part of the rule:
                    if not self.m_bPrendreEnCompteQuantitatifsGauche:
                        bItemCondCouvertReglePotentielle = self.m_tLignesCouvertesGauche[iIndiceLigneDonnees]
                    else:

                        iIndiceDimension=1
                        iIndiceIntervalle = self.m_iDisjonctionGaucheCourante + self.m_schemaRegleOptimale.m_iNombreDisjonctionsGauche
                        while bItemCondCouvertReglePotentielle and (iIndiceDimension<self.m_iNombreItemsQuantCond):
                            bItemCondCouvertReglePotentielle = (tValeursReelles[iIndiceDimension] >= reglePotentielle.m_tIntervalleMin[iIndiceIntervalle]) and (tValeursReelles[iIndiceDimension] <= reglePotentielle.m_tIntervalleMax[iIndiceIntervalle])
                            iIndiceDimension += 1
                            iIndiceIntervalle += self.m_schemaRegleOptimale.m_iNombreDisjonctionsGauche



                    if bItemCondCouvertReglePotentielle:

                        reglePotentielle.m_iSupportCond += 1


                        # Test of the quantitative values in the right part of the rule
                        # (useful only if the left part is covered, in order to increase the support of the ruler,
                        # and provided that straight qualitative items are also covered)
                        if not self.m_bPrendreEnCompteQuantitatifsDroite:
                            bItemRegleCouvertReglePotentielle = (self.m_tLignesCouvertesDroite[iIndiceLigneDonnees])
                        else:

                            bItemRegleCouvertReglePotentielle = bItemCondCouvertReglePotentielle and (self.m_tPrendreEnCompteLigneDroite[iIndiceLigneDonnees])
                            iIndiceDimension = self.m_iNombreItemsQuantCond
                            iIndiceIntervalle = self.m_iDebutIntervallesDroite + self.m_iDisjonctionDroiteCourante
                            while bItemRegleCouvertReglePotentielle and (iIndiceDimension<self.m_iDimension):
                                bItemRegleCouvertReglePotentielle = (tValeursReelles[iIndiceDimension] >= reglePotentielle.m_tIntervalleMin[iIndiceIntervalle]) and (tValeursReelles[iIndiceDimension] <= reglePotentielle.m_tIntervalleMax[iIndiceIntervalle])
                                iIndiceDimension += 1
                                iIndiceIntervalle += self.m_schemaRegleOptimale.m_iNombreDisjonctionsDroite

                        if bItemRegleCouvertReglePotentielle:
                            reglePotentielle.m_iSupportRegle += 1

                iIndiceReglePotentielle += 1
            iIndiceLigne += 1


        # The quality measurement remains the responsibility of the daughter class:  
        iIndiceReglePotentielle = 0
        while iIndiceReglePotentielle<self.m_iNombreReglesPotentiellesAEvaluer:
            self.EvaluerQualiteReglePotentielle(self.m_tReglesPotentiellesAEvaluer[iIndiceReglePotentielle])
            iIndiceReglePotentielle += 1


        # All the quality indices are now up to date:
        self.m_iNombreReglesPotentiellesAEvaluer = 0

        # Sort ascending by quality:     
        self.m_tReglesPotentielles.sort()


        # Memorization of the best potential rule:
        if self.m_tReglesPotentielles[self.m_iNombreReglesPotentielles-1].m_fQualite >= self.m_meilleureReglePotentielle[0].m_fQualite:
            self.m_meilleureReglePotentielle[0].Copier(self.m_tReglesPotentielles[self.m_iNombreReglesPotentielles-1])

    #obtain the best rule
    #adding index so we can get the best rule at the index - (index + 1)th best rule
    def ObtenirMeilleureRegle(self, index):
        item = None
        itemQual = None
        itemQuant = None
        iIndiceItem = 0
        iIndiceItemQuant = 0
        fConfianceRegle = 0.0
        iIndiceIntervalleReglePotentielle = 0
        iIndiceDisjonction = 0

        if self.m_schemaRegleOptimale is None:
            return None

        
        # Determination of the optimal bounds in the left part of the rule:
        iIndiceIntervalleReglePotentielle = 0
        iIndiceItemQuant = 0
        iIndiceItem = 0
        while iIndiceItem < self.m_schemaRegleOptimale.m_iNombreItemsGauche:

            item = self.m_schemaRegleOptimale.ObtenirItemGauche(iIndiceItem)

            if item.m_iTypeItem == Item.ITEM_TYPE_QUANTITATIF:
                itemQuant = item
                iIndiceDisjonction = 0
                while iIndiceDisjonction < self.m_iNombreDisjonctionsGaucheValides:
                    itemQuant.m_tBornes[iIndiceDisjonction*2] = self.m_meilleureReglePotentielle[index].m_tIntervalleMin[iIndiceIntervalleReglePotentielle]
                    itemQuant.m_tBornes[iIndiceDisjonction*2+1] = self.m_meilleureReglePotentielle[index].m_tIntervalleMax[iIndiceIntervalleReglePotentielle]
                    iIndiceIntervalleReglePotentielle += 1
                    iIndiceDisjonction += 1
                iIndiceItemQuant += 1
                iIndiceIntervalleReglePotentielle += self.m_schemaRegleOptimale.m_iNombreDisjonctionsGauche - iIndiceDisjonction

            iIndiceItem += 1


        # Determination of the optimal bounds in the right part of the rule:
        iIndiceIntervalleReglePotentielle = self.m_iDebutIntervallesDroite
        iIndiceItemQuant = self.m_iNombreItemsQuantCond
        iIndiceItem = 0
        while iIndiceItem<self.m_schemaRegleOptimale.m_iNombreItemsDroite:

            item = self.m_schemaRegleOptimale.ObtenirItemDroite(iIndiceItem)

            if item.m_iTypeItem == Item.ITEM_TYPE_QUANTITATIF:
                itemQuant = item
                iIndiceDisjonction = 0
                while iIndiceDisjonction<self.m_iNombreDisjonctionsDroiteValides:
                    itemQuant.m_tBornes[iIndiceDisjonction*2] = self.m_meilleureReglePotentielle[index].m_tIntervalleMin[iIndiceIntervalleReglePotentielle]
                    itemQuant.m_tBornes[iIndiceDisjonction*2+1] = self.m_meilleureReglePotentielle[index].m_tIntervalleMax[iIndiceIntervalleReglePotentielle]
                    iIndiceIntervalleReglePotentielle += 1
                    iIndiceDisjonction += 1
                iIndiceItemQuant += 1
                iIndiceIntervalleReglePotentielle += self.m_schemaRegleOptimale.m_iNombreDisjonctionsDroite - iIndiceDisjonction

            iIndiceItem += 1

        self.m_schemaRegleOptimale.m_iNombreDisjonctionsGaucheValides = self.m_iNombreDisjonctionsGaucheValides
        self.m_schemaRegleOptimale.m_iNombreDisjonctionsDroiteValides = self.m_iNombreDisjonctionsDroiteValides

        self.m_meilleureReglePotentielle[index].m_iSupportCond = self.m_iSupportCumuleCond
        self.m_meilleureReglePotentielle[index].m_iSupportRegle = self.m_iSupportCumuleRegle

        #This is where the best rule's support and confidence are assigned
        self.m_schemaRegleOptimale.AssignerNombreOccurrences(self.m_meilleureReglePotentielle[index].m_iSupportRegle)
        self.m_schemaRegleOptimale.AssignerSupport((float(self.m_meilleureReglePotentielle[index].m_iSupportRegle)) / (float(self.m_iNombreTransactions)))

        if self.m_meilleureReglePotentielle[index].m_iSupportCond > 0:
            fConfianceRegle = (float(self.m_meilleureReglePotentielle[index].m_iSupportRegle)) / (float(self.m_meilleureReglePotentielle[index].m_iSupportCond))
        else:
            fConfianceRegle = 0.0
        self.m_schemaRegleOptimale.AssignerConfiance(fConfianceRegle)

        return self.m_schemaRegleOptimale


    def ObtenirMeilleurSupportCourant(self):
        return self.m_tReglesPotentielles[self.m_iNombreReglesPotentielles-1].m_iSupportRegle



    def ObtenirMeilleurSupportRelatifCourant(self):
        return (float(self.m_tReglesPotentielles[self.m_iNombreReglesPotentielles-1].m_iSupportRegle) / float(self.m_iNombreTransactions))



    def ObtenirMeilleureConfianceCourant(self):
        iSupportCond = 0
        iSupportRegle = 0

        iSupportCond = self.m_tReglesPotentielles[self.m_iNombreReglesPotentielles-1].m_iSupportCond
        iSupportRegle = self.m_tReglesPotentielles[self.m_iNombreReglesPotentielles-1].m_iSupportRegle

        if iSupportCond>0:
            return (float(iSupportRegle) / float(iSupportCond))
        else:
            return 0.0



    def CalculerQualiteMoyenne(self):
        iIndiceReglePotentielle = 0
        fCumulQualite = 0.0

        fCumulQualite = 0.0
        iIndiceReglePotentielle = 0
        while iIndiceReglePotentielle < self.m_iNombreReglesPotentielles:
            fCumulQualite += self.m_tReglesPotentielles[iIndiceReglePotentielle].m_fQualite
            iIndiceReglePotentielle += 1

        return (fCumulQualite / float(self.m_iNombreReglesPotentielles))



    def ObtenirMeilleureQualiteCourante(self):
        return self.m_tReglesPotentielles[self.m_iNombreReglesPotentielles-1].m_fQualite



    def ObtenirPireQualiteCourante(self):
        return self.m_tReglesPotentielles[0].m_fQualite


    def EvaluerQualiteReglePotentielle(self, reglePotentielle):
        iIndiceDimension = 0
        iIndiceDisjonction = 0
        iNombreDisjonctions = 0
        iIndiceIntervalle = 0
        iSupportIntervalle = 0
        iSupportMax = 0
        fTauxCouvertureDomaine1 = 0.0
        fTauxCouvertureDomaine2 = 0.0
        colonneDonnees = None

        # 1 quality measure:
        # individual.m_fQuality = (float) individual.m_iSupportRegle - m_fMinConf * (float) individual.m_iSupportCond
        # if ((float) individual.m_iSupportRegle <m_fMinSupp * (float) m_iNumberTransactions)
        # individual.m_fQuality = - (float) m_iNumberTransactions
        #        


        # 2nd quality measure: we weight by the coverage rate of the domain of each quantitative value
        # calculate the gain
        reglePotentielle.m_fQualite = float(reglePotentielle.m_iSupportRegle) - self.m_fMinConf * float(reglePotentielle.m_iSupportCond)

        #reglePotentielle.m_fQualite /= (float)m_iNombreTransactions


        if reglePotentielle.m_fQualite > 0.0:

            iIndiceDimension = 0
            while iIndiceDimension<self.m_iDimension:

                if (self.m_bPrendreEnCompteQuantitatifsGauche and (iIndiceDimension<self.m_iNombreItemsQuantCond)) or (self.m_bPrendreEnCompteQuantitatifsDroite and (iIndiceDimension>=self.m_iNombreItemsQuantCond)):


                    if iIndiceDimension<self.m_iNombreItemsQuantCond:
                        iIndiceIntervalle = (iIndiceDimension*self.m_schemaRegleOptimale.m_iNombreDisjonctionsGauche) + self.m_iDisjonctionGaucheCourante
                        colonneDonnees = self.m_tItemsQuantCond[iIndiceDimension].m_colonneDonnees
                    else:
                        iIndiceIntervalle = self.m_iDebutIntervallesDroite + ((iIndiceDimension-self.m_iNombreItemsQuantCond)*self.m_schemaRegleOptimale.m_iNombreDisjonctionsDroite) + self.m_iDisjonctionDroiteCourante
                        colonneDonnees = self.m_tItemsQuantObj[iIndiceDimension-self.m_iNombreItemsQuantCond].m_colonneDonnees


                    # Technique 2:
                     # - problem of small lots whose support is <minsupp / nb intervals and therefore not found,
                     # - tends not to exceed minimal support, while it could without losing quality
                    fTauxCouvertureDomaine1 = reglePotentielle.m_tIntervalleMax[iIndiceIntervalle] - reglePotentielle.m_tIntervalleMin[iIndiceIntervalle]
                    fTauxCouvertureDomaine1 /= (colonneDonnees.m_fValeurMax - colonneDonnees.m_fValeurMin)


                    iSupportMax = colonneDonnees.m_iNombreValeursReellesCorrectes
                    if iSupportMax > 0:
                        iSupportIntervalle = colonneDonnees.ObtenirSupportIntervalle(reglePotentielle.m_tIndiceMin[iIndiceIntervalle], reglePotentielle.m_tIndiceMax[iIndiceIntervalle])
                        fTauxCouvertureDomaine2 = (float(iSupportIntervalle)) / (float(iSupportMax))

                    #                        
                    #                    if (iIndiceDimension<m_iNombreItemsQuantCond)
                    #                        fTauxCouvertureDomaine2 = 1.0
                    #                    else {
                    #                        iSupportIntervalle = m_tItemsQuantObj[ iIndiceDimension-m_iNombreItemsQuantCond ].m_colonneDonnees.ObtenirSupportIntervalle(reglePotentielle.m_tIndiceMin[iIndiceIntervalle], reglePotentielle.m_tIndiceMax[iIndiceIntervalle])
                    #                        iSupportMax = m_tItemsQuantObj[ iIndiceDimension-m_iNombreItemsQuantCond ].m_colonneDonnees.m_iNombreValeursReellesCorrectes
                    #                        fTauxCouvertureDomaine2 = ((float)iSupportIntervalle) / ((float)iSupportMax)
                    #                    }
                    #

                    reglePotentielle.m_fQualite *= (1.0-fTauxCouvertureDomaine1) * (1.0-fTauxCouvertureDomaine2)

                iIndiceDimension += 1


        if float(reglePotentielle.m_iSupportRegle) < self.m_fMinSupp*float(self.m_iNombreTransactions):
            reglePotentielle.m_fQualite -= float(self.m_iNombreTransactions) + float(reglePotentielle.m_iSupportRegle) - self.m_fMinSupp*float(self.m_iNombreTransactions) #) / ((float)m_iNombreTransactions);


import math
import sys
sys.path.append('C:\\Users\\aalsahee\\python_physical_model\\Saudi\\trace\\Traces\\qtm\\src\\')

# from apriori import *
# from database import *
# from geneticAlgorithm import *

# GMeansClusterer is still a work in progress functionality. Therefore, it will have some commented out print statements, and will be 
#revised in the future. 
class GMeansClusterer(object):

    #parametrized constructor
    def __init__(self, assocRules, input_parametresReglesQuantitatives):
        self.__kMeansClusterer = None
        self.__rules = []
        self.__listOfCentroids = []
        self.__centroidClusters = {}
        print("self.__centroidClusters1: " + str(self.__centroidClusters))
        self.m_parametresReglesQuantitatives = None


        # For testing clustering, uncomment
        #        TesterClustering.printOutRules(assocRules)
        #        TesterClustering.printOutLHVals(assocRules)
        #        TesterClustering.printOutRHVals(assocRules)

        self.__rules = assocRules

        self.m_parametresReglesQuantitatives = input_parametresReglesQuantitatives

        self.__kMeansClusterer = KMeansClusterer(assocRules, self.m_parametresReglesQuantitatives)

        self.__listOfCentroids = []
        self.__centroidClusters = {}
        print("self.__centroidClusters2: " + str(self.__centroidClusters))


    def applyGMeansAlgo(self):
        return []

    def applyGMeansAlgo(self, maxKClusterAmt):

        i =0
        totalNumKClusters = 0

        self.__listOfCentroids = self.__kMeansClusterer.applyKMeansAlgo(1)

        while i < len(self.__listOfCentroids) and totalNumKClusters < maxKClusterAmt:

            # System.out.println("G MEANS LIST OF CENTROIDS SIZE: " + listOfCentroids.size())

            # System.out.println("current centroid G MEANS: " + listOfCentroids.get(i))

            #centroidClusters will be the entirety of the data set, since all points map to the one cluster
            self.__centroidClusters = self.__kMeansClusterer.getCentroidClusters()
            print("self.__centroidClusters3: " + str(self.__centroidClusters))

            #Uncomment to verify centroidClusters has all the points (since one key, and all points as values for the key)
            #System.out.println(centroidClusters.size())
            oldCentroid = self.__listOfCentroids[i]
            initialDataPoints = self.__centroidClusters[oldCentroid]
            print("self.__centroidClusters4: " + str(self.__centroidClusters))

            print("initialDataPoints: " + initialDataPoints)

            if initialDataPoints is None:
                i += 1
                continue

            # For when other times, when data points restricted:
            newKMeansClusterer = KMeansClusterer(initialDataPoints, self.m_parametresReglesQuantitatives)

            # Get 2 clusters for data points
            #ArrayList<Centroid> newListOfCentroids = newKMeansClusterer.applyKMeansAlgo(numKClusters + 1, listOfCentroids)
            newListOfCentroids = newKMeansClusterer.applyKMeansAlgo(2)

            newCentroidClusters = newKMeansClusterer.getCentroidClusters()

            # Uncomment for value checking
            # System.out.println("newCentroidClusters.keySet(): " + newCentroidClusters.keySet())

            # System.out.println("newCentroidClusters.keySet().size(): " + newCentroidClusters.keySet().size())

            # System.out.println("newListOfCentroids.size(): " + newListOfCentroids.size())

            c1 = Centroid()
            c2 = Centroid()

            if len(newListOfCentroids) == 2:

                c1 = newListOfCentroids[0]
                c2 = newListOfCentroids[1]


                if c1 is not None and c2 is not None:
                    # Vector will be <c1 coordinates> + t<direction vector>. Represent as ArrayList: {c1 coordinates, direction vector}
                    vectorAL = self.__createVector(c1, c2)

                    #project points in initialDataPoints onto vectorAL

                    projectedPoints = self.__projectPoints(initialDataPoints, vectorAL)

                    standardizedPoints = self.__standardizePoints(projectedPoints)

                    andersonDarlingResult = self.__andersonDarlingTest(standardizedPoints)

                    isNonCritical = self.__isNonCritical(andersonDarlingResult)

                    # if(andersonDarlingResult is in range of noncritical vals at confidence level phi ie isNonCritical == true)
                    if isNonCritical:
                        #accept original center
                        i += 1
                    else:
                        #ie isNonCritical == false
                        #replace original center with c1 and c2 in listOfCentroids
                        removedCentroid = self.__listOfCentroids[i]
                        #added a cluster

                        if (removedCentroid.getCoordinates()) is c2.getCoordinates() or (removedCentroid.getCoordinates()) is c2.getCoordinates():
                            i += 1
                        else:

                            #only add if one of the new centroids does not equal the old one, since otherwise an infinitely long recursive loop occurs.
                            self.__listOfCentroids.pop(i)
                            self.__listOfCentroids.insert(i, c2)
                            self.__listOfCentroids.insert(i, c1)

                            #i stays the same
                            self.__centroidClusters.pop(oldCentroid)
                            print("self.__centroidClusters5: " + str(self.__centroidClusters))
                            self.__centroidClusters.update({c1: newCentroidClusters[c1]})
                            print("self.__centroidClusters6: " + str(self.__centroidClusters))
                            self.__centroidClusters.update({c2: newCentroidClusters[c2]})
                            print("self.__centroidClusters7: " + str(self.__centroidClusters))
                            totalNumKClusters += 1
            else:
                #throw error
                print("ERROR: newListOfCentroids.size() != 2")
                #IMPORTANT: 
                #note: this can happen if the new list of centroids removes a centroid that had no points mapped to it. What do I do here? keep the one centroid??
                i += 1



        self.__listOfCentroids = self.__cleanUpRepeatRules(self.__listOfCentroids)

        return self.__listOfCentroids


    def __cleanUpRepeatRules(self, listOfCentroids):

        cleanedUpList = listOfCentroids

        ruleProximity = self.testRuleProximities(listOfCentroids)

        i = 0
        while i<len(listOfCentroids):

            centroidConsidered = listOfCentroids[i]

            # Uncomment to get minimum support and minimum confidence values
            #  System.out.println("m_parametresReglesQuantitatives.m_fMinSupp: " + m_parametresReglesQuantitatives.m_fMinSupp)
            # System.out.println("m_parametresReglesQuantitatives.m_fMinConf: " + m_parametresReglesQuantitatives.m_fMinConf)

            # TODO: only display values above a certain support or confidence threshold value
            #            if(centroidConsidered.getSupport() < m_parametresReglesQuantitatives.m_fMinSupp || centroidConsidered.getConfidence() < m_parametresReglesQuantitatives.m_fMinConf ){
            #                listOfCentroids.remove(i)
            #                continue
            #            }

            j = 0
            while j<len(listOfCentroids):

                centroidInComparison = listOfCentroids[j]

                distanceBtwnCentroids = self.__kMeansClusterer.calculateEuclideanDistance(centroidConsidered.getCoordinates(), centroidInComparison.getCoordinates())
                if not j == i:
                    # print(distanceBtwnCentroids)

                    # Use euclidean distance to remove 'similar' rules. TODO: how to find how far to consider 'distinct'?
                    if distanceBtwnCentroids < float((ruleProximity)):

                        centroidConsidered.setNumOccurrences(centroidConsidered.getNumOccurrences() + centroidInComparison.getNumOccurrences())

                        centroidConsidered.setSupport(centroidConsidered.getSupport() + centroidInComparison.getSupport())

                        centroidConsidered.setConfidence(centroidConsidered.getConfidence() + centroidInComparison.getConfidence())

                        cleanedUpList.pop(j)

                        j -= 1

                j += 1

            i += 1

        return cleanedUpList


    # [Tester function] Return the average distance between all Centroids in centroidList (passed in as a parameter)
    def testRuleProximities(self, centroidList):

        avgDist = 0

        centListSize = len(centroidList)

        i = 0
        while i<centListSize:
            centConsidered1 = centroidList[i]

            listOfIntervalsA = centConsidered1.getCoordinates()

            j = i+1
            while j<centListSize:

                centConsidered2 = centroidList[j]
                listOfIntervalsB = centConsidered2.getCoordinates()

                doubleDistance = 0

                # List of intervals: has intervals ([, ], [, ], [, ]) etc in assocation rule from left to right
                a = 0
                while a < len(listOfIntervalsA):

                    #TODO: need CHECKING for if list of intervals' sizes not the same
                    #checks if double or float
                    coordinate = float(abs(float(listOfIntervalsA[a]) - float(listOfIntervalsB[a])))

                    coordSquared = coordinate*coordinate
                    doubleDistance += coordSquared

                    a += 1

                distance = math.sqrt(doubleDistance)
                avgDist += distance


                j += 1

            i += 1

        #sum of nums from 1 to (n - 1) is 0.5(n-1)(n-2)
        #check that this is not negative! if sizeOfARList is small.
        avgDist /= ((centListSize - 1)*(centListSize - 2) * 0.5)

        return avgDist


    # AL representation of vector returned will be <c1 coordinates> + t<direction vector>. Represent as ArrayList: {c1 coordinates, direction vector}
    def __createVector(self, c1, c2):

        vector = []

        c1Coords = c1.getCoordinates()
        c2Coords = c2.getCoordinates()

        vector.append(c1Coords)

        directionVector = []

        if len(c1Coords) == len(c2Coords):
            i = 0
            while i<len(c2Coords):
                difference = float(c2Coords[i]) - float(c1Coords[i])
                directionVector.append(difference)
                i += 1

            #System.out.println("directionVector: " + directionVector)

        else:
            print("ERROR: not c1Coords.size() == c2Coords.size()")

        vector.append(directionVector)


        return vector


    def __projectPoints(self, dataPoints, vectorAL):

        # AL of centroids, to be the projected points onto the vector
        projectedPoints = []

        #vectorAL.get(0) is c1. vectorAL.get(1) is direction vector
        i = 0
        while i<len(dataPoints):
            rule = dataPoints[i]

            # Each elt of quantIntervalsForRule is a tuple {lower bd, upper bd}
            quantIntervalsForRule = self.__kMeansClusterer.getQuantIntervals(rule)
            coordinatesForRule = []
            j = 0
            while j<len(quantIntervalsForRule):
                coordinatesForRule.append(quantIntervalsForRule[j][0])
                coordinatesForRule.append(quantIntervalsForRule[j][1])
                j += 1

            #Make a centroid for the rule, with the coordinates being coordinatesForRule
            centroidForRule = Centroid(coordinatesForRule)

            #seems inefficient to make new centroid out of c1 coords... find a better way

            c1Coords = (vectorAL[0])
            c1copy = Centroid(c1Coords)

            vectorToRulePt = self.__createVector(c1copy, centroidForRule)

            # Distance: dot product of vectorAL and vectorToRulePt, over magnitude of vector AL squared
            distance = 0

            dotProduct = 0

            v1Direction = (vectorAL[1])
            v2Direction = (vectorToRulePt[1])

            # TODO: resolve issue of NaN if init to 0, but otherwise get NaN error...
            magnitudeV1Squared = 0


            if len(v1Direction) == len(v2Direction):

                a = 0
                while a< len(v1Direction):

                    v1Coord = float(v1Direction[a])
                    v2Coord = float(v2Direction[a])

                    dotProduct += (v1Coord * v2Coord)
                    magnitudeV1Squared += (v2Coord * v2Coord)

                    a += 1

                if magnitudeV1Squared > 0:
                    distance = float((dotProduct / magnitudeV1Squared))




            else:
                print("ERROR: v1Direction.size() != v2Direction.size()")

            projectedCoords = []

            direction = (vectorAL[1])

            #new point is vectorAL with t = distance
            if len(direction) == len(c1Coords):
                k = 0
                while k < len(c1Coords):
                    newCoord = float(c1Coords[k]) + distance*float(direction[k])
                    projectedCoords.append(newCoord)
                    k += 1
            else:
                print("ERROR: direction.size() != c1Coords.size()")

            if len(projectedCoords) > 0:
                projectedCentroid = Centroid(projectedCoords)

                # projectedPoints is made into an AL of centroids
                projectedPoints.append(projectedCentroid)


            i += 1

        # Uncomment to check projectedPoints value
        # System.out.println("projectedPoints: " + projectedPoints)

        return projectedPoints

    def __standardizePoints(self, projectedPoints):

        standardizedPoints = []

        mean = self.__getMean(projectedPoints)

        stdDev = self.__getStdDev(mean, projectedPoints)

        currCentroid = None

        numPoints = len(projectedPoints)

        i = 0
        while i<numPoints:

            currCentroid = projectedPoints[i]

            coords = currCentroid.getCoordinates()

            standardizedCoords = []

            j = 0
            while j<len(coords):
                #TODO fix issue: stdDev = 0; divide by 0 --> get float NaN issue
                stdDevCoord = float(float(stdDev[j]))

                if stdDevCoord == 0:
                    #stdDevCoord == 0 means all the points are the same for that coordinate val
                    standardizedCoords.append(float((coords[j] - float(mean[j]))))
                else:
                    standardizedCoords.append(float((coords[j] - mean[j])) / stdDevCoord)

                j += 1

            standardizedCent = Centroid(standardizedCoords)
            standardizedPoints.append(standardizedCent)

            i += 1

        meanStandard = self.__getMean(standardizedPoints)

        stdDevStandard = self.__getStdDev(meanStandard, standardizedPoints)

        # Uncomment to test values
        #  System.out.println("meanStandard: " + meanStandard + " | stdDevStandard: " + stdDevStandard)

        #  System.out.println("standardizedPoints: " + standardizedPoints)

        return standardizedPoints

    def __getMean(self, projectedPoints):
        mean = []

        tempSum = 0

        currCentroid = None

        numPoints = len(projectedPoints)
        print("numPoints: " + numPoints)

        i = 0
        while i<numPoints:
            currCentroid = projectedPoints[i]
            coords = currCentroid.getCoordinates()
            j = 0
            while j<len(coords):

                if mean is not None and len(mean) > j:
                    tempSum = mean[j] + coords[j]
                    mean[j] = tempSum
                else:
                    tempSum = coords[j]
                    mean.append(tempSum)

                j += 1
            i += 1

        i = 0
        while i<len(mean):
            if not numPoints == 0:
                sum = mean[i]
                meanVal = (sum / numPoints)
                mean[i] = meanVal
            else:
                print("ERROR: numPoints == 0")
                mean[i] = float(0)

            i += 1

        return mean

    def __getStdDev(self, mean, projectedPoints):

        stdDev = []
        sdSum = []

        currCentroid = None

        tempSum = 0

        numPoints = len(projectedPoints)

        i = 0
        while i<numPoints:
            currCentroid = projectedPoints[i]
            coords = currCentroid.getCoordinates()
            j = 0
            while j<len(coords):
                if sdSum is not None and len(sdSum) > j:
                    tempSum = sdSum[j] + (coords[j] - mean[j] ** 2 / numPoints)
                    sdSum[j] = tempSum
                else:
                    tempSum = (coords[j] - mean[j] ** 2 / numPoints)
                    sdSum.append(tempSum)
                j += 1

            i += 1

        i = 0
        while i<len(sdSum):
            stdDev.append(math.sqrt(float(sdSum[i])))
            i += 1

        print("stdDev: " + stdDev)

        return stdDev


    # Anderson Darling test (a statistical test of whether a given sample of data is drawn from a given probability distribution) for normal distribution
    def __andersonDarlingTest(self, standardizedPoints):
        #double andersonDarlingResult = 0.0

        numPoints = len(standardizedPoints)

        cumulativeDistribution = self.__applyCumulativeDistributionFxn(standardizedPoints)

        aSqZ = []

        i = 0
        while i<len(cumulativeDistribution):
            CDforCoord = cumulativeDistribution[i]
            CDCoordsize = len(CDforCoord)
            j = 0
            while j<CDCoordsize:

                #TODO fix issue: getting NaN when second log input is negative... and log only defined for x > 0
                addedVal = ((2*(j + 1) - 1) * (math.log(CDforCoord[j]) + math.log(1 - CDforCoord[CDCoordsize - 1 - j])))

                #TODO fix issue: need to check for NaN -- but how to avoid with NaN not impacting calculations?
                if not Double.isNaN(addedVal):
                    if len(aSqZ) > i:
                        aSqZ[i] = aSqZ[i] + addedVal
                    else:
                        aSqZ.append(addedVal)
                else:
                    if len(aSqZ) > i:
                        aSqZ[i] = 0.0
                    else:
                        aSqZ.append(0.0)

                j += 1

            if len(aSqZ) > i:
                aSqZ[i] = (-1 * aSqZ[i] / CDCoordsize) - CDCoordsize


            i += 1

        # Uncomment to test aSqZ value 
        # System.out.println("aSqZ: " + aSqZ)

        aSqZStar = []

        i = 0
        while i<len(aSqZ):
            CDforCoord = cumulativeDistribution[i]
            n = len(CDforCoord)

            aSqZStar.append(aSqZ[i] * (1 + 4/(n - 25/(n ** 2))))

            i += 1

        # Uncomment to test aSqZStar value (the metric for the A-D test result)
        #System.out.println("aSqZStar: " + aSqZStar)

        return aSqZStar

    def __applyCumulativeDistributionFxn(self, standardizedPoints):

        # Has the cumulative distribution of each x_i, for each x_i in the coordinates of the centroid
        cumulativeDistribution = []

        # ArrayList with elts that are ALs of all the vals for each coordinate x_i
        ALsOfCoords = []

        i = 0
        while i<len(standardizedPoints):
            thisCentroid = standardizedPoints[i]
            coords = thisCentroid.getCoordinates()
            j = 0
            while j<len(coords):
                if len(ALsOfCoords) > j:
                    thisCoordAL = ALsOfCoords[j]
                    thisCoordAL.append(coords[j])
                    ALsOfCoords[j] = thisCoordAL
                else:
                    thisCoordAL = []
                    thisCoordAL.append(coords[j])
                    ALsOfCoords.append(thisCoordAL)
                j += 1
            i += 1

        #ALsOfCooords has, at each index, all the coordinates for that coordinate place.
        i = 0
        while i<len(ALsOfCoords):

            thisCoordAL = ALsOfCoords[i]

            # Make all values their absolute values, because we need the magnitude, and will be squared in computations
            j = 0
            while j<len(thisCoordAL):

                coord = thisCoordAL[j]

                if isinstance(coord, Number):
                    thisCoordAL[j] = abs((coord).doubleValue())

                j += 1

            thisCoordAL.sort()

            # Transform into a hashmap with key = x value, value = num. occurrences
            thisCoordHM = {}
            j = 0
            while j<len(thisCoordAL):
                thisCoord = thisCoordAL[j]
                if thisCoord in thisCoordHM.keys():
                    thisCoordHM.update({thisCoord: int(thisCoordHM[thisCoord]) + 1})
                    #TODO: remove double occurrence?

                else:
                    thisCoordHM.update({thisCoord: 1})
                j += 1

            numDistinctVals = len(thisCoordHM.keys())

            thisCoordCDF = []
            cumulativeDistVal = 0.0

            prevVal = 0.0

            #TODO fix issue: cumulative distribution should be between 0 and 1, and this is not the case.
            j = 0
            while j<len(thisCoordAL):

                #TODO: throw conversion error if applicable
                coordDoubleVal = float(thisCoordAL[j])

                numOccurences = thisCoordHM[thisCoordAL[j]]

                power = (-0.5 * coordDoubleVal * coordDoubleVal)
                ePower = math.exp(power)
                sqrt2Pi = math.sqrt(2 * math.pi)

                #for summation / Riemann sum, multiply height (f(x) val) times change in x.
                fXVal = (ePower / sqrt2Pi)

                #change in x value
                dx = 0.0

                if j == 0:
                    dx = coordDoubleVal
                else:
                    dx = coordDoubleVal - prevVal

                addedVal = 0.0

                #numDistinctVals is the 'number of rectangles' in the Riemann sum
                addedVal = (numOccurences * (fXVal * dx)) / numDistinctVals

                # TODO: check that this relies on other values, and does so correctly
                cumulativeDistVal += addedVal

                # TODO: need to make sure doesn't increment each time if numOccurrences > 1.
                if not Double.isNaN(cumulativeDistVal):
                    q = 0
                    while q<numOccurences:
                        thisCoordCDF.append(cumulativeDistVal)
                        q += 1

                #set prevVal, for next iteration
                prevVal = float(thisCoordAL[j])
                # - 1 because j++ each iteration
                j += (numOccurences - 1)


                j += 1

            cumulativeDistribution.append(thisCoordCDF)
            i += 1

        # Uncomment to check the cumulative distribution
        # System.out.println("ALsOfCoords sorted: " + ALsOfCoords)
        # System.out.println("cumulativeDistribution: " + cumulativeDistribution)


        return cumulativeDistribution


    def __isNonCritical(self, andersonDarlingResult):
        isNonCritical = True

        # Based on the research paper's suggestion. Maybe modify based on other sources.
        criticalValue = 1.8692

        i = 0
        while i<len(andersonDarlingResult):
            if andersonDarlingResult[i] > criticalValue:
                isNonCritical = False
                return isNonCritical
            i += 1


        return isNonCritical

    def getParametresReglesQuantitives(self):
        return self.m_parametresReglesQuantitatives


import math
import sys
sys.path.append('C:\\Users\\aalsahee\\python_physical_model\\Saudi\\trace\\Traces\\qtm\\src\\')

# from apriori import *
# from database import *
# from geneticAlgorithm import *

class KMeansClusterer(object):

    #parametrized constructor
    def __init__(self, assocRules, input_parametresReglesQuantitatives):
        self.__originalInterval = [sys.float_info.max, -sys.float_info.max]
        self.__initialInterval = [sys.float_info.max, -sys.float_info.max]
        self.__NUM_K_CLUSTERS = 3
        self.__NUM_GENERATIONS = 1000
        self.__kMeansAssocRules = None
        self.__listOfCentroids = []
        self.__centroidClusters = {}
        print("self.__centroidClusters8: " + str(self.__centroidClusters))
        self.__roundedCentroids = []
        self.m_parametresReglesQuantitatives = None


        self.__kMeansAssocRules = []
        self.__listOfCentroids = []
        self.__centroidClusters = {}
        print("self.__centroidClusters9: " + str(self.__centroidClusters))
        self.__roundedCentroids = []

        self.m_parametresReglesQuantitatives = input_parametresReglesQuantitatives

        for a in assocRules:
            self.__kMeansAssocRules.append(a)


    # Return the average distance between all AssocationRules in kMeansAssocRules
    def testRuleProximities(self):

        avgDistance = 0.0

        sizeOfARList = len(self.__kMeansAssocRules)

        i = 0
        while i<sizeOfARList:
            ruleConsidered1 = self.__kMeansAssocRules[i]

            listOfIntervalsA = self.getQuantIntervals(ruleConsidered1)

            numDifferentPoints = 0

            j = i+1
            while j<sizeOfARList:

                ruleConsidered2 = self.__kMeansAssocRules[j]
                listOfIntervalsB = self.getQuantIntervals(ruleConsidered2)

                floatDistance = 0
                #list of intervals has intervals ([, ], [, ], [, ]) etc in assocation rule from left to right
                a = 0
                while a < len(listOfIntervalsA):
                    intervalA = listOfIntervalsA[a]
                    intervalB = listOfIntervalsB[a]

                    b = 0
                    while b<len(intervalB):

                        coordinate = abs(intervalA[b] - intervalB[b])
                        coordSquared = coordinate*coordinate

                        floatDistance += coordSquared

                        b += 1

                    a += 1

                distance = math.sqrt(floatDistance)

                #add up all this distances
                avgDistance += distance

                j += 1

            i += 1

        #sum of nums from 1 to (n - 1) is 0.5(n-1)(n-2)
        avgDistance /= ((sizeOfARList-1)*(sizeOfARList - 2) * 0.5)

        return avgDistance


    def getQuantIntervals(self, ruleConsidered):
        item = None
        itemQual = None
        itemQuant = None
        iIndiceItem = 0
        #each elt is an array of len 2: m_tBornes = {min, max}
        listOfIntervals = []

        if ruleConsidered is None:
            print("rule considered is null")
            return None

        iIndiceItem = 0
        while iIndiceItem < ruleConsidered.m_iNombreItemsGauche:

            item = ruleConsidered.ObtenirItemGauche(iIndiceItem)

            if item.m_iTypeItem == Item.ITEM_TYPE_QUANTITATIF:

                itemQuant = item

                listOfIntervals.append(itemQuant.m_tBornes)

            iIndiceItem += 1


        iIndiceItem = 0
        while iIndiceItem < ruleConsidered.m_iNombreItemsDroite:

            item = ruleConsidered.ObtenirItemDroite(iIndiceItem)

            if item.m_iTypeItem == Item.ITEM_TYPE_QUANTITATIF:

                itemQuant = item

                listOfIntervals.append(itemQuant.m_tBornes)

            iIndiceItem += 1

        return listOfIntervals



    def applyKMeansAlgo(self, *args):
        if len(args) == 0:
            #run k means with default number of k clusters
            return self.applyKMeansAlgo(self.__NUM_K_CLUSTERS)
        if len(args) == 1:
            numForK = args[0]
            leftIsQuantitative = False
            rightIsQuantitative = False
    
            intervals = []
    
            #Get the min and max of intervals for quantitative LHS and/or RHS
            i = 0
            while i<len(self.__kMeansAssocRules):
    
                #maybe initialize outside of the for loop, b/c that would be less expensive.
                ruleConsidered = self.__kMeansAssocRules[i]
    
                item = None
                itemQual = None
                itemQuant = None
                iIndiceItem = 0
                intervalIndexCount = 0
    
                if ruleConsidered is None:
                    print("rule considered is null")
                    return None
    
                #left part of rule, if quantitative:
    
                iIndiceItem = 0
                while iIndiceItem < ruleConsidered.m_iNombreItemsGauche:
    
                    item = ruleConsidered.ObtenirItemGauche(iIndiceItem)
    
                    if item.m_iTypeItem == Item.ITEM_TYPE_QUANTITATIF:
    
                        itemQuant = item
    
                        originalInterval = [sys.float_info.max, -sys.float_info.max]
                        if len(intervals) <= intervalIndexCount:
                            intervals.append(originalInterval)
    
                        if itemQuant.m_tBornes[0] <= intervals[intervalIndexCount][0]:
                            intervals[intervalIndexCount][0] = itemQuant.m_tBornes[0]
    
                        #set max of left interval, if smaller
                        if itemQuant.m_tBornes[1] >= intervals[intervalIndexCount][1]:
                            intervals[intervalIndexCount][1] = itemQuant.m_tBornes[1]
    
                        intervalIndexCount += 1
    
                    iIndiceItem += 1
    
                #right part of rule, if quantitative: 
    
                iIndiceItem = 0
                while iIndiceItem<ruleConsidered.m_iNombreItemsDroite:
    
                    item = ruleConsidered.ObtenirItemDroite(iIndiceItem)
    
                    if item.m_iTypeItem == Item.ITEM_TYPE_QUANTITATIF:
    
                        itemQuant = item
    
    
                        originalInterval = [sys.float_info.max, -sys.float_info.max]
                        if len(intervals) <= intervalIndexCount:
                            intervals.append(originalInterval)
    
                        if itemQuant.m_tBornes[0] <= intervals[intervalIndexCount][0]:
                            intervals[intervalIndexCount][0] = itemQuant.m_tBornes[0]
    
                        #set max of left interval, if smaller
                        if itemQuant.m_tBornes[1] >= intervals[intervalIndexCount][1]:
                            intervals[intervalIndexCount][1] = itemQuant.m_tBornes[1]
    
                        intervalIndexCount += 1
    
                    iIndiceItem += 1
                i += 1
    
            #Generating random centroids
    
            i = 0
            while i< numForK:
                self.__listOfCentroids.append(self.generateRandomCentroid(intervals))
                i += 1
    
            listOfCentroidsPrev = []
            roundedCentroids = []
    
            numIterations = 0
            while numIterations < self.__NUM_GENERATIONS and ((not self.__equalLists(roundedCentroids, listOfCentroidsPrev)) or len(    roundedCentroids) == 0 and len(listOfCentroidsPrev) == 0):
                #find nearest centroid for each rule
    
                #clear centroidClusters
                self.__centroidClusters.clear()
                print("self.__centroidClusters10: " + str(self.__centroidClusters))
    
                i = 0
                while i<len(self.__kMeansAssocRules):
    
                    ruleConsidered = self.__kMeansAssocRules[i]
    
                    itemsQuant = []
    
                    itemsQuant = self.__findItemsQuant(ruleConsidered)
    
                    nearestCentroid = self.findNearestCentroid(itemsQuant)
                    
                    print("self.__centroidClusters11: " + str(self.__centroidClusters))
                    if nearestCentroid not in self.__centroidClusters.keys():
                        rulesForCentroid = []
                        self.__centroidClusters.update({nearestCentroid: rulesForCentroid})
                    
                    print("self.__centroidClusters12: " + str(self.__centroidClusters))
                    # centroidClusters.get(nearestCentroid) is the ArrayList with the rules for the centroid's cluster
                    print("ruleConsidered: " + str(ruleConsidered))
                    self.__centroidClusters[nearestCentroid].append(ruleConsidered)
    
                    i += 1
    
                # get rounded centroid coordinates (for comparison, to see when to stop iterating in the k-means algorithm)
    
                listOfCentroidsPrev = self.__listOfCentroids.copy()
                listOfCentroidsPrev = self.roundCentroids(listOfCentroidsPrev)
    
                #relocate centroids
                newCentroids = self.relocateCentroids(self.__centroidClusters)
                roundedCentroids = self.roundCentroids(newCentroids)
                print(self.m_listeRegles)
    
                # numIterations ensures that the loop does not run forever. only consider if lists not equal if we have not exceeded the    max number of iterations
                if numIterations < self.__NUM_GENERATIONS - 1 and not self.__equalLists(roundedCentroids, listOfCentroidsPrev):
                    self.__listOfCentroids = newCentroids
    
                numIterations += 1
            # end of while loop

            totalNumPoints = 0
            i = 0
            while i<len(self.__listOfCentroids):
                print("self.__centroidClusters13: " + str(self.__centroidClusters))
                if self.__centroidClusters[self.__listOfCentroids[i]] is not None:
                    totalNumPoints += len(self.__centroidClusters[self.__listOfCentroids[i]])
                i += 1
    
            i = 0
            while i<len(self.__listOfCentroids):
    
                centroidRule = ""
    
                thisCentroid = self.__listOfCentroids[i]
                
                print("self.__centroidClusters14: " + str(self.__centroidClusters))
                #set centroid's number of occurrences
                if self.__centroidClusters[thisCentroid] is None:
                    thisCentroid.setNumOccurrences(0)
                else:
                    print("self.__centroidClusters15: " + str(self.__centroidClusters))
                    thisCentroid.setNumOccurrences(len(self.__centroidClusters[thisCentroid]))
    
                #set centroid's support
                if totalNumPoints > 0:
                    thisCentroid.setSupport((math.trunc((100*thisCentroid.getNumOccurrences()) / float(totalNumPoints))))
                else:
                    thisCentroid.setSupport(0)
    
                #set centroid's confidence
    
                support = thisCentroid.getSupport()
    
                if support > 0:
                    thisCentroid.setConfidence((math.trunc((100*thisCentroid.getNumOccurrences()) / float(support))))
                else:
                    thisCentroid.setConfidence(0)
    
                centroidRule = self.__constructCentroidRule(thisCentroid, totalNumPoints)
    
                thisCentroid.setCentroidRule(centroidRule)
    
                i += 1
    
            # Rule proximity to use
            ruleProximity = self.testRuleProximities()
    
            i = 0
            while i<len(self.__listOfCentroids):
    
                centroidConsidered = self.__listOfCentroids[i]
    
                # Uncomment to see the minimum support and confidence parameters
                # System.out.println("m_parametresReglesQuantitatives.m_fMinSupp: " + m_parametresReglesQuantitatives.m_fMinSupp)
                # System.out.println("m_parametresReglesQuantitatives.m_fMinConf: " + m_parametresReglesQuantitatives.m_fMinConf)
    
                j = 0
                while j<len(self.__listOfCentroids):
    
                    centroidInComparison = self.__listOfCentroids[j]
    
                    distanceBtwnCentroids = self.calculateEuclideanDistance(centroidConsidered.getCoordinates(), centroidInComparison.  getCoordinates())
                    if j != i:
    
                        # Use euclidean distance to remove 'similar' rules. TODO: consider how to find how far to consider 'distinct'
                        if distanceBtwnCentroids < float((ruleProximity)):
                            centroidConsidered.setNumOccurrences(centroidConsidered.getNumOccurrences() + centroidInComparison. getNumOccurrences())
    
                            centroidConsidered.setSupport(centroidConsidered.getSupport() + centroidInComparison.getSupport())
    
                            centroidConsidered.setConfidence(centroidConsidered.getConfidence() + centroidInComparison.getConfidence())
    
                            self.__listOfCentroids.pop(j)
                            j -= 1
                    j += 1
                i += 1
            #the rules are the list of centroids
            return self.__listOfCentroids

    def getCentroidClusters(self):
        print("self.__centroidClusters16: " + str(self.__centroidClusters))
        return self.__centroidClusters


    def __constructCentroidRule(self, thisCentroid, totalNumPoints):

        centroidRule = ""

        print("self.__centroidClusters17: " + str(self.__centroidClusters))
        if self.__centroidClusters[thisCentroid] is None:
            return centroidRule

        numOccurrences = thisCentroid.getNumOccurrences()

        support = thisCentroid.getSupport()
        confidence = thisCentroid.getConfidence()

        centroidRule += ("support = " + numOccurrences + " (" + support + "%) , ")

        centroidRule += ("confidence = " + confidence + " %  :  ")

        print("self.__centroidClusters18: " + str(self.__centroidClusters))
        firstRuleMapped = self.__centroidClusters[thisCentroid][0] # to get the items on left and right, since same for all mapped rules for that Centroid
        r = 0
        j = 0
        while j<firstRuleMapped.m_iNombreItemsGauche:
            item = firstRuleMapped.ObtenirItemGauche(j)

            if item.m_iTypeItem == Item.ITEM_TYPE_QUANTITATIF:

                #just get 0th item's to string, since we want the labels, not the quantitative values, but we will just use the labels frm the 0th item
                stringToPrint = (item).toString(0)
                if "[" in stringToPrint:
                    stringToPrint = stringToPrint[0:stringToPrint.find("[") - 1]
                centroidRule += stringToPrint

                centroidRule += (" [ " + thisCentroid.getRoundedCoordinates()[r] + " , " + thisCentroid.getRoundedCoordinates()[r+1] + " ]")
                r = r+2
            else:
                centroidRule += ((item).toString())

            if j < firstRuleMapped.m_iNombreItemsGauche - 1:
                centroidRule += " AND "
            j += 1

        centroidRule += "  -->  "

        j = 0
        while j<firstRuleMapped.m_iNombreItemsDroite:

            #and, or, etc? how to tell this?
            item = firstRuleMapped.ObtenirItemDroite(j)

            if item.m_iTypeItem == Item.ITEM_TYPE_QUANTITATIF:

                #just get 0th item's to string, since we want the labels, not the quantitative values, but we will just use the labels frm the 0th item
                stringToPrint = (item).toString(0)
                if "[" in stringToPrint:
                    stringToPrint = stringToPrint[0:stringToPrint.find("[") - 1]
                centroidRule += stringToPrint
                centroidRule += (" [ " + thisCentroid.getRoundedCoordinates()[r] + " , " + thisCentroid.getRoundedCoordinates()[r+1] + " ]")
                r = r+2
            else:
                centroidRule += ((item).toString())
            if j < firstRuleMapped.m_iNombreItemsDroite - 1:
                centroidRule += " AND "
            j += 1

        return centroidRule


    #TODO: optimize this, since is intensive operation
    def __equalLists(self, list1, list2):

        if len(list1) == len(list2):
            i = 0
            while i<len(list1):

                isInList = False
                cent1 = list1[i]
                coords1 = cent1.getCoordinates()

                j = 0
                while j<len(list2):
                    cent2 = list2[j]
                    coords2 = cent2.getCoordinates()
                    if coords1 is coords2:
                        isInList = True
                    j += 1

                if not isInList:
                    #Lists not equal
                    return False

                i += 1
        else:
            #Lists not equal
            return False

        #Lists equal
        return True


    def roundCentroids(self, listOfCentroids):
        self.__roundedCentroids = []

        i = 0
        while i<len(listOfCentroids):

            roundedCent = Centroid.Centroid((listOfCentroids[i]).getRoundedCoordinates())
            self.__roundedCentroids.append(roundedCent)

            i += 1

        return self.__roundedCentroids

    def __findItemsQuant(self, ruleConsidered):

        itemsQuant = []

        iIndiceItem = 0
        while iIndiceItem < ruleConsidered.m_iNombreItemsGauche:

            item = ruleConsidered.ObtenirItemGauche(iIndiceItem)

            if item.m_iTypeItem == Item.ITEM_TYPE_QUANTITATIF:
                itemQuant = item
                itemsQuant.append(itemQuant)

            iIndiceItem += 1

        iIndiceItem = 0
        while iIndiceItem < ruleConsidered.m_iNombreItemsDroite:

            item = ruleConsidered.ObtenirItemDroite(iIndiceItem)

            if item.m_iTypeItem == Item.ITEM_TYPE_QUANTITATIF:
                itemQuant = item
                itemsQuant.append(itemQuant)

            iIndiceItem += 1

        return itemsQuant


    def calculateEuclideanDistance(self, coordinates1, coordinates2):

        sum = 0
        i = 0
        while i<len(coordinates1):
            xCoordinate = abs(float(coordinates1[i]) - float(coordinates2[i]))
            yCoordinate = abs(float(coordinates1[i + 1]) - float(coordinates2[i + 1]))

            xCoordSquared = xCoordinate * xCoordinate
            yCoordSquared = yCoordinate * yCoordinate
            sum = sum + xCoordSquared + yCoordSquared

            i = i+2

        distance = math.sqrt(sum)

        return distance


    def generateRandomCentroid(self, intervals):

        r = random.random()

        #randomCoords[0] is random x coord, randomCoords[1] is random y coord, randomCoords[2] is random z coord, randomCoords[3] is random q coord, etc
        randomCoords = [0 for _ in range(len(intervals) * 2)]

        k =0

        #x and y random interval in i and i+1 index in randomCoords
        i = 0
        while i<len(intervals)*2:
            #random y coordinate 
            #intervals[i][0] is min of interval i for example
            r = random.random()
            randomCoords[i] = (intervals[k][0] + r * (intervals[k][1] - intervals[k][0]))
            #random y coordinate
            #intervals[i][1] is max of interval i for example
            #use random x coordinate as min because, since we are dealing with intervals as our "coordinates" for the Centroid, it only logically makes sense for randomYCoord to be >= randomXCoord 
            r = random.random()
            randomCoords[i+1] = randomCoords[i] + r * (intervals[k][1] - randomCoords[i])

            k += 1

            i = i+2

        randomCentroid = Centroid.Centroid(randomCoords)

        return randomCentroid



    def findNearestCentroid(self, itemsQuant):

        #coordinates of the centroid to test against the random centroids
        myCoordinates = []

        myCoordinates = self.__getCoordinatesForItemsQuant(itemsQuant)

        minDistance = sys.float_info.max

        nearestCentroid = Centroid.Centroid()

        i = 0
        while i<len(self.__listOfCentroids):

            #currCentroid is the current random centroid
            currCentroid = (self.__listOfCentroids[i])

            #find distance between random current centroid and myCoordinates, the coordinates of the centroid considered
            euclidDistance = self.calculateEuclideanDistance(myCoordinates, currCentroid.getCoordinates())

            if euclidDistance < minDistance:
                nearestCentroid = self.__listOfCentroids[i]
                minDistance = euclidDistance

            i += 1

        return nearestCentroid

    def __getCoordinatesForItemsQuant(self, itemsQuant):

        myCoordinates = []

        i = 0
        while i<len(itemsQuant):
            minOfItem = itemsQuant[i].m_tBornes[0]
            maxOfItem = itemsQuant[i].m_tBornes[1]

            myCoordinates.append(minOfItem)
            myCoordinates.append(maxOfItem)
            i += 1

        return myCoordinates


    def relocateCentroids(self, centroidClusters):
        relocatedCentroids = []

        i = 0
        while i<len(self.__listOfCentroids):
            thisCentroid = self.__listOfCentroids[i]
            mappedCoords = centroidClusters[thisCentroid]
            #centroidClusters.remove(thisCentroid)
            newCentroid = self.__avgCentroidForCluster(thisCentroid, mappedCoords)

            relocatedCentroids.append(newCentroid)

            i += 1

        return relocatedCentroids


    def __avgCentroidForCluster(self, centroid, mappedPoints):
        if mappedPoints is None or len(mappedPoints) == 0:
            #Mapped coords is null
            return centroid

        coordsAvg = []

        #each mapped points is an assocation rule
        i = 0
        while i<len(mappedPoints):
            itemsQuant = []
            itemsQuant = self.__findItemsQuant(mappedPoints[i])
            coordinatesForItems = self.__getCoordinatesForItemsQuant(itemsQuant)
            j = 0
            while j<len(coordinatesForItems):
                if len(coordsAvg) <= j:
                    coordsAvg.append(float(0))

                coordsAvg[j] = float(coordsAvg[j]) + float(coordinatesForItems[j])


                j += 1

            i += 1

        j = 0
        while j<len(coordsAvg):
            #check that the size of coordsAvg and coordinatesForItems is the same?
            coordsAvg[j] = float(coordsAvg[j]) / float(len(mappedPoints))
            j += 1


        avgCentroid = Centroid(coordsAvg)
        return avgCentroid



    def getParametresReglesQuantitives(self):
        return self.m_parametresReglesQuantitatives

    # Hard-coded number of clusters for K-means. If want flexible number of clusters, use G-means.
    #list of rounded centroids, given a list of centroids


#                                             
# *Copyright 2007, 2011 CCLS Columbia University (USA), LIFO University of Orleans (France), BRGM (France)
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


# Class listing all the parameters defined by the user for the next one
# loading a rules file.
# Class enumerating all the parameters defined by the user to be used for the next loading of a rule file.

class LoadingParameters(object):
    def __init__(self):
        self.m_sNomFichier = None
        self.m_sNomUtilisateurOrigine = None
        self.m_sNomBaseOrigine = None
        self.m_sDateOrigine = None
        self.m_sDescriptionRegles = None
        self.m_sDescriptionCompleteContexte = None

        self.m_sNomFichier = None
        self.m_sNomUtilisateurOrigine = "User unknown"
        self.m_sNomBaseOrigine = "Database unknown"
        self.m_sDateOrigine = "Date unknown"
        self.m_sDescriptionRegles = "Missing Description"
        self.m_sDescriptionCompleteContexte = "No information."


    def toString(self):
        return self.m_sDescriptionCompleteContexte

#                                             
# *Copyright 2007, 2011 CCLS Columbia University (USA), LIFO University of Orleans (France), BRGM (France)
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
sys.path.append('C:\\Users\\aalsahee\\python_physical_model\\Saudi\\trace\\Traces\\qtm\\src\\')

# from apriori import *
# from database.onefile import *
# from solver.ResolutionContext import ResolutionContext

# 

# Defines the use for which the parameters are intended (can modify the behavior of some methods):
# 

class PositionRuleParameters(object):

    # (for a qualitative attribute, it suffices that one of its items is mandatory for it to be considered mandatory)
    PARAMETRES_POSITION_REGLES = 0 # PARAMETERS POSITION RULES
    PARAMETRES_FILTRAGE_REGLES = 1 # PARAMETERS FILTER RULES



    # Storage class of parameters on qualitative attributes:
    #    *
    #     * Class of parameters for qualitative (categorical) attributes
    #     
    class ParametresItemsQualitatifs(object):



        def __init__(self, outerInstance):
            self.m_iTypePriseEnCompte = 0
            self.m_bPresenceObligatoire = False

            self.__outerInstance = outerInstance

            self.m_iTypePriseEnCompte = ResolutionContext.PRISE_EN_COMPTE_ITEM_NULLE_PART
            self.m_bPresenceObligatoire = False



    # 
    #    *
    #     * Class of parameters for quantitative (numerical) attributes
    #     
    class ParametresAttributsQuantitatifs(object):



        def __init__(self, outerInstance):
            self.m_iTypePriseEnCompte = 0
            self.m_bPresenceObligatoire = False

            self.__outerInstance = outerInstance

            self.m_iTypePriseEnCompte = ResolutionContext.PRISE_EN_COMPTE_ITEM_NULLE_PART
            self.m_bPresenceObligatoire = False






    def __init__(self, contexteResolution, iTypeParametrage):
        self.__m_iTypeParametrage = 0
        self.__m_contexteResolution = None
        self.__m_tableParametresItemsQualitatifs = None
        self.__m_tableParametresAttributsQuantitatifs = None
        self.__m_tablePresenceObligatoire = None

        self.__m_iTypeParametrage = iTypeParametrage

        self.__m_contexteResolution = contexteResolution

        self.__m_tableParametresItemsQualitatifs = {}
        self.__m_tableParametresAttributsQuantitatifs = {}
        self.__m_tablePresenceObligatoire = {}
        
    # * Build or adapt, following a modification of the attributes considered in the DB,
    # * a data structure at 2 levels of hashing tables, the first on the name of
    # * the attributes, the second on the items. Only for the qualitative (categorical) attibutes.
    #     
    def GenererStructuresDonneesSelonBDPriseEnCompte(self):
        parametreItemDefaut = None
        parametreQuantDefaut = None
        iNombreColonnesPrisesEnCompte = 0
        iIndiceColonne = 0
        iIndiceItem = 0
        colonne = None
        sousTable = None
        tListeItems = None
        bEnregistrerParametres = False


        if self.__m_contexteResolution.m_gestionnaireBD == None:
            return

        # In the case of filtering information, we reset the parameters:
        if self.__m_iTypeParametrage == self.PARAMETRES_FILTRAGE_REGLES:
            self.__m_tableParametresItemsQualitatifs.clear()
            self.__m_tableParametresAttributsQuantitatifs.clear()
            # print("len1: " + str(len(self.__m_tableParametresAttributsQuantitatifs)))
            self.__m_tablePresenceObligatoire.clear()

        #Number of items checked in Step 1
        iNombreColonnesPrisesEnCompte = self.__m_contexteResolution.m_gestionnaireBD.ObtenirNombreColonnesPrisesEnCompte()
        iIndiceColonne = 0
        while iIndiceColonne < iNombreColonnesPrisesEnCompte:

            #Get the column information about the selected column in step 1, i.e the data load step
            colonne = self.__m_contexteResolution.m_gestionnaireBD.ObtenirColonneBDPriseEnCompte(iIndiceColonne)
            
            if not colonne.m_sNomColonne == None:
                
                # # ATTRIBUTS QUALITATIFS :
                # print(DatabaseAdmin.TYPE_VALEURS_COLONNE_ITEM)
                # print(colonne.m_iTypeValeurs)
                # print(self.__m_tableParametresItemsQualitatifs.keys())
                if colonne.m_iTypeValeurs == DatabaseAdmin.TYPE_VALEURS_COLONNE_ITEM:

                    # Table des items qualitatifs :

                    # If the attribute is already listed, we do not modify the information concerning it,
                     # otherwise we create a new entry:
                    if colonne.m_sNomColonne not in self.__m_tableParametresItemsQualitatifs.keys():
                        sousTable = {}

                        self.__m_tableParametresItemsQualitatifs.update({colonne.m_sNomColonne: sousTable})
                        
                        tListeItems = colonne.ConstituerTableauValeurs()
                        iIndiceItem = 0
                        while iIndiceItem < len(tListeItems):
                            if tListeItems[iIndiceItem] is not None:

                                # If we are constructing the filtering parameters, we do not consider
                                # that the items retained to constitute the rules:
                                bEnregistrerParametres = True
                                if self.__m_iTypeParametrage == self.PARAMETRES_FILTRAGE_REGLES:
                                    bEnregistrerParametres = not (self.__m_contexteResolution.ObtenirTypePrisEnCompteItem(colonne.m_sNomColonne, tListeItems[iIndiceItem]) == ResolutionContext.PRISE_EN_COMPTE_ITEM_NULLE_PART)

                                if bEnregistrerParametres:
                                    parametreItemDefaut = PositionRuleParameters.ParametresItemsQualitatifs(self)

                                    if self.__m_iTypeParametrage == self.PARAMETRES_FILTRAGE_REGLES:
                                        parametreItemDefaut.m_iTypePriseEnCompte = self.__m_contexteResolution.ObtenirTypePrisEnCompteItem(colonne.m_sNomColonne, tListeItems[iIndiceItem])
                                        parametreItemDefaut.m_bPresenceObligatoire = self.__m_contexteResolution.ObtenirPresenceObligatoireItem(colonne.m_sNomColonne, tListeItems[iIndiceItem])
                                    else:
                                        if (tListeItems[iIndiceItem].strip()) == "":
                                            parametreItemDefaut.m_iTypePriseEnCompte = ResolutionContext.PRISE_EN_COMPTE_ITEM_NULLE_PART
                                        else:
                                            parametreItemDefaut.m_iTypePriseEnCompte = ResolutionContext.PRISE_EN_COMPTE_ITEM_NULLE_PART #PRISE_EN_COMPTE_ITEM_2_COTES;
                                        parametreItemDefaut.m_bPresenceObligatoire = False

                                    sousTable.update({tListeItems[iIndiceItem]: parametreItemDefaut})
                                    # print(sousTable)
                            iIndiceItem += 1


                        # Table of quantitative attributes:
                        # print(self.__m_tableParametresAttributsQuantitatifs)
                        # print("VV: " + str(colonne.m_sNomColonne))
                        if colonne.m_sNomColonne in self.__m_tableParametresAttributsQuantitatifs.keys():
                            # print("len22: " + str(len(self.__m_tableParametresAttributsQuantitatifs)))
                            self.__m_tableParametresAttributsQuantitatifs.pop(colonne.m_sNomColonne)
                        # print("len2: " + str(len(self.__m_tableParametresAttributsQuantitatifs)))
                        # print("-len2: " + str(len(self.__m_tableParametresItemsQualitatifs)))
                        



                # QUANTITATIVE ATTRIBUTES:
                elif colonne.m_iTypeValeurs == DatabaseAdmin.TYPE_VALEURS_COLONNE_REEL:

                    # Table of qualitative items:
                    if colonne.m_sNomColonne in self.__m_tableParametresItemsQualitatifs.keys():
                        self.__m_tableParametresItemsQualitatifs.pop(colonne.m_sNomColonne)


                    # Table of quantitative attributes:
                    if colonne.m_sNomColonne not in self.__m_tableParametresAttributsQuantitatifs.keys():
                        # print("len3: " + str(len(self.__m_tableParametresAttributsQuantitatifs)))

                        # If we are constructing the filtering parameters, we do not consider
                        # that the attributes retained to constitute the rules:
                        bEnregistrerParametres = True
                        if self.__m_iTypeParametrage == self.PARAMETRES_FILTRAGE_REGLES:
                            bEnregistrerParametres = not (self.__m_contexteResolution.ObtenirTypePrisEnCompteAttribut(colonne.m_sNomColonne) == ResolutionContext.PRISE_EN_COMPTE_ITEM_NULLE_PART)

                        if bEnregistrerParametres:
                            parametreQuantDefaut = self.ParametresAttributsQuantitatifs(self)

                            if self.__m_iTypeParametrage == self.PARAMETRES_FILTRAGE_REGLES:
                                parametreQuantDefaut.m_iTypePriseEnCompte = self.__m_contexteResolution.ObtenirTypePrisEnCompteAttribut(colonne.m_sNomColonne)
                                parametreQuantDefaut.m_bPresenceObligatoire = (self.__m_contexteResolution.ObtenirPresenceObligatoireAttribut(colonne.m_sNomColonne) == 1)
                            else:
                                parametreQuantDefaut.m_iTypePriseEnCompte = ResolutionContext.PRISE_EN_COMPTE_ITEM_NULLE_PART
                                parametreQuantDefaut.m_bPresenceObligatoire = False

                                # If the attribute contains only missing values, we ignore it:
                                if colonne.m_iNombreValeursReellesCorrectes <= 0:
                                    parametreQuantDefaut.m_iTypePriseEnCompte = ResolutionContext.PRISE_EN_COMPTE_ITEM_NULLE_PART
                                    parametreQuantDefaut.m_bPresenceObligatoire = False
                            # print("KK: " + str(colonne.m_sNomColonne))
                            self.__m_tableParametresAttributsQuantitatifs.update({colonne.m_sNomColonne: parametreQuantDefaut})
                            # print("len4: " + str(len(self.__m_tableParametresAttributsQuantitatifs)))

            iIndiceColonne += 1





    def DefinirTypePrisEnCompteItem(self, sAttribut, sItem, iTypePosition):
        sousTable = None
        parametres = None

        if (sAttribut == None) or (sItem == None):
            return

        sousTable = (self.__m_tableParametresItemsQualitatifs[sAttribut])
        if sousTable == None:
            return

        parametres = (sousTable[sItem])
        if parametres == None:
            return

        # Modification of the value taken into account:
        parametres.m_iTypePriseEnCompte = iTypePosition


    #    *
    #     * return categorical item's position in the rule
    #     * @param sAttribut
    #     * @param sItem
    #     * @return int
    #     
    def ObtenirTypePrisEnCompteItem(self, sAttribut, sItem):
        iTypePosition = 0
        sousTable = None
        parametres = None

        if (sAttribut == None) or (sItem == None):
            return 0

        sousTable = (self.__m_tableParametresItemsQualitatifs[sAttribut])
        if sousTable == None:
            return 0

        parametres = (sousTable[sItem])
        if parametres == None:
            return 0
        else:
            return parametres.m_iTypePriseEnCompte


    # DefineTypeAccountAttribute
    def DefinirTypePrisEnCompteAttribut(self, sAttribut, iTypePosition):
        parametreItemDefaut = None
        parametreQuantDefaut = None
        sousTable = None
        enumItems = None

        # Quantitative attribute:
        parametreQuantDefaut = (self.__m_tableParametresAttributsQuantitatifs[sAttribut])
        # print("len5: " + str(len(self.__m_tableParametresAttributsQuantitatifs)))
        if not parametreQuantDefaut == None:
            parametreQuantDefaut.m_iTypePriseEnCompte = iTypePosition

        # Qualitative attribute:
        else:
            sousTable = (self.__m_tableParametresItemsQualitatifs[sAttribut])
            if not sousTable == None:

                enumItems = sousTable.elements()
                if enumItems.hasMoreElements():

                    while enumItems.hasMoreElements():
                        parametreItemDefaut = enumItems.nextElement()
                        parametreItemDefaut.m_iTypePriseEnCompte = iTypePosition



    #    *
    #     * return numercial's position in the rule
    #     * @param sAttribut
    #     * @return int
    #     
    def ObtenirTypePrisEnCompteAttribut(self, sAttribut):
        parametreItemDefaut = None
        parametreQuantDefaut = None
        bTypesTousPareils = False
        iTypePosition = 0
        sousTable = None
        enumItems = None

        # print(list(self.__m_tableParametresAttributsQuantitatifs.keys()))
        # print(len(list(self.__m_tableParametresAttributsQuantitatifs.keys())))
        # print(sAttribut in list(self.__m_tableParametresAttributsQuantitatifs.keys()))
        # print(sAttribut in list(self.__m_tableParametresItemsQualitatifs.keys()))
        # print(sAttribut)
        # print("&&&&&&&&&&&&")

        iTypePosition = ResolutionContext.PRISE_EN_COMPTE_ITEM_NULLE_PART

        if sAttribut in list(self.__m_tableParametresAttributsQuantitatifs.keys()):
            # Quantitative attribute:
            parametreQuantDefaut = (self.__m_tableParametresAttributsQuantitatifs[sAttribut])

        # print("len6: " + str(len(self.__m_tableParametresAttributsQuantitatifs)))
        if not parametreQuantDefaut == None:
            iTypePosition = parametreQuantDefaut.m_iTypePriseEnCompte

        # Qualitative attribute:
        else:
            sousTable = (self.__m_tableParametresItemsQualitatifs[sAttribut])
            if not sousTable == None:

                enumItems = list(sousTable.keys())
                if parametreItemDefaut in range(0, len(enumItems)):
                    parametreItemDefaut = sousTable[enumItems[i]]
                    bTypesTousPareils = True
                    iTypePosition = parametreItemDefaut.m_iTypePriseEnCompte
                    ii = i+1
                    while (bTypesTousPareils) and len(enumItems) > ii:
                        parametreItemDefaut = sousTable[enumItems[ii]]
                        bTypesTousPareils = (iTypePosition == parametreItemDefaut.m_iTypePriseEnCompte)

                    if not bTypesTousPareils:
                        iTypePosition = ResolutionContext.PRISE_EN_COMPTE_INDEFINI

        return iTypePosition




    def DefinirPresenceObligatoireItem(self, sAttribut, sItem, bPresenceObligatoire):
        sousTable = None
        parametres = None

        if (sAttribut == None) or (sItem == None):
            return

        sousTable = (self.__m_tableParametresItemsQualitatifs[sAttribut])
        if sousTable == None:
            return

        parametres = (sousTable[sItem])
        if parametres == None:
            return

        parametres.m_bPresenceObligatoire = bPresenceObligatoire



    def DefinirPresenceObligatoireAttribut(self, sAttribut, bPresenceObligatoire):
        parametreItemDefaut = None
        parametreQuantDefaut = None
        sousTable = None
        enumItems = None

        # Quantitative attribute:
        print("^^^^^^^^")
        print(self.__m_tableParametresAttributsQuantitatifs)
        # print("len7: " + str(len(self.__m_tableParametresAttributsQuantitatifs)))
        parametreQuantDefaut = (self.__m_tableParametresAttributsQuantitatifs[sAttribut])
        if not parametreQuantDefaut == None:
            parametreQuantDefaut.m_bPresenceObligatoire = bPresenceObligatoire

        # Qualitative attribute:
        else:
            sousTable = (self.__m_tableParametresItemsQualitatifs[sAttribut])
            if not sousTable == None:

                enumItems = sousTable.elements()
                if enumItems.hasMoreElements():

                    while enumItems.hasMoreElements():
                        parametreItemDefaut = enumItems.nextElement()
                        if ((not bPresenceObligatoire)) or not (parametreItemDefaut.m_iTypePriseEnCompte == ResolutionContext.PRISE_EN_COMPTE_ITEM_NULLE_PART):
                            parametreItemDefaut.m_bPresenceObligatoire = bPresenceObligatoire


    def ObtenirPresenceObligatoireItem(self, sAttribut, sItem):
        bPresenceObligatoire = False
        sousTable = None
        parametres = None

        if (sAttribut == None) or (sItem == None):
            return False

        sousTable = (self.__m_tableParametresItemsQualitatifs[sAttribut])
        if sousTable == None:
            return False

        parametres = (sousTable[sItem])
        if parametres == None:
            return False
        else:
            return parametres.m_bPresenceObligatoire


    #    *Whether present or not
    #     * @param sAttribut
    #     * @return 0 for False, 1 for True, -1 to indicate that all the values are not the same
    #     
    def ObtenirPresenceObligatoireAttribut(self, sAttribut):
        parametreItemDefaut = None
        parametreQuantDefaut = None
        bTypesTousPareils = False
        bPresenceObligatoire = False
        sousTable = None
        enumItems = None

        bTypesTousPareils = True
        bPresenceObligatoire = False

        # Quantitative attribute:
        parametreQuantDefaut = (self.__m_tableParametresAttributsQuantitatifs[sAttribut])
        # print("len8: " + str(len(self.__m_tableParametresAttributsQuantitatifs)))
        if not parametreQuantDefaut == None:
            bPresenceObligatoire = parametreQuantDefaut.m_bPresenceObligatoire


        # Qualitative attribute:
        else:
            sousTable = (self.__m_tableParametresItemsQualitatifs[sAttribut])
            if not sousTable == None:

                enumItems = sousTable.elements()
                if enumItems.hasMoreElements():

                    parametreItemDefaut = enumItems.nextElement()
                    bPresenceObligatoire = parametreItemDefaut.m_bPresenceObligatoire
                    while (bTypesTousPareils) and enumItems.hasMoreElements():
                        parametreItemDefaut = enumItems.nextElement()
                        bTypesTousPareils = (bPresenceObligatoire == parametreItemDefaut.m_bPresenceObligatoire)



        if not bTypesTousPareils:
            return -1
        elif bPresenceObligatoire:
            return 1
        else:
            return 0



    #    *
    #     * Build the data structures optimizing the filtering process
    #     
    def MettreAJourDonneesInternesFiltre(self):
        enumAttributs = None
        enumItems = None
        parametreQuant = None
        parametreQual = None
        sousTable = None
        sNomAttribut = None
        bFinEnumItems = False

        self.__m_tablePresenceObligatoire.clear()

        #Enumeration of mandatory quantitative attributes
        enumAttributs = list(self.__m_tableParametresAttributsQuantitatifs.keys())
        # print("len9: " + str(len(self.__m_tableParametresAttributsQuantitatifs)))
        # print(self.__m_tableParametresAttributsQuantitatifs)
        for sNomAttribut in enumAttributs:
            parametreQuant = self.__m_tableParametresAttributsQuantitatifs[sNomAttribut]
            if not parametreQuant == None: 
                if parametreQuant.m_bPresenceObligatoire and not (parametreQuant.m_iTypePriseEnCompte == ResolutionContext.PRISE_EN_COMPTE_ITEM_NULLE_PART):

                    self.__m_tablePresenceObligatoire.update({sNomAttribut: False})

        # Enumeration of mandatory qualitative attributes
        enumAttributs = list(self.__m_tableParametresItemsQualitatifs.keys())
        for sNomAttribut in enumAttributs:
            sousTable = self.__m_tableParametresItemsQualitatifs[sNomAttribut]
            if not sousTable == None:
                enumItems = list(sousTable.keys())
                bFinEnumItems = False

                # while ((not bFinEnumItems)) and (enumItems.hasMoreElements()):
                for e in enumItems:
                    parametreQual = sousTable[e]

                    if parametreQual.m_bPresenceObligatoire and not (parametreQual.m_iTypePriseEnCompte == ResolutionContext.PRISE_EN_COMPTE_ITEM_NULLE_PART):
                        self.__m_tablePresenceObligatoire.update({sNomAttribut: False})
                        bFinEnumItems = True
                        break
                        
    #    *
    #     * Reset the table of mandatory presence for a new presence test
    #     
    def __ReinitialiserTablePresenceObligatoire(self):
        enumAttributs = None
        sNomAttribut = None

        enumAttributs = list(self.__m_tablePresenceObligatoire.keys())
        for k in enumAttributs:
            # sNomAttribut = str(self.__m_tablePresenceObligatoire[k])
            sNomAttribut = k
            self.__m_tablePresenceObligatoire.update({sNomAttribut: False})
            # sys.exit()

    #    *
    #     * Validate all the quantitative attributes in case they are not taken into consideration
    #     
    def __ValiderAttributsQuantitatifs(self):
        iNombreColonnesPrisesEnCompte = 0
        iIndiceColonne = 0
        colonne = None
        sNomColonne = None

        if self.__m_contexteResolution.m_gestionnaireBD == None:
            return

        iNombreColonnesPrisesEnCompte = self.__m_contexteResolution.m_gestionnaireBD.ObtenirNombreColonnesPrisesEnCompte()
        iIndiceColonne = 0
        while iIndiceColonne<iNombreColonnesPrisesEnCompte:

            colonne = self.__m_contexteResolution.m_gestionnaireBD.ObtenirColonneBDPriseEnCompte(iIndiceColonne)
            sNomColonne = colonne.m_sNomColonne
            if not sNomColonne == None:
                if colonne.m_iTypeValeurs == DatabaseAdmin.TYPE_VALEURS_COLONNE_REEL:
                    if sNomColonne in self.__m_tablePresenceObligatoire.keys():
                        self.__m_tablePresenceObligatoire.update({sNomColonne: True})

            iIndiceColonne += 1



    #    *
    #     * Test wehther all the entries in the mandatory table are valid
    #     * @return boolean
    #     
    def __TesterValidationTablePresenceObligatoire(self):
        enumAttributs = None
        sNomAttribut = None
        bTableValidee = True

        enumAttributs = list(self.__m_tablePresenceObligatoire.keys())
        for k in enumAttributs:
            bTableValidee = bool(self.__m_tablePresenceObligatoire[k])

        return bTableValidee



    #    *
    #     * Indicate the presence of a mandatory attribute
    #     * @param sNomAttribut
    #     
    def __ValiderPresenceObligatoireAttribut(self, sNomAttribut):
        if sNomAttribut in self.__m_tablePresenceObligatoire.keys():
            self.__m_tablePresenceObligatoire.update({sNomAttribut: True})




    def DefinirPositionnementPourTous(self, iTypePosition, bPresenceObligatoire):
        iNombreColonnesPrisesEnCompte = 0
        iIndiceColonne = 0
        colonne = None
        sNomColonne = None


        if not self.__m_contexteResolution.m_gestionnaireBD == None:
            return

        iNombreColonnesPrisesEnCompte = self.__m_contexteResolution.m_gestionnaireBD.ObtenirNombreColonnesPrisesEnCompte()
        iIndiceColonne = 0
        while iIndiceColonne<iNombreColonnesPrisesEnCompte:

            colonne = self.__m_contexteResolution.m_gestionnaireBD.ObtenirColonneBDPriseEnCompte(iIndiceColonne)
            sNomColonne = colonne.m_sNomColonne

            if not sNomColonne == None:
                self.DefinirTypePrisEnCompteAttribut(sNomColonne, iTypePosition)
                self.DefinirPresenceObligatoireAttribut(sNomColonne, bPresenceObligatoire)
            iIndiceColonne += 1




    #    *
    #     * Check whether the filter allowing to position the attribite on the left or the right for the rule to generate
    #     
    def EstFiltreCoherent(self):
        enumItems = None
        parametreItem = None
        sousTable = None # subTable
        iNombreColonnesPrisesEnCompte = 0 # iNumberColumnsTakenInAccount
        iIndiceColonne = 0
        colonne = None
        sNomColonne = None
        iTypePosition = 0
        iNombreAttributsGauche = 0 # iNumberAttributesLeft
        iNombreAttributsDroite = 0 # iNumberAttributesRight
        iNombreAttributsTotal = 0 # iNumberAttributesTotal
        bItemAGauche = False # buildingLeft
        bItemADroite = False # buildingRight

        if self.__m_contexteResolution.m_gestionnaireBD == None:
            return False

        iNombreColonnesPrisesEnCompte = self.__m_contexteResolution.m_gestionnaireBD.ObtenirNombreColonnesPrisesEnCompte()

        iNombreAttributsGauche = 0
        iNombreAttributsDroite = 0
        iNombreAttributsTotal = 0
        iIndiceColonne=0
        while ((iNombreAttributsTotal<2) or (iNombreAttributsGauche<1) or (iNombreAttributsDroite<1)) and (iIndiceColonne<iNombreColonnesPrisesEnCompte):

            colonne = self.__m_contexteResolution.m_gestionnaireBD.ObtenirColonneBDPriseEnCompte(iIndiceColonne)
            sNomColonne = colonne.m_sNomColonne

            if not sNomColonne == None:
                # Attributs quantitatifs :
                if colonne.m_iTypeValeurs == DatabaseAdmin.TYPE_VALEURS_COLONNE_REEL:

                    iTypePosition = self.ObtenirTypePrisEnCompteAttribut(sNomColonne)
                    if (iTypePosition==ResolutionContext.PRISE_EN_COMPTE_ITEM_GAUCHE) or (iTypePosition==ResolutionContext.PRISE_EN_COMPTE_ITEM_2_COTES):
                        iNombreAttributsGauche += 1
                    if (iTypePosition==ResolutionContext.PRISE_EN_COMPTE_ITEM_DROITE) or (iTypePosition==ResolutionContext.PRISE_EN_COMPTE_ITEM_2_COTES):
                        iNombreAttributsDroite += 1
                    if (iTypePosition==ResolutionContext.PRISE_EN_COMPTE_ITEM_GAUCHE) or (iTypePosition==ResolutionContext.PRISE_EN_COMPTE_ITEM_DROITE) or (iTypePosition==ResolutionContext.PRISE_EN_COMPTE_ITEM_2_COTES):
                        iNombreAttributsTotal += 1


                # Attributs qualitatifs :
                elif colonne.m_iTypeValeurs == DatabaseAdmin.TYPE_VALEURS_COLONNE_ITEM:
                    sousTable = (self.__m_tableParametresItemsQualitatifs[sNomColonne])

                    if not sousTable == None:
                        enumItems = list(sousTable.keys())

                        bItemAGauche = False
                        bItemADroite = False

                        i = 0
                        while (not(bItemAGauche and bItemADroite)) and i < len(enumItems):
                            parametreItem = sousTable[enumItems[i]]
                            iTypePosition = parametreItem.m_iTypePriseEnCompte

                            if (iTypePosition==ResolutionContext.PRISE_EN_COMPTE_ITEM_GAUCHE) or (iTypePosition==ResolutionContext.PRISE_EN_COMPTE_ITEM_2_COTES):
                                bItemAGauche = True
                            if (iTypePosition==ResolutionContext.PRISE_EN_COMPTE_ITEM_DROITE) or (iTypePosition==ResolutionContext.PRISE_EN_COMPTE_ITEM_2_COTES):
                                bItemADroite = True

                            i += 1

                    if bItemAGauche:
                        iNombreAttributsGauche += 1
                    if bItemADroite:
                        iNombreAttributsDroite += 1
                    if bItemAGauche or bItemADroite:
                        iNombreAttributsTotal += 1

            iIndiceColonne += 1

        return ((iNombreAttributsTotal>=2) and (iNombreAttributsGauche>0) and (iNombreAttributsDroite>0))

    #    *
    #     * Test whether an itemset fulfills the user filtering criteria
    #     * @param itemSet
    #     * @return boolean
    #     
    def EstItemSetValide(self, itemSet):
        iIndiceItem = 0
        item = None
        bItemSetValide = False
        sNomAttribut = None
        sNomItem = None

        bItemSetValide = True

        # We re-initialise the counting table for mandatory attributes for this itemset,
        # then we validatr all the quantitative attributes since an itemset is purely qualitative:
        self.__ReinitialiserTablePresenceObligatoire()
        self.__ValiderAttributsQuantitatifs()

        iIndiceItem = 0
        item = itemSet.ObtenirItem(0)
        while not item == None:

            sNomAttribut = item.m_attributQual.ObtenirNom()
            sNomItem = item.ObtenirIdentifiantTexteItem()

            bItemSetValide = not (self.ObtenirTypePrisEnCompteItem(sNomAttribut, sNomItem) == ResolutionContext.PRISE_EN_COMPTE_ITEM_NULLE_PART)

            if bItemSetValide:
                if self.ObtenirPresenceObligatoireItem(sNomAttribut, sNomItem):
                    self.__ValiderPresenceObligatoireAttribut(sNomAttribut)

                iIndiceItem += 1
                item = itemSet.ObtenirItem(iIndiceItem)

        if bItemSetValide:
            bItemSetValide = self.__TesterValidationTablePresenceObligatoire()

        return bItemSetValide





    #    *
    #     * Test whether a rule fulfills the user filtering criteria
    #     * @param regle # rule
    #     * @return boolean
    #     
    def EstRegleValide(self, regle):
        item = None
        itemQual = None
        itemQuant = None
        parametreItemDefaut = None
        parametreQuantDefaut = None
        sNomAttribut = None
        iIndiceItem = 0
        iTypePosition = 0
        iEtapeTestRegle = 0
        iNombreItems = 0
        iTypeTestEtape = 0

        if regle == None:
            return False

        bRegleValide = True

        # We reset the counting table of mandatory attributes for this rule:
        self.__ReinitialiserTablePresenceObligatoire()
        # self.__ValiderAttributsQuantitatifs()

        # 2-step test: first on the left and then on the right
        iEtapeTestRegle=0
        while bRegleValide and (iEtapeTestRegle<2):
            if iEtapeTestRegle==0:
                iNombreItems = regle.m_iNombreItemsGauche
                iTypeTestEtape = ResolutionContext.PRISE_EN_COMPTE_ITEM_GAUCHE
            else:
                iNombreItems = regle.m_iNombreItemsDroite
                iTypeTestEtape = ResolutionContext.PRISE_EN_COMPTE_ITEM_DROITE

            iIndiceItem=0
            while (bRegleValide) and (iIndiceItem<iNombreItems):
                if iEtapeTestRegle==0:
                    item = regle.ObtenirItemGauche(iIndiceItem)
                else:
                    item = regle.ObtenirItemDroite(iIndiceItem)

                if item == None:
                    bRegleValide = False
                else:
                    iTypePosition = ResolutionContext.PRISE_EN_COMPTE_INDEFINI

                    if item.m_iTypeItem == Item.ITEM_TYPE_QUANTITATIF:
                        itemQuant = item
                        sNomAttribut = itemQuant.m_attributQuant.ObtenirNom()
                        iTypePosition = self.ObtenirTypePrisEnCompteAttribut(sNomAttribut)
                        if self.ObtenirPresenceObligatoireAttribut(sNomAttribut) == 1:
                            self.__ValiderPresenceObligatoireAttribut(sNomAttribut)
                    elif item.m_iTypeItem == Item.ITEM_TYPE_QUALITATIF:
                        itemQual = item
                        sNomAttribut = itemQual.m_attributQual.ObtenirNom()
                        iTypePosition = self.ObtenirTypePrisEnCompteItem(sNomAttribut, itemQual.ObtenirIdentifiantTexteItem())
                        if self.ObtenirPresenceObligatoireItem(sNomAttribut, itemQual.ObtenirIdentifiantTexteItem()):
                            self.__ValiderPresenceObligatoireAttribut(sNomAttribut)

                    
                    bRegleValide = (iTypePosition == iTypeTestEtape) or (iTypePosition == ResolutionContext.PRISE_EN_COMPTE_ITEM_2_COTES)
                    

                    iIndiceItem += 1

            iEtapeTestRegle += 1


        if bRegleValide:
            bRegleValide = self.__TesterValidationTablePresenceObligatoire()
            # print(bRegleValide)

        return bRegleValide

#                                             
# *Copyright 2007, 2011 CCLS Columbia University (USA), LIFO University of Orleans (France), BRGM (France)
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
sys.path.append('C:\\Users\\aalsahee\\python_physical_model\\Saudi\\trace\\Traces\\qtm\\src\\')

# from apriori import *
# from database import *
# from geneticAlgorithm import *
from graphicalInterface import *
from simulatedAnnealing import *
from tools import *
# from apriori.StandardParameters import StandardParameters
# from apriori.StandardParametersQuantitative import StandardParametersQuantitative
from geneticAlgorithm.ParametersGeneticAlgo import ParametersGeneticAlgo
from simulatedAnnealing.SimulatedAnnealingParameters import SimulatedAnnealingParameters
# from solver.LoadingParameters import LoadingParameters
# from solver.PositionRuleParameters import PositionRuleParameters
import csv


# Class allowing to remember a set of parameters to use all over the process:
class ResolutionContext(object):
    # Identification of possible techniques of quantitative extraction rules:
    TECHNIQUE_INDEFINIE = 0 #undefined technique
    TECHNIQUE_APRIORI_QUAL = 1 #Apriori algorithm
    TECHNIQUE_ALGO_GENETIQUE = 2 #Generic algorithm
    TECHNIQUE_RECUIT_SIMULE = 3 #simulated annealing algorithm
    TECHNIQUE_CHARGEMENT = 4 #load rule file
    
    # Indicate the position of each item in the association rule:
    PRISE_EN_COMPTE_INDEFINI = 0 #undefined
    PRISE_EN_COMPTE_ITEM_NULLE_PART = 1 #no where
    PRISE_EN_COMPTE_ITEM_GAUCHE = 2 #left side
    PRISE_EN_COMPTE_ITEM_DROITE = 3 #right side
    PRISE_EN_COMPTE_ITEM_2_COTES = 4 #two sides
    
    # These parameter has something to do with profile
    PROFIL_INFO_PRECHARGEMENT = 1
    PROFIL_INFO_PREEXTRACTION = 2
    PROFIL_INFO_ALGO_APRIORI = 4
    PROFIL_INFO_ALGO_GENETIQUE = 8
    PROFIL_INFO_ALGO_RECUIT = 16
    PROFIL_INFO_ALGO_CHARGEMENT = 32
    
    # constant values used to write the profile files
    __FICHIER_PROFIL_DONNEES_AUCUNES = 0
    __FICHIER_PROFIL_DONNEES_PRECHARGE = 1
    __FICHIER_PROFIL_DONNEES_PREEXTRACTION = 2
    __FICHIER_PROFIL_DONNEES_ALGO_APRIORI = 3
    __FICHIER_PROFIL_DONNEES_ALGO_GENETIQUE = 4
    __FICHIER_PROFIL_DONNEES_ALGO_RECUIT = 5
    __FICHIER_PROFIL_DONNEES_ALGO_CHARGEMENT = 6
    
    __FICHIER_PROFIL_CHAMP_TYPE_QUAL = 1
    __FICHIER_PROFIL_CHAMP_TYPE_QUANT = 2

    # Class to implement the graphical recording of a rule in a file: 
    class EnregistreurGraphiqueRegle(object):
        # Function that create a JPEG picture of the rule and send back the name of the file on disc:
        def EnregistrerRegle(self, regle, iIndiceRegle):
            pass



    #Following two will be in profile file



    # Objects defining user parameters for each extraction technique:
    # ... Add here other objects for each new technique

    def __init__(self, fenetreProprietaire):
        self.__m_positionnementRegles = None
        self.__m_filtrageRegles = None
        self.m_sNomUtilisateur = None
        self.m_sDescriptionRegles = None
        self.m_fenetreProprietaire = None
        self.m_gestionnaireBD = None
        self.m_iTechniqueResolution = 0
        self.m_listeRegles = None
        self.m_parametresRegles = None
        self.m_parametresReglesQuantitatives = None
        self.m_parametresTechAlgoGenetique = None
        self.m_parametresTechRecuitSimule = None
        self.m_parametresTechChargement = None
        self.m_aprioriCourant = None


        self.m_sNomUtilisateur = "ENV.NOM_UTILISATEUR" #user name
        self.m_sDescriptionRegles = "No description." #description

        self.m_fenetreProprietaire = fenetreProprietaire
        self.m_gestionnaireBD = None
        self.m_iTechniqueResolution = self.TECHNIQUE_APRIORI_QUAL
        self.m_listeRegles = None

        self.m_parametresRegles = StandardParameters()
        self.m_parametresReglesQuantitatives = StandardParametersQuantitative()
        self.m_parametresTechAlgoGenetique = ParametersGeneticAlgo()
        self.m_parametresTechRecuitSimule = SimulatedAnnealingParameters()
        self.m_parametresTechChargement = LoadingParameters()

        self.__m_positionnementRegles = PositionRuleParameters(self, PositionRuleParameters.PARAMETRES_POSITION_REGLES)
        self.__m_filtrageRegles = PositionRuleParameters(self, PositionRuleParameters.PARAMETRES_FILTRAGE_REGLES)

        self.m_aprioriCourant = None

    # Methods to directly access to the positionning parameters of the attributes in the rules
    def GenererStructuresDonneesSelonBDPriseEnCompte(self):
        self.__m_positionnementRegles.GenererStructuresDonneesSelonBDPriseEnCompte()
    def DefinirTypePrisEnCompteItem(self, sAttribut, sItem, iTypePosition):
        self.__m_positionnementRegles.DefinirTypePrisEnCompteItem(sAttribut, sItem, iTypePosition)
    def ObtenirTypePrisEnCompteItem(self, sAttribut, sItem):
        return self.__m_positionnementRegles.ObtenirTypePrisEnCompteItem(sAttribut, sItem)
    def DefinirTypePrisEnCompteAttribut(self, sAttribut, iTypePosition):
        self.__m_positionnementRegles.DefinirTypePrisEnCompteAttribut(sAttribut, iTypePosition)
    def ObtenirTypePrisEnCompteAttribut(self, sAttribut):
        return self.__m_positionnementRegles.ObtenirTypePrisEnCompteAttribut(sAttribut)
    def DefinirPresenceObligatoireItem(self, sAttribut, sItem, bPresenceObligatoire):
        self.__m_positionnementRegles.DefinirPresenceObligatoireItem(sAttribut, sItem, bPresenceObligatoire)
    def DefinirPresenceObligatoireAttribut(self, sAttribut, bPresenceObligatoire):
        self.__m_positionnementRegles.DefinirPresenceObligatoireAttribut(sAttribut, bPresenceObligatoire)
    def ObtenirPresenceObligatoireItem(self, sAttribut, sItem):
        return self.__m_positionnementRegles.ObtenirPresenceObligatoireItem(sAttribut, sItem)
    def ObtenirPresenceObligatoireAttribut(self, sAttribut):
        return self.__m_positionnementRegles.ObtenirPresenceObligatoireAttribut(sAttribut)
    def MettreAJourDonneesInternesFiltre(self):
        self.__m_positionnementRegles.MettreAJourDonneesInternesFiltre()
    def DefinirPositionnementPourTous(self, iTypePosition, bPresenceObligatoire):
        self.__m_positionnementRegles.DefinirPositionnementPourTous(iTypePosition, bPresenceObligatoire)
    def EstFiltreCoherent(self):
        return self.__m_positionnementRegles.EstFiltreCoherent()
    def EstItemSetValide(self, itemSet):
        return self.__m_positionnementRegles.EstItemSetValide(itemSet)
    def EstRegleValide(self, regle):
        return self.__m_positionnementRegles.EstRegleValide(regle)


    # Methods to directly access to the filtering of the attributes in the rules:
    def GenererStructuresDonneesSelonBDPriseEnCompte_Filtrage(self):
        self.__m_filtrageRegles.GenererStructuresDonneesSelonBDPriseEnCompte()
    def DefinirTypePrisEnCompteItem_Filtrage(self, sAttribut, sItem, iTypePosition):
        self.__m_filtrageRegles.DefinirTypePrisEnCompteItem(sAttribut, sItem, iTypePosition)
    def ObtenirTypePrisEnCompteItem_Filtrage(self, sAttribut, sItem):
        return self.__m_filtrageRegles.ObtenirTypePrisEnCompteItem(sAttribut, sItem)
    def DefinirTypePrisEnCompteAttribut_Filtrage(self, sAttribut, iTypePosition):
        self.__m_filtrageRegles.DefinirTypePrisEnCompteAttribut(sAttribut, iTypePosition)
    def ObtenirTypePrisEnCompteAttribut_Filtrage(self, sAttribut):
        return self.__m_filtrageRegles.ObtenirTypePrisEnCompteAttribut(sAttribut)
    def DefinirPresenceObligatoireItem_Filtrage(self, sAttribut, sItem, bPresenceObligatoire):
        self.__m_filtrageRegles.DefinirPresenceObligatoireItem(sAttribut, sItem, bPresenceObligatoire)
    def DefinirPresenceObligatoireAttribut_Filtrage(self, sAttribut, bPresenceObligatoire):
        self.__m_filtrageRegles.DefinirPresenceObligatoireAttribut(sAttribut, bPresenceObligatoire)
    def ObtenirPresenceObligatoireItem_Filtrage(self, sAttribut, sItem):
        return self.__m_filtrageRegles.ObtenirPresenceObligatoireItem(sAttribut, sItem)
    def ObtenirPresenceObligatoireAttribut_Filtrage(self, sAttribut):
        return self.__m_filtrageRegles.ObtenirPresenceObligatoireAttribut(sAttribut)
    def MettreAJourDonneesInternesFiltre_Filtrage(self):
        self.__m_filtrageRegles.MettreAJourDonneesInternesFiltre()
    def DefinirPositionnementPourTous_Filtrage(self, iTypePosition, bPresenceObligatoire):
        self.__m_filtrageRegles.DefinirPositionnementPourTous(iTypePosition, bPresenceObligatoire)
    def EstFiltreCoherent_Filtrage(self):
        return self.__m_filtrageRegles.EstFiltreCoherent()
    def EstItemSetValide_Filtrage(self, itemSet):
        return self.__m_filtrageRegles.EstItemSetValide(itemSet)
    def EstRegleValide_Filtrage(self, regle):
        return self.__m_filtrageRegles.EstRegleValide(regle)

    # Assessors for the positionning information
    def ObtenirInfosPostionnementRegles(self):
        return self.__m_positionnementRegles
    def ObtenirInfosPostionnementFiltrage(self):
        return self.__m_filtrageRegles

    def ObtenirInfosContexte(self, bAjouterTagsHTML):
        sInfoContexte = None
        iNombreColonnesPrisesEnCompte = 0
        iIndiceColonne = 0
        colonne = None
        attributQual = None
        attributQuant = None

        sInfoContexte = ""

        if (self.m_aprioriCourant == None) or (self.m_gestionnaireBD == None):
            return sInfoContexte

        # If the rules come from a file, we send the general context:
        if self.m_iTechniqueResolution == ResolutionContext.TECHNIQUE_CHARGEMENT:
            return self.m_parametresTechChargement.toString()


        if bAjouterTagsHTML:
            sInfoContexte += "<a name=\"conftech\"><big><u><b>"
        sInfoContexte += "Parameters :"
        if bAjouterTagsHTML:
            sInfoContexte += "</b></u></big></a>"
        sInfoContexte += "\n\n\n"

        # summarization of the parameters:
        if bAjouterTagsHTML:
            sInfoContexte += "<i>"
        sInfoContexte += "Method : "
        if bAjouterTagsHTML:
            sInfoContexte += "</i><b>"

        if self.m_iTechniqueResolution == ResolutionContext.TECHNIQUE_APRIORI_QUAL:
            sInfoContexte += "Apriori algorithm (categorical)\n\n\n"
            if bAjouterTagsHTML:
                sInfoContexte += "</b>"
            sInfoContexte += self.m_parametresRegles.toString() + "\n\n"

        elif self.m_iTechniqueResolution == ResolutionContext.TECHNIQUE_ALGO_GENETIQUE:
            sInfoContexte += "genetic algorithm\n\n\n"
            if bAjouterTagsHTML:
                sInfoContexte += "</b>"
            sInfoContexte += self.m_parametresReglesQuantitatives.toString() + "\n\n"
            sInfoContexte += self.m_parametresTechAlgoGenetique.toString() + "\n\n"

        elif self.m_iTechniqueResolution == ResolutionContext.TECHNIQUE_RECUIT_SIMULE:
            sInfoContexte += "simulated annealing\n\n\n"
            if bAjouterTagsHTML:
                sInfoContexte += "</b>"
            sInfoContexte += self.m_parametresReglesQuantitatives.toString() + "\n\n"
            sInfoContexte += self.m_parametresTechRecuitSimule.toString() + "\n\n"

        else:
            if bAjouterTagsHTML:
                sInfoContexte += "</b>"
        sInfoContexte += "\n\n\n"

        if bAjouterTagsHTML:
            sInfoContexte += "<a name=\"recapattr\"><big><u><b>"
        sInfoContexte += "Summary of the attributes used in mining rules:"
        if bAjouterTagsHTML:
            sInfoContexte += "</b></u></big></a>"
        sInfoContexte += "\n\n\n"

        iNombreColonnesPrisesEnCompte = self.m_gestionnaireBD.ObtenirNombreColonnesPrisesEnCompte()

        if bAjouterTagsHTML:
            sInfoContexte += "<b>"
        sInfoContexte += "Qualitative attributes :"
        if bAjouterTagsHTML:
            sInfoContexte += "</b>"
        sInfoContexte += "\n\n"

        iIndiceColonne = 0
        while iIndiceColonne<iNombreColonnesPrisesEnCompte:
            colonne = self.m_gestionnaireBD.ObtenirColonneBDPriseEnCompte(iIndiceColonne)
            if not colonne == None:
                if (not colonne.m_sNomColonne == None) and (colonne.m_iTypeValeurs == DatabaseAdmin.TYPE_VALEURS_COLONNE_ITEM):
                    # if not self.__m_positionnementRegles.ObtenirTypePrisEnCompteAttribut(colonne.m_sNomColonne) == ResolutionContext.PRISE_EN_COMPTE_ITEM_NULLE_PART:
                    attributQual = self.m_aprioriCourant.ObtenirAttributQualitatifDepuisNom(colonne.m_sNomColonne)
                    if not attributQual == None:
                        sInfoContexte += attributQual.ObtenirNom() + ", "
                    sInfoContexte += str(attributQual.m_colonneDonnees.ObtenirNombreValeursDifferentes()) + " values.\n"
            iIndiceColonne += 1
        sInfoContexte += "\n\n"


        if not self.m_iTechniqueResolution == ResolutionContext.TECHNIQUE_APRIORI_QUAL:
            if bAjouterTagsHTML:
                sInfoContexte += "<b>"
            sInfoContexte += "Quantitative attributes:"
            if bAjouterTagsHTML:
                sInfoContexte += "</b>"
            sInfoContexte += "\n\n"

            iIndiceColonne = 0
            while iIndiceColonne<iNombreColonnesPrisesEnCompte:
                colonne = self.m_gestionnaireBD.ObtenirColonneBDPriseEnCompte(iIndiceColonne)
                if not colonne == None:
                    if (not colonne.m_sNomColonne == None) and (colonne.m_iTypeValeurs == DatabaseAdmin.TYPE_VALEURS_COLONNE_REEL):
                        if not self.__m_positionnementRegles.ObtenirTypePrisEnCompteAttribut(colonne.m_sNomColonne) == ResolutionContext.PRISE_EN_COMPTE_ITEM_NULLE_PART:
                            attributQuant = self.m_aprioriCourant.ObtenirAttributQuantitatifDepuisNom(colonne.m_sNomColonne)
                            if not attributQuant == None:
                                sInfoContexte += attributQuant.ObtenirNom() + ", domain "
                            sInfoContexte += "[ " + str(colonne.ObtenirBorneMin())
                            sInfoContexte += ", " + str(colonne.ObtenirBorneMax()) + "].\n"
                iIndiceColonne += 1
            sInfoContexte += "\n\n"

        sInfoContexte += "\n\n\n"


        if bAjouterTagsHTML:
            sInfoContexte += "<a name=\"lstfreq\"><big><u><b>"
        sInfoContexte += "Frequent itemsets:"
        if bAjouterTagsHTML:
            sInfoContexte += "</b></u></big></a>"
        sInfoContexte += "\n\n\n"

        sInfoContexte += self.m_aprioriCourant.EcrireListeFrequents()
        sInfoContexte += "\n\n\n\n\n"

        if bAjouterTagsHTML:
            sInfoContexte = FormateHTML(sInfoContexte)

        return sInfoContexte


    # (replace the carriages "\n" with the tag <BR>):
    @staticmethod
    def FormateHTML(sChaineInitiale):
        if sChaineInitiale == None:
            return None

        return sChaineInitiale.replaceAll("\n", "<BR>")

    def SauvegarderReglesCsv(self, sCheminFichier, tRegles):
        iNombreRegles = 0
        iIndiceRegle = 0
        iNombreLignesBD = 0
        fValeurConfiance = 0.0
        regle = None
        csvPrinter = None

        print(sCheminFichier)
        try:
            csvPrinter = csv.writer(open(sCheminFichier))
        except Exception as e:
            print(e)
            return

        if not tRegles == None:
            iNombreRegles = len(tRegles)
            print(iNombreRegles)
        else:
            iNombreRegles = 0

        #output the attributes
        attribute = ["Left", "Right", "Frequency[L and R]", "Support[L and R]", "Confidence[L->R]", "Confidence[(~L)->R]", "Confidence[R->L]", "Confidence[(~R)->L]", "Confidence[L<->R]"]
        try:
            csvPrinter.writerow(attribute)

            iNombreLignesBD = self.m_gestionnaireBD.ObtenirNombreLignes()
            iIndiceRegle = 0
            while iIndiceRegle < iNombreRegles:
                regle = tRegles[iIndiceRegle]
                csvPrinter.writerow(regle.leftToString())
                csvPrinter.writerow(regle.rightToString())
                csvPrinter.writerow(str(regle.m_iOccurrences))
                csvPrinter.writerow(EcrirePourcentage(regle.m_fSupport, 2, True))
                csvPrinter.writerow(EcrirePourcentage(regle.m_fConfiance, 2, True))

                if (iNombreLignesBD - regle.m_iOccurrencesGauche) > 0:
                    fValeurConfiance = (float(regle.m_iOccurrences_NonGauche_Droite)) / (float((iNombreLignesBD - regle.m_iOccurrencesGauche)))
                    csvPrinter.writerow(EcrirePourcentage(fValeurConfiance, 2, True))
                else:
                    csvPrinter.writerow("no non-left")

                fValeurConfiance = (float(regle.m_iOccurrences)) / (float(regle.m_iOccurrencesDroite))
                csvPrinter.writerow(EcrirePourcentage(fValeurConfiance, 2, True))

                if (iNombreLignesBD - regle.m_iOccurrencesDroite) > 0:
                    fValeurConfiance = (float(regle.m_iOccurrences_Gauche_NonDroite)) / (float((iNombreLignesBD - regle.m_iOccurrencesDroite)))
                    csvPrinter.writerow(EcrirePourcentage(fValeurConfiance, 2, True))
                else:
                    csvPrinter.writerow("no non-left")

                fValeurConfiance = (float((regle.m_iOccurrences + regle.m_iOccurrences_NonGauche_NonDroite))) / (float(iNombreLignesBD))
                csvPrinter.writerow(EcrirePourcentage(fValeurConfiance, 2, True))
                iIndiceRegle += 1
        except Exception as e:
            print(e)
        try:
            csvPrinter.close()
        except Exception as e:
            print(e)

    #save rules in HTML file (text and graphic)
    def SauvegarderReglesHTML(self, sCheminFichier, tRegles, bGraphique, enregistreurGraphique):
        fluxFichier = None
        iNombreRegles = 0
        iIndiceRegle = 0
        regle = None
        tNomsFichiersGraphiques = None

        try:
            fluxFichier = DataOutputStream(FileOutputStream(sCheminFichier))
        except Exception as e:
            print(e)
            return

        try:
            fluxFichier.writeChars("<HTML>")
            fluxFichier.writeChars("<HEAD>")
            fluxFichier.writeChars("<TITLE>" + "Rules extraction- Results" + "</TITLE>")
            fluxFichier.writeChars("</HEAD>")
            fluxFichier.writeChars("<BODY>")
        except Exception as e:
            pass

        # Ecriture du titre, quelques infos et du sommaire :
        try:
            fluxFichier.writeChars("<BR><p align=\"center\"><big><big><big><b>ASSOCIATION RULES ANALYSIS</b></big></big></big></p>")
            fluxFichier.writeChars("<BR><BR><BR>")

            fluxFichier.writeChars("<i><BR>Software: </i><b>QuantMiner version "+"ENV.VERSION_QUANTMINER"+"</b><BR>")
            fluxFichier.writeChars("<i>Date: </i><b>"+ "ENV.ObtenirDateCourante()" +"</b><BR>")
            fluxFichier.writeChars("<i>Database: </i><b>"+ self.m_gestionnaireBD.ObtenirNomBaseDeDonnees() +"</b><BR>")
            fluxFichier.writeChars("<i>Author: </i><b>"+ self.m_sNomUtilisateur +"</b><BR>")

            fluxFichier.writeChars("<BR><BR><BR><BR><p align=\"center\">")
            fluxFichier.writeChars("<a href=\"#conftech\">Parameters</a><BR><BR>")
            if not self.m_iTechniqueResolution == ResolutionContext.TECHNIQUE_CHARGEMENT:
                fluxFichier.writeChars("<a href=\"#recapattr\">Attributes used</a><BR><BR>")
                fluxFichier.writeChars("<a href=\"#lstfreq\">List of frequent itemsets</a><BR><BR>")
            fluxFichier.writeChars("<a href=\"#lstregles\">Extracted Rules List</a><BR><BR>")
            fluxFichier.writeChars("</p><BR><BR><BR><BR><BR><BR>")
        except Exception as e:
            pass

        try:
            fluxFichier.writeChars(self.ObtenirInfosContexte(True))
        except Exception as e:
            pass

        # write the rule list
        try:
            fluxFichier.writeChars("<a name=\"lstregles\"><big><u><b>List of Rules:</b></u></big></a><BR><BR><BR>")
        except Exception as e:
            pass

        if not tRegles == None:
            iNombreRegles = len(tRegles)
            tNomsFichiersGraphiques = [None for _ in range(iNombreRegles)]
        else:
            iNombreRegles = 0
            tNomsFichiersGraphiques = None

        iIndiceRegle = 0
        while iIndiceRegle < iNombreRegles:
            regle = tRegles[iIndiceRegle]
            tNomsFichiersGraphiques[iIndiceRegle] = None

            try:
                if bGraphique and (not enregistreurGraphique == None):
                    tNomsFichiersGraphiques[iIndiceRegle] = enregistreurGraphique.EnregistrerRegle(regle, iIndiceRegle)

                if not tNomsFichiersGraphiques[iIndiceRegle] == None:
                    fluxFichier.writeChars("<a href=\"#" + str(iIndiceRegle) + "\">")

                fluxFichier.writeChars(regle.toString())

                if not tNomsFichiersGraphiques[iIndiceRegle] == None:
                    fluxFichier.writeChars("</a>")

                fluxFichier.writeChars("<BR><BR>")
            except Exception as e:
                pass
            iIndiceRegle += 1


        # Browsing the lists or rules images: 
        if bGraphique and (not enregistreurGraphique == None):

            try:
                fluxFichier.writeChars("<BR><BR>")
            except Exception as e:
                pass

            iIndiceRegle = 0
            while iIndiceRegle<iNombreRegles:
                regle = tRegles[iIndiceRegle]
                if not tNomsFichiersGraphiques[iIndiceRegle] == None:
                    try:
                        fluxFichier.writeChars("<BR><BR><hr width=\"40%\" size=\"4\" align=\"center\"><BR>")
                        fluxFichier.writeChars("<a name=\"" + str(iIndiceRegle) + "\"><BR></a><BR>")
                        fluxFichier.writeChars("<p align=\"center\"><img src=\"" + tNomsFichiersGraphiques[iIndiceRegle] + "\"><BR><p><BR>")

                    except Exception as e:
                        pass
                iIndiceRegle += 1



        try:
            fluxFichier.writeChars("<BR><BR><BR><BR><BR><BR><BR><BR><BR>")
        except Exception as e:
            pass


        # Cloture du fichier HTML :
        # Closing the HTML file:
        try:
            fluxFichier.writeChars("</BODY>")
            fluxFichier.writeChars("</HTML>")
        except Exception as e:
            pass


        try:
            fluxFichier.close()
        except Exception as e:
            pass


    #    *Saving a profile
    #     * @param sCheminFichier File name
    #     * @param iInfosSelectionnees
    #     

    def SauvegarderProfil(self, sCheminFichier, iInfosSelectionnees):
        fluxFichier = None
        iNombreChamps = 0
        iIndiceChamp = 0
        sNomChamp = None
        iNombreAttributsPrisEnCompte = 0
        iIndiceAttribut = 0
        colonneDonnees = None
        sNomAttribut = None
        tItems = None
        iIndiceItem = 0

        if self.m_gestionnaireBD == None:
            return

        try:
            fluxFichier = DataOutputStream(FileOutputStream(sCheminFichier))
        except Exception as e:
            print(e)
            return


        try:
            fluxFichier.writeUTF("PROFIL01.00") # Identification
            fluxFichier.writeUTF(self.m_gestionnaireBD.ObtenirNomBaseDeDonnees()) # name of the data file for that profile!!!
            print(self.m_gestionnaireBD.ObtenirNomBaseDeDonnees())
        except Exception as e:
            pass


        # Informations about pre-load the information about that BD :
        if not (iInfosSelectionnees & PROFIL_INFO_PRECHARGEMENT) == 0:
            try:
                fluxFichier.writeByte(__FICHIER_PROFIL_DONNEES_PRECHARGE) # Identification !!!  1
            except Exception as e:
                pass


            # For every column de la BD, indicate son type et s'il est pris en compte :
            iNombreChamps = self.m_gestionnaireBD.ObtenirNombreColonnesBDInitiale() #obtain the number of columns in the data file

            # Ecriture du nombre de champs :
            # Writing the number of fields:
            try:
                fluxFichier.writeInt(iNombreChamps) #Number of columns in that data file!!!
            except Exception as e:
                pass

            if iNombreChamps > 0:

                iIndiceChamp = 0
                while iIndiceChamp < iNombreChamps:
                    sNomChamp = self.m_gestionnaireBD.ObtenirNomColonneBDInitiale(iIndiceChamp) #name of the columns in that data file

                    try:
                        # Write the name of that column:
                        fluxFichier.writeUTF(sNomChamp) #name of the columns in that data file!!!

                        # Write the type of that column:
                        if self.m_gestionnaireBD.ObtenirTypeColonne(sNomChamp) == DatabaseAdmin.TYPE_VALEURS_COLONNE_REEL:
                            fluxFichier.writeByte(__FICHIER_PROFIL_CHAMP_TYPE_QUANT) #column type!!!
                        else:
                            fluxFichier.writeByte(__FICHIER_PROFIL_CHAMP_TYPE_QUAL) #column type!!!

                        # Write value (0 or 1) indicating if that column has been selected during computation:
                        if self.m_gestionnaireBD.EstPriseEnCompteColonne(sNomChamp): #Not checked in Step 1
                            fluxFichier.writeByte(1) #selected during computation
                        else:
                            fluxFichier.writeByte(0) #no selected during computation
                    except Exception as e:
                        pass

                    iIndiceChamp += 1

        # Information about pre-extraction from information of that BD:
        if not (iInfosSelectionnees & PROFIL_INFO_PREEXTRACTION) == 0:

            try:
                fluxFichier.writeByte(__FICHIER_PROFIL_DONNEES_PREEXTRACTION) # Identification!!! 2
            except Exception as e:
                pass

            iNombreAttributsPrisEnCompte = self.m_gestionnaireBD.ObtenirNombreColonnesPrisesEnCompte() #Checked in Step 1

            # Ecriture du nombre d'attributs pris en compte pour l'extraction des r�gles :
            # Writing the number of attributes taking into consideration for rule extraction: 
            try:
                #Writes an int to the underlying output stream as four bytes, high byte first
                fluxFichier.writeInt(iNombreAttributsPrisEnCompte) #Number of item checked in Step 1
            except Exception as e:
                pass

            iIndiceAttribut = 0
            while iIndiceAttribut < iNombreAttributsPrisEnCompte:

                try:

                    colonneDonnees = self.m_gestionnaireBD.ObtenirColonneBDPriseEnCompte(iIndiceAttribut)
                    if not colonneDonnees == None:

                        sNomAttribut = str(colonneDonnees.m_sNomColonne)

                        fluxFichier.writeUTF(sNomAttribut)

                        # Write in the profile if the column type is categorical
                        if self.m_gestionnaireBD.ObtenirTypeColonne(sNomAttribut) == DatabaseAdmin.TYPE_VALEURS_COLONNE_ITEM:
                            fluxFichier.writeByte(1) # Indicate que l'attribut est pas qualitatif, et so qu'il faut prendre en compte le positionnement de ses items -- indicate that the attribute id qualitative

                            tItems = colonneDonnees.ConstituerTableauValeurs()
                            fluxFichier.writeInt(len(tItems)) #Write the number of d'items pour l'attribut!!!

                            if not tItems == None:
                                iIndiceItem = 0
                                while iIndiceItem < len(tItems):
                                    fluxFichier.writeUTF(tItems[iIndiceItem])
                                    print("xixi " + tItems[iIndiceItem])
                                    fluxFichier.writeByte(self.ObtenirTypePrisEnCompteItem(sNomAttribut, tItems[iIndiceItem]))
                                    if self.ObtenirPresenceObligatoireItem(sNomAttribut, tItems[iIndiceItem]):
                                        fluxFichier.writeByte(1)
                                    else:
                                        fluxFichier.writeByte(0)
                                    iIndiceItem += 1
                        # Sinon on place un identificateur pour indiquer qu'il n'y a pas d'items qualitatifs,
                        # mais simplement le positionnement general de l'attribut quantitatif :
                        # otherwise we place an indicator that there is no qualitative items, but simply the general postionning of the quantitative attribute
                        else:
                            fluxFichier.writeByte(0) #Indique que l'attribut n'est pas qualitatif -- indicate that the attribute is not qualitative
                            fluxFichier.writeByte(self.ObtenirTypePrisEnCompteAttribut(sNomAttribut))
                            if self.ObtenirPresenceObligatoireAttribut(sNomAttribut) == 1:
                                fluxFichier.writeByte(1)
                            else:
                                fluxFichier.writeByte(0)

                except Exception as e:
                    pass

                iIndiceAttribut += 1


        # Parameter of algorithme APriori :
        if not (iInfosSelectionnees & PROFIL_INFO_ALGO_APRIORI) == 0:

            try:
                fluxFichier.writeByte(__FICHIER_PROFIL_DONNEES_ALGO_APRIORI)
            except Exception as e:
                pass

            try:
                # Memorisation de la techique de resolution courante : memorize the current technique
                fluxFichier.writeInt(self.m_iTechniqueResolution) #TECHNIQUE_APRIORI_QUAL
                # Parameters of that rule :
                fluxFichier.writeFloat(self.m_parametresRegles.m_fMinSupp) #min_support
                fluxFichier.writeFloat(self.m_parametresRegles.m_fMinConf) #min_confidence!
            except Exception as e:
                pass


        # Parameter of generic algorithm :
        if not (iInfosSelectionnees & PROFIL_INFO_ALGO_GENETIQUE) == 0:
            try:
                fluxFichier.writeByte(__FICHIER_PROFIL_DONNEES_ALGO_GENETIQUE)
            except Exception as e:
                pass

            try:
                # Memorisation de la techique de resolution courante : memorize the current technique
                fluxFichier.writeInt(self.m_iTechniqueResolution)

                # Parameters of that rule :
                fluxFichier.writeFloat(self.m_parametresReglesQuantitatives.m_fMinSupp)
                fluxFichier.writeFloat(self.m_parametresReglesQuantitatives.m_fMinConf)
                fluxFichier.writeInt(self.m_parametresReglesQuantitatives.m_iNombreDisjonctionsGauche) ## of OR on left side
                fluxFichier.writeInt(self.m_parametresReglesQuantitatives.m_iNombreDisjonctionsDroite) ## of OR on right side
                fluxFichier.writeInt(self.m_parametresReglesQuantitatives.m_iNombreMinAttributsQuant) #min # of numerical attri
                fluxFichier.writeInt(self.m_parametresReglesQuantitatives.m_iNombreMaxAttributsQuant) #max # of numerical attri in the rule
                fluxFichier.writeFloat(self.m_parametresReglesQuantitatives.m_fMinSuppDisjonctions) #support threshold for additional interval
                fluxFichier.writeFloat(self.m_parametresReglesQuantitatives.m_iNombreAssociationRules) # # of rules per association to use

                # Technique Parameter about generic algorithm:
                fluxFichier.writeInt(self.m_parametresTechAlgoGenetique.m_iTaillePopulation)
                fluxFichier.writeInt(self.m_parametresTechAlgoGenetique.m_iNombreGenerations)
                fluxFichier.writeFloat(self.m_parametresTechAlgoGenetique.m_fPourcentageCroisement)
                fluxFichier.writeFloat(self.m_parametresTechAlgoGenetique.m_fPourcentageMutation)
            except Exception as e:
                pass

        # Parameters about simulated annealing algorithm:
        if not (iInfosSelectionnees & PROFIL_INFO_ALGO_RECUIT) == 0:
            try:
                fluxFichier.writeByte(__FICHIER_PROFIL_DONNEES_ALGO_RECUIT)
            except Exception as e:
                pass

            try:
                # Memorisation de la techique de resolution courante : memorize the current technique
                fluxFichier.writeInt(self.m_iTechniqueResolution)

                # Parametres concernant les regles : Parameters of the rules:
                fluxFichier.writeFloat(self.m_parametresReglesQuantitatives.m_fMinSupp)
                fluxFichier.writeFloat(self.m_parametresReglesQuantitatives.m_fMinConf)
                fluxFichier.writeInt(self.m_parametresReglesQuantitatives.m_iNombreDisjonctionsGauche)
                fluxFichier.writeInt(self.m_parametresReglesQuantitatives.m_iNombreDisjonctionsDroite)
                fluxFichier.writeInt(self.m_parametresReglesQuantitatives.m_iNombreMinAttributsQuant)
                fluxFichier.writeInt(self.m_parametresReglesQuantitatives.m_iNombreMaxAttributsQuant)
                fluxFichier.writeFloat(self.m_parametresReglesQuantitatives.m_fMinSuppDisjonctions)
                fluxFichier.writeFloat(self.m_parametresReglesQuantitatives.m_iNombreAssociationRules) # # of rules per association to use

                # Parameters about that technique :
                fluxFichier.writeInt(self.m_parametresTechRecuitSimule.m_iNombreIterations)
                fluxFichier.writeInt(self.m_parametresTechRecuitSimule.m_iNombreSolutionsParalleles)
            except Exception as e:
                pass


        # Parametres du processus de chargement de regles pre-calculees : parameters of loading pre-calculated rules
        # 
        if not (iInfosSelectionnees & PROFIL_INFO_ALGO_CHARGEMENT) == 0:

            try:
                fluxFichier.writeByte(__FICHIER_PROFIL_DONNEES_ALGO_CHARGEMENT)
            except Exception as e:
                pass

            try:
                # Memorisation de la techique de resolution courante : memorize the current technique
                fluxFichier.writeInt(self.m_iTechniqueResolution)

                # Parameters about technique :
                fluxFichier.writeUTF(self.m_parametresTechChargement.m_sNomFichier) #name of the loaded rule file
            except Exception as e:
                pass


        try:
            fluxFichier.close()
        except Exception as e:
            pass


    # Load profile
    # La fonction renvoie "null" ou un message indiquant un avertissement ou une erreur :
    # The function returns "nullor a message indicating an error message:
    def ChargerProfil(self, sCheminFichier):
        fluxFichier = None
        sChaineUTF = None
        sNomBaseDeDonneesOuverte = None
        iIdentificateur = 0
        bFichierValide = False
        iNombreChamps = 0
        iIndiceChamp = 0
        sNomChamp = None
        iTypeChamp = 0
        bPrendreEnCompteChamp = False
        iNombreAttributs = 0
        iIndiceAttribut = 0
        # ColonneDonnees colonneDonnees = null
        bBaseDeDonneesChargee = False
        sNomAttribut = None
        sNomItem = None
        iNombreItems = 0
        iIndiceItem = 0
        sMessageInformation = None


        bBaseDeDonneesChargee = False
        sMessageInformation = None

        if self.m_gestionnaireBD == None:
            return None

        sNomBaseDeDonneesOuverte = self.m_gestionnaireBD.ObtenirNomBaseDeDonnees()
        if sNomBaseDeDonneesOuverte == None:
            return None

        try:
            fluxFichier = DataInputStream(FileInputStream(sCheminFichier))
        except Exception as e:
            print(e)
            return None

        # Lecture de l'identificateur d'un fichier de profil :
        # reading of the identifier of the profile file
        bFichierValide = False
        try:
            sChaineUTF = fluxFichier.readUTF() # Identificateur
            if not sChaineUTF == None:
                bFichierValide = sChaineUTF == "PROFIL01.00"
        except Exception as e:
            pass

        if not bFichierValide:
            try:
                fluxFichier.close()
            except Exception as e2:
                pass
            return None

        try:
            sChaineUTF = fluxFichier.readUTF()
            if not sNomBaseDeDonneesOuverte == sChaineUTF:
                sMessageInformation = "Warning : The profile was generated for a database named \""+sChaineUTF+"\", which does not correspond to the current database (\""+sNomBaseDeDonneesOuverte+"\").\nParameters were loaded to the best but could be inadequate."
        except Exception as e:
            try:
                fluxFichier.close()
            except Exception as e2:
                pass
            return None

        # Lecture de chaque categories d'informations contenues dans le profil : reading the information in the profile
        condition = True
        while condition:

            try:
                iIdentificateur = int(fluxFichier.readByte()) # Identificateur
            except Exception as e:
                iIdentificateur = __FICHIER_PROFIL_DONNEES_AUCUNES

            # Lecture des informations de pre-chargement des infos de la BD : reading the information about pre-loading the DB
            if iIdentificateur == __FICHIER_PROFIL_DONNEES_PRECHARGE:

                # Lecture du nombre de champs memorises : reading the number of field saved
                try:
                    iNombreChamps = fluxFichier.readInt()
                except Exception as e:
                    iNombreChamps = 0


                # Lecture de la configuration, champ par champ : reading the configuration field by field
                iIndiceChamp = 0
                while iIndiceChamp<iNombreChamps:

                    try:
                        # Lecture du nom du champ : reading the name of the field
                        sNomChamp = fluxFichier.readUTF()

                        # Lecture du type du champ : reading the type of the field
                        if fluxFichier.readByte() == __FICHIER_PROFIL_CHAMP_TYPE_QUANT:
                            iTypeChamp = DatabaseAdmin.TYPE_VALEURS_COLONNE_REEL
                        else:
                            iTypeChamp = DatabaseAdmin.TYPE_VALEURS_COLONNE_ITEM

                        # Lecture de la valeur (0 ou 1) indiquant si on prend ou non en compte le champ : reading the value of 0 or 1 indicating whether to take into consideration the field
                        bPrendreEnCompteChamp = fluxFichier.readByte() == 1

                        self.m_gestionnaireBD.DefinirPriseEnCompteColonne(sNomChamp, iTypeChamp, bPrendreEnCompteChamp)
                    except Exception as e:
                        pass

                    iIndiceChamp += 1

                # Chargement du contenu de la base de donnees : loading the content of the DB
                self.m_gestionnaireBD.ChargerDonneesPrisesEnCompte()
                self.GenererStructuresDonneesSelonBDPriseEnCompte()
                self.MettreAJourDonneesInternesFiltre()
                bBaseDeDonneesChargee = True


            # Lecture des informations sur la facon de construire une regle a extraire : reading the information on the way to build the rule to extract
            elif iIdentificateur == __FICHIER_PROFIL_DONNEES_PREEXTRACTION:

                # Creation des structures de donnees necessaires a la prise en compte des parametres de positionnement : Building data structure of the positionning parameters
                # si cette operation n'a pas encore ete effectuee prealablement : if not done before
                if not bBaseDeDonneesChargee:
                    self.m_gestionnaireBD.ChargerDonneesPrisesEnCompte()
                    self.GenererStructuresDonneesSelonBDPriseEnCompte()
                    bBaseDeDonneesChargee = True

                # Lecture du nombre d'attributs dont le positionnement est memorisee dans le fichier profil : read the number of attributes of positionning in the profile file
                try:
                    iNombreAttributs = fluxFichier.readInt()
                except Exception as e:
                    pass

                iIndiceAttribut = 0
                while iIndiceAttribut<iNombreAttributs:

                    try:

                        sNomAttribut = fluxFichier.readUTF()

                        # Lecture d'un attribut qualitatif : reading qualitative attribute
                        if fluxFichier.readByte() == 1:
                            iNombreItems = fluxFichier.readInt()
                            iIndiceItem = 0
                            while iIndiceItem<iNombreItems:
                                sNomItem = fluxFichier.readUTF()
                                self.DefinirTypePrisEnCompteItem(sNomAttribut, sNomItem, int(fluxFichier.readByte()))
                                self.DefinirPresenceObligatoireItem(sNomAttribut, sNomItem, (int(fluxFichier.readByte()) == 1))
                                iIndiceItem += 1

                        # Lecture d'un attribut quantitatif :  reading quantitative attribute
                        else:
                            self.DefinirTypePrisEnCompteAttribut(sNomAttribut, int(fluxFichier.readByte()))
                            self.DefinirPresenceObligatoireAttribut(sNomAttribut, (int(fluxFichier.readByte()) == 1))

                    except Exception as e:
                        pass

                    iIndiceAttribut += 1

                self.MettreAJourDonneesInternesFiltre()


            # Lecture des parametres concerant la technique d'extraction par Apriori : reading apriori parameters
            elif iIdentificateur == __FICHIER_PROFIL_DONNEES_ALGO_APRIORI:
                try:
                    # Technique courante lors de l'enregistrement du profil : technique used at the profile recording
                    self.m_iTechniqueResolution = fluxFichier.readInt()

                    # Parametres concernant les regles : parameters related to rules
                    self.m_parametresRegles.m_fMinSupp = fluxFichier.readFloat()
                    self.m_parametresRegles.m_fMinConf = fluxFichier.readFloat()
                except Exception as e:
                    pass


            # Lecture des parametres concerant la technique d'extraction par algorithme genetique : reading parameters w.r.t. the genetic algorithm
            elif iIdentificateur == __FICHIER_PROFIL_DONNEES_ALGO_GENETIQUE:
                try:
                    # Technique courante lors de l'enregistrement du profil :  technique used at the profile recording
                    self.m_iTechniqueResolution = fluxFichier.readInt()

                    # Param�tres concernant les r�gles :  parameters related to rules
                    self.m_parametresReglesQuantitatives.m_fMinSupp = fluxFichier.readFloat()
                    self.m_parametresReglesQuantitatives.m_fMinConf = fluxFichier.readFloat()
                    self.m_parametresReglesQuantitatives.m_iNombreDisjonctionsGauche = fluxFichier.readInt()
                    self.m_parametresReglesQuantitatives.m_iNombreDisjonctionsDroite = fluxFichier.readInt()
                    self.m_parametresReglesQuantitatives.m_iNombreMinAttributsQuant = fluxFichier.readInt()
                    self.m_parametresReglesQuantitatives.m_iNombreMaxAttributsQuant = fluxFichier.readInt()
                    self.m_parametresReglesQuantitatives.m_fMinSuppDisjonctions = fluxFichier.readFloat()
                    self.m_parametresReglesQuantitatives.m_iNombreAssociationRules = fluxFichier.readInt() # # of rules per association to use

                    # Param�tres concernant la technique :  parameters related to the technique
                    self.m_parametresTechAlgoGenetique.m_iTaillePopulation = fluxFichier.readInt()
                    self.m_parametresTechAlgoGenetique.m_iNombreGenerations = fluxFichier.readInt()
                    self.m_parametresTechAlgoGenetique.m_fPourcentageCroisement = fluxFichier.readFloat()
                    self.m_parametresTechAlgoGenetique.m_fPourcentageMutation = fluxFichier.readFloat()
                except Exception as e:
                    pass

            # Lecture des param�tres concerant la technique d'extraction par recuit simul� :  reading parameters w.r.t. simulated annealing technique
            elif iIdentificateur == __FICHIER_PROFIL_DONNEES_ALGO_RECUIT:
                try:
                    # Technique courante lors de l'enregistrement du profil : technique used at the profile recording
                    self.m_iTechniqueResolution = fluxFichier.readInt()

                    # Param�tres concernant les r�gles : parameters related to rules
                    self.m_parametresReglesQuantitatives.m_fMinSupp = fluxFichier.readFloat()
                    self.m_parametresReglesQuantitatives.m_fMinConf = fluxFichier.readFloat()
                    self.m_parametresReglesQuantitatives.m_iNombreDisjonctionsGauche = fluxFichier.readInt()
                    self.m_parametresReglesQuantitatives.m_iNombreDisjonctionsDroite = fluxFichier.readInt()
                    self.m_parametresReglesQuantitatives.m_iNombreMinAttributsQuant = fluxFichier.readInt()
                    self.m_parametresReglesQuantitatives.m_iNombreMaxAttributsQuant = fluxFichier.readInt()
                    self.m_parametresReglesQuantitatives.m_fMinSuppDisjonctions = fluxFichier.readFloat()
                    self.m_parametresReglesQuantitatives.m_iNombreAssociationRules = fluxFichier.readInt() # # of rules per association to use

                    # Param�tres concernant la technique : parameters related to the technique
                    self.m_parametresTechRecuitSimule.m_iNombreIterations = fluxFichier.readInt()
                    self.m_parametresTechRecuitSimule.m_iNombreSolutionsParalleles = fluxFichier.readInt()
                except Exception as e:
                    pass

            # Lecture des param�tres concerant len chargement de r�gles pr�-calcul�es : reading parameters w.r.t. precalculated rules
            elif iIdentificateur == __FICHIER_PROFIL_DONNEES_ALGO_CHARGEMENT:
                try:
                    # Technique courante lors de l'enregistrement du profil : technique used at the profile recording
                    self.m_iTechniqueResolution = fluxFichier.readInt()

                    # Param�tres concernant la technique : parameters related to the technique
                    self.m_parametresTechChargement.m_sNomFichier = fluxFichier.readUTF()
                    self.PreChargerFichierReglesBinaires(self.m_parametresTechChargement.m_sNomFichier)
                except Exception as e:
                    pass

            else:
                iIdentificateur = __FICHIER_PROFIL_DONNEES_AUCUNES
            condition = not iIdentificateur == __FICHIER_PROFIL_DONNEES_AUCUNES

        try:
            fluxFichier.close()
        except Exception as e:
            pass

        return sMessageInformation


    #return percentage in string format
    @staticmethod
    def EcrirePourcentage(fProportion, iNombreChiffresApresVirgule, bAfficherPourcent):
        sChaine = None
        iPartieEntiere = 0
        iPartieDecimale = 0

        fProportion *= 100.0
        iPartieEntiere = int(fProportion)

        fProportion -= float(iPartieEntiere)
        fProportion *= float(10.0 ** float(iNombreChiffresApresVirgule))
        iPartieDecimale = round(fProportion)

        sChaine = str(iPartieEntiere) + "." + str(iPartieDecimale)

        if bAfficherPourcent:
            sChaine += " %"

        return sChaine


    def EcrireSupport(self, iNombreOccurrences):
        sChaine = None

        sChaine = str(iNombreOccurrences)
        sChaine += " ("
        if not self.m_gestionnaireBD == None:
            sChaine += str(EcrirePourcentage((float(iNombreOccurrences)) / (float(self.m_gestionnaireBD.ObtenirNombreLignes())), 2, True))
        else:
            sChaine += " ? "
        sChaine += ")"

        return sChaine


    #save in rules in qmr file
    def SauvegarderReglesBinaire(self, sCheminFichier, tRegles):
        fluxFichier = None
        iNombreRegles = 0
        iIndiceRegle = 0
        iIndiceItem = 0
        iNombreItems = 0
        iEtapeTestRegle = 0
        iIndiceDisjonction = 0
        iNombreDisjonctions = 0
        item = None
        itemQual = None
        itemQuant = None
        regle = None

        if (m_aprioriCourant == None) or (sCheminFichier == None):
            return

        try:
            fluxFichier = DataOutputStream(FileOutputStream(sCheminFichier))
        except Exception as e:
            print(e)
            return

        try:
            fluxFichier.writeUTF("QUANTMINER_REGLES.00") # Identificateur
        except Exception as e:
            pass


        # Enregistrement des informations sur le contexte d'enregistrement : Saving informnation about the recording context
        try:
            fluxFichier.writeUTF(self.m_sNomUtilisateur)
            fluxFichier.writeUTF(self.m_gestionnaireBD.ObtenirNomBaseDeDonnees())
            fluxFichier.writeUTF("ENV.ObtenirDateCourante()")
            fluxFichier.writeUTF(self.m_sDescriptionRegles)
            fluxFichier.writeUTF(self.ObtenirInfosContexte(True))
        except Exception as e:
            pass

        # Enregistrement du nombre de r�gles : recording the number of rules
        if not tRegles == None:
            iNombreRegles = len(tRegles)
        else:
            iNombreRegles = 0

        try:
            fluxFichier.writeInt(iNombreRegles)
        except Exception as e:
            pass


        # Enregistrement du support utilis� pour l'extraction des r�gles : recording the support used for rule extraction
        try:
            fluxFichier.writeFloat(self.m_aprioriCourant.ObtenirSupportMinimal())
        except Exception as e:
            pass


        iIndiceRegle = 0
        while iIndiceRegle<iNombreRegles:

            regle = tRegles[iIndiceRegle]

            try:

                # Informations sur la structure de la r�gle : information about the rule structure
                fluxFichier.writeInt(regle.m_iNombreItemsGauche)
                fluxFichier.writeInt(regle.m_iNombreItemsDroite)
                fluxFichier.writeInt(regle.m_iNombreDisjonctionsGaucheValides)
                fluxFichier.writeInt(regle.m_iNombreDisjonctionsDroiteValides)

                # Informations statistiques sur la r�gle : information about rule stats
                fluxFichier.writeFloat(regle.m_fSupport)
                fluxFichier.writeFloat(regle.m_fConfiance)
                fluxFichier.writeInt(regle.m_iOccurrences)
                fluxFichier.writeInt(regle.m_iOccurrencesGauche)
                fluxFichier.writeInt(regle.m_iOccurrencesDroite)
                fluxFichier.writeInt(regle.m_iOccurrences_Gauche_NonDroite)
                fluxFichier.writeInt(regle.m_iOccurrences_NonGauche_Droite)
                fluxFichier.writeInt(regle.m_iOccurrences_NonGauche_NonDroite)

                # Contenu de la r�gle : rule content
                for iEtapeTestRegle in range(0, 2):

                    if iEtapeTestRegle==0:
                        iNombreItems = regle.m_iNombreItemsGauche
                        iNombreDisjonctions = regle.m_iNombreDisjonctionsGaucheValides
                    else:
                        iNombreItems = regle.m_iNombreItemsDroite
                        iNombreDisjonctions = regle.m_iNombreDisjonctionsDroiteValides

                    iIndiceItem = 0
                    while iIndiceItem<iNombreItems:

                        if iEtapeTestRegle==0:
                            item = regle.ObtenirItemGauche(iIndiceItem)
                        else:
                            item = regle.ObtenirItemDroite(iIndiceItem)

                        # Enregistrement du type de l'item : recording the type of item
                        fluxFichier.writeInt(item.m_iTypeItem)

                        # Enregistrement des donnees de l'item suivant son type : recording the data of the item depending on its type

                        if item.m_iTypeItem == Item.ITEM_TYPE_QUALITATIF:
                            itemQual = item
                            fluxFichier.writeUTF(itemQual.m_attributQual.ObtenirNom())
                            fluxFichier.writeUTF(itemQual.ObtenirIdentifiantTexteItem())
                        elif item.m_iTypeItem == Item.ITEM_TYPE_QUANTITATIF:
                            itemQuant = item
                            fluxFichier.writeUTF(itemQuant.m_attributQuant.ObtenirNom())

                            # Ecriture des bornes pour chaque disjonction : writing the bounds of each disjunction
                            iIndiceDisjonction = 0
                            while iIndiceDisjonction<iNombreDisjonctions:
                                fluxFichier.writeFloat(itemQuant.m_tBornes[iIndiceDisjonction*2])
                                fluxFichier.writeFloat(itemQuant.m_tBornes[iIndiceDisjonction*2+1])
                                iIndiceDisjonction += 1
                        iIndiceItem += 1
            except Exception as e:
                pass
            iIndiceRegle += 1


        try:
            fluxFichier.close()
        except Exception as e:
            pass


    #pre-load qmr file
    def PreChargerFichierReglesBinaires(self, sCheminFichier):
        fluxFichier = None
        sChaineUTF = None
        bFichierValide = False

        # Retour aux valeurs par defaut en cas d'echec : recover default values in case of failure
        self.m_parametresTechChargement.m_sNomFichier = None
        self.m_parametresTechChargement.m_sNomUtilisateurOrigine = "User unknown"
        self.m_parametresTechChargement.m_sNomBaseOrigine = "Database unkown"
        self.m_parametresTechChargement.m_sDateOrigine = "Date unknown"
        self.m_parametresTechChargement.m_sDescriptionRegles = "Missing Description"
        self.m_parametresTechChargement.m_sDescriptionCompleteContexte = "No information."

        if sCheminFichier == None:
            return

        try:
            fluxFichier = DataInputStream(FileInputStream(sCheminFichier))
        except Exception as e:
            print(e)
            return

        # Lecture de l'identificateur d'un fichier binaire de regles :
        bFichierValide = False
        try:
            sChaineUTF = fluxFichier.readUTF()
            if not sChaineUTF == None:
                bFichierValide = sChaineUTF == "QUANTMINER_REGLES.00"
        except Exception as e:
            pass

        if not bFichierValide:
            try:
                fluxFichier.close()
            except Exception as e:
                pass
            return


        # Le fichier est valide : on le m�morise pour le param�trage :
        self.m_parametresTechChargement.m_sNomFichier = sCheminFichier

        # Lecture des informations d'en-tete contenues dans le fichier de r�gles :
        try:
            self.m_parametresTechChargement.m_sNomUtilisateurOrigine = fluxFichier.readUTF()
            self.m_parametresTechChargement.m_sNomBaseOrigine = fluxFichier.readUTF()
            self.m_parametresTechChargement.m_sDateOrigine = fluxFichier.readUTF()
            self.m_parametresTechChargement.m_sDescriptionRegles = fluxFichier.readUTF()
            self.m_parametresTechChargement.m_sDescriptionCompleteContexte = fluxFichier.readUTF()
        except Exception as e:
            pass


        try:
            fluxFichier.close()
        except Exception as e:
            pass


    @staticmethod
    def EcrireDescriptionFichierReglesBinairesHTML(sCheminFichier):
        fluxFichier = None
        sChaineUTF = None
        bFichierValide = False
        iNombreRegles = 0
        sNomUtilisateurOrigine = None
        sNomBaseOrigine = None
        sDateOrigine = None
        sDescriptionRegles = None
        sDescriptionCompleteContexte = None
        sDescriptifTotal = None


        if sCheminFichier == None:
            return "<BR><BR><b>Impossible to open the file!</b>"

        # Valeurs par d�faut :
        sNomUtilisateurOrigine = "user unknown"
        sNomBaseOrigine = "database unkown"
        sDateOrigine = "date unknown"
        sDescriptionRegles = "Missing description"
        sDescriptionCompleteContexte = "No information."
        iNombreRegles = 0
        sDescriptifTotal = ""

        try:
            fluxFichier = DataInputStream(FileInputStream(sCheminFichier))
        except Exception as e:
            return "<BR><BR><b>Impossible to open the file!</b>"

        # Lecture de l'identificateur d'un fichier binaire de r�gles :
        bFichierValide = False
        try:
            sChaineUTF = fluxFichier.readUTF()
            if not sChaineUTF == None:
                bFichierValide = sChaineUTF == "QUANTMINER_REGLES.00"
        except Exception as e:
            pass

        if not bFichierValide:
            try:
                fluxFichier.close()
            except Exception as e:
                pass
            return "<BR><BR><b>This file is not a valid QuantMiner file of rules!</b>"


        # Lecture des informations d'en-tete contenues dans le fichier de r�gles :
        try:
            sNomUtilisateurOrigine = fluxFichier.readUTF()
            sNomBaseOrigine = fluxFichier.readUTF()
            sDateOrigine = fluxFichier.readUTF()
            sDescriptionRegles = fluxFichier.readUTF()
            sDescriptionCompleteContexte = fluxFichier.readUTF()
            iNombreRegles = fluxFichier.readInt()
        except Exception as e:
            pass


        # Ecriture du compte-rendu HTML :
        sDescriptifTotal += "<BR><i>Database: </i><b>" + sNomBaseOrigine + "</b>"
        sDescriptifTotal += "<BR><i>Date:</i><b>" + sDateOrigine + "</b>"
        sDescriptifTotal += "<BR><i>Author: </i><b>" + sNomUtilisateurOrigine + "</b>"
        sDescriptifTotal += "<BR><i>Number of rules: </i><b>" + str(iNombreRegles) + "</b>"

        sDescriptifTotal += "<BR><BR><BR><BR><BR><b><u><i><big>Extracted rules:</big></i></u></b><BR><BR><BR><BR>"
        sDescriptifTotal += FormateHTML(sDescriptionRegles)

        sDescriptifTotal += "<BR><BR><BR><BR><BR><b><u><i><big>Extraction context:</big></i></u></b><BR><BR><BR><BR>"
        sDescriptifTotal += sDescriptionCompleteContexte

        try:
            fluxFichier.close()
        except Exception as e:
            pass

        return sDescriptifTotal

    #load rules
    def ChargerReglesBinaire(self, sCheminFichier):
        fluxFichier = None
        sChaineUTF = None
        bFichierValide = False
        bRegleValide = False
        iNombreRegles = 0
        iIndiceRegle = 0
        iIndiceItem = 0
        iNombreItems = 0
        iEtapeTestRegle = 0
        iIndiceDisjonction = 0
        iNombreDisjonctions = 0
        iNombreItemsGauche = 0
        iNombreItemsDroite = 0
        iNombreDisjonctionsGauche = 0
        iNombreDisjonctionsDroite = 0
        iTypeItem = 0
        iIndiceValeurItemQual = 0
        item = None
        itemQual = None
        itemQuant = None
        attributQual = None
        attributQuant = None
        regle = None
        iIndiceAjoutItem = 0
        sNomAttribut = None
        sNomItem = None
        fSupportMin = 0.0
        fBorneMin = 0.0
        fBorneMax = 0.0

        if sCheminFichier == None:
            return

        if self.m_listeRegles == None:
            self.m_listeRegles = []
        else:
            self.m_listeRegles.clear()

        try:
            fluxFichier = DataInputStream(FileInputStream(sCheminFichier))
        except Exception as e:
            print(e)
            return

        # Lexture de l'identificateur d'un fichier binaire de r�gles :
        bFichierValide = False
        try:
            sChaineUTF = fluxFichier.readUTF()
            if not sChaineUTF == None:
                bFichierValide = sChaineUTF == "QUANTMINER_REGLES.00"
        except Exception as e:
            pass

        if not bFichierValide:
            try:
                fluxFichier.close()
            except Exception as e2:
                pass
            return


        # Lecture des informations contenues dans l'en-tete du fichier de r�gles :
        try:
            # Simples informations d�j� charg�es via un pr�-chargement du fichier :
            fluxFichier.readUTF()
            fluxFichier.readUTF()
            fluxFichier.readUTF()
            fluxFichier.readUTF()
            fluxFichier.readUTF()

            # Nombre de r�gles � lire dans le fichier :
            iNombreRegles = fluxFichier.readInt()
        except Exception as e:
            pass


        # Lecture du support utilis� pour l'extraction :
        try:
            fSupportMin = fluxFichier.readFloat()
        except Exception as e:
            pass


        # Cr�ation d'un Apriori r�pertoriant attributs et items :
        self.m_aprioriCourant = AprioriQuantitative(self)
        self.m_aprioriCourant.SpecifierSupportMinimal(fSupportMin)
        self.m_aprioriCourant.ExecuterPretraitement(False)


        # Lecture de la liste de r�gles :
        iIndiceRegle = 0
        while iIndiceRegle<iNombreRegles:

            try:

                # Informations sur la structure de la r�gle :
                iNombreItemsGauche = fluxFichier.readInt()
                iNombreItemsDroite = fluxFichier.readInt()
                iNombreDisjonctionsGauche = fluxFichier.readInt()
                iNombreDisjonctionsDroite = fluxFichier.readInt()

                regle = AssociationRule(iNombreItemsGauche, iNombreItemsDroite, iNombreDisjonctionsGauche, iNombreDisjonctionsDroite)

                # Informations statistiques sur la r�gle :
                regle.m_fSupport = fluxFichier.readFloat()
                regle.m_fConfiance = fluxFichier.readFloat()
                regle.m_iOccurrences = fluxFichier.readInt()
                regle.m_iOccurrencesGauche = fluxFichier.readInt()
                regle.m_iOccurrencesDroite = fluxFichier.readInt()
                regle.m_iOccurrences_Gauche_NonDroite = fluxFichier.readInt()
                regle.m_iOccurrences_NonGauche_Droite = fluxFichier.readInt()
                regle.m_iOccurrences_NonGauche_NonDroite = fluxFichier.readInt()

                # Contenu de la r�gle :
                bRegleValide = True
                iEtapeTestRegle=0
                while iEtapeTestRegle<2:

                    if iEtapeTestRegle==0:
                        iNombreItems = iNombreItemsGauche
                        iNombreDisjonctions = iNombreDisjonctionsGauche
                    else:
                        iNombreItems = iNombreItemsDroite
                        iNombreDisjonctions = iNombreDisjonctionsDroite

                    iIndiceAjoutItem = 0

                    iIndiceItem=0
                    while iIndiceItem<iNombreItems:

                        # Lecture du type de l'item :
                        iTypeItem = fluxFichier.readInt()

                        # Lecture des donn�es de l'item suivant son type :

                        if iTypeItem == Item.ITEM_TYPE_QUALITATIF:

                            sNomAttribut = fluxFichier.readUTF()
                            sNomItem = fluxFichier.readUTF()

                            itemQual = None
                            attributQual = self.m_aprioriCourant.ObtenirAttributQualitatifDepuisNom(sNomAttribut)
                            if not attributQual == None:
                                iIndiceValeurItemQual = attributQual.ObtenirIndiceCorrespondantValeur(sNomItem)
                                if iIndiceValeurItemQual >= 0:
                                    itemQual = self.m_aprioriCourant.ObtenirItem(attributQual, iIndiceValeurItemQual)

                            item = itemQual

                        elif iTypeItem == Item.ITEM_TYPE_QUANTITATIF:

                            sNomAttribut = fluxFichier.readUTF()

                            itemQuant = None
                            attributQuant = self.m_aprioriCourant.ObtenirAttributQuantitatifDepuisNom(sNomAttribut)
                            if not attributQuant == None:
                                itemQuant = ItemQuantitative(attributQuant, iNombreDisjonctions)

                            iIndiceDisjonction = 0
                            while iIndiceDisjonction<iNombreDisjonctions:
                                fBorneMin = fluxFichier.readFloat()
                                fBorneMax = fluxFichier.readFloat()
                                if not itemQuant == None:
                                    itemQuant.m_tBornes[iIndiceDisjonction*2] = fBorneMin
                                    itemQuant.m_tBornes[iIndiceDisjonction*2+1] = fBorneMax
                                iIndiceDisjonction += 1

                            item = itemQuant

                        if item == None:
                            bRegleValide = False
                        else:
                            if iEtapeTestRegle==0:
                                regle.AssignerItemGauche(item, iIndiceAjoutItem)
                            else:
                                regle.AssignerItemDroite(item, iIndiceAjoutItem)
                            iIndiceAjoutItem += 1

                        iIndiceItem += 1
                    iEtapeTestRegle += 1
            except Exception as e:
                bRegleValide = False

            # Add the rule if it is valid:
            # Adding the rule to m_listeRegles (- change from top 1 to top 'n' added)
            if bRegleValide:
                if self.EstRegleValide(regle):
                    self.m_listeRegles.append(regle)

            iIndiceRegle += 1

        try:
            fluxFichier.close()
        except Exception as e:
            pass


#                                             
# *Copyright 2007, 2011 CCLS Columbia University (USA), LIFO University of Orleans (France), BRGM (France)
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


class RuleOptimizer(object):

    def __init__(self):
        self.m_contexteResolution = None



    def DefinirContexteResolution(self, contexteResolution):
        self.m_contexteResolution = contexteResolution

    #public abstract boolean OptimiseRegle(AssociationRule regle)
    def OptimiseRegle(self, regle, i):
        pass

#                                             
# *Copyright 2007, 2011 CCLS Columbia University (USA), LIFO University of Orleans (France), BRGM (France)
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
import threading

cwd = os.getcwd()
sys.path.append(cwd)
# sys.path.append('C:\\Users\\aalsahee\\python_physical_model\\Saudi\\trace\\Traces\\qtm\\src\\')

# from apriori import *
# from apriori import AprioriQuantitative
# from database import *
# from geneticAlgorithm import *

class RuleTester(threading.Thread):
    # Class allowing the execution of a particular code during the calculation of the rules:
    # Class allowing to execute a particular code during the cumputation of rules:
    class IndicateurCalculRegles(object):
        def IndiquerFinCalcul(self):
            pass
        def EnvoyerInfo(self, sNouvelleInfo):
            pass
        def IndiquerNombreReglesATester(self, iNombreReglesATester):
            pass

    # Definition of a specific process to be inserted during the execution of the Apriori algorithm:
    # Definition of a specific treatment to do during the apriori algorithm execution
    class TraitementPendantCalculFrequents(): #AprioriQuantitative.TraitementExternePendantCalcul

        def __init__(self, outerInstance):
            self.__outerInstance = outerInstance


        def ExecuterTraitementExterne(self):
            try:
                sleep(0)
            except Exception as e:
                pass

            return self.__outerInstance.m_bEnExecution

    # Indicate that a set of rule are completely calculated




    def __init__(self, contexteResolution, indicateurCalcul):
        threading.Thread.__init__(self)
        self.__m_contexteResolution = None
        self.__m_optimiseurCourant = None
        self.m_bEnExecution = False
        self.__m_bResultatDisponible = False
        self.m_apriori = None
        self.m_iNombreTotalAttributsQuant = 0
        self.m_iNombreItemsQuantConsideres = 0
        self.__m_iMinimumItemsQuantConsideres = 0
        self.__m_iMaximumItemsQuantConsideres = 0
        self.m_iTailleFrequent = 0
        self.m_iIndiceFrequent = 0
        self.m_iIndiceCombinaisonItemsQuant = 0
        self.m_iIndiceRepartitionItems = 0
        self.m_bFinTestRegles = False
        self.m_iNombreReglesTestees = 0
        self.m_listeRegles = None
        self.m_listeCentroids = None
        self.__m_listeAttributsQuant = None
        self.__m_indicateurCalcul = None
        self.__m_bIndiquerFinCalcul = False
        self.__m_bModeSpecialComptabilisationRegles = False
        self.__m_iNombreReglesComptabilisees = 0
        self.m_fMinSupp = 0.0
        self.m_fMinConf = 0.0
        self.m_iNombreDisjonctionsGauche = 0
        self.m_iNombreDisjonctionsDroite = 0
        self.m_applyKMeans = 0

        self.__m_contexteResolution = contexteResolution
        self.__m_indicateurCalcul = indicateurCalcul
        self.__m_bIndiquerFinCalcul = True
        self.m_bEnExecution = False
        self.__m_bResultatDisponible = False
        self.m_iNombreReglesTestees = 0
        self.__m_bModeSpecialComptabilisationRegles = False

        # Pre-calculate a l'aide de l'algorithme Apriori standard :
        # pre-calculate with apriori standard algorithm
        if self.__m_contexteResolution is None:
            return


        if self.__m_contexteResolution.m_iTechniqueResolution == ResolutionContext.TECHNIQUE_APRIORI_QUAL:
            self.m_fMinSupp = self.__m_contexteResolution.m_parametresRegles.m_fMinSupp
            self.m_fMinConf = self.__m_contexteResolution.m_parametresRegles.m_fMinConf
            self.__m_iMinimumItemsQuantConsideres = 0
            self.__m_iMaximumItemsQuantConsideres = 0
            self.m_iNombreDisjonctionsGauche = 1 #Disjunctions 'OR'
            self.m_iNombreDisjonctionsDroite = 1
            self.m_applyKMeans = 0

        elif self.__m_contexteResolution.m_iTechniqueResolution == ResolutionContext.TECHNIQUE_ALGO_GENETIQUE:
            self.m_fMinSupp = self.__m_contexteResolution.m_parametresReglesQuantitatives.m_fMinSupp
            self.m_fMinConf = self.__m_contexteResolution.m_parametresReglesQuantitatives.m_fMinConf
            self.m_iNombreDisjonctionsGauche = self.__m_contexteResolution.m_parametresReglesQuantitatives.m_iNombreDisjonctionsGauche
            self.m_iNombreDisjonctionsDroite = self.__m_contexteResolution.m_parametresReglesQuantitatives.m_iNombreDisjonctionsDroite
            self.__m_iMinimumItemsQuantConsideres = self.__m_contexteResolution.m_parametresReglesQuantitatives.m_iNombreMinAttributsQuant
            self.__m_iMaximumItemsQuantConsideres = self.__m_contexteResolution.m_parametresReglesQuantitatives.m_iNombreMaxAttributsQuant
            self.m_applyKMeans = self.__m_contexteResolution.m_parametresReglesQuantitatives.m_applyKMeans

        elif self.__m_contexteResolution.m_iTechniqueResolution == ResolutionContext.TECHNIQUE_RECUIT_SIMULE:
            self.m_fMinSupp = self.__m_contexteResolution.m_parametresReglesQuantitatives.m_fMinSupp
            self.m_fMinConf = self.__m_contexteResolution.m_parametresReglesQuantitatives.m_fMinConf
            self.m_iNombreDisjonctionsGauche = self.__m_contexteResolution.m_parametresReglesQuantitatives.m_iNombreDisjonctionsGauche
            self.m_iNombreDisjonctionsDroite = self.__m_contexteResolution.m_parametresReglesQuantitatives.m_iNombreDisjonctionsDroite
            self.__m_iMinimumItemsQuantConsideres = self.__m_contexteResolution.m_parametresReglesQuantitatives.m_iNombreMinAttributsQuant
            self.__m_iMaximumItemsQuantConsideres = self.__m_contexteResolution.m_parametresReglesQuantitatives.m_iNombreMaxAttributsQuant
            self.m_applyKMeans = self.__m_contexteResolution.m_parametresReglesQuantitatives.m_applyKMeans

        else:
            return


        if self.__m_contexteResolution.m_gestionnaireBD is None:
            return

        # Mise en place d'une nouvelle execution de l'algorithme Arpriori, repertoriee dans le contexte d'execution :
        # Setting for a new execution of apriori defined in the context of execution:
        self.__m_contexteResolution.m_aprioriCourant = None
        self.m_apriori = AprioriQuantitative(self.__m_contexteResolution)
        self.__m_contexteResolution.m_aprioriCourant = self.m_apriori

        self.m_apriori.SpecifierSupportMinimal(self.m_fMinSupp)
        self.m_apriori.SpecifierTraitementExterne(self.TraitementPendantCalculFrequents(self))
        self.m_apriori.ExecuterPretraitement(True) #execute pre-process

    #Getter method, used in PanelGenetic.java
    def getNumAssocationRules(self):
        return self.__m_contexteResolution.m_parametresReglesQuantitatives.m_iNombreAssociationRules

    def AutoriserIndicationFinCalcul(self, bIndiquerFinCalcul):
        self.__m_bIndiquerFinCalcul = bIndiquerFinCalcul


    #Define the optimizer(e.g. Genetic algorithm) used to optimize rules
    def DefinirOptimiseurRegle(self, optimiseur):
        if optimiseur is not None:
            self.__m_optimiseurCourant = optimiseur
            self.__m_optimiseurCourant.DefinirContexteResolution(self.__m_contexteResolution)


    #start to do optimization
    def run(self):

        #add while loop if running testRuleProximities() in KMeansClusterer, in order to test different values of n
        # while(m_contexteResolution.m_parametresReglesQuantitatives.m_iNombreAssociationRules <= 200){
        iTypePriseEnCompte = 0
        iIndiceAttributsQuant = 0
        iNombreAttributsQuantBase = 0
        attributQuant = None
        bFinInitApriori = False
        iTailleFrequents = 0
        iNombreReglesATester = 0
        self.m_iNombreReglesTestees = 0
        self.__m_bResultatDisponible = False
        self.m_listeRegles = []
        self.m_listeCentroids = []

        if self.m_apriori is None:
            return


        self.m_bEnExecution = True
        bFinInitApriori = False
        iTailleFrequents = 2

        if self.__m_indicateurCalcul is not None:
            self.__m_indicateurCalcul.EnvoyerInfo("Pre-computation with the Apriori algorithm:\n")


        # try:

        while (self.m_bEnExecution) and ((not bFinInitApriori)) and (iTailleFrequents <= 3): #

            # On genere les listes de K-items frequency successively:     
            # We generate the list of the frequency of K-items successively:
            if self.__m_indicateurCalcul is not None:
                self.__m_indicateurCalcul.EnvoyerInfo("Computing the set of "+ str(iTailleFrequents) + " consecutive frequent modalities...")

            bFinInitApriori = not self.m_apriori.GenererNouvelleListeItemSets()
            # bFinInitApriori = True

            if self.__m_indicateurCalcul is not None:
                if bFinInitApriori:
                    self.__m_indicateurCalcul.EnvoyerInfo("FINISH!\n")
                else:
                    self.__m_indicateurCalcul.EnvoyerInfo("OK\n")
            iTailleFrequents += 1


            if bFinInitApriori or (iTailleFrequents > 3):

                self.m_apriori.ElaguerItemsetsSelonFiltre()

                # On repertorie uniquement les attributs quantitatifs a prendre en compte :
                # we list only the quantitative attributes to consider: 
                self.__m_listeAttributsQuant = []
                self.m_iNombreTotalAttributsQuant = 0

                if self.__m_iMaximumItemsQuantConsideres > 0:

                    iNombreAttributsQuantBase = self.m_apriori.ObtenirNombreAttributsQuantitatifs()
                    iIndiceAttributsQuant = 0
                    while iIndiceAttributsQuant < iNombreAttributsQuantBase:
                        attributQuant = self.m_apriori.ObtenirAttributQuantitatif(iIndiceAttributsQuant)
                        if attributQuant is not None:
                            iTypePriseEnCompte = self.__m_contexteResolution.ObtenirTypePrisEnCompteAttribut(attributQuant.ObtenirNom())

                            if iTypePriseEnCompte != ResolutionContext.PRISE_EN_COMPTE_ITEM_NULLE_PART:
                                self.__m_listeAttributsQuant.append(attributQuant)
                                self.m_iNombreTotalAttributsQuant += 1
                        iIndiceAttributsQuant += 1

                    if self.__m_iMaximumItemsQuantConsideres > self.m_iNombreTotalAttributsQuant:
                        self.__m_iMaximumItemsQuantConsideres = self.m_iNombreTotalAttributsQuant


                # Calculate the number of rules to test:
                if self.__m_indicateurCalcul is not None:
                    self.__m_indicateurCalcul.EnvoyerInfo("\n\nComputing the number of rules to test...")

                #number of rules to test
                iNombreReglesATester = self.ComptabiliserNombreMaxReglesTestees()


                if self.__m_indicateurCalcul is not None:
                    self.__m_indicateurCalcul.IndiquerNombreReglesATester(iNombreReglesATester)
                    self.__m_indicateurCalcul.EnvoyerInfo(":  " + str(iNombreReglesATester * self.__m_contexteResolution.m_parametresReglesQuantitatives.m_iNombreAssociationRules) + " rules.\n\n\n")


        # Calculate the rules:
        if self.m_bEnExecution:
            self.m_iNombreItemsQuantConsideres = self.__m_iMinimumItemsQuantConsideres
            self.m_iTailleFrequent = max(2-self.m_iNombreItemsQuantConsideres, 0)
            self.m_iIndiceFrequent = 0
            self.m_iIndiceCombinaisonItemsQuant = 0
            self.m_iIndiceRepartitionItems = 0
            self.m_bFinTestRegles = False
            self.__m_bModeSpecialComptabilisationRegles = False

            if self.__m_indicateurCalcul is not None:
                #print the information of the context to the context text area
                self.__m_indicateurCalcul.EnvoyerInfo(self.__m_contexteResolution.ObtenirInfosContexte(False))

            while (self.m_bEnExecution) and ((not self.m_bFinTestRegles)):
                #Calculate new rule
                self.CalculerNouvelleRegle()

                try:
                    sleep(1)
                except Exception as e:
                    pass

        # except Exception as e:
        #     print("----*")
        #     print(str(e))
        #     print("----")

            if self.__m_indicateurCalcul is not None:
                # self.__m_indicateurCalcul.EnvoyerInfo("\n\n\nDEPASSEMENT DES CAPACITES MEMOIRE !")
                # self.__m_indicateurCalcul.EnvoyerInfo("\nPlease intensify filtering or reduce the minimum support...\n")
                print("\n\n\nDEPASSEMENT DES CAPACITES MEMOIRE !")
                print("\nPlease intensify filtering or reduce the minimum support...\n\n\n\n")

                # print("CWD: " + str(cwd))
                f = open("output/rules.txt", "a")
                i = 1
                for rule in self.m_listeRegles:
                    line = str(i) + ". " + str(rule.toString()) + "\n"
                    print(line)
                    f.write(line)
                    # sys.exit()
                    i += 1

                f.close()

                RuleTester.threadFinished = True


        self.__m_bResultatDisponible = True

        #Calculation finishes
        if (self.__m_indicateurCalcul is not None) and (self.__m_bIndiquerFinCalcul):
            self.__m_indicateurCalcul.IndiquerFinCalcul()


        #increment m_contexteResolution.m_parametresReglesQuantitatives.m_iNombreAssociationRules by 5
        self.__m_contexteResolution.m_parametresReglesQuantitatives.m_iNombreAssociationRules += 5

        # }
    #END OF RUN


    # Simulate an optimization to count the number of rules that will be tested
    def ComptabiliserNombreMaxReglesTestees(self):
        iNombreNouvellesBoucles = 0

        if self.m_apriori is None:
            return 0

        self.m_iNombreItemsQuantConsideres = self.__m_iMinimumItemsQuantConsideres
        self.m_iTailleFrequent = max(2-self.m_iNombreItemsQuantConsideres, 0)
        self.m_iIndiceFrequent = 0
        self.m_iIndiceCombinaisonItemsQuant = 0
        self.m_iIndiceRepartitionItems = 0
        self.m_bFinTestRegles = False
        self.__m_bModeSpecialComptabilisationRegles = True
        # self.__m_iNombreReglesComptabilisees = 0
        iNombreNouvellesBoucles = 0

        while (self.m_bEnExecution) and ((not self.m_bFinTestRegles)):
            self.CalculerNouvelleRegle()
            iNombreNouvellesBoucles += 1

            if iNombreNouvellesBoucles > 25000:
                try:
                    sleep(1)
                except Exception as e:
                    pass
                iNombreNouvellesBoucles = 0

                if self.__m_indicateurCalcul is not None:
                    self.__m_indicateurCalcul.EnvoyerInfo(".")

        # self.__m_iNombreReglesComptabilisees = iNombreNouvellesBoucles
        return self.__m_iNombreReglesComptabilisees

    lastPrintedRules = 0
    threadFinished = False
    #calculate new rules
    def CalculerNouvelleRegle(self):
        itemSetFrequent = None
        attributQuant = None
        iIndiceItemRegle = 0
        iIndiceAttributQuant = 0
        iIndiceEvolution = 0
        itemQual = None
        itemQuant = None
        tRepartitionItems = None
        iIndiceAttributQuantAjoute = 0
        tCombinaisonItemsQuant = None
        listeRegles = None

        if self.__m_optimiseurCourant is None:
            self.m_bFinTestRegles = True
            return

        # On arrete quand on a teste toutes les regles possibles dont le nombre d'attributs quantitatifs ne depasse pas le nombre autorise :
        # We stop when we have tested all the possible rules for which the number of quantative attributes does not exceed the authorized number: 
        if self.m_iNombreItemsQuantConsideres > self.__m_iMaximumItemsQuantConsideres:
            self.m_bFinTestRegles = True
            return

        if self.m_iTailleFrequent > 0:
            itemSetFrequent = self.m_apriori.RecupererFrequent(self.m_iTailleFrequent, self.m_iIndiceFrequent)
            if itemSetFrequent is None:
                self.m_iTailleFrequent += 1
                self.m_iIndiceFrequent = 0
                self.m_iIndiceCombinaisonItemsQuant = 0
                self.m_iIndiceRepartitionItems = 0
                itemSetFrequent = self.m_apriori.RecupererFrequent(self.m_iTailleFrequent, self.m_iIndiceFrequent)

            # Cas ou tous les items ont ete traites pour un nombre d'attributs quantitatifs donne :
            # Case where all the items are treated for a given number of quantitative attribute:
            if itemSetFrequent is None:
                self.m_iNombreItemsQuantConsideres += 1
                self.m_iTailleFrequent = max(2-self.m_iNombreItemsQuantConsideres, 0)
                self.m_iIndiceFrequent = 0
                self.m_iIndiceCombinaisonItemsQuant = 0
                self.m_iIndiceRepartitionItems = 0
                return


        if self.m_iNombreItemsQuantConsideres > 0:

            tCombinaisonItemsQuant = AprioriQuantitative.CalculerEnsemblesItems(self.m_iIndiceCombinaisonItemsQuant, self.m_iNombreTotalAttributsQuant, self.m_iNombreItemsQuantConsideres)
            if tCombinaisonItemsQuant is None:
                if self.m_iTailleFrequent == 0:
                    self.m_iTailleFrequent += 1
                    self.m_iIndiceFrequent = 0
                else:
                    self.m_iIndiceFrequent += 1
                self.m_iIndiceCombinaisonItemsQuant = 0
                self.m_iIndiceRepartitionItems = 0
                return


        # Calcul de la repartition des items a droite et a gauche. Dans le tableau
        # ou chaque indice correspond a un item (les "iTailleFrequent" premiers sont les items qualitatifs)
        # on placera les items ayant la valeur "vrai" dans la case du tableau qui lui correspond
        # dans la partie gauche de la regle, les autres integrant la partie droite.

        # Calculate repartition of items on the right and left. In the table
        # where each index corresponds to an item (the first "iTailleFrequent" are the qualitative items
        # we will place the items having "true" value in their corresponding table cell 
        # in the right side of the ru;e, the rest going to the right side.
        tRepartitionItems = AprioriQuantitative.CalculerRepartitionItems(self.m_iIndiceRepartitionItems, self.m_iTailleFrequent+self.m_iNombreItemsQuantConsideres)

        if tRepartitionItems is None:
            if self.m_iNombreItemsQuantConsideres==0:
                self.m_iIndiceFrequent += 1
            else:
                self.m_iIndiceCombinaisonItemsQuant += 1
            self.m_iIndiceRepartitionItems = 0
            return
        else:

            # Construction du schema de la rule optimiser :
            regle = None
            iNombreItemsGauche = 0
            iNombreItemsDroite = 0
            iNombreItems = 0 # Number of items in the rule, qualitatifs and quantitatifs
            iIndiceAjoutGauche = 0
            iIndiceAjoutDroite = 0

            iNombreItems = self.m_iTailleFrequent + self.m_iNombreItemsQuantConsideres

            # On compte le nombre d'items qu'on va placer a gauche :
            # We count the number of items to be placed on the left:
            iNombreItemsGauche = 0
            iNombreItemsDroite = 0
            iIndiceItemRegle = 0
            while iIndiceItemRegle < iNombreItems:
                if tRepartitionItems[iIndiceItemRegle]:
                    iNombreItemsGauche += 1
                else:
                    iNombreItemsDroite += 1
                iIndiceItemRegle += 1

            #create a new rule template
            regle = AssociationRule(iNombreItemsGauche, iNombreItemsDroite, self.m_iNombreDisjonctionsGauche, self.m_iNombreDisjonctionsDroite)

            regle.AssignerNombreAssociationRules(self.__m_contexteResolution.m_parametresReglesQuantitatives.m_iNombreAssociationRules)

            iIndiceAjoutGauche = 0
            iIndiceAjoutDroite = 0

            # On specifie les items qualitatifs :
            # We specify all qualitative items:
            iIndiceItemRegle = 0
            while iIndiceItemRegle < self.m_iTailleFrequent:

                itemQual = itemSetFrequent.ObtenirItem(iIndiceItemRegle)
                if tRepartitionItems[iIndiceItemRegle]:
                    regle.AssignerItemGauche(itemQual, iIndiceAjoutGauche)
                    iIndiceAjoutGauche += 1
                else:
                    regle.AssignerItemDroite(itemQual, iIndiceAjoutDroite)
                    iIndiceAjoutDroite += 1

                iIndiceItemRegle += 1


            # On specifie les attributs quantitatifs :
            # We specify all quantitative items:
            if self.m_iNombreItemsQuantConsideres > 0:

                iIndiceAttributQuantAjoute = 0
                iIndiceAttributQuant = 0

                while iIndiceAttributQuant < self.m_iNombreTotalAttributsQuant:

                    if tCombinaisonItemsQuant[iIndiceAttributQuant]:

                        attributQuant = (self.__m_listeAttributsQuant[iIndiceAttributQuant])

                        if tRepartitionItems[self.m_iTailleFrequent + iIndiceAttributQuantAjoute]:
                            
                            itemQuant = ItemQuantitative(attributQuant, self.m_iNombreDisjonctionsGauche)
                            regle.AssignerItemGauche(itemQuant, iIndiceAjoutGauche)
                            iIndiceAjoutGauche += 1
                        else:
                            itemQuant = ItemQuantitative(attributQuant, self.m_iNombreDisjonctionsDroite)
                            regle.AssignerItemDroite(itemQuant, iIndiceAjoutDroite)
                            iIndiceAjoutDroite += 1

                        iIndiceAttributQuantAjoute += 1
                    iIndiceAttributQuant += 1

            
            if self.__m_contexteResolution.EstRegleValide(regle):
                print(".", end="")
                # print(regle)
                # In the rules accounting mode, there is nothing to optimize:
                # if in the mode of calculating max rule to test, simply increase m_iNombreReglesComptabilisees
                if self.__m_bModeSpecialComptabilisationRegles:
                    self.__m_iNombreReglesComptabilisees += 1

                # Otherwise, optimise the rule:
                else:
                    i = 0
                    while i<self.__m_contexteResolution.m_parametresReglesQuantitatives.m_iNombreAssociationRules:
                        if self.__m_optimiseurCourant.OptimiseRegle(regle, i):
                            if self.m_listeRegles is not None:
                                #We need to deep copy regle, or else the same regle shows up n times (since it's a shallow copy otherwise and everything would point to the same memory location / object)
                                regleAdd = AssociationRule(regle)

                                self.m_listeRegles.append(regleAdd)

                            # On indique qu'on vient de tester une nouvelle forme de regle :
                            # we indicate that we just tested a new form of rule:
                        i += 1

                    # print("NNNNNNNNNNNNNNNNN")
                    # if len(self.m_listeRegles) > RuleTester.lastPrintedRules:
                    #     print("------")
                    #     for rule in self.m_listeRegles:
                    #         print("Rule: " + str(rule.toString()))
                    #     RuleTester.lastPrintedRules = len(self.m_listeRegles)

                    # self.__m_contexteResolution.m_parametresReglesQuantitatives.m_applyKMeans = 1
                    #if apply k means indicated
                    if self.__m_contexteResolution.m_parametresReglesQuantitatives.m_applyKMeans >= 1:

                        #the rules for that particular association (the last added)
                        rulesOfAssociation = list(self.m_listeRegles[len(self.m_listeRegles) - self.__m_contexteResolution.m_parametresReglesQuantitatives.m_iNombreAssociationRules:len(self.m_listeRegles)])

                        if self.m_listeCentroids is not None:
                            if self.__m_contexteResolution.m_parametresReglesQuantitatives.m_applyKMeans == 1:
                                #Apply K-means
                                kMeans = KMeansClusterer(rulesOfAssociation, self.__m_contexteResolution.m_parametresReglesQuantitatives)
                                self.m_listeCentroids = kMeans.applyKMeansAlgo()
                            elif self.__m_contexteResolution.m_parametresReglesQuantitatives.m_applyKMeans == 2:
                                #Apply G-means
                                gMeans = GMeansClusterer(rulesOfAssociation, self.__m_contexteResolution.m_parametresReglesQuantitatives)
                                self.m_listeCentroids = gMeans.applyGMeansAlgo()



                        #Uncomment to test the rule proximities
                        #double avg = kMeans.testRuleProximities()

                    self.m_iNombreReglesTestees += 1
            self.m_iIndiceRepartitionItems += 1

    def ArreterExecution(self):
        self.m_bEnExecution = False



    def ObtenirRegleCalculee(self, iIndiceRegle):

        if self.m_listeRegles is not None:
            try:
                return (self.m_listeRegles[iIndiceRegle])
            except IndexOutOfBoundsException as e:
                return None
        else:
            return None


    def ObtenirCentroidCalculee(self, iIndiceRegle):
        if self.m_listeCentroids is not None:
            try:
                return (self.m_listeCentroids[iIndiceRegle])
            except IndexOutOfBoundsException as e:
                return None
        else:
            return None

    def ObtenirListOfCentroids(self):
        if self.m_listeCentroids is not None:
            return self.m_listeCentroids
        else:
            return None


    def ObtenirListeReglesOptimales(self):
        return self.m_listeRegles



    def EstResultatDisponible(self):
        return self.__m_bResultatDisponible

import sys
sys.path.append('C:\\Users\\aalsahee\\python_physical_model\\Saudi\\trace\\Traces\\qtm\\src\\')



# from apriori import *
# from database import *
# from geneticAlgorithm import *

# Tester class for the clutering methods 
class TesterClustering(object):


    @staticmethod
    def printOutRules(assocRules):
        i = 0
        while i<len(assocRules):

            # TODO: maybe initialize outside of the for loop, b/c that would be less expensive.
            ruleConsidered = assocRules[i]

            print(ruleConsidered.toString())

            i += 1

    #for a rule Quant [ _ , _] --> Qual
    @staticmethod
    def printOutLHVals(assocRules):

        print("Lower bound vals: ")
        #Get the min and max of intervals for quantitative LHS and/or RHS
        i = 0
        while i<len(assocRules):

            # TODO: maybe initialize outside of the for loop, b/c that would be less expensive.
            ruleConsidered = assocRules[i]

            item = None
            itemQual = None
            itemQuant = None
            iIndiceItem = 0
            intervalIndexCount = 0

            if ruleConsidered is None:
                print("rule considered is null")

            #left part of rule:

            item = ruleConsidered.ObtenirItemDroite(iIndiceItem)

            if item.m_iTypeItem == Item.ITEM_TYPE_QUANTITATIF:

                itemQuant = item

                # print(itemQuant.m_tBornes[0])


            i += 1


    #for a rule Quant [ _ , _] --> Qual
    @staticmethod
    def printOutRHVals(assocRules):

        print("Upper bound vals: ")

        #Get the min and max of intervals for quantitative LHS and/or RHS
        i = 0
        while i<len(assocRules):

            #maybe initialize outside of the for loop, b/c that would be less expensive.
            ruleConsidered = assocRules[i]

            item = None
            itemQual = None
            itemQuant = None
            iIndiceItem = 0
            intervalIndexCount = 0

            if ruleConsidered is None:
                print("rule considered is null")

            #left part of rule:

            item = ruleConsidered.ObtenirItemDroite(iIndiceItem)

            if item.m_iTypeItem == Item.ITEM_TYPE_QUANTITATIF:

                itemQuant = item

                # print(itemQuant.m_tBornes[1])


            i += 1


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
sys.path.append('C:\\Users\\aalsahee\\python_physical_model\\Saudi\\trace\\Traces\\qtm\\src\\')

from database.onefile import *
# from solver.onefile import *
# from solver.onefile import RuleOptimizer

class AprioriQuantitative(object):
    # Base class allowing the execution of a particular code during the generation of itemsets:
    class TraitementExternePendantCalcul(object):
        # Returns false if the external processing asks to stop the calculations:
        def ExecuterTraitementExterne(self):
            return True



    def __init__(self, contexteResolution):
        self.m_listeAttributsQual = None
        self.m_listeAttributsQuant = None
        self.m_tableItems = None
        self.m_listeListeItemSets = None
        self.m_gestionnaireBD = None
        self.__m_contexteResolution = None
        self.m_fMinSupp = 0.0
        self.m_iNombreTransactions = 0
        self.m_traitementExterne = None

        self.m_listeAttributsQual = []
        self.m_listeAttributsQuant = []
        self.m_tableItems = TableItems()
        self.m_listeListeItemSets = []
        self.m_fMinSupp = 0.0
        self.m_iNombreTransactions = 0
        self.m_traitementExterne = None

        self.__m_contexteResolution = contexteResolution
        if not self.__m_contexteResolution == None:
            self.m_gestionnaireBD = self.__m_contexteResolution.m_gestionnaireBD


    #    * specify external treatment
    #     * @param traitementExterne External Treatment For Calculating
    #     
    def SpecifierTraitementExterne(self, traitementExterne):
        self.m_traitementExterne = traitementExterne


    #    *
    #     * Run Pretreatment
    #     * @param bGenererItemSetsSingletons
    #     
    def ExecuterPretraitement(self, bGenererItemSetsSingletons):
        iNombreAttributsQual = 0
        iIndiceAttributQual = 0
        iNombreColonnes = 0
        iIndiceColonne = 0
        iTypePriseEnCompte = 0
        attributQual = None
        attributQuant = None
        colonneDonnees = None
        self.m_iNombreTransactions = self.m_gestionnaireBD.ObtenirNombreLignes() #obtain the number of lines

        iNombreColonnes = self.m_gestionnaireBD.ObtenirNombreColonnesPrisesEnCompte() #obtain the number of selected columns??

        iIndiceColonne = 0
        while iIndiceColonne < iNombreColonnes:

            colonneDonnees = self.m_gestionnaireBD.ObtenirColonneBDPriseEnCompte(iIndiceColonne)

            if colonneDonnees.m_iTypeValeurs == DatabaseAdmin.TYPE_VALEURS_COLONNE_ITEM: #add categorical attribute to categorical list
                '''
                iTypePriseEnCompte = self.__m_contexteResolution.ObtenirTypePrisEnCompteAttribut(colonneDonnees.m_sNomColonne)
                if not iTypePriseEnCompte == ResolutionContext.PRISE_EN_COMPTE_ITEM_NULLE_PART:
                    attributQual = AttributQualitative(colonneDonnees.m_sNomColonne, colonneDonnees)
                    self.m_listeAttributsQual.append(attributQual)
                '''
                attributQual = AttributQualitative(colonneDonnees.m_sNomColonne, colonneDonnees)
                self.m_listeAttributsQual.append(attributQual)

            elif colonneDonnees.m_iTypeValeurs == DatabaseAdmin.TYPE_VALEURS_COLONNE_REEL: #add quantitative attribute to categorical list
                iTypePriseEnCompte = self.__m_contexteResolution.ObtenirTypePrisEnCompteAttribut(colonneDonnees.m_sNomColonne)
                if not iTypePriseEnCompte == ResolutionContext.PRISE_EN_COMPTE_ITEM_NULLE_PART:
                    attributQuant = AttributQuantitative(colonneDonnees.m_sNomColonne, colonneDonnees)
                    self.m_listeAttributsQuant.append(attributQuant)

            iIndiceColonne += 1


        iNombreAttributsQual = len(self.m_listeAttributsQual)
        iIndiceAttributQual = 0
        iIndiceAttributQual = 0
        while iIndiceAttributQual < iNombreAttributsQual:

            attributQual = self.m_listeAttributsQual[iIndiceAttributQual]
            attributQual.GenererItems(self.m_tableItems)

            iIndiceAttributQual += 1


        if bGenererItemSetsSingletons:
            self.GenererNouvelleListeItemSets() #generate new itemset list


    #   *
    #    * Calculate Distribution Items
    #    * @param iIndiceRepartition Index Distribution
    #    * @param iNombreItems Number of Items
    #    * @return
    #    
    @staticmethod
    def CalculerRepartitionItems(iIndiceRepartition, iNombreItems):
        tRepartitionItems = None
        iIndiceItem = 0
        iIndiceMaxPourItem = 0
        iNombreItemsRestants = 0
        bTestPremierItem = True # Vrai tant qu'on peut contruire l'ensemble contenant tous les attributs, qu'il faut prendre garde d'�liminer

        if iNombreItems==0:
            return None

        tRepartitionItems = []
        for i in range(0, iNombreItems):
            tRepartitionItems.append(False)

        iNombreItemsRestants = iNombreItems
        iIndiceItem = 0
        bTestPremierItem = True
        while iIndiceItem<iNombreItems:

            iIndiceMaxPourItem = 1 << (iNombreItems - iIndiceItem - 1)

            if bTestPremierItem:
                iIndiceMaxPourItem -= 1

            if iIndiceRepartition==0:
                tRepartitionItems[iIndiceItem] = True
                iNombreItemsRestants -= 1
                iIndiceItem = iNombreItems # Pour provoquer la fin de l'algo

            elif iIndiceRepartition<iIndiceMaxPourItem:
                tRepartitionItems[iIndiceItem] = True
                iNombreItemsRestants -= 1
                iIndiceRepartition -= 1

            else:
                iIndiceRepartition -= iIndiceMaxPourItem
                bTestPremierItem = False

            iIndiceItem += 1

        if iNombreItemsRestants==iNombreItems:
            return None
        else:
            return tRepartitionItems



    # Compute all possible sets of items, each set consisting of 'iNumberPlaces' elements
    # (returns an array indicating whether or not the i-th item is present in the set):
    #    *
    #     * Calculate Sets Items
    #     * @param iIndiceRepartition Index Distribution
    #     * @param iNombreItems Number of items
    #     * @param iNombrePlaces Number of places
    #     
    @staticmethod
    def CalculerEnsemblesItems(iIndiceRepartition, iNombreItems, iNombrePlaces):
        tRepartitionItems = None
        bItemAffecte = False
        iIndiceItem = 0
        iNombreItemsRestants = 0
        iNombrePlacesRestantes = 0
        iCompteur = 0
        factN = 0 # Variables dedicated to the computation of the combinations of p values among n
        factP = 0
        factN_P = 0
        iCNP = 0

        if iNombreItems==0:
            return None

        tRepartitionItems = []
        for i in range(0, iNombreItems):
            tRepartitionItems.append(False)

        iIndiceItem = 0
        iNombreItemsRestants = iNombreItems
        iNombrePlacesRestantes = iNombrePlaces
        while (iNombrePlacesRestantes>0) and (iNombreItemsRestants>=iNombrePlacesRestantes) and (iIndiceItem<iNombreItems):

            if iNombreItemsRestants> iNombrePlacesRestantes:

                factN = factP = factN_P = 1

                iCompteur = 2
                while iCompteur<iNombreItemsRestants:
                    factN *= iCompteur
                    iCompteur += 1

                iCompteur = 2
                while iCompteur<iNombrePlacesRestantes:
                    factP *= iCompteur
                    iCompteur += 1

                iCompteur = 2
                while iCompteur<=(iNombreItemsRestants-iNombrePlacesRestantes):
                    factN_P *= iCompteur
                    iCompteur += 1

                iCNP = math.trunc(factN / float((factP * factN_P)))

            # Sinon cas iNombreItemsRestants == iNombrePlacesRestantes :
            else:
                iCNP = 1

            if iIndiceRepartition < iCNP:
                tRepartitionItems[iIndiceItem] = True
                iNombrePlacesRestantes -= 1
            else:
                iIndiceRepartition -= iCNP

            iIndiceItem += 1
            iNombreItemsRestants -= 1


        if iNombrePlacesRestantes==iNombrePlaces:
            return None
        else:
            return tRepartitionItems


    #    * set minimum support
    #     * @param fMinSupp Minimum Support value
    #     
    def SpecifierSupportMinimal(self, fMinSupp):
        self.m_fMinSupp = fMinSupp



    def ObtenirSupportMinimal(self):
        return self.m_fMinSupp


    #*Write Frequents List
    def EcrireListeFrequents(self):
        sTexteListeFrequents = None
        iTailleMaxItemSets = 0
        iIndiceListesItemSets = 0
        iNombreItemSets = 0
        iIndiceItemSet = 0
        listeItemSets = None
        itemset = None

        sTexteListeFrequents = ""

        iTailleMaxItemSets = len(self.m_listeListeItemSets)
        iIndiceListesItemSets = 0
        while iIndiceListesItemSets<iTailleMaxItemSets:
            # sTexteListeFrequents += "K"
            listeItemSets = self.m_listeListeItemSets[iIndiceListesItemSets]

            iNombreItemSets = len(listeItemSets)
            iIndiceItemSet = 0
            while iIndiceItemSet<iNombreItemSets:

                itemset = listeItemSets[iIndiceItemSet]

                if itemset.m_iSupport >= int((self.m_fMinSupp*float(self.m_iNombreTransactions))):
                    sTexteListeFrequents += itemset.EcrireItemSet(self.m_iNombreTransactions, True)
                    sTexteListeFrequents += "\n"

                iIndiceItemSet += 1

            if iNombreItemSets > 0:
                sTexteListeFrequents += "\n"
            iIndiceListesItemSets += 1

        return sTexteListeFrequents


    #    *
    #     * Remove Not Frequent Sets
    #     * @param iIndiceListe index of the ListItemSet
    #     
    def RetirerNonFrequentsDeListeItemSets(self, iIndiceListe):

        listeItemSets = None
        listeItemSetsTemp = None
        itemSet = None
        iIndiceItemSet = 0
        iNombreItemSets = 0

        listeItemSets = self.m_listeListeItemSets[iIndiceListe]
        listeItemSetsTemp = []
        iNombreItemSets = len(listeItemSets)

        iIndiceItemSet = 0
        while iIndiceItemSet<iNombreItemSets:

            itemSet = listeItemSets[iIndiceItemSet]

            # We keep only frequent itemSets:
            if itemSet.m_iSupport >= int((self.m_fMinSupp*float(self.m_iNombreTransactions))):
                listeItemSetsTemp.append(itemSet)

            iIndiceItemSet += 1

        # We replace the old list with the new one:
        self.m_listeListeItemSets[iIndiceListe] = listeItemSetsTemp

    # Remove all itemsets which do not satisfy the conditions given by the user
    # in the filter table:
    def ElaguerItemsetsSelonFiltre(self):
        listeItemSets = None
        listeItemSetsTemp = None
        itemSet = None
        iIndiceListeItemSets = 0
        iNombreListesItemSets = 0
        iIndiceItemSet = 0
        iNombreItemSets = 0

        iNombreListesItemSets = len(self.m_listeListeItemSets)
        iIndiceListeItemSets = 0
        while iIndiceListeItemSets<iNombreListesItemSets:

            listeItemSets = self.m_listeListeItemSets[iIndiceListeItemSets]
            listeItemSetsTemp = []
            iNombreItemSets = len(listeItemSets)

            iIndiceItemSet = 0
            while iIndiceItemSet<iNombreItemSets:

                itemSet = listeItemSets[iIndiceItemSet]
                if not itemSet == None:
                    if self.__m_contexteResolution.EstItemSetValide(itemSet):
                        listeItemSetsTemp.append(itemSet)

                iIndiceItemSet += 1

            # We replace the old list with the new one:
            if len(listeItemSetsTemp) > 0:
                self.m_listeListeItemSets[iIndiceListeItemSets] = listeItemSetsTemp
            
            iIndiceListeItemSets += 1


    #*Generate new item sets
    def GenererNouvelleListeItemSets(self):

        nouvelleListe = None
        precedenteListe = None
        iSupportItem = 0
        iIndiceListe = 0
        iNombreAttributsQual = 0
        iIndiceAttributQual = 0
        itemSet = None
        item = None
        attributQual = None

        iIndiceListe = len(self.m_listeListeItemSets)
        iNombreAttributsQual = len(self.m_listeAttributsQual)


        # We reset the count pointers of the itemsets, which put in relation
        # any value of an attribute with the set of itemsets that contained it:
        iIndiceAttributQual = 0
        while iIndiceAttributQual < iNombreAttributsQual:
            attributQual = self.m_listeAttributsQual[iIndiceAttributQual]
            attributQual.ReinitialiserListeLiensItemSets()
            iIndiceAttributQual += 1


        nouvelleListe = []

        # Itemsets of size 1:
        if iIndiceListe == 0:
            item = self.m_tableItems.ObtenirPremierItem()
            while not item == None:

                if not self.__m_contexteResolution.ObtenirTypePrisEnCompteItem(item.m_attributQual.m_sNomAttribut, item.ObtenirIdentifiantTexteItem()) == ResolutionContext.PRISE_EN_COMPTE_ITEM_NULLE_PART:

                    itemSet = ItemSet(1)
                    itemSet.SpecifierItem(item)

                    iSupportItem = item.m_attributQual.ObtenirSupportItem(item.m_iIndiceValeur)

                    itemSet.SpecifierSupport(iSupportItem)
                    item.m_attributQual.AjouterLienVersItemSet(item.m_iIndiceValeur, itemSet)

                    nouvelleListe.append(itemSet)

                item = (item.m_itemSuivant)



        # Combinations of items:
        else:
            iIndiceParcours1 = 0
            iIndiceParcours2 = 0
            iNombreItemSets = 0
            iTailleNouveauxItemSets = 0
            iNombreItemsIdentiques = 0
            iIndiceItem = 0
            bContinuerParcours = False
            itemSet1 = None
            itemSet2 = None

            bContinuerParcours = True


            # We purify the list of (K-1) -itemSets from those which are not frequent:
            self.RetirerNonFrequentsDeListeItemSets(iIndiceListe-1)


            # We generate the list of K-itemSets from the previous one containing the frequent (K-1) -itemSets:
            precedenteListe = self.m_listeListeItemSets[iIndiceListe-1]
            iNombreItemSets = len(precedenteListe)
            iTailleNouveauxItemSets = iIndiceListe + 1
            iNombreItemsIdentiques = iIndiceListe - 1

            iIndiceParcours1=0
            while bContinuerParcours and (iIndiceParcours1<iNombreItemSets):

                itemSet1 = precedenteListe[iIndiceParcours1]

                iIndiceParcours2 = iIndiceParcours1+1
                while iIndiceParcours2<iNombreItemSets:

                    itemSet2 = precedenteListe[iIndiceParcours2]

                    if itemSet1.EstGenerateurCandidatAvec(itemSet2):

                        # We must also check that the last 2 items (those which are different
                        # of each other) do not match values from a
                        # same attribute of the database (the values of the same attribute are exclusive).
                        # It is not useful to compare them to common items
                        # since by "recursion" the (K-1) -itemSet are
                        # already made up of items responding to this imperative.
                        if not itemSet1.m_listeItems[iNombreItemsIdentiques].m_attributQual.equals(itemSet2.m_listeItems[iNombreItemsIdentiques].m_attributQual):
                            itemSet = ItemSet(iTailleNouveauxItemSets)

                            # The new itemSet is made up of the first k-2 items common to both
                            # (K-1) -itemSets generators ...:
                            iIndiceItem = 0
                            while iIndiceItem<iNombreItemsIdentiques:
                                item = itemSet1.m_listeItems[iIndiceItem]
                                itemSet.SpecifierItem(item)
                                item.m_attributQual.AjouterLienVersItemSet(item.m_iIndiceValeur, itemSet)
                                iIndiceItem += 1

                            # ... to which we add the two items which are not in common:
                            item = itemSet1.m_listeItems[iNombreItemsIdentiques]
                            itemSet.SpecifierItem(item)
                            item.m_attributQual.AjouterLienVersItemSet(item.m_iIndiceValeur, itemSet)

                            item = itemSet2.m_listeItems[iNombreItemsIdentiques]
                            itemSet.SpecifierItem(item)
                            item.m_attributQual.AjouterLienVersItemSet(item.m_iIndiceValeur, itemSet)

                            itemSet.SpecifierSupport(0)

                            nouvelleListe.append(itemSet)

                    iIndiceParcours2 += 1

                iIndiceParcours1 += 1
                if not self.m_traitementExterne == None:
                    bContinuerParcours = self.m_traitementExterne.ExecuterTraitementExterne()

            # We perform a new reading pass of the BD in order to calculate the new supports:
            iIndiceTransaction = 0
            iNombreTransactions = 0

            iNombreAttributsQual = len(self.m_listeAttributsQual)
            iIndiceAttributQual = 0
            attributQual = None

            # Read line by line ...
            iNombreTransactions = self.m_gestionnaireBD.ObtenirNombreLignes()
            iIndiceTransaction = 0

            if bContinuerParcours:
                iIndiceTransaction = 0
                while iIndiceTransaction<iNombreTransactions:

                    # ... then attribute by attribute:
                    iIndiceAttributQual = 0
                    while iIndiceAttributQual<iNombreAttributsQual:

                        attributQual = self.m_listeAttributsQual[iIndiceAttributQual]
                        if not attributQual == None:
                            attributQual.ComptabiliserOcurrenceValeur(iIndiceTransaction, attributQual.m_colonneDonnees.m_tIDQualitatif[iIndiceTransaction])

                        iIndiceAttributQual += 1

                    iIndiceTransaction += 1



        if len(nouvelleListe) > 0:
            self.m_listeListeItemSets.append(nouvelleListe)
            return True
        else:
            return False

    #   *
    #    * Frequent recover 
    #    * @param iTailleFrequent Frequent size
    #    * @param iIndiceFrequent Frequent index
    #    * @return an Item Set
    #    
    def RecupererFrequent(self, iTailleFrequent, iIndiceFrequent):
        iDimensionMax = 0
        iNombreFrequents = 0
        listeItemSets = None

        iDimensionMax = len(self.m_listeListeItemSets)
        if (iTailleFrequent<=0) or (iTailleFrequent> iDimensionMax):
            return None

        listeItemSets = self.m_listeListeItemSets[(iTailleFrequent-1)]

        iNombreFrequents = len(listeItemSets)
        if (iIndiceFrequent<0) or (iIndiceFrequent>=iNombreFrequents):
            return None

        return listeItemSets[iIndiceFrequent]



    #   Search among the list of frequent the itemset containing the items passed in parameter:
    #   *
    #    * Search through the list of the frquents itemset containing items in passs paramtre
    #    * @param items An array of Qualitative item
    #    
    def RechercherFrequent(self, items):
        iTailleFrequent = 0
        iDimensionMax = 0
        listeItemSets = None
        itemSet = None
        bItemSetTrouve = False
        iNombreItemSets = 0
        iIndiceItemSet = 0
        item = None
        iIndiceItem = 0
        bItemTrouveDansItemSet = False
        iIndiceItemDansItemSet = 0

        iTailleFrequent = len(items)
        iDimensionMax = len(self.m_listeListeItemSets)
        if (iTailleFrequent<=0) or (iTailleFrequent> iDimensionMax):
            return None

        listeItemSets = self.m_listeListeItemSets[(iTailleFrequent-1)]

        iNombreItemSets = len(listeItemSets)
        iIndiceItemSet = 0
        itemSet = None
        bItemSetTrouve = False
        while ((not bItemSetTrouve)) and (iIndiceItemSet<iNombreItemSets):
            itemSet = listeItemSets[iIndiceItemSet]

            # We check if each item is present in the itemset:
            iIndiceItem = 0
            bItemSetTrouve = True
            while (bItemSetTrouve) and (iIndiceItem<iTailleFrequent):
                item = items[iIndiceItem]

                # We search for the presence of the item in the itemset:
                bItemTrouveDansItemSet = False
                iIndiceItemDansItemSet = 0
                while ((not bItemTrouveDansItemSet)) and (iIndiceItemDansItemSet<iTailleFrequent):
                    bItemTrouveDansItemSet = item.equals(itemSet.m_listeItems[iIndiceItemDansItemSet])
                    iIndiceItemDansItemSet += 1

                bItemSetTrouve = bItemTrouveDansItemSet
                iIndiceItem += 1

            iIndiceItemSet += 1

        if bItemSetTrouve:
            return itemSet
        else:
            return None


    #    *
    #     * Obtain quantitative attributes
    #     * @param iIndiceQuant Index of the quantitative attribute
    #     * @return Quantitative attribute
    #     
    def ObtenirAttributQuantitatif(self, iIndiceQuant):
        if (iIndiceQuant>=0) and (iIndiceQuant<len(self.m_listeAttributsQuant)):
            return self.m_listeAttributsQuant[iIndiceQuant]
        else:
            return None



    def ObtenirNombreAttributsQuantitatifs(self):
        if self.m_listeAttributsQuant == None:
            return 0
        else:
            return len(self.m_listeAttributsQuant)


    #    *
    #     * Obtaining quantitative attributes by Name
    #     * @param sNomAttributQuant
    #     * @return quantitative attribute
    #     
    def ObtenirAttributQuantitatifDepuisNom(self, sNomAttributQuant):
        attribut = None
        iNombreAttributsQuant = 0
        iIndiceAttributQuant = 0

        if sNomAttributQuant == None:
            return None

        iNombreAttributsQuant = len(self.m_listeAttributsQuant)

        attribut = None
        iIndiceAttributQuant = 0
        while (attribut == None) and (iIndiceAttributQuant<iNombreAttributsQuant):
            attribut = self.m_listeAttributsQuant[iIndiceAttributQuant]
            if not attribut == None:
                if not sNomAttributQuant == attribut.ObtenirNom():
                    attribut = None
            iIndiceAttributQuant += 1

        return attribut


    #    *
    #     * Get Attribute From Name Qualitative
    #     * @param sNomAttributQual Name of Quanlitative Attribute
    #     * @return Qualitative attribute
    #     
    def ObtenirAttributQualitatifDepuisNom(self, sNomAttributQual):
        attribut = None
        iNombreAttributsQual = 0
        iIndiceAttributQual = 0

        if sNomAttributQual == None:
            return None

        iNombreAttributsQual = len(self.m_listeAttributsQual)

        attribut = None
        iIndiceAttributQual = 0
        while (attribut == None) and (iIndiceAttributQual<iNombreAttributsQual):
            attribut = self.m_listeAttributsQual[iIndiceAttributQual]
            if not attribut == None:
                if not sNomAttributQual == attribut.ObtenirNom():
                    attribut = None
            iIndiceAttributQual += 1

        return attribut


    #    *
    #     * Return Qualitative Item from AttributQualitatif
    #     * @param attribut Quanlitative Attribute
    #     * @param iIndiceValeur Index
    #     * @return Qualitative Item
    #     
    def ObtenirItem(self, attribut, iIndiceValeur):
        item = None
        bItemTrouve = False

        bItemTrouve = False
        item = self.m_tableItems.ObtenirPremierItem()
        while ((not bItemTrouve)) and (not item == None):

            # We test the equality of the attribute then that of the item itself:
            if item.m_attributQual == attribut:
                bItemTrouve = (item.m_iIndiceValeur == iIndiceValeur)

            if not bItemTrouve:
                item = (item.m_itemSuivant)

        return item

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


class AssociationRule(object):
    def _initialize_instance_fields(self):
        self.m_tItemsGauche = None
        self.m_tItemsDroite = None
        self.m_iNombreItemsGauche = 0
        self.m_iNombreItemsDroite = 0
        self.m_iOccurrences = 0
        self.m_fSupport = 0.0
        self.m_fConfiance = 0.0
        self.m_iOccurrencesGauche = 0
        self.m_iOccurrencesDroite = 0
        self.m_iOccurrences_Gauche_NonDroite = 0
        self.m_iOccurrences_NonGauche_Droite = 0
        self.m_iOccurrences_NonGauche_NonDroite = 0
        self.m_iNombreDisjonctionsGauche = 0
        self.m_iNombreDisjonctionsDroite = 0
        self.m_iNombreDisjonctionsGaucheValides = 0
        self.m_iNombreDisjonctionsDroiteValides = 0
        self.m_iNombreAssociationRules = 1
        self.m_applyKMeans = 0


    def __init__(self, *args):
        if len(args) >= 4:
            iNombreItemsGauche = args[0] 
            iNombreItemsDroite = args[1]
            iNombreDisjonctionsGauche = args[2]
            iNombreDisjonctionsDroite = args[3]

            self._initialize_instance_fields()

            if (iNombreItemsGauche <= 0) or (iNombreItemsDroite <= 0):
                self.m_iNombreItemsGauche = 0
                self.m_iNombreItemsDroite = 0
                self.m_tItemsGauche = None
                self.m_tItemsDroite = None
                self.m_iNombreDisjonctionsGauche = 0
                self.m_iNombreDisjonctionsDroite = 0
            else:
                self.m_iNombreItemsGauche = iNombreItemsGauche
                self.m_iNombreItemsDroite = iNombreItemsDroite
                self.m_tItemsGauche = []
                for i in range(0, self.m_iNombreItemsGauche):
                    self.m_tItemsGauche.append(None)
                self.m_tItemsDroite = []
                for i in range(0, self.m_iNombreItemsDroite):
                    self.m_tItemsDroite.append(None)
                self.m_iNombreDisjonctionsGauche = iNombreDisjonctionsGauche
                self.m_iNombreDisjonctionsDroite = iNombreDisjonctionsDroite
    
            self.m_iNombreDisjonctionsGaucheValides = self.m_iNombreDisjonctionsGauche
            self.m_iNombreDisjonctionsDroiteValides = self.m_iNombreDisjonctionsDroite
    
            self.m_iOccurrences = 0
            self.m_fSupport = 0.0
            self.m_fConfiance = 0.0
            self.m_iOccurrencesGauche = 0
            self.m_iOccurrencesDroite = 0
            self.m_iOccurrences_Gauche_NonDroite = 0
            self.m_iOccurrences_NonGauche_Droite = 0
            self.m_iOccurrences_NonGauche_NonDroite = 0

        else:
            regle = args[0]

            self._initialize_instance_fields()
            self.CopierRegleAssociation(regle)




    # Copy construct:
    def CopierRegleAssociation(self, regle):

        iIndiceItem = 0
        item = None

        if not regle == None:

            self.m_iNombreItemsGauche = regle.m_iNombreItemsGauche
            self.m_iNombreItemsDroite = regle.m_iNombreItemsDroite

            self.m_tItemsGauche = [None for _ in range(self.m_iNombreItemsGauche)]
            self.m_tItemsDroite = [None for _ in range(self.m_iNombreItemsDroite)]

            # Copie des items de la partie gauche :
            iIndiceItem = 0
            while iIndiceItem < self.m_iNombreItemsGauche:
                item = regle.m_tItemsGauche[iIndiceItem]
                # item = self.m_tItemsGauche[iIndiceItem]
                if item.m_iTypeItem == Item.ITEM_TYPE_QUANTITATIF:
                    self.m_tItemsGauche[iIndiceItem] = ItemQuantitative(item)
                else:
                    self.m_tItemsGauche[iIndiceItem] = item
                iIndiceItem += 1

            iIndiceItem = 0
            while iIndiceItem<self.m_iNombreItemsDroite:
                item = regle.m_tItemsDroite[iIndiceItem]
                if item.m_iTypeItem == Item.ITEM_TYPE_QUANTITATIF:
                    self.m_tItemsDroite[iIndiceItem] = ItemQuantitative(item)
                else:
                    self.m_tItemsDroite[iIndiceItem] = item
                iIndiceItem += 1

            self.m_iOccurrences = regle.m_iOccurrences
            self.m_fSupport = regle.m_fSupport
            self.m_fConfiance = regle.m_fConfiance
            self.m_iOccurrencesGauche = regle.m_iOccurrencesGauche
            self.m_iOccurrencesDroite = regle.m_iOccurrencesDroite
            self.m_iOccurrences_Gauche_NonDroite = regle.m_iOccurrences_Gauche_NonDroite
            self.m_iOccurrences_NonGauche_Droite = regle.m_iOccurrences_NonGauche_Droite
            self.m_iOccurrences_NonGauche_NonDroite = regle.m_iOccurrences_NonGauche_NonDroite
            self.m_iNombreDisjonctionsGauche = regle.m_iNombreDisjonctionsGauche
            self.m_iNombreDisjonctionsDroite = regle.m_iNombreDisjonctionsDroite
            self.m_iNombreDisjonctionsGaucheValides = regle.m_iNombreDisjonctionsGaucheValides
            self.m_iNombreDisjonctionsDroiteValides = regle.m_iNombreDisjonctionsDroiteValides

            #Added parameters for k-means algorithm
            self.m_iNombreAssociationRules = regle.m_iNombreAssociationRules
            self.m_applyKMeans = regle.m_applyKMeans
        else:

            self.m_iNombreItemsGauche = 0
            self.m_iNombreItemsDroite = 0
            self.m_tItemsGauche = None
            self.m_tItemsDroite = None
            self.m_iOccurrences = 0
            self.m_fSupport = 0.0
            self.m_fConfiance = 0.0
            self.m_iOccurrencesGauche = 0
            self.m_iOccurrencesDroite = 0
            self.m_iOccurrences_Gauche_NonDroite = 0
            self.m_iOccurrences_NonGauche_Droite = 0
            self.m_iOccurrences_NonGauche_NonDroite = 0
            self.m_iNombreDisjonctionsGauche = 0
            self.m_iNombreDisjonctionsDroite = 0
            self.m_iNombreDisjonctionsGaucheValides = 0
            self.m_iNombreDisjonctionsDroiteValides = 0

            self.m_iNombreAssociationRules = 1
            self.m_applyKMeans = 0

    # Class allowing comparison of rules according to confidence value
    # class ComparateurRegles(Comparator):
    class ComparateurRegles:
        def __init__(self, bTriDecroissant):
            self.m_bTriDecroissant = False
            self.m_bTriDecroissant = bTriDecroissant


        def compare(self, o1, o2):
            iResultatComparaison = 0
            iResultatComparaison = self.CompareRegles(o1, o2)

            if self.m_bTriDecroissant:
                iResultatComparaison = -iResultatComparaison

            return iResultatComparaison


        def CompareRegles(self, regle1, regle2):
            pass


        def equals(self, obj):
            return (self.compare(self, obj) == 0)


    #    *comparing RULES on the value of Confidence
    #     
    class ComparateurConfiance(ComparateurRegles):

        def __init__(self, bTriDecroissant):
            super().__init__(bTriDecroissant)

        def CompareRegles(self, regle1, regle2):
            if regle1.m_fConfiance > regle2.m_fConfiance:
                return 1
            elif regle1.m_fConfiance < regle2.m_fConfiance:
                return -1
            else:
                if regle1.m_iOccurrences > regle2.m_iOccurrences:
                    return 1
                elif regle1.m_iOccurrences < regle2.m_iOccurrences:
                    return -1
                else:
                    return 0



    #    *comparing RULES on the value of support
    #     
    class ComparateurSupport(ComparateurRegles):

        def __init__(self, bTriDecroissant):
            super().__init__(bTriDecroissant)

        def CompareRegles(self, regle1, regle2):
            if regle1.m_iOccurrences > regle2.m_iOccurrences:
                return 1
            elif regle1.m_iOccurrences < regle2.m_iOccurrences:
                return -1
            else:
                if regle1.m_fConfiance > regle2.m_fConfiance:
                    return 1
                elif regle1.m_fConfiance < regle2.m_fConfiance:
                    return -1
                else:
                    return 0



    #    *Class for comparing RULES depending on the number of attributes it contains
    #     
    class ComparateurNombreAttributs(ComparateurRegles):

        def __init__(self, bTriDecroissant):
            super().__init__(bTriDecroissant)

        def CompareRegles(self, regle1, regle2):
            iNombreItemsRegle1 = 0
            iNombreItemsRegle2 = 0

            iNombreItemsRegle1 = regle1.m_iNombreItemsGauche + regle1.m_iNombreItemsDroite
            iNombreItemsRegle2 = regle2.m_iNombreItemsGauche + regle2.m_iNombreItemsDroite

            if iNombreItemsRegle1 > iNombreItemsRegle2:
                return 1
            elif iNombreItemsRegle1 < iNombreItemsRegle2:
                return -1
            else:
                if regle1.m_iNombreItemsGauche > regle2.m_iNombreItemsGauche:
                    return 1
                elif regle1.m_iNombreItemsGauche < regle2.m_iNombreItemsGauche:
                    return -1
                else:
                    if regle1.m_fConfiance > regle2.m_fConfiance:
                        return 1
                    elif regle1.m_fConfiance < regle2.m_fConfiance:
                        return -1
                    else:
                        if regle1.m_iOccurrences > regle2.m_iOccurrences:
                            return 1
                        elif regle1.m_iOccurrences < regle2.m_iOccurrences:
                            return -1
                        else:
                            return 0



    # Comparator generators:
    @staticmethod
    def ObtenirComparateurConfiance(bTriDecroissant):
        return ComparateurConfiance(bTriDecroissant)
    @staticmethod
    def ObtenirComparateurSupport(bTriDecroissant):
        return ComparateurSupport(bTriDecroissant)
    @staticmethod
    def ObtenirComparateurNombreAttributs(bTriDecroissant):
        return ComparateurNombreAttributs(bTriDecroissant)


    #    *Assign Left Item 
    #     * @param item
    #     * @param iPosition
    #     
    def AssignerItemGauche(self, item, iPosition):
        if (iPosition < self.m_iNombreItemsGauche) and (not item == None):
            self.m_tItemsGauche[iPosition] = item


    #    *
    #     * Assign Right Item
    #     * @param item
    #     * @param iPosition
    #     
    def AssignerItemDroite(self, item, iPosition):
        if (iPosition < self.m_iNombreItemsDroite) and (not item == None):
            self.m_tItemsDroite[iPosition] = item



    def AssignerNombreOccurrences(self, iOccurrences):
        self.m_iOccurrences = iOccurrences



    def AssignerSupport(self, fSupport):
        self.m_fSupport = fSupport



    def AssignerConfiance(self, fConfiance):
        self.m_fConfiance = fConfiance

    #Assign m_iNombreAssociationRules, the number of top rules per association
    def AssignerNombreAssociationRules(self, iNumAssociationRules):
        self.m_iNombreAssociationRules = iNumAssociationRules

    #Assign m_applyKMeans, metric of if clustering algorithm should be applied
    #0 = no; 1 = yes (k-means); 2 yes (g-means)
    def AssignerApplyKMeans(self, applyKMeans):
        self.m_applyKMeans = applyKMeans



    #    *
    #     * Get left item
    #     * @param iPosition
    #     * @return Item
    #     
    def ObtenirItemGauche(self, iPosition):
        if iPosition < self.m_iNombreItemsGauche:
            return self.m_tItemsGauche[iPosition]
        else:
            return None


    #    *
    #     * Get right item
    #     * @param iPosition
    #     * @return item
    #     
    def ObtenirItemDroite(self, iPosition):
        if iPosition < self.m_iNombreItemsDroite:
            return self.m_tItemsDroite[iPosition]
        else:
            return None


    #    *Compute the number of items of a specific type on the left
    #     * @param iTypeItem
    #     * @return int
    #     
    def CompterItemsGaucheSelonType(self, iTypeItem):
        iPosition = 0
        iCompteur = 0

        iCompteur = 0
        iPosition = 0
        while iPosition < self.m_iNombreItemsGauche:
            if self.m_tItemsGauche[iPosition].m_iTypeItem == iTypeItem:
                iCompteur += 1
            iPosition += 1

        return iCompteur


    #    *Compute the number of items of a specific type on the right
    #     * 
    #     * @param iTypeItem
    #     * @return int
    #     
    def CompterItemsDroiteSelonType(self, iTypeItem):
        iPosition = 0
        iCompteur = 0

        iCompteur = 0
        iPosition = 0
        while iPosition<self.m_iNombreItemsDroite:
            if self.m_tItemsDroite[iPosition].m_iTypeItem == iTypeItem:
                iCompteur += 1
            iPosition += 1

        return iCompteur



    def EvaluerSiQualitative(self, contexteResolution):
        itemsGauche = None
        itemsTotaux = None
        iIndiceItem = 0
        item = None
        iIndiceAjoutItemGauche = 0
        iIndiceAjoutItemTotaux = 0
        itemSetGauche = None
        itemSetTotal = None
        apriori = None

        if contexteResolution == None:
            return

        apriori = contexteResolution.m_aprioriCourant
        if apriori == None:
            return

        itemsGauche = [None for _ in range(self.m_iNombreItemsGauche)]
        itemsTotaux = [None for _ in range(self.m_iNombreItemsGauche+self.m_iNombreItemsDroite)]
        iIndiceAjoutItemGauche = 0
        iIndiceAjoutItemTotaux = 0

        # On r�pertorie tous les items qualitatifs de gauche :
        iIndiceItem = 0
        while iIndiceItem<self.m_iNombreItemsGauche:
            item = self.m_tItemsGauche[iIndiceItem]
            if item.m_iTypeItem == Item.ITEM_TYPE_QUALITATIF:
                itemsGauche[iIndiceAjoutItemGauche] = item
                itemsTotaux[iIndiceAjoutItemTotaux] = item
                iIndiceAjoutItemGauche += 1
                iIndiceAjoutItemTotaux += 1
            else:
                return
            iIndiceItem += 1

        # On r�pertorie tous les items qualitatifs de droite :
        iIndiceItem = 0
        while iIndiceItem<self.m_iNombreItemsDroite:
            item = self.m_tItemsDroite[iIndiceItem]
            if item.m_iTypeItem == Item.ITEM_TYPE_QUALITATIF:
                itemsTotaux[iIndiceAjoutItemTotaux] = item
                iIndiceAjoutItemTotaux += 1
            else:
                return
            iIndiceItem += 1


        if (not iIndiceAjoutItemGauche == self.m_iNombreItemsGauche) or (not iIndiceAjoutItemTotaux == (self.m_iNombreItemsGauche+self.m_iNombreItemsDroite)):
            return

        # Evaluation des valeurs statistiques de la r�gle :
        itemSetTotal = apriori.RechercherFrequent(itemsTotaux)
        if not itemSetTotal == None:

            # Evaluation du support de la r�gle :
            self.m_iOccurrences = itemSetTotal.m_iSupport
            self.m_fSupport = (float(self.m_iOccurrences)) / (float(contexteResolution.m_gestionnaireBD.ObtenirNombreLignes()))

            # Evaluation de la confiance de la r�gle :
            itemSetGauche = apriori.RechercherFrequent(itemsGauche)
            if (not itemSetGauche == None) and (itemSetGauche.m_iSupport > 0):
                self.m_fConfiance = self.m_iOccurrences / (float(itemSetGauche.m_iSupport))

    def leftToString(self):
        sRegle = None
        iIndiceItem = 0
        item = None
        bItemsQualitatifsPresents = False
        bPremierItemInscrit = False
        iIndiceDisjonction = 0
        iNombreDisjonctions = 0
        iNombreItemsQuantitatifs = 0
        iNombreItems = 0
        tItemsRegle = None
        sRegle = str("")

        iNombreItems = self.m_iNombreItemsGauche #number of items on left
        tItemsRegle = self.m_tItemsGauche #the left items
        iNombreItemsQuantitatifs = self.CompterItemsGaucheSelonType(Item.ITEM_TYPE_QUANTITATIF)
        iNombreDisjonctions = self.m_iNombreDisjonctionsGaucheValides

        #Firstly, write the qualitative items. if more than one exist, concatenate with AND
        bPremierItemInscrit = False
        iIndiceItem = 0
        while iIndiceItem < iNombreItems:
            item = tItemsRegle[iIndiceItem]
            if item.m_iTypeItem == Item.ITEM_TYPE_QUALITATIF:
                if bPremierItemInscrit:
                    sRegle += "  AND  " # "  ET  "
                sRegle += (item).toString()
                bPremierItemInscrit = True
            iIndiceItem += 1
        bItemsQualitatifsPresents = bPremierItemInscrit #if has qualitative item

        #Next, display quantitative items:
        if iNombreItemsQuantitatifs > 0:
            if bItemsQualitatifsPresents:
                sRegle += "  AND  "
                if iNombreDisjonctions > 1:
                    sRegle += "( "

            iIndiceDisjonction = 0
            while iIndiceDisjonction < iNombreDisjonctions:

                if iIndiceDisjonction > 0:
                    sRegle += "  OR  " #OU

                if (iNombreItemsQuantitatifs > 1) and (iNombreDisjonctions > 1):
                    sRegle += "( "

                bPremierItemInscrit = False
                iIndiceItem = 0
                while iIndiceItem < iNombreItems:
                    item = tItemsRegle[iIndiceItem]
                    if item.m_iTypeItem == Item.ITEM_TYPE_QUANTITATIF:
                        if bPremierItemInscrit:
                            sRegle += "  AND  " #ET
                        sRegle += (item).toString(iIndiceDisjonction)
                        bPremierItemInscrit = True
                    iIndiceItem += 1

                if (iNombreItemsQuantitatifs > 1) and (iNombreDisjonctions > 1):
                    sRegle += " )"
                iIndiceDisjonction += 1

            if (bItemsQualitatifsPresents) and (iNombreDisjonctions > 1):
                sRegle += " ) "

        return sRegle

    def leftQualiToArray(self):
        # TODO Auto-generated method stub
        iIndiceItem = 0
        item = None
        iNombreItems = 0 #number of items on the left
        tItemsRegle = None #the left items
        array = []

        iNombreItems = self.m_iNombreItemsGauche #number of items on left
        tItemsRegle = self.m_tItemsGauche #the left items

        #Firstly, write the qualitative items. if more than one exist, concatenate with AND
        iIndiceItem = 0
        while iIndiceItem < iNombreItems:
            item = tItemsRegle[iIndiceItem]
            if item.m_iTypeItem == Item.ITEM_TYPE_QUALITATIF:
                array.append((item).getAttributeNameValue())
            iIndiceItem += 1
        return array

    def leftQuantiToArray(self):
        # TODO Auto-generated method stub
        iIndiceItem = 0
        item = None
        iIndiceDisjonction = 0 #which or
        iNombreDisjonctions = 0 #number of ORs
        iNombreItemsQuantitatifs = 0 #number of Quantitatives
        iNombreItems = 0 #number of items on the left
        tItemsRegle = None #the left items

        iNombreItems = self.m_iNombreItemsGauche #number of items on left
        tItemsRegle = self.m_tItemsGauche #the left items
        iNombreItemsQuantitatifs = self.CompterItemsGaucheSelonType(Item.ITEM_TYPE_QUANTITATIF)
        iNombreDisjonctions = self.m_iNombreDisjonctionsGaucheValides

        if iNombreItemsQuantitatifs == 0:
            return None

        array = []

        iIndiceDisjonction = 0
        while iIndiceDisjonction < iNombreDisjonctions:

            temp = []
            iIndiceItem = 0
            while iIndiceItem < iNombreItems:
                item = tItemsRegle[iIndiceItem]
                if item.m_iTypeItem == Item.ITEM_TYPE_QUANTITATIF:
                    temp.append((item).getAttributeNameBoundary(iIndiceDisjonction))
                iIndiceItem += 1

            array.append(temp)

            iIndiceDisjonction += 1

        return array

    def rightToString(self):
        # TODO Auto-generated method stub
        sRegle = None
        iIndiceItem = 0
        item = None
        bItemsQualitatifsPresents = False
        bPremierItemInscrit = False
        iIndiceDisjonction = 0
        iNombreDisjonctions = 0
        iNombreItemsQuantitatifs = 0
        iNombreItems = 0
        tItemsRegle = None
        sRegle = str("")

        iNombreItems = self.m_iNombreItemsDroite
        tItemsRegle = self.m_tItemsDroite
        iNombreItemsQuantitatifs = self.CompterItemsDroiteSelonType(Item.ITEM_TYPE_QUANTITATIF)
        iNombreDisjonctions = self.m_iNombreDisjonctionsDroiteValides

        #Firstly, write the qualitative items. if more than one exist, concatenate with AND
        bPremierItemInscrit = False
        iIndiceItem = 0
        while iIndiceItem < iNombreItems:
            item = tItemsRegle[iIndiceItem]
            if item.m_iTypeItem == Item.ITEM_TYPE_QUALITATIF:
                if bPremierItemInscrit:
                    sRegle += "  AND  " # "  ET  "
                sRegle += (item).toString()
                bPremierItemInscrit = True
            iIndiceItem += 1
        bItemsQualitatifsPresents = bPremierItemInscrit #if has qualitative item

        #Next, display quantitative items:
        if iNombreItemsQuantitatifs > 0:
            if bItemsQualitatifsPresents:
                sRegle += "  AND  "
                if iNombreDisjonctions > 1:
                    sRegle += "( "

            iIndiceDisjonction = 0
            while iIndiceDisjonction < iNombreDisjonctions:

                if iIndiceDisjonction > 0:
                    sRegle += "  OR  " #OU

                if (iNombreItemsQuantitatifs > 1) and (iNombreDisjonctions > 1):
                    sRegle += "( "

                bPremierItemInscrit = False
                iIndiceItem = 0
                while iIndiceItem < iNombreItems:
                    item = tItemsRegle[iIndiceItem]
                    if item.m_iTypeItem == Item.ITEM_TYPE_QUANTITATIF:
                        if bPremierItemInscrit:
                            sRegle += "  AND  " #ET
                        sRegle += (item).toString(iIndiceDisjonction)
                        bPremierItemInscrit = True
                    iIndiceItem += 1

                if (iNombreItemsQuantitatifs > 1) and (iNombreDisjonctions > 1):
                    sRegle += " )"
                iIndiceDisjonction += 1

            if (bItemsQualitatifsPresents) and (iNombreDisjonctions > 1):
                sRegle += " ) "

        return sRegle


    def rightQualiToArray(self):
        # TODO Auto-generated method stub
        iIndiceItem = 0
        item = None
        iNombreItems = 0 #number of items on the left
        tItemsRegle = None #the left items
        array = []

        iNombreItems = self.m_iNombreItemsDroite
        tItemsRegle = self.m_tItemsDroite

        #Firstly, write the qualitative items. if more than one exist, concatenate with AND
        iIndiceItem = 0
        while iIndiceItem < iNombreItems:
            item = tItemsRegle[iIndiceItem]
            if item.m_iTypeItem == Item.ITEM_TYPE_QUALITATIF:
                array.append((item).getAttributeNameValue())
            iIndiceItem += 1
        return array

    def rightQuantiToArray(self):
        # TODO Auto-generated method stub
        iIndiceItem = 0
        item = None
        iIndiceDisjonction = 0 #which or
        iNombreDisjonctions = 0 #number of ORs
        iNombreItemsQuantitatifs = 0 #number of Quantitatives
        iNombreItems = 0 #number of items on the left
        tItemsRegle = None #the left items

        iNombreItems = self.m_iNombreItemsDroite
        tItemsRegle = self.m_tItemsDroite
        iNombreItemsQuantitatifs = self.CompterItemsDroiteSelonType(Item.ITEM_TYPE_QUANTITATIF)
        iNombreDisjonctions = self.m_iNombreDisjonctionsDroiteValides

        if iNombreItemsQuantitatifs == 0:
            return None

        array = []

        iIndiceDisjonction = 0
        while iIndiceDisjonction < iNombreDisjonctions:

            temp = []
            iIndiceItem = 0
            while iIndiceItem < iNombreItems:
                item = tItemsRegle[iIndiceItem]
                if item.m_iTypeItem == Item.ITEM_TYPE_QUANTITATIF:
                    temp.append((item).getAttributeNameBoundary(iIndiceDisjonction))
                iIndiceItem += 1

            array.append(temp)

            iIndiceDisjonction += 1

        return array
    def toString(self):
        iIndiceItem = 0
        sRegle = None
        item = None
        bItemsQualitatifsPresents = False
        bPremierItemInscrit = False
        iIndiceDisjonction = 0
        iNombreDisjonctions = 0
        iNombreItemsQuantitatifs = 0
        iIndiceCoteRegle = 0
        iNombreItems = 0
        tItemsRegle = None

        sRegle = str("")

        sRegle += "support = "
        sRegle += str(self.m_iOccurrences)
        sRegle += " ("
        sRegle += str(int((100.0*self.m_fSupport)))
        sRegle += "%) , confidence = "
        sRegle += str(int((100.0*self.m_fConfiance)))
        sRegle += " %"

        sRegle += "  :  "

        # left(qualitative, quantitative) --> right(qualitative, quantitative):
        for iIndiceCoteRegle in range(0, 2):

            if iIndiceCoteRegle==0:
                iNombreItems = self.m_iNombreItemsGauche #number of items on left
                tItemsRegle = self.m_tItemsGauche #the left items
                iNombreItemsQuantitatifs = self.CompterItemsGaucheSelonType(Item.ITEM_TYPE_QUANTITATIF)
                iNombreDisjonctions = self.m_iNombreDisjonctionsGaucheValides
            else:
                iNombreItems = self.m_iNombreItemsDroite
                tItemsRegle = self.m_tItemsDroite
                iNombreItemsQuantitatifs = self.CompterItemsDroiteSelonType(Item.ITEM_TYPE_QUANTITATIF)
                iNombreDisjonctions = self.m_iNombreDisjonctionsDroiteValides
                sRegle += "   -->   "


            #Firstly, write the qualitative items. if more than one exist, concatenate with AND
            bPremierItemInscrit = False
            iIndiceItem = 0
            while iIndiceItem < iNombreItems:
                item = tItemsRegle[iIndiceItem]
                if item.m_iTypeItem == Item.ITEM_TYPE_QUALITATIF:
                    if bPremierItemInscrit:
                        sRegle += "  AND  " # "  ET  "
                    sRegle += (item).toString()
                    bPremierItemInscrit = True
                iIndiceItem += 1
            bItemsQualitatifsPresents = bPremierItemInscrit #if has qualitative item

            #Next, display quantitative items:
            if iNombreItemsQuantitatifs > 0:
                if bItemsQualitatifsPresents:
                    sRegle += "  AND  "
                    if iNombreDisjonctions > 1:
                        sRegle += "( "

                iIndiceDisjonction = 0
                while iIndiceDisjonction < iNombreDisjonctions:

                    if iIndiceDisjonction > 0:
                        sRegle += "  OR  " #OU

                    if (iNombreItemsQuantitatifs > 1) and (iNombreDisjonctions > 1):
                        sRegle += "( "

                    bPremierItemInscrit = False
                    iIndiceItem = 0
                    while iIndiceItem < iNombreItems:
                        item = tItemsRegle[iIndiceItem]
                        if item.m_iTypeItem == Item.ITEM_TYPE_QUANTITATIF:
                            if bPremierItemInscrit:
                                sRegle += "  AND  " #ET
                            sRegle += (item).toString(iIndiceDisjonction)
                            bPremierItemInscrit = True
                        iIndiceItem += 1

                    if (iNombreItemsQuantitatifs > 1) and (iNombreDisjonctions > 1):
                        sRegle += " )"
                    iIndiceDisjonction += 1

                if (bItemsQualitatifsPresents) and (iNombreDisjonctions > 1):
                    sRegle += " ) "

        return sRegle




    @staticmethod
    def CalculerMesuresDiverses(tRegles, contexte):
        regle = None
        iNombreRegles = 0
        iIndiceRegle = 0
        iNombreLignes = 0
        iIndiceLigne = 0
        iIndiceItem = 0
        iIndiceDisjonction =0
        item = None
        itemQual = None
        itemQuant = None
        bGaucheCouvert = True
        bDroiteCouvert = False
        fValeurReelle = 0.0

        if (tRegles == None) or (contexte == None):
            return

        iNombreRegles = len(tRegles)

        if iNombreRegles == 0:
            return


        # On r�initialise les diverses mesures avant de faire les comptes :
        iIndiceRegle = 0
        while iIndiceRegle<iNombreRegles:
            regle = tRegles[iIndiceRegle]
            regle.m_iOccurrencesGauche = 0
            regle.m_iOccurrencesDroite = 0
            regle.m_iOccurrences_Gauche_NonDroite = 0
            regle.m_iOccurrences_NonGauche_Droite = 0
            regle.m_iOccurrences_NonGauche_NonDroite = 0


            regle.m_iOccurrences = 0
            iIndiceRegle += 1


        iNombreLignes = contexte.m_gestionnaireBD.ObtenirNombreLignes()

        iIndiceLigne = 0
        while iIndiceLigne<iNombreLignes:

            iIndiceRegle = 0
            while iIndiceRegle<iNombreRegles:

                regle = tRegles[iIndiceRegle]

                # V�rification de la couverture de tous les items qualitatifs de gauche ou si la ligne contient une valeur manquante :
                bGaucheCouvert = True
                iIndiceItem=0
                while (bGaucheCouvert) and (iIndiceItem<regle.m_iNombreItemsGauche):
                    # item = regle.m_tItemsGauche[iIndiceItem]
                    item = self.m_tItemsGauche[iIndiceItem]
                    if item.m_iTypeItem == Item.ITEM_TYPE_QUALITATIF:
                        itemQual = item
                        bGaucheCouvert = (itemQual.m_iIndiceValeur == itemQual.m_attributQual.m_colonneDonnees.m_tIDQualitatif[iIndiceLigne])
                    else:
                        itemQuant = item
                        fValeurReelle = itemQuant.m_attributQuant.m_colonneDonnees.m_tValeurReelle[iIndiceLigne]
                        bGaucheCouvert = (not fValeurReelle == DatabaseAdmin.VALEUR_MANQUANTE_FLOAT)
                    iIndiceItem += 1


                # V�rification de la couverture de tous les items quantitatifs de gauche :
                if bGaucheCouvert:
                    bGaucheCouvert = False
                    iIndiceDisjonction=0
                    while ((not bGaucheCouvert)) and (iIndiceDisjonction<regle.m_iNombreDisjonctionsGaucheValides):
                        bGaucheCouvert = True
                        iIndiceItem=0
                        while (bGaucheCouvert) and (iIndiceItem<regle.m_iNombreItemsGauche):
                            # item = regle.m_tItemsGauche[iIndiceItem]
                            item = self.m_tItemsGauche[iIndiceItem]
                            if item.m_iTypeItem == Item.ITEM_TYPE_QUANTITATIF:
                                itemQuant = item
                                fValeurReelle = itemQuant.m_attributQuant.m_colonneDonnees.m_tValeurReelle[iIndiceLigne]
                                bGaucheCouvert = (fValeurReelle >= itemQuant.m_tBornes[iIndiceDisjonction*2]) and (fValeurReelle <= itemQuant.m_tBornes[iIndiceDisjonction*2+1])
                            iIndiceItem += 1
                        iIndiceDisjonction += 1


                # V�rification de la couverture de tous les items qualitatifs de droite ou si la ligne contient une valeur manquante :
                bDroiteCouvert = True
                iIndiceItem=0
                while (bDroiteCouvert) and (iIndiceItem<regle.m_iNombreItemsDroite):
                    item = regle.m_tItemsDroite[iIndiceItem]
                    if item.m_iTypeItem == Item.ITEM_TYPE_QUALITATIF:
                        itemQual = item
                        bDroiteCouvert = (itemQual.m_iIndiceValeur == itemQual.m_attributQual.m_colonneDonnees.m_tIDQualitatif[iIndiceLigne])
                    else:
                        itemQuant = item
                        fValeurReelle = itemQuant.m_attributQuant.m_colonneDonnees.m_tValeurReelle[iIndiceLigne]
                        bDroiteCouvert = (not fValeurReelle == DatabaseAdmin.VALEUR_MANQUANTE_FLOAT)
                    iIndiceItem += 1


                # V�rification de la couverture de tous les items quantitatifs de droite :
                if bDroiteCouvert:
                    bDroiteCouvert = False
                    iIndiceDisjonction=0
                    while ((not bDroiteCouvert)) and (iIndiceDisjonction<regle.m_iNombreDisjonctionsDroiteValides):
                        bDroiteCouvert = True
                        iIndiceItem=0
                        while (bDroiteCouvert) and (iIndiceItem<regle.m_iNombreItemsDroite):
                            item = regle.m_tItemsDroite[iIndiceItem]
                            if item.m_iTypeItem == Item.ITEM_TYPE_QUANTITATIF:
                                itemQuant = item
                                fValeurReelle = itemQuant.m_attributQuant.m_colonneDonnees.m_tValeurReelle[iIndiceLigne]
                                bDroiteCouvert = (fValeurReelle >= itemQuant.m_tBornes[iIndiceDisjonction*2]) and (fValeurReelle <= itemQuant.m_tBornes[iIndiceDisjonction*2+1])
                            iIndiceItem += 1
                        iIndiceDisjonction += 1



                if (bGaucheCouvert) and (bDroiteCouvert):
                    regle.m_iOccurrences += 1

                if bGaucheCouvert:
                    regle.m_iOccurrencesGauche += 1

                if bDroiteCouvert:
                    regle.m_iOccurrencesDroite += 1

                if (bGaucheCouvert) and ((not bDroiteCouvert)):
                    regle.m_iOccurrences_Gauche_NonDroite += 1

                if ((not bGaucheCouvert)) and (bDroiteCouvert):
                    regle.m_iOccurrences_NonGauche_Droite += 1

                if ((not bGaucheCouvert)) and ((not bDroiteCouvert)):
                    regle.m_iOccurrences_NonGauche_NonDroite += 1

                iIndiceRegle += 1
            iIndiceLigne += 1

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

from tools.dataStructures import *



class AttributQualitative(object):
    # indexed by their unique identifier.
    # the value indicates whether or not it should be taken into account during the rule extraction process
    def __init__(self, sNomAttribut, colonneDonnees):
        self.m_sNomAttribut = None
        self.m_iNombreValeurs = 0
        self.m_tTableauValeurs = None
        self.m_tTableauPriseEnCompte = None
        self.m_colonneDonnees = None
        self.m_LiensItemSets = None


        iIndiceValeur = 0

        self.m_sNomAttribut = sNomAttribut
        self.m_colonneDonnees = colonneDonnees

        if not self.m_colonneDonnees == None:
            self.m_iNombreValeurs = self.m_colonneDonnees.ObtenirNombreValeursDifferentes()
            self.m_LiensItemSets = [None for _ in range(self.m_iNombreValeurs)]

            iIndiceValeur = 0
            while iIndiceValeur < self.m_iNombreValeurs:
                self.m_LiensItemSets[iIndiceValeur] = []
                iIndiceValeur += 1
        else:
            self.m_iNombreValeurs = 0
            self.m_LiensItemSets = None

        if self.m_iNombreValeurs > 0:
            self.m_tTableauValeurs = colonneDonnees.ConstituerTableauValeurs()
            self.m_tTableauPriseEnCompte = [False for _ in range(self.m_iNombreValeurs)]

            iIndiceValeur = 0
            while iIndiceValeur<self.m_iNombreValeurs:
                self.m_tTableauPriseEnCompte[iIndiceValeur] = True
                iIndiceValeur += 1
        else:
            self.m_tTableauValeurs = None
            self.m_tTableauPriseEnCompte = None



    #    *Get Correspondent Index Value 
    #     * @param sNomItem Item Name
    #     
    def ObtenirIndiceCorrespondantValeur(self, sNomItem):
        return self.m_colonneDonnees.ObtenirNumeroCorrespondance(sNomItem)



    #    * return the value of an attribute by index.
    #     * @param iIndice Index of an attribute
    #     * @return value of the attribute
    #     
    def ObtenirValeurCorrespondantIndice(self, iIndice):
        if (iIndice >= 0) and (int(iIndice) < self.m_iNombreValeurs):
            return self.m_tTableauValeurs[iIndice]
        else:
            return None


    #    *Compute number of occurrence
    #     * @param iNumeroTransaction Transaction Number
    #     * @param iIndiceValeur Index Value
    #     
    def ComptabiliserOcurrenceValeur(self, iNumeroTransaction, iIndiceValeur):

        itemSet = None
        iIndiceItemSet = 0
        iNombreItemSets = 0
        listeItemSets = None

        if (iIndiceValeur<0) or (int(iIndiceValeur) >= self.m_iNombreValeurs):
            return

        listeItemSets = self.m_LiensItemSets[int(iIndiceValeur)]

        iNombreItemSets = len(listeItemSets)

        iIndiceItemSet = 0
        while iIndiceItemSet<iNombreItemSets:
            itemSet = listeItemSets[iIndiceItemSet]
            itemSet.ComptabiliserDecouverteItem(iNumeroTransaction)
            iIndiceItemSet += 1


    #    *Get the name of the attribute
    #     * @return name of the attribute
    #     
    def ObtenirNom(self):
        return self.m_sNomAttribut


    def GenererItems(self, tableItems):

        iIndiceValeur = 0

        iIndiceValeur = 0
        while iIndiceValeur < self.m_iNombreValeurs:
            tableItems.DeclarerItemQualitatif(self, iIndiceValeur)
            iIndiceValeur += 1


    # Two attributes are equal if and only if they have the same name:
    def equals(self, obj):

        if obj == None:
            return False

        if (self.m_sNomAttribut == None) or ((obj).m_sNomAttribut == None):
            return False

        return (self.m_sNomAttribut == (obj).m_sNomAttribut)


    #    *Add item set
    #     * @param iIndiceValeur
    #     * @param itemSet
    #     
    def AjouterLienVersItemSet(self, iIndiceValeur, itemSet):
        if (iIndiceValeur>=0) and (int(iIndiceValeur)<self.m_iNombreValeurs):
            self.m_LiensItemSets[iIndiceValeur].append(itemSet)


    #    *Reset ItemSets
    #     
    def ReinitialiserListeLiensItemSets(self):
        iIndiceValeur = 0

        iIndiceValeur = 0
        while iIndiceValeur<self.m_iNombreValeurs:
            self.m_LiensItemSets[iIndiceValeur].clear()
            iIndiceValeur += 1

    #    *Get the support of an item
    #     * @param iIndiceValeur index
    #     * @return
    #     
    def ObtenirSupportItem(self, iIndiceValeur):

        infosMot = None

        if (iIndiceValeur>=0) and (int(iIndiceValeur) < self.m_iNombreValeurs):
            infosMot = self.m_colonneDonnees.m_listeValeurs.ChercherInfosMot(self.m_tTableauValeurs[iIndiceValeur])
            if not infosMot == None:
                return infosMot.m_iOccurrences
            else:
                return 0
        else:
            return 0



    def DefinirPriseEnCompteValeur(self, sNomItem, bPrendreEnCompte):
        iIndiceItem = -1

        # On r�cup�re l'identificateur de l'item :
        iIndiceItem = self.ObtenirIndiceCorrespondantValeur(sNomItem)
        if iIndiceItem < 0:
            return

        self.m_tTableauPriseEnCompte[iIndiceItem] = bPrendreEnCompte



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

class AttributQuantitative(object):



    def __init__(self, sNomAttribut, colonneDonnees):
        self.m_sNomAttribut = None
        self.m_fBorneMin = 0
        self.m_fBorneMax = 0
        self.m_colonneDonnees = None


        self.m_sNomAttribut = sNomAttribut
        self.m_colonneDonnees = colonneDonnees

        if self.m_colonneDonnees is not None:
            self.m_fBorneMin = self.m_colonneDonnees.ObtenirBorneMin()
            self.m_fBorneMax = self.m_colonneDonnees.ObtenirBorneMax()
        else:
            self.m_fBorneMin = self.m_fBorneMax = 0.0



    def ObtenirNom(self):
        return self.m_sNomAttribut



    # Two attributes are equal if and only if they have the same name:
    def equals(self, obj):

        if obj is None:
            return False

        if (m_sNomAttribut is None) or ((obj).m_sNomAttribut is None):
            return False

        return (self.m_sNomAttribut == (obj).m_sNomAttribut)



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



class Item(object):

    ITEM_TYPE_INDEFINI = 0
    ITEM_TYPE_QUALITATIF = 1
    ITEM_TYPE_QUANTITATIF = 2



    def __init__(self):
        self.m_itemSuivant = None
        self.m_iTypeItem = self.ITEM_TYPE_INDEFINI

        self.m_iTypeItem = self.ITEM_TYPE_INDEFINI
        self.m_itemSuivant = None


    def toString(self):
        sItem = None


        if self.m_iTypeItem == Item.ITEM_TYPE_QUALITATIF:
            sItem = "Item Qualitatif"

        elif self.m_iTypeItem == Item.ITEM_TYPE_QUANTITATIF:
            sItem = "Item Quantitatif"

        else:
            sItem = "Item undefined" #undefined

        return sItem

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
sys.path.append('C:\\Users\\aalsahee\\python_physical_model\\Saudi\\trace\\Traces\\qtm\\src\\')

from tools.dataStructures import *
# from Item import Item


class ItemQualitative(Item):
    def __init__(self, attributQual, iIndiceValeur):
        self.m_lIdentifieur = 0
        self.m_attributQual = None
        self.m_iIndiceValeur = 0

        super().__init__()

        self.m_iTypeItem = self.ITEM_TYPE_QUALITATIF

        # print(TableItems.m_lCompteurItem)
        # Obtaining a unique identification number for the newly created item:
        self.m_lIdentifieur = TableItems.ObtenirIdentifieurUnique()

        self.m_attributQual = attributQual
        self.m_iIndiceValeur = iIndiceValeur

        self.m_itemSuivant = None



    #    *Get full Name of the item
    #     * @return name of the item
    #     
    def ObtenirNomCompletItem(self):
        sChaineItem = None

        if self.m_attributQual is None:
            return None

        sChaineItem = self.m_attributQual.ObtenirNom()
        sChaineItem += "."
        sChaineItem += self.m_attributQual.ObtenirValeurCorrespondantIndice(self.m_iIndiceValeur)

        return sChaineItem



    #    *Get value of an item ID
    #     * @return value of an item
    #     
    def ObtenirIdentifiantTexteItem(self):

        if self.m_attributQual is None:
            return None

        return self.m_attributQual.ObtenirValeurCorrespondantIndice(self.m_iIndiceValeur)

    #    *Obtain the name and value of this item/attribute
    #     * @return A Qualitative item
    #     
    def getAttributeNameValue(self):
        element = Qualitative()
        sNomAttribut = None #name of the attribute
        sValeurItem = None #value of the item

        if self.m_attributQual is None:
            return None

        sNomAttribut = self.m_attributQual.ObtenirNom() #get the name of the attribute
        if sNomAttribut is not None:
            sNomAttribut = sNomAttribut.strip()

        sValeurItem = self.m_attributQual.ObtenirValeurCorrespondantIndice(self.m_iIndiceValeur) #get the value of the attribute
        if sValeurItem is not None:
            sValeurItem = sValeurItem.strip()

        element.setM_name(sNomAttribut)
        element.setM_value(sValeurItem)

        return element


    #return something like COD_GEOL = Tv
    def toString(self):
        sItem = None
        sNomAttribut = None #name of the attribute
        sValeurItem = None #value of the item

        if self.m_attributQual is None:
            return "Item nul"

        sNomAttribut = self.m_attributQual.ObtenirNom() #get the name of the attribute
        if sNomAttribut is not None:
            sNomAttribut = sNomAttribut.strip()

        sValeurItem = self.m_attributQual.ObtenirValeurCorrespondantIndice(self.m_iIndiceValeur) #get the value of the attribute
        if sValeurItem is not None:
            sValeurItem = sValeurItem.strip()

        sItem = sNomAttribut
        sItem += " = "
        sItem += sValeurItem

        return sItem



    def compareTo(self, o):
        if self.m_lIdentifieur > (o).m_lIdentifieur:
            return 1
        elif self.m_lIdentifieur < (o).m_lIdentifieur:
            return -1
        else:
            return 0

    def __lt__(self, o):
        if self.m_lIdentifieur > (o).m_lIdentifieur:
            return 1
        elif self.m_lIdentifieur < (o).m_lIdentifieur:
            return -1
        else:
            return 0



    def equals(self, obj):
        if obj is None:
            return False
        else:
            return (self.m_lIdentifieur == (obj).m_lIdentifieur)

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
sys.path.append('C:\\Users\\aalsahee\\python_physical_model\\Saudi\\trace\\Traces\\qtm\\src\\')

from tools.dataStructures import *
# from Item import Item


class ItemQuantitative(Item):

    def _initialize_instance_fields(self):
        self.m_attributQuant = None
        self.m_iNombreDisjonctions = 0
        self.m_tBornes = None


    #        The min and max limits, stored successively 2 e 2 (each pair corresponds to an interval in order to be able to authorize unions)
    #    


    #    *
    #     * Creating Multi Item Quantitative Intervals
    #     * @param attributQuant Quantitative attributes
    #     * @param tBornes Interval bounds
    #     
    def __CreerItemQuantitatifMultiIntervalles(self, attributQuant, tBornes):
        iIndiceDisjonction = 0

        self.m_iTypeItem = Item.ITEM_TYPE_QUANTITATIF

        self.m_attributQuant = attributQuant
        if tBornes is None:
            self.m_iNombreDisjonctions = 0
        else:
            self.m_iNombreDisjonctions = math.trunc(len(tBornes) / float(2))

        if self.m_iNombreDisjonctions == 0:
            self.m_tBornes = None
            return

        self.m_tBornes = [0 for _ in range(self.m_iNombreDisjonctions * 2)]
        iIndiceDisjonction = 0
        while iIndiceDisjonction<(self.m_iNombreDisjonctions*2):
            self.m_tBornes[iIndiceDisjonction] = tBornes[iIndiceDisjonction]
            iIndiceDisjonction += 1

    def __init__(self, *args):
        if len(args) == 2 and not type(args[1]) == int:
            attributQuant = args[0]
            tBornes = args[1]
            self._initialize_instance_fields()
            super().__init__()
            self.__CreerItemQuantitatifMultiIntervalles(attributQuant, tBornes)
        elif len(args) == 2 and type(args[1]) == int:
            attributQuant = args[0]
            iNombreDisjonctions = args[1]
            self._initialize_instance_fields()
            super().__init__()
            tBornes = None
            iIndiceBorne = 0
            if iNombreDisjonctions <= 0:
                self.__CreerItemQuantitatifMultiIntervalles(attributQuant, None)
            else:
                tBornes = [0 for _ in range(iNombreDisjonctions*2)]
                iIndiceBorne = 0
                while iIndiceBorne<iNombreDisjonctions*2:
                    tBornes[iIndiceBorne] = 0.0
                    iIndiceBorne += 1
                self.__CreerItemQuantitatifMultiIntervalles(attributQuant, tBornes)
        elif len(args) == 3:
            attributQuant = args[0]
            fBorneMin = args[1]
            fBorneMax = args[2]
            self._initialize_instance_fields()
            super().__init__()

            self.m_iTypeItem = Item.ITEM_TYPE_QUANTITATIF
            self.m_attributQuant = attributQuant
            self.m_iNombreDisjonctions = 1
            self.m_tBornes = [0 for _ in range(2)]
            self.m_tBornes[0] = fBorneMin
            self.m_tBornes[1] = fBorneMax
        elif len(args) == 1:
            item = args[0]
            self._initialize_instance_fields()
            super().__init__()
            self.CopierItemQuantitatif(item)


    def CopierItemQuantitatif(self, item):
        iIndiceDisjonction = 0

        self.m_iTypeItem = Item.ITEM_TYPE_QUANTITATIF
        self.m_attributQuant = item.m_attributQuant
        self.m_iNombreDisjonctions = item.m_iNombreDisjonctions

        if self.m_iNombreDisjonctions == 0:
            self.m_tBornes = None
            return

        self.m_tBornes = [0 for _ in range(self.m_iNombreDisjonctions * 2)]
        iIndiceDisjonction = 0
        while iIndiceDisjonction<(self.m_iNombreDisjonctions*2):
            self.m_tBornes[iIndiceDisjonction] = item.m_tBornes[iIndiceDisjonction]
            iIndiceDisjonction += 1


    #obtain the min value of the iIndiceDisjonction disjunct
    def ObtenirBorneMinIntervalle(self, iIndiceDisjonction):
        if iIndiceDisjonction < self.m_iNombreDisjonctions:
            return self.m_tBornes[iIndiceDisjonction * 2]
        else:
            return 0

    #obtain the max value of the iIndiceDisjonction disjunct    
    def ObtenirBorneMaxIntervalle(self, iIndiceDisjonction):
        if iIndiceDisjonction < self.m_iNombreDisjonctions:
            return self.m_tBornes[iIndiceDisjonction*2 + 1]
        else:
            return 0

    #obtain the name, min, max value of the attribute
    def getAttributeNameBoundary(self, iIndiceDisjonction):
        element = Quantitative()
        sNomItem = None

        if self.m_attributQuant is None:
            return None

        sNomItem = self.m_attributQuant.ObtenirNom()
        if sNomItem is not None:
            sNomItem = sNomItem.strip()

        element.setM_name(sNomItem)
        element.setM_lower(self.m_tBornes[iIndiceDisjonction*2])
        element.setM_upper(self.m_tBornes[iIndiceDisjonction*2 + 1])

        return element


    #return something like ALTITUDE in [1814.0; 4926.0]
    def toString(self, iIndiceDisjonction):
        sItem = None
        sNomItem = None

        if self.m_attributQuant is None:
            return "Item nul"

        sNomItem = self.m_attributQuant.ObtenirNom()
        if sNomItem is not None:
            sNomItem = sNomItem.strip()

        sItem = sNomItem
        sItem += " in "

        sItem += "["
        sItem += str(self.m_tBornes[iIndiceDisjonction*2]) #min
        sItem += "; "
        sItem += str(self.m_tBornes[iIndiceDisjonction*2 + 1]) #max
        sItem += "]"

        return sItem

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
sys.path.append('C:\\Users\\aalsahee\\python_physical_model\\Saudi\\trace\\Traces\\qtm\\src\\')

# from tools.dataStructures import *
# from Item import Item


class ItemSet(object):


    def __init__(self, iTaille):
        self.m_iTaille = 0
        self.m_listeItems = None
        self.m_iNombreItemsSpecifies = 0
        self.m_iSupport = 0
        self.m_iNombreItemsComptabilises = 0
        self.m_iDerniereTransactionComptabilisee = -1


        iIndiceItem = 0

        self.m_iTaille = iTaille

        if self.m_iTaille>0:
            self.m_listeItems = [None for _ in range(iTaille)]
            # java.util.Arrays.fill(self.m_listeItems, None)

        self.m_iNombreItemsSpecifies = 0
        self.m_iSupport = 0
        self.m_iNombreItemsComptabilises = 0
        self.m_iDerniereTransactionComptabilisee = -1


    def SpecifierItem(self, item):

        if self.m_iNombreItemsSpecifies < self.m_iTaille:

            self.m_listeItems[self.m_iNombreItemsSpecifies] = item
            self.m_iNombreItemsSpecifies += 1

            if self.m_iNombreItemsSpecifies == self.m_iTaille:
                self.m_listeItems.sort()



    def ObtenirItem(self, iIndiceItem):
        if (iIndiceItem >= 0) and (iIndiceItem < self.m_iNombreItemsSpecifies):
            return self.m_listeItems[iIndiceItem]
        else:
            return None



    def SpecifierSupport(self, iSupport):
        self.m_iSupport = iSupport


    #    *
    #     * This function is called each time one of the items belonging to the itemset is found 
    #    * while reading a tuple of the dataset.  The counter must be re-initialized for each new tuple 
    #     * with the function 'ReinitialiserComptabilisationItems'.
    #     * @param iNumeroTransaction
    #     
    def ComptabiliserDecouverteItem(self, iNumeroTransaction):

        if iNumeroTransaction == self.m_iDerniereTransactionComptabilisee:
            self.m_iNombreItemsComptabilises += 1
        else:
            self.m_iNombreItemsComptabilises = 1

        # On incr�mente le support si tous les items ont �t� trouv�s :
        if self.m_iNombreItemsComptabilises==self.m_iTaille:
            self.m_iSupport += 1

        self.m_iDerniereTransactionComptabilisee = iNumeroTransaction


    def ReinitialiserComptabilisationItems(self):
        self.m_iNombreItemsComptabilises = 0
        self.m_iDerniereTransactionComptabilisee = -1

    #    *
    #     * Get string format of Item sets
    #     * @param iNombreTransactions number of transactions
    #     * @param bAfficherSuppport    display Support or not
    #     * @return string
    #     
    def EcrireItemSet(self, iNombreTransactions, bAfficherSuppport):
        sTexteItemSet = None
        sTexteItem = None
        iIndiceItem = 0
        item = None

        sTexteItemSet = "{ "

        iIndiceItem = 0
        while iIndiceItem<self.m_iTaille:
            item = self.m_listeItems[iIndiceItem]

            if item is not None:
                if iIndiceItem>0:
                    sTexteItemSet += ", "

                sTexteItemSet += item.toString()
            iIndiceItem += 1

        sTexteItemSet += " }"

        if bAfficherSuppport:
            sTexteItemSet += "  ,  support = "
            sTexteItemSet += str(self.m_iSupport)
            sTexteItemSet += " ("
            sTexteItemSet += str(float((100.0*(float(self.m_iSupport) / float(iNombreTransactions)))))
            sTexteItemSet += "%)"

        return sTexteItemSet



    #    *
    #     * Generate a K-itemset starting from two (k-1) itemsets given they share the same (k-2) items in the beginning: 
    #     * (the two itemsets used by the function must have the same size)
    #     * @param itemSetAutre
    #     * @return
    #     
    def EstGenerateurCandidatAvec(self, itemSetAutre):

        iIndiceItem = 0
        bItemTousIdentiques = True

        iIndiceItem=0
        while (bItemTousIdentiques) and (iIndiceItem<self.m_iTaille-1):

            bItemTousIdentiques = (self.m_listeItems[iIndiceItem].compareTo(itemSetAutre.m_listeItems[iIndiceItem]) == 0)

            iIndiceItem += 1

        return bItemTousIdentiques


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

# from tools.dataStructures import *
# from Item import Item


class OptimizerAprioriQual(RuleOptimizer):
    def __init__(self):
        self.m_parametresRegles = None
        self.m_parametresRegles = None



    # Override of the context specification function:
    def DefinirContexteResolution(self, contexteResolution):
        super().DefinirContexteResolution(contexteResolution)

        if self.m_contexteResolution is None:
            self.m_parametresRegles = None
            return

        self.m_parametresRegles = self.m_contexteResolution.m_parametresRegles



    # Overriding the optimization function:
    #int i not used but needed in abstract class for OptimizerGeneticAlgorithm
    def OptimiseRegle(self, regle, i):
        iNombreItemsQuantitatifs = 0

        if regle is None:
            return False

        iNombreItemsQuantitatifs = regle.CompterItemsGaucheSelonType(Item.ITEM_TYPE_QUANTITATIF) + regle.CompterItemsDroiteSelonType(Item.ITEM_TYPE_QUANTITATIF)

        if iNombreItemsQuantitatifs > 0:
            return False

        # Calculation of support and confidence of the qualitative rule:
        regle.EvaluerSiQualitative(self.m_contexteResolution)

        return ((regle.m_fSupport >= self.m_parametresRegles.m_fMinSupp) and (regle.m_fConfiance >= self.m_parametresRegles.m_fMinConf))

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

class Qualitative(object):

    def __init__(self):
        self.m_name = None
        self.m_value = None


    def getM_name(self):
        return self.m_name

    def setM_name(self, m_name):
        self.m_name = m_name

    def getM_value(self):
        return self.m_value

    def setM_value(self, m_value):
        self.m_value = m_value

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

class Quantitative(object):

    def __init__(self):
        self.m_name = None
        self.m_lower = 0
        self.m_upper = 0

    def getM_name(self):
        return self.m_name
    def setM_name(self, m_name):
        self.m_name = m_name
    def getM_lower(self):
        return self.m_lower
    def setM_lower(self, m_lower):
        self.m_lower = m_lower
    def getM_upper(self):
        return self.m_upper
    def setM_upper(self, m_upper):
        self.m_upper = m_upper

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

# Class listing all the parameters defined by the user for the next
# execution of the rule extractor algorithm.

# * Apiori rule parameter
# 
class StandardParameters(object):

    



    def __init__(self):
        self.m_fMinSupp = 0.0
        self.m_fMinConf = 0.0

        self.m_fMinSupp = DEFAUT_MINSUPP
        self.m_fMinConf = DEFAUT_MINCONF


    def toString(self):
        sParametres = None

        sParametres = "General parameters selected for rule extraction:" + "\n" + "\n"
        sParametres += "Minimal Support: " + ResolutionContext.EcrirePourcentage(self.m_fMinSupp, 3, True) + "\n"
        sParametres += "Minimal Confidence: " + ResolutionContext.EcrirePourcentage(self.m_fMinConf, 3, True) + "\n"

        return sParametres
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

# DEFAUT_MINSUPP = 0.10
# DEFAUT_MINCONF = 0.60
DEFAUT_MINSUPP_DISJONCTIONS = 0.0 #support threshold for additional intervals

# Class listing all the parameters defined by the user for the next
# execution of the rule extractor algorithm.

#*Generic algorithm rule parameter
# 
class StandardParametersQuantitative(object):




    def __init__(self):
        self.m_fMinSupp = 0.0
        self.m_fMinConf = 0.0
        self.m_iNombreMinAttributsQuant = 0
        self.m_iNombreMaxAttributsQuant = 0
        self.m_iNombreDisjonctionsGauche = 0
        self.m_iNombreDisjonctionsDroite = 0
        self.m_fMinSuppDisjonctions = 0.0
        self.m_iNombreAssociationRules = 1
        self.m_applyKMeans = 0

        self.m_fMinSupp = DEFAUT_MINSUPP
        self.m_fMinConf = DEFAUT_MINCONF
        self.m_iNombreMinAttributsQuant = 1
        self.m_iNombreMaxAttributsQuant = 3
        self.m_iNombreDisjonctionsGauche = 1
        self.m_iNombreDisjonctionsDroite = 1
        self.m_fMinSuppDisjonctions = DEFAUT_MINSUPP_DISJONCTIONS
        self.m_iNombreAssociationRules = 1
        self.m_applyKMeans = 0

    def toString(self):
        sParametres = None

        sParametres = "Gerneral parameters selected for rule extraction:" + "\n" + "\n"
        sParametres += "Minimal Support: " + ResolutionContext.EcrirePourcentage(self.m_fMinSupp, 3, True) + "\n"
        sParametres += "Minimal Confidence: " + ResolutionContext.EcrirePourcentage(self.m_fMinConf, 3, True) + "\n"
        sParametres += "Minimum number of numerical attributes in a rule: " + str(self.m_iNombreMinAttributsQuant) + "\n"
        sParametres += "Maximum number of numerical attributes in a rule: " + str(self.m_iNombreMaxAttributsQuant) + "\n"
        sParametres += "Number of disjunctions allowed in the left-hand side: " + str(self.m_iNombreDisjonctionsGauche) + "\n"
        sParametres += "Number of disjunctions allowed in the right-hand side: " + str(self.m_iNombreDisjonctionsDroite) + "\n"
        sParametres += "Minimal support for the additional interval: " + str(self.m_fMinSuppDisjonctions) + "\n"
        sParametres += "Number of top rules per association: " + str(self.m_iNombreAssociationRules) + "\n"

        if self.m_applyKMeans == 1:
            sParametres += "Apply clustering: Yes (k-means)\n"
        elif self.m_applyKMeans == 2:
            sParametres += "Apply clustering: Yes (g-means)\n"
        else:
            sParametres += "Apply clustering: No (top fitness only)\n"

        return sParametres
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



class TableItems:

    m_lCompteurItem = 0 # ID sur 64 bits (borne � 9 milliards de milliards)

    def __init__(self):
        self.m_premierItem = None
        self.m_dernierItem = None
        self.m_premierItem = None
        self.m_dernierItem = None
        
    @staticmethod
    def ObtenirIdentifieurUnique():
        TableItems.m_lCompteurItem += 1
        return TableItems.m_lCompteurItem


    def DeclarerItemQualitatif(self, attribut, iIndiceValeur):

        nouvelItem = ItemQualitative(attribut, iIndiceValeur)

        if (self.m_premierItem is None) or (self.m_dernierItem is None):
            self.m_premierItem = self.m_dernierItem = nouvelItem
        else:
            self.m_dernierItem.m_itemSuivant = nouvelItem
            self.m_dernierItem = nouvelItem


    def ObtenirPremierItem(self):
        return self.m_premierItem


