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

from tools.dataStructures.WordList import WordList
# from database.DatabaseAdmin import DatabaseAdmin


class DataColumn(object):

    # Member about unique the column of value categorical:
    # Member about unique column that value quantitative:

    def __init__(self, sNomColonne, iTypeValeurs, iNombreLignes, index):
        self.m_sNomColonne = None
        self.m_iIndiceChamp = 0
        self.m_iTypeValeurs = 0
        self.m_iNombreLignes = 0
        self.m_tIDQualitatif = None
        self.m_listeValeurs = None
        self.m_tValeurReelle = None
        self.m_tValeursReellesTriees = None
        self.m_iNombreValeursReellesCorrectes = 0
        self.m_tValeursUniques = None
        self.m_tCumulSupportCroissant = None
        self.m_iNombreValeursUniques = 0
        self.m_fValeurMin = 0.0
        self.m_fValeurMax = 0.0
        self.__m_bBornesReellesDefinies = False


        self.m_sNomColonne = sNomColonne
        self.m_iTypeValeurs = iTypeValeurs
        self.m_iNombreLignes = iNombreLignes
        self.__m_bBornesReellesDefinies = False
        self.m_iIndiceChamp = index
        self.m_fValeurMin = 0.0
        self.m_fValeurMax = 0.0
        self.m_iNombreValeursReellesCorrectes = 0
        self.m_tValeursReellesTriees = None

        if iNombreLignes > 0:
            if self.m_iTypeValeurs == TYPE_VALEURS_COLONNE_ITEM:
                self.m_listeValeurs = WordList()
                self.m_tIDQualitatif = []
                for i in range(0, iNombreLignes):
                    self.m_tIDQualitatif.append(0)

            elif self.m_iTypeValeurs == TYPE_VALEURS_COLONNE_REEL:
                self.m_tValeurReelle = []
                for i in range(0, iNombreLignes):
                    self.m_tValeurReelle.append(0)
        else:
            self.m_listeValeurs = None
            self.m_tIDQualitatif = None
            self.m_tValeurReelle = None


    def RepertorierValeur(self, sValeur):
        return self.m_listeValeurs.InsererMot(sValeur)


    #    *
    #     * Function allowing to make the correspondence between the textual representation of a value and its numerical identifier
    #     * @param sValeur
    #     * @return short
    #     
    def ObtenirNumeroCorrespondance(self, sValeur):
        infosMot = None

        infosMot = self.m_listeValeurs.ChercherInfosMot(sValeur)
        if infosMot is not None:
            return infosMot.m_iIdentifiantUnique
        else:
            return -1


    #    *
    #     *  Unique for cateogorical (qualitative) values, it returns the number of occurrences of a given item in all the tuples
    #     * @param sValeur The item
    #     * @return number of occurrences
    #     
    def ObtenirNombreOccurrencesItem(self, sValeur):
        infosMot = None

        infosMot = self.m_listeValeurs.ChercherInfosMot(sValeur)
        if infosMot is None:
            return 0
        else:
            return infosMot.m_iOccurrences


    # For quantitative values only, returns the smallest value found in the data:
    def ObtenirBorneMin(self):
        return self.m_fValeurMin


    # For quantitative values only, returns the largest value found in the data:
    def ObtenirBorneMax(self):
        return self.m_fValeurMax


    #    *
    #     * keeps in memory a real value and updates the min and max if necessary
    #     * @param iIndiceLigne
    #     * @param fValeur
    #     
    def AssignerValeurReelle(self, iIndiceLigne, fValeur):

        if not fValeur == VALEUR_MANQUANTE_FLOAT:

            if self.__m_bBornesReellesDefinies:
                if fValeur < self.m_fValeurMin:
                    self.m_fValeurMin = fValeur
                if fValeur > self.m_fValeurMax:
                    self.m_fValeurMax = fValeur
            else:
                self.m_fValeurMin = self.m_fValeurMax = fValeur
                self.__m_bBornesReellesDefinies = True


        self.m_tValeurReelle[iIndiceLigne] = fValeur



    def ObtenirNombreValeursDifferentes(self):
        return self.m_listeValeurs.ObtenirNombreMots()

    def ConstituerTableauValeurs(self):
        iNombreValeurs = 0
        iIdentifiantValeur = 0
        tTableauValeurs = []

        if not self.m_iTypeValeurs == TYPE_VALEURS_COLONNE_ITEM:
            return None

        iNombreValeurs = self.m_listeValeurs.ObtenirNombreMots()
        if iNombreValeurs <= 0:
            return None

        tTableauValeurs = []
        for i in range(0, iNombreValeurs):
            #Assigns the specified Object reference to each element of the specified array of Objects
            tTableauValeurs.append(None)

        self.m_listeValeurs.InicierParcours()
        while self.m_listeValeurs.AvancerParcours():
            iIdentifiantValeur = (self.m_listeValeurs.ObtenirInfosMotParcouru()).m_iIdentifiantUnique
            if (iIdentifiantValeur >= 0) and (iIdentifiantValeur < iNombreValeurs):
                tTableauValeurs[iIdentifiantValeur] = self.m_listeValeurs.ObtenirMotParcouru()

        return tTableauValeurs


    #    *
    #     *  fills an additional table containing all the numerical values of the column, but sorted.
    #     
    def ConstruireTableauValeursQuantitativesTriees(self):
        fValeurCourante = 0.0
        fValeurSuivante = 0.0
        iValeurUniqueCourante = 0
        iValeurUniqueSuivante = 0
        iIndiceValeur = 0
        iIndiceValeurSuivante = 0
        iIndiceRemplissage = 0
        iSupportCumule = 0


        if not self.m_iTypeValeurs == TYPE_VALEURS_COLONNE_REEL:
            return


        # We count the number of non-missing numerical values:
        self.m_iNombreValeursReellesCorrectes = 0
        iIndiceValeur = 0
        while iIndiceValeur < self.m_iNombreLignes:
            if not self.m_tValeurReelle[iIndiceValeur] == VALEUR_MANQUANTE_FLOAT:
                self.m_iNombreValeursReellesCorrectes += 1
            iIndiceValeur += 1

        if self.m_iNombreValeursReellesCorrectes == 0:
            self.m_tValeursReellesTriees = None
        else:
            self.m_tValeursReellesTriees = []
            for i in range(0, self.m_iNombreValeursReellesCorrectes):
                self.m_tValeursReellesTriees.append(0)


        # We fill the table with the correct numerical values:
        iIndiceValeur = 0
        while iIndiceValeur < self.m_iNombreValeursReellesCorrectes:
            if not self.m_tValeurReelle[iIndiceValeur] == VALEUR_MANQUANTE_FLOAT:
                self.m_tValeursReellesTriees[iIndiceValeur] = self.m_tValeurReelle[iIndiceValeur]
            iIndiceValeur += 1


        # Then we sort them:
        if self.m_tValeursReellesTriees is not None:
            self.m_tValeursReellesTriees.sort()

        #----------------------------------------------
        # CONSTRUCTION OF THE TABLE OF UNIQUE VALUES:
        if self.m_iNombreValeursReellesCorrectes == 0:
            self.m_tValeursUniques = None
        else:
            self.m_tValeursUniques = []
            for i in range(0, self.m_iNombreValeursReellesCorrectes):
                self.m_tValeursUniques.append(0)

        self.m_iNombreValeursUniques = 0
        iIndiceValeur=0
        while iIndiceValeur < self.m_iNombreValeursReellesCorrectes:
            fValeurSuivante = fValeurCourante = self.m_tValeursReellesTriees[iIndiceValeur]

            iIndiceValeurSuivante = iIndiceValeur + 1
            while (fValeurSuivante == fValeurCourante) and (iIndiceValeurSuivante < self.m_iNombreValeursReellesCorrectes):
                fValeurSuivante = self.m_tValeursReellesTriees[iIndiceValeurSuivante]
                if fValeurSuivante == fValeurCourante:
                    iIndiceValeurSuivante += 1

            # Filling of the table for the same cumulative support value:
            iIndiceRemplissage = iIndiceValeur
            while iIndiceRemplissage < iIndiceValeurSuivante:
                self.m_tValeursUniques[iIndiceRemplissage] = self.m_iNombreValeursUniques
                iIndiceRemplissage += 1

            iIndiceValeur = iIndiceValeurSuivante
            self.m_iNombreValeursUniques += 1

        #-----------------------------------------------
        # CONSTRUCTION DU TABLEAU DES SUPPORTS CUMULES :

        if self.m_iNombreValeursUniques == 0:
            self.m_tCumulSupportCroissant = None
        else:
            self.m_tCumulSupportCroissant = []
            for i in range(0, self.m_iNombreValeursUniques):
                self.m_tCumulSupportCroissant.append(0)

        iSupportCumule = 1
        iIndiceValeur = 0
        while iIndiceValeur < self.m_iNombreValeursReellesCorrectes:
            iValeurUniqueSuivante = iValeurUniqueCourante = self.m_tValeursUniques[iIndiceValeur]

            iIndiceValeurSuivante = iIndiceValeur + 1
            while (iValeurUniqueSuivante==iValeurUniqueCourante) and (iIndiceValeurSuivante < self.m_iNombreValeursReellesCorrectes):
                iValeurUniqueSuivante = self.m_tValeursUniques[iIndiceValeurSuivante]
                if iValeurUniqueSuivante == iValeurUniqueCourante:
                    iSupportCumule += 1
                    iIndiceValeurSuivante += 1

            self.m_tCumulSupportCroissant[iValeurUniqueCourante] = iSupportCumule

            iIndiceValeur = iIndiceValeurSuivante
            iSupportCumule += 1


    def ObtenirSupportIntervalle(self, iBorneMin, iBorneMax):
        iIndiceUniqueMin = 0
        iIndiceUniqueMax = 0

        if self.m_tCumulSupportCroissant is None:
            return 0

        if iBorneMin < 0:
            iBorneMin = 0

        if iBorneMax >= self.m_iNombreValeursReellesCorrectes:
            iBorneMax = self.m_iNombreValeursReellesCorrectes - 1

        iIndiceUniqueMin = self.m_tValeursUniques[iBorneMin]
        iIndiceUniqueMax = self.m_tValeursUniques[iBorneMax]

        if iIndiceUniqueMin == 0:
            return self.m_tCumulSupportCroissant[iIndiceUniqueMax]
        else:
            return (self.m_tCumulSupportCroissant[iIndiceUniqueMax] - self.m_tCumulSupportCroissant[iIndiceUniqueMin-1])


