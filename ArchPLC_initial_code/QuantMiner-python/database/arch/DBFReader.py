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

        #		*isplay column information
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

    #	*
    #	 * This function gets all field information, i.e. number of fields, type, name. It also gets number of records/rows
    #	 * This function does not read each row's value
    #	 * @param sNomFichier the full name of a file, including path 
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


    #	*Get the index of a column by name
    #	 * @param sNomChamp Column name
    #	 * @return int
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

