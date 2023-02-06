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

class WordList(object):
    t_index = 0

    class InfosMot(object):

        def __init__(self, outerInstance, iIdentifiantUnique):
            self.m_iIdentifiantUnique = 0
            self.m_iOccurrences = 0

            self.__outerInstance = outerInstance

            self.m_iIdentifiantUnique = iIdentifiantUnique
            self.m_iOccurrences = 1

    def __init__(self):
        self.m_tableMots = None
        self.m_iNombreMots = 0
        self.m_sChaineParcours = None
        self.m_bParcoursInicie = False
        self.m_enumerationMotsParcourus = None

        self.m_tableMots = {}
        self.m_iNombreMots = 0

        self.m_sChaineParcours = None
        self.m_bParcoursInicie = False
        self.m_enumerationMotsParcourus = None



    def ObtenirNombreMots(self):
        return self.m_iNombreMots

    #    *Return the position of the word in String
    #     * @param sChaine String
    #     * @return position
    #     
    def InsererMot(self, sChaine):
        iIdentificateurChaine = 0
        infosMot = None

        if sChaine is None:
            return -1

        if sChaine in self.m_tableMots.keys():
            infosMot = self.m_tableMots[sChaine]

        # Case where the chain is already listed:
        if infosMot is not None:
            infosMot.m_iOccurrences += 1
            iIdentificateurChaine = infosMot.m_iIdentifiantUnique
        else:# Case where it is not listed, in this case we add it:
            infosMot = WordList.InfosMot(self, self.m_iNombreMots)
            self.m_tableMots.update({sChaine: infosMot})
            # print(self.m_tableMots)
            iIdentificateurChaine = self.m_iNombreMots #Position in Chain
            self.m_iNombreMots += 1 #number of words increase by one

        return iIdentificateurChaine



    def EstDansListe(self, sChaine):
        if sChaine is None:
            return False
        else:
            return sChaine in self.m_tableMots.keys()



    # Retrieve the information stored for a given word in the list:
    def ChercherInfosMot(self, sChaine):
        if sChaine is None:
            return None
        else:
            return self.m_tableMots[sChaine] #Returns the value to which the specified key is mapped in this hashtable.



    def InicierParcours(self):
        self.m_bParcoursInicie = True
        self.m_sChaineParcours = None
        self.m_enumerationMotsParcourus = list(self.m_tableMots.keys()) #Returns an enumeration of the keys in this hashtable.
        self.t_index = 0
        # print("self.m_enumerationMotsParcourus: " + str(self.m_enumerationMotsParcourus))



    def AvancerParcours(self):
        if ((not self.m_bParcoursInicie)) or (self.m_enumerationMotsParcourus is None):
            return False
        
        # print(self.m_enumerationMotsParcourus)
        # print(self.m_tableMots)
        # if self.m_enumerationMotsParcourus.hasMoreElements(): #Tests if this enumeration contains more elements.
        if len(self.m_enumerationMotsParcourus) > 0 and self.t_index < len(self.m_enumerationMotsParcourus):
            self.m_sChaineParcours = self.m_enumerationMotsParcourus[self.t_index]
            # print(self.m_sChaineParcours)
            self.t_index += 1
            # print(self.t_index)
        else:
            self.m_enumerationMotsParcourus = None
            self.m_sChaineParcours = None
            self.m_bParcoursInicie = False

        return self.m_bParcoursInicie


    def ObtenirMotParcouru(self):
        if self.m_bParcoursInicie:
            return self.m_sChaineParcours
        else:
            return None


    def ObtenirInfosMotParcouru(self):
        if (self.m_bParcoursInicie) and (self.m_sChaineParcours is not None):
            return self.ChercherInfosMot(self.m_sChaineParcours)
        else:
            return None

