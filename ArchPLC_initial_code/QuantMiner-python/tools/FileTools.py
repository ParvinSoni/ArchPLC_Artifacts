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


class FileTools(object):


    @staticmethod
    def ObtenirCheminSansExtension(sCheminFichier):
        iPositionExtension = 0

        if sCheminFichier is None:
            return None

        iPositionExtension = sCheminFichier.rfind('.')

        if iPositionExtension<0:
            return sCheminFichier

        return sCheminFichier[0:iPositionExtension]



    @staticmethod
    def AssurerBonneExtension(sCheminFichier, sExtension):
        sNomFichierEnMinuscules = None
        sExtensionEnMinuscules = None

        if (sCheminFichier is None) or (sExtension is None):
            return None

        sNomFichierEnMinuscules = (sCheminFichier.trim()).toLowerCase()
        sExtensionEnMinuscules = "." + sExtension.casefold()

        if sNomFichierEnMinuscules.endswith(sExtensionEnMinuscules):
            return sCheminFichier
        else:
            return (ObtenirCheminSansExtension(sCheminFichier) + "." + sExtension)


