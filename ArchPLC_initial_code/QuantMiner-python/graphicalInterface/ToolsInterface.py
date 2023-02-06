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


from src.tools import *

class ToolsInterface(object):

    @staticmethod
    def DialogSauvegardeFichier(parent, sCheminDossier, sDescriptionExtension, sExtension):
        fenetreChoixFichier = None
        filtreChoix = None
        iResultatChoixFichier = 0
        fichierChoisi = None
        sFichierChoisi = None
        bFichierCibleOK = False

        fenetreChoixFichier = JFileChooser(sCheminDossier)
        fenetreChoixFichier.setMultiSelectionEnabled(False)
        fenetreChoixFichier.setAcceptAllFileFilterUsed(False)

        filtreChoix = FiltreChoiceFiles(sDescriptionExtension)
        filtreChoix.AjouterExtension(sExtension)
        fenetreChoixFichier.setFileFilter(filtreChoix)

        bFichierCibleOK = False

        iResultatChoixFichier = fenetreChoixFichier.showSaveDialog(parent)
        if iResultatChoixFichier == JFileChooser.APPROVE_OPTION:

            fichierChoisi = fenetreChoixFichier.getSelectedFile()

            if fichierChoisi is not None:
                sFichierChoisi = fichierChoisi.getAbsolutePath()

                # Correction de l'extension si besoin :
                sFichierChoisi = FileTools.AssurerBonneExtension(sFichierChoisi, sExtension)
                fichierChoisi = File(sFichierChoisi)

                if fichierChoisi.exists():
                    bFichierCibleOK = (JOptionPane.showConfirmDialog(parent, "This file exists, do you want to replace it?", "Confirmation replace file.", JOptionPane.YES_NO_OPTION, JOptionPane.WARNING_MESSAGE) == JOptionPane.YES_OPTION)
                else:
                    bFichierCibleOK = True

        if bFichierCibleOK:
            return sFichierChoisi
        else:
            return None

    @staticmethod
    def DialogOuvertureFichier(parent, sCheminDossier, sDescription, sExtention):
        fenetreChoixFichier = None
        filtreChoix = None
        iResultatChoixFichier = 0
        fichierChoisi = None
        sFichierChoisi = None
        bFichierCibleOK = False

        fenetreChoixFichier = JFileChooser(sCheminDossier)
        fenetreChoixFichier.setMultiSelectionEnabled(False)
        fenetreChoixFichier.setAcceptAllFileFilterUsed(False)

        assert(len(sDescription) == len(sDescription))

        i = 0
        while i < len(sDescription):
            filtreChoix = FiltreChoiceFiles(sDescription[i])
            filtreChoix.AjouterExtension(sExtention[i])
            fenetreChoixFichier.addChoosableFileFilter(filtreChoix)
            i += 1


        bFichierCibleOK = False

        iResultatChoixFichier = fenetreChoixFichier.showOpenDialog(parent)
        if iResultatChoixFichier == JFileChooser.APPROVE_OPTION:

            fichierChoisi = fenetreChoixFichier.getSelectedFile()
            if fichierChoisi is not None:
                sFichierChoisi = fichierChoisi.getAbsolutePath()
                bFichierCibleOK = True

        if bFichierCibleOK:
            return sFichierChoisi
        else:
            return None



    # Classe permettant la correction de la saisie dans un JTextField d'un nombre contraint � un intervalle :
    class VerifieurTextFieldIntervalleFloat(InputVerifier):

        def __init__(self, fValeurMin, fValeurMax):
            self.m_fValeurMin = 0.0f
            self.m_fValeurMax = 0.0f

            super().__init__()

            self.m_fValeurMin = fValeurMin
            self.m_fValeurMax = fValeurMax


        def verify(self, input):
            fValeur = 0.0f


            # V�rification de la valeur de support minimal saisie :
            if isinstance(input, JTextField):

                try:
                    fValeur = float((input).getText())
                except NumberFormatException as e:
                    return False

                if fValeur > self.m_fValeurMax:
                    (input).setText(String.valueOf(self.m_fValeurMax))

                if fValeur < self.m_fValeurMin:
                    (input).setText(String.valueOf(self.m_fValeurMin))

                return True

            return True




    @staticmethod
    def JouerSon(sCheminFichierSon):
        fichierSon = None
        audioInputStream = None
        audioFormat = None
        ligne = None
        info = None
        iNombreOctetsLus = 0
        tBuffer = [0 for _ in range(128000)]

        fichierSon = File(sCheminFichierSon)
        try:
            audioInputStream = AudioSystem.getAudioInputStream(fichierSon)
        except Exception as e:
            e.printStackTrace()
            return

        audioFormat = audioInputStream.getFormat()


        info = DataLine.Info(SourceDataLine.class, audioFormat)

        try:
            ligne = AudioSystem.getLine(info)
            ligne.open(audioFormat)
        except LineUnavailableException as e:
            return
        except Exception as e:
            return

        ligne.start()


        while iNombreOctetsLus != -1:

            try:
                iNombreOctetsLus = audioInputStream.read(tBuffer, 0, len(tBuffer))
            except IOException as e:
                iNombreOctetsLus = -1

            if iNombreOctetsLus > 0:
                nBytesWritten = ligne.write(tBuffer, 0, iNombreOctetsLus)


        ligne.drain()

        ligne.close()


