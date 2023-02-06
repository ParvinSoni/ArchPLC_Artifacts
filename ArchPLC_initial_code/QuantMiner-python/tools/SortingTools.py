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



class SortingTools(object):


    # Class returning an array of strings sorted relative to the contents of an array of integers
    # (At equal integer values, 2 elements are distinguished in alphabetical order):
    @staticmethod
    def CompateurBiTableaux_Chaines_Entiers(tChaines, tEntiers, bTriEntiersCroissants):
        
        tIndices = None # Table of indexes of strings to sort in 'tChains'
        tChainesTriees = None
        iNombreChaines = 0
        iIndiceChaine = 0

        if (tChaines is None) or (tEntiers is None):
            return tChaines

        iNombreChaines = len(tChaines)

        if iNombreChaines == 0:
            return tChaines

        if iNombreChaines != len(tEntiers):
            return tChaines

        tIndices = [None for _ in range(iNombreChaines)]
        iIndiceChaine = 0
        while iIndiceChaine<iNombreChaines:
            tIndices[iIndiceChaine] = iIndiceChaine
            iIndiceChaine += 1

        # Sort the indices by taking into account first the order of the integer array then the alphabetical order of the strings:
        tIndices.sort()

        # We reorder the array of chains according to the new order of the calculated indices:
        tChainesTriees = [None for _ in range(iNombreChaines)]
        iIndiceChaine = 0
        while iIndiceChaine<iNombreChaines:
            tChainesTriees[iIndiceChaine] = tChaines[tIndices[iIndiceChaine]]
            iIndiceChaine += 1

        return tChainesTriees

