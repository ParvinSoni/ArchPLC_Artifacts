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

from src.solver import *
from src.tools import *



class DialogSaveProfile(javax.swing.JDialog):




    SELECTION_UTILISATEUR_ANNULER = 0 #user cancel saving profile
    SELECTION_UTILISATEUR_ENREGISTRER = 1 #user save profile


    # Classe permettant de maintenir les donn�es internes � la bo�te de dialogue, m�me apr�s sa fermeture :
    class DialogEnregistrementProfil_Donnees(object):


        def __init__(self, outerInstance):
            self.m_iSelectionUtilisateur = 0
            self.m_iMasqueEnregistrement = 0

            self.__outerInstance = outerInstance

            self.m_iSelectionUtilisateur = SELECTION_UTILISATEUR_ANNULER
            self.m_iMasqueEnregistrement = 0




    #The dialog of save a profile
    def __init__(self, iPanneauCourant, parent, modal):
        self.m_iPanneauCourant = MainWindow.PANNEAU_AUCUN
        self.m_iMasqueEnregistrement = 0
        self.m_donnees = None
        self.__jButtonAide = None
        self.__jButtonAnnuler = None
        self.__jButtonSauvegarder = None
        self.__jCheckBoxApriori = None
        self.__jCheckBoxChargementRegles = None
        self.__jCheckBoxGenetique = None
        self.__jCheckBoxPreChargement = None
        self.__jCheckBoxPreExtraction = None
        self.__jCheckBoxRecuit = None
        self.__jLabelTechniques = None
        self.__jPanelGeneral = None
        self.__jPanelSelection = None

        super().__init__(parent, modal)

        iMasqueEnregistrement = 0

        iMasqueEnregistrement = 0
        self.m_iPanneauCourant = iPanneauCourant

        self.__initComponents()

        self.m_donnees = DialogEnregistrementProfil_Donnees(self)


        if self.m_iPanneauCourant == MainWindow.PANNEAU_PRE_CHARGEMENT_BD:
            iMasqueEnregistrement = ResolutionContext.PROFIL_INFO_PRECHARGEMENT

        elif self.m_iPanneauCourant == MainWindow.PANNEAU_PRE_EXTRACION:
            iMasqueEnregistrement = ResolutionContext.PROFIL_INFO_PRECHARGEMENT | ResolutionContext.PROFIL_INFO_PREEXTRACTION

        elif self.m_iPanneauCourant == MainWindow.PANNEAU_CONFIG_TECHNIQUE:
            iMasqueEnregistrement = ResolutionContext.PROFIL_INFO_PRECHARGEMENT | ResolutionContext.PROFIL_INFO_PREEXTRACTION | ResolutionContext.PROFIL_INFO_ALGO_APRIORI | ResolutionContext.PROFIL_INFO_ALGO_GENETIQUE | ResolutionContext.PROFIL_INFO_ALGO_RECUIT | ResolutionContext.PROFIL_INFO_ALGO_CHARGEMENT

        self.__jCheckBoxPreChargement.setEnabled((iPanneauCourant==MainWindow.PANNEAU_PRE_CHARGEMENT_BD) or (iPanneauCourant==MainWindow.PANNEAU_PRE_EXTRACION) or (iPanneauCourant==MainWindow.PANNEAU_CONFIG_TECHNIQUE))
        self.__jCheckBoxPreExtraction.setEnabled((iPanneauCourant==MainWindow.PANNEAU_PRE_EXTRACION) or (iPanneauCourant==MainWindow.PANNEAU_CONFIG_TECHNIQUE))
        self.__jCheckBoxApriori.setEnabled(iPanneauCourant == MainWindow.PANNEAU_CONFIG_TECHNIQUE)
        self.__jCheckBoxGenetique.setEnabled(iPanneauCourant == MainWindow.PANNEAU_CONFIG_TECHNIQUE)
        self.__jCheckBoxRecuit.setEnabled(iPanneauCourant == MainWindow.PANNEAU_CONFIG_TECHNIQUE)
        self.__jCheckBoxChargementRegles.setEnabled(iPanneauCourant == MainWindow.PANNEAU_CONFIG_TECHNIQUE)

        self.__jCheckBoxPreChargement.setSelected((iMasqueEnregistrement & ResolutionContext.PROFIL_INFO_PRECHARGEMENT) != 0)
        self.__jCheckBoxPreExtraction.setSelected((iMasqueEnregistrement & ResolutionContext.PROFIL_INFO_PREEXTRACTION) != 0)
        self.__jCheckBoxApriori.setSelected((iMasqueEnregistrement & ResolutionContext.PROFIL_INFO_ALGO_APRIORI) != 0)
        self.__jCheckBoxGenetique.setSelected((iMasqueEnregistrement & ResolutionContext.PROFIL_INFO_ALGO_GENETIQUE) != 0)
        self.__jCheckBoxRecuit.setSelected((iMasqueEnregistrement & ResolutionContext.PROFIL_INFO_ALGO_RECUIT) != 0)
        self.__jCheckBoxChargementRegles.setSelected((iMasqueEnregistrement & ResolutionContext.PROFIL_INFO_ALGO_CHARGEMENT) != 0)

        setLocationRelativeTo(None)



    def LierStructureDonnees(self):
        return self.m_donnees



    def __MemoriserSelectionsUtilisateur(self):
        iMasqueEnregistrement = 0


        if self.m_iPanneauCourant == MainWindow.PANNEAU_PRE_CHARGEMENT_BD:
            if self.__jCheckBoxPreChargement.isSelected():
                iMasqueEnregistrement |= ResolutionContext.PROFIL_INFO_PRECHARGEMENT

        elif self.m_iPanneauCourant == MainWindow.PANNEAU_PRE_EXTRACION:
            if self.__jCheckBoxPreChargement.isSelected():
                iMasqueEnregistrement |= ResolutionContext.PROFIL_INFO_PRECHARGEMENT
            if self.__jCheckBoxPreExtraction.isSelected():
                iMasqueEnregistrement |= ResolutionContext.PROFIL_INFO_PREEXTRACTION

        elif self.m_iPanneauCourant == MainWindow.PANNEAU_CONFIG_TECHNIQUE:
            if self.__jCheckBoxPreChargement.isSelected():
                iMasqueEnregistrement |= ResolutionContext.PROFIL_INFO_PRECHARGEMENT
            if self.__jCheckBoxPreExtraction.isSelected():
                iMasqueEnregistrement |= ResolutionContext.PROFIL_INFO_PREEXTRACTION
            if self.__jCheckBoxApriori.isSelected():
                iMasqueEnregistrement |= ResolutionContext.PROFIL_INFO_ALGO_APRIORI
            if self.__jCheckBoxGenetique.isSelected():
                iMasqueEnregistrement |= ResolutionContext.PROFIL_INFO_ALGO_GENETIQUE
            if self.__jCheckBoxRecuit.isSelected():
                iMasqueEnregistrement |= ResolutionContext.PROFIL_INFO_ALGO_RECUIT
            if self.__jCheckBoxChargementRegles.isSelected():
                iMasqueEnregistrement |= ResolutionContext.PROFIL_INFO_ALGO_CHARGEMENT

        self.m_donnees.m_iMasqueEnregistrement = iMasqueEnregistrement

        return (iMasqueEnregistrement != 0)



    # <editor-fold defaultstate="collapsed" desc=" Generated Code ">//GEN-BEGIN:initComponents
    def __initComponents(self):
        self.__jPanelGeneral = javax.swing.JPanel()
        self.__jPanelSelection = javax.swing.JPanel()
        self.__jCheckBoxPreExtraction = javax.swing.JCheckBox()
        self.__jCheckBoxPreChargement = javax.swing.JCheckBox()
        self.__jCheckBoxApriori = javax.swing.JCheckBox()
        self.__jLabelTechniques = javax.swing.JLabel()
        self.__jCheckBoxGenetique = javax.swing.JCheckBox()
        self.__jCheckBoxRecuit = javax.swing.JCheckBox()
        self.__jCheckBoxChargementRegles = javax.swing.JCheckBox()
        self.__jButtonSauvegarder = javax.swing.JButton()
        self.__jButtonAnnuler = javax.swing.JButton()
        self.__jButtonAide = javax.swing.JButton()

        setResizable(False)
        addWindowListener(WindowAdapterAnonymousInnerClass(self))

        self.__jPanelGeneral.setLayout(None)

        self.__jPanelGeneral.setPreferredSize(java.awt.Dimension(460, 420))
        self.__jPanelSelection.setLayout(None)

        self.__jPanelSelection.setBorder(javax.swing.BorderFactory.createTitledBorder(None, "Choice of the information to memorize in the profile file:", javax.swing.border.TitledBorder.DEFAULT_JUSTIFICATION, javax.swing.border.TitledBorder.DEFAULT_POSITION, java.awt.Font("Dialog", 3, 12)))
        self.__jCheckBoxPreExtraction.setText("Filter for positioning attributes/values in rules")
        self.__jPanelSelection.add(self.__jCheckBoxPreExtraction)
        self.__jCheckBoxPreExtraction.setBounds(10, 80, 410, 23)

        self.__jCheckBoxPreChargement.setText("Filter for loading database attributes")
        self.__jPanelSelection.add(self.__jCheckBoxPreChargement)
        self.__jCheckBoxPreChargement.setBounds(10, 40, 410, 23)

        self.__jCheckBoxApriori.setText(" 'Apriori'algorithm qualitatif")
        self.__jPanelSelection.add(self.__jCheckBoxApriori)
        self.__jCheckBoxApriori.setBounds(50, 150, 260, 23)

        self.__jLabelTechniques.setFont(java.awt.Font("Dialog", 3, 12))
        self.__jLabelTechniques.setText("Rules mining parameters:")
        self.__jPanelSelection.add(self.__jLabelTechniques)
        self.__jLabelTechniques.setBounds(20, 120, 360, 16)

        self.__jCheckBoxGenetique.setText("Genetic algorithm")
        self.__jPanelSelection.add(self.__jCheckBoxGenetique)
        self.__jCheckBoxGenetique.setBounds(50, 180, 190, 23)

        self.__jCheckBoxRecuit.setText("Simulated annealing ")
        self.__jPanelSelection.add(self.__jCheckBoxRecuit)
        self.__jCheckBoxRecuit.setBounds(50, 210, 180, 23)

        self.__jCheckBoxChargementRegles.setText("Loading a rules file")
        self.__jPanelSelection.add(self.__jCheckBoxChargementRegles)
        self.__jCheckBoxChargementRegles.setBounds(50, 240, 270, 23)

        self.__jPanelGeneral.add(self.__jPanelSelection)
        self.__jPanelSelection.setBounds(10, 40, 440, 290)
        self.__jPanelSelection.getAccessibleContext().setAccessibleName("Information to memorize in the profile:")

        self.__jButtonSauvegarder.setText("Save profile")
        self.__jButtonSauvegarder.addActionListener(ActionListenerAnonymousInnerClass(self))

        self.__jPanelGeneral.add(self.__jButtonSauvegarder)
        self.__jButtonSauvegarder.setBounds(110, 350, 270, 23)

        self.__jButtonAnnuler.setText("Cancel")
        self.__jButtonAnnuler.addActionListener(ActionListenerAnonymousInnerClass2(self))

        self.__jPanelGeneral.add(self.__jButtonAnnuler)
        self.__jButtonAnnuler.setBounds(200, 380, 100, 23)

        self.__jButtonAide.setText("?")
        self.__jButtonAide.addActionListener(ActionListenerAnonymousInnerClass3(self))

        self.__jPanelGeneral.add(self.__jButtonAide)
        self.__jButtonAide.setBounds(398, 11, 50, 23)

        getContentPane().add(self.__jPanelGeneral, java.awt.BorderLayout.CENTER)

        pack() # </editor-fold>//GEN-END:initComponents

    class WindowAdapterAnonymousInnerClass(java.awt.event.WindowAdapter):

        def __init__(self, outerInstance):
            self.__outerInstance = outerInstance

        def windowClosing(self, evt):
            outerInstance.__closeDialog(evt)

    class ActionListenerAnonymousInnerClass(java.awt.event.ActionListener):

        def __init__(self, outerInstance):
            self.__outerInstance = outerInstance

        def actionPerformed(self, evt):
            outerInstance.__jButtonSauvegarderActionPerformed(evt)

    class ActionListenerAnonymousInnerClass2(java.awt.event.ActionListener):

        def __init__(self, outerInstance):
            self.__outerInstance = outerInstance

        def actionPerformed(self, evt):
            outerInstance.__jButtonAnnulerActionPerformed(evt)

    class ActionListenerAnonymousInnerClass3(java.awt.event.ActionListener):

        def __init__(self, outerInstance):
            self.__outerInstance = outerInstance

        def actionPerformed(self, evt):
            outerInstance.__jButtonAideActionPerformed(evt)



    def __jButtonAideActionPerformed(self, evt):
        dialogAide = DialogHelp(ENV.REPERTOIRE_AIDE+"profils.htm", None, True)
        dialogAide.show() #GEN-LAST:event_jButtonAideActionPerformed



    def __jButtonAnnulerActionPerformed(self, evt):
        self.m_donnees.m_iSelectionUtilisateur = SELECTION_UTILISATEUR_ANNULER
        setVisible(False)
        dispose() #GEN-LAST:event_jButtonAnnulerActionPerformed



    def __jButtonSauvegarderActionPerformed(self, evt):
        if self.__MemoriserSelectionsUtilisateur():
            self.m_donnees.m_iSelectionUtilisateur = SELECTION_UTILISATEUR_ENREGISTRER
            setVisible(False)
            dispose()
        else:
            JOptionPane.showMessageDialog(None, "Veuillez choisir au moins une cat�gorie de param�tres � enregistrer !", "Erreur", JOptionPane.ERROR_MESSAGE) #GEN-LAST:event_jButtonSauvegarderActionPerformed



    def __closeDialog(self, evt):
        setVisible(False)
        dispose() #GEN-LAST:event_closeDialog

    #    *
    #     * @param args the command line arguments
    #     
    @staticmethod
    def main(args):
        (DialogSaveProfile(0, javax.swing.JFrame(), True)).show()


    # Variables declaration - do not modify//GEN-BEGIN:variables
    # End of variables declaration//GEN-END:variables

