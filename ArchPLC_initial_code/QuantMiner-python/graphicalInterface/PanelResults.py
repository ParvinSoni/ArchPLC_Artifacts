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
from database.onefile import CsvFileParser
from tools import *
from graphicalInterface.DatabasePanelAssistant import DatabasePanelAssistant

# from com import Ostermiller.util.ExcelCSVPrinter



class PanelResults(DatabasePanelAssistant):

    #called when saving file in html with graph
    class ResultatsEnregistreurGraphiqueRegle(ResolutionContext.EnregistreurGraphiqueRegle):

        #Enregistrer means record/write down

        def __init__(self, outerInstance, sNomBaseFichier):
            self.__m_sNomBaseFichier = None

            super().__init__()
            self.__outerInstance = outerInstance

            self.__m_sNomBaseFichier = sNomBaseFichier

        def EnregistrerRegle(self, regle, iIndiceRegle):
            fichier = None
            sCheminFichier = None
            sCheminFichier = self.__m_sNomBaseFichier+String.valueOf(iIndiceRegle)+".jpg"
            outerInstance.__m_afficheurRegles.EnregistrerImageRegle(regle, iIndiceRegle, sCheminFichier)
            fichier = File(sCheminFichier)
            return fichier.getName()

    #* Creates new form PanneauResultats 
    def __init__(self, contexteResolution):
        self.__jButtonCopy = None
        self.__jButtonSauver = None
        self.__jButtonVoirContexte = None
        self.__jScrollBarRegles = None
        self.__jScrollRegles = None
        self.__jTextNumeroRegle = None
        self.__jButtonExtractRows = None
        self.__m_afficheurRegles = None
        self.__m_panneauTri = None
        self.__m_iNombreReglesTotales = 0
        self.__m_iIndexCurrentRule = 0
        self.__m_iNombreReglesRetenues = 0
        self.__m_tReglesFiltrees = None

        super().__init__(contexteResolution)

        iNombreRegles = 0
        tRegles = None

        self.__m_tReglesFiltrees = None

        # If les rules sont issues d'un file, on commence by les load :
        if self.m_contexteResolution.m_iTechniqueResolution == ResolutionContext.TECHNIQUE_CHARGEMENT:
            self.m_contexteResolution.m_sDescriptionRegles = self.m_contexteResolution.m_parametresTechChargement.m_sDescriptionRegles
            # super().m_contexteResolution.ChargerReglesBinaire(self.m_contexteResolution.m_parametresTechChargement.m_sNomFichier)
            self.m_contexteResolution.ChargerReglesBinaire(self.m_contexteResolution.m_parametresTechChargement.m_sNomFichier)

        # Mise � jour des informations de filtrage :
        # super().m_contexteResolution.GenererStructuresDonneesSelonBDPriseEnCompte_Filtrage()
        # super().m_contexteResolution.MettreAJourDonneesInternesFiltre_Filtrage()
        self.m_contexteResolution.GenererStructuresDonneesSelonBDPriseEnCompte_Filtrage()
        self.m_contexteResolution.MettreAJourDonneesInternesFiltre_Filtrage()

        self.__initComponents()

        '''
        self.__jButtonCopy.setIcon(ImageIcon(ENV.REPERTOIRE_RESSOURCES + "copier.jpg")) #set icon for the copy button

        self.__jTextNumeroRegle.setText("no rule selected") #initialized with no rule selected

        #the middle part
        self.__m_panneauTri = PanelSort(self, self.m_contexteResolution)
        self.__m_panneauTri.setBorder(javax.swing.border.EtchedBorder())
        add(self.__m_panneauTri)

        #the third part
        self.__m_afficheurRegles = RuleBrowser(self.m_contexteResolution)
        self.__m_afficheurRegles.setBackground(java.awt.Color(255, 255, 255))
        self.__jScrollRegles.setViewportView(self.__m_afficheurRegles)
        self.__jScrollRegles.validate()

        #the scroll bar
        self.__jScrollBarRegles.setMinimum(0)
        self.__jScrollBarRegles.setMaximum(0)
        self.__jScrollBarRegles.setUnitIncrement(1)
        self.__jScrollBarRegles.setVisibleAmount(1)
        '''
        iNombreRegles = 0

        if self.m_contexteResolution.m_listeRegles is not None:
            iNombreRegles = len(self.m_contexteResolution.m_listeRegles)

        if iNombreRegles > 0:
            # Calcul des mesures suppl�mentaires permettant d'�valuer plus finement les r�gles :
            # (si les r�gles ont �t� charg�es depuis un fichier, ces calculs sont d�j� faits)
            if self.m_contexteResolution.m_iTechniqueResolution != ResolutionContext.TECHNIQUE_CHARGEMENT:
                tRegles = [None for _ in range(1)]
                # tRegles = (super().m_contexteResolution.m_listeRegles.toArray(tRegles))
                tRegles = (self.m_contexteResolution.m_listeRegles.toArray(tRegles))
                AssociationRule.CalculerMesuresDiverses(tRegles, self.m_contexteResolution)

            # self.__jScrollBarRegles.setMaximum(iNombreRegles-1)
        else:
            # self.__jScrollBarRegles.setMaximum(0)
            None


        # super().DefinirEtape(5, "Results", ENV.REPERTOIRE_AIDE+"consult_results.htm")


        if self.m_contexteResolution.m_iTechniqueResolution == ResolutionContext.TECHNIQUE_APRIORI_QUAL:
            # super().DefinirPanneauPrecedent(MainWindow.PANNEAU_TECH_GENERIQUE)
            None

        elif self.m_contexteResolution.m_iTechniqueResolution == ResolutionContext.TECHNIQUE_ALGO_GENETIQUE:
            # self.DefinirPanneauPrecedent(MainWindow.PANNEAU_TECH_GENERIQUE)
            None

        elif self.m_contexteResolution.m_iTechniqueResolution == ResolutionContext.TECHNIQUE_RECUIT_SIMULE:
            # super().DefinirPanneauPrecedent(MainWindow.PANNEAU_TECH_GENERIQUE)
            None

        elif self.m_contexteResolution.m_iTechniqueResolution == ResolutionContext.TECHNIQUE_CHARGEMENT:
            # super().DefinirPanneauPrecedent(MainWindow.PANNEAU_CONFIG_TECHNIQUE)
            None

        else:
            # super().DefinirPanneauPrecedent(MainWindow.PANNEAU_AUCUN)
            None

        # super().DefinirPanneauSuivant(MainWindow.PANNEAU_AUCUN)
        super().initBaseComponents()

        self.MettreAJourListeRegles()


    #    * This method is called from within the constructor to
    #     * initialize the form.
    #     * WARNING: Do NOT modify this code. The content of this method is
    #     * always regenerated by the Form Editor.
    #     
    def __initComponents(self):
        # self.__jScrollBarRegles = javax.swing.JScrollBar() #rule scroll bar
        # self.__jButtonSauver = javax.swing.JButton() #save in a file
        # self.__jTextNumeroRegle = javax.swing.JTextField() #rules
        # self.__jScrollRegles = javax.swing.JScrollPane() #rules
        # self.__jButtonCopy = javax.swing.JButton() #copy button
        # self.__jButtonVoirContexte = javax.swing.JButton() #visualize the extraction context
        # self.__jButtonExtractRows = javax.swing.JButton() #Extract the rows of a specific rule

        # setLayout(None)

        # #text field --number of rules 
        # self.__jTextNumeroRegle.setEditable(False)
        # self.__jTextNumeroRegle.setFont(java.awt.Font("Dialog", 1, 12))
        # self.__jTextNumeroRegle.setText("Rule n\u00b0.. / .. (total : ...)")
        # add(self.__jTextNumeroRegle)
        # self.__jTextNumeroRegle.setBounds(10, 110, 210, 20)

        # #scroll bar
        # self.__jScrollBarRegles.setMaximum(0)
        # self.__jScrollBarRegles.setOrientation(javax.swing.JScrollBar.HORIZONTAL)
        # self.__jScrollBarRegles.addAdjustmentListener(AdjustmentListenerAnonymousInnerClass(self))

        # add(self.__jScrollBarRegles)
        # self.__jScrollBarRegles.setBounds(220, 110, 100, 20)
        # #jScrollBarRegles.setBounds(220, 110, 130, 20)

        # #copy button
        # self.__jButtonCopy.addActionListener(ActionListenerAnonymousInnerClass(self))

        # add(self.__jButtonCopy)
        # self.__jButtonCopy.setBounds(320, 110, 20, 20)
        # # jButtonCopy.setBounds(350, 110, 20, 20)

        # #button --Extract rows for a specific rule
        # self.__jButtonExtractRows.setText("Extract rows")
        # self.__jButtonExtractRows.addActionListener(ActionListenerAnonymousInnerClass2(self))
        # add(self.__jButtonExtractRows)
        # self.__jButtonExtractRows.setBounds(340, 110, 120, 20)


        # #button --save in a file 
        # self.__jButtonSauver.setText("Save in a file")
        # self.__jButtonSauver.addActionListener(ActionListenerAnonymousInnerClass3(self))

        # add(self.__jButtonSauver)
        # self.__jButtonSauver.setBounds(10, 10, 210, 26)

        # #scroll panel --about resulted rules
        # self.__jScrollRegles.setHorizontalScrollBarPolicy(javax.swing.JScrollPane.HORIZONTAL_SCROLLBAR_NEVER)
        # self.__jScrollRegles.setVerticalScrollBarPolicy(javax.swing.JScrollPane.VERTICAL_SCROLLBAR_ALWAYS)
        # add(self.__jScrollRegles)
        # self.__jScrollRegles.setBounds(10, 130, 360, 40)

        # #button --Visualize the extraction context
        # self.__jButtonVoirContexte.setText("Visualize the extraction context")
        # self.__jButtonVoirContexte.addActionListener(ActionListenerAnonymousInnerClass4(self))

        # add(self.__jButtonVoirContexte)
        # self.__jButtonVoirContexte.setBounds(240, 10, 250, 26)
        None
 #GEN-END:initComponents

    class AdjustmentListenerAnonymousInnerClass():
        def __init__(self, outerInstance):
            self.__outerInstance = outerInstance

        def adjustmentValueChanged(self, evt):
            outerInstance.__jScrollBarReglesAdjustmentValueChanged(evt)

    class ActionListenerAnonymousInnerClass():

        def __init__(self, outerInstance):
            self.__outerInstance = outerInstance

        def actionPerformed(self, evt):
            outerInstance.__jButtonCopyActionPerformed(evt)

    class ActionListenerAnonymousInnerClass2():

        def __init__(self, outerInstance):
            self.__outerInstance = outerInstance

        def actionPerformed(self, evt):
            outerInstance.__jButtonExtractActionPerformed(evt)

    class ActionListenerAnonymousInnerClass3():

        def __init__(self, outerInstance):
            self.__outerInstance = outerInstance

        def actionPerformed(self, evt):
            outerInstance.__jButtonSauverActionPerformed(evt)

    class ActionListenerAnonymousInnerClass4():

        def __init__(self, outerInstance):
            self.__outerInstance = outerInstance

        def actionPerformed(self, evt):
            outerInstance.__jButtonVoirContexteActionPerformed(evt)

    def __jButtonVoirContexteActionPerformed(self, evt):
        dialogContexte = None
        sInfosContexte = None

        sInfosContexte = self.m_contexteResolution.ObtenirInfosContexte(True)
        dialogContexte = DialogWindowInfoHTML("Information on the context of extraction of rules", sInfosContexte, self.m_contexteResolution.m_fenetreProprietaire, True)
        dialogContexte.show() #GEN-LAST:event_jButtonVoirContexteActionPerformed



    def __jButtonCopyActionPerformed(self, evt):
        selection = None
        regleCourante = None
        clipboard = None

        # On place la r�gle courante dans le presse papier :
        try:
            clipboard = getToolkit().getSystemClipboard()
            regleCourante = self.ObtenirRegleCourante()
            if regleCourante is not None:
                selection = StringSelection(regleCourante.toString())
            else:
                selection = StringSelection("No rule copied!")
            clipboard.setContents(selection, selection)
        except HeadlessException as e:
            pass #GEN-LAST:event_jButtonCopyActionPerformed


    #save result in a file
    def __jButtonSauverActionPerformed(self, evt):
        sFichierChoisi = None
        fenetreTypeEnregistrement = None
        donnees = None
        enregistreurGraphique = None

        #save a list of rules, dialog
        fenetreTypeEnregistrement = DialogChoiceFileRecords(self.m_contexteResolution, self.m_contexteResolution.m_fenetreProprietaire, True)
        donnees = fenetreTypeEnregistrement.LierStructureDonnees()
        fenetreTypeEnregistrement.show()

        #cancel
        if donnees.m_iTypeEnregistrement == DialogChoiceFileRecords.TYPE_ENREGISTREMENT_ANNULER:
            return

        self.m_contexteResolution.m_sNomUtilisateur = donnees.m_sNomUtilisateur #user name
        self.m_contexteResolution.m_sDescriptionRegles = donnees.m_sDescriptionRegles #rule description

        #save as html file (text or graphic)
        if (donnees.m_iTypeEnregistrement == DialogChoiceFileRecords.TYPE_ENREGISTREMENT_HTML_TEXTE) or (donnees.m_iTypeEnregistrement == DialogChoiceFileRecords.TYPE_ENREGISTREMENT_HTML_GRAPHIQUE):
            sFichierChoisi = ToolsInterface.DialogSauvegardeFichier(self, ENV.REPERTOIRE_RESULTATS, "HTML File", "htm") #"Fichiers HTML", "htm");
        #save as qmr file
        elif donnees.m_iTypeEnregistrement == DialogChoiceFileRecords.TYPE_ENREGISTREMENT_BINAIRE:
            sFichierChoisi = ToolsInterface.DialogSauvegardeFichier(self, ENV.REPERTOIRE_REGLES_QMR, "QuantMiner File", "qmr") #"Fichiers QuantMiner", "qmr");

        #save as csv file
        else:
            sFichierChoisi = ToolsInterface.DialogSauvegardeFichier(self, ENV.REPERTOIRE_RESULTATS, "CSV File", "csv")

        if sFichierChoisi is not None:

            if donnees.m_iTypeEnregistrement == DialogChoiceFileRecords.TYPE_ENREGISTREMENT_HTML_TEXTE:
                super().m_contexteResolution.SauvegarderReglesHTML(sFichierChoisi, self.__m_tReglesFiltrees, False, None)
            elif donnees.m_iTypeEnregistrement == DialogChoiceFileRecords.TYPE_ENREGISTREMENT_HTML_GRAPHIQUE:
                enregistreurGraphique = ResultatsEnregistreurGraphiqueRegle(self, FileTools.ObtenirCheminSansExtension(sFichierChoisi))
                super().m_contexteResolution.SauvegarderReglesHTML(sFichierChoisi, self.__m_tReglesFiltrees, True, enregistreurGraphique)
            elif donnees.m_iTypeEnregistrement == DialogChoiceFileRecords.TYPE_ENREGISTREMENT_BINAIRE:
                super().m_contexteResolution.SauvegarderReglesBinaire(sFichierChoisi, self.__m_tReglesFiltrees)
            elif donnees.m_iTypeEnregistrement == DialogChoiceFileRecords.TYPE_ENREGISTREMENT_CSV:
                super().m_contexteResolution.SauvegarderReglesCsv(sFichierChoisi, self.__m_tReglesFiltrees) #GEN-LAST:event_jButtonSauverActionPerformed

    #Extract the rows for a specific rule
    def __jButtonExtractActionPerformed(self, evt):
        print("m_iIndexCurrentRule" + self.__m_iIndexCurrentRule)
        sFichierChoisi = None
        sFichierChoisi = ToolsInterface.DialogSauvegardeFichier(self, ENV.REPERTOIRE_RESULTATS, "CSV File", "csv")
        print(sFichierChoisi)
        csvPrinter = None
        try:
            csvPrinter = com.Ostermiller.util.ExcelCSVPrinter(FileOutputStream(sFichierChoisi))
        except IOException as e:
            print(e.getMessage())
            return

        if self.__m_tReglesFiltrees is None:
            return
        if self.__m_tReglesFiltrees[self.__m_iIndexCurrentRule] is None:
            return

        left = self.__m_tReglesFiltrees[self.__m_iIndexCurrentRule].leftToString()
        print(left)
        right = self.__m_tReglesFiltrees[self.__m_iIndexCurrentRule].rightToString()
        print(right)

        csvParser = self.m_contexteResolution.m_gestionnaireBD.csvParser

        leftQualitative = self.__m_tReglesFiltrees[self.__m_iIndexCurrentRule].leftQualiToArray()
        leftQuantitative = self.__m_tReglesFiltrees[self.__m_iIndexCurrentRule].leftQuantiToArray()
        rightQualitative = self.__m_tReglesFiltrees[self.__m_iIndexCurrentRule].rightQualiToArray()
        rightQuantitative = self.__m_tReglesFiltrees[self.__m_iIndexCurrentRule].rightQuantiToArray()
        #//////////////////////////////////////////////////////////////////////////////////////////////////////////////
        label = []
        if leftQualitative is not None:
            i = 0
            while i < len(leftQualitative):
                label.append(leftQualitative[i].getM_name())
                i += 1
        if rightQualitative is not None:
            i = 0
            while i < len(rightQualitative):
                label.append(rightQualitative[i].getM_name())
                i += 1
        if leftQuantitative is not None:
            i = 0
            while i < len(leftQuantitative[0]):
                label.append(leftQuantitative[0][i].getM_name())
                i += 1
        if rightQuantitative is not None:
            i = 0
            while i < len(rightQuantitative[0]):
                label.append(rightQuantitative[0][i].getM_name())
                i += 1

        labelString = [None for _ in range(1)]
        labelString = label.toArray(labelString)
        try:
            #csvPrinter.writeln(labelString)
            csvPrinter.writeln(csvParser.m_nameChamp)
        except IOException as e:
            # TODO Auto-generated catch block
            e.printStackTrace()

        #//////////////////////////////////////////////////////////////////////////////////////////////////////////////
        countline = 0
        line = 0
        while line < csvParser.ObtenirNombreLignes():
            running = False

            if leftQualitative is not None:
                iterLeftQuali = leftQualitative.iterator()
                while iterLeftQuali.hasNext():
                    ruleElement =  iterLeftQuali.next()
                    index = csvParser.ObtenirIndiceChamp(ruleElement.getM_name())
                    if csvParser.m_data[line][index] == ruleElement.getM_value():
                        running = True
                    else:
                        running = False
                        break

            if not running:
                continue

            if rightQualitative is not None:
                iterRightQuali = rightQualitative.iterator()
                while iterRightQuali.hasNext():
                    ruleElement =  iterRightQuali.next()
                    index = csvParser.ObtenirIndiceChamp(ruleElement.getM_name())
                    if csvParser.m_data[line][index] == ruleElement.getM_value():
                        running = True
                    else:
                        running = False
                        break

            if not running:
                continue
            if leftQuantitative is not None:
                iterLeftQuanti = leftQuantitative.iterator()
                while iterLeftQuanti.hasNext():
                    disjunctElement = iterLeftQuanti.next()
                    iter = disjunctElement.iterator()
                    while iter.hasNext():
                        ruleElement =  iter.next()
                        index = csvParser.ObtenirIndiceChamp(ruleElement.getM_name())
                        if float(csvParser.m_data[line][index]) >= ruleElement.getM_lower() and float(csvParser.m_data[line][index]) <= ruleElement.getM_upper():
                            running = True
                        else:
                            running = False
                            break
                    if running == True:
                        break #jump out of OR

            if not running:
                continue
            if rightQuantitative is not None:
                iterRightQuanti = rightQuantitative.iterator()
                while iterRightQuanti.hasNext():
                    disjunctElement = iterRightQuanti.next()
                    iter = disjunctElement.iterator()
                    while iter.hasNext():
                        ruleElement =  iter.next()
                        index = csvParser.ObtenirIndiceChamp(ruleElement.getM_name())
                        if float(csvParser.m_data[line][index]) >= ruleElement.getM_lower() and float(csvParser.m_data[line][index]) <= ruleElement.getM_upper():
                            running = True
                        else:
                            running = False
                            break
                    if running == True:
                        break #jump out of OR
            if running:
                countline += 1
                #for (int i = 0; i < (label.size()-1); i++){
                #	System.out.println("*****************"+csvParser.m_data[line][csvParser.ObtenirIndiceChamp(label.get(i))]+ "************")
                try:
                    j = 0
                    while j < csvParser.ObtenirNombreChamps()-1:
                        #csvPrinter.write(csvParser.m_data[line][csvParser.ObtenirIndiceChamp(label.get(i))])
                        csvPrinter.write(csvParser.m_data[line][j])
                        j += 1
                except IOException as e:
                    # TODO Auto-generated catch block
                    e.printStackTrace()
                #}

                try:
                    #System.out.println("###########"+csvParser.m_data[line][csvParser.ObtenirIndiceChamp(label.get(label.size()-1))]+ "##########")
                    #csvPrinter.writeln(csvParser.m_data[line][csvParser.ObtenirIndiceChamp(label.get(label.size()-1))])
                    csvPrinter.writeln(csvParser.m_data[line][csvParser.ObtenirNombreChamps()-1])
                except IOException as e:
                    # TODO Auto-generated catch block
                    e.printStackTrace()
                print()
            line += 1 #END OF FOR LOOP
        try:
            csvPrinter.close()
        except IOException as e:
            e.printStackTrace()
    #once switch to another rule, update the rule index and repaint
    def __jScrollBarReglesAdjustmentValueChanged(self, evt):
        iIndiceRegle = 0

        iIndiceRegle = evt.getValue()
        self.IndiquerRegleCourante(iIndiceRegle) #GEN-LAST:event_jScrollBarReglesAdjustmentValueChanged


    # Variables declaration - do not modify//GEN-BEGIN:variables
    # End of variables declaration//GEN-END:variables

    #Display rules, the third panel

    #The middle panel

    # Indique qu'on a appuy� sur le bouton d'affichage du filtre :
    def IndiquerModificationAffichageFiltre(self):
        self.ArrangerDisposition()


    # Met � jour la liste des r�gles en appliquant les param�tres de tri et de filtrage :
    # Updates the list of rules by applying the sorting and filtering parameters:
    def MettreAJourListeRegles(self):
        listeTempRegles = None
        iIndiceRegle = 0
        regle = None
        comparateur = None
        bTriDecroissant = False
        fSeuilMaxSupportDroite = 0.0
        iNombreMaxOccurrencesDroite = 0

        if self.m_contexteResolution.m_listeRegles is None:
            return

        # Prise en compte des informations entr�es pour le tri et le filtrage :
        super().m_contexteResolution.MettreAJourDonneesInternesFiltre_Filtrage()

        fSeuilMaxSupportDroite = self.__m_panneauTri.ObtenirSueilMaxSupportConsequent()
        iNombreMaxOccurrencesDroite = super().m_contexteResolution.m_gestionnaireBD.ObtenirNombreLignes()
        if fSeuilMaxSupportDroite >= 0.0:
            iNombreMaxOccurrencesDroite = int(((float(iNombreMaxOccurrencesDroite))*(float(fSeuilMaxSupportDroite))))


        listeTempRegles = []
        self.__m_iNombreReglesTotales = len(self.m_contexteResolution.m_listeRegles)

        self.__m_iNombreReglesRetenues = 0
        iIndiceRegle = 0
        while iIndiceRegle<self.__m_iNombreReglesTotales:
            regle = self.m_contexteResolution.m_listeRegles[iIndiceRegle]
            if super().m_contexteResolution.EstRegleValide_Filtrage(regle):
                if regle.m_iOccurrencesDroite <= iNombreMaxOccurrencesDroite:
                    listeTempRegles.append(regle)
                    self.__m_iNombreReglesRetenues += 1
            iIndiceRegle += 1

        # Copie d�finitive dans le tableau des r�gles filtr�es :
        #Final copy in the table of filtered rules:
        self.__m_tReglesFiltrees = None
        if self.__m_iNombreReglesRetenues > 0:
            self.__m_tReglesFiltrees = [None for _ in range(1)]
            self.__m_tReglesFiltrees = (listeTempRegles.toArray(self.__m_tReglesFiltrees))


            # Tri des r�gles :
            bTriDecroissant = self.__m_panneauTri.EstTriDecroissant()
            if self.__m_panneauTri.ObtenirMethodeTri() == PanelSort.METHODE_TRI_SUPPORT:
                comparateur = AssociationRule.ObtenirComparateurSupport(bTriDecroissant)
            elif self.__m_panneauTri.ObtenirMethodeTri() == PanelSort.METHODE_TRI_NOMBRE_ATTRIBUTS:
                comparateur = AssociationRule.ObtenirComparateurNombreAttributs(bTriDecroissant)
            else:
                comparateur = AssociationRule.ObtenirComparateurConfiance(bTriDecroissant)
            java.util.Arrays.sort(self.__m_tReglesFiltrees, comparateur)


        # On d�clare le nouveau tableau des r�gles filtr�es et tri�es :
        # We declare the new table of filtered and sorted rules:
        self.__m_afficheurRegles.DefinirListeRegles(self.__m_tReglesFiltrees)
        if self.__m_iNombreReglesRetenues > 0:
            self.__jScrollBarRegles.setMaximum(self.__m_iNombreReglesRetenues-1)
        else:
            self.__jScrollBarRegles.setMaximum(0)

        if self.__m_iNombreReglesRetenues > 0:
            self.IndiquerRegleCourante(0)
        else:
            self.IndiquerRegleCourante(-1)


    #the index of the rule --middle part
    #This is in the "Results" part (part 5/5) QuantMiner progression
    def IndiquerRegleCourante(self, iIndiceRegleCourante):
        sTexteNumeroRegleCourante = None

        self.__m_iIndexCurrentRule = iIndiceRegleCourante

        if (iIndiceRegleCourante >= 0) and (self.__m_iNombreReglesRetenues>0):
            sTexteNumeroRegleCourante = "Rule "
            sTexteNumeroRegleCourante += String.valueOf(iIndiceRegleCourante+1)
            sTexteNumeroRegleCourante += "/"
            sTexteNumeroRegleCourante += String.valueOf(self.__m_iNombreReglesRetenues)
            sTexteNumeroRegleCourante += " (total : "
            sTexteNumeroRegleCourante += String.valueOf(self.__m_iNombreReglesTotales)
            sTexteNumeroRegleCourante += ")"
        else:
            sTexteNumeroRegleCourante = "No rule selected"

        self.__jTextNumeroRegle.setText(sTexteNumeroRegleCourante)

        #at the same time, repaint the third part to match with the current index of rule!!!
        self.__m_afficheurRegles.DefinirIndiceRegleAffichee(iIndiceRegleCourante)



    def ObtenirRegleCourante(self):
        iIndiceRegleCourante = 0

        iIndiceRegleCourante = self.__m_afficheurRegles.ObtenirIndiceRegleAffichee()

        if (m_tReglesFiltrees is not None) and (iIndiceRegleCourante >= 0) and (self.__m_iNombreReglesRetenues>0):
            return self.__m_tReglesFiltrees[iIndiceRegleCourante]
        else:
            return None



    def ArrangerDisposition(self):
        iDeltaPosX = 0 # Diff�rence de positionnement horizontal entre la position id�ale et celle de l'�diteur de formulaires
        iDeltaPosY = 0 # Diff�rence de positionnement vertical entre la position id�ale et celle de l'�diteur de formulaires

        super().ArrangerDisposition()

        iDeltaPosX = self.__jButtonSauver.getX() - self.m_zoneControles.x
        iDeltaPosY = self.__jButtonSauver.getY() - self.m_zoneControles.y

        self.__jButtonSauver.setLocation(self.__jButtonSauver.getX()-iDeltaPosX, self.__jButtonSauver.getY()-iDeltaPosY)
        self.__jButtonVoirContexte.setLocation(self.__jButtonVoirContexte.getX()-iDeltaPosX, self.__jButtonVoirContexte.getY()-iDeltaPosY)

        if self.__m_panneauTri.EstFiltreAffiche():
            self.__m_panneauTri.setBounds(self.m_zoneControles.x, self.__jButtonSauver.getY()+self.__jButtonSauver.getHeight()+10, self.m_zoneControles.width, self.m_zoneControles.height/2)
        else:
            self.__m_panneauTri.setBounds(self.m_zoneControles.x, self.__jButtonSauver.getY()+self.__jButtonSauver.getHeight()+10, self.m_zoneControles.width, self.__m_panneauTri.ObtenirTailleReduite())

        self.__m_panneauTri.ArrangerDisposition()

        self.__jTextNumeroRegle.setBounds(self.__jTextNumeroRegle.getX()-iDeltaPosX, self.__m_panneauTri.getY()+self.__m_panneauTri.getHeight()+10, self.__jTextNumeroRegle.getWidth(), self.__jTextNumeroRegle.getHeight())

        self.__jButtonExtractRows.setBounds(self.m_zoneControles.width+self.m_zoneControles.x - (self.__jButtonExtractRows.getWidth()), self.__jTextNumeroRegle.getY(), self.__jButtonExtractRows.getWidth(), self.__jButtonExtractRows.getHeight())


        self.__jButtonCopy.setBounds(self.__jButtonExtractRows.getX()-self.__jButtonCopy.getWidth(), self.__jTextNumeroRegle.getY(), self.__jButtonCopy.getWidth(), self.__jButtonCopy.getHeight())

        self.__jScrollBarRegles.setBounds(self.__jScrollBarRegles.getX()-iDeltaPosX, self.__jTextNumeroRegle.getY(), self.__jButtonCopy.getX() - 2 - (self.__jScrollBarRegles.getX()-iDeltaPosX), self.__jScrollBarRegles.getHeight())

        self.__jScrollRegles.setBounds(self.m_zoneControles.x, self.__jTextNumeroRegle.getY()+self.__jTextNumeroRegle.getHeight()+2, self.m_zoneControles.width, self.m_zoneControles.height+self.m_zoneControles.y-(self.__jTextNumeroRegle.getY()+self.__jTextNumeroRegle.getHeight()+2))
        self.__jScrollRegles.validate()

        self.__m_afficheurRegles.setPreferredSize(self.__jScrollRegles.getViewport().getExtentSize())
        self.__m_afficheurRegles.revalidate()

        self.__m_afficheurRegles.DefinirDimensionConteneur(self.__jScrollRegles.getWidth(), self.__jScrollRegles.getHeight())
        self.__m_afficheurRegles.repaint()


