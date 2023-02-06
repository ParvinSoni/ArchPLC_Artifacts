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

class DialogGraphQuality(javax.swing.JDialog):


    class PanneauGrapheQualite(JPanel):




        def __init__(self, outerInstance, iNombrePoints, iLargeurGraphe, iHauteurGraphe):
            self.__m_graphe = None
            self.__m_iLargeurGraphe = 0
            self.__m_iHauteurGraphe = 0
            self.m_iNombrePoints = 0
            self.m_tQualiteMoyenne = None
            self.m_tQualiteMin = None
            self.m_tQualiteMax = None
            self.__m_fQualiteMax = 0.0f
            self.__m_fQualiteMin = 0.0f
            self.__m_iPositionYAxeAbscisse = 0
            self.__m_fontEchelle = None

            self.__outerInstance = outerInstance


            self.__m_iLargeurGraphe = iLargeurGraphe
            self.__m_iHauteurGraphe = iHauteurGraphe

            self.m_iNombrePoints = iNombrePoints

            self.__m_fontEchelle = UtilDraw.ChargerFonte("arial.ttf")
            if self.__m_fontEchelle is not None:
                self.__m_fontEchelle = self.__m_fontEchelle.deriveFont(11.0f)
            else:
                self.__m_fontEchelle = Font("Dialog", Font.BOLD|Font.ITALIC, 10)

            self.__m_graphe = BufferedImage(self.__m_iLargeurGraphe, self.__m_iHauteurGraphe, BufferedImage.TYPE_INT_RGB)



        def __CalculerPointsCulminants(self):
            iIndicePoint = 0

            self.__m_fQualiteMax = self.m_tQualiteMax[0]
            iIndicePoint = 0
            while iIndicePoint<self.m_iNombrePoints:
                if self.__m_fQualiteMax < self.m_tQualiteMax[iIndicePoint]:
                    self.__m_fQualiteMax = self.m_tQualiteMax[iIndicePoint]
                iIndicePoint += 1

            self.__m_fQualiteMin = self.m_tQualiteMin[0]
            iIndicePoint = 0
            while iIndicePoint<self.m_iNombrePoints:
                if self.__m_fQualiteMin > self.m_tQualiteMin[iIndicePoint]:
                    self.__m_fQualiteMin = self.m_tQualiteMin[iIndicePoint]
                iIndicePoint += 1


        def __DessinerPoint(self, gc, x, y):
            gc.drawLine(x, y, x, y)


        def DessinerGraphe(self):
            gc = None
            iIndicePoint = 0
            fEchelleQualite = 0.0f

            if (m_tQualiteMoyenne is None) or (m_tQualiteMax is None) or (m_tQualiteMin is None):
                return

            self.__CalculerPointsCulminants()

            # Trac� des composantes communes du dessin :
            gc = self.__m_graphe.createGraphics()

            gc.setStroke(BasicStroke(2.0f, BasicStroke.CAP_SQUARE, BasicStroke.JOIN_MITER))

            # Effacement du fond de la fen�tre :
            gc.setColor(Color.WHITE)
            gc.fillRect(0, 0, self.__m_iLargeurGraphe, self.__m_iHauteurGraphe)

            # Trac� des axes :
            gc.setColor(Color.BLACK)


            if (self.__m_fQualiteMax-self.__m_fQualiteMin) == 0.0f:
                return
            elif (self.__m_fQualiteMax >= 0.0f) and (self.__m_fQualiteMin >= 0.0f):
                self.__m_iPositionYAxeAbscisse = self.__m_iHauteurGraphe-20
                fEchelleQualite = (float((self.__m_iHauteurGraphe-40))) / self.__m_fQualiteMax
            elif (self.__m_fQualiteMax <= 0.0f) and (self.__m_fQualiteMin <= 0.0f):
                self.__m_iPositionYAxeAbscisse = 20
                fEchelleQualite = (float((self.__m_iHauteurGraphe-40))) / (-self.__m_fQualiteMin)
            elif (self.__m_fQualiteMax * self.__m_fQualiteMin) < 0.0f:
                self.__m_iPositionYAxeAbscisse = 20 + int(((float((self.__m_iHauteurGraphe-40))) * (self.__m_fQualiteMax / (self.__m_fQualiteMax-self.__m_fQualiteMin))))
                fEchelleQualite = (float((self.__m_iHauteurGraphe-40))) / (self.__m_fQualiteMax-self.__m_fQualiteMin)


            # Axe vertical :
            gc.drawLine(20, self.__m_iHauteurGraphe-20, 20, 20)
            gc.drawLine(20, 20, 20-10, 20+10)
            gc.drawLine(20, 20, 20+10, 20+10)
            gc.drawLine(20, self.__m_iHauteurGraphe-20, 20-10, self.__m_iHauteurGraphe-20-10)
            gc.drawLine(20, self.__m_iHauteurGraphe-20, 20+10, self.__m_iHauteurGraphe-20-10)

            # Axe horizontal :
            gc.drawLine(20, self.__m_iPositionYAxeAbscisse, self.__m_iLargeurGraphe-20, self.__m_iPositionYAxeAbscisse)
            gc.drawLine(self.__m_iLargeurGraphe-20, self.__m_iPositionYAxeAbscisse, self.__m_iLargeurGraphe-20-10, self.__m_iPositionYAxeAbscisse-10)
            gc.drawLine(self.__m_iLargeurGraphe-20, self.__m_iPositionYAxeAbscisse, self.__m_iLargeurGraphe-20-10, self.__m_iPositionYAxeAbscisse+10)


            # Trac� des courbes d'�volution de la qualit� :

            # Qualit� moyenne :
            gc.setColor(Color.BLUE)
            iIndicePoint = 0
            while iIndicePoint<self.m_iNombrePoints:
                self.__DessinerPoint(gc, 20+iIndicePoint, self.__m_iPositionYAxeAbscisse-int((self.m_tQualiteMoyenne[iIndicePoint]*fEchelleQualite)))
                iIndicePoint += 1

            # Qualit� max :
            gc.setColor(Color.RED)
            iIndicePoint = 0
            while iIndicePoint<self.m_iNombrePoints:
                self.__DessinerPoint(gc, 20+iIndicePoint, self.__m_iPositionYAxeAbscisse-int((self.m_tQualiteMax[iIndicePoint]*fEchelleQualite)))
                iIndicePoint += 1

            # Qualit� min :
            gc.setColor(Color.GREEN)
            iIndicePoint = 0
            while iIndicePoint<self.m_iNombrePoints:
                self.__DessinerPoint(gc, 20+iIndicePoint, self.__m_iPositionYAxeAbscisse-int((self.m_tQualiteMin[iIndicePoint]*fEchelleQualite)))
                iIndicePoint += 1

            # Bornes :
            gc.setColor(Color.BLACK)
            gc.setFont(self.__m_fontEchelle)
            gc.drawString(String.valueOf(self.__m_fQualiteMax), 10, 18)
            gc.drawString(String.valueOf(self.__m_fQualiteMin), 10, self.__m_iHauteurGraphe-8)


        def paintComponent(self, g):
            g2D = None

            super().paintComponent(g)

            g2D = g

            g2D.drawImage(self.__m_graphe, AffineTransformOp(AffineTransform(), AffineTransformOp.TYPE_NEAREST_NEIGHBOR), 0, 0)






    #* Creates new form DialogGrapheQualite 
    def __init__(self, parent, modal, contexteResolution):
        self.__m_panneauGrapheQualite = None
        self.__m_tQualiteMoyenne = None
        self.__m_tQualiteMin = None
        self.__m_tQualiteMax = None
        self.__jButtonFermer = None
        self.__jScrollGrapheQualite = None

        super().__init__(parent, modal)
        self.__initComponents()

        setSize(600, 600)
        validate()


    #    * This method is called from within the constructor to
    #     * initialize the form.
    #     * WARNING: Do NOT modify this code. The content of this method is
    #     * always regenerated by the Form Editor.
    #     
    def __initComponents(self):
        self.__jButtonFermer = javax.swing.JButton()
        self.__jScrollGrapheQualite = javax.swing.JScrollPane()

        getContentPane().setLayout(None)

        setDefaultCloseOperation(javax.swing.WindowConstants.DISPOSE_ON_CLOSE)
        setResizable(False)
        addWindowListener(WindowAdapterAnonymousInnerClass(self))

        self.__jButtonFermer.setText("Close")
        self.__jButtonFermer.addActionListener(ActionListenerAnonymousInnerClass(self))

        getContentPane().add(self.__jButtonFermer)
        self.__jButtonFermer.setBounds(333, 160, 90, 26)

        getContentPane().add(self.__jScrollGrapheQualite)
        self.__jScrollGrapheQualite.setBounds(0, 0, 430, 150)

        pack() #GEN-END:initComponents

    class WindowAdapterAnonymousInnerClass(java.awt.event.WindowAdapter):

        def __init__(self, outerInstance):
            self.__outerInstance = outerInstance

        def windowClosing(self, evt):
            outerInstance.__closeDialog(evt)

    class ActionListenerAnonymousInnerClass(java.awt.event.ActionListener):

        def __init__(self, outerInstance):
            self.__outerInstance = outerInstance

        def actionPerformed(self, evt):
            outerInstance.__jButtonFermerActionPerformed(evt)

    def __jButtonFermerActionPerformed(self, evt):
        self.__FermerBoiteDialogue() #GEN-LAST:event_jButtonFermerActionPerformed

    #* Closes the dialog 
    def __closeDialog(self, evt):
        self.__FermerBoiteDialogue() #GEN-LAST:event_closeDialog


    def __FermerBoiteDialogue(self):
        setVisible(False)
        dispose()


    # Variables declaration - do not modify//GEN-BEGIN:variables
    # End of variables declaration//GEN-END:variables



    # Repositionne chaque contr�le pour remplir au mieux l'espace de la fen�tre :
    def ArrangerDisposition(self):
        tailleZoneFenetre = None

        tailleZoneFenetre = getContentPane().getSize()

        self.__jScrollGrapheQualite.setBounds(0, 0, tailleZoneFenetre.width, tailleZoneFenetre.height-(self.__jButtonFermer.getHeight()+20))
        self.__jButtonFermer.setLocation(tailleZoneFenetre.width-self.__jButtonFermer.getWidth()-20, self.__jScrollGrapheQualite.getHeight()+10)



    def SpecifierQualitesMoyennes(self, tQualiteMoyenne):
        self.__m_tQualiteMoyenne = tQualiteMoyenne



    def SpecifierQualitesMax(self, tQualiteMax):
        self.__m_tQualiteMax = tQualiteMax



    def SpecifierQualitesMin(self, tQualiteMin):
        self.__m_tQualiteMin = tQualiteMin



    def ConstruireGraphe(self):
        iNombrePoints = 0

        iNombrePoints = len(self.__m_tQualiteMoyenne)
        self.__m_panneauGrapheQualite = PanneauGrapheQualite(self, iNombrePoints, 50+iNombrePoints, 500)

        self.__m_panneauGrapheQualite.m_tQualiteMoyenne = self.__m_tQualiteMoyenne
        self.__m_panneauGrapheQualite.m_tQualiteMax = self.__m_tQualiteMax
        self.__m_panneauGrapheQualite.m_tQualiteMin = self.__m_tQualiteMin

        self.__m_panneauGrapheQualite.DessinerGraphe()

        self.__jScrollGrapheQualite.setViewportView(self.__m_panneauGrapheQualite)
        self.__jScrollGrapheQualite.validate()

        self.ArrangerDisposition()
        validate()

