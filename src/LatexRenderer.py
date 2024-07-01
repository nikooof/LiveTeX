import os
import subprocess
from pathlib import Path
import psutil
import time
from threading import Thread
import pyautogui

class LatexRenderer:
    def __init__(self, editor):
        self.editor = editor
        
    def compileLatex(self, inputName):
        command = f'latexmk -pdf {inputName}'
        subprocess.Popen(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    
    def openPDF(self, fileName):
        if self._pdfViewerExists():
            self.switchPrevApp()
            self.switchPrevApp()
            return
        
        command = ["open"]
        pdfPath = Path(fileName).absolute()
        command.append(str(pdfPath))
        subprocess.Popen(command, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        self.switchPrevApp()

    def _pdfViewerExists(self):
        for proc in psutil.process_iter():
            if proc.name() == "Preview":
                return True
        return False

    def renderDocument(self):
        text = self.editor.text()

        with open("temp.tex", "w") as f:
            f.write(text)

        self.compileLatex("temp.tex")

        delayThread = Thread(target=self.delayedOpen(1.5))
        delayThread.start()

    def delayedOpen(self, seconds):
        time.sleep(seconds)
        self.openPDF("temp.pdf")

    def switchPrevApp(self):
        pyautogui.hotkey('command', 'tab', interval=0.01)