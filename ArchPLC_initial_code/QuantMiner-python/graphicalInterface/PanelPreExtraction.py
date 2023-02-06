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
from graphicalInterface.TreeTable import *
from graphicalInterface.DatabasePanelAssistant import *
from graphicalInterface.TreeTable.AttributsBDModel import AttributsBDModel
from apriori_solver.onefile import *
from tools.SortingTools import *

class PanelPreExtraction(DatabasePanelAssistant):

    def __init__(self, contexteResolution):
        super().__init__(contexteResolution)

        self.__InitialiserContenuPanneau()

        # super().DefinirEtape(2, "Choosing rule templates", ENV.REPERTOIRE_AIDE + "preextraction_english.htm")
        # super().DefinirPanneauPrecedent(MainWindow.PANNEAU_PRE_CHARGEMENT_BD) #previous step is step 1
        # super().DefinirPanneauSuivant(MainWindow.PANNEAU_CONFIG_TECHNIQUE) #next step is algorithm chosen and set parameters
        # super().initBaseComponents()

    # def __jButtonNeRienSelectionnerActionPerformed(self, evt):
    #     super().m_contexteResolution.DefinirPositionnementPourTous(ResolutionContext.PRISE_EN_COMPTE_ITEM_NULLE_PART, False)
    #     self.__jScrollPaneAttributs.repaint() #GEN-LAST:event_jButtonNeRienSelectionnerActionPerformed

    # def __jButtonToutSelectionnerActionPerformed(self, evt):
    #     super().m_contexteResolution.DefinirPositionnementPourTous(ResolutionContext.PRISE_EN_COMPTE_ITEM_2_COTES, False)
    #     self.__jScrollPaneAttributs.repaint() #repaint this component //GEN-LAST:event_jButtonToutSelectionnerActionPerformed


    # Variables declaration - do not modify//GEN-BEGIN:variables
    # End of variables declaration//GEN-END:variables

    def __InitialiserContenuPanneau(self):
        iNombreColonnes = 0
        iIndiceColonne = 0
        iTypeNoeud = 0
        sNomColonne = None
        attributsBD = None #AttributsBDModel extends AbstractTreeTableModel
        treeTable = None #JTreeTable extends JTable
        gestionnaireBD = None
        tItems = None
        tOccurrences = None
        iIndiceItem = 0
        noeudRacine = None #noeud means node, Racine means root
        noeudCourant = None
        sDescriptionElement = None


        if self.m_contexteResolution is None:
            return

        gestionnaireBD = self.m_contexteResolution.m_gestionnaireBD

        if gestionnaireBD is None:
            return

        iNombreColonnes = gestionnaireBD.ObtenirNombreColonnesPrisesEnCompte() #Get the number of columns that are selected in the first step

        if iNombreColonnes == 0:
            return


        # attributsBD = AttributsBDModel()
        #A DefaultMutableTreeNode is a general-purpose node in a tree data structure
        # noeudRacine = attributsBD.getRoot() #return the root of the tree

        print("\nAttributes description:\n[String sNomAttribut, int iType, String sDescription, PositionRuleParameters parametresPosition, boolean bParametresConstants]\n")

        # Filling in the list of names of qualitative columns available in total in the database:  
        print("Handle qualitative columns ...")
        iIndiceColonne = 0
        while iIndiceColonne < iNombreColonnes:

            #Name of the attribute:
            colonneDonnees = gestionnaireBD.ObtenirColonneBDPriseEnCompte(iIndiceColonne)
            if colonneDonnees is not None:

                sNomColonne = str(colonneDonnees.m_sNomColonne)
                if colonneDonnees.m_iTypeValeurs == DatabaseAdmin.TYPE_VALEURS_COLONNE_ITEM:
                    sDescriptionElement = str(colonneDonnees.ObtenirNombreValeursDifferentes()) + " distinct values"
                    print(sDescriptionElement)
                    noeudCourant = [sNomColonne, AttributsBDModel.ELEMENT_MODEL_ATTRIBUT_QUAL, sDescriptionElement, self.m_contexteResolution.ObtenirInfosPostionnementRegles(), False]
                    # noeudCourant = [AttributsBDModel.AttributBDDescription(sNomColonne, AttributsBDModel.ELEMENT_MODEL_ATTRIBUT_QUAL, sDescriptionElement, self.m_contexteResolution.ObtenirInfosPostionnementRegles(), False)]
                    # print(noeudCourant)

                    # noeudCourant = attributsBD.AjouterNoeud(noeudRacine, AttributsBDModel.AttributBDDescription(sNomColonne, AttributsBDModel.ELEMENT_MODEL_ATTRIBUT_QUAL, sDescriptionElement, self.m_contexteResolution.ObtenirInfosPostionnementRegles(), False))

                    # We include in a sub-tree each of the values of the attribute:
                    # print("@@@@@@@@@@@@")
                    tItems = colonneDonnees.ConstituerTableauValeurs()
                    # print("@@@@@@@@@@@@")
                    # print("tItemsssss: " + str(tItems))
                    if tItems is not None:
                        if len(tItems) > 0:
                            # Constitution of the table listing the occurrences for every item:
                            tOccurrences = [0 for _ in range(len(tItems))]
                            iIndiceItem = 0
                            while iIndiceItem < len(tItems):
                                tOccurrences[iIndiceItem] = colonneDonnees.ObtenirNombreOccurrencesItem(tItems[iIndiceItem])
                                # print("tOccurrences: " + str(tOccurrences))
                                iIndiceItem += 1
                            # print(tItems)
                            # print(tOccurrences)
                            # Sorting items by occurrence:
                            tItems = SortingTools.CompateurBiTableaux_Chaines_Entiers(tItems, tOccurrences, False)
                            print("tItems: " + str(tItems))
                            iIndiceItem = 0
                            while iIndiceItem < len(tItems):
                                sDescriptionElement = str(colonneDonnees.ObtenirNombreOccurrencesItem(tItems[iIndiceItem])) + " occurrences."
                                # print(sDescriptionElement)
                                noeudCourant = [sNomColonne, tItems[iIndiceItem], sDescriptionElement, self.m_contexteResolution.ObtenirInfosPostionnementRegles(), False]
                                # noeudCourant = [AttributsBDModel.AttributBDDescription(sNomColonne, tItems[iIndiceItem], sDescriptionElement, self.m_contexteResolution.ObtenirInfosPostionnementRegles(), False)]
                                print(noeudCourant)

                                # attributsBD.AjouterNoeud(noeudCourant, AttributsBDModel.AttributBDDescription(sNomColonne, tItems[iIndiceItem], sDescriptionElement, self.m_contexteResolution.ObtenirInfosPostionnementRegles(), False))
                                iIndiceItem += 1
            iIndiceColonne += 1

        print("\nHandle quantitative columns ...")
        # Fill in the list of quantitative column names available in total in the database: 
        iIndiceColonne = 0
        while iIndiceColonne < iNombreColonnes:

            # Attribute name:
            colonneDonnees = gestionnaireBD.ObtenirColonneBDPriseEnCompte(iIndiceColonne)
            if colonneDonnees is not None:

                sNomColonne = str(colonneDonnees.m_sNomColonne)
                if colonneDonnees.m_iTypeValeurs == DatabaseAdmin.TYPE_VALEURS_COLONNE_REEL:

                    sDescriptionElement = "[ " + str(colonneDonnees.ObtenirBorneMin()) + ", " + str(colonneDonnees.ObtenirBorneMax()) + "]"
                    sDescriptionElement += ",  " + str(colonneDonnees.m_iNombreLignes-colonneDonnees.m_iNombreValeursReellesCorrectes) + " missing values."

                    noeudCourant = [sNomColonne, AttributsBDModel.ELEMENT_MODEL_ATTRIBUT_QUANT, sDescriptionElement, self.m_contexteResolution.ObtenirInfosPostionnementRegles(), (colonneDonnees.m_iNombreValeursReellesCorrectes<=0)]
                    print(noeudCourant)
                    # noeudCourant = attributsBD.AjouterNoeud(noeudRacine, AttributsBDModel.AttributBDDescription(sNomColonne, AttributsBDModel.ELEMENT_MODEL_ATTRIBUT_QUANT, sDescriptionElement, self.m_contexteResolution.ObtenirInfosPostionnementRegles(), (colonneDonnees.m_iNombreValeursReellesCorrectes<=0)))
            iIndiceColonne += 1


        # treeTable = JTreeTable(attributsBD)

        # Addition a posteriori of some specificities to the table:
        # attributsBD.AdapterTreeTableAModele(treeTable)

        # self.__jScrollPaneAttributs.setViewportView(treeTable)
        # self.__jScrollPaneAttributs.validate()

        self.TraitementsSpecifiquesAvantSuivant()

    def TraitementsSpecifiquesAvantSuivant(self):
        # seems like a GUI validation step
        # if not super().TraitementsSpecifiquesAvantSuivant():
        #     return False
        
        # if not super().m_contexteResolution.EstFiltreCoherent():
        # print(self.m_contexteResolution.__m_tableParametresAttributsQuantitatifs)
        # print(self.m_contexteResolution.EstFiltreCoherent())
        # sys.exit()

        if not self.m_contexteResolution.EstFiltreCoherent():
            print("\nERROR: For the procces of rule extraction to work properly, you need to specify an attribute on the left-hand side of the rules and a different one on the right-hand side")
            return False

        # super().m_contexteResolution.MettreAJourDonneesInternesFiltre()
        # super().contexteResolution.MettreAJourDonneesInternesFiltre()
        self.m_contexteResolution.MettreAJourDonneesInternesFiltre()

        return True
