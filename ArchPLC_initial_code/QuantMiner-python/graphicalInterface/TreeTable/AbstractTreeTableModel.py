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

from graphicalInterface.TreeTable.TreeTableModel import TreeTableModel


class AbstractTreeTableModel(TreeTableModel):
    def __init__(self, root):
        root = None
        self.listenerList = None

        self.root = root
        # self.listenerList = EventListenerList()


    def getRoot(self):
        return self.root


    def isLeaf(self, node):
        return getChildCount(node) == 0


    def valueForPathChanged(self, path, newValue):
        pass


    def getIndexOfChild(self, parent, child):

        i = 0
        while i < getChildCount(parent):
            if getChild(parent, i) is child:
                return i
            i += 1

        return -1



    def addTreeModelListener(self, l):
        self.listenerList.add(TreeModelListener, l)


    def removeTreeModelListener(self, l):
        self.listenerList.remove(TreeModelListener, l)


    def fireTreeNodesChanged(self, source, path, childIndices, children):

        listeners = self.listenerList.getListenerList()
        e = None

        for i in range(len(listeners)-2, -1, -2):
            if listeners[i] is TreeModelListener:
                if e is None:
                    e = TreeModelEvent(source, path, childIndices, children)
                (listeners[i+1]).treeNodesChanged(e)


    def fireTreeNodesInserted(self, source, path, childIndices, children):

        listeners = self.listenerList.getListenerList()
        e = None

        for i in range(len(listeners)-2, -1, -2):
            if listeners[i] is TreeModelListener:
                if e is None:
                    e = TreeModelEvent(source, path, childIndices, children)
                (listeners[i+1]).treeNodesInserted(e)


    def fireTreeNodesRemoved(self, source, path, childIndices, children):

        listeners = self.listenerList.getListenerList()
        e = None

        for i in range(len(listeners)-2, -1, -2):
            if listeners[i] is TreeModelListener:
                if e is None:
                    e = TreeModelEvent(source, path, childIndices, children)
                (listeners[i+1]).treeNodesRemoved(e)


    def fireTreeStructureChanged(self, source, path, childIndices, children):

        listeners = self.listenerList.getListenerList()
        e = None

        for i in range(len(listeners)-2, -1, -2):
            if listeners[i] is TreeModelListener:
                if e is None:
                    e = TreeModelEvent(source, path, childIndices, children)
                (listeners[i+1]).treeStructureChanged(e)



    def getColumnClass(self, column):
        return Object



    def isCellEditable(self, node, column):
        return self.getColumnClass(column) is TreeTableModel



    def setValueAt(self, aValue, node, column):
        pass



    def getCellRenderer(self, node, column):
        return None # Renderer par d�faut


    # A implanter dans la sous-classe :
    #     
    #     *   public Object getChild(Object parent, int index)
    #     *   public int getChildCount(Object parent) 
    #     *   public int getColumnCount() 
    #     *   public String getColumnName(Object node, int column)  
    #     *   public Object getValueAt(Object node, int column) 
    #     

