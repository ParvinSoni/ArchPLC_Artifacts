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

DEFAUT_NBITER = 1000
DEFAUT_NBPARALL = 4
    
# Classe r�pertoriant l'ensemble des param�tres d�finis par l'utilisateur pour la prochaine
# ex�cution de l'algorithme de recuit simul�.

class SimulatedAnnealingParameters(object):





    def __init__(self):
        self.m_iNombreIterations = 0
        self.m_iNombreSolutionsParalleles = 0

        self.m_iNombreIterations = DEFAUT_NBITER
        self.m_iNombreSolutionsParalleles = DEFAUT_NBPARALL


    def toString(self):
        sParametres = None

        sParametres = "Selected parameters for the simulated annealing algorithm:" + "\n" + "\n"
        sParametres += "Number of tentatives to improve the rule: " + String.valueOf(self.m_iNombreIterations) + "\n"
        sParametres += "Number of potential rules to test in parallel: " + String.valueOf(self.m_iNombreSolutionsParalleles) + "\n"

        return sParametres

