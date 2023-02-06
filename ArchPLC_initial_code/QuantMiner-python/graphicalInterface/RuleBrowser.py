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

from src.apriori import *
from src.solver import *
from src.tools import *

#
#The com.sun.image.codec.jpeg.* package is deprecated for Java versions after 7. 
#This import statement is therefore commented out to avoid the "not found" error messages that appear when this package is called.
#Removing this line of code does not change the functionality of any component of QuantMiner.
#
#import com.sun.image.codec.jpeg.*

class RuleBrowser(javax.swing.JPanel):

    __serialVersionUID = 1






    def __init__(self, contexteResolution):
        self.__m_contexteResolution = None
        self.__m_fontEnTete = None
        self.__m_fontItems = None
        self.__m_fontDetails = None
        self.__m_iIndiceRegleAffichee = 0
        self.__m_tReglesFiltrees = None
        self.__m_dimensionConteneur = None

        self.__m_tReglesFiltrees = None
        self.__m_iIndiceRegleAffichee = 0

        self.__m_contexteResolution = contexteResolution

        self.__m_dimensionConteneur = getSize()

        #title font
        self.__m_fontEnTete = UtilDraw.ChargerFonte("font_tahomabd.ttf")
        if self.__m_fontEnTete is not None:
            self.__m_fontEnTete = self.__m_fontEnTete.deriveFont(14.0f)
        else:
            self.__m_fontEnTete = Font("Dialog", Font.BOLD|Font.ITALIC, 12)

        #item font
        self.__m_fontItems = UtilDraw.ChargerFonte("font_timesbi.ttf")
        if self.__m_fontItems is not None:
            self.__m_fontItems = self.__m_fontItems.deriveFont(11.0f)
        else:
            self.__m_fontItems = Font("Dialog", Font.BOLD|Font.ITALIC, 10)

        #details font
        self.__m_fontDetails = UtilDraw.ChargerFonte("arial.ttf")
        if self.__m_fontDetails is not None:
            self.__m_fontDetails = self.__m_fontDetails.deriveFont(11.0f)
        else:
            self.__m_fontDetails = Font("Dialog", Font.BOLD|Font.ITALIC, 10)


    #define a list of rules
    def DefinirListeRegles(self, tReglesFiltrees):
        self.__m_tReglesFiltrees = tReglesFiltrees


    #define the index of a rule and repaint the rule panel
    def DefinirIndiceRegleAffichee(self, iIndiceRegleAffichee):
        self.__m_iIndiceRegleAffichee = iIndiceRegleAffichee
        repaint()



    def ObtenirIndiceRegleAffichee(self):
        return self.__m_iIndiceRegleAffichee


    def DefinirDimensionConteneur(self, largeur, hauteur):
        self.__m_dimensionConteneur = Dimension(largeur, hauteur)


    def PeindreRegle(self, iNumeroRegle, regle, iY, iLargeurZone, g2D):
        frc = None
        layout = None
        mesuresFont = None
        item = None
        itemQuant = None
        iLargeurMaxi = 0
        iLargeurMaxiGauche = 0
        iLargeurMaxiDroite = 0
        iIndiceItem = 0
        fHauteurCumulee = 0.0f
        fHauteurCumuleeGauche = 0.0f
        fHauteurCumuleeDroite = 0.0f
        fHauteurCumuleeElement = 0.0f
        fHauteurHautAccolade = 0.0f
        fMilieuItems = 0.0f
        sTexte = None
        fMaxHauteur = 0.0f
        ancienPinceau = None
        iNombreLignesBD = 0
        iPositionMilieuZone = 0
        fValeurConfiance = 0.0f
        fAmplitudeDomaine = 0.0f
        fBorneMin = 0.0f
        fBorneMax = 0.0f
        fProportionMin = 0.0f
        fProportionMax = 0.0f
        bItemsQualitatifsPresents = False
        bPremierItemInscrit = False
        iIndiceDisjonction = 0
        iNombreDisjonctions = 0
        iNombreItemsQuantitatifs = 0
        iIndiceCoteRegle = 0
        iPositionTexteX = 0
        iNombreItems = 0
        tItemsRegle = None
        iPositionItemsQuantX = 0
        iLargeurMaxItemsQuantX = 0

        if regle is None:
            return 0.0f

        #set title font
        g2D.setFont(self.__m_fontEnTete)
        g2D.setColor(Color(255, 30, 50))
        frc = g2D.getFontRenderContext()

        iPositionMilieuZone = math.trunc(iLargeurZone / float(2))
        iLargeurMaxiGauche = iLargeurMaxiDroite = math.trunc((iLargeurZone - 140) / float(2))

        sTexte = String.valueOf(iNumeroRegle) + ". "
        sTexte += "SUPPORT = "
        sTexte += String.valueOf(regle.m_iOccurrences)
        sTexte += " ("
        sTexte += ResolutionContext.EcrirePourcentage(regle.m_fSupport, 2, True)
        sTexte += ") , CONFIDENCE = "
        sTexte += ResolutionContext.EcrirePourcentage(regle.m_fConfiance, 2, True)
        sTexte += "  :  "

        mesuresFont = self.__m_fontEnTete.getLineMetrics(sTexte, frc)
        g2D.drawString(sTexte, 20, iY+mesuresFont.getAscent())

        layout = TextLayout(sTexte, self.__m_fontEnTete, frc)
        fHauteurCumulee = float((layout.getBounds()).getHeight()) + 20.0f

        g2D.setFont(self.__m_fontItems)
        frc = g2D.getFontRenderContext()

        # left side and right side:
        for iIndiceCoteRegle in range(0, 2):
            #left side
            if iIndiceCoteRegle==0:
                iNombreItems = regle.m_iNombreItemsGauche
                tItemsRegle = regle.m_tItemsGauche
                iNombreItemsQuantitatifs = regle.CompterItemsGaucheSelonType(Item.ITEM_TYPE_QUANTITATIF)
                iNombreDisjonctions = regle.m_iNombreDisjonctionsGaucheValides
                iLargeurMaxi = iLargeurMaxiGauche
                iPositionTexteX = 20
            else:
                iNombreItems = regle.m_iNombreItemsDroite
                tItemsRegle = regle.m_tItemsDroite
                iNombreItemsQuantitatifs = regle.CompterItemsDroiteSelonType(Item.ITEM_TYPE_QUANTITATIF)
                iNombreDisjonctions = regle.m_iNombreDisjonctionsDroiteValides
                iLargeurMaxi = iLargeurMaxiDroite
                iPositionTexteX = iLargeurMaxiGauche + 120

            fHauteurCumuleeElement = fHauteurCumulee


            g2D.setColor(Color(85, 34, 0))

            bPremierItemInscrit = False
            iIndiceItem = 0
            while iIndiceItem < iNombreItems:
                item = tItemsRegle[iIndiceItem]
                if item.m_iTypeItem == Item.ITEM_TYPE_QUALITATIF:
                    if bPremierItemInscrit:
                        fHauteurCumuleeElement += 15.0f
                    fHauteurCumuleeElement += UtilDraw.PeindreTexteLimite(item.toString(), iLargeurMaxi, iPositionTexteX, iY+int(fHauteurCumuleeElement), g2D)
                    bPremierItemInscrit = True
                iIndiceItem += 1
            bItemsQualitatifsPresents = bPremierItemInscrit


            # Next display quantitative items:

            if iNombreItemsQuantitatifs > 0:

                g2D.setColor(Color(19, 45, 91))

                if bItemsQualitatifsPresents:
                    fHauteurCumuleeElement += 15.0f

                if iNombreDisjonctions > 1:
                    iPositionItemsQuantX = iPositionTexteX+20
                    iLargeurMaxItemsQuantX = iLargeurMaxi-40
                else:
                    iPositionItemsQuantX = iPositionTexteX
                    iLargeurMaxItemsQuantX = iLargeurMaxi

                iIndiceDisjonction = 0
                while iIndiceDisjonction < iNombreDisjonctions:

                    if iIndiceDisjonction>0:
                        fHauteurCumuleeElement += 30.0f + UtilDraw.PeindreTexteCentreLimite("OR", iLargeurMaxi-40, iPositionTexteX+20, iY+int(fHauteurCumuleeElement)+15, g2D)

                    fHauteurHautAccolade = fHauteurCumuleeElement

                    bPremierItemInscrit = False
                    iIndiceItem = 0
                    while iIndiceItem < iNombreItems:
                        item = tItemsRegle[iIndiceItem]
                        if item.m_iTypeItem == Item.ITEM_TYPE_QUANTITATIF:
                            if bPremierItemInscrit:
                                fHauteurCumuleeElement += 15.0f
                            fHauteurCumuleeElement += UtilDraw.PeindreTexteLimite((item).toString(iIndiceDisjonction), iLargeurMaxItemsQuantX, iPositionItemsQuantX, iY+int(fHauteurCumuleeElement), g2D)
                            bPremierItemInscrit = True
                        iIndiceItem += 1

                    # Display accolades about des items quantitatifs : 
                    if iNombreDisjonctions > 1:
                        ancienPinceau = g2D.getStroke()
                        g2D.setStroke(BasicStroke(2.0f))
                        fMilieuItems = fHauteurHautAccolade + (fHauteurCumuleeElement - fHauteurHautAccolade)/2
                        UtilDraw.PeindreAccolade(iPositionTexteX+10, float(iY) + fMilieuItems, (fHauteurCumuleeElement-fHauteurHautAccolade)/2 + 2.0f, True, g2D)
                        UtilDraw.PeindreAccolade(iPositionTexteX+10+iLargeurMaxi-20, float(iY) + fMilieuItems, (fHauteurCumuleeElement-fHauteurHautAccolade)/2 + 2.0f, False, g2D)
                        g2D.setStroke(ancienPinceau)
                    iIndiceDisjonction += 1


            if iIndiceCoteRegle == 0:
                fHauteurCumuleeGauche = fHauteurCumuleeElement
            else:
                fHauteurCumuleeDroite = fHauteurCumuleeElement



        fMaxHauteur = Math.max(fHauteurCumuleeGauche, fHauteurCumuleeDroite) - fHauteurCumulee
        fMilieuItems = fHauteurCumulee + fMaxHauteur/2

        g2D.setColor(Color.BLACK)
        g2D.setPaint(Color.BLACK)

        # Display de la fl�che :
        UtilDraw.PeindreFleche(iLargeurMaxiGauche+35, iY + int(fMilieuItems), g2D)

        # Display des accolades :
        ancienPinceau = g2D.getStroke()
        g2D.setStroke(BasicStroke(2.0f))

        UtilDraw.PeindreAccolade(10.0f, float(iY) + fMilieuItems, fMaxHauteur/2 + 2.0f, True, g2D)
        UtilDraw.PeindreAccolade(iLargeurMaxiGauche+30.0f, float(iY) + fMilieuItems, fMaxHauteur/2 + 2.0f, False, g2D)
        UtilDraw.PeindreAccolade(iLargeurMaxiGauche+110.0f, float(iY) + fMilieuItems, fMaxHauteur/2 + 2.0f, True, g2D)
        UtilDraw.PeindreAccolade(iLargeurMaxiGauche+iLargeurMaxiDroite+130.0f, float(iY) + fMilieuItems, fMaxHauteur/2 + 2.0f, False, g2D)

        g2D.setStroke(ancienPinceau)

        # Display the indicator of the 2 parties of the rule:
        g2D.setFont(self.__m_fontEnTete)
        g2D.drawString("A", 3, iY+int(fHauteurCumulee)+2)
        g2D.drawString("B", iLargeurMaxiGauche+103, iY+int(fHauteurCumulee)+2)

        fHauteurCumulee += fMaxHauteur

        #set detail font
        g2D.setFont(self.__m_fontDetails)
        g2D.setColor(Color.BLACK)

        fHauteurCumulee += 15.0f

        #display the percentage bar
        #left and right side
        for iIndiceCoteRegle in range(0, 2):
            #left side
            if iIndiceCoteRegle==0:
                iNombreItems = regle.m_iNombreItemsGauche
                tItemsRegle = regle.m_tItemsGauche
                iNombreItemsQuantitatifs = regle.CompterItemsGaucheSelonType(Item.ITEM_TYPE_QUANTITATIF)
                iNombreDisjonctions = regle.m_iNombreDisjonctionsGaucheValides
            else:
                iNombreItems = regle.m_iNombreItemsDroite
                tItemsRegle = regle.m_tItemsDroite
                iNombreItemsQuantitatifs = regle.CompterItemsDroiteSelonType(Item.ITEM_TYPE_QUANTITATIF)
                iNombreDisjonctions = regle.m_iNombreDisjonctionsDroiteValides


            if iNombreItemsQuantitatifs > 0:
                fHauteurCumulee += 15.0f
                if iIndiceCoteRegle==0:
                    fHauteurCumulee += 15.0f # + UtilDessin.PeindreTexteLimite("PROPORTIONS DU DOMAINE COUVERT PAR LES INTERVALLES DE LA PARTIE LEFT :", iLargeurZone-20, 10, iY+(int)fHauteurCumulee, g2D);
                else:
                    fHauteurCumulee += 15.0f # + UtilDessin.PeindreTexteLimite("PROPORTIONS DU DOMAINE COUVERT PAR LES INTERVALLES DE LA PARTIE RIGHT :", iLargeurZone-20, 10, iY+(int)fHauteurCumulee, g2D);


            if iNombreItemsQuantitatifs > 0:
                iIndiceDisjonction = 0
                while iIndiceDisjonction < iNombreDisjonctions:

                    if iIndiceDisjonction > 0:
                        fHauteurCumulee += 10.0f

                    fHauteurHautAccolade = fHauteurCumulee
                    iIndiceItem = 0
                    while iIndiceItem < iNombreItems:

                        item = tItemsRegle[iIndiceItem]
                        if item.m_iTypeItem == Item.ITEM_TYPE_QUANTITATIF:

                            itemQuant = item
                            UtilDraw.PeindreTexteLimite(itemQuant.m_attributQuant.ObtenirNom()+" :", 90, 30, iY+int(fHauteurCumulee), g2D)
                            g2D.drawRect(130, iY+int(fHauteurCumulee), 300, 10)

                            fBorneMin = itemQuant.m_attributQuant.m_colonneDonnees.ObtenirBorneMin()
                            fBorneMax = itemQuant.m_attributQuant.m_colonneDonnees.ObtenirBorneMax()
                            fAmplitudeDomaine = fBorneMax - fBorneMin

                            if fAmplitudeDomaine != 0.0f:
                                fProportionMin = (itemQuant.ObtenirBorneMinIntervalle(iIndiceDisjonction) - fBorneMin) / fAmplitudeDomaine
                                fProportionMax = (itemQuant.ObtenirBorneMaxIntervalle(iIndiceDisjonction) - fBorneMin) / fAmplitudeDomaine
                            else:
                                fProportionMin = fProportionMax = 0.0f

                            iTailleProportionAffichee = 0

                            iTailleProportionAffichee = int(((fProportionMax-fProportionMin)*300.0f))
                            if iTailleProportionAffichee < 1:
                                iTailleProportionAffichee = 1

                            g2D.fillRect(130+int((fProportionMin*300.0f)), iY+int(fHauteurCumulee), iTailleProportionAffichee, 10)

                            sTexte = ResolutionContext.EcrirePourcentage((fProportionMax-fProportionMin), 2, True) + " of ["
                            sTexte += String.valueOf(fBorneMin) + ", " + String.valueOf(fBorneMax) + "]"

                            UtilDraw.PeindreTexteLimite(sTexte, iLargeurZone-460, 450, iY+int(fHauteurCumulee), g2D)

                            fHauteurCumulee += 20.0f
                        iIndiceItem += 1

                    ancienPinceau = g2D.getStroke()
                    g2D.setStroke(BasicStroke(2.0f))
                    UtilDraw.PeindreAccolade(20, float(iY)+fHauteurHautAccolade+(fHauteurCumulee-10.0f-fHauteurHautAccolade)/2, (fHauteurCumulee-10.0f-fHauteurHautAccolade)/2 + 2.0f, True, g2D)
                    g2D.setStroke(ancienPinceau)
                    iIndiceDisjonction += 1


        # Display the mesures suppl�mentaires :
        iNombreLignesBD = self.__m_contexteResolution.m_gestionnaireBD.ObtenirNombreLignes()

        fHauteurCumulee += 20.0f
        fHauteurCumuleeGauche = fHauteurCumulee
        fHauteurCumuleeDroite = fHauteurCumulee

        g2D.setFont(self.__m_fontDetails)

        #Display the supports :
        g2D.setColor(Color.BLUE)
        UtilDraw.PeindreTexteLimite("SUPPORTS :", 100, 10, iY+int(fHauteurCumuleeGauche), g2D)
        fHauteurCumuleeGauche += 20.0f

        UtilDraw.PeindreTexteLimite("A and B", 80, 10, iY+int(fHauteurCumuleeGauche), g2D)
        g2D.fill3DRect(100, iY+int(fHauteurCumuleeGauche), math.trunc((120*regle.m_iOccurrences) / float(iNombreLignesBD)), 10, True)
        UtilDraw.PeindreTexteLimite(self.__m_contexteResolution.EcrireSupport(regle.m_iOccurrences), 90, 230, iY+int(fHauteurCumuleeGauche), g2D)
        fHauteurCumuleeGauche += 15.0f

        UtilDraw.PeindreTexteLimite("A", 80, 10, iY+int(fHauteurCumuleeGauche), g2D)
        g2D.fill3DRect(100, iY+int(fHauteurCumuleeGauche), math.trunc((120*regle.m_iOccurrencesGauche) / float(iNombreLignesBD)), 10, True)
        UtilDraw.PeindreTexteLimite(self.__m_contexteResolution.EcrireSupport(regle.m_iOccurrencesGauche), 90, 230, iY+int(fHauteurCumuleeGauche), g2D)
        fHauteurCumuleeGauche += 15.0f

        UtilDraw.PeindreTexteLimite("B", 80, 10, iY+int(fHauteurCumuleeGauche), g2D)
        g2D.fill3DRect(100, iY+int(fHauteurCumuleeGauche), math.trunc((120*regle.m_iOccurrencesDroite) / float(iNombreLignesBD)), 10, True)
        UtilDraw.PeindreTexteLimite(self.__m_contexteResolution.EcrireSupport(regle.m_iOccurrencesDroite), 90, 230, iY+int(fHauteurCumuleeGauche), g2D)
        fHauteurCumuleeGauche += 15.0f

        UtilDraw.PeindreTexteLimite("A and (~B)", 80, 10, iY+int(fHauteurCumuleeGauche), g2D)
        g2D.fill3DRect(100, iY+int(fHauteurCumuleeGauche), math.trunc((120*regle.m_iOccurrences_Gauche_NonDroite) / float(iNombreLignesBD)), 10, True)
        UtilDraw.PeindreTexteLimite(self.__m_contexteResolution.EcrireSupport(regle.m_iOccurrences_Gauche_NonDroite), 90, 230, iY+int(fHauteurCumuleeGauche), g2D)
        fHauteurCumuleeGauche += 15.0f

        UtilDraw.PeindreTexteLimite("(~A) and B", 80, 10, iY+int(fHauteurCumuleeGauche), g2D)
        g2D.fill3DRect(100, iY+int(fHauteurCumuleeGauche), math.trunc((120*regle.m_iOccurrences_NonGauche_Droite) / float(iNombreLignesBD)), 10, True)
        UtilDraw.PeindreTexteLimite(self.__m_contexteResolution.EcrireSupport(regle.m_iOccurrences_NonGauche_Droite), 90, 230, iY+int(fHauteurCumuleeGauche), g2D)
        fHauteurCumuleeGauche += 15.0f

        UtilDraw.PeindreTexteLimite("(~A) and (~B)", 80, 10, iY+int(fHauteurCumuleeGauche), g2D)
        g2D.fill3DRect(100, iY+int(fHauteurCumuleeGauche), math.trunc((120*regle.m_iOccurrences_NonGauche_NonDroite) / float(iNombreLignesBD)), 10, True)
        UtilDraw.PeindreTexteLimite(self.__m_contexteResolution.EcrireSupport(regle.m_iOccurrences_NonGauche_NonDroite), 90, 230, iY+int(fHauteurCumuleeGauche), g2D)
        fHauteurCumuleeGauche += 15.0f


        # Display the confidences :
        g2D.setColor(Color.RED)
        UtilDraw.PeindreTexteLimite("CONFIDENCES:", 100, iPositionMilieuZone+10, iY+int(fHauteurCumuleeDroite), g2D)
        fHauteurCumuleeDroite += 20.0f

        fValeurConfiance = (float(regle.m_iOccurrences)) / (float(regle.m_iOccurrencesGauche))
        UtilDraw.PeindreTexteLimite("A -> B", 80, iPositionMilieuZone+10, iY+int(fHauteurCumuleeDroite), g2D)
        g2D.fill3DRect(iPositionMilieuZone+100, iY+int(fHauteurCumuleeDroite), int((120.0f*fValeurConfiance)), 10, True)
        UtilDraw.PeindreTexteLimite(ResolutionContext.EcrirePourcentage(fValeurConfiance, 2, True), 90, iPositionMilieuZone+230, iY+int(fHauteurCumuleeDroite), g2D)
        fHauteurCumuleeDroite += 15.0f

        UtilDraw.PeindreTexteLimite("(~A) -> B", 80, iPositionMilieuZone+10, iY+int(fHauteurCumuleeDroite), g2D)
        if (iNombreLignesBD - regle.m_iOccurrencesGauche) == 0:
            UtilDraw.PeindreTexteLimite("ind�termin� car 'non A' n'apparait jamais dans la BD.", 220, iPositionMilieuZone+100, iY+int(fHauteurCumuleeDroite), g2D)
        else:
            fValeurConfiance = (float(regle.m_iOccurrences_NonGauche_Droite)) / (float((iNombreLignesBD - regle.m_iOccurrencesGauche)))
            g2D.fill3DRect(iPositionMilieuZone+100, iY+int(fHauteurCumuleeDroite), int((120.0f*fValeurConfiance)), 10, True)
            UtilDraw.PeindreTexteLimite(ResolutionContext.EcrirePourcentage(fValeurConfiance, 2, True), 90, iPositionMilieuZone+230, iY+int(fHauteurCumuleeDroite), g2D)
        fHauteurCumuleeDroite += 15.0f

        fValeurConfiance = (float(regle.m_iOccurrences)) / (float(regle.m_iOccurrencesDroite))
        UtilDraw.PeindreTexteLimite("B -> A", 80, iPositionMilieuZone+10, iY+int(fHauteurCumuleeDroite), g2D)
        g2D.fill3DRect(iPositionMilieuZone+100, iY+int(fHauteurCumuleeDroite), int((120.0f*fValeurConfiance)), 10, True)
        UtilDraw.PeindreTexteLimite(ResolutionContext.EcrirePourcentage(fValeurConfiance, 2, True), 90, iPositionMilieuZone+230, iY+int(fHauteurCumuleeDroite), g2D)
        fHauteurCumuleeDroite += 15.0f

        UtilDraw.PeindreTexteLimite("(~B) -> A", 80, iPositionMilieuZone+10, iY+int(fHauteurCumuleeDroite), g2D)
        if (iNombreLignesBD - regle.m_iOccurrencesDroite) == 0:
            UtilDraw.PeindreTexteLimite("ind�termin� car 'non B' n'apparait jamais dans la BD.", 220, iPositionMilieuZone+100, iY+int(fHauteurCumuleeDroite), g2D)
        else:
            fValeurConfiance = (float(regle.m_iOccurrences_Gauche_NonDroite)) / (float((iNombreLignesBD - regle.m_iOccurrencesDroite)))
            g2D.fill3DRect(iPositionMilieuZone+100, iY+int(fHauteurCumuleeDroite), int((120.0f*fValeurConfiance)), 10, True)
            UtilDraw.PeindreTexteLimite(ResolutionContext.EcrirePourcentage(fValeurConfiance, 2, True), 90, iPositionMilieuZone+230, iY+int(fHauteurCumuleeDroite), g2D)
        fHauteurCumuleeDroite += 30.0f

        fValeurConfiance = (float((regle.m_iOccurrences + regle.m_iOccurrences_NonGauche_NonDroite))) / (float(iNombreLignesBD))
        UtilDraw.PeindreTexteLimite("A <-> B", 80, iPositionMilieuZone+10, iY+int(fHauteurCumuleeDroite), g2D)
        g2D.fill3DRect(iPositionMilieuZone+100, iY+int(fHauteurCumuleeDroite), int((120.0f*fValeurConfiance)), 10, True)
        UtilDraw.PeindreTexteLimite(ResolutionContext.EcrirePourcentage(fValeurConfiance, 2, True), 90, iPositionMilieuZone+230, iY+int(fHauteurCumuleeDroite), g2D)
        fHauteurCumuleeDroite += 15.0f

        # Trac� du s�parateur entre infos de support et infos de confiance :
        fMaxHauteur = Math.max(fHauteurCumuleeGauche, fHauteurCumuleeDroite)

        g2D.setColor(Color.BLACK)
        g2D.drawLine(iPositionMilieuZone, iY+(int(fHauteurCumulee))+5, iPositionMilieuZone, iY+(int(fMaxHauteur))-10)

        fHauteurCumulee = fMaxHauteur

        return fHauteurCumulee



    @staticmethod
    def antialias(g):
        g2 =  g
        g2.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_ON)
        g2.setRenderingHint(RenderingHints.KEY_FRACTIONALMETRICS, RenderingHints.VALUE_FRACTIONALMETRICS_ON)
        # Enable antialiasing for shapes
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON)
        return g2

    def paintComponent(self, g):
        g2D = None
        regle = None
        fHauteurCumulee = 0.0f

        g2D = antialias(g)


        super().paintComponent(g)

        if (m_tReglesFiltrees is None) or (self.__m_iIndiceRegleAffichee<0):
            fHauteurCumulee = float((self.__m_dimensionConteneur.height/2-12))
            g2D.setFont(self.__m_fontEnTete)
            g2D.setColor(Color(255, 30, 50))
            fHauteurCumulee += UtilDraw.PeindreTexteCentreLimite("No rule returned for the selected critera.", getWidth(), 0, int(fHauteurCumulee), g2D)
            setPreferredSize(Dimension(getWidth(), int(fHauteurCumulee)))
            revalidate()
            return


        try:
            fHauteurCumulee = 10.0f
            regle = self.__m_tReglesFiltrees[self.__m_iIndiceRegleAffichee]
            fHauteurCumulee += 10.0f + self.PeindreRegle(1+self.__m_iIndiceRegleAffichee, regle, int(fHauteurCumulee), getWidth(), g2D)
            setPreferredSize(Dimension(getWidth(), int(fHauteurCumulee)))
            revalidate()
        except IndexOutOfBoundsException as e:
            pass




    # Enregistre dans un fichier JPEG la repr�sentation graphique de la r�gle :
    def EnregistrerImageRegle(self, regle, iIndiceRegle, sCheminFichier):
        imageRegle = None
        contexteImage = None
        fichierImage = None
        fluxSortieImage = None
        #        
        #        The com.sun.image.codec.jpeg.* package is deprecated for Java versions after 7. 
        #        JPEGImageEncoder (encoderJPEG) is part of this package, and therefore this block of code is commented out to avoid the "not found" error messages that appear when it is included.
        #        Removing this block of code does not change the functionality of any component of QuantMiner.
        #        
        #JPEGImageEncoder encoderJPEG = null;g
        bProcessusInterrompu = False
        iLargeur = 0
        iHauteur = 0

        if (sCheminFichier is None) or (regle is None):
            return

        iLargeur = 950
        iHauteur = 1
        imageRegle = BufferedImage(iLargeur, iHauteur, BufferedImage.TYPE_INT_RGB)

        contexteImage = antialias(imageRegle.createGraphics())

        if contexteImage is not None:

            if self.__m_tReglesFiltrees is not None:

                bProcessusInterrompu = False

                # On peint l'image une premi�re fois pour calculer sa hauteur :
                contexteImage.setColor(Color.WHITE)
                contexteImage.fillRect(0, 0, iLargeur, iHauteur)
                iHauteur = 10 + int(self.PeindreRegle(1+iIndiceRegle, regle, 10, iLargeur, contexteImage))
                contexteImage = None
                imageRegle = None

                # Puis on la peint une seconde fois dans une image � la bonne dimension :
                imageRegle = BufferedImage(iLargeur, iHauteur, BufferedImage.TYPE_INT_RGB)
                contexteImage = imageRegle.createGraphics()
                if contexteImage is not None:

                    contexteImage.setColor(Color.WHITE)
                    contexteImage.fillRect(0, 0, iLargeur, iHauteur)
                    self.PeindreRegle(1+iIndiceRegle, regle, 10, iLargeur, contexteImage)

                    try:
                        fichierImage = File(sCheminFichier)
                        fluxSortieImage = FileOutputStream(fichierImage)
                    except FileNotFoundException as e1:
                        bProcessusInterrompu = True
                    except SecurityException as e2:
                        bProcessusInterrompu = True

                    #                    
                    #                    The com.sun.image.codec.jpeg.* package is deprecated for Java versions after 7. 
                    #                    JPEGImageEncoder (encoderJPEG) is part of this package this package, and therefore this block of code is commented out to avoid the "not found" error messages that appear when it is included.
                    #                    Removing this block of code does not change the functionality of any component of QuantMiner.
                    #                    
                    #                    try {
                    #                        encoderJPEG = JPEGCodec.createJPEGEncoder(fluxSortieImage)
                    #                        encoderJPEG.encode(imageRegle)
                    #                    }
                    #                    catch (IOException e1) {}
                    #                    catch (ImageFormatException e2) {}

                    try:
                        fluxSortieImage.close()
                    except IOException as e:
                        pass


