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





class AbstractCellEditor(CellEditor):

    def __init__(self):
        self.listenerList = EventListenerList()




    def getCellEditorValue(self):
        return None
    def isCellEditable(self, anEvent):
        return True
    def shouldSelectCell(self, anEvent):
        return False
    def stopCellEditing(self):
        return True
    def cancelCellEditing(self):
        pass



    def addCellEditorListener(self, l):
        self.listenerList.add(CellEditorListener.class, l)



    def removeCellEditorListener(self, l):
        self.listenerList.remove(CellEditorListener.class, l)



    def fireEditingStopped(self):
        # Guaranteed to return a non-null array
        listeners = self.listenerList.getListenerList()
        # Process the listeners last to first, notifying
        # those that are interested in this event
        for i in range(len(listeners)-2, -1, -2):
            if listeners[i] is CellEditorListener.class:
                (listeners[i+1]).editingStopped(ChangeEvent(self))



    def fireEditingCanceled(self):
        # Guaranteed to return a non-null array
        listeners = self.listenerList.getListenerList()
        # Process the listeners last to first, notifying
        # those that are interested in this event
        for i in range(len(listeners)-2, -1, -2):
            if listeners[i] is CellEditorListener.class:
                (listeners[i+1]).editingCanceled(ChangeEvent(self))


