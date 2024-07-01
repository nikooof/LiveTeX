import sys
import atexit

from PyQt5.QtWidgets import QApplication

from EditorGUI import EditorGUI

def main():
    app = QApplication([])
    window = EditorGUI()
    atexit.register(window.cleanup)
    sys.exit(app.exec())

if __name__ == '__main__':
    main()