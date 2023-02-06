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



class CelluleCheckButton3StatesEditor(JButton, TableCellEditor):



    def __init__(self):
        self.m_iEtat = 0
        self.iconeCoche = None
        self.iconeNonCoche = None
        self.iconeSemiCoche = None

        self.m_iEtat = 0
        self.iconeCoche = ImageIcon(ENV.REPERTOIRE_RESSOURCES + "case_coche.jpg")
        self.iconeNonCoche = ImageIcon(ENV.REPERTOIRE_RESSOURCES + "case_noncoche.jpg")
        self.iconeSemiCoche = ImageIcon(ENV.REPERTOIRE_RESSOURCES + "case_semicoche.jpg")
        setText("")


    def getTableCellEditorComponent(self, table, value, isSelected, row, column):
        if isSelected:
            setForeground(table.getSelectionForeground())
            super().setBackground(table.getSelectionBackground())
        else:
            setForeground(table.getForeground())
            setBackground(table.getBackground())

        # Select the current value
        self.m_iEtat = int((int(value)))

        if self.m_iEtat == 1:
            setIcon(self.iconeCoche)
        elif self.m_iEtat == 0:
            setIcon(self.iconeNonCoche)
        else:
            setIcon(self.iconeSemiCoche)

        addActionListener(ActionListenerAnonymousInnerClass(self))

        return self

    class ActionListenerAnonymousInnerClass(java.awt.event.ActionListener):

        def __init__(self, outerInstance):
            self.__outerInstance = outerInstance

        def actionPerformed(self, evt):
            outerInstance.__jBouton3EtatsActionPerformed(evt)



    def __jBouton3EtatsActionPerformed(self, evt):
        if self.m_iEtat == 0:
            self.m_iEtat = 1
            setIcon(self.iconeCoche)
        else:
            self.m_iEtat = 0
            setIcon(self.iconeNonCoche)
        self.stopCellEditing()


    def getCellEditorValue(self):
        return Integer(self.m_iEtat)



    def isCellEditable(self, anEvent):
        return True

    def shouldSelectCell(self, anEvent):
        return False


    def stopCellEditing(self):
        self.fireEditingStopped()
        return True


    def cancelCellEditing(self):
        self.fireEditingCanceled()



    def addCellEditorListener(self, l):
        listenerList.add(CellEditorListener.class, l)



    def removeCellEditorListener(self, l):
        listenerList.remove(CellEditorListener.class, l)



    def fireEditingStopped(self):
        # Guaranteed to return a non-null array
        listeners = listenerList.getListenerList()
        # Process the listeners last to first, notifying
        # those that are interested in this event
        for i in range(len(listeners)-2, -1, -2):
            if listeners[i] is CellEditorListener.class:
                (listeners[i+1]).editingStopped(ChangeEvent(self))



    def fireEditingCanceled(self):
        # Guaranteed to return a non-null array
        listeners = listenerList.getListenerList()
        # Process the listeners last to first, notifying
        # those that are interested in this event
        for i in range(len(listeners)-2, -1, -2):
            if listeners[i] is CellEditorListener.class:
                (listeners[i+1]).editingCanceled(ChangeEvent(self))





