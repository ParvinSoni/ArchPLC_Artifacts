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

# Classe r�pertoriant l'ensemble des param�tres d�finis par l'utilisateur pour la prochaine
# ex�cution de l'algorithme g�n�tique.

#*Generic algorithm's technique parameters
# 
class ParametersGeneticAlgo(object):
    DEFAUT_TAILLEPOP = 250 #population size
    DEFAUT_NBGEN = 100 ## of generations
    DEFAUT_COEFFCROIS = 0.50 #cross-over rate
    DEFAUT_COEFMUT = 0.40  #mutation rate

    def __init__(self):
        self.m_iTaillePopulation = 0
        self.m_iNombreGenerations = 0
        self.m_fPourcentageCroisement = 0.0
        self.m_fPourcentageMutation = 0.0

        self.m_iTaillePopulation = self.DEFAUT_TAILLEPOP
        self.m_iNombreGenerations = self.DEFAUT_NBGEN
        self.m_fPourcentageCroisement = ParametersGeneticAlgo.DEFAUT_COEFFCROIS
        self.m_fPourcentageMutation = self.DEFAUT_COEFMUT


    def toString(self):
        sParametres = None

        sParametres = "Selected parameters for the genetic algorithm :" + "\n" + "\n"
        sParametres += "Size of the population: " + str(self.m_iTaillePopulation) + "\n"
        sParametres += "Number of generations: " + str(self.m_iNombreGenerations) + "\n"
        sParametres += "Percent cross-over: " + str(self.m_fPourcentageCroisement) + "\n"
        sParametres += "Percent of mutation: " + str(self.m_fPourcentageMutation) + "\n"

        return sParametres

