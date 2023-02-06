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

from src.apriori import *
from src.solver import *




class PanelRuleGraphs(JPanel):




    def __init__(self, contexteResolution, iIndiceRegle):
        self.__m_contexteResolution = None
        self.__m_graphes = None
        self.__m_regle = None
        self.__m_iLargeurGraphe = 0
        self.__m_iHauteurGraphe = 0
        self.__m_fontItem = None

        iNombreTotalItems = 0
        iIndiceItem = 0

        self.__m_contexteResolution = contexteResolution
        self.__m_regle = None

        if self.__m_contexteResolution.m_listeRegles is None:
            return

        try:
            self.__m_regle = self.__m_contexteResolution.m_listeRegles[iIndiceRegle]
        except IndexOutOfBoundsException as e:
            return

        if self.__m_regle is None:
            return


        # Chargement des ressources utilis�es pour l'affichage des r�gles :
        self.__m_fontItem = UtilDraw.ChargerFonte("font_tahomabd.ttf")
        if self.__m_fontItem is not None:
            self.__m_fontItem = self.__m_fontItem.deriveFont(12.0f)
        else:
            self.__m_fontItem = Font("Dialog", Font.BOLD|Font.ITALIC, 12)


        iNombreTotalItems = self.__m_regle.m_iNombreItemsGauche + self.__m_regle.m_iNombreItemsDroite
        self.__m_iLargeurGraphe = 256
        self.__m_iHauteurGraphe = 300

        self.__m_graphes = [None for _ in range(iNombreTotalItems)]
        iIndiceItem = 0
        while iIndiceItem<iNombreTotalItems:
            self.__m_graphes[iIndiceItem] = BufferedImage(self.__m_iLargeurGraphe, self.__m_iHauteurGraphe, BufferedImage.TYPE_INT_RGB)
            self.DessinerGraphe(iIndiceItem)
            iIndiceItem += 1



    def DessinerGraphe(self, iIndiceItem):
        graphe = None
        item = None
        itemQual = None
        itemQuant = None
        gc = None
        sNomItem = None

        if self.__m_regle is None:
            return

        graphe = self.__m_graphes[iIndiceItem]

        if iIndiceItem < self.__m_regle.m_iNombreItemsGauche:
            item = self.__m_regle.ObtenirItemGauche(iIndiceItem)
        else:
            item = self.__m_regle.ObtenirItemDroite(iIndiceItem - self.__m_regle.m_iNombreItemsGauche)

        if item is None:
            return

        if item.m_iTypeItem == Item.ITEM_TYPE_QUALITATIF:
            itemQual = item
        elif item.m_iTypeItem == Item.ITEM_TYPE_QUANTITATIF:
            itemQuant = item
        else:
            return


        # Trac� des composantes communes du dessin :
        gc = graphe.createGraphics()

        gc.setStroke(BasicStroke(2.0f, BasicStroke.CAP_SQUARE, BasicStroke.JOIN_MITER))

        # Effacement du fond de la fen�tre :
        gc.setColor(Color.WHITE)
        gc.fillRect(0, 0, self.__m_iLargeurGraphe, self.__m_iHauteurGraphe)

        # Trac� des axes :
        gc.setColor(Color.BLACK)

        gc.drawLine(20, self.__m_iLargeurGraphe-20, 20, 20)
        gc.drawLine(20, 20, 20-(10*self.__m_iLargeurGraphe)/256, 20+(10*self.__m_iHauteurGraphe)/300)
        gc.drawLine(20, 20, 20+(10*self.__m_iLargeurGraphe)/256, 20+(10*self.__m_iHauteurGraphe)/300)

        gc.drawLine(20, self.__m_iLargeurGraphe-20, self.__m_iHauteurGraphe-20, self.__m_iHauteurGraphe-20)
        gc.drawLine(self.__m_iLargeurGraphe-20, self.__m_iLargeurGraphe-20, self.__m_iHauteurGraphe-20-(10*self.__m_iHauteurGraphe)/300, self.__m_iHauteurGraphe-20-(10*self.__m_iHauteurGraphe)/300)
        gc.drawLine(self.__m_iLargeurGraphe-20, self.__m_iLargeurGraphe-20, self.__m_iHauteurGraphe-20-(10*self.__m_iHauteurGraphe)/300, self.__m_iHauteurGraphe-20+(10*self.__m_iHauteurGraphe)/300)

        gc.setFont(self.__m_fontItem)

        # Trac� des composantes du dessin relatives � un item qualitatif :
        # Trac� des composantes du dessin relatives � un item quantitatif :



    def paintComponent(self, g):
        g2D = None
        iNombreTotalItems = 0
        iIndiceItem = 0

        super().paintComponent(g)

        if self.__m_regle is None:
            return

        iNombreTotalItems = self.__m_regle.m_iNombreItemsGauche + self.__m_regle.m_iNombreItemsDroite

        g2D = g

        iIndiceItem = 0
        while iIndiceItem<iNombreTotalItems:
            g2D.drawImage(self.__m_graphes[iIndiceItem], AffineTransformOp(AffineTransform(), AffineTransformOp.TYPE_NEAREST_NEIGHBOR), iIndiceItem * (20+self.__m_iLargeurGraphe), 0)
            iIndiceItem += 1


