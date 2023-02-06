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



from graphicalInterface.TableEvolvedCells import *
from graphicalInterface.TreeTable.AbstractTreeTableModel import AbstractTreeTableModel
from graphicalInterface.TreeTable.TreeTableModel import TreeTableModel
from apriori_solver import *



class AttributsBDModel(AbstractTreeTableModel):

    # Default column names:
    tNomsDefaut = ["Attribute / Value", "Informations", "Position in the rule", "Present necessarily"]
    # Common names of columns:

    # Types of columns:
    tTypes = [TreeTableModel, str, str, str]

    # Editing possibilities:
    tEditable = [True, False, True, True]

    # Options of the column indicating the position of the chosen item:
    tComboBoxPositionsItem = ["2 sides", "left-hand side (condition)", "right-hand side (conclusion)", "nowhere"]
    tComboBoxPositionsAttribut = ["variable", "2 sides", "left-hand side (condition)", "right-hand side (conclusion)", "nowhere"]

    ELEMENT_MODEL_ATTRIBUT_QUAL = 0
    ELEMENT_MODEL_ATTRIBUT_QUANT = 1
    ELEMENT_MODEL_ITEM = 2

    class AttributBDDescription(object):

        def _initialize_instance_fields(self):
            self.__m_sNomAttribut = None
            self.__m_sNomItem = None
            self.__m_iType = 0
            self.__m_sDescription = None
            self.__m_parametresPosition = None
            self.__m_bParametresConstants = False




        def __init__(self, sNomAttribut, iType, sDescription, parametresPosition, bParametresConstants):
            self._initialize_instance_fields()

            self.__m_sNomAttribut = sNomAttribut
            self.__m_sNomItem = None
            self.__m_iType = self.__m_iType
            self.__m_sDescription = sDescription
            self.__m_parametresPosition = parametresPosition
            self.__m_bParametresConstants = bParametresConstants


        def __init__(self, sNomAttribut, sNomItem, sDescription, parametresPosition, bParametresConstants):
            self._initialize_instance_fields()

            self.__m_sNomAttribut = sNomAttribut
            self.__m_sNomItem = sNomItem
            self.__m_iType = AttributsBDModel.ELEMENT_MODEL_ITEM
            self.__m_sDescription = sDescription
            self.__m_parametresPosition = parametresPosition
            self.__m_bParametresConstants = bParametresConstants


        def ObtenirNomAttribut(self):
            if self.__m_iType == self.ELEMENT_MODEL_ITEM:
                return self.__m_sNomItem
            else:
                return self.__m_sNomAttribut


        def ObtenirInformation(self):
            return self.__m_sDescription


        def EstItem(self):
            return (self.__m_iType == ELEMENT_MODEL_ITEM)


        def ObtenirPositionItem(self):
            iPositionItem = 0

            if self.EstItem():
                iPositionItem = self.__m_parametresPosition.ObtenirTypePrisEnCompteItem(self.__m_sNomAttribut, self.__m_sNomItem)
            else:
                iPositionItem = self.__m_parametresPosition.ObtenirTypePrisEnCompteAttribut(self.__m_sNomAttribut)


            if iPositionItem == ResolutionContext.PRISE_EN_COMPTE_INDEFINI:
                return "variable"

            if (iPositionItem == ResolutionContext.PRISE_EN_COMPTE_INDEFINI) or (iPositionItem == ResolutionContext.PRISE_EN_COMPTE_ITEM_GAUCHE):
                return "left-hand side (condition)"

            if (iPositionItem == ResolutionContext.PRISE_EN_COMPTE_INDEFINI) or (iPositionItem == ResolutionContext.PRISE_EN_COMPTE_ITEM_GAUCHE) or (iPositionItem == ResolutionContext.PRISE_EN_COMPTE_ITEM_DROITE):
                return "right-hand side (conclusion)"

            if (iPositionItem == ResolutionContext.PRISE_EN_COMPTE_INDEFINI) or (iPositionItem == ResolutionContext.PRISE_EN_COMPTE_ITEM_GAUCHE) or (iPositionItem == ResolutionContext.PRISE_EN_COMPTE_ITEM_DROITE) or (iPositionItem == ResolutionContext.PRISE_EN_COMPTE_ITEM_2_COTES):
                return "2 sides"


            if True:
                return "nowhere"



        def DefinirPositionItem(self, sPositionItem):
            iPositionItem = 0

            if self.__m_bParametresConstants:
                return

            if sPositionItem == "2 sides":
                iPositionItem = ResolutionContext.PRISE_EN_COMPTE_ITEM_2_COTES

            elif sPositionItem == "left-hand side (condition)":
                iPositionItem = ResolutionContext.PRISE_EN_COMPTE_ITEM_GAUCHE

            elif sPositionItem == "right-hand side (conclusion)":
                iPositionItem = ResolutionContext.PRISE_EN_COMPTE_ITEM_DROITE

            elif sPositionItem == "nowhere":
                iPositionItem = ResolutionContext.PRISE_EN_COMPTE_ITEM_NULLE_PART

            if self.EstItem():
                if not((iPositionItem==ResolutionContext.PRISE_EN_COMPTE_ITEM_NULLE_PART) and (self.__m_parametresPosition.ObtenirPresenceObligatoireItem(self.__m_sNomAttribut, self.__m_sNomItem))):
                    self.__m_parametresPosition.DefinirTypePrisEnCompteItem(self.__m_sNomAttribut, self.__m_sNomItem, iPositionItem)
            else:
                if not((iPositionItem==ResolutionContext.PRISE_EN_COMPTE_ITEM_NULLE_PART) and (self.__m_parametresPosition.ObtenirPresenceObligatoireAttribut(self.__m_sNomAttribut)!=0)):
                    self.__m_parametresPosition.DefinirTypePrisEnCompteAttribut(self.__m_sNomAttribut, iPositionItem)



        # Renvoie 0 pour faux, 1 pour vrai, et -1 pour indiquer que toutes les valeurs ne sont pas les m�mes
        def ObtenirPresenceObligatoireItem(self):

            if self.EstItem():
                if self.__m_parametresPosition.ObtenirPresenceObligatoireItem(self.__m_sNomAttribut, self.__m_sNomItem):
                    return 1
                else:
                    return 0
            else:
                return self.__m_parametresPosition.ObtenirPresenceObligatoireAttribut(self.__m_sNomAttribut)


        def DefinirPresenceObligatoireItem(self, bPresenceObligatoire):

            if self.__m_bParametresConstants:
                return

            if self.EstItem():
                if self.__m_parametresPosition.ObtenirTypePrisEnCompteItem(self.__m_sNomAttribut, self.__m_sNomItem) != ResolutionContext.PRISE_EN_COMPTE_ITEM_NULLE_PART:
                    self.__m_parametresPosition.DefinirPresenceObligatoireItem(self.__m_sNomAttribut, self.__m_sNomItem, bPresenceObligatoire)
            else:
                if self.__m_parametresPosition.ObtenirTypePrisEnCompteAttribut(self.__m_sNomAttribut) != ResolutionContext.PRISE_EN_COMPTE_ITEM_NULLE_PART:
                    self.__m_parametresPosition.DefinirPresenceObligatoireAttribut(self.__m_sNomAttribut, bPresenceObligatoire)



        # String displayed at a tree node:
        def toString(self):
            return self.ObtenirNomAttribut()





    def __init__(self):
        self.tNoms = None
        self.m_rendererComboAttribut = None
        self.m_treeTable = None

        # super().__init__(DefaultMutableTreeNode(None))
        super().__init__(None)

        iIndiceNom = 0
        iNombreNoms = 0

        iNombreNoms = len(self.tNomsDefaut)

        self.tNoms = [None for _ in range(iNombreNoms)]
        iIndiceNom = 0
        while iIndiceNom<iNombreNoms:
            self.tNoms[iIndiceNom] = self.tNomsDefaut[iIndiceNom]
            iIndiceNom += 1

        self.m_treeTable = None



    def ModifierNomColonne(self, iIndiceColonne, sNouveauNom):
        if iIndiceColonne < len(self.tNomsDefaut):
            self.tNoms[iIndiceColonne] = str(sNouveauNom)

    # Add some specificities to the tree-table associated with the data model:
    def AdapterTreeTableAModele(self, treeTable):
        colonneTableau = None

        # The column indicating the position of the item takes the form of a combo box:
        colonneTableau = treeTable.getColumnModel().getColumn(2)

        colonneTableau.setCellEditor(CelluleComboBoxEditor(tComboBoxPositionsItem))
        colonneTableau.setCellRenderer(CelluleComboBoxRenderer(tComboBoxPositionsItem))

        self.m_rendererComboAttribut = CelluleComboBoxRenderer(tComboBoxPositionsAttribut)


        # La colonne indiquant la position de l'item prend la forme d'une combo box :
        colonneTableau = treeTable.getColumnModel().getColumn(3)
        colonneTableau.setCellEditor(CelluleCheckButton3StatesEditor())
        colonneTableau.setCellRenderer(CelluleCheckButton3StatesRenderer())

        colonneTableau.setMaxWidth(140)
        colonneTableau.setMinWidth(140)
        colonneTableau.setPreferredWidth(140)

        self.m_treeTable = treeTable


    # AddNode
    def AjouterNoeud(self, noeudParent, attribut):

        nouveauNoeud = None

        if (noeudParent is None) or (attribut is None):
            return None

        nouveauNoeud = DefaultMutableTreeNode(attribut)

        noeudParent.add(nouveauNoeud) #add new node

        return nouveauNoeud




    #
    # M�thodes issues de l'interface 'TreeModel' :
    #

    def getChildCount(self, node):
        return (node).getChildCount()



    def getChild(self, node, i):
        return (node).getChildAt(i)



    def isLeaf(self, node):
        return (node).isLeaf()



    #
    # M�thodes issues de l'interface 'TreeTableModel' :
    #

    def getColumnCount(self):
        return len(self.tNoms)



    def getColumnName(self, column):
        return self.tNoms[column]



    def getColumnClass(self, column):
        return tTypes[column]



    def getValueAt(self, node, column):
        defaultNode = None
        attributDescription = None
        iIndicateurPresenceObligatoire = 0

        defaultNode = node
        attributDescription = (defaultNode.getUserObject())

        if attributDescription is None:
            return None

        if column == 0:
            return attributDescription.ObtenirNomAttribut()
        if (column == 0) or (column == 1):
            return attributDescription.ObtenirInformation()
        if (column == 0) or (column == 1) or (column == 2):
            return attributDescription.ObtenirPositionItem()
        if (column == 0) or (column == 1) or (column == 2) or (column == 3):
            return Integer(attributDescription.ObtenirPresenceObligatoireItem())

        return None



    def setValueAt(self, aValue, node, column):
        defaultNode = None
        attributDescription = None

        defaultNode = node
        attributDescription = (defaultNode.getUserObject())

        if attributDescription is None:
            return

        if column == 0:
            # Rien � modifier : le nom de l'attribut n'est pas �ditable
            pass
        elif column == 1:
            # Rien � modifier : l'information sur l'attribut est en lecture seule
            pass
        elif column == 2:
            if aValue is not None:
                attributDescription.DefinirPositionItem(str(aValue))
                self.IndiquerColonneChangee(2)
        elif column == 3:
            if aValue is not None:
                attributDescription.DefinirPresenceObligatoireItem(int((int(aValue))) == 1)
                self.IndiquerColonneChangee(3)



    def isCellEditable(self, node, column):
        return tEditable[column]



    def getCellRenderer(self, node, column):
        defaultNode = None
        attributDescription = None

        defaultNode = node
        attributDescription = (defaultNode.getUserObject())

        if attributDescription is None:
            return None

        if column == 0:
            return None
        if (column == 0) or (column == 1):
            return None
        if (column == 0) or (column == 1) or (column == 2):
            if not attributDescription.EstItem():
                return self.m_rendererComboAttribut
            else:
                return None
        if (column == 0) or (column == 1) or (column == 2) or (column == 3):
            return None

        return None



    def IndiquerColonneChangee(self, iColonne):
        tableModel = None
        iNombreLignes = 0

        if self.m_treeTable is None:
            return

        tableModel = self.m_treeTable.getModel()
        if tableModel is None:
            return

        iNombreLignes = tableModel.getRowCount()
        if iNombreLignes==0:
            return

        self.m_treeTable.tableChanged(TableModelEvent(tableModel, 0, iNombreLignes-1, iColonne))

