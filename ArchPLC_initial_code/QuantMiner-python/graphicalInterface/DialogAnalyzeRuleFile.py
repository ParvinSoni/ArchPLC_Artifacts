﻿#                                             
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



class DialogAnalyzeRuleFile(javax.swing.JDialog):

    __serialVersionUID = 1
    #* Creates new form DialogAnalyseFichierRegles 
    def __init__(self, parent, modal):
        self.__jButtonAide = None
        self.__jButtonFermer = None
        self.__jButtonSelectionner = None
        self.__jEditorPaneDescriptif = None
        self.__jPanelGeneral = None
        self.__jScrollPaneDescriptif = None
        self.__jTextFieldChemin = None

        super().__init__(parent, modal)
        self.__initComponents()

        setLocationRelativeTo(None)

    #    * This method is called from within the constructor to
    #     * initialize the form.
    #     * WARNING: Do NOT modify this code. The content of this method is
    #     * always regenerated by the Form Editor.
    #     
    # <editor-fold defaultstate="collapsed" desc=" Generated Code ">//GEN-BEGIN:initComponents
    def __initComponents(self):
        self.__jPanelGeneral = javax.swing.JPanel()
        self.__jButtonSelectionner = javax.swing.JButton()
        self.__jTextFieldChemin = javax.swing.JTextField()
        self.__jScrollPaneDescriptif = javax.swing.JScrollPane()
        self.__jEditorPaneDescriptif = javax.swing.JEditorPane()
        self.__jButtonFermer = javax.swing.JButton()
        self.__jButtonAide = javax.swing.JButton()

        setDefaultCloseOperation(javax.swing.WindowConstants.DISPOSE_ON_CLOSE)
        setTitle("Information of a rule file \".QMR\"")
        setResizable(False)
        addWindowListener(WindowAdapterAnonymousInnerClass(self))

        self.__jPanelGeneral.setLayout(None)

        self.__jPanelGeneral.setPreferredSize(java.awt.Dimension(700, 500))
        self.__jButtonSelectionner.setText("Select a rules file")
        self.__jButtonSelectionner.addActionListener(ActionListenerAnonymousInnerClass(self))

        self.__jPanelGeneral.add(self.__jButtonSelectionner)
        self.__jButtonSelectionner.setBounds(10, 10, 240, 20)

        self.__jTextFieldChemin.setEditable(False)
        self.__jPanelGeneral.add(self.__jTextFieldChemin)
        self.__jTextFieldChemin.setBounds(260, 10, 370, 19)

        self.__jEditorPaneDescriptif.setEditable(False)
        self.__jEditorPaneDescriptif.setContentType("text/html")
        self.__jScrollPaneDescriptif.setViewportView(self.__jEditorPaneDescriptif)

        self.__jPanelGeneral.add(self.__jScrollPaneDescriptif)
        self.__jScrollPaneDescriptif.setBounds(10, 40, 680, 410)

        self.__jButtonFermer.setText("close")
        self.__jButtonFermer.addActionListener(ActionListenerAnonymousInnerClass2(self))

        self.__jPanelGeneral.add(self.__jButtonFermer)
        self.__jButtonFermer.setBounds(300, 460, 100, 23)

        self.__jButtonAide.setText("?")
        self.__jButtonAide.addActionListener(ActionListenerAnonymousInnerClass3(self))

        self.__jPanelGeneral.add(self.__jButtonAide)
        self.__jButtonAide.setBounds(640, 6, 50, 30)

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
            outerInstance.__jButtonSelectionnerActionPerformed(evt)

    class ActionListenerAnonymousInnerClass2(java.awt.event.ActionListener):

        def __init__(self, outerInstance):
            self.__outerInstance = outerInstance

        def actionPerformed(self, evt):
            outerInstance.__jButtonFermerActionPerformed(evt)

    class ActionListenerAnonymousInnerClass3(java.awt.event.ActionListener):

        def __init__(self, outerInstance):
            self.__outerInstance = outerInstance

        def actionPerformed(self, evt):
            outerInstance.__jButtonAideActionPerformed(evt)

    def __jButtonAideActionPerformed(self, evt):
        dialogAide = DialogHelp(ENV.REPERTOIRE_AIDE+"rule_analysis.htm", None, True)
        dialogAide.show() #GEN-LAST:event_jButtonAideActionPerformed

    def __jButtonFermerActionPerformed(self, evt):
        setVisible(False)
        dispose() #GEN-LAST:event_jButtonFermerActionPerformed

    def __jButtonSelectionnerActionPerformed(self, evt):
        sFichierChoisi = None

        description = []
        description.append("QuantMiner Files")
        extention = []
        extention.append("qmr")

        sFichierChoisi = ToolsInterface.DialogOuvertureFichier(self, ENV.REPERTOIRE_REGLES_QMR, description, extention)

        if sFichierChoisi is not None:
            self.__jTextFieldChemin.setText(sFichierChoisi)
            self.__jEditorPaneDescriptif.setText(ResolutionContext.EcrireDescriptionFichierReglesBinairesHTML(sFichierChoisi))
            self.__jEditorPaneDescriptif.setCaretPosition(0) #GEN-LAST:event_jButtonSelectionnerActionPerformed

    #* Closes the dialog 
    def __closeDialog(self, evt):
        setVisible(False)
        dispose() #GEN-LAST:event_closeDialog

    #    *
    #     * @param args the command line arguments
    #     
    @staticmethod
    def main(args):
        (DialogAnalyzeRuleFile(javax.swing.JFrame(), True)).show()


    # Variables declaration - do not modify//GEN-BEGIN:variables
    # End of variables declaration//GEN-END:variables

