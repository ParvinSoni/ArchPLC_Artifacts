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
import sys
sys.path.append('C:\\Users\\Administrator\\Desktop\\qtm\\src\\')
from database.CsvFileParser import CsvFileParser
from database.DataColumn import DataColumn
# import CsvFileParser
# import sys

class DatabaseAdmin(object):
    # Constant chosen in the domain covered by the float type to indicate a missing value
    VALEUR_MANQUANTE_FLOAT = -(sys.float_info.max / 2.0)
    TYPE_VALEURS_COLONNE_ERREUR = 0
    TYPE_VALEURS_COLONNE_ITEM = 1
    TYPE_VALEURS_COLONNE_REEL = 2
    SOURCE_FICHIER_DBF = 1
    SOURCE_FLUX_ODBC = 2
    SOURCE_FICHIER_CSV = 3

    # Class defining a column of data which must be loaded into memory:
    class DescripteurColonnePriseEnCompte(object):
        def __init__(self, outerInstance, iTypeColonne, bPrendreEnCompte):
            self.m_bPrendreEnCompte = False
            self.m_iTypeColonne = 0
            self.__outerInstance = outerInstance
            self.m_iTypeColonne = iTypeColonne
            self.m_bPrendreEnCompte = bPrendreEnCompte



    def __InitialiserGestionnaireBaseDeDonnees(self):

        self.m_tNomsColonnes = None #name of columns
        self.m_tDonneesColonnes = None #selected columns
        self.m_sNomBaseDeDonnees = None #name of database, i.e. the name of the data file, without path
        self.m_sNomFichier = None
        self.m_sNomFlux = None
        self.m_iTypeSource = 0
        self.__m_iNombreColonnesTotales = 0
        self.m_iNombreLignes = 0
        self.m_colonnesPrisesEnCompte = None #descriptor of column, e.g if selected, column type...

    def __init__(self, sCheminFichier, extension):
        self.csvParser = None
        self.m_tNomsColonnes = None
        self.m_colonnesPrisesEnCompte = None
        self.m_tDonneesColonnes = None
        self.m_sNomBaseDeDonnees = None
        self.m_sNomFichier = None
        self.m_sNomFlux = None
        self.m_iTypeSource = 0
        self.__m_iNombreColonnesTotales = 0
        self.m_iNombreLignes = 0

        if extension == "dbf":
            self.GestionnaireBaseDeDonneesDBF(sCheminFichier)
        if extension == "csv":
            self.GestionnaireBaseDeDonneesCSV(sCheminFichier)


    def GestionnaireBaseDeDonneesDBF(self, sCheminFichier):
        lecteurDBF = None
        champDBF = None
        iIndiceColonne = 0
        iDernierePositionSeparateur = 0

        self.__InitialiserGestionnaireBaseDeDonnees()

        if sCheminFichier == None:
            return


        iDernierePositionSeparateur = sCheminFichier.rfind("\\")

        #Get the base name of the database file without path, e.g. BASE_TEST.dbf
        if iDernierePositionSeparateur == -1:
            self.m_sNomBaseDeDonnees = sCheminFichier
        else:
            try:
                self.m_sNomBaseDeDonnees = sCheminFichier[iDernierePositionSeparateur+1:len(sCheminFichier)]
            except Exception as e:
                self.m_sNomBaseDeDonnees = None

        self.m_sNomFichier = sCheminFichier #m_sNomFichier is the full name of the database file, including path
        self.m_sNomFlux = None
        self.m_iTypeSource = SOURCE_FICHIER_DBF


        try:
            #This function gets all field information, i.e. number of fields, type, name. It also gets number of records/rows
            #This function does not read each row's value
            lecteurDBF = DBFReader(self.m_sNomFichier)
        except Exception as e:
            lecteurDBF = None
            print(e)

        if lecteurDBF == None:
            self.m_sNomBaseDeDonnees = None
            return


        # Obtain number of rows in that file:
        self.m_iNombreLignes = lecteurDBF.ObtenirNombreLignes()

        # Obtain number of columns in that file:
        self.__m_iNombreColonnesTotales = lecteurDBF.ObtenirNombreChamps()

        if self.__m_iNombreColonnesTotales > 0:
            self.m_tNomsColonnes = []
            self.m_colonnesPrisesEnCompte = []
            for i in range(0, self.__m_iNombreColonnesTotales):
                self.m_tNomsColonnes.append(None)
                self.m_colonnesPrisesEnCompte.append(None)

            iIndiceColonne = 0
            while iIndiceColonne < self.__m_iNombreColonnesTotales:

                champDBF = lecteurDBF.ObtenirChamp(iIndiceColonne)

                if not champDBF == None:
                    self.m_tNomsColonnes[iIndiceColonne] = champDBF.ObtenirNom()
                else:
                    self.m_tNomsColonnes[iIndiceColonne] = None
                #At present, all columns are not selected,and by default, we suppose they are item type
                self.m_colonnesPrisesEnCompte[iIndiceColonne] = self.DescripteurColonnePriseEnCompte(self, TYPE_VALEURS_COLONNE_ITEM, False)
                iIndiceColonne += 1

            self.m_tNomsColonnes.sort()


        lecteurDBF.close()

    def GestionnaireBaseDeDonneesCSV(self, sCheminFichier):
        self.csvParser = None
        iIndiceColonne = 0
        iDernierePositionSeparateur = 0
        global SOURCE_FICHIER_CSV

        
        self.__InitialiserGestionnaireBaseDeDonnees()


        if sCheminFichier == None:
            return

        iDernierePositionSeparateur = sCheminFichier.rfind("\\")

        #Get the base name of the database file without path, e.g. BASE_TEST.csv
        if iDernierePositionSeparateur == -1:
            self.m_sNomBaseDeDonnees = sCheminFichier
        else:
            try:
                self.m_sNomBaseDeDonnees = sCheminFichier[iDernierePositionSeparateur+1:len(sCheminFichier)]
            except Exception as e:
                self.m_sNomBaseDeDonnees = None

        self.m_sNomFichier = sCheminFichier #m_sNomFichier is the full name of the database file, including path
        self.m_sNomFlux = None
        self.m_iTypeSource = SOURCE_FICHIER_CSV


        try:
            #This function gets information, i.e. number of fields, name. It also gets number of records/rows
            #This function read each row's value to data
            self.csvParser = CsvFileParser(self.m_sNomFichier)
        except Exception as e:
            self.csvParser = None
            print(e)


        
        if self.csvParser == None:
            self.m_sNomBaseDeDonnees = None
            return

        # Obtain number of rows in that file:
        self.m_iNombreLignes = self.csvParser.ObtenirNombreLignes()


        # Obtain number of columns in that file:
        self.__m_iNombreColonnesTotales = self.csvParser.ObtenirNombreChamps()

        if self.__m_iNombreColonnesTotales > 0:
            self.m_tNomsColonnes = []
            self.m_colonnesPrisesEnCompte = []
            for i in range(0, self.__m_iNombreColonnesTotales):
                self.m_tNomsColonnes.append(None)
                self.m_colonnesPrisesEnCompte.append(None)
                
            iIndiceColonne = 0
            while iIndiceColonne < self.__m_iNombreColonnesTotales:
                self.m_tNomsColonnes[iIndiceColonne] = self.csvParser.ObtenirNomChamps()[iIndiceColonne]

                #At present, all columns are not selected,and by default, we suppose they are item type
                self.m_colonnesPrisesEnCompte[iIndiceColonne] = self.DescripteurColonnePriseEnCompte(self, TYPE_VALEURS_COLONNE_ITEM, False)
                iIndiceColonne += 1
            self.m_tNomsColonnes.sort()


        self.csvParser.close()


    def EstBaseDeDonneesValide(self):
        return (not self.m_sNomBaseDeDonnees == None)

    #Take into consideration all columns
    #In step 1, at the beginning, all columns are selected, and we also get to know column type due to AnalyserTypesChampsBD()
    def PrendreEnCompteToutesLesColonnes(self):
        tTypes = None
        iIndiceColonne = 0

        #Get the type of each column: numerical or categorical
        if self.m_iTypeSource == SOURCE_FICHIER_DBF:
            tTypes = self.AnalyserTypesChampsDBF()
        elif self.m_iTypeSource == SOURCE_FICHIER_CSV:
            tTypes = self.__AnalyserTypesChampsCSV()
        else:
            return

        if tTypes == None:
            return


        iIndiceColonne = 0
        while iIndiceColonne < self.__m_iNombreColonnesTotales:
            self.m_colonnesPrisesEnCompte[iIndiceColonne].m_iTypeColonne = tTypes[iIndiceColonne]
            self.m_colonnesPrisesEnCompte[iIndiceColonne].m_bPrendreEnCompte = True
            iIndiceColonne += 1

    def ConsiderAllColumns(self):
        iIndiceColonne = 0
        iIndiceColonne = 0
        while iIndiceColonne < self.__m_iNombreColonnesTotales:
            self.m_colonnesPrisesEnCompte[iIndiceColonne].m_bPrendreEnCompte = True
            iIndiceColonne += 1

    def NotConsiderAnyColumn(self):
        iIndiceColonne = 0
        iIndiceColonne = 0
        while iIndiceColonne < self.__m_iNombreColonnesTotales:
            self.m_colonnesPrisesEnCompte[iIndiceColonne].m_bPrendreEnCompte = False
            iIndiceColonne += 1


    def __AnalyserTypesChampsCSV(self):
        # TODO Auto-generated method stub
        tTypesChamps = None
        tCorrespondanceIndicesChamps = None
        iIndiceColonne = None
        iIndiceLigne = None
        iIndiceChamp = None
        sValeurItem = None
        tValeursChamps = []

        if self.__m_iNombreColonnesTotales <= 0:
            return None

        if self.csvParser == None:
            return None

        # By default consider all fields type is quantitative :
        tTypesChamps = []
        for i in range(0, self.__m_iNombreColonnesTotales):
            tTypesChamps.append(TYPE_VALEURS_COLONNE_REEL)

        tCorrespondanceIndicesChamps = []
        for i in range(0, self.__m_iNombreColonnesTotales):
            tCorrespondanceIndicesChamps.append(-1)

        iIndiceColonne = 0
        while iIndiceColonne < self.__m_iNombreColonnesTotales:
            tCorrespondanceIndicesChamps[iIndiceColonne] = self.csvParser.ObtenirIndiceChamp(self.m_tNomsColonnes[iIndiceColonne])
            iIndiceColonne += 1

        # Read line by line (200 maximum, number sufficiently significant):
        tValeursChamps = self.csvParser.m_data[0]
        iIndiceLigne = 0
        while (not tValeursChamps == None) and (iIndiceLigne < self.m_iNombreLignes) and (iIndiceLigne < 200):

            iIndiceColonne = 0
            while iIndiceColonne < self.__m_iNombreColonnesTotales:

                iIndiceChamp = tCorrespondanceIndicesChamps[iIndiceColonne] #order in data file
                if iIndiceChamp >= 0:
                    sValeurItem = tValeursChamps[iIndiceChamp]

                    # If until then the field was considered as numeric, we check that the new
                     # value does not contradict it; otherwise it becomes quantitative:
                    if tTypesChamps[iIndiceColonne] == TYPE_VALEURS_COLONNE_REEL:
                        if not sValeurItem == None:
                            if not sValeurItem.strip() == "":
                                try:
                                    float(sValeurItem) #Throws: if the string does not contain a parsable float
                                except Exception as e:
                                    # print('Error: {}'.format(e))
                                    tTypesChamps[iIndiceColonne] = TYPE_VALEURS_COLONNE_ITEM


                iIndiceColonne += 1

            iIndiceLigne += 1
            if iIndiceLigne == self.m_iNombreLignes - 1:
                break
            tValeursChamps = self.csvParser.m_data[iIndiceLigne]

        # Close the file:

        return tTypesChamps




    def ObtenirNomBaseDeDonnees(self):
        return self.m_sNomBaseDeDonnees


    def ObtenirNombreLignes(self):
        return self.m_iNombreLignes



    def __ObtenirIndiceColonneDepuisNom(self, sNomColonne):
        bTrouveColonne = False
        iIndiceColonne = 0

        if sNomColonne == None:
            return -1

        iIndiceColonne = 0
        while ((not bTrouveColonne)) and (iIndiceColonne < len(self.m_tNomsColonnes)):

            if sNomColonne == self.m_tNomsColonnes[iIndiceColonne]:
                bTrouveColonne = True
            else:
                iIndiceColonne += 1


        if bTrouveColonne:
            return iIndiceColonne
        else:
            return -1



    # Call this function to declare each column of the initial database that you want to take
    # taken into account when loading data into memory:
    def DefinirPriseEnCompteColonne(self, sNomColonne, iTypeValeurs, bPrendreEnCompte):
        iIndiceColonnePriseEnCompte = 0

        iIndiceColonnePriseEnCompte = self.__ObtenirIndiceColonneDepuisNom(sNomColonne)
        if iIndiceColonnePriseEnCompte < 0:
            return

        self.m_colonnesPrisesEnCompte[iIndiceColonnePriseEnCompte].m_iTypeColonne = iTypeValeurs
        self.m_colonnesPrisesEnCompte[iIndiceColonnePriseEnCompte].m_bPrendreEnCompte = bPrendreEnCompte



    def ObtenirTypeColonne(self, sNomColonne):
        iIndiceColonnePriseEnCompte = 0

        iIndiceColonnePriseEnCompte = self.__ObtenirIndiceColonneDepuisNom(sNomColonne)
        if iIndiceColonnePriseEnCompte < 0:
            return TYPE_VALEURS_COLONNE_ERREUR
        else:
            return self.m_colonnesPrisesEnCompte[iIndiceColonnePriseEnCompte].m_iTypeColonne


    def EstPriseEnCompteColonne(self, sNomColonne):
        iIndiceColonnePriseEnCompte = 0

        iIndiceColonnePriseEnCompte = self.__ObtenirIndiceColonneDepuisNom(sNomColonne)
        if iIndiceColonnePriseEnCompte < 0:
            return False
        else:
            return self.m_colonnesPrisesEnCompte[iIndiceColonnePriseEnCompte].m_bPrendreEnCompte


    # Get the initial number of columns, i.e. the number of columns in data file
    def ObtenirNombreColonnesBDInitiale(self):
        return self.__m_iNombreColonnesTotales

    def ObtenirNombreColonnesPrisesEnCompte(self):
        iIndiceColonne = 0
        iNombreColonnesPrisesEnCompte = 0

        iNombreColonnesPrisesEnCompte = 0
        iIndiceColonne = 0
        while iIndiceColonne < len(self.m_tNomsColonnes):
            if self.m_colonnesPrisesEnCompte[iIndiceColonne].m_bPrendreEnCompte:
                iNombreColonnesPrisesEnCompte += 1
            iIndiceColonne += 1

        return iNombreColonnesPrisesEnCompte


    # Get the column information about the selected column in step 1, i.e the data load step
    # m_tDonneesColonnes contains all the selected columns
    def ObtenirColonneBDPriseEnCompte(self, iIndiceColonne):
        if self.m_tDonneesColonnes == None:
            return None

        if iIndiceColonne < len(self.m_tDonneesColonnes):
            return self.m_tDonneesColonnes[iIndiceColonne]
        else:
            return None

    # Return the name of the 'iIndexColumn'-th column in the original database:
    def ObtenirNomColonneBDInitiale(self, iIndiceColonne):
        if iIndiceColonne < self.__m_iNombreColonnesTotales:
            return self.m_tNomsColonnes[iIndiceColonne]
        else:
            return None



    # Returns the name of the 'iIndexColumn'-th column taken into account:
    def ObtenirNomColonneBDPriseEnCompte(self, iIndiceColonne):
        colonnePriseEnCompte = None

        colonnePriseEnCompte = self.ObtenirColonneBDPriseEnCompte(iIndiceColonne)

        if not colonnePriseEnCompte == None:
            return colonnePriseEnCompte.m_sNomColonne
        else:
            return None



    #Anaylize the type of each column, numerical or categorical
    # Analyze and extract the presumed types of the fields contained in the database (returns an array of types):
    def AnalyserTypesChampsDBF(self):
        lecteurDBF = None
        champDBF = None
        iIndiceLigne = 0
        iIndiceColonne = 0
        sValeurItem = None
        tValeursChamps = None
        tCorrespondanceIndicesChamps = None # Correspondence table between the number of a column and the index of the field it represents in the file
        iIndiceChamp = 0
        tTypesChamps = None


        if self.__m_iNombreColonnesTotales <= 0:
            return None

        # By default consider all fields type is quantitative :
        tTypesChamps = []
        for i in range(0, self.__m_iNombreColonnesTotales):
            tTypesChamps.append(TYPE_VALEURS_COLONNE_REEL) #assigned the specified int value to each element in the array


        # Open the DBF file and read the header:   
        try:
            lecteurDBF = DBFReader(self.m_sNomFichier)
        except Exception as e:
            lecteurDBF = None
            print(e)

        if lecteurDBF == None:
            return None

        # make a table of correspondence between names and indices of fields:
        # [iIndexColumn] -> order in data file
        tCorrespondanceIndicesChamps = []
        for i in range(0, self.__m_iNombreColonnesTotales):
            tCorrespondanceIndicesChamps.append(-1)

        iIndiceColonne = 0
        while iIndiceColonne < self.__m_iNombreColonnesTotales:
            tCorrespondanceIndicesChamps[iIndiceColonne] = lecteurDBF.ObtenirIndiceChamp(self.m_tNomsColonnes[iIndiceColonne])
            iIndiceColonne += 1


        # Read line by line (200 maximum, number suffisemment significatif) :
        tValeursChamps = lecteurDBF.LireEnregistrementSuivant()
        iIndiceLigne = 0
        while (not tValeursChamps == None) and (iIndiceLigne < self.m_iNombreLignes) and (iIndiceLigne < 200):

            iIndiceColonne = 0
            while iIndiceColonne < self.__m_iNombreColonnesTotales:

                iIndiceChamp = tCorrespondanceIndicesChamps[iIndiceColonne] #order in data file
                if iIndiceChamp >= 0:

                    sValeurItem = tValeursChamps[iIndiceChamp]

                    # If until then the field was considered as numeric, we check that the new
                    # value does not contradict it; otherwise it becomes quantitative:
                    if tTypesChamps[iIndiceColonne] == TYPE_VALEURS_COLONNE_REEL:
                        if not sValeurItem == None:
                            if not sValeurItem.strip() == "":
                                try:
                                    float(sValeurItem) #Throws: if the string does not contain a parsable float
                                except Exception as e:
                                    tTypesChamps[iIndiceColonne] = TYPE_VALEURS_COLONNE_ITEM


                iIndiceColonne += 1

            iIndiceLigne += 1
            if iIndiceLigne == self.m_iNombreLignes - 1:
                break
            tValeursChamps = lecteurDBF.LireEnregistrementSuivant()

        # Fermeture du fichier :
        lecteurDBF.close()

        return tTypesChamps


    # Store in memory the content of all the columns declared with successive calls
    # of the 'TakeColumnAccount' function:
    def ChargerDonneesPrisesEnCompte(self):
        iNombreColonnesPrisesEnCompte = 0

        iNombreColonnesPrisesEnCompte = self.ObtenirNombreColonnesPrisesEnCompte()

        if iNombreColonnesPrisesEnCompte > 0:
            self.m_tDonneesColonnes = []
            for i in range(0, iNombreColonnesPrisesEnCompte):
                self.m_tDonneesColonnes.append(None)
        else:
            self.m_tDonneesColonnes = None

        if (iNombreColonnesPrisesEnCompte <= 0) or (self.m_iNombreLignes <= 0):
            return

        # The function delegates the work according to the type of source data:
        if self.m_iTypeSource == SOURCE_FICHIER_DBF:
            self.__ChargerDonneesPrisesEnCompteDBF()
        elif self.m_iTypeSource == SOURCE_FICHIER_CSV:
            self.__ChargerDonneesPrisesEnCompteCSV()
        else:
            return



    def __ChargerDonneesPrisesEnCompteCSV(self):
        # TODO Auto-generated method stub
        if self.csvParser == None:
            return

        iIndiceLigne = 0
        iIndiceColonne = 0
        colonnePriseEnCompte = None
        colonneCourante = None
        sValeurItem = None
        tValeursChamps = None
        # Correspondence table between the number of a column and the index of the field it represents in the file
        tCorrespondanceIndicesChamps = None 
        iIndiceChamp = 0
        iNombreColonnesPrisesEnCompte = 0
        iIndiceColonnePriseEnCompte = 0

        if self.m_tDonneesColonnes == None:
            return

        iNombreColonnesPrisesEnCompte = len(self.m_tDonneesColonnes)


        tCorrespondanceIndicesChamps = []
        for i in range(0, iNombreColonnesPrisesEnCompte):
            tCorrespondanceIndicesChamps.append(-1)

        iIndiceColonnePriseEnCompte = 0
        iIndiceColonne = 0
        while iIndiceColonne < self.__m_iNombreColonnesTotales:

            colonnePriseEnCompte = self.m_colonnesPrisesEnCompte[iIndiceColonne]

            if colonnePriseEnCompte.m_bPrendreEnCompte:
                tCorrespondanceIndicesChamps[iIndiceColonnePriseEnCompte] = self.csvParser.ObtenirIndiceChamp(self.m_tNomsColonnes[iIndiceColonne])

                self.m_tDonneesColonnes[iIndiceColonnePriseEnCompte] = DataColumn(self.m_tNomsColonnes[iIndiceColonne], colonnePriseEnCompte.m_iTypeColonne, self.m_iNombreLignes, tCorrespondanceIndicesChamps[iIndiceColonnePriseEnCompte])

                iIndiceColonnePriseEnCompte += 1
            iIndiceColonne += 1



        # Read line by line:
        iIndiceLigne = 0
        tValeursChamps = self.csvParser.m_data[iIndiceLigne]

        while (not tValeursChamps == None) and (iIndiceLigne < self.m_iNombreLignes):

            iIndiceColonne = 0
            while iIndiceColonne < iNombreColonnesPrisesEnCompte:

                iIndiceChamp = tCorrespondanceIndicesChamps[iIndiceColonne]
                if iIndiceChamp >= 0:

                    colonneCourante = self.m_tDonneesColonnes[iIndiceColonne]
                    sValeurItem = tValeursChamps[iIndiceChamp]

                    if colonneCourante.m_iTypeValeurs == TYPE_VALEURS_COLONNE_ITEM:
                        colonneCourante.m_tIDQualitatif[iIndiceLigne] = colonneCourante.RepertorierValeur(sValeurItem)
                        
                    elif colonneCourante.m_iTypeValeurs == TYPE_VALEURS_COLONNE_REEL:
                        fValeurReelle = 0.0
                        try:
                            fValeurReelle = float(sValeurItem)
                        except Exception as e:
                            fValeurReelle = VALEUR_MANQUANTE_FLOAT # wrong or missing value
                        colonneCourante.AssignerValeurReelle(iIndiceLigne, fValeurReelle)


                iIndiceColonne += 1

            iIndiceLigne += 1
            if iIndiceLigne == self.m_iNombreLignes:
                break
            tValeursChamps = self.csvParser.m_data[iIndiceLigne]

        # Close the file:


        # Post processing on numeric type columns (sorted table of value indices):
        iIndiceColonne = 0
        while iIndiceColonne < iNombreColonnesPrisesEnCompte:
            colonneCourante = self.m_tDonneesColonnes[iIndiceColonne]
            if colonneCourante.m_iTypeValeurs == TYPE_VALEURS_COLONNE_REEL:
                colonneCourante.ConstruireTableauValeursQuantitativesTriees()
            iIndiceColonne += 1



    # Version de 'ChargerDonneesPrisesEnCompte' op�rant sur les fichiers DBF :
    def __ChargerDonneesPrisesEnCompteDBF(self):

        lecteurDBF = None
        champDBF = None
        iIndiceLigne = 0
        iIndiceColonne = 0
        colonnePriseEnCompte = None
        colonneCourante = None
        sValeurItem = None
        tValeursChamps = None
        tCorrespondanceIndicesChamps = None # Table de correspondance entre le num�ro d'une colonne et l'indice du champ qu'elle repr�sente dans le fichier
        iIndiceChamp = 0
        iNombreColonnesPrisesEnCompte = 0
        iIndiceColonnePriseEnCompte = 0

        if self.m_tDonneesColonnes == None:
            return

        iNombreColonnesPrisesEnCompte = len(self.m_tDonneesColonnes)


        try:
            lecteurDBF = DBFReader(self.m_sNomFichier)
        except Exception as e:
            lecteurDBF = None
            print(e)

        if lecteurDBF == None:
            return


        tCorrespondanceIndicesChamps = []
        for i in range(0, iNombreColonnesPrisesEnCompte):
            tCorrespondanceIndicesChamps.append(-1)

        iIndiceColonnePriseEnCompte = 0
        iIndiceColonne = 0
        while iIndiceColonne < self.__m_iNombreColonnesTotales:

            colonnePriseEnCompte = self.m_colonnesPrisesEnCompte[iIndiceColonne]

            if colonnePriseEnCompte.m_bPrendreEnCompte:

                tCorrespondanceIndicesChamps[iIndiceColonnePriseEnCompte] = lecteurDBF.ObtenirIndiceChamp(self.m_tNomsColonnes[iIndiceColonne])
                self.m_tDonneesColonnes[iIndiceColonnePriseEnCompte] = DataColumn(self.m_tNomsColonnes[iIndiceColonne], colonnePriseEnCompte.m_iTypeColonne, self.m_iNombreLignes, tCorrespondanceIndicesChamps[iIndiceColonnePriseEnCompte])

                iIndiceColonnePriseEnCompte += 1
            iIndiceColonne += 1



        # Lecture ligne par ligne :
        tValeursChamps = lecteurDBF.LireEnregistrementSuivant()
        iIndiceLigne = 0
        while (not tValeursChamps == None) and (iIndiceLigne < self.m_iNombreLignes):

            iIndiceColonne = 0
            while iIndiceColonne < iNombreColonnesPrisesEnCompte:

                iIndiceChamp = tCorrespondanceIndicesChamps[iIndiceColonne]
                if iIndiceChamp >= 0:

                    colonneCourante = self.m_tDonneesColonnes[iIndiceColonne]
                    sValeurItem = tValeursChamps[iIndiceChamp]

                    if colonneCourante.m_iTypeValeurs == TYPE_VALEURS_COLONNE_ITEM:
                        colonneCourante.m_tIDQualitatif[iIndiceLigne] = colonneCourante.RepertorierValeur(sValeurItem)
                    elif colonneCourante.m_iTypeValeurs == TYPE_VALEURS_COLONNE_REEL:
                        fValeurReelle = 0.0
                        try:
                            fValeurReelle = float(sValeurItem)
                        except Exception as e:
                            fValeurReelle = VALEUR_MANQUANTE_FLOAT # valeur erronn�e ou manquante
                        colonneCourante.AssignerValeurReelle(iIndiceLigne, fValeurReelle)


                iIndiceColonne += 1

            iIndiceLigne += 1
            tValeursChamps = lecteurDBF.LireEnregistrementSuivant()

        # Fermeture du fichier :
        lecteurDBF.close()


        # Post traitement sur les colonnes de type num�rique (table tri�e des indices des valeurs) :
        iIndiceColonne = 0
        while iIndiceColonne < iNombreColonnesPrisesEnCompte:
            colonneCourante = self.m_tDonneesColonnes[iIndiceColonne]
            if colonneCourante.m_iTypeValeurs == TYPE_VALEURS_COLONNE_REEL:
                colonneCourante.ConstruireTableauValeursQuantitativesTriees()
            iIndiceColonne += 1



    def EcrireDescriptifColonnesQuantitatives(self):
        iIndiceColonne = 0
        colonnePriseEnCompte = None
        sTexteDescriptif = None

        if self.m_tDonneesColonnes == None:
            return "No column selected."

        sTexteDescriptif = str("")

        sTexteDescriptif += "ATTRIBUTS QUANTITATIFS :\n\n"
        iIndiceColonne = 0
        while iIndiceColonne<len(self.m_tDonneesColonnes):
            if self.m_tDonneesColonnes[iIndiceColonne].m_iTypeValeurs == TYPE_VALEURS_COLONNE_REEL:
                sTexteDescriptif += self.m_tDonneesColonnes[iIndiceColonne].m_sNomColonne
                sTexteDescriptif += ", domaine [ "
                sTexteDescriptif += String.valueOf(self.m_tDonneesColonnes[iIndiceColonne].ObtenirBorneMin())
                sTexteDescriptif += ", "
                sTexteDescriptif += String.valueOf(self.m_tDonneesColonnes[iIndiceColonne].ObtenirBorneMax())
                sTexteDescriptif += " ]\n"
            iIndiceColonne += 1

        return sTexteDescriptif



    # Lib�re de la m�moire tous les champs qui ont �t� charg�s : 
    def LibererDonneesEnMemoire(self):
        self.m_tDonneesColonnes = None

