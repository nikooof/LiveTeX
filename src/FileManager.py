import os
from pathlib import Path

from PyQt5.Qsci import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class FileManager(QTreeView):
    def __init__(self, tabView, setNewTab=None, mainWindow = None):
        super(FileManager, self).__init__(None)

        self.tabView = tabView
        self.setNewTab = setNewTab
        self.mainWindow = mainWindow

        self.initFileManager()
        self.initFileModel()
        self.initView()

        self.initConnects()

    def initConnects(self):
        self.customContextMenuRequested.connect(self.showContextMenu)
        self.clicked.connect(self.treeViewClicked)

    def initView(self):
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QTreeView.SelectRows)
        self.setEditTriggers(QTreeView.EditTrigger.NoEditTriggers)
        self.setIndentation(10)
        self.setHeaderHidden(True)
        
        for col in range(1, 4):
            self.setColumnHidden(col, True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

    def initFileModel(self):
        self.model = QFileSystemModel()
        self.model.setRootPath(os.getcwd())
        self.model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Files | QDir.Drives)
        self.model.setReadOnly(False)
        self.setModel(self.model)
        self.setRootIndex(self.model.index(os.getcwd()))

    def initFileManager(self):
        self.managerFont = QFont("Arial", 14)
        self.setFont(self.managerFont)
        self.setFocusPolicy(Qt.NoFocus)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def treeViewClicked(self, index: QModelIndex):
        path = self.model.filePath(index)
        p = Path(path)
        if p.is_file():
            self.setNewTab(p)

    def showContextMenu(self, x):
        return
