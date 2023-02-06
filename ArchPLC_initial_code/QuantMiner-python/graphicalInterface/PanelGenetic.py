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


from apriori_solver import *
from apriori_solver.onefile import ResolutionContext
from apriori_solver.onefile import RuleTester
from database import *
from geneticAlgorithm import *
from geneticAlgorithm.OptimizerGeneticAlgo import *
from geneticAlgorithm.GeneticAlgo import *
# from geneticAlgorithm.OptimizerAprioriQual import *
# from geneticAlgorithm.OptimizerSimulatedAnnealing import *
# from geneticAlgorithm.DefinirOptimiseurRegle import *
from graphicalInterface.DatabasePanelAssistant import DatabasePanelAssistant
from graphicalInterface.DialogEndComputeRules import DialogEndComputeRules

from simulatedAnnealing import *
from tools import *
from tools.ENV import *



class PanelGenetic(DatabasePanelAssistant):
    class IndicateurCalculReglesGenerique(RuleTester.IndicateurCalculRegles):
        def __init__(self, outerInstance, panneauParent):
            self.m_panneauParent = None

            super().__init__()
            self.__outerInstance = outerInstance


            self.m_panneauParent = panneauParent

        #indicate that calculation is finished
        def IndiquerFinCalcul(self):
            fenetreFinCalcul = None

            if not ENV.AVERTIR_FIN_CALCUL: #AVERTIR notice finishing calculation
                return

            fenetreFinCalcul = DialogEndComputeRules(self.m_panneauParent.m_contexteResolution.m_fenetreProprietaire, True)

            # if (self.m_panneauParent.m_contexteResolution.m_fenetreProprietaire.getExtendedState()) != 0:
            #     self.m_panneauParent.m_contexteResolution.m_fenetreProprietaire.setExtendedState(java.awt.Frame.MAXIMIZED_BOTH)
            #     self.m_panneauParent.m_contexteResolution.m_fenetreProprietaire.toFront()
            # fenetreFinCalcul.show()

        #send information
        def EnvoyerInfo(self, sNouvelleInfo):
            print(sNouvelleInfo)
            # self.m_panneauParent.__AjouterInfo(sNouvelleInfo)

        #indicate the number of the rule being tested
        def IndiquerNombreReglesATester(self, iNombreReglesATester):
            self.__outerInstance.__m_iMaxReglesTestees = iNombreReglesATester
            self.__outerInstance.__jProgressResolution = self.__outerInstance.__m_iMaxReglesTestees
            self.__outerInstance.__jProgressResolution = 0
            self.__outerInstance.__m_iIndiceRegleAffichee = 0 #END OF CLASS IndicateurCalculReglesGenerique

    #* Creates new form PanneauAlgoGenetique 
    def __init__(self, contexteResolution):
        self.__m_calculateur = None
        self.__m_iMaxReglesTestees = 0
        self.__m_iIndiceRegleAffichee = 0
        self.__m_bResultatAffiche = False
        self.__jBoutonArreter = None
        self.__jBoutonDemarrer = None
        self.__jButtonTravaillerFond = None
        self.__jProgressResolution = None
        self.__jScrollPaneContexte = None
        self.__jScrollPaneRegles = None
        self.__jTextAreaContexte = None
        self.__jZoneTexteRegles = None

        super().__init__(contexteResolution)

        self.__initComponents()


        if contexteResolution.m_iTechniqueResolution == ResolutionContext.TECHNIQUE_APRIORI_QUAL:
            # super().DefinirEtape(4, "Mining rules using Apriori", ENV.REPERTOIRE_AIDE+"computation.htm")
            print("Mining rules using Apriori")

        elif contexteResolution.m_iTechniqueResolution == ResolutionContext.TECHNIQUE_ALGO_GENETIQUE:
            # super().DefinirEtape(4, "Mining rules using a genetic algorithm", ENV.REPERTOIRE_AIDE+"computation.htm")
            print("Mining rules using a genetic algorithm")



        elif contexteResolution.m_iTechniqueResolution == ResolutionContext.TECHNIQUE_RECUIT_SIMULE:
            # super().DefinirEtape(4, "Mining rules using a simulated annealing algorithm", ENV.REPERTOIRE_AIDE+"computation.htm")
            print("Mining rules using a simulated annealing algorithm")

        # super().DefinirPanneauPrecedent(MainWindow.PANNEAU_CONFIG_TECHNIQUE) #previous step is step 3
        # super().DefinirPanneauSuivant(MainWindow.PANNEAU_RESULTATS) #next step is step 5
        super().initBaseComponents()

        self.__m_iMaxReglesTestees = 0
        self.__m_iIndiceRegleAffichee = 0

        '''
        # Initialization des propri�t�s de la barre de progression :
        self.__jProgressResolution.setMinimum(0)
        self.__jProgressResolution.setMaximum(100)
        self.__jProgressResolution.setValue(0)
        self.__jProgressResolution.setIndeterminate(False)
        self.__jProgressResolution.setStringPainted(True)
        '''

        if self.m_contexteResolution is not None:
            self.m_contexteResolution.m_listeRegles = None

        # Create a timer for le refresh des contr�les durant l'extraction :
        # tacheProgrammee = ActionListenerAnonymousInnerClass(self)
        alaic = self.ActionListenerAnonymousInnerClass(self)
        # alaic.actionPerformed("evt")
        self.__jBoutonDemarrerActionPerformed("evt")

        #Starts the Timer, causing it to start sending action events to its listeners. 
        # (None # javax.swing.Timer(1000, tacheProgrammee)).start() #call tacheProgrammee to do refresh every second

    class ActionListenerAnonymousInnerClass():
        def __init__(self, outerInstance):
            self.__outerInstance = outerInstance

        def actionPerformed(self, evt):
            outerInstance.__RafraichirControles() #Rafraichir means refresh

    #    * This method is called from within the constructor to
    #     * initialize the form.
    #     * WARNING: Do NOT modify this code. The content of this method is
    #     * always regenerated by the Form Editor.
    #     
    def __initComponents(self):
        # '''
        self.__jBoutonDemarrer = None # javax.swing.JButton() #Demarrer means start
        self.__jBoutonArreter = None # javax.swing.JButton() #Arreter means stop
        self.__jScrollPaneRegles = None # javax.swing.JScrollPane() #rule display panel
        self.__jZoneTexteRegles = None # javax.swing.JTextArea() #text area to display rules
        self.__jScrollPaneContexte = None # javax.swing.JScrollPane() #context display panel
        self.__jTextAreaContexte = None # javax.swing.JTextArea() #text area to display context
        self.__jProgressResolution = None # javax.swing.JProgressBar() #progress bar
        self.__jButtonTravaillerFond = None # javax.swing.JButton() #work as a background task

        '''
        # setLayout(None)
        #start button

        self.__jBoutonDemarrer.setText("Start")
        self.__jBoutonDemarrer.addActionListener(ActionListenerAnonymousInnerClass(self))

        add(self.__jBoutonDemarrer)
        self.__jBoutonDemarrer.setBounds(30, 170, 100, 26)

        #stop button
        self.__jBoutonArreter.setText("Stop")
        self.__jBoutonArreter.addActionListener(ActionListenerAnonymousInnerClass2(self))

        add(self.__jBoutonArreter)
        self.__jBoutonArreter.setBounds(150, 170, 100, 26)

        #rule panel
        self.__jScrollPaneRegles.setAutoscrolls(True)
        self.__jZoneTexteRegles.setEditable(False)
        self.__jZoneTexteRegles.setFont(java.awt.Font("Lucida Bright", 3, 12))
        self.__jScrollPaneRegles.setViewportView(self.__jZoneTexteRegles)

        add(self.__jScrollPaneRegles)
        self.__jScrollPaneRegles.setBounds(30, 250, 770, 250)

        #context panel
        self.__jScrollPaneContexte.setAutoscrolls(True)
        self.__jTextAreaContexte.setEditable(False)
        self.__jTextAreaContexte.setLineWrap(True)
        self.__jScrollPaneContexte.setViewportView(self.__jTextAreaContexte)

        add(self.__jScrollPaneContexte)
        self.__jScrollPaneContexte.setBounds(30, 10, 810, 150)

        #progress bar
        add(self.__jProgressResolution)
        self.__jProgressResolution.setBounds(30, 210, 440, 20)

        #the button of working as a background task
        self.__jButtonTravaillerFond.setText("Work as a background task")
        self.__jButtonTravaillerFond.addActionListener(ActionListenerAnonymousInnerClass3(self))

        add(self.__jButtonTravaillerFond)
        self.__jButtonTravaillerFond.setBounds(440, 170, 300, 26)
        '''
        None
 #GEN-END:initComponents

    class ActionListenerAnonymousInnerClass():

        def __init__(self, outerInstance):
            self.__outerInstance = outerInstance
            # self.__outerInstance.__jBoutonDemarrerActionPerformed()

        def actionPerformed(self, evt):
            print(type(self.__outerInstance))
            # print(type(self.__outerInstance.m_contexteResolution))
            # self.__outerInstance.__jBoutonDemarrerActionPerformed()
            # self.__outerInstance.__jBoutonDemarrerActionPerformed(evt)

    class ActionListenerAnonymousInnerClass2():

        def __init__(self, outerInstance):
            self.__outerInstance = outerInstance

        def actionPerformed(self, evt):
            outerInstance.__jBoutonArreterActionPerformed(evt)

    class ActionListenerAnonymousInnerClass3():

        def __init__(self, outerInstance):
            self.__outerInstance = outerInstance

        def actionPerformed(self, evt):
            outerInstance.__jButtonTravaillerFondActionPerformed(evt)



    #the button of working as a background task
    def __jButtonTravaillerFondActionPerformed(self, evt):
        if self.__m_calculateur is not None:
            self.__m_calculateur.setPriority(Thread.MIN_PRIORITY)

        super().m_contexteResolution.m_fenetreProprietaire.setExtendedState(java.awt.Frame.ICONIFIED) #GEN-LAST:event_jButtonTravaillerFondActionPerformed



    #stop calculation
    def __jBoutonArreterActionPerformed(self, evt):
        self.__ArreterCalculateur(True) #GEN-LAST:event_jBoutonArreterActionPerformed

    #start calculation
    def __jBoutonDemarrerActionPerformed(self, evt):
        optimiseur = None #optimize rule
        self.__ArreterCalculateur(False) #stop calculation

        self.__m_calculateur = RuleTester(self.m_contexteResolution, self.IndicateurCalculReglesGenerique(self, self))

        self.__m_bResultatAffiche = False

        # self.__jZoneTexteRegles.setText("") #set rule text area empty
        # self.__jTextAreaContexte.setText("") #set context text area empty

        #create an optimizer
        if self.m_contexteResolution.m_iTechniqueResolution == ResolutionContext.TECHNIQUE_APRIORI_QUAL:
            optimiseur = OptimizerAprioriQual()

        elif self.m_contexteResolution.m_iTechniqueResolution == ResolutionContext.TECHNIQUE_ALGO_GENETIQUE:
            optimiseur = OptimizerGeneticAlgo()

        elif self.m_contexteResolution.m_iTechniqueResolution == ResolutionContext.TECHNIQUE_RECUIT_SIMULE:
            optimiseur = OptimizerSimulatedAnnealing()

        self.__m_calculateur.DefinirOptimiseurRegle(optimiseur)
        #Causes this thread to begin execution; the Java Virtual Machine calls the run method of this thread. 
        self.__m_calculateur.start() #GEN-LAST:event_jBoutonDemarrerActionPerformed

    # Variables declaration - do not modify//GEN-BEGIN:variables
    # End of variables declaration//GEN-END:variables


    #stop calculation
    def __ArreterCalculateur(self, bEnregistrerRegles):

        if self.__m_calculateur is not None:

            self.__m_calculateur.AutoriserIndicationFinCalcul(False)

            self.__m_calculateur.ArreterExecution()

            if not self.__m_calculateur.EstResultatDisponible():
                while self.__m_calculateur.isAlive():
                    pass

            if bEnregistrerRegles:
                if self.m_contexteResolution is not None:
                    self.m_contexteResolution.m_listeRegles = self.__m_calculateur.ObtenirListeReglesOptimales()

            self.__RafraichirControles()

            self.__m_calculateur = None




    #append more rules to the rule text being displayed (Step 4/5)
    def __AjouterRegle(self, sNouvelleRegle):
        self.__jZoneTexteRegles.append(sNouvelleRegle)

    #append more information to the context text being displayed
    def __AjouterInfo(self, sInfo):
        #Appends the given text to the end of the document. Does nothing if the model is null or the string is null or empty. 
        self.__jTextAreaContexte.append(sInfo)


    #refresh
    def __RafraichirControles(self):
        sIndicateur = None
        regle = None
        centroid = None
        centroidList = None
        bResultatDisponible = False

        if self.__m_calculateur is not None:
            if not self.__m_bResultatAffiche:
                bResultatDisponible = self.__m_calculateur.EstResultatDisponible()
                if (self.__m_calculateur.m_bEnExecution) or (bResultatDisponible):

                    self.__m_bResultatAffiche = bResultatDisponible

                    if self.__m_iMaxReglesTestees == 0:
                        self.__jProgressResolution.setValue(0)
                        self.__jProgressResolution.setString("")
                    else:
                        self.__jProgressResolution.setValue(self.__m_calculateur.m_iNombreReglesTestees)
                        sIndicateur = String.valueOf(self.__m_calculateur.m_iNombreReglesTestees * self.__m_calculateur.getNumAssocationRules()) + " tested rules /  " + String.valueOf(self.__m_iMaxReglesTestees * self.__m_calculateur.getNumAssocationRules())
                        self.__jProgressResolution.setString(sIndicateur)
                        self.__jProgressResolution.repaint()

                    # Display the progress of the rules being calculated:
                    condition = True
                    while condition:

                        #not k-means
                        if self.__m_calculateur.m_applyKMeans < 1:
                            regle = self.__m_calculateur.ObtenirRegleCalculee(self.__m_iIndiceRegleAffichee)
                            #regle is the rule obtained
                            if regle is not None:
                                self.__AjouterRegle(String.valueOf(self.__m_iIndiceRegleAffichee + 1) + ".  ")
                                self.__AjouterRegle(regle.toString())
                                self.__AjouterRegle("\n")
                                self.__m_iIndiceRegleAffichee += 1
                        else:

                            centroidList = self.__m_calculateur.ObtenirListOfCentroids()

                            a = 0
                            while a< len(centroidList):
                                centroid = centroidList[a]
                                centroidRule = centroid.getCentroidRule()
                                #PRINTING DOUBLE ETC SOMETIMES - TEMPORARY 'HASBEENPRINTED'
                                if centroid is not None and (not centroid.getHasBeenPrinted()) and centroidRule != "":
                                    self.__AjouterRegle(String.valueOf(self.__m_iIndiceRegleAffichee + 1) + ".  ")
                                    self.__AjouterRegle(centroidRule)
                                    self.__AjouterRegle("\n")
                                    self.__m_iIndiceRegleAffichee += 1
                                    centroid.setHasBeenPrinted(True)
                                a += 1


                        condition = regle is not None



    # Outrepassement de la m�thode m�re pour l'ajustement des champs :
    def ArrangerDisposition(self):
        iDeltaPosX = 0 # Diff�rence de positionnement horizontal entre la position id�ale et celle de l'�diteur de formulaires
        iDeltaPosY = 0 # Diff�rence de positionnement vertical entre la position id�ale et celle de l'�diteur de formulaires

        super().ArrangerDisposition()

        iDeltaPosX = self.__jScrollPaneContexte.getX() - self.m_zoneControles.x
        iDeltaPosY = self.__jScrollPaneContexte.getY() - self.m_zoneControles.y

        self.__jScrollPaneContexte.setBounds(self.__jScrollPaneContexte.getX() - iDeltaPosX, self.__jScrollPaneContexte.getY() - iDeltaPosY, self.m_zoneControles.width, self.__jScrollPaneContexte.getHeight())

        self.__jBoutonDemarrer.setLocation(self.__jBoutonDemarrer.getX()-iDeltaPosX, self.__jBoutonDemarrer.getY()-iDeltaPosY)
        self.__jBoutonArreter.setLocation(self.__jBoutonArreter.getX()-iDeltaPosX, self.__jBoutonArreter.getY()-iDeltaPosY)
        self.__jButtonTravaillerFond.setLocation((self.m_zoneControles.width+self.m_zoneControles.x)-self.__jButtonTravaillerFond.getWidth(), self.__jButtonTravaillerFond.getY()-iDeltaPosY)

        self.__jProgressResolution.setBounds(self.__jProgressResolution.getX()-iDeltaPosX, self.__jProgressResolution.getY()-iDeltaPosY, self.m_zoneControles.width, self.__jProgressResolution.getHeight())

        self.__jScrollPaneRegles.setBounds(self.__jScrollPaneRegles.getX() - iDeltaPosX, self.__jScrollPaneRegles.getY() - iDeltaPosY, self.m_zoneControles.width, self.m_zoneControles.height + self.m_zoneControles.y - (self.__jScrollPaneRegles.getY()-iDeltaPosY))


    # Outrepassement de la m�thode m�re pour des traitements sp�cifiques :
    def TraitementsSpecifiquesAvantSuivant(self):
        self.__ArreterCalculateur(True)

        return True


    # Outrepassement de la m�thode m�re pour l'annulation du processus � partir de ce panneau :
    def AnnulerPanneau(self):
        self.__ArreterCalculateur(False)

        return True
