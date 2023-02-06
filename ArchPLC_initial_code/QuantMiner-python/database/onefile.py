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
import csv


class CsvFileParser(object):

    def __init__(self, nomFichier):
        self.m_InputStream = None
        self.m_iNombreChamps = 0
        self.m_iNombreLignes = 0
        self.__csvParser = None
        self.m_data = None
        self.m_nameChamp = None
        self.rows = []

        try:
            self.m_InputStream = open(nomFichier)
            try:
                self.__csvParser = csv.reader(self.m_InputStream)
            except Exception as e:
                print('Error: {}'.format(e))
        except Exception as e:
            print('Error: {}'.format(e))
            self.m_InputStream = None

        if self.m_InputStream == None:
            return

        # try:
        #     self.m_data = self.__csvParser
        #     # print(self.m_data)
        #     # sys.exit()
        # except Exception as e:
        #     print('Error: {}'.format(e))

        try:
            for row in self.__csvParser:
                self.rows.append(row)
            self.m_nameChamp = self.rows[0]
            self.m_iNombreChamps = len(self.rows[0]) #  for column names
            self.m_data = self.rows
        except Exception as e:
            print('Error: {}'.format(e))
        self.m_iNombreLignes = len(self.rows) -1 # -1 for column names
        print()

    def ObtenirNombreLignes(self):
        return self.m_iNombreLignes

    def ObtenirNombreChamps(self):
        return self.m_iNombreChamps

    def ObtenirNomChamps(self):
        return self.m_nameChamp

    def close(self):
        try:
            self.m_InputStream.close()
        except Exception as e:
            print('Error: {}'.format(e))

    def ObtenirIndiceChamp(self, sNomChamp):
        iIndiceChamp = 0
        bChampTrouve = False
        sNomChampEnumere = None

        if sNomChamp == None:
            return -1

        iIndiceChamp = 0
        #print("===========number of columns ==========" + m_iNombreChamps)
        while ((not bChampTrouve)) and (iIndiceChamp < self.m_iNombreChamps):
            sNomChampEnumere = self.m_nameChamp[iIndiceChamp]
            #print("sNomChampEnumere is " + sNomChampEnumere)
            #print("passed in sNomChamp is " + sNomChamp)
            # print(sNomChampEnumere)
            if sNomChamp == sNomChampEnumere.strip(): # 
                bChampTrouve = True
            else:
                iIndiceChamp += 1

        if bChampTrouve:
            #print("---------find-----------")
            return iIndiceChamp

        else:
            return -1


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
                self.m_colonnesPrisesEnCompte[iIndiceColonne] = self.DescripteurColonnePriseEnCompte(self, self.TYPE_VALEURS_COLONNE_ITEM, False)
                iIndiceColonne += 1

            self.m_tNomsColonnes.sort()


        lecteurDBF.close()

    def GestionnaireBaseDeDonneesCSV(self, sCheminFichier):
        self.csvParser = None
        iIndiceColonne = 0
        iDernierePositionSeparateur = 0

        
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
        self.m_iTypeSource = self.SOURCE_FICHIER_CSV


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
                self.m_colonnesPrisesEnCompte[iIndiceColonne] = self.DescripteurColonnePriseEnCompte(self, self.TYPE_VALEURS_COLONNE_ITEM, False)
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
        if self.m_iTypeSource == self.SOURCE_FICHIER_DBF:
            tTypes = self.AnalyserTypesChampsDBF()
        elif self.m_iTypeSource == self.SOURCE_FICHIER_CSV:
            tTypes = self.__AnalyserTypesChampsCSV()
            print("tTypes: " + str(tTypes))
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
            tTypesChamps.append(self.TYPE_VALEURS_COLONNE_REEL)


        tCorrespondanceIndicesChamps = []
        for i in range(0, self.__m_iNombreColonnesTotales):
            tCorrespondanceIndicesChamps.append(-1)

        iIndiceColonne = 0
        while iIndiceColonne < self.__m_iNombreColonnesTotales:
            tCorrespondanceIndicesChamps[iIndiceColonne] = self.csvParser.ObtenirIndiceChamp(self.m_tNomsColonnes[iIndiceColonne])
            iIndiceColonne += 1

        

        # print("self.csvParser.m_data: " + str(self.csvParser.m_data))
        # sys.exit()
        # Read line by line (200 maximum, number sufficiently significant):
        tValeursChamps = self.csvParser.m_data[1]
        iIndiceLigne = 0
        while (not tValeursChamps == None) and (iIndiceLigne < self.m_iNombreLignes) and (iIndiceLigne < 200):

            iIndiceColonne = 0
            while iIndiceColonne < self.__m_iNombreColonnesTotales:

                iIndiceChamp = tCorrespondanceIndicesChamps[iIndiceColonne] #order in data file
                if iIndiceChamp >= 0:
                    sValeurItem = tValeursChamps[iIndiceChamp]

                    # If until then the field was considered as numeric, we check that the new
                     # value does not contradict it; otherwise it becomes quantitative:
                    if tTypesChamps[iIndiceColonne] == self.TYPE_VALEURS_COLONNE_REEL:
                        if not sValeurItem == None:
                            if not sValeurItem.strip() == "":
                                try:
                                    # print("sValeurItem CCCCCCCCCC: " + str(sValeurItem))
                                    float(sValeurItem) #Throws: if the string does not contain a parsable float
                                except Exception as e:
                                    # print('Error: {}'.format(e))
                                    tTypesChamps[iIndiceColonne] = self.TYPE_VALEURS_COLONNE_ITEM


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
        # print(self.m_tDonneesColonnes[iIndiceColonne])
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
                                    tTypesChamps[iIndiceColonne] = self.TYPE_VALEURS_COLONNE_ITEM


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
        if self.m_iTypeSource == self.SOURCE_FICHIER_DBF:
            self.__ChargerDonneesPrisesEnCompteDBF()
        elif self.m_iTypeSource == self.SOURCE_FICHIER_CSV:
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
        iIndiceLigne = 1
        tValeursChamps = self.csvParser.m_data[iIndiceLigne]

        while (not tValeursChamps == None) and (iIndiceLigne < self.m_iNombreLignes):

            iIndiceColonne = 0
            while iIndiceColonne < iNombreColonnesPrisesEnCompte:

                iIndiceChamp = tCorrespondanceIndicesChamps[iIndiceColonne]

                if iIndiceChamp >= 0:
                    # current column
                    colonneCourante = self.m_tDonneesColonnes[iIndiceColonne]
                    # print("colonneCourante: " + str(colonneCourante))
                    sValeurItem = tValeursChamps[iIndiceChamp]
                    # print(tValeursChamps)

                    if colonneCourante.m_iTypeValeurs == self.TYPE_VALEURS_COLONNE_ITEM:
                        # print("sValeurItem: " + str(sValeurItem))
                        colonneCourante.m_tIDQualitatif[iIndiceLigne] = colonneCourante.RepertorierValeur(sValeurItem)
                        
                    elif colonneCourante.m_iTypeValeurs == self.TYPE_VALEURS_COLONNE_REEL:
                        fValeurReelle = 0.0
                        try:
                            fValeurReelle = float(sValeurItem)
                        except Exception as e:
                            fValeurReelle = self.VALEUR_MANQUANTE_FLOAT # wrong or missing value
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
            if colonneCourante.m_iTypeValeurs == self.TYPE_VALEURS_COLONNE_REEL:
                colonneCourante.ConstruireTableauValeursQuantitativesTriees()
            iIndiceColonne += 1



    # Version of 'LoadDataTakenInAccount' operating on DBF files:
    def __ChargerDonneesPrisesEnCompteDBF(self):

        lecteurDBF = None
        champDBF = None
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


