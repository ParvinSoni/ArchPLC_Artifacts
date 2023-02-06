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




class JTreeTable(JTable):




    #***********************
    # TreeTableCellRenderer 
    #***********************

    class TreeTableCellRenderer(JTree, TableCellRenderer):




        def __init__(self, outerInstance, treeModel):

            self.visibleRow = 0

            super().__init__(treeModel)
            self.__outerInstance = outerInstance



        def updateUI(self):

            super().updateUI()
            tcr = super().getCellRenderer()
            if isinstance(tcr, DefaultTreeCellRenderer):
                dtcr = (tcr)
                dtcr.setTextSelectionColor(UIManager.getColor("Table.selectionForeground"))
                dtcr.setBackgroundSelectionColor(UIManager.getColor("Table.selectionBackground"))



        def setRowHeight(self, rowHeight):
            if rowHeight > 0:
                super().setRowHeight(rowHeight)
                if (outerInstance is not None) and (self.__outerInstance.getRowHeight()!=rowHeight):
                    self.__outerInstance.setRowHeight(getRowHeight())



        def setBounds(self, x, y, w, h):
            super().setBounds(x, 0, w, self.__outerInstance.getHeight())



        def paint(self, g):
            g.translate(0, -self.visibleRow * getRowHeight())
            super().paint(g)



        def getTableCellRendererComponent(self, table, value, isSelected, hasFocus, row, column):
            if isSelected:
                setBackground(table.getSelectionBackground())
            else:
                setBackground(table.getBackground())

            self.visibleRow = row
            return self




    #*********************
    # TreeTableCellEditor 
    #*********************

    class TreeTableCellEditor(AbstractCellEditor, TableCellEditor):

        def __init__(self, outerInstance):
            self.__outerInstance = outerInstance


        def getTableCellEditorComponent(self, table, value, isSelected, r, c):
            return outerInstance.m_treeRenderer



        def isCellEditable(self, e):

            if isinstance(e, MouseEvent):
                for counter in range(getColumnCount() - 1, -1, -1):
                    if getColumnClass(counter) == TreeTableModel.class:
                        me = e
                        newME = MouseEvent(outerInstance.m_treeRenderer, me.getID(), me.getWhen(), me.getModifiers(), me.getX() - getCellRect(0, counter, True).x, me.getY(), me.getClickCount(), me.isPopupTrigger())
                        outerInstance.m_treeRenderer.dispatchEvent(newME)
                        break

            return False





    #*********************************
    # ListToTreeSelectionModelWrapper 
    #*********************************

    class ListToTreeSelectionModelWrapper(DefaultTreeSelectionModel):



        def __init__(self, outerInstance):
            self.updatingListSelectionModel = False

            super().__init__()
            self.__outerInstance = outerInstance

            self.getListSelectionModel().addListSelectionListener(self.createListSelectionListener())



        def getListSelectionModel(self):
            return listSelectionModel



        def resetRowSelection(self):
            if not self.updatingListSelectionModel:
                self.updatingListSelectionModel = True
                try:
                    super().resetRowSelection()
                finally:
                    self.updatingListSelectionModel = False



        def createListSelectionListener(self):
            return ListSelectionHandler(self)



        def updateSelectedPathsFromSelectedRows(self):
            if not self.updatingListSelectionModel:
                self.updatingListSelectionModel = True
                try:
                    min = listSelectionModel.getMinSelectionIndex()
                    max = listSelectionModel.getMaxSelectionIndex()

                    clearSelection()
                    if min != -1 and max != -1:
                        counter = min
                        while counter <= max:
                            if listSelectionModel.isSelectedIndex(counter):
                                selPath = outerInstance.m_treeRenderer.getPathForRow(counter)

                                if selPath is not None:
                                    addSelectionPath(selPath)
                            counter += 1
                finally:
                    self.updatingListSelectionModel = False



        class ListSelectionHandler(ListSelectionListener):

            def __init__(self, outerInstance):
                self.__outerInstance = outerInstance

            def valueChanged(self, e):
                outerInstance.updateSelectedPathsFromSelectedRows()





    def __init__(self, treeTableModel):
        self.m_treeRenderer = None
        self.m_treeTableModel = None


        super().__init__()

        self.m_treeRenderer = TreeTableCellRenderer(self, treeTableModel)

        self.m_treeTableModel = treeTableModel
        super().setModel(TreeTableModelAdapter(treeTableModel, self.m_treeRenderer))

        selectionWrapper = ListToTreeSelectionModelWrapper(self)
        self.m_treeRenderer.setSelectionModel(selectionWrapper)
        setSelectionModel(selectionWrapper.getListSelectionModel())

        self.m_treeRenderer.setRootVisible(False)

        setDefaultRenderer(TreeTableModel.class, self.m_treeRenderer)
        setDefaultEditor(TreeTableModel.class, TreeTableCellEditor(self))

        setShowGrid(True)
        setIntercellSpacing(Dimension(1, 1))

        self.setRowHeight(22)




    def updateUI(self):
        super().updateUI()
        if self.m_treeRenderer is not None:
            self.m_treeRenderer.updateUI()

        LookAndFeel.installColorsAndFont(self, "Tree.background", "Tree.foreground", "Tree.font")



    def getEditingRow(self):
        return -1 if (getColumnClass(editingColumn) == TreeTableModel.class) else editingRow



    def setRowHeight(self, rowHeight):
        super().setRowHeight(rowHeight)
        if (m_treeRenderer is not None) and (self.m_treeRenderer.getRowHeight()!=rowHeight):
            self.m_treeRenderer.setRowHeight(getRowHeight())



    def getTree(self):
        return self.m_treeRenderer



    def getCellRenderer(self, row, column):
        treePath = None
        renderer = None

        renderer = None
        if self.m_treeTableModel is not None:
            treePath = self.m_treeRenderer.getPathForRow(row)
            if treePath is not None:
                renderer = self.m_treeTableModel.getCellRenderer(treePath.getLastPathComponent(), column)

        if renderer is not None:
            return renderer
        else:
            return super().getCellRenderer(row, column)

