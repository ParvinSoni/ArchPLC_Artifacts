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



class FiltreChoiceFiles(FileFilter):




    def __init__(self, sDescription):
        self.__m_listeExtensions = None
        self.__m_sDescription = None

        self.__m_listeExtensions = []
        if sDescription is not None:
            self.__m_sDescription = str(sDescription)



    def accept(self, fichier):
        sExtension = None

        if fichier is not None:

            if fichier.isDirectory():
                return True

            sExtension = self.ObtenirExtension(fichier)
            if sExtension is not None:
                if sExtension in self.__m_listeExtensions:
                    return True

        return False



    def ObtenirExtension(self, fichier):
        sNomFichier = None
        iIndiceLettre = 0

        if fichier is not None:

            sNomFichier = fichier.getName()
            iIndiceLettre = sNomFichier.rfind('.')

            if (iIndiceLettre>0) and (iIndiceLettre<len(sNomFichier)-1): # On �limine le cas tr�s particulier d'un fichier commen�ant par un '.' (improbable sous Windows)
                return sNomFichier[iIndiceLettre+1:].toLowerCase()

        return None



    def AjouterExtension(self, sExtension):
        iPositionPoint = 0

        if sExtension is not None:

            # On retire un '.' �ventuel devant l'extension proprement dite :
            iPositionPoint = sExtension.rfind('.')
            if iPositionPoint>=0:
                iPositionPoint += 1
            else:
                iPositionPoint = 0

            self.__m_listeExtensions.append(sExtension[iPositionPoint:].toLowerCase())



    # Fontion abstraite surcharg�e :
    def getDescription(self):
        sDescriptionComplete = None
        iNombreExtensions = 0
        iIndiceExtension = 0

        iNombreExtensions = len(self.__m_listeExtensions)

        if iNombreExtensions==0:
            return ""

        if self.__m_sDescription is not None:
            sDescriptionComplete = self.__m_sDescription + " ("
        else:
            sDescriptionComplete = str("(")

        sDescriptionComplete += "." + str(self.__m_listeExtensions[0])

        iIndiceExtension = 1
        while iIndiceExtension<iNombreExtensions:
            sDescriptionComplete += ", ." + str(self.__m_listeExtensions[iIndiceExtension])
            iIndiceExtension += 1

        return sDescriptionComplete + ")"