import os

cwd = os.getcwd()
sys.path.append(cwd)
# sys.path.append('C:\\Users\\aalsahee\\python_physical_model\\Saudi\\trace\\Traces\\qtm\\src\\')

from tools.dataStructures.WordList import WordList
# from database.DatabaseAdmin import DatabaseAdmin


class DataColumn(object):

    # Member about unique the column of value categorical:
    # Member about unique column that value quantitative:

    def __init__(self, sNomColonne, iTypeValeurs, iNombreLignes, index):
        self.m_sNomColonne = None
        self.m_iIndiceChamp = 0
        self.m_iTypeValeurs = 0
        self.m_iNombreLignes = 0
        self.m_tIDQualitatif = None
        self.m_listeValeurs = None
        self.m_tValeurReelle = None
        self.m_tValeursReellesTriees = None
        self.m_iNombreValeursReellesCorrectes = 0
        self.m_tValeursUniques = None
        self.m_tCumulSupportCroissant = None
        self.m_iNombreValeursUniques = 0
        self.m_fValeurMin = 0.0
        self.m_fValeurMax = 0.0
        self.__m_bBornesReellesDefinies = False


        self.m_sNomColonne = sNomColonne
        self.m_iTypeValeurs = iTypeValeurs
        self.m_iNombreLignes = iNombreLignes
        self.__m_bBornesReellesDefinies = False
        self.m_iIndiceChamp = index
        self.m_fValeurMin = 0.0
        self.m_fValeurMax = 0.0
        self.m_iNombreValeursReellesCorrectes = 0
        self.m_tValeursReellesTriees = None

        if iNombreLignes > 0:
            if self.m_iTypeValeurs == DatabaseAdmin.TYPE_VALEURS_COLONNE_ITEM:
                self.m_listeValeurs = WordList()
                self.m_tIDQualitatif = []
                for i in range(0, iNombreLignes):
                    self.m_tIDQualitatif.append(0)

            elif self.m_iTypeValeurs == DatabaseAdmin.TYPE_VALEURS_COLONNE_REEL:
                self.m_tValeurReelle = []
                for i in range(0, iNombreLignes):
                    self.m_tValeurReelle.append(0)
        else:
            self.m_listeValeurs = None
            self.m_tIDQualitatif = None
            self.m_tValeurReelle = None


    def RepertorierValeur(self, sValeur):
        return self.m_listeValeurs.InsererMot(sValeur)


    #    *
    #     * Function allowing to make the correspondence between the textual representation of a value and its numerical identifier
    #     * @param sValeur
    #     * @return short
    #     
    def ObtenirNumeroCorrespondance(self, sValeur):
        infosMot = None

        infosMot = self.m_listeValeurs.ChercherInfosMot(sValeur)
        if infosMot is not None:
            return infosMot.m_iIdentifiantUnique
        else:
            return -1


    #    *
    #     *  Unique for cateogorical (qualitative) values, it returns the number of occurrences of a given item in all the tuples
    #     * @param sValeur The item
    #     * @return number of occurrences
    #     
    def ObtenirNombreOccurrencesItem(self, sValeur):
        infosMot = None

        infosMot = self.m_listeValeurs.ChercherInfosMot(sValeur)
        if infosMot is None:
            return 0
        else:
            return infosMot.m_iOccurrences


    # For quantitative values only, returns the smallest value found in the data:
    def ObtenirBorneMin(self):
        return self.m_fValeurMin


    # For quantitative values only, returns the largest value found in the data:
    def ObtenirBorneMax(self):
        return self.m_fValeurMax


    #    *
    #     * keeps in memory a real value and updates the min and max if necessary
    #     * @param iIndiceLigne
    #     * @param fValeur
    #     
    def AssignerValeurReelle(self, iIndiceLigne, fValeur):

        if not fValeur == DatabaseAdmin.VALEUR_MANQUANTE_FLOAT:

            if self.__m_bBornesReellesDefinies:
                if fValeur < self.m_fValeurMin:
                    self.m_fValeurMin = fValeur
                if fValeur > self.m_fValeurMax:
                    self.m_fValeurMax = fValeur
            else:
                self.m_fValeurMin = self.m_fValeurMax = fValeur
                self.__m_bBornesReellesDefinies = True


        self.m_tValeurReelle[iIndiceLigne] = fValeur



    def ObtenirNombreValeursDifferentes(self):
        return self.m_listeValeurs.ObtenirNombreMots()

    def ConstituerTableauValeurs(self):
        iNombreValeurs = 0
        iIdentifiantValeur = 0
        tTableauValeurs = []

        if not self.m_iTypeValeurs == DatabaseAdmin.TYPE_VALEURS_COLONNE_ITEM:
            return None

        iNombreValeurs = self.m_listeValeurs.ObtenirNombreMots()
        # print("iNombreValeurs: " +str(iNombreValeurs))
        if iNombreValeurs <= 0:
            return None

        # tTableauValeurs = []
        for i in range(0, iNombreValeurs):
            #Assigns the specified Object reference to each element of the specified array of Objects
            tTableauValeurs.append(None)
        # Initiate Course
        self.m_listeValeurs.InicierParcours()
        # Move forward
        while self.m_listeValeurs.AvancerParcours():
            # GetInfosWord Browsed
            iIdentifiantValeur = (self.m_listeValeurs.ObtenirInfosMotParcouru()).m_iIdentifiantUnique
            # print(self.m_listeValeurs)
            if (iIdentifiantValeur >= 0) and (iIdentifiantValeur < iNombreValeurs):
                tTableauValeurs[iIdentifiantValeur] = self.m_listeValeurs.ObtenirMotParcouru()
                # print(tTableauValeurs[iIdentifiantValeur])
                # print(tTableauValeurs)
        #         print("!")
        # print("XXX")
        # print(tTableauValeurs)
        return tTableauValeurs


    #    *
    #     *  fills an additional table containing all the numerical values of the column, but sorted.
    #     
    def ConstruireTableauValeursQuantitativesTriees(self):
        fValeurCourante = 0.0
        fValeurSuivante = 0.0
        iValeurUniqueCourante = 0
        iValeurUniqueSuivante = 0
        iIndiceValeur = 0
        iIndiceValeurSuivante = 0
        iIndiceRemplissage = 0
        iSupportCumule = 0


        if not self.m_iTypeValeurs == DatabaseAdmin.TYPE_VALEURS_COLONNE_REEL:
            return


        # We count the number of non-missing numerical values:
        self.m_iNombreValeursReellesCorrectes = 0
        iIndiceValeur = 0
        while iIndiceValeur < self.m_iNombreLignes:
            if not self.m_tValeurReelle[iIndiceValeur] == DatabaseAdmin.VALEUR_MANQUANTE_FLOAT:
                self.m_iNombreValeursReellesCorrectes += 1
            iIndiceValeur += 1

        if self.m_iNombreValeursReellesCorrectes == 0:
            self.m_tValeursReellesTriees = None
        else:
            self.m_tValeursReellesTriees = []
            for i in range(0, self.m_iNombreValeursReellesCorrectes):
                self.m_tValeursReellesTriees.append(0)


        # We fill the table with the correct numerical values:
        iIndiceValeur = 0
        while iIndiceValeur < self.m_iNombreValeursReellesCorrectes:
            if not self.m_tValeurReelle[iIndiceValeur] == DatabaseAdmin.VALEUR_MANQUANTE_FLOAT:
                self.m_tValeursReellesTriees[iIndiceValeur] = self.m_tValeurReelle[iIndiceValeur]
            iIndiceValeur += 1


        # Then we sort them:
        if self.m_tValeursReellesTriees is not None:
            self.m_tValeursReellesTriees.sort()

        #----------------------------------------------
        # CONSTRUCTION OF THE TABLE OF UNIQUE VALUES:
        if self.m_iNombreValeursReellesCorrectes == 0:
            self.m_tValeursUniques = None
        else:
            self.m_tValeursUniques = []
            for i in range(0, self.m_iNombreValeursReellesCorrectes):
                self.m_tValeursUniques.append(0)

        self.m_iNombreValeursUniques = 0
        iIndiceValeur=0
        while iIndiceValeur < self.m_iNombreValeursReellesCorrectes:
            fValeurSuivante = fValeurCourante = self.m_tValeursReellesTriees[iIndiceValeur]

            iIndiceValeurSuivante = iIndiceValeur + 1
            while (fValeurSuivante == fValeurCourante) and (iIndiceValeurSuivante < self.m_iNombreValeursReellesCorrectes):
                fValeurSuivante = self.m_tValeursReellesTriees[iIndiceValeurSuivante]
                if fValeurSuivante == fValeurCourante:
                    iIndiceValeurSuivante += 1

            # Filling of the table for the same cumulative support value:
            iIndiceRemplissage = iIndiceValeur
            while iIndiceRemplissage < iIndiceValeurSuivante:
                self.m_tValeursUniques[iIndiceRemplissage] = self.m_iNombreValeursUniques
                iIndiceRemplissage += 1

            iIndiceValeur = iIndiceValeurSuivante
            self.m_iNombreValeursUniques += 1

        #-----------------------------------------------
        # CONSTRUCTION DU TABLEAU DES SUPPORTS CUMULES :

        if self.m_iNombreValeursUniques == 0:
            self.m_tCumulSupportCroissant = None
        else:
            self.m_tCumulSupportCroissant = []
            for i in range(0, self.m_iNombreValeursUniques):
                self.m_tCumulSupportCroissant.append(0)

        iSupportCumule = 1
        iIndiceValeur = 0
        while iIndiceValeur < self.m_iNombreValeursReellesCorrectes:
            iValeurUniqueSuivante = iValeurUniqueCourante = self.m_tValeursUniques[iIndiceValeur]

            iIndiceValeurSuivante = iIndiceValeur + 1
            while (iValeurUniqueSuivante==iValeurUniqueCourante) and (iIndiceValeurSuivante < self.m_iNombreValeursReellesCorrectes):
                iValeurUniqueSuivante = self.m_tValeursUniques[iIndiceValeurSuivante]
                if iValeurUniqueSuivante == iValeurUniqueCourante:
                    iSupportCumule += 1
                    iIndiceValeurSuivante += 1

            self.m_tCumulSupportCroissant[iValeurUniqueCourante] = iSupportCumule

            iIndiceValeur = iIndiceValeurSuivante
            iSupportCumule += 1


    def ObtenirSupportIntervalle(self, iBorneMin, iBorneMax):
        iIndiceUniqueMin = 0
        iIndiceUniqueMax = 0

        if self.m_tCumulSupportCroissant is None:
            return 0

        if iBorneMin < 0:
            iBorneMin = 0

        if iBorneMax >= self.m_iNombreValeursReellesCorrectes:
            iBorneMax = self.m_iNombreValeursReellesCorrectes - 1

        iIndiceUniqueMin = self.m_tValeursUniques[iBorneMin]
        iIndiceUniqueMax = self.m_tValeursUniques[iBorneMax]

        if iIndiceUniqueMin == 0:
            return self.m_tCumulSupportCroissant[iIndiceUniqueMax]
        else:
            return (self.m_tCumulSupportCroissant[iIndiceUniqueMax] - self.m_tCumulSupportCroissant[iIndiceUniqueMin-1])


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


