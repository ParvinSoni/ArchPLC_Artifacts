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


class JSplashWindow(JWindow):


    def __init__(self, duration, path):
        self.__m_duration = 0
        self.__m_path = None

        self.__m_duration = duration
        self.__m_path = path

    def showSplash(self):
        content = getContentPane()
        content.setBackground(Color.white)

        width = 785
        height =514
        screen = Toolkit.getDefaultToolkit().getScreenSize()
        x = (screen.width-width)/2
        y = (screen.height-height)/2
        setBounds(x,y,width,height)

        # Build the splash screen
        label = JLabel(ImageIcon(self.__m_path + java.io.File.separator + "QuantMiner.png"))
        content.add(label, BorderLayout.CENTER)
        setVisible(True)

        try:
            Thread.sleep(self.__m_duration)
        except Exception as e:
            pass
        setVisible(False)

