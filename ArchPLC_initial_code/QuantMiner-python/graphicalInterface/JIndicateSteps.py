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


from src.tools import *



class JIndicateSteps(JPanel):





    def __init__(self, iNumero, sIntitule):
        self.m_labelEtape = None
        self.m_labelEtapeTotal = None
        self.m_labelIntitule = None
        self.m_boutonAide = None
        self.m_sFichierAide = None

        iconeEtape = None
        iconeEtapeTotal = None
        sNomIconeEtape = None
        interieurPanneau = None

        if (iNumero<1) and (iNumero>5):
            return

        self.m_sFichierAide = None

        setLayout(None)
        setBackground(Color(160,160,192))
        setBorder(javax.swing.BorderFactory.createBevelBorder(BevelBorder.RAISED))

        interieurPanneau = self.__calculerZoneInterieurPanneau()

        if iNumero == 1:
            sNomIconeEtape = "etape_1.jpg"
        elif iNumero == 2:
            sNomIconeEtape = "etape_2.jpg"
        elif iNumero == 3:
            sNomIconeEtape = "etape_3.jpg"
        elif iNumero == 4:
            sNomIconeEtape = "etape_4.jpg"
        elif iNumero == 5:
            sNomIconeEtape = "etape_5.jpg"

        iconeEtape = ImageIcon(ENV.REPERTOIRE_RESSOURCES + sNomIconeEtape)
        iconeEtapeTotal = ImageIcon(ENV.REPERTOIRE_RESSOURCES + "drapeau_5.jpg")

        self.m_labelEtape = JLabel(iconeEtape)
        self.m_labelEtape.setSize(iconeEtape.getIconWidth(), iconeEtape.getIconHeight())

        self.m_labelEtapeTotal = JLabel(iconeEtapeTotal)
        self.m_labelEtapeTotal.setSize(iconeEtapeTotal.getIconWidth(), iconeEtapeTotal.getIconHeight())

        self.m_labelIntitule = JLabel(sIntitule)

        self.m_boutonAide = javax.swing.JButton()
        self.m_boutonAide.setText("?")

        try:
            fontStream = FileInputStream(ENV.REPERTOIRE_RESSOURCES + "font_comic.ttf")
            font = Font.createFont(Font.TRUETYPE_FONT, fontStream)
            font = font.deriveFont(Font.BOLD|Font.ITALIC, 18.0f)
            fontStream.close()
            self.m_labelIntitule.setFont(font)
            self.m_boutonAide.setFont(font)
        except IOException as e:
            pass
        except FontFormatException as e:
            pass

        add(self.m_labelEtape)
        add(self.m_labelEtapeTotal)
        add(self.m_labelIntitule)
        add(self.m_boutonAide)

        validate()

        self.RedimensionnerSelonLargeur(self.m_labelEtape.getWidth() + self.m_labelEtapeTotal.getWidth() + 100)

        self.m_boutonAide.addActionListener(ActionListenerAnonymousInnerClass(self))


    class ActionListenerAnonymousInnerClass(java.awt.event.ActionListener):

        def __init__(self, outerInstance):
            self.__outerInstance = outerInstance

        def actionPerformed(self, evt):
            outerInstance.__jButtonAideActionPerformed(evt)



    def SpecifierFichierAide(self, sFichierAide):
        self.m_sFichierAide = sFichierAide



    def __jButtonAideActionPerformed(self, evt):
        dialogAide = None

        if self.m_sFichierAide is not None:
            dialogAide = DialogHelp(self.m_sFichierAide, None, True)
            dialogAide.show()



    def __calculerZoneInterieurPanneau(self):
        bordure = None
        insets = None
        rectInterieur = None

        bordure = getBorder()

        if bordure is None:
            return Rectangle(0, 0, getWidth(), getHeight())

        rectInterieur = getBounds()
        insets = bordure.getBorderInsets(self)
        rectInterieur.x = insets.left
        rectInterieur.y = insets.top
        rectInterieur.width -= (insets.left + insets.right)
        rectInterieur.height -= (insets.bottom + insets.top)

        return rectInterieur



    # Calcule la hauteur totale prise par les bordures en haut et en bas du panneau :
    def CalculerCumulHauteurBordures(self):
        bordure = None
        insets = None

        bordure = getBorder()

        if bordure is None:
            return 0

        insets = bordure.getBorderInsets(self)

        return insets.top + insets.bottom



    def RedimensionnerSelonLargeur(self, largeur):
        iPositionXIntitule = 0
        positionElement = None
        interieurPanneau = None
        iMaxIconHeight = 0
        iTempHeight = 0
        iCumulHauteurBordures = 0

        iMaxIconHeight = self.m_labelEtape.getHeight()
        iTempHeight = self.m_labelEtapeTotal.getHeight()
        if iTempHeight> iMaxIconHeight:
            iMaxIconHeight = iTempHeight

        iCumulHauteurBordures = self.CalculerCumulHauteurBordures()

        setPreferredSize(java.awt.Dimension(largeur-20, iMaxIconHeight+iCumulHauteurBordures))
        reshape(10, 10, largeur-20, iMaxIconHeight+iCumulHauteurBordures)

        interieurPanneau = self.__calculerZoneInterieurPanneau()

        self.m_labelEtape.setLocation(interieurPanneau.x, interieurPanneau.y)
        self.m_labelEtapeTotal.setLocation(interieurPanneau.x+self.m_labelEtape.getWidth(), interieurPanneau.y)

        self.m_boutonAide.setBounds(interieurPanneau.width+interieurPanneau.x-50, interieurPanneau.y, 50, iMaxIconHeight)

        positionElement = self.m_labelEtapeTotal.getLocation()
        iPositionXIntitule = positionElement.x + self.m_labelEtapeTotal.getWidth() + 10
        self.m_labelIntitule.setBounds(iPositionXIntitule, interieurPanneau.y, interieurPanneau.width+interieurPanneau.x-iPositionXIntitule-10-self.m_boutonAide.getWidth()-10, iMaxIconHeight)

