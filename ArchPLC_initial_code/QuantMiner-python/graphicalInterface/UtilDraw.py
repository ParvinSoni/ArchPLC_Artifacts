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

from src.tools import *



class UtilDraw(object):


    @staticmethod
    def ChargerFonte(sNomFichier):
        fontStream = None
        font = None

        try:
            fontStream = FileInputStream(ENV.REPERTOIRE_RESSOURCES + sNomFichier)
            font = Font.createFont(Font.TRUETYPE_FONT, fontStream)
            fontStream.close()
        except IOException as e:
            font = None
        except FontFormatException as e:
            print(e)
            font = None

        return font



    @staticmethod
    def PeindreTexteCentreLimite(sTexte, iLargeurMax, iX, iY, g2D):
        iLargeurTexte = 0
        fontCourante = None
        frc = None
        layout = None
        contourTexte = None

        if g2D is None:
            return 0.0f

        fontCourante = g2D.getFont()
        if fontCourante is None:
            return 0.0f

        frc = g2D.getFontRenderContext()

        layout = TextLayout(sTexte, fontCourante, frc)
        contourTexte = layout.getBounds()

        iLargeurTexte = int(contourTexte.getWidth())
        if iLargeurTexte > iLargeurMax:
            iLargeurTexte = iLargeurMax

        return PeindreTexteLimite(sTexte, iLargeurMax-math.trunc((iLargeurMax-iLargeurTexte) / float(2)), iX+math.trunc((iLargeurMax-iLargeurTexte) / float(2)), iY, g2D)


    #draw text boundary 
    @staticmethod
    def PeindreTexteLimite(sTexte, iLargeurMax, iX, iY, g2D):
        fontCourante = None
        frc = None
        layout = None
        layout3Points = None
        hitInfo = None
        mesuresFont = None
        contourTexte = None
        sTextePeint = None
        fLargeur3Points = 0.0f # Largeur de la cha�ne "..."
        fHauteurTexte = 0.0f

        if g2D is None:
            return 0.0f

        fontCourante = g2D.getFont()
        if fontCourante is None:
            return 0.0f

        frc = g2D.getFontRenderContext()

        layout = TextLayout(sTexte, fontCourante, frc)
        contourTexte = layout.getBounds()
        fHauteurTexte = float(contourTexte.getHeight())

        if contourTexte.getWidth() > float(iLargeurMax):

            # Calcul de la distance n�cessaire au trac� de la cha�ne "..." indiquant qu'on a tronqu� le texte :
            layout3Points = TextLayout("...", fontCourante, frc)
            fLargeur3Points = float(((layout3Points.getBounds()).getWidth()))

            # Construction de la nouvelle cha�ne, tronqu�e :
            if fLargeur3Points >= float(iLargeurMax):
                sTexte = "..."
            else:
                hitInfo = layout.hitTestChar((float(iLargeurMax)) - fLargeur3Points, 0.0f)
                sTexte = sTexte[0:hitInfo.getCharIndex()] + "..."

        mesuresFont = fontCourante.getLineMetrics(sTexte, frc)
        g2D.drawString(sTexte, iX, iY+mesuresFont.getAscent())

        return fHauteurTexte



    @staticmethod
    def PeindreFleche(iPosFlecheX, iPosFlecheY, g2D):
        elementFleche = None

        elementFleche = Polygon()
        elementFleche.addPoint(iPosFlecheX, iPosFlecheY-5)
        elementFleche.addPoint(iPosFlecheX+10, iPosFlecheY)
        elementFleche.addPoint(iPosFlecheX, iPosFlecheY+5)
        elementFleche.addPoint(iPosFlecheX+45, iPosFlecheY+2)
        elementFleche.addPoint(iPosFlecheX+40, iPosFlecheY+10)
        elementFleche.addPoint(iPosFlecheX+70, iPosFlecheY)
        elementFleche.addPoint(iPosFlecheX+40, iPosFlecheY-10)
        elementFleche.addPoint(iPosFlecheX+45, iPosFlecheY-2)

        g2D.fill(elementFleche)



    @staticmethod
    def PeindreAccolade(fPosX, fPosMilieuY, fTaille, bOuvrante, g2D):
        fCoeffSens = 0.0f

        if bOuvrante:
            fCoeffSens = 1.0f
        else:
            fCoeffSens = -1.0f

        pointAccolade = None

        pointAccolade = [None for _ in range(7)]

        pointAccolade[0] = Point2D.Float(fPosX + 10.0f*fCoeffSens, fPosMilieuY - fTaille)
        pointAccolade[1] = Point2D.Float(fPosX + 5.0f*fCoeffSens, fPosMilieuY - fTaille + 4.0f)
        pointAccolade[2] = Point2D.Float(fPosX + 5.0f*fCoeffSens, fPosMilieuY - 4.0f)
        pointAccolade[3] = Point2D.Float(fPosX, fPosMilieuY)
        pointAccolade[4] = Point2D.Float(pointAccolade[2].x, fPosMilieuY + 5.0f)
        pointAccolade[5] = Point2D.Float(pointAccolade[1].x, fPosMilieuY + fTaille - 5.0f)
        pointAccolade[6] = Point2D.Float(pointAccolade[0].x, fPosMilieuY + fTaille)

        accolade = GeneralPath()
        accolade.append(Line2D.Float(pointAccolade[0], pointAccolade[1]), False)
        accolade.append(Line2D.Float(pointAccolade[1], pointAccolade[2]), False)
        accolade.append(Line2D.Float(pointAccolade[2], pointAccolade[3]), False)
        accolade.append(Line2D.Float(pointAccolade[3], pointAccolade[4]), False)
        accolade.append(Line2D.Float(pointAccolade[4], pointAccolade[5]), False)
        accolade.append(Line2D.Float(pointAccolade[5], pointAccolade[6]), False)

        g2D.draw(accolade)


