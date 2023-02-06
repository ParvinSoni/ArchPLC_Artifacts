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