#*DBF file reader
# 

class DBFReader(object):


    DBF_TYPE_CHAMP_ERRONE = 0
    DBF_TYPE_CHAMP_CARAC = 1
    DBF_TYPE_CHAMP_DATE = 2
    DBF_TYPE_CHAMP_REEL = 3
    DBF_TYPE_CHAMP_DECIMAL = 4
    DBF_TYPE_CHAMP_LOGIQUE = 5
    DBF_TYPE_CHAMP_MEMO = 6

    class DBFChamp(object):
        def __init__(self, outerInstance, sNom, iTypeChamp, iTailleChamp):
            self.m_sNom = None
            self.m_iTypeChamp = DBF_TYPE_CHAMP_ERRONE
            self.m_iTailleChamp = 0

            self.__outerInstance = outerInstance

            self.m_sNom = sNom
            self.m_iTypeChamp = iTypeChamp
            self.m_iTailleChamp = iTailleChamp

        def ObtenirNom(self):
            return self.m_sNom

        def ObtenirType(self):
            return self.m_iTypeChamp

        def ObtenirTaille(self):
            return self.m_iTailleChamp

        #       *isplay column information
        #        
        def AfficherChamp(self):
            sType = None

            print(self.m_sNom + " : ", end = '')

            sType = "type "
            if self.m_iTypeChamp == DBF_TYPE_CHAMP_CARAC:
                sType += "caract�res"
            elif self.m_iTypeChamp == DBF_TYPE_CHAMP_DATE:
                sType += "date"
            elif self.m_iTypeChamp == DBF_TYPE_CHAMP_REEL:
                sType += "flottant"
            elif self.m_iTypeChamp == DBF_TYPE_CHAMP_DECIMAL:
                sType += "d�cimal"
            elif self.m_iTypeChamp == DBF_TYPE_CHAMP_LOGIQUE:
                sType += "bool�en"
            elif self.m_iTypeChamp == DBF_TYPE_CHAMP_MEMO:
                sType += "m�mo"
            else:
                sType += "ind�termin�"
            print(sType, end = '')
            print(", taille ", end = '')
            print(self.m_iTailleChamp)


    def LireValeur32Bits(self, fluxEntree):

        iValeurLue = 0
        iDecalage = 0

        for iDecalage in range(0, 32, 8):
            iValeurLue |= (next(fluxEntree) & 0xff) << iDecalage

        return iValeurLue

    def LireValeur16Bits(self, fluxEntree):

        iValeurLue = 0
        iDecalage = 0

        for iDecalage in range(0, 16, 8):
            iValeurLue |= (next(fluxEntree) & 0xff) << iDecalage

        return iValeurLue

    def IgnorerOctets(self, fluxEntree, iNombreOctets):

        iValeurLue = 0
        iDecalage = 0

        iDecalage = 0
        while iDecalage < iNombreOctets:
            next(fluxEntree)
            iDecalage += 1

    #   *
    #    * This function gets all field information, i.e. number of fields, type, name. It also gets number of records/rows
    #    * This function does not read each row's value
    #    * @param sNomFichier the full name of a file, including path 
    #    
    def __init__(self, sNomFichier):
        self.m_dataInputStream = None
        self.m_iNombreChamps = 0
        self.m_champs = None
        self.m_iTailleEnregistrement = 0
        self.m_iNombreLignes = 0


        bChampsTousLus = False
        bLectureEnTeteCorrecte = False
        octetLu = 0
        tOctetsLus = None
        positionZeroTerminal = 0
        iIndexLettre = 0 # Lettre means letter
        iTypeChamp = DBF_TYPE_CHAMP_ERRONE # ERRONE means error
        sNomChamp = None
        iTailleChamp = 0
        champs = None
        champ = None

        # Structure Informations about DBF file :
        signature = None # 1st byte "database start signal（if database includes DBT file->80H，else->03H）"
        annee = None # 2nd byte  annee means year "file create or modify date（YYMMDD with YY=Date-1900）"
        mois = None # 3rd byte   mois means month
        jour = None # 4th byte   jour means day
        longueurEnTete = None # 9-10 Length of File structure information

        try:
            self.m_dataInputStream = open(sNomFichier)
        except Exception as e:
            print(e)
            self.m_dataInputStream = None

        if self.m_dataInputStream is None:
            return

        try:
            signature = next(self.m_dataInputStream) #Reads one signed input byte. range -128 through 127
            annee = next(self.m_dataInputStream)
            mois = next(self.m_dataInputStream)
            jour = next(self.m_dataInputStream)
            self.m_iNombreLignes = self.LireValeur32Bits(self.m_dataInputStream) #lire means read. number of lines 5-8bytes
            #5-8bytes number of database records，with lower bytes in front and higher bytes after

            longueurEnTete = self.LireValeur16Bits(self.m_dataInputStream)
            print("longueurEnTete " + longueurEnTete)
            self.m_iTailleEnregistrement = int(self.LireValeur16Bits(self.m_dataInputStream)) #11-12bytes　the total length of each record
            print("m_iTailleEnregistrement " + self.m_iTailleEnregistrement)
            # We go to the level of the description of the fields:
            self.IgnorerOctets(self.m_dataInputStream, 20) #13-32bytes　 reserved
        except Exception as e:

            pass
        # End of Structure Informations about DBF file

        champs = []

        bChampsTousLus = False
        while not bChampsTousLus:

            try:
                octetLu = next(self.m_dataInputStream)
                if octetLu ==  0x0d:
                    # l'en-t�te
                    bChampsTousLus = True
                    bLectureEnTeteCorrecte = True
            except Exception as e:
                bChampsTousLus = True
                bLectureEnTeteCorrecte = False

            if not bChampsTousLus:

                try:
                    # Get field's name  1-11 bytes
                    tOctetsLus = [0 for _ in range(11)]
                    self.m_dataInputStream.read(tOctetsLus, 1, 10) #read 10 bytes to tOctetsLus, start at tOctetsLus[1]
                    tOctetsLus[0] = octetLu

                    for iIndexLettre in range(10, -1, -1):
                        if tOctetsLus[iIndexLettre] == 0:
                            positionZeroTerminal = iIndexLettre

                    if positionZeroTerminal > 0:
                        sNomChamp = str(tOctetsLus, 0, positionZeroTerminal)
                    else:
                        sNomChamp = str("")

                    # Get field's type the 12th byte
                    octetLu = next(self.m_dataInputStream)
                    if octetLu ==  0x43:
                        iTypeChamp = DBF_TYPE_CHAMP_CARAC #type is character
                    elif octetLu ==  0x44:
                        iTypeChamp = DBF_TYPE_CHAMP_DATE #type is date
                    elif octetLu ==  0x46:
                        iTypeChamp = DBF_TYPE_CHAMP_REEL #type is float number
                    elif octetLu ==  0x4E:
                        iTypeChamp = DBF_TYPE_CHAMP_DECIMAL #type is decimal
                    elif octetLu ==  0x4C:
                        iTypeChamp = DBF_TYPE_CHAMP_LOGIQUE #type is boolean
                    elif octetLu ==  0x4D:
                        iTypeChamp = DBF_TYPE_CHAMP_MEMO #type is memo??
                    else:
                        iTypeChamp = DBF_TYPE_CHAMP_ERRONE #type is error

                    self.IgnorerOctets(self.m_dataInputStream, 4)

                    # Get the length of the field:
                    iTailleChamp = int(self.m_dataInputStream.readUnsignedByte())

                    self.IgnorerOctets(self.m_dataInputStream, 15)

                    # create a field and put into field list
                    champ = DBFChamp(self, sNomChamp, iTypeChamp, iTailleChamp) #field name, field type and field length
                    champs.append(champ) #add to field list
                except Exception as e:
                    pass


        # End of Structure of Records

        self.m_iNombreChamps = len(champs)
        #System.out.println("m_iNombreChamps before " + m_iNombreChamps)
        if self.m_iNombreChamps > 0:
            self.m_champs =  champs.toArray([None for _ in range(1)]) #return an array with all elements in that vector, the array type is specified
            self.m_iNombreChamps = len(self.m_champs) # pour �tre s�r...
            print("m_iNombreChamps after " + self.m_iNombreChamps)

        else:
            self.m_champs = None

    def close(self):

        if self.m_dataInputStream is None:
            return

        try:
            self.m_dataInputStream.close()
        except Exception as e:
            pass

    def ObtenirNombreChamps(self):
        return self.m_iNombreChamps

    def ObtenirChamp(self, iIndexChamp):
        if iIndexChamp < self.m_iNombreChamps:
            return self.m_champs[iIndexChamp]
        else:
            return None


    #   *Get the index of a column by name
    #    * @param sNomChamp Column name
    #    * @return int
    #    
    def ObtenirIndiceChamp(self, sNomChamp):
        iIndiceChamp = 0
        bChampTrouve = False
        sNomChampEnumere = None

        if sNomChamp is None:
            return -1

        iIndiceChamp = 0
        while ((not bChampTrouve)) and (iIndiceChamp < self.m_iNombreChamps):
            sNomChampEnumere = self.m_champs[iIndiceChamp].ObtenirNom()
            if sNomChamp == sNomChampEnumere:
                bChampTrouve = True
            else:
                iIndiceChamp += 1

        if bChampTrouve:
            return iIndiceChamp
        else:
            return -1

    def ObtenirNombreLignes(self):
        return self.m_iNombreLignes

    def LireEnregistrementSuivant(self):

        octetLu = 0
        tOctetsLus = None
        iIndiceChamp = 0
        iTailleChamp = 0
        iTypeChamp = 0
        tValeursChamps = None
        sChaineLue = None

        if self.m_dataInputStream is None:
            return None

        tValeursChamps = [None for _ in range(self.m_iNombreChamps)]

        try:

            # On ignore les enregistrements marqu�s comme effac�s :
            octetLu = 0x2A
            while octetLu == 0x2A:

                octetLu = next(self.m_dataInputStream)
                if octetLu == 0x2A:
                    self.IgnorerOctets(self.m_dataInputStream, self.m_iTailleEnregistrement - 1)


            # mark the end of that file:
            if octetLu == 0x1A:
                return None

            iIndiceChamp = 0
            while iIndiceChamp < self.m_iNombreChamps:

                iTailleChamp = self.m_champs[iIndiceChamp].ObtenirTaille()
                iTypeChamp = self.m_champs[iIndiceChamp].ObtenirType()

                # Test de correction en cas de fichier mal con�u :
                if iTailleChamp <= 0:
                    if iTypeChamp == DBF_TYPE_CHAMP_DATE:
                        iTailleChamp = 8
                    elif iTypeChamp == DBF_TYPE_CHAMP_LOGIQUE:
                        iTailleChamp = 1
                    else:
                        iTailleChamp = 0

                if iTailleChamp > 0:

                    tOctetsLus = [0 for _ in range(iTailleChamp)]
                    self.m_dataInputStream.read(tOctetsLus)


                    if iTypeChamp == DBF_TYPE_CHAMP_CARAC:
                        tValeursChamps[iIndiceChamp] = str(tOctetsLus)

                    elif iTypeChamp == DBF_TYPE_CHAMP_DATE:
                        tValeursChamps[iIndiceChamp] = str(tOctetsLus)

                    elif iTypeChamp == DBF_TYPE_CHAMP_REEL:
                        tValeursChamps[iIndiceChamp] = (str(tOctetsLus)).trim()


                    elif iTypeChamp == DBF_TYPE_CHAMP_DECIMAL:
                        tValeursChamps[iIndiceChamp] = (str(tOctetsLus)).trim()


                    elif iTypeChamp == DBF_TYPE_CHAMP_LOGIQUE:
                        if tOctetsLus[0] == 0x59 or tOctetsLus[0] == 0x79 or tOctetsLus[0] == 0x54 or tOctetsLus[0] == 0x74: # 'Y', 'y', 'T', 't'
                            tValeursChamps[iIndiceChamp] = str("Vrai") #True
                        else:
                            tValeursChamps[iIndiceChamp] = str("Faux") #False

                    else:
                        tValeursChamps[iIndiceChamp] = str(tOctetsLus)
                else:
                    tValeursChamps[iIndiceChamp] = ""
                iIndiceChamp += 1

        except Exception as e:
            return None
        except Exception as e:
            return None

        return tValeursChamps


