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
#---------------------------------------------------------------------------------------------------
#
# Cette classe un peu particuli�re a pour but de stocker diverse informations sur
# l'environnement d'ex�cution, et ainsi de les mettre � disposition des autres classes du programme.
# Tous les membres doivent �tre d�clar�s 'static'.
#
#---------------------------------------------------------------------------------------------------





class ENV(object):

    LOOK_INTERFACE_JAVA = 0
    LOOK_INTERFACE_OS = 1

    REPERTOIRE_TRAVAIL = "./"
    REPERTOIRE_AIDE = "./HELP/"
    REPERTOIRE_RESSOURCES = "./RESOURCES/"
    REPERTOIRE_PROFILS = "./PROFILES/"
    REPERTOIRE_RESULTATS = "./RESULTS/"
    REPERTOIRE_REGLES_QMR = "./RULES_QMR/"
    REPERTOIRE_TABLES_DBF = "./TABLES/"

    VERSION_QUANTMINER = "1.0"
    ANNEE_COPYRIGHT = "2003"
    NOM_UTILISATEUR = "User Unknown"
    LOOK_INTERFACE = LOOK_INTERFACE_JAVA
    AVERTIR_FIN_CALCUL = True
    CHEMIN_FICHIER_SON_FIN_CALCUL = REPERTOIRE_RESSOURCES + "fin_calcul.wav"
    CHEMIN_DERNIERE_BASE_OUVERTE = REPERTOIRE_TABLES_DBF


    @staticmethod
    def Initialiser():

        repertoireCourant = None

        repertoireCourant = File("")
        try:
            REPERTOIRE_TRAVAIL = str(repertoireCourant.getAbsolutePath())
            while REPERTOIRE_TRAVAIL.endswith("."):
                REPERTOIRE_TRAVAIL = REPERTOIRE_TRAVAIL[0:(len(REPERTOIRE_TRAVAIL)-1)]
        except Exception as e:
            REPERTOIRE_TRAVAIL = "./"

        print(REPERTOIRE_TRAVAIL)
        REPERTOIRE_RESSOURCES = REPERTOIRE_TRAVAIL + File.separator + "RESOURCES" + File.separator
        REPERTOIRE_PROFILS = REPERTOIRE_TRAVAIL + File.separator + "PROFILES" + File.separator
        REPERTOIRE_RESULTATS = REPERTOIRE_TRAVAIL + File.separator + "RESULTS" + File.separator
        REPERTOIRE_REGLES_QMR = REPERTOIRE_TRAVAIL + File.separator + "RULES_QMR" + File.separator
        REPERTOIRE_TABLES_DBF = REPERTOIRE_TRAVAIL + File.separator + "TABLES" + File.separator
        REPERTOIRE_AIDE = REPERTOIRE_TRAVAIL + File.separator + "HELP" + File.separator

        CHEMIN_FICHIER_SON_FIN_CALCUL = REPERTOIRE_RESSOURCES + "fin_calcul.wav"
        CHEMIN_DERNIERE_BASE_OUVERTE = REPERTOIRE_TABLES_DBF
        ChargerFichierParametrage()



    @staticmethod
    def EnregistrerFichierParametrage():
        fluxFichier = None
        try:
            fluxFichier = DataOutputStream(FileOutputStream(REPERTOIRE_TRAVAIL + File.separator + "quantminer.ini"))
        except IOException as e:
            print(e.getMessage())
            return

        try:
            fluxFichier.writeUTF(NOM_UTILISATEUR)
            fluxFichier.writeInt(LOOK_INTERFACE)
            fluxFichier.writeBoolean(AVERTIR_FIN_CALCUL)
            fluxFichier.writeUTF(CHEMIN_FICHIER_SON_FIN_CALCUL)
            fluxFichier.writeUTF(CHEMIN_DERNIERE_BASE_OUVERTE)
        except IOException as e:
            print(e.getMessage())

        try:
            fluxFichier.close()
        except IOException as e:
            print(e.getMessage())



    @staticmethod
    def ChargerFichierParametrage():
        fluxFichier = None
        fichierParametrage = None
        sCheminFichier = None

        sCheminFichier = REPERTOIRE_TRAVAIL + File.separator + "quantminer.ini"

        #If the parameter file doens't exist, create a parameter file with value by default:
        fichierParametrage = File(sCheminFichier)
        if not fichierParametrage.exists():
            EnregistrerFichierParametrage()

        try:
            fluxFichier = DataInputStream(FileInputStream(sCheminFichier))
        except IOException as e:
            print(e.getMessage())
            return

        try:
            NOM_UTILISATEUR = fluxFichier.readUTF()
            LOOK_INTERFACE = fluxFichier.readInt()
            AVERTIR_FIN_CALCUL = fluxFichier.readBoolean()
            CHEMIN_FICHIER_SON_FIN_CALCUL = fluxFichier.readUTF()
            CHEMIN_DERNIERE_BASE_OUVERTE = fluxFichier.readUTF()
        except IOException as e:
            pass

        try:
            fluxFichier.close()
        except IOException as e:
            pass


    #obtain date -- used in save a file 
    @staticmethod
    def ObtenirDateCourante():
        dateCourante = None
        sInfoDate = ""

        dateCourante = GregorianCalendar()

        if dateCourante.get(Calendar.MONTH) == 1:
            sInfoDate += "January"
        elif dateCourante.get(Calendar.MONTH) == 2:
            sInfoDate += "February"
        elif dateCourante.get(Calendar.MONTH) == 3:
            sInfoDate += "March"
        elif dateCourante.get(Calendar.MONTH) == 4:
            sInfoDate += "April"
        elif dateCourante.get(Calendar.MONTH) == 5:
            sInfoDate += "May"
        elif dateCourante.get(Calendar.MONTH) == 6:
            sInfoDate += "June"
        elif dateCourante.get(Calendar.MONTH) == 7:
            sInfoDate += "July"
        elif dateCourante.get(Calendar.MONTH) == 8:
            sInfoDate += "August"
        elif dateCourante.get(Calendar.MONTH) == 9:
            sInfoDate += "September"
        elif dateCourante.get(Calendar.MONTH) == 10:
            sInfoDate += "October"
        elif dateCourante.get(Calendar.MONTH) == 11:
            sInfoDate += "November"
        elif dateCourante.get(Calendar.MONTH) == 12:
            sInfoDate += "December"

        sInfoDate += " " + String.valueOf(dateCourante.get(Calendar.DAY_OF_MONTH))
        sInfoDate += ", " + String.valueOf(dateCourante.get(Calendar.YEAR)) + " "
        sInfoDate += " " + String.valueOf(dateCourante.get(Calendar.HOUR_OF_DAY)) + ":"
        sInfoDate += String.valueOf(dateCourante.get(Calendar.MINUTE))

        return sInfoDate

