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

from apriori_solver.onefile import *
from tools import *

from graphicalInterface.PanelBaseParam import *



class PanelQuantitativeRuleParam(PanelBaseParam):

    #* Creates new form PanneauParamRegles 
    def __init__(self, contexteResolution):
        None
        '''
        self.__jButtonDefautConfiance = None
        self.__jButtonDefautSupport = None
        self.__jButtonDefautSupportDisjonctions = None
        self.__jComboDisjonctionsDroite = None
        self.__jComboDisjonctionsGauche = None
        self.__jComboNumAssociationRules = None
        self.__jComboApplyKMeans = None
        self.__jLabelNumAssociationRules = None
        self.__jLabelApplyKMeans = None
        self.__jLabelConfiance = None
        self.__jLabelDisjonctionsDroite = None
        self.__jLabelDisjonctionsGauche = None
        self.__jLabelMaxiQuants = None
        self.__jLabelMiniQuants = None
        self.__jLabelSupport = None
        self.__jLabelSupportSupplementaire = None
        self.__jSeparatorDisjonctions = None
        self.__jTextFieldConfiance = None
        self.__jTextFieldSupport = None
        self.__jTextMaxiQuants = None
        self.__jTextMiniQuants = None
        self.__jTextSupportSupplementaire = None

        super().__init__(contexteResolution)

        iconeRetourDefaut = None

        self.__initComponents()

        if self.m_contexteResolution is None:
            return

        # Ic�nes sur les boutons :
        iconeRetourDefaut = ImageIcon(ENV.REPERTOIRE_RESSOURCES + "retour_defaut.jpg")
        self.__jButtonDefautSupport.setIcon(iconeRetourDefaut)
        self.__jButtonDefautConfiance.setIcon(iconeRetourDefaut)
        self.__jButtonDefautSupportDisjonctions.setIcon(iconeRetourDefaut)


        # Initialisation du contenu des champs :
        self.__jTextFieldSupport.setText(ResolutionContext.EcrirePourcentage(self.m_contexteResolution.m_parametresReglesQuantitatives.m_fMinSupp, 3, False))
        self.__jTextFieldConfiance.setText(ResolutionContext.EcrirePourcentage(self.m_contexteResolution.m_parametresReglesQuantitatives.m_fMinConf, 3, False))

        self.__jTextMiniQuants.setText(String.valueOf(self.m_contexteResolution.m_parametresReglesQuantitatives.m_iNombreMinAttributsQuant))
        self.__jTextMaxiQuants.setText(String.valueOf(self.m_contexteResolution.m_parametresReglesQuantitatives.m_iNombreMaxAttributsQuant))

        if (self.m_contexteResolution.m_parametresReglesQuantitatives.m_iNombreDisjonctionsGauche>0) and (self.m_contexteResolution.m_parametresReglesQuantitatives.m_iNombreDisjonctionsGauche<=10):
            self.__jComboDisjonctionsGauche.setSelectedIndex(self.m_contexteResolution.m_parametresReglesQuantitatives.m_iNombreDisjonctionsGauche - 1)
        else:
            self.__jComboDisjonctionsGauche.setSelectedIndex(0)

        if (self.m_contexteResolution.m_parametresReglesQuantitatives.m_iNombreDisjonctionsDroite>0) and (self.m_contexteResolution.m_parametresReglesQuantitatives.m_iNombreDisjonctionsDroite<=10):
            self.__jComboDisjonctionsDroite.setSelectedIndex(self.m_contexteResolution.m_parametresReglesQuantitatives.m_iNombreDisjonctionsDroite - 1)
        else:
            self.__jComboDisjonctionsDroite.setSelectedIndex(0)

        if (self.m_contexteResolution.m_parametresReglesQuantitatives.m_iNombreAssociationRules>0) and (self.m_contexteResolution.m_parametresReglesQuantitatives.m_iNombreAssociationRules<=10):
            self.__jComboNumAssociationRules.setSelectedIndex(0)
        else:
            self.__jComboNumAssociationRules.setSelectedIndex(0)

        if (self.m_contexteResolution.m_parametresReglesQuantitatives.m_applyKMeans>0) and (self.m_contexteResolution.m_parametresReglesQuantitatives.m_applyKMeans<=2):
            self.__jComboApplyKMeans.setSelectedIndex(self.m_contexteResolution.m_parametresReglesQuantitatives.m_applyKMeans)
        else:
            self.__jComboApplyKMeans.setSelectedIndex(0)

        self.__jTextSupportSupplementaire.setText(ResolutionContext.EcrirePourcentage(self.m_contexteResolution.m_parametresReglesQuantitatives.m_fMinSuppDisjonctions, 3, False))
    '''

    #    * This method is called from within the constructor to
    #     * initialize the form.
    #     * WARNING: Do NOT modify this code. The content of this method is
    #     * always regenerated by the Form Editor.
    #     
    # <editor-fold defaultstate="collapsed" desc=" Generated Code ">//GEN-BEGIN:initComponents
    def __initComponents(self):
        '''
        self.__jTextFieldSupport = javax.swing.JTextField()
        self.__jLabelSupport = javax.swing.JLabel()
        self.__jLabelConfiance = javax.swing.JLabel()
        self.__jTextFieldConfiance = javax.swing.JTextField()
        self.__jLabelDisjonctionsGauche = javax.swing.JLabel()
        self.__jLabelDisjonctionsDroite = javax.swing.JLabel()
        self.__jComboDisjonctionsGauche = javax.swing.JComboBox()
        self.__jComboDisjonctionsDroite = javax.swing.JComboBox()

        #is it ok that this is in english and the rest is in french?
        self.__jLabelNumAssociationRules = javax.swing.JLabel()
        self.__jLabelApplyKMeans = javax.swing.JLabel()
        self.__jComboNumAssociationRules = javax.swing.JComboBox()
        self.__jComboApplyKMeans = javax.swing.JComboBox()

        self.__jLabelMiniQuants = javax.swing.JLabel()
        self.__jTextMiniQuants = javax.swing.JTextField()
        self.__jLabelMaxiQuants = javax.swing.JLabel()
        self.__jTextMaxiQuants = javax.swing.JTextField()
        self.__jLabelSupportSupplementaire = javax.swing.JLabel()
        self.__jTextSupportSupplementaire = javax.swing.JTextField()
        self.__jSeparatorDisjonctions = javax.swing.JSeparator()
        self.__jButtonDefautSupport = javax.swing.JButton()
        self.__jButtonDefautConfiance = javax.swing.JButton()
        self.__jButtonDefautSupportDisjonctions = javax.swing.JButton()

        setLayout(None)

        #added +30 * 2to 237 because of extra 30-height row for number of top association rules to show and apply k-means to show
        setPreferredSize(java.awt.Dimension(570, 297))
        self.__jTextFieldSupport.setInputVerifier(ToolsInterface.VerifieurTextFieldIntervalleFloat(0.0, 100.0))
        add(self.__jTextFieldSupport)
        self.__jTextFieldSupport.setBounds(190, 20, 100, 19)

        self.__jLabelSupport.setText("Support threshold (%):")
        add(self.__jLabelSupport)
        self.__jLabelSupport.setBounds(20, 20, 220, 14) #160-->220

        self.__jLabelConfiance.setText("Confidence threshold  (%): ")
        add(self.__jLabelConfiance)
        self.__jLabelConfiance.setBounds(20, 50, 220, 14) #160-->220

        self.__jTextFieldConfiance.setInputVerifier(ToolsInterface.VerifieurTextFieldIntervalleFloat(0.0, 100.0))
        add(self.__jTextFieldConfiance)
        self.__jTextFieldConfiance.setBounds(190, 50, 100, 19)

        self.__jLabelDisjonctionsGauche.setText("Number of allowed disjunctions (\"OR\") in the rule left-hand side:")
        add(self.__jLabelDisjonctionsGauche)
        self.__jLabelDisjonctionsGauche.setBounds(20, 140, 380, 14)

        self.__jLabelDisjonctionsDroite.setText("Number of allowed disjunctions (\"OR\") in the rule right-hand side:")
        add(self.__jLabelDisjonctionsDroite)
        self.__jLabelDisjonctionsDroite.setBounds(20, 170, 380, 14)

        self.__jComboDisjonctionsGauche.setModel(javax.swing.DefaultComboBoxModel(["0 (only one interval)", "1", "2", "3", "4", "5", "6", "7", "8", "9"]))
        add(self.__jComboDisjonctionsGauche)
        self.__jComboDisjonctionsGauche.setBounds(400, 140, 150, 20)

        self.__jComboDisjonctionsDroite.setModel(javax.swing.DefaultComboBoxModel(["0 (only one  interval)", "1", "2", "3", "4", "5", "6", "7", "8", "9"]))
        add(self.__jComboDisjonctionsDroite)
        self.__jComboDisjonctionsDroite.setBounds(400, 170, 150, 20)

        self.__jLabelMiniQuants.setText("Number of quantitative attributes in a rule, minimum: ")
        add(self.__jLabelMiniQuants)
        self.__jLabelMiniQuants.setBounds(20, 90, 370, 14) #310--> 370

        add(self.__jTextMiniQuants)
        self.__jTextMiniQuants.setBounds(400, 90, 60, 19) #340-->400

        self.__jLabelMaxiQuants.setText("maximum:")
        add(self.__jLabelMaxiQuants)
        self.__jLabelMaxiQuants.setBounds(470, 90, 70, 14) #410 --> 470

        add(self.__jTextMaxiQuants)
        self.__jTextMaxiQuants.setBounds(550, 90, 60, 19) #490-->550

        self.__jLabelSupportSupplementaire.setText("Support threshold for additional intervals (%):")
        add(self.__jLabelSupportSupplementaire)
        self.__jLabelSupportSupplementaire.setBounds(20, 200, 340, 14)

        self.__jTextSupportSupplementaire.setInputVerifier(ToolsInterface.VerifieurTextFieldIntervalleFloat(0.0, 100.0))
        add(self.__jTextSupportSupplementaire)
        self.__jTextSupportSupplementaire.setBounds(400, 200, 100, 19)

        self.__jLabelNumAssociationRules.setText("Number of top rules per association (fitness):")
        add(self.__jLabelNumAssociationRules)
        self.__jLabelNumAssociationRules.setBounds(20, 230, 380, 14)

        self.__jComboNumAssociationRules.setModel(javax.swing.DefaultComboBoxModel(["1 (top cluster)", "2", "3", "4", "5", "6", "7", "8", "9", "10"]))
        add(self.__jComboNumAssociationRules)
        self.__jComboNumAssociationRules.setBounds(400, 230, 150, 20)

        self.__jLabelApplyKMeans.setText("Apply clustering algorithm:")
        add(self.__jLabelApplyKMeans)
        self.__jLabelApplyKMeans.setBounds(20, 260, 380, 14)

        self.__jComboApplyKMeans.setModel(javax.swing.DefaultComboBoxModel(["No (top fitness only)", "Yes (k-means)", "Yes (g-means)"]))
        add(self.__jComboApplyKMeans)
        self.__jComboApplyKMeans.setBounds(400, 260, 150, 20)

        add(self.__jSeparatorDisjonctions)
        self.__jSeparatorDisjonctions.setBounds(20, 125, 530, 10)

        self.__jButtonDefautSupport.setBackground(java.awt.Color(255, 255, 255))
        self.__jButtonDefautSupport.addActionListener(ActionListenerAnonymousInnerClass(self))

        add(self.__jButtonDefautSupport)
        self.__jButtonDefautSupport.setBounds(300, 20, 20, 20)

        self.__jButtonDefautConfiance.setBackground(java.awt.Color(255, 255, 255))
        self.__jButtonDefautConfiance.addActionListener(ActionListenerAnonymousInnerClass2(self))

        add(self.__jButtonDefautConfiance)
        self.__jButtonDefautConfiance.setBounds(300, 50, 20, 20)

        self.__jButtonDefautSupportDisjonctions.setBackground(java.awt.Color(255, 255, 255))
        self.__jButtonDefautSupportDisjonctions.addActionListener(ActionListenerAnonymousInnerClass3(self))

        add(self.__jButtonDefautSupportDisjonctions)
        self.__jButtonDefautSupportDisjonctions.setBounds(510, 200, 20, 20)
        '''
        None
    
    # </editor-fold>//GEN-END:initComponents
    '''
    class ActionListenerAnonymousInnerClass(java.awt.event.ActionListener):

        def __init__(self, outerInstance):
            self.__outerInstance = outerInstance

        def actionPerformed(self, evt):
            outerInstance.__jButtonDefautSupportActionPerformed(evt)

    class ActionListenerAnonymousInnerClass2(java.awt.event.ActionListener):

        def __init__(self, outerInstance):
            self.__outerInstance = outerInstance

        def actionPerformed(self, evt):
            outerInstance.__jButtonDefautConfianceActionPerformed(evt)

    class ActionListenerAnonymousInnerClass3(java.awt.event.ActionListener):

        def __init__(self, outerInstance):
            self.__outerInstance = outerInstance

        def actionPerformed(self, evt):
            outerInstance.__jButtonDefautSupportDisjonctionsActionPerformed(evt)

    def __jButtonDefautSupportDisjonctionsActionPerformed(self, evt):
        self.__jTextSupportSupplementaire.setText(ResolutionContext.EcrirePourcentage(StandardParametersQuantitative.DEFAUT_MINSUPP_DISJONCTIONS, 3, False)) #GEN-LAST:event_jButtonDefautSupportDisjonctionsActionPerformed

    def __jButtonDefautSupportActionPerformed(self, evt):
        self.__jTextFieldSupport.setText(ResolutionContext.EcrirePourcentage(StandardParametersQuantitative.DEFAUT_MINSUPP, 3, False)) #GEN-LAST:event_jButtonDefautSupportActionPerformed

    def __jButtonDefautConfianceActionPerformed(self, evt):
        self.__jTextFieldConfiance.setText(ResolutionContext.EcrirePourcentage(StandardParametersQuantitative.DEFAUT_MINCONF, 3, False)) #GEN-LAST:event_jButtonDefautConfianceActionPerformed


    # Variables declaration - do not modify//GEN-BEGIN:variables
    #Note: CASSANDRA MODIFIED - ADDED jLabelNumAssociationRules
    # End of variables declaration//GEN-END:variables

    '''


    def EnregistrerParametres(self):

        parametresReglesQuantitatives = None
        fMinSupp = 0.0
        fMinConf = 0.0
        iNombreMaxAttributsQuant = 0
        iNombreMinAttributsQuant = 0
        iNombreDisjonctionsGauche = 0
        iNombreDisjonctionsDroite = 0
        iNombreAssociationRules = 0
        fMinSuppDisjonctions = 0.0
        applyKMeans = 0


        parametresReglesQuantitatives = self.m_contexteResolution.m_parametresReglesQuantitatives
        if parametresReglesQuantitatives is None:
            return True

        # M�morisation des param�tres :

        try:
            fMinSupp = float((float(self.__jTextFieldSupport.getText()) / 100.0))
            parametresReglesQuantitatives.m_fMinSupp = fMinSupp
        except NumberFormatException as e:
            return False

        try:
            fMinConf = float((float(self.__jTextFieldConfiance.getText()) / 100.0))
            parametresReglesQuantitatives.m_fMinConf = fMinConf
        except NumberFormatException as e:
            return False

        try:
            iNombreMinAttributsQuant = int(self.__jTextMiniQuants.getText())
            parametresReglesQuantitatives.m_iNombreMinAttributsQuant = iNombreMinAttributsQuant
        except NumberFormatException as e:
            return False

        try:
            iNombreMaxAttributsQuant = int(self.__jTextMaxiQuants.getText())
            parametresReglesQuantitatives.m_iNombreMaxAttributsQuant = iNombreMaxAttributsQuant
        except NumberFormatException as e:
            return False

        iNombreDisjonctionsGauche = self.__jComboDisjonctionsGauche.getSelectedIndex()
        if (iNombreDisjonctionsGauche<0) or (iNombreDisjonctionsGauche>=10):
            iNombreDisjonctionsGauche = 0
        parametresReglesQuantitatives.m_iNombreDisjonctionsGauche = iNombreDisjonctionsGauche + 1

        iNombreDisjonctionsDroite = self.__jComboDisjonctionsDroite.getSelectedIndex()
        if (iNombreDisjonctionsDroite<0) or (iNombreDisjonctionsDroite>=10):
            iNombreDisjonctionsDroite = 0
        parametresReglesQuantitatives.m_iNombreDisjonctionsDroite = iNombreDisjonctionsDroite + 1


        applyKMeans = self.__jComboApplyKMeans.getSelectedIndex()
        if (applyKMeans<0) or (applyKMeans>=3):
            applyKMeans = 0
        parametresReglesQuantitatives.m_applyKMeans = applyKMeans

        # If we are using k means, we want to have 1000x more rules tested
        # We want to test the values of k incremented by 5 - from 5 to 100
        if applyKMeans >= 1:
            iNombreAssociationRules = (self.__jComboNumAssociationRules.getSelectedIndex() + 1) * 9
            if (iNombreAssociationRules<0) or (iNombreAssociationRules>=91):
                iNombreAssociationRules = 1

        else:
            iNombreAssociationRules = self.__jComboNumAssociationRules.getSelectedIndex()
            if (iNombreAssociationRules<0) or (iNombreAssociationRules>=10):
                iNombreAssociationRules = 1

            iNombreAssociationRules += 1

        parametresReglesQuantitatives.m_iNombreAssociationRules = iNombreAssociationRules

        try:
            fMinSuppDisjonctions = float((float(self.__jTextSupportSupplementaire.getText()) / 100.0))
            parametresReglesQuantitatives.m_fMinSuppDisjonctions = fMinSuppDisjonctions
        except NumberFormatException as e:
            return False


        return True


