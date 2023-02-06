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





class TreeTableModelAdapter(AbstractTableModel):



    def __init__(self, treeTableModel, tree):
        self.m_tree = None
        self.m_treeTableModel = None

        self.m_tree = tree
        self.m_treeTableModel = treeTableModel

        self.m_tree.addTreeExpansionListener(TreeExpansionListenerAnonymousInnerClass(self))

    class TreeExpansionListenerAnonymousInnerClass(TreeExpansionListener):

        def __init__(self, outerInstance):
            self.__outerInstance = outerInstance

        def treeExpanded(self, event):
            fireTableDataChanged()
        def treeCollapsed(self, event):
            fireTableDataChanged()



    def getColumnCount(self):
        return self.m_treeTableModel.getColumnCount()



    def getColumnName(self, column):
        return self.m_treeTableModel.getColumnName(column)



    def getColumnClass(self, column):
        return self.m_treeTableModel.getColumnClass(column)



    def getRowCount(self):
        return self.m_tree.getRowCount()



    def nodeForRow(self, row):
        treePath = self.m_tree.getPathForRow(row)
        return treePath.getLastPathComponent()



    def getValueAt(self, row, column):
        return self.m_treeTableModel.getValueAt(self.nodeForRow(row), column)



    def isCellEditable(self, row, column):
        return self.m_treeTableModel.isCellEditable(self.nodeForRow(row), column)



    def setValueAt(self, value, row, column):
        self.m_treeTableModel.setValueAt(value, self.nodeForRow(row), column)


