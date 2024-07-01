import os
from pathlib import Path
import subprocess

from PyQt5.Qsci import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer

from Editor import Editor
from FileManager import FileManager

class EditorGUI(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        self.sideBarColor = "#141221"
        self.currentFile = None
        self.autoSaveTimerInterval = 60 #sec

        self.initUI()
        self.initAutoSaveTimer()

    def initAutoSaveTimer(self):
        self.autoSaveTimer = QTimer(self)
        self.autoSaveTimer.timeout.connect(self.autoSave)
        self.autoSaveTimer.start(self.autoSaveTimerInterval*1000)

    def autoSave(self):
        editor = self.tabView.currentWidget()
        if editor:
            self.saveAndRender()

    def getEditor(self) -> QsciScintilla:
        return Editor()

    def isBinary(self, path):
        with open(path, 'rb') as f:
            return b'\0' in f.read(1024)
    
    def setNewTab(self, path, isNewFile = False):
        editor = self.getEditor()

        if isNewFile:
            self._addNewTab(editor, "untitled")
            return
        
        if not path.is_file() or self.isBinary(path):
            return
        
        if self.isBinary(path):
            self.statusBar().showMessage("Cannot open Binary File", 2000)
            return

        if self._activateExistingTab(path):
            return
    
        self._addNewTab(editor, path.name)
        editor.setText(path.read_text())
        self.setWindowTitle(path.name)
        self.currentFile = path
        self.statusBar().showMessage(f"Opened {path.name}", 2000)

    def _activateExistingTab(self, path):
        for i in range(self.tabView.count()):
            if self.tabView.tabText(i) == path.name:
                self.tabView.setCurrentIndex(i)
                self.currentFile = path
                return True
        return False

    def _addNewTab(self, editor, title):
        self.tabView.addTab(editor, title)
        self.setWindowTitle(title)
        self.statusBar().showMessage(f"Opened {title}")
        self.tabView.setCurrentIndex(self.tabView.count() - 1)
        self.currentFile = None

    def initUI(self):
        self.setWindowTitle("LiveTeX")
        self.resize(1300, 900)
        self.setStyleSheet(open("css/style.qss", 'r').read())

        self.windowFont = QFont("Arial")
        self.windowFont.setPointSize(16)
        self.setFont(self.windowFont)

        self.initMenu()
        self.initBody()
        self.initStatusBar()
        self.show()

    def initStatusBar(self):
        statusBar = QStatusBar(self)
        statusBar.setStyleSheet('''
                                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                      stop:0 #141221, stop:1 #1e1d2f);
                                color: #4fcdb9;
                                ''')
        statusBar.showMessage("Ready", 3000)
        self.setStatusBar(statusBar)

    def initMenu(self):
        menuBar = self.menuBar()

        fileMenu = menuBar.addMenu("File")
        fileMenu.addAction("New File", self.newFile, "Ctrl+N")
        fileMenu.addAction("Open File", self.openFile, "Ctrl+O")
        fileMenu.addAction("Open Folder", self.openFolder, "Ctrl+Shift+O")
        fileMenu.addAction("Save File", self.saveAndRender, "Ctrl+S")
        fileMenu.addAction("Render File", self.renderFile, "Ctrl+R")
        fileMenu.addSeparator()

        editMenu = menuBar.addMenu("Edit")
        editMenu.addAction("Copy", self.copy, "Ctrl+C")
        editMenu.addAction("Paste", self.paste, "Ctrl+V")

    def initSideBarLabel(self, path, name):
        label = QLabel()
        label.setPixmap(QPixmap(path).scaled(QSize(30, 30)))
        label.setAlignment(Qt.AlignmentFlag.AlignTop)
        label.setFont(self.windowFont)
        label.mousePressEvent = lambda e: self.showHideTab(e, name)
        return label
    
    def getFrame(self):
        frame = QFrame()
        frame.setLineWidth(1)
        frame.setContentsMargins(0, 0, 0, 0)
        return frame

    def initBody(self):
        bodyFrame = QFrame()
        bodyFrame.setFrameShape(QFrame.NoFrame)
        bodyFrame.setContentsMargins(0, 0, 0, 0)
        bodyFrame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        bodyLayout = QHBoxLayout()
        bodyLayout.setContentsMargins(0, 0, 0, 0)
        bodyLayout.setSpacing(0)
        bodyFrame.setLayout(bodyLayout)

        self.tabView = QTabWidget()
        self.tabView.setTabsClosable(True)
        self.tabView.setMovable(True)
        self.tabView.setDocumentMode(True)
        self.tabView.tabCloseRequested.connect(self.closeTab)

        self.sideBarFrame = self._createSideBar()
        bodyLayout.addWidget(self.sideBarFrame)

        self.hsplit = QSplitter(Qt.Horizontal)
        self.fileManagerFrame = self._createFileManagerFrame()
        
        self.hsplit.addWidget(self.fileManagerFrame)
        self.hsplit.addWidget(self.tabView)

        bodyLayout.addWidget(self.hsplit)

        bodyFrame.setLayout(bodyLayout)
        self.setCentralWidget(bodyFrame)
        

    def _createFileManagerFrame(self):
        fileManagerFrame = self.getFrame()
        fileManagerFrame.setMaximumSize(200, 1300)
        fileManagerFrame.setStyleSheet('''background-color: #141221; border: none;''')

        fileManagerLayout = QVBoxLayout()
        fileManagerLayout.setSpacing(0)
        fileManagerFrame.setLayout(fileManagerLayout)
        
        self.model = QFileSystemModel()
        self.model.setRootPath(os.getcwd())
        self.model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Files)

        self.fileManager = FileManager(tabView=self.tabView, setNewTab=self.setNewTab, mainWindow=self)
       
        fileManagerLayout.addWidget(self.fileManager)

        return fileManagerFrame
    def _createSideBar(self):
        sideBarFrame = QFrame()
        sideBarFrame.setStyleSheet(f"background-color: {self.sideBarColor};")

        sideBarLayout = QVBoxLayout()
        sideBarLayout.setContentsMargins(15, 10, 5, 0)
        sideBarLayout.setSpacing(15)
        sideBarLayout.setAlignment(Qt.AlignTop or Qt.AlignCenter)
        sideBarFrame.setLayout(sideBarLayout)

        folderLabel = self.initSideBarLabel("icons/folder_icon.svg", "folderIcon")
        sideBarLayout.addWidget(folderLabel)

        return sideBarFrame
    
    def closeTab(self, index):
        self.tabView.removeTab(index)

    def showHideTab(self, e, type):
        if type == 'folderIcon':
            if self.fileManagerFrame.isHidden():
                self.fileManagerFrame.show()
            else:
                self.fileManagerFrame.hide()

    def treeViewClicked(self, index: QModelIndex):
        path = Path(self.model.filePath(index))
        self.setNewTab(path)

    def newFile(self):
        self.setNewTab(None, isNewFile=True)

    def saveFile(self):
        if self.currentFile is None and self.tabView.count() > 0:
            self.save_as()
        
        editor = self.tabView.currentWidget()
        self.currentFile.write_text(editor.text())
        self.statusBar().showMessage(f"Saved {self.currentFile.name}", 2000)

    def save_as(self):
        editor = self.tabView.currentWidget()
        if editor is None:
            return

        filePath = QFileDialog.getSaveFileName(self, "Save As", os.getcwd())[0]

        if filePath:
            path = Path(filePath)
            path.write_text(editor.text())
            self.tabView.setTabText(self.tabView.currentIndex(), path.name)
            self.statusBar().showMessage(f"Saved {path.name}", 2000)
            self.currentFile = path

    def openFile(self):
        newFile, _ = QFileDialog.getOpenFileName(self,
                    "Pick A File", "" "All Files (*);;Tex Files (*.tex)")
        
        if newFile == '':
            self.statusBar().showMessage("Cancelled", 2000)
            return
        
        f = Path(newFile)
        self.setNewTab(f)

    def openFolder(self):
        newFolder = QFileDialog.getExistingDirectory(self, "Pick A Folder", "")
        if newFolder:
            self.model.setRootPath(newFolder)
            self.fileManager.setRootIndex(self.model.index(newFolder))
            self.statusBar().showMessage(f"Opened {newFolder}", 2000)

    def copy(self):
        editor = self.tabView.currentWidget()
        if editor:
            editor.copy()

    def paste(self):
        editor = self.tabView.currentWidget()
        if editor:
            editor.paste()

    def renderFile(self):
        editor = self.tabView.currentWidget()
        if editor: 
            editor.renderPDFfile()
        return
    
    def saveAndRender(self):
        self.saveFile()
        self.renderFile()

    def delExtraFiles(self):
        command = 'latexmk -c'
        subprocess.run(command, shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

    def rename_pdf(self):
        try:
            os.rename("temp.pdf", "texPDF.pdf")
        except:
            return

    def cleanup(self):
        self.delExtraFiles()
        self.rename_pdf()
        try:
            os.remove("temp.tex")
        except:
            return